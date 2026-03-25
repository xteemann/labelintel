#!/usr/bin/env python3
"""
LabelIntel — Breakout Scoring Engine
=====================================
Pulls latest artist data from Supabase and scores each artist on their
breakout probability (0–100) using a weighted multi-factor model.

Scoring Weights:
    - Streaming velocity (30d growth rate)    × 0.35
    - Playlist momentum (7d playlist adds)    × 0.25
    - Social signals (TikTok/social score)    × 0.20
    - Organic ratio (follower:listener)       × 0.10
    - Consistency (release frequency/steady)  × 0.10

Usage:
    python scoring.py                  # Score all artists
    python scoring.py --top 50         # Score and display top 50
    python scoring.py --dry-run        # Score without saving to DB

Designed to run daily after spotify_scanner.py completes.
"""

import os
import sys
import math
import logging
from datetime import datetime, timezone
from typing import Optional

from dotenv import load_dotenv
from supabase import create_client, Client

# ── Configuration ────────────────────────────────────────────────
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', os.environ.get('SUPABASE_ANON_KEY', ''))

# Scoring weights (must sum to 1.0)
WEIGHTS = {
    'streaming_velocity': 0.35,
    'playlist_momentum': 0.25,
    'social_signals': 0.20,
    'organic_ratio': 0.10,
    'consistency': 0.10,
}

# ── Logging ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
log = logging.getLogger('labelintel.scoring')


