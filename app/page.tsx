import Hero from '@/components/Hero';
import Problem from '@/components/Problem';
import HowItWorks from '@/components/HowItWorks';
import SampleReport from '@/components/SampleReport';
import Features from '@/components/Features';
import Pricing from '@/components/Pricing';
import SocialProof from '@/components/SocialProof';
import FAQ from '@/components/FAQ';
import WaitlistForm from '@/components/WaitlistForm';
import Footer from '@/components/Footer';

export default function Home() {
  return (
    <main>
      <Hero />
      <Problem />
      <HowItWorks />
      <SampleReport />
      <Features />
      <Pricing />
      <SocialProof />
      <FAQ />

      {/* ── Footer CTA ──────────────────────────────────────── */}
      <section className="section-padding bg-gradient-to-b from-brand-dark to-brand-darker">
        <div className="container-tight text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to discover the next big artist?
          </h2>
          <p className="text-brand-muted text-lg mb-10 max-w-xl mx-auto">
            Join the waitlist today. Your first Hot&nbsp;50 report is completely free.
          </p>
          <div className="max-w-lg mx-auto">
            <WaitlistForm variant="footer" />
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}
