#!/usr/bin/env python3
"""
LabelIntel — Spotify Artist Scanner
====================================
Scans Spotify for emerging artists by analyzing new releases, playlist
additions, and artist growth metrics. Stores results in Supabase.

Usage:
    python spotify_scanner.py              # Full scan
    python spotify_scanner.py --quick      # Quick scan (fewer playlists)

Designed to run as a daily cron job.
"""

import os
import sys
import time
import logging
from datetime import datetime, timezone
from typing import Optional

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from supabase import create_client, Client

# ── Configuration ────────────────────────────────────────────────
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID', '')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET', '')
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', os.environ.get('SUPABASE_ANON_KEY', ''))

# Playlists to scan for emerging artists (curated discovery playlists)
DISCOVERY_PLAYLISTS = [
    '37i9dQZF1DX0XUsuxWHRQd',  # RapCaviar
    '37i9dQZF1DWXRqgorJj26U',  # Fresh Finds
    '37i9dQZF1DX2Nc3B70tvx0',  # New Music Friday
    '37i9dQZF1DX4JAvHpjipBk',  # New Music Friday Hip Hop
    '37i9dQZF1DX4SBhb3fqCJd',  # Are & Be
    '37i9dQZF1DWUa8ZRTfalHk',  # Pop Rising
    '37i9dQZF1DWWBHeXOYZf74',  # Indie Pop
    '37i9dQZF1DWTwnEm1IYyoj',  # Soft Pop Hits
    '37i9dQZF1DX76Wlfdnj7AP',  # Beast Mode
    '37i9dQZF1DX186v583rmzp',  # I Love My '90s Hip-Hop (baseline comparison)
    '37i9dQZF1DX4o1oenSJRJd',  # All New Indie
    '37i9dQZF1DXan38dNVDdl4',  # This is Indie
    '37i9dQZF1DX2pSTOxoPbx9',  # Hot Country
    '37i9dQZF1DX18jTM2l2fJY',  # Rock This
    '37i9dQZF1DX10zKzsJ2jva',  # Viva Latino
]

# Minimum thresholds — skip well-established artists
MAX_MONTHLY_LISTENERS = 5_000_000  # Skip artists with >5M listeners (already mainstream)
MIN_MONTHLY_LISTENERS = 1_000      # Skip very small artists (not enough signal)

# ── Logging ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
log = logging.getLogger('labelintel.scanner')


def init_spotify() -> spotipy.Spotify:
    """Initialize Spotify API client with client credentials flow."""
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        log.error('Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET')
        sys.exit(1)

    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
    )
    return spotipy.Spotify(auth_manager=auth_manager, requests_timeout=30)


