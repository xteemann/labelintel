export default function Problem() {
  return (
    <section className="section-padding">
      <div className="container-tight">
        <div className="glass-card p-8 md:p-12 max-w-4xl mx-auto text-center">
          {/* Icon */}
          <div className="w-14 h-14 rounded-xl bg-red-500/10 border border-red-500/20 flex items-center justify-center mx-auto mb-6">
            <svg className="w-7 h-7 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>

          <h2 className="text-2xl md:text-3xl font-bold mb-4">
            The A&R Problem
          </h2>

          <p className="text-lg md:text-xl text-zinc-300 leading-relaxed mb-8">
            A&R teams spend <span className="text-white font-semibold">40+ hours weekly</span> manually
            scrolling SoundCloud, TikTok, and Spotify.{' '}
            <span className="text-red-400 font-semibold">90% of breakout artists are discovered too late</span> —
            after they&apos;ve already been signed by faster-moving competitors.
          </p>

          {/* Stats row */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
            {[
              { value: '40+', label: 'Hours wasted weekly on manual scouting', color: 'text-red-400' },
              { value: '90%', label: 'Of breakout artists discovered too late', color: 'text-amber-400' },
              { value: '$2.1M', label: 'Avg. revenue lost per missed signing', color: 'text-red-400' },
            ].map((stat) => (
              <div key={stat.label} className="text-center">
                <div className={`text-3xl md:text-4xl font-bold ${stat.color} mb-2`}>
                  {stat.value}
                </div>
                <p className="text-sm text-brand-muted">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
