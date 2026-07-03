'use client';

import { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Image from 'next/image';
import { identityWords, bio, tagline } from '@/lib/data';

export default function Hero() {
  const nameRef = useRef<HTMLHeadingElement>(null);
  const [mouse, setMouse] = useState({ x: 0.5, y: 0.5 });
  const [hovering, setHovering] = useState(false);
  const [wordIndex, setWordIndex] = useState(0);

  useEffect(() => {
    const node = nameRef.current;
    if (!node) return;
    const handleMove = (e: MouseEvent) => {
      const rect = node.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      const y = (e.clientY - rect.top) / rect.height;
      setMouse({ x: Math.max(0, Math.min(1, x)), y: Math.max(0, Math.min(1, y)) });
    };
    node.addEventListener('mousemove', handleMove);
    return () => node.removeEventListener('mousemove', handleMove);
  }, []);

  useEffect(() => {
    if (!hovering) return;
    const interval = setInterval(() => {
      setWordIndex((i) => (i + 1) % identityWords.length);
    }, 380);
    return () => clearInterval(interval);
  }, [hovering]);

  return (
    <section className="relative isolate pt-20 pb-6 sm:pt-24 sm:pb-8">
      {/* Large radial blue glow behind hero */}
      <div
        className="pointer-events-none absolute left-1/4 top-0 -translate-x-1/2"
        style={{
          width: '700px',
          height: '500px',
          background: 'radial-gradient(ellipse at center, rgba(46,142,255,0.13) 0%, transparent 70%)',
          filter: 'blur(40px)',
        }}
        aria-hidden
      />

      <div className="relative z-10 mx-auto max-w-6xl px-8">
        <div className="grid grid-cols-1 items-center gap-10 md:grid-cols-[1fr_auto]">

          {/* LEFT — name, tagline, bio, status */}
          <div>
            {/* Status pill */}
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="mb-5 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-xs font-mono text-white/60 backdrop-blur"
            >
              <span className="relative flex h-1.5 w-1.5">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-electric-400 opacity-75" />
                <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-electric-400" />
              </span>
              Available for Summer 2026 internships
            </motion.div>

            {/* Name */}
            <h1
              ref={nameRef}
              onMouseEnter={() => setHovering(true)}
              onMouseLeave={() => setHovering(false)}
              className="relative inline-block cursor-default leading-[0.92] tracking-tight"
              style={{
                fontSize: 'clamp(3.5rem, 8vw, 6.5rem)',
              }}
            >
              <motion.span
                initial={{ opacity: 0, y: 14 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, delay: 0.1 }}
                className="block font-bold text-white"
                style={{ fontFamily: 'var(--font-body)' }}
              >
                Davis
              </motion.span>
              <motion.span
                initial={{ opacity: 0, y: 14 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.7, delay: 0.22 }}
                className="draw-underline block font-display italic"
                style={{
                  backgroundImage: hovering
                    ? `radial-gradient(circle at ${mouse.x * 100}% ${mouse.y * 100}%, rgba(94,180,255,1), rgba(46,142,255,0.7) 40%, rgba(255,255,255,0.95) 75%)`
                    : 'linear-gradient(135deg, #ffffff 60%, rgba(94,180,255,0.6) 100%)',
                  WebkitBackgroundClip: 'text',
                  backgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  transition: 'background-image 0.2s ease',
                }}
              >
                Higgins
              </motion.span>
            </h1>

            {/* Identity cycle */}
            <div className="mt-3 h-6 font-mono text-sm text-electric-400">
              <AnimatePresence mode="wait">
                {hovering && (
                  <motion.span
                    key={identityWords[wordIndex]}
                    initial={{ opacity: 0, y: 5 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -5 }}
                    transition={{ duration: 0.18 }}
                    className="inline-block"
                  >
                    {'> '}{identityWords[wordIndex]}
                  </motion.span>
                )}
              </AnimatePresence>
            </div>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="mt-3 font-mono text-xs uppercase tracking-[0.18em] text-white/40"
            >
              {tagline}
            </motion.p>

            <motion.p
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              className="mt-4 max-w-lg text-[0.95rem] leading-relaxed text-white/65"
            >
              {bio}
            </motion.p>
          </div>

          {/* RIGHT — photo */}
          <motion.div
            initial={{ opacity: 0, scale: 0.93 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.9, delay: 0.15 }}
            className="mx-auto md:mx-0"
          >
            <div className="relative h-52 w-52 sm:h-60 sm:w-60 md:h-72 md:w-72">
              {/* Outer glow ring */}
              <div
                className="absolute -inset-4 rounded-full opacity-50 blur-2xl"
                style={{
                  background: 'conic-gradient(from 180deg, rgba(46,142,255,0.55), rgba(94,180,255,0.15), rgba(46,142,255,0.55))',
                }}
              />
              {/* Inner ring border */}
              <div className="absolute -inset-1 rounded-full"
                style={{
                  background: 'linear-gradient(135deg, rgba(46,142,255,0.4), transparent 60%)',
                  borderRadius: '50%',
                }}
              />
              <div className="relative h-full w-full overflow-hidden rounded-full border border-white/10">
                <Image
                  src="/images/davis.jpeg"
                  alt="Davis Higgins"
                  fill
                  priority
                  sizes="(max-width: 768px) 208px, 288px"
                  className="object-cover object-top"
                />
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
