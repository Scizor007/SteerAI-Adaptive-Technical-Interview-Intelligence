import type { CandidateProfile, Mission } from '../types';

const TOTAL_DAYS = 31;

export interface CandidateInsights {
  completionPct: number;
  strengths: string[];
  weaknesses: string[];
  heatmap: { day: number; status: 'passed' | 'struggled' | 'skipped' | 'unknown' }[];
}

function missionStatus(m: Mission): CandidateInsights['heatmap'][0]['status'] {
  if (m.skipped) return 'skipped';
  if (m.passed && (m.attempts ?? 1) <= 1) return 'passed';
  if (m.passed && (m.attempts ?? 1) > 2) return 'struggled';
  if (m.passed) return 'passed';
  return 'unknown';
}

export function analyzeCandidate(candidate: CandidateProfile): CandidateInsights {
  const { missions, signals } = candidate;
  const completionPct = Math.round((signals.missionsCompleted / TOTAL_DAYS) * 100);

  const firstTry = missions.filter((m) => m.passed && (m.attempts ?? 1) === 1);
  const struggled = missions.filter((m) => m.passed && (m.attempts ?? 1) >= 3);
  const skipped = missions.filter((m) => m.skipped);

  const strengths = firstTry.slice(0, 4).map((m) => m.title);
  if (strengths.length === 0 && signals.missionsFirstTry > 0) {
    strengths.push('Consistent first-try completion');
  }

  const weaknesses = [
    ...struggled.slice(0, 3).map((m) => `${m.title} (${m.attempts} attempts)`),
    ...skipped.slice(0, 2).map((m) => `Skipped: ${m.title}`),
  ].slice(0, 4);

  if (weaknesses.length === 0 && completionPct < 80) {
    weaknesses.push('Incomplete curriculum coverage');
  }

  const heatmap = Array.from({ length: TOTAL_DAYS }, (_, i) => {
    const day = i + 1;
    const mission = missions.find((m) => m.day === day);
    return {
      day,
      status: mission ? missionStatus(mission) : 'unknown',
    };
  });

  return { completionPct, strengths, weaknesses, heatmap };
}

export function getInitials(name: string): string {
  return name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();
}

export function avatarHue(name: string): number {
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  return Math.abs(hash) % 360;
}
