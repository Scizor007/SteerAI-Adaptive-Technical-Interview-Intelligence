import type { CandidateProfile } from '../types';
import { analyzeCandidate } from './candidateUtils';

export interface SkillScore {
  skill: string;
  score: number;
}

export interface TimelineEvent {
  id: string;
  label: string;
  detail: string;
  time: string;
}

export interface MockFeedbackReport {
  overallScore: number;
  confidenceScore: number;
  skills: SkillScore[];
  strengths: string[];
  weaknesses: string[];
  recommendedTopics: string[];
  improvementPath: string[];
  timeline: TimelineEvent[];
  summary: string;
}

const SKILL_POOL = [
  'RAG Systems',
  'Prompt Engineering',
  'Vector Databases',
  'Agent Orchestration',
  'API Integration',
  'MLOps & Deployment',
  'System Design',
];

export function generateMockFeedback(candidate: CandidateProfile): MockFeedbackReport {
  const insights = analyzeCandidate(candidate);
  const base = insights.completionPct;

  const skills: SkillScore[] = SKILL_POOL.map((skill, i) => ({
    skill,
    score: Math.min(100, Math.max(35, base + (i % 3) * 8 - 12 + (candidate.signals.missionsFirstTry % 7))),
  }));

  const overallScore = Math.round(skills.reduce((a, s) => a + s.score, 0) / skills.length);

  return {
    overallScore,
    confidenceScore: Math.min(98, overallScore + 4),
    skills,
    strengths: insights.strengths.length
      ? insights.strengths
      : ['Strong foundational knowledge', 'Clear communication'],
    weaknesses: insights.weaknesses.length
      ? insights.weaknesses
      : ['Limited depth in advanced topics'],
    recommendedTopics: [
      'Multi-agent coordination patterns',
      'Production observability',
      'Evaluation frameworks for LLM apps',
    ],
    improvementPath: [
      'Review skipped curriculum modules',
      'Build a capstone with end-to-end deployment',
      'Practice system design for AI pipelines',
    ],
    timeline: [
      { id: '1', label: 'Session Started', detail: 'Profile analysis complete', time: '0:00' },
      { id: '2', label: 'RAG Architecture', detail: 'Strong conceptual answer', time: '4:12' },
      { id: '3', label: 'Follow-up Probe', detail: 'Chunking strategy discussed', time: '8:45' },
      { id: '4', label: 'Agent Design', detail: 'Partial — missing error handling', time: '14:20' },
      { id: '5', label: 'Evaluation', detail: 'Scoring complete', time: '22:08' },
    ],
    summary: `${candidate.member.name} demonstrated ${overallScore >= 75 ? 'solid' : 'developing'} technical depth across AI engineering topics. Performance aligned with curriculum signals — strengths in completed first-try missions, with gaps in areas requiring additional practice.`,
  };
}
