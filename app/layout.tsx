import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export const metadata: Metadata = {
  metadataBase: new URL('https://labelintel.ai'),
  title: {
    default: 'LabelIntel — AI-Powered A&R Intelligence Platform',
    template: '%s | LabelIntel',
  },
  description:
    'Discover breakout artists before they blow up. LabelIntel scans Spotify, TikTok, and SoundCloud to deliver AI-scored artist intelligence to record labels every week.',
  keywords: [
    'AI A&R tool',
    'artist discovery platform',
    'music intelligence',
    'breakout artist prediction',
    'record label tools',
    'A&R technology',
    'Spotify analytics',
    'music data analytics',
    'artist scouting AI',
    'music industry intelligence',
  ],
  authors: [{ name: 'LabelIntel' }],
  creator: 'LabelIntel',
  publisher: 'LabelIntel',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://labelintel.ai',
    siteName: 'LabelIntel',
    title: 'LabelIntel — AI-Powered A&R Intelligence Platform',
    description:
      'Discover breakout artists before they blow up. AI-scored intelligence delivered weekly.',
    images: [
      {
        url: '/api/og',
        width: 1200,
        height: 630,
        alt: 'LabelIntel — AI A&R Intelligence',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'LabelIntel — AI-Powered A&R Intelligence',
    description:
      'Discover breakout artists before they blow up. AI-scored intelligence delivered weekly.',
    images: ['/api/og'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <head>
        {/* Google Analytics — replace GA_ID in production */}
        {process.env.NEXT_PUBLIC_GA_ID && (
          <>
            <script
              async
              src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
            />
            <script
              dangerouslySetInnerHTML={{
                __html: `
                  window.dataLayer = window.dataLayer || [];
                  function gtag(){dataLayer.push(arguments);}
                  gtag('js', new Date());
                  gtag('config', '${process.env.NEXT_PUBLIC_GA_ID}');
                `,
              }}
            />
          </>
        )}
      </head>
      <body className={`${inter.className} bg-brand-dark text-white antialiased`}>
        <div className="bg-grid min-h-screen">
          {children}
        </div>
      </body>
    </html>
  );
}