def init_supabase() -> Client:
    """Initialize Supabase client."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        log.error('Missing SUPABASE_URL or SUPABASE_KEY')
        sys.exit(1)
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def sigmoid_normalize(value: float, midpoint: float, steepness: float = 1.0) -> float:
    """Normalize a value to 0–100 using a sigmoid curve.

    This prevents extreme outliers from dominating scores while still
    rewarding high values. midpoint = value that maps to 50.
    """
    try:
        x = steepness * (value - midpoint) / max(midpoint, 1)
        return 100 / (1 + math.exp(-x))
    except (OverflowError, ZeroDivisionError):
        return 50.0


def score_streaming_velocity(velocity_30d: float) -> float:
    """Score the 30-day monthly listener growth rate.

    Exceptional growth (>200%) = 90+
    Strong growth (>100%) = 70-90
    Moderate growth (>50%) = 50-70
    Low growth (<50%) = <50
    """
    if velocity_30d <= 0:
        return max(0, 10 + velocity_30d * 0.1)  # Negative growth = low score

    return sigmoid_normalize(velocity_30d, midpoint=100, steepness=2.0)


def score_playlist_momentum(playlist_adds_7d: int, total_playlists: int) -> float:
    """Score playlist addition velocity.

    High playlist adds relative to total = strong momentum signal.
    """
    if total_playlists == 0 and playlist_adds_7d == 0:
        return 20.0  # No data

    # Raw momentum based on absolute adds
    raw_adds = sigmoid_normalize(playlist_adds_7d, midpoint=20, steepness=1.5)

    # Ratio of new adds to total (higher ratio = faster growing)
    if total_playlists > 0:
        ratio = (playlist_adds_7d / total_playlists) * 100
        ratio_score = sigmoid_normalize(ratio, midpoint=10, steepness=1.5)
    else:
        ratio_score = raw_adds

    return 0.6 * raw_adds + 0.4 * ratio_score


def score_social_signals(social_score: float) -> float:
    """Score social media signals (TikTok sounds, mentions, etc.).

    This is a composite score from external social data.
    0 = no data, 100 = viral social presence.
    """
    if social_score <= 0:
        return 15.0  # No social data yet (placeholder)

    return sigmoid_normalize(social_score, midpoint=50, steepness=1.0)


def score_organic_ratio(followers: int, monthly_listeners: int) -> float:
    """Score the follower-to-listener ratio.

    High ratio (>0.3) = highly organic, fans convert to followers
    Medium ratio (0.1-0.3) = healthy balance
    Low ratio (<0.05) = playlist-driven, not building a real fanbase
    """
    if monthly_listeners == 0:
        return 30.0  # No data

    ratio = followers / monthly_listeners

    if ratio > 1.0:
        ratio = 1.0  # Cap at 1:1

    # Optimal range is 0.15–0.5
    return sigmoid_normalize(ratio * 100, midpoint=20, steepness=1.2)


def score_consistency(scan_history: list[dict]) -> float:
    """Score release/activity consistency based on scan history.

    More scan entries with positive growth = consistent upward trajectory.
    Erratic or declining = lower score.
    """
    if not scan_history or len(scan_history) < 2:
        return 40.0  # Not enough history

    # Calculate trend direction across scans
    listeners = [s.get('monthly_listeners', 0) for s in scan_history]
    positive_changes = 0
    total_changes = 0

    for i in range(1, len(listeners)):
        if listeners[i] > listeners[i - 1]:
            positive_changes += 1
        total_changes += 1

    if total_changes == 0:
        return 40.0

    consistency_pct = (positive_changes / total_changes) * 100
    return sigmoid_normalize(consistency_pct, midpoint=50, steepness=1.5)


def calculate_breakout_score(
    artist: dict,
    scan_history: list[dict],
) -> float:
    """Calculate the composite breakout score for an artist.

    Returns a score from 0–100.
    """
    # Individual dimension scores
    velocity = score_streaming_velocity(artist.get('listener_velocity_30d', 0))
    playlist = score_playlist_momentum(
        artist.get('playlist_adds_7d', 0),
        artist.get('total_playlists', 0),
    )
    social = score_social_signals(artist.get('social_signal_score', 0))
    organic = score_organic_ratio(
        artist.get('followers', 0),
        artist.get('monthly_listeners', 0),
    )
    consistency = score_consistency(scan_history)

    # Weighted composite score
    composite = (
        velocity * WEIGHTS['streaming_velocity']
        + playlist * WEIGHTS['playlist_momentum']
        + social * WEIGHTS['social_signals']
        + organic * WEIGHTS['organic_ratio']
        + consistency * WEIGHTS['consistency']
    )

    # Clamp to 0–100
    return round(min(100, max(0, composite)), 1)


def get_scan_history(db: Client, artist_id: str, limit: int = 14) -> list[dict]:
    """Fetch recent scan history for an artist."""
    try:
        result = (
            db.table('scan_history')
            .select('*')
            .eq('artist_id', artist_id)
            .order('scanned_at', desc=True)
            .limit(limit)
            .execute()
        )
        return list(reversed(result.data or []))  # Chronological order
    except Exception:
        return []


def run_scoring(top_n: int = 50, dry_run: bool = False) -> list[dict]:
    """Score all artists and return the top N."""
    log.info('═' * 60)
    log.info('LabelIntel Scoring Engine — Starting')
    log.info(f'Weights: {WEIGHTS}')
    log.info('═' * 60)

    db = init_supabase()

    # Fetch all artists
    try:
        result = db.table('artists').select('*').execute()
        artists = result.data or []
    except Exception as e:
        log.error(f'Failed to fetch artists: {e}')
        return []

    log.info(f'Scoring {len(artists)} artists...')

    scored = []
    for artist in artists:
        history = get_scan_history(db, artist['id'])
        score = calculate_breakout_score(artist, history)

        artist['breakout_score'] = score
        scored.append(artist)

        # Update score in database
        if not dry_run:
            try:
                db.table('artists').update({
                    'breakout_score': score,
                }).eq('id', artist['id']).execute()
            except Exception as e:
                log.warning(f'Failed to update score for {artist["name"]}: {e}')

    # Sort by breakout score descending
    scored.sort(key=lambda a: a['breakout_score'], reverse=True)
    top = scored[:top_n]

    # Display results
    log.info('')
    log.info(f'═══ TOP {top_n} BREAKOUT CANDIDATES ═══')
    log.info(f'{"Rank":<6}{"Score":<8}{"Artist":<30}{"Genres"}')
    log.info('─' * 70)

    for i, artist in enumerate(top, 1):
        genres = ', '.join(artist.get('genres', [])[:3]) or 'N/A'
        log.info(
            f'{i:<6}{artist["breakout_score"]:<8.1f}'
            f'{artist["name"][:28]:<30}{genres}'
        )

    log.info('')
    log.info(f'Scoring complete. {len(scored)} artists scored.')
    if dry_run:
        log.info('DRY RUN — no scores saved to database.')

    return top


if __name__ == '__main__':
    top_count = 50
    is_dry_run = '--dry-run' in sys.argv

    # Parse --top argument
    if '--top' in sys.argv:
        idx = sys.argv.index('--top')
        if idx + 1 < len(sys.argv):
            try:
                top_count = int(sys.argv[idx + 1])
            except ValueError:
                pass

    run_scoring(top_n=top_count, dry_run=is_dry_run)
