/**
 * SteerAI design tokens — use in JS logic (charts, dynamic styles).
 * CSS custom properties live in index.css @theme block.
 */

export const COLORS = {
  bgPrimary: '#09090B',
  bgSecondary: '#111114',
  surface: '#1A1A1F',
  textPrimary: '#F4F4F5',
  textSecondary: '#8B8B95',
  border: '#2A2A30',
  accent: '#5E6AD2',
  signal: '#22C55E',
} as const;

export const SEMANTIC = {
  warning: '#EAB308',
  error: '#EF4444',
} as const;

export const FONTS = {
  display: "'Plus Jakarta Sans', system-ui, sans-serif",
  body: "'Inter', system-ui, sans-serif",
  mono: "'IBM Plex Mono', 'JetBrains Mono', monospace",
} as const;

export const SPACING = {
  xs: '0.25rem',
  sm: '0.5rem',
  md: '1rem',
  lg: '1.5rem',
  xl: '2rem',
  '2xl': '3rem',
  '3xl': '4rem',
} as const;

export const MOTION = {
  fast: 0.15,
  normal: 0.25,
  slow: 0.4,
  spring: { type: 'spring' as const, stiffness: 380, damping: 32 },
  ease: [0.22, 1, 0.36, 1] as const,
} as const;

export const LAYOUT = {
  maxContentWidth: 1400,
} as const;

export const BRAND = {
  name: 'SteerAI',
  tagline: 'Adaptive Technical Interview Intelligence',
} as const;

export const INTERVIEW_PHASES = [
  'initializing',
  'asking',
  'listening',
  'evaluating',
  'complete',
] as const;

export const PHASE_LABELS: Record<string, string> = {
  idle: 'Ready',
  initializing: 'Initializing',
  asking: 'Question Active',
  listening: 'Awaiting Response',
  evaluating: 'Evaluating',
  complete: 'Complete',
} as const;

export const API_BASE_URL = '/api';
export const MAX_QUESTIONS = 10;
