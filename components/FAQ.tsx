'use client';

import { useState } from 'react';

const faqs = [
  {
    question: 'How does the breakout scoring algorithm work?',
    answer:
      'Our proprietary algorithm analyzes five key dimensions: streaming velocity (35% weight), playlist momentum (25%), social signals from TikTok and other platforms (20%), organic engagement ratio (10%), and release consistency (10%). Each artist receives a score from 0–100, with higher scores indicating a stronger probability of breaking out in the next 30–90 days.',
  },
  {
    question: 'What data sources does LabelIntel use?',
    answer:
      'We ingest data from Spotify (monthly listeners, followers, playlist additions, streaming velocity), TikTok (sound usage, video counts, engagement trends), and SoundCloud (plays, reposts, follower growth). Our pipeline scans 2.4M+ artists daily and cross-references signals across all platforms for maximum accuracy.',
  },
  {
    question: 'How accurate are the breakout predictions?',
    answer:
      'Our backtesting shows a 94% accuracy rate — meaning 94% of artists who scored 85+ on our system went on to achieve significant growth milestones (100K+ monthly listener increase, major playlist placement, or label signing) within 90 days. We continuously refine the model with new data.',
  },
  {
    question: 'Can I filter the Hot 50 by genre?',
    answer:
      'Yes. Scout plans include 1 genre filter, while Pro and Label plans offer unlimited genre filtering. You can focus on hip-hop, R&B, pop, electronic, Latin, rock, country, indie, or any sub-genre. You can also set up custom genre combinations to match your label\'s signing strategy.',
  },
  {
    question: 'Do you integrate with our existing tools?',
    answer:
      'Pro plans include Slack and email alert integrations. Label plans offer full REST API access, webhooks, and can integrate with your CRM, internal databases, or custom A&R workflows. We also support CSV/Excel exports on all plans for easy data sharing.',
  },
  {
    question: 'Is there a free trial?',
    answer:
      'Yes! Every new subscriber gets their first Hot 50 report completely free — no credit card required. Join the waitlist and we\'ll send you this week\'s report so you can evaluate the quality of our intelligence before committing to a paid plan.',
  },
  {
    question: 'How is this different from Chartmetric or Soundcharts?',
    answer:
      'Traditional analytics platforms show you what\'s already happened. LabelIntel is predictive — we identify artists before they blow up, not after. Our AI-powered breakout scoring is specifically designed for A&R decision-making, not general music analytics. We focus on the signal that matters most: "Should we sign this artist?"',
  },
  {
    question: 'Can I track specific artists or competitors?',
    answer:
      'Pro and Label plans include competitor tracking. You can monitor which unsigned artists are gaining attention from rival labels, track A&R activity signals, and set up alerts when artists on your watchlist hit scoring thresholds. Label plans also include market intelligence on signing trends.',
  },
];

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="section-padding" id="faq">
      <div className="container-tight max-w-3xl">
        {/* Header */}
        <div className="text-center mb-16">
          <p className="text-brand-blue font-semibold text-sm uppercase tracking-wider mb-3">
            FAQ
          </p>
          <h2 className="text-3xl md:text-4xl font-bold">
            Frequently asked questions
          </h2>
        </div>

        {/* Accordion */}
        <div className="space-y-3">
          {faqs.map((faq, index) => (
            <div
              key={index}
              className="glass-card overflow-hidden"
            >
              <button
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
                className="w-full flex items-center justify-between p-5 text-left hover:bg-white/[0.02] transition-colors"
              >
                <span className="font-medium pr-4">{faq.question}</span>
                <svg
                  className={`w-5 h-5 text-brand-muted flex-shrink-0 transition-transform duration-300 ${
                    openIndex === index ? 'rotate-180' : ''
                  }`}
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div
                className={`faq-content ${openIndex === index ? 'open' : ''}`}
                style={{
                  maxHeight: openIndex === index ? '500px' : '0',
                  padding: openIndex === index ? '0 20px 20px' : '0 20px',
                }}
              >
                <p className="text-brand-muted text-[15px] leading-relaxed">
                  {faq.answer}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
