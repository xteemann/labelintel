import { ImageResponse } from 'next/og';

export const runtime = 'edge';

export async function GET() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'linear-gradient(135deg, #0A0A0F 0%, #12121A 50%, #0A0A0F 100%)',
          fontFamily: 'Inter, system-ui, sans-serif',
        }}
      >
        {/* Grid overlay */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            backgroundImage:
              'linear-gradient(rgba(59, 130, 246, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(59, 130, 246, 0.05) 1px, transparent 1px)',
            backgroundSize: '60px 60px',
          }}
        />

        {/* Glow */}
        <div
          style={{
            position: 'absolute',
            top: '-100px',
            width: '600px',
            height: '400px',
            background: 'radial-gradient(ellipse at center, rgba(59, 130, 246, 0.2) 0%, transparent 70%)',
          }}
        />

        {/* Logo & Brand */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            marginBottom: '24px',
          }}
        >
          <div
            style={{
              width: '48px',
              height: '48px',
              borderRadius: '12px',
              background: '#3B82F6',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '24px',
            }}
          >
            🎵
          </div>
          <span style={{ fontSize: '28px', fontWeight: 700, color: '#ffffff' }}>
            LabelIntel
          </span>
        </div>

        {/* Headline */}
        <div
          style={{
            fontSize: '56px',
            fontWeight: 800,
            color: '#ffffff',
            textAlign: 'center',
            lineHeight: 1.1,
            maxWidth: '900px',
            marginBottom: '16px',
          }}
        >
          AI-Powered A&R Intelligence
        </div>

        {/* Subheadline */}
        <div
          style={{
            fontSize: '24px',
            color: '#A1A1AA',
            textAlign: 'center',
            maxWidth: '700px',
          }}
        >
          Discover breakout artists before they blow up. Data-driven scouting for record labels.
        </div>

        {/* Bottom bar */}
        <div
          style={{
            position: 'absolute',
            bottom: '40px',
            display: 'flex',
            gap: '32px',
            fontSize: '16px',
            color: '#71717A',
          }}
        >
          <span>labelintel.ai</span>
          <span>·</span>
          <span>2.4M+ artists scanned daily</span>
          <span>·</span>
          <span>94% accuracy</span>
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  );
}
