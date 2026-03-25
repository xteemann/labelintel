'use client';

import { useState } from 'react';

export default function Hero() {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;
    setStatus('loading');

    try {
      const res = await fetch('/api/waitlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      if (res.ok) {
        setStatus('success');
        setEmail('');
      } else {
        setStatus('error');
      }
    } catch {
      setStatus('error');
    }
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center hero-glow overflow-hidden">
      {/* Animated orbs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-blue/5 rounded-full blur-3xl animate-pulse-slow" />
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '2s' }} />

      <div className="relative z-10 container-tight text-center px-4 py-20">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-brand-border bg-brand-card/50 text-sm text-brand-muted mb-8 animate-fade-in">
          <span className="w-2 h-2 rounded-full bg-brand-green animate-pulse" />
          Scanning 2.4M+ artists in real time
        </div>

        {/* Headline */}
        <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold leading-tight mb-6 animate-slide-up">
          Discover Tomorrow&apos;s{' '}
          <span className="gradient-text">Stars Today</span>
        </h1>

        {/* Sub-headline */}
        <p className="text-lg md:text-xl text-zinc-400 max-w-2xl mx-auto mb-10 animate-slide-up" style={{ animationDelay: '0.15s' }}>
          AI-powered artist intelligence for labels that sign first.
          We scan Spotify, TikTok, and SoundCloud so you never miss a breakout.
        </p>

        {/* CTA Form */}
        <form
          onSubmit={handleSubmit}
          className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto animate-slide-up"
          style={{ animationDelay: '0.3s' }}
        >
          <input
            type="email"
            placeholder="your@label.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="flex-1 px-4 py-3.5 rounded-lg bg-brand-card border border-brand-border
                       text-white placeholder-brand-muted focus:outline-none focus:border-brand-blue
                       focus:ring-1 focus:ring-brand-blue/50 transition-all"
          />
          <button
            type="submit"
            disabled={status === 'loading'}
            className="btn-primary whitespace-nowrap disabled:opacity-60"
          >
            {status === 'loading' ? (
              <span className="flex items-center gap-2">
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Joining…
              </span>
            ) : status === 'success' ? (
              '✓ You\'re In!'
            ) : (
              'Get Free Report'
            )}
          </button>
        </form>

        {status === 'error' && (
          <p className="text-red-400 text-sm mt-3">Something went wrong. Please try again.</p>
        )}

        {/* Social proof */}
        <p className="text-brand-muted text-sm mt-6 animate-fade-in" style={{ animationDelay: '0.5s' }}>
          Join <span className="text-white font-medium">50+ labels</span> already on the waitlist
        </p>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <svg className="w-5 h-5 text-brand-muted" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
        </div>
      </div>
    </section>
  );
}
