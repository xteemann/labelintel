#!/usr/bin/env python3
"""
LabelIntel — Weekly Report Generator
======================================
Pulls the top 50 scored artists from Supabase, generates a beautiful
HTML email report, and sends it to all waitlist subscribers via Resend.

Usage:
    python generate_report.py                # Generate and send report
    python generate_report.py --preview      # Generate HTML to stdout (no send)
    python generate_report.py --test email   # Send to a single test email

Designed to run weekly (every Monday) via cron.
"""

import os
import sys
import logging
from datetime import datetime, timezone

import resend
from dotenv import load_dotenv
from supabase import create_client, Client

# ── Configuration ────────────────────────────────────────────────
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', os.environ.get('SUPABASE_ANON_KEY', ''))
RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')

FROM_EMAIL = 'LabelIntel <report@labelintel.ai>'
REPORT_SUBJECT_TEMPLATE = 'LabelIntel Hot 50 — Week of {date}'

# ── Logging ──────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
log = logging.getLogger('labelintel.report')


def init_supabase() -> Client:
    """Initialize Supabase client."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        log.error('Missing SUPABASE_URL or SUPABASE_KEY')
        sys.exit(1)
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_top_artists(db: Client, limit: int = 50) -> list[dict]:
    """Fetch top artists by breakout score."""
    try:
        result = (
            db.table('artists')
            .select('*')
            .order('breakout_score', desc=True)
            .limit(limit)
            .execute()
        )
        return result.data or []
    except Exception as e:
        log.error(f'Failed to fetch top artists: {e}')
        return []


def get_waitlist_emails(db: Client) -> list[str]:
    """Fetch all waitlist emails."""
    try:
        result = db.table('waitlist').select('email').execute()
        return [row['email'] for row in (result.data or [])]
    except Exception as e:
        log.error(f'Failed to fetch waitlist: {e}')
        return []


def score_color(score: float) -> str:
    """Return a hex color based on the breakout score."""
    if score >= 95:
        return '#10B981'  # Emerald green
    elif score >= 85:
        return '#3B82F6'  # Blue
    elif score >= 75:
        return '#60A5FA'  # Light blue
    elif score >= 60:
        return '#F59E0B'  # Amber
    else:
        return '#71717A'  # Gray


def generate_artist_card(rank: int, artist: dict) -> str:
    """Generate HTML for a single artist card in the report."""
    name = artist.get('name', 'Unknown Artist')
    score = artist.get('breakout_score', 0)
    genres = artist.get('genres', [])
    genre_str = ', '.join(genres[:3]) if genres else 'Uncategorized'
    velocity = artist.get('listener_velocity_30d', 0)
    followers = artist.get('followers', 0)
    playlist_adds = artist.get('playlist_adds_7d', 0)
    color = score_color(score)
    spotify_url = artist.get('spotify_url', '#')

    velocity_sign = '+' if velocity > 0 else ''
    followers_fmt = f'{followers:,}'

    return f'''
    <tr>
      <td style="padding: 16px 0; border-bottom: 1px solid #1E1E2A;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0">
          <tr>
            <!-- Rank -->
            <td width="40" style="vertical-align: top; padding-right: 12px;">
              <span style="font-size: 18px; font-weight: 700; color: #71717A;">
                {rank}
              </span>
            </td>

            <!-- Artist Info -->
            <td style="vertical-align: top;">
              <a href="{spotify_url}" style="color: #FFFFFF; text-decoration: none; font-size: 16px; font-weight: 600;">
                {name}
              </a>
              <br/>
              <span style="font-size: 12px; color: #60A5FA; background: rgba(59,130,246,0.1);
                           padding: 2px 8px; border-radius: 4px; display: inline-block; margin-top: 4px;">
                {genre_str}
              </span>
              <div style="margin-top: 8px; font-size: 12px; color: #A1A1AA;">
                Listeners: <span style="color: #10B981;">{velocity_sign}{velocity:.0f}%</span> (30d)
                &nbsp;&middot;&nbsp;
                Followers: {followers_fmt}
                &nbsp;&middot;&nbsp;
                Playlist adds: <span style="color: #10B981;">+{playlist_adds}</span> (7d)
              </div>
            </td>

            <!-- Score Badge -->
            <td width="60" style="vertical-align: top; text-align: right;">
              <div style="display: inline-block; background: {color}15; border: 1px solid {color}40;
                          border-radius: 8px; padding: 4px 10px; text-align: center;">
                <span style="font-size: 20px; font-weight: 800; color: {color};">
                  {score:.0f}
                </span>
              </div>
            </td>
          </tr>
        </table>
      </td>
    </tr>'''


def generate_report_html(artists: list[dict], report_date: str) -> str:
    """Generate the complete HTML email report."""
    artist_cards = '\n'.join(
        generate_artist_card(i + 1, artist) for i, artist in enumerate(artists)
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>LabelIntel Hot 50 — {report_date}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0A0A0F; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
  <!-- Wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #0A0A0F;">
    <tr>
      <td align="center" style="padding: 40px 20px;">

        <!-- Content Container -->
        <table width="600" cellpadding="0" cellspacing="0" border="0"
               style="max-width: 600px; width: 100%;">

          <!-- Header -->
          <tr>
            <td style="padding-bottom: 32px; text-align: center;">
              <div style="display: inline-flex; align-items: center; gap: 8px; margin-bottom: 16px;">
                <div style="width: 32px; height: 32px; background: #3B82F6; border-radius: 8px;
                            display: inline-block; text-align: center; line-height: 32px; font-size: 16px;">
                  🎵
                </div>
                <span style="font-size: 20px; font-weight: 700; color: #FFFFFF; vertical-align: middle;">
                  LabelIntel
                </span>
              </div>
              <h1 style="margin: 0; font-size: 28px; font-weight: 800; color: #FFFFFF; line-height: 1.2;">
                Hot 50 Report
              </h1>
              <p style="margin: 8px 0 0; font-size: 14px; color: #71717A;">
                Week of {report_date} &middot; AI-Generated Intelligence
              </p>
            </td>
          </tr>

          <!-- Summary Bar -->
          <tr>
            <td style="padding: 20px; background: #12121A; border: 1px solid #1E1E2A;
                        border-radius: 12px; margin-bottom: 24px;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td width="33%" style="text-align: center;">
                    <div style="font-size: 24px; font-weight: 700; color: #3B82F6;">50</div>
                    <div style="font-size: 11px; color: #71717A; margin-top: 2px;">Artists Ranked</div>
                  </td>
                  <td width="33%" style="text-align: center;">
                    <div style="font-size: 24px; font-weight: 700; color: #10B981;">
                      {artists[0]['breakout_score']:.0f}
                    </div>
                    <div style="font-size: 11px; color: #71717A; margin-top: 2px;">Top Score</div>
                  </td>
                  <td width="33%" style="text-align: center;">
                    <div style="font-size: 24px; font-weight: 700; color: #8B5CF6;">
                      {len(set(g for a in artists for g in a.get('genres', [])[:1]))}
                    </div>
                    <div style="font-size: 11px; color: #71717A; margin-top: 2px;">Genres</div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Spacer -->
          <tr><td style="height: 24px;"></td></tr>

          <!-- Artist Cards -->
          <tr>
            <td style="background: #12121A; border: 1px solid #1E1E2A; border-radius: 12px; padding: 20px;">
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                {artist_cards}
              </table>
            </td>
          </tr>

          <!-- Spacer -->
          <tr><td style="height: 32px;"></td></tr>

          <!-- CTA -->
          <tr>
            <td style="text-align: center; padding: 24px; background: #12121A;
                        border: 1px solid #1E1E2A; border-radius: 12px;">
              <p style="margin: 0 0 16px; font-size: 16px; color: #FFFFFF; font-weight: 600;">
                Want deeper intelligence?
              </p>
              <p style="margin: 0 0 20px; font-size: 14px; color: #A1A1AA;">
                Upgrade to Pro for artist pitch decks, genre filtering, and Slack alerts.
              </p>
              <a href="https://labelintel.ai/#pricing"
                 style="display: inline-block; background: #3B82F6; color: #FFFFFF;
                        font-weight: 600; font-size: 14px; padding: 12px 32px;
                        border-radius: 8px; text-decoration: none;">
                View Plans →
              </a>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="padding: 32px 0; text-align: center;">
              <p style="margin: 0; font-size: 12px; color: #71717A;">
                © 2026 LabelIntel. AI-powered artist intelligence.
              </p>
              <p style="margin: 8px 0 0; font-size: 12px; color: #71717A;">
                <a href="https://labelintel.ai" style="color: #3B82F6; text-decoration: none;">
                  labelintel.ai
                </a>
                &nbsp;&middot;&nbsp;
                <a href="#" style="color: #71717A; text-decoration: none;">Unsubscribe</a>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>'''


def send_report(html: str, recipients: list[str], subject: str) -> None:
    """Send the HTML report to all recipients via Resend."""
    if not RESEND_API_KEY:
        log.error('Missing RESEND_API_KEY — cannot send emails')
        return

    resend.api_key = RESEND_API_KEY

    # Resend batch sending (up to 100 per batch)
    batch_size = 50
    sent_count = 0

    for i in range(0, len(recipients), batch_size):
        batch = recipients[i:i + batch_size]

        for email in batch:
            try:
                resend.Emails.send({
                    'from': FROM_EMAIL,
                    'to': [email],
                    'subject': subject,
                    'html': html,
                })
                sent_count += 1
            except Exception as e:
                log.warning(f'Failed to send to {email}: {e}')

        log.info(f'Sent batch: {sent_count}/{len(recipients)} emails delivered')

    log.info(f'Report delivery complete: {sent_count}/{len(recipients)} emails sent')


def run_report(preview: bool = False, test_email: str = '') -> None:
    """Generate and optionally send the weekly report."""
    log.info('═' * 60)
    log.info('LabelIntel Report Generator — Starting')
    log.info('═' * 60)

    db = init_supabase()

    # Get top 50 artists
    artists = get_top_artists(db, limit=50)
    if not artists:
        log.error('No artists found. Run the scanner and scoring first.')
        return

    log.info(f'Loaded {len(artists)} top artists')

    # Generate report
    report_date = datetime.now(timezone.utc).strftime('%B %d, %Y')
    subject = REPORT_SUBJECT_TEMPLATE.format(date=report_date)
    html = generate_report_html(artists, report_date)

    log.info(f'Generated HTML report ({len(html):,} bytes)')

    if preview:
        # Output HTML to stdout for preview
        print(html)
        log.info('Preview mode — report printed to stdout')
        return

    if test_email:
        # Send to a single test email
        log.info(f'Sending test report to: {test_email}')
        send_report(html, [test_email], f'[TEST] {subject}')
        return

    # Get all waitlist subscribers
    recipients = get_waitlist_emails(db)
    if not recipients:
        log.warning('No waitlist subscribers found. Skipping send.')
        return

    log.info(f'Sending to {len(recipients)} subscribers')
    send_report(html, recipients, subject)

    # Log report in history
    try:
        db.table('report_history').insert({
            'report_date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
            'artist_count': len(artists),
            'recipients_count': len(recipients),
            'sent_at': datetime.now(timezone.utc).isoformat(),
        }).execute()
    except Exception as e:
        log.warning(f'Failed to log report history: {e}')

    log.info('═' * 60)
    log.info('Report generation and delivery complete')
    log.info('═' * 60)


if __name__ == '__main__':
    if '--preview' in sys.argv:
        run_report(preview=True)
    elif '--test' in sys.argv:
        idx = sys.argv.index('--test')
        if idx + 1 < len(sys.argv):
            run_report(test_email=sys.argv[idx + 1])
        else:
            log.error('--test requires an email address')
    else:
        run_report()
