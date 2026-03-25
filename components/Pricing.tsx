'use client';

const tiers = [
  {
    name: 'Scout',
    price: '$499',
    period: '/mo',
    description: 'For independent A&R professionals and small teams getting started with data-driven scouting.',
    features: [
      { text: 'Weekly Hot 50 email report', included: true },
      { text: 'Basic artist cards with scores', included: true },
      { text: '1 genre filter', included: true },
      { text: 'Breakout score + key signals', included: true },
      { text: '30-day data history', included: true },
      { text: 'Artist pitch decks', included: false },
      { text: 'Slack / webhook alerts', included: false },
      { text: 'API access', included: false },
    ],
    cta: 'Start Free Trial',
    popular: false,
  },
  {
    name: 'Pro',
    price: '$1,500',
    period: '/mo',
    description: 'For A&R teams at mid-size labels who need deeper intelligence and workflow integration.',
    features: [
      { text: 'Everything in Scout', included: true },
      { text: 'Unlimited genre filters', included: true },
      { text: 'Auto-generated artist pitch decks', included: true },
      { text: 'Slack & email alerts', included: true },
      { text: 'Competitor tracking dashboard', included: true },
      { text: '90-day data history', included: true },
      { text: 'Priority support', included: true },
      { text: 'API access', included: false },
    ],
    cta: 'Start Free Trial',
    popular: true,
  },
  {
    name: 'Label',
    price: '$5,000',
    period: '/mo',
    description: 'For major labels and large A&R teams that need full platform access and custom intelligence.',
    features: [
      { text: 'Everything in Pro', included: true },
      { text: 'Full REST API + webhooks', included: true },
      { text: 'Custom scoring models', included: true },
      { text: 'Unlimited data history', included: true },
      { text: 'CRM integrations', included: true },
      { text: 'Dedicated account manager', included: true },
      { text: 'Custom reports & exports', included: true },
      { text: 'SLA guarantee', included: true },
    ],
    cta: 'Contact Sales',
    popular: false,
  },
];

export default function Pricing() {
  const scrollToWaitlist = () => {
    document.getElementById('waitlist')?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <section className="section-padding bg-gradient-to-b from-brand-dark via-brand-darker to-brand-dark" id="pricing">
      <div className="container-tight">
        {/* Header */}
        <div className="text-center mb-16">
          <p className="text-brand-blue font-semibold text-sm uppercase tracking-wider mb-3">
            Pricing
          </p>
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Intelligence that <span className="gradient-text-blue">pays for itself</span>
          </h2>
          <p className="text-brand-muted text-lg max-w-xl mx-auto">
            One signed artist covers years of LabelIntel. Choose the plan that fits your team.
          </p>
        </div>

        {/* Pricing cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-start">
          {tiers.map((tier) => (
            <div
              key={tier.name}
              className={`glass-card p-8 relative ${
                tier.popular ? 'pricing-popular md:-mt-4 md:mb-0' : ''
              }`}
            >
              {/* Popular badge */}
              {tier.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                  <span className="px-4 py-1 rounded-full bg-brand-blue text-white text-xs font-semibold uppercase tracking-wider">
                    Most Popular
                  </span>
                </div>
              )}

              {/* Plan name */}
              <h3 className="text-lg font-semibold mb-2">{tier.name}</h3>

              {/* Price */}
              <div className="flex items-baseline gap-1 mb-3">
                <span className="text-4xl font-bold">{tier.price}</span>
                <span className="text-brand-muted text-sm">{tier.period}</span>
              </div>

              <p className="text-brand-muted text-sm mb-6 leading-relaxed">{tier.description}</p>

              {/* CTA */}
              <button
                onClick={scrollToWaitlist}
                className={`w-full py-3 rounded-lg font-semibold text-sm transition-all mb-8 ${
                  tier.popular
                    ? 'btn-primary'
                    : 'btn-secondary'
                }`}
              >
                {tier.cta}
              </button>

              {/* Features */}
              <ul className="space-y-3">
                {tier.features.map((feature) => (
                  <li key={feature.text} className="flex items-start gap-3">
                    {feature.included ? (
                      <svg className="w-5 h-5 text-brand-green flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      <svg className="w-5 h-5 text-brand-muted/40 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    )}
                    <span className={`text-sm ${feature.included ? 'text-zinc-300' : 'text-brand-muted/50'}`}>
                      {feature.text}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
