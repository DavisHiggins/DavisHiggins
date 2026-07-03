'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import { AnimatePresence, motion } from 'framer-motion';
import { verses } from '@/lib/data';

export default function Footer() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    setIndex(Math.floor(Math.random() * verses.length));
    const interval = setInterval(() => {
      setIndex((i) => (i + 1) % verses.length);
    }, 9000);
    return () => clearInterval(interval);
  }, []);

  const verse = verses[index];

  return (
    <footer
      className="relative py-8"
      style={{
        borderTop: '1px solid rgba(255,255,255,0.05)',
        background: 'rgba(2,4,8,0.7)',
        backdropFilter: 'blur(12px)',
      }}
    >
      <div className="mx-auto max-w-6xl px-8">
        {/* Rotating verse */}
        <div className="mb-6 min-h-[52px] text-center">
          <AnimatePresence mode="wait">
            <motion.blockquote
              key={verse.ref}
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -6 }}
              transition={{ duration: 0.5 }}
              className="mx-auto max-w-xl"
            >
              <p className="font-display text-base italic text-white/55 sm:text-lg">
                &ldquo;{verse.text}&rdquo;
              </p>
              <cite className="mt-1.5 block font-mono text-[11px] not-italic text-electric-400/80">
                — {verse.ref}
              </cite>
            </motion.blockquote>
          </AnimatePresence>
        </div>

        {/* Divider */}
        <div
          className="mb-5 h-px"
          style={{
            background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.07) 30%, rgba(255,255,255,0.07) 70%, transparent)',
          }}
        />

        {/* Bottom row */}
        <div className="flex flex-col items-center justify-between gap-3 sm:flex-row">
          <div className="flex items-center gap-3">
            {/* DH logo — mix-blend-mode screen removes white background */}
            <div
              className="relative h-8 w-8 overflow-hidden rounded"
              style={{ mixBlendMode: 'screen' }}
            >
              <Image
                src="/logos/dh-monogram.jpeg"
                alt="DH"
                fill
                sizes="32px"
                className="object-contain"
              />
            </div>
            <span className="font-mono text-xs text-white/40">
              © Davis Higgins 2026
            </span>
          </div>

          <div className="flex items-center gap-2 font-mono text-[11px] text-white/25">
            <span className="hidden sm:inline">designed &amp; deployed in Charlotte</span>
            <span className="hidden sm:inline text-white/15">·</span>
            <span>Next.js</span>
            <span className="text-white/15">/</span>
            <span>Tailwind</span>
            <span className="text-white/15">/</span>
            <span>Vercel</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
