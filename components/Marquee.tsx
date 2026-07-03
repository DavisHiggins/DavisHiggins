'use client';

import Image from 'next/image';
import { marqueeItems } from '@/lib/data';

export default function Marquee() {
  // Triplicate for a fully seamless dense strip
  const items = [...marqueeItems, ...marqueeItems, ...marqueeItems];

  return (
    <section
      className="relative py-6"
      style={{
        background: 'rgba(255,255,255,0.015)',
        borderTop: '1px solid rgba(46,142,255,0.25)',
        borderBottom: '1px solid rgba(255,255,255,0.05)',
      }}
    >
      <div className="marquee-mask overflow-hidden">
        <div
          className="flex items-center"
          style={{
            width: 'max-content',
            animation: 'marquee 35s linear infinite',
            gap: '64px',
          }}
        >
          {items.map((item, i) => (
            <div
              key={`${item.name}-${i}`}
              className="group flex shrink-0 items-center justify-center"
              style={{ height: '56px', minWidth: '56px' }}
            >
              {item.logo ? (
                <div
                  className="relative transition-all duration-400"
                  style={{
                    height: '56px',
                    width: 'auto',
                    minWidth: '56px',
                    maxWidth: '140px',
                    filter: 'grayscale(1) brightness(0.7)',
                  }}
                  onMouseEnter={(e) => {
                    (e.currentTarget as HTMLDivElement).style.filter = 'grayscale(0) brightness(1.1)';
                  }}
                  onMouseLeave={(e) => {
                    (e.currentTarget as HTMLDivElement).style.filter = 'grayscale(1) brightness(0.7)';
                  }}
                >
                  <Image
                    src={item.logo}
                    alt={item.name}
                    height={56}
                    width={140}
                    style={{
                      height: '56px',
                      width: 'auto',
                      objectFit: 'contain',
                      mixBlendMode: 'screen',
                    }}
                  />
                </div>
              ) : (
                <div
                  className="flex items-center justify-center rounded-lg border transition-all duration-300"
                  style={{
                    height: '56px',
                    minWidth: '80px',
                    padding: '0 16px',
                    border: '1px solid rgba(255,255,255,0.08)',
                    background: 'rgba(255,255,255,0.02)',
                    color: 'rgba(255,255,255,0.35)',
                    fontFamily: 'var(--font-mono)',
                    fontSize: '11px',
                    letterSpacing: '0.1em',
                    textTransform: 'uppercase',
                    whiteSpace: 'nowrap',
                  }}
                  onMouseEnter={(e) => {
                    (e.currentTarget as HTMLDivElement).style.color = 'rgba(94,180,255,0.9)';
                    (e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(46,142,255,0.3)';
                  }}
                  onMouseLeave={(e) => {
                    (e.currentTarget as HTMLDivElement).style.color = 'rgba(255,255,255,0.35)';
                    (e.currentTarget as HTMLDivElement).style.borderColor = 'rgba(255,255,255,0.08)';
                  }}
                >
                  {item.name}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
