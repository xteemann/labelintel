# LabelIntel — AI-Powered A&R Intelligence Platform

> Discover breakout artists before they blow up. AI-scored intelligence delivered weekly to record labels.

**Live at:** [labelintel.ai](https://labelintel.ai)

---

## What It Does

LabelIntel scans Spotify, TikTok, and SoundCloud data to identify under-the-radar artists showing breakout signals. Every Monday, subscribers receive a **Hot 50** report — a ranked list of the 50 artists most likely to break out, with data-backed scores and key signals.

Labels pay $499–$5,000/mo for this intelligence.

## Tech Stack

| Layer | Technology | Cost |
|-------|-----------|------|
| Frontend | Next.js 14 (App Router) + TypeScript | Free |
| Styling | Tailwind CSS | Free |
| Hosting | Vercel | Free tier |
| Database | Supabase (PostgreSQL) | Free tier |
| Email | Resend.com | Free tier |
| Data Source | Spotify Web API | Free |

---

## 🚀 Deployment Guide

### Step 1: Push to GitHub

```bash
cd labelintel
git init
git add .
git commit -m "Initial commit — LabelIntel MVP"
git remote add origin https://github.com/YOUR_USERNAME/labelintel.git
git push -u origin main
```

### Step 2: Deploy on Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click **"New Project"** → Import your `labelintel` repository
3. Framework: **Next.js** (auto-detected)
4. Click **Deploy**
5. Your site is live at `labelintel.vercel.app`

### Step 3: Set Up Supabase

1. Go to [supabase.com](https://supabase.com) → **New Project**
2. Choose a name, password, and region (US East recommended)
3. Once created, go to **SQL Editor**
4. Paste the contents of `supabase/schema.sql` and click **Run**
5. Go to **Settings → API** to get your:
   - **Project URL** → `SUPABASE_URL`
   - **anon/public key** → `SUPABASE_ANON_KEY`
   - **service_role key** → `SUPABASE_SERVICE_ROLE_KEY`

### Step 4: Get Spotify API Credentials

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Click **Create App**
3. Set a name and description (redirect URI can be `http://localhost:3000`)
4. Copy your:
   - **Client ID** → `SPOTIFY_CLIENT_ID`
   - **Client Secret** → `SPOTIFY_CLIENT_SECRET`

### Step 5: Set Up Resend

1. Go to [resend.com](https://resend.com) → Sign up (free)
2. Go to **API Keys** → Create a new key
3. Copy the key → `RESEND_API_KEY`
4. Add & verify your domain `labelintel.ai` for sending

### Step 6: Connect Domain

1. In Vercel Dashboard → **Settings → Domains**
2. Add `labelintel.ai`
3. Update your domain's DNS:
   - **A Record:** `76.76.21.21`
   - **CNAME:** `cname.vercel-dns.com` (for `www`)
4. Wait for DNS propagation (usually 5–30 minutes)

### Step 7: Configure Environment Variables

In Vercel Dashboard → **Settings → Environment Variables**, add:

```
SPOTIFY_CLIENT_ID=your_id
SPOTIFY_CLIENT_SECRET=your_secret
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
RESEND_API_KEY=re_xxxxxxxxxxxxx
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX  (optional)
```

### Step 8: Set Up Data Pipeline (Cron Jobs)

The Python scripts run independently of the Next.js app. Set them up on any server or use a cron service:

```bash
# Install Python dependencies
cd scripts
pip install -r requirements.txt

# Create .env file in the project root with your credentials
cp ../.env.example ../.env
# Edit .env with your actual values

# Test the scanner
python spotify_scanner.py --quick

# Test scoring
python scoring.py --dry-run --top 10

# Test report generation
python generate_report.py --preview > report.html
# Open report.html in a browser to verify

# Test sending to your email
python generate_report.py --test your@email.com
```

**Recommended cron schedule:**

```cron
# Scan artists daily at 2 AM
0 2 * * * cd /path/to/labelintel/scripts && python spotify_scanner.py

# Score artists daily at 4 AM (after scanner finishes)
0 4 * * * cd /path/to/labelintel/scripts && python scoring.py

# Send weekly report every Monday at 8 AM
0 8 * * 1 cd /path/to/labelintel/scripts && python generate_report.py
```

---

## Project Structure

```
labelintel/
├── app/
│   ├── api/
│   │   ├── og/route.tsx          # Dynamic OG image
│   │   └── waitlist/route.ts     # Waitlist signup endpoint
│   ├── globals.css               # Dark theme + glass morphism
│   ├── layout.tsx                # Root layout with SEO
│   ├── page.tsx                  # Main landing page
│   ├── robots.ts                 # SEO robots.txt
│   └── sitemap.ts                # SEO sitemap
├── components/
│   ├── FAQ.tsx                   # Accordion FAQ
│   ├── Features.tsx              # Feature grid
│   ├── Footer.tsx                # Footer with links
│   ├── Hero.tsx                  # Hero with email CTA
│   ├── HowItWorks.tsx            # 3-step process
│   ├── Pricing.tsx               # 3-tier pricing cards
│   ├── Problem.tsx               # Problem statement
│   ├── SampleReport.tsx          # Mock Hot 50 preview
│   ├── SocialProof.tsx           # Social proof + stats
│   └── WaitlistForm.tsx          # Full waitlist form
├── scripts/
│   ├── spotify_scanner.py        # Spotify data ingestion
│   ├── scoring.py                # Breakout scoring engine
│   ├── generate_report.py        # HTML email report generator
│   └── requirements.txt          # Python dependencies
├── supabase/
│   └── schema.sql                # Database schema
├── .env.example                  # Environment variable template
├── next.config.js                # Next.js config
├── package.json                  # Node.js dependencies
├── postcss.config.js             # PostCSS config
├── tailwind.config.ts            # Tailwind config with brand tokens
├── tsconfig.json                 # TypeScript config
└── README.md                     # This file
```

---

## Scoring Algorithm

Each artist receives a **Breakout Score (0–100)** based on:

| Factor | Weight | What It Measures |
|--------|--------|-----------------|
| Streaming Velocity | 35% | Monthly listener growth rate (30d) |
| Playlist Momentum | 25% | Playlist additions in the last 7 days |
| Social Signals | 20% | TikTok sounds, social mentions |
| Organic Ratio | 10% | Follower-to-listener ratio (organic vs. playlist-driven) |
| Consistency | 10% | Steady upward trajectory over time |

Scores are normalized using sigmoid functions to prevent outliers from dominating.

---

## License

Proprietary — © 2026 LabelIntel. All rights reserved.
