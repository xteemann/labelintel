'use client';

import { useState } from 'react';

interface WaitlistFormProps {
  variant?: 'default' | 'footer';
}

export default function WaitlistForm({ variant = 'default' }: WaitlistFormProps) {
  const [email, setEmail] = useState('');
  const [company, setCompany] = useState('');
  const [role, setRole] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [errorMsg, setErrorMsg] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) return;

    setStatus('loading');
    setErrorMsg('');

    try {
      const res = await fetch('/api/waitlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, company, role }),
      });

      const data = await res.json();

      if (res.ok) {
        setStatus('success');
        setEmail('');
        setCompany('');
        setRole('');
      } else {
        setStatus('error');
        setErrorMsg(data.error || 'Something went wrong. Please try again.');
      }
    } catch {
      setStatus('error');
      setErrorMsg('Network error. Please check your connection.');
    }
  };

  /* ── Success state ─────────────────────────────────────────── */
  if (status === 'success') {
    return (
      <div className="glass-card p-8 text-center animate-fade-in" id="waitlist">
        <div className="w-14 h-14 rounded-full bg-brand-green/10 border border-brand-green/20 flex items-center justify-center mx-auto mb-4">
          <svg className="w-7 h-7 text-brand-green" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h3 className="text-xl font-bold mb-2">You&apos;re on the list!</h3>
        <p className="text-brand-muted text-sm">
          We&apos;ll send your free Hot&nbsp;50 report to your inbox this Monday.
        </p>
      </div>
    );
  }

  /* ── Footer variant (compact) ──────────────────────────────── */
  if (variant === 'footer') {
    return (
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3" id="waitlist">
        <input
          type="email"
          placeholder="your@label.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="flex-1 px-4 py-3 rounded-lg bg-brand-card border border-brand-border
                     text-white placeholder-brand-muted focus:outline-none focus:border-brand-blue
                     focus:ring-1 focus:ring-brand-blue/50 transition-all"
        />
        <button
          type="submit"
          disabled={status === 'loading'}
          className="btn-primary whitespace-nowrap disabled:opacity-60"
        >
          {status === 'loading' ? 'Joining…' : 'Join Waitlist'}
        </button>
        {status === 'error' && (
          <p className="text-red-400 text-xs mt-1 sm:col-span-2">{errorMsg}</p>
        )}
      </form>
    );
  }

  /* ── Default (full form) ───────────────────────────────────── */
  return (
    <form onSubmit={handleSubmit} className="glass-card p-8 space-y-4" id="waitlist">
      <div>
        <label htmlFor="wl-email" className="block text-sm font-medium text-zinc-300 mb-1.5">
          Work Email *
        </label>
        <input
          id="wl-email"
          type="email"
          placeholder="your@label.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full px-4 py-3 rounded-lg bg-brand-dark border border-brand-border
                     text-white placeholder-brand-muted focus:outline-none focus:border-brand-blue
                     focus:ring-1 focus:ring-brand-blue/50 transition-all"
        />
      </div>

      <div>
        <label htmlFor="wl-company" className="block text-sm font-medium text-zinc-300 mb-1.5">
          Company / Label
        </label>
        <input
          id="wl-company"
          type="text"
          placeholder="Atlantic Records"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          className="w-full px-4 py-3 rounded-lg bg-brand-dark border border-brand-border
                     text-white placeholder-brand-muted focus:outline-none focus:border-brand-blue
                     focus:ring-1 focus:ring-brand-blue/50 transition-all"
        />
      </div>

      <div>
        <label htmlFor="wl-role" className="block text-sm font-medium text-zinc-300 mb-1.5">
          Your Role
        </label>
        <select
          id="wl-role"
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="w-full px-4 py-3 rounded-lg bg-brand-dark border border-brand-border
                     text-white focus:outline-none focus:border-brand-blue
                     focus:ring-1 focus:ring-brand-blue/50 transition-all appearance-none"
        >
          <option value="">Select your role</option>
          <option value="A&R">A&R</option>
          <option value="Manager">Artist Manager</option>
          <option value="Label Head">Label Head / Executive</option>
          <option value="Marketing">Marketing</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <button
        type="submit"
        disabled={status === 'loading'}
        className="btn-primary w-full disabled:opacity-60"
      >
        {status === 'loading' ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            Joining waitlist…
          </span>
        ) : (
          'Get Free Hot 50 Report'
        )}
      </button>

      {status === 'error' && (
        <p className="text-red-400 text-sm text-center">{errorMsg}</p>
      )}

      <p className="text-brand-muted text-xs text-center">
        No credit card required. Unsubscribe anytime.
      </p>
    </form>
  );
}
