-- ============================================================
-- LabelIntel Database Schema
-- Run this in your Supabase SQL Editor to set up the database
-- ============================================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ── Artists Table ────────────────────────────────────────────
-- Core table storing artist profiles and latest metrics
CREATE TABLE artists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  spotify_id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  genres TEXT[] DEFAULT '{}',
  image_url TEXT,
  spotify_url TEXT,
  monthly_listeners INT DEFAULT 0,
  followers INT DEFAULT 0,
  listener_velocity_7d FLOAT DEFAULT 0,
  listener_velocity_30d FLOAT DEFAULT 0,
  playlist_adds_7d INT DEFAULT 0,
  total_playlists INT DEFAULT 0,
  social_signal_score FLOAT DEFAULT 0,
  breakout_score FLOAT DEFAULT 0,
  last_scanned TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_artists_breakout_score ON artists(breakout_score DESC);
CREATE INDEX idx_artists_spotify_id ON artists(spotify_id);
CREATE INDEX idx_artists_last_scanned ON artists(last_scanned);
CREATE INDEX idx_artists_genres ON artists USING GIN(genres);

-- ── Waitlist Table ───────────────────────────────────────────
-- Stores email signups from the landing page
CREATE TABLE waitlist (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  company TEXT,
  role TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_waitlist_email ON waitlist(email);
CREATE INDEX idx_waitlist_created_at ON waitlist(created_at DESC);

-- ── Scan History Table ───────────────────────────────────────
-- Historical snapshots of artist metrics for trend analysis
CREATE TABLE scan_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  artist_id UUID REFERENCES artists(id) ON DELETE CASCADE,
  monthly_listeners INT,
  followers INT,
  playlist_count INT,
  breakout_score FLOAT,
  scanned_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_scan_history_artist_id ON scan_history(artist_id);
CREATE INDEX idx_scan_history_scanned_at ON scan_history(scanned_at DESC);

-- ── Report History Table ─────────────────────────────────────
-- Track generated and sent reports
CREATE TABLE report_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_date DATE NOT NULL,
  artist_count INT DEFAULT 0,
  recipients_count INT DEFAULT 0,
  sent_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── Row Level Security ───────────────────────────────────────
-- Enable RLS on all tables
ALTER TABLE artists ENABLE ROW LEVEL SECURITY;
ALTER TABLE waitlist ENABLE ROW LEVEL SECURITY;
ALTER TABLE scan_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE report_history ENABLE ROW LEVEL SECURITY;

-- Waitlist: allow anonymous inserts (for the landing page)
CREATE POLICY "Allow anonymous waitlist insert"
  ON waitlist FOR INSERT
  TO anon
  WITH CHECK (true);

-- Artists: read-only for anon (public API future use)
CREATE POLICY "Allow anonymous artist reads"
  ON artists FOR SELECT
  TO anon
  USING (true);

-- Service role has full access (used by Python scripts)
-- No additional policies needed — service_role bypasses RLS

-- ── Updated At Trigger ───────────────────────────────────────
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER artists_updated_at
  BEFORE UPDATE ON artists
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
