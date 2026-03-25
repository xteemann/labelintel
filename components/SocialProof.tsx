export default function SocialProof() {
  return (
    <section className="section-padding">
      <div className="container-tight text-center">
        <p className="text-brand-muted text-sm uppercase tracking-wider mb-10">
          Trusted by forward-thinking labels
        </p>

        {/* Logo placeholders — replace with actual client logos */}
        <div className="flex flex-wrap items-center justify-center gap-8 md:gap-14 opacity-40">
          {['Label One', 'Sonic Records', 'Wave Music', 'Apex Ent.', 'Prism Audio'].map((name) => (
            <div
              key={name}
              className="flex items-center gap-2 text-zinc-500 hover:text-zinc-300 transition-colors"
            >
              <div className="w-8 h-8 rounded-lg bg-zinc-800 flex items-center justify-center">
                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z" />
                </svg>
              </div>
              <span className="font-semibold text-sm tracking-wide">{name}</span>
            </div>
          ))}
        </div>

        {/* Stat bar */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-16 pt-10 border-t border-brand-border">
          {[
            { value: '2.4M+', label: 'Artists scanned daily' },
            { value: '50+', label: 'Labels on waitlist' },
            { value: '94%', label: 'Score accuracy rate' },
            { value: '<24h', label: 'Avg. detection speed' },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="text-2xl md:text-3xl font-bold gradient-text-blue mb-1">{stat.value}</div>
              <p className="text-brand-muted text-sm">{stat.label}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