def init_supabase() -> Client:
    """Initialize Supabase client."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        log.error('Missing SUPABASE_URL or SUPABASE_KEY')
        sys.exit(1)

    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_playlist_artists(sp: spotipy.Spotify, playlist_id: str) -> list[dict]:
    """Extract unique artists from a Spotify playlist."""
    artists = {}

    try:
        results = sp.playlist_tracks(playlist_id, limit=100)
        tracks = results.get('items', [])

        for item in tracks:
            track = item.get('track')
            if not track or not track.get('artists'):
                continue

            for artist in track['artists']:
                artist_id = artist.get('id')
                if artist_id and artist_id not in artists:
                    artists[artist_id] = {
                        'spotify_id': artist_id,
                        'name': artist.get('name', 'Unknown'),
                    }

    except Exception as e:
        log.warning(f'Error fetching playlist {playlist_id}: {e}')

    return list(artists.values())


def get_artist_details(sp: spotipy.Spotify, artist_id: str) -> Optional[dict]:
    """Fetch detailed artist information from Spotify."""
    try:
        artist = sp.artist(artist_id)
        return {
            'spotify_id': artist['id'],
            'name': artist.get('name', 'Unknown'),
            'genres': artist.get('genres', []),
            'followers': artist.get('followers', {}).get('total', 0),
            'image_url': artist['images'][0]['url'] if artist.get('images') else None,
            'spotify_url': artist.get('external_urls', {}).get('spotify'),
            'popularity': artist.get('popularity', 0),
        }
    except Exception as e:
        log.warning(f'Error fetching artist {artist_id}: {e}')
        return None


def calculate_velocity(
    current: int,
    previous: Optional[int],
    days: int = 30,
) -> float:
    """Calculate growth velocity as a percentage.

    Returns 0 if no previous data exists (first scan).
    """
    if previous is None or previous == 0:
        return 0.0

    change = current - previous
    velocity = (change / previous) * 100

    return round(velocity, 2)


def upsert_artist(db: Client, artist_data: dict, existing: Optional[dict] = None) -> None:
    """Insert or update an artist record in Supabase."""
    now = datetime.now(timezone.utc).isoformat()

    # Calculate velocity based on previous scan data
    monthly_listeners = artist_data.get('monthly_listeners', 0)
    followers = artist_data.get('followers', 0)

    velocity_7d = 0.0
    velocity_30d = 0.0

    if existing:
        prev_listeners = existing.get('monthly_listeners', 0)
        velocity_7d = calculate_velocity(monthly_listeners, prev_listeners, days=7)
        velocity_30d = calculate_velocity(monthly_listeners, prev_listeners, days=30)

    record = {
        'spotify_id': artist_data['spotify_id'],
        'name': artist_data['name'],
        'genres': artist_data.get('genres', []),
        'image_url': artist_data.get('image_url'),
        'spotify_url': artist_data.get('spotify_url'),
        'monthly_listeners': monthly_listeners,
        'followers': followers,
        'listener_velocity_7d': velocity_7d,
        'listener_velocity_30d': velocity_30d,
        'last_scanned': now,
    }

    try:
        db.table('artists').upsert(record, on_conflict='spotify_id').execute()

        # Also insert a scan history record
        db.table('scan_history').insert({
            'artist_id': existing['id'] if existing else None,
            'monthly_listeners': monthly_listeners,
            'followers': followers,
            'playlist_count': artist_data.get('playlist_count', 0),
        }).execute()

    except Exception as e:
        log.warning(f'Error upserting artist {artist_data["name"]}: {e}')


def get_existing_artists(db: Client) -> dict:
    """Fetch all existing artists from the database, keyed by spotify_id."""
    try:
        result = db.table('artists').select('*').execute()
        return {a['spotify_id']: a for a in (result.data or [])}
    except Exception as e:
        log.warning(f'Error fetching existing artists: {e}')
        return {}


def count_playlist_appearances(
    sp: spotipy.Spotify,
    artist_id: str,
    playlists_checked: dict[str, set],
) -> int:
    """Count how many of our tracked playlists an artist appears in."""
    count = 0
    for playlist_id, artist_ids in playlists_checked.items():
        if artist_id in artist_ids:
            count += 1
    return count


def run_scan(quick: bool = False) -> None:
    """Execute a full artist scan pipeline."""
    log.info('═' * 60)
    log.info('LabelIntel Spotify Scanner — Starting scan')
    log.info('═' * 60)

    sp = init_spotify()
    db = init_supabase()

    # Get existing artist data for velocity calculations
    existing_artists = get_existing_artists(db)
    log.info(f'Loaded {len(existing_artists)} existing artists from database')

    # Scan playlists for artist IDs
    playlists_to_scan = DISCOVERY_PLAYLISTS[:5] if quick else DISCOVERY_PLAYLISTS
    all_artists: dict[str, dict] = {}
    playlist_artist_sets: dict[str, set] = {}

    for i, playlist_id in enumerate(playlists_to_scan):
        log.info(f'Scanning playlist {i + 1}/{len(playlists_to_scan)}: {playlist_id}')
        artists = get_playlist_artists(sp, playlist_id)
        artist_ids_in_playlist = set()

        for artist in artists:
            all_artists[artist['spotify_id']] = artist
            artist_ids_in_playlist.add(artist['spotify_id'])

        playlist_artist_sets[playlist_id] = artist_ids_in_playlist
        time.sleep(0.5)  # Respect rate limits

    log.info(f'Found {len(all_artists)} unique artists across {len(playlists_to_scan)} playlists')

    # Fetch detailed info and upsert
    scanned = 0
    skipped = 0

    for artist_id, basic_info in all_artists.items():
        details = get_artist_details(sp, artist_id)
        if not details:
            skipped += 1
            continue

        followers = details.get('followers', 0)

        # Skip mainstream artists (>5M followers as proxy for monthly listeners)
        # Note: Monthly listeners requires web scraping or unofficial API
        # We use followers as a proxy metric via the official API
        if followers > MAX_MONTHLY_LISTENERS:
            skipped += 1
            continue

        if followers < MIN_MONTHLY_LISTENERS:
            skipped += 1
            continue

        # Count playlist appearances
        playlist_count = count_playlist_appearances(sp, artist_id, playlist_artist_sets)
        details['playlist_count'] = playlist_count
        details['monthly_listeners'] = followers  # Using followers as proxy

        existing = existing_artists.get(artist_id)
        upsert_artist(db, details, existing)
        scanned += 1

        if scanned % 50 == 0:
            log.info(f'Progress: {scanned} artists scanned, {skipped} skipped')

        time.sleep(0.3)  # Respect rate limits

    log.info('═' * 60)
    log.info(f'Scan complete: {scanned} artists scanned, {skipped} skipped')
    log.info('═' * 60)


if __name__ == '__main__':
    quick_mode = '--quick' in sys.argv
    run_scan(quick=quick_mode)
