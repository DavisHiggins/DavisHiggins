// Single source of truth — edit anything here and it propagates across the site.

export const identityWords = [
  'Builder',
  'Analyst',
  'Athlete',
  'Founder',
  'Believer',
  'Brother',
];

export const bio =
  "Data Science junior at UNC Charlotte, AI minor, graduating May 2027. Data Analyst Intern at Kewaunee Scientific. Founder of Higgins Digital. Creator of Propify — a player-prop analytics platform powered by a custom ML pipeline.";

export const tagline = 'Data Science · Analytics · ML · Sports';

export type LinkTier = 'primary' | 'secondary' | 'tertiary';

export interface LinkItem {
  label: string;
  href: string;
  description?: string;
  icon: string; // lucide-react icon name
  tier: LinkTier;
}

export const links: LinkItem[] = [
  // PRIMARY
  {
    label: 'LinkedIn',
    href: 'https://linkedin.com/in/davishiggins',
    description: 'Professional profile · open to opportunities',
    icon: 'Linkedin',
    tier: 'primary',
  },
  {
    label: 'GitHub',
    href: 'https://github.com/DavisHiggins',
    description: 'Code, projects, and contributions',
    icon: 'Github',
    tier: 'primary',
  },
  {
    label: 'Portfolio',
    href: 'https://portfoliodbh.vercel.app',
    description: 'Full project portfolio',
    icon: 'LayoutGrid',
    tier: 'primary',
  },
  {
    label: 'Propify',
    href: 'https://propifysite.vercel.app',
    description: 'Player-prop analytics platform',
    icon: 'LineChart',
    tier: 'primary',
  },

  // SECONDARY
  {
    label: 'Higgins Digital',
    href: 'https://higginsd.com',
    description: 'Custom apparel & creative studio',
    icon: 'Sparkles',
    tier: 'secondary',
  },
  {
    label: 'PDT Chaplain',
    href: 'https://pdtchaplain.vercel.app',
    description: 'Phi Delta Theta chaplain platform',
    icon: 'Shield',
    tier: 'secondary',
  },
  {
    label: 'Personal Email',
    href: 'mailto:davishiggins@icloud.com',
    description: 'davishiggins@icloud.com',
    icon: 'Mail',
    tier: 'secondary',
  },
  {
    label: 'Work Email',
    href: 'mailto:davishiggins@higginsd.com',
    description: 'davishiggins@higginsd.com',
    icon: 'AtSign',
    tier: 'secondary',
  },

  // TERTIARY
  {
    label: '@davishigginss',
    href: 'https://instagram.com/davishigginss',
    description: 'Personal Instagram',
    icon: 'Instagram',
    tier: 'tertiary',
  },
  {
    label: '@higgins.digital',
    href: 'https://instagram.com/higgins.digital',
    description: 'Higgins Digital Instagram',
    icon: 'Instagram',
    tier: 'tertiary',
  },
];

// Marquee — affiliations & tools
export interface MarqueeItem {
  name: string;
  logo?: string; // optional local image path
}

export const marqueeItems: MarqueeItem[] = [
  { name: 'UNC Charlotte' },
  { name: 'Kewaunee Scientific' },
  { name: 'Higgins Digital', logo: '/logos/higgins-digital.png' },
  { name: 'Propify' },
  { name: 'Phi Delta Theta', logo: '/logos/phi-delta-theta.jpeg' },
  { name: 'Live Like Lou Foundation' },
  { name: 'Claude Code' },
  { name: 'DH', logo: '/logos/dh-monogram.jpeg' },
];

// Rotating footer verses
export const verses: { ref: string; text: string }[] = [
  {
    ref: 'Philippians 4:13',
    text: 'I can do all things through Christ who strengthens me.',
  },
  {
    ref: 'John 3:16',
    text: 'For God so loved the world that he gave his one and only Son.',
  },
  {
    ref: 'Jeremiah 29:11',
    text: 'For I know the plans I have for you, plans to prosper you and not to harm you.',
  },
  {
    ref: 'James 1:2-4',
    text: 'Consider it pure joy whenever you face trials of many kinds.',
  },
  {
    ref: 'Philippians 4:6',
    text: 'Do not be anxious about anything, but in every situation present your requests to God.',
  },
  {
    ref: 'Isaiah 40:11',
    text: 'He tends his flock like a shepherd; he gathers the lambs in his arms.',
  },
  {
    ref: 'Philippians 3:13',
    text: 'Forgetting what is behind and straining toward what is ahead.',
  },
  {
    ref: 'Colossians 3:23',
    text: 'Whatever you do, work at it with all your heart, as working for the Lord.',
  },
  {
    ref: 'Proverbs 3:5-6',
    text: 'Trust in the Lord with all your heart and lean not on your own understanding.',
  },
  {
    ref: 'Joshua 1:9',
    text: 'Be strong and courageous. Do not be afraid; the Lord your God will be with you.',
  },
];
