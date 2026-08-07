import { useState, useCallback } from 'react';
import type { CandidateProfile, InterviewPhase } from '../types';

/** UI-only interview state — no backend logic wired. */
export function useInterviewUI(candidate: CandidateProfile | null) {
  const [phase, setPhase] = useState<InterviewPhase>('asking');
  const [answer, setAnswer] = useState('');
  const [questionIndex, setQuestionIndex] = useState(0);
  const [isEvaluating, setIsEvaluating] = useState(false);

  const MOCK_QUESTIONS = [
    {
      topic: 'RAG Architecture',
      question:
        'Walk me through how you would design a retrieval-augmented generation pipeline for a document Q&A system. What components would you include and why?',
      followUp: 'How would you handle chunking strategy for mixed-format documents?',
    },
    {
      topic: 'Vector Databases',
      question:
        'Compare dense vs. sparse retrieval approaches. When would you choose one over the other in production?',
      followUp: null,
    },
    {
      topic: 'Agent Orchestration',
      question:
        'Describe a multi-agent workflow you have built or would build. How do agents coordinate and handle failures?',
      followUp: 'What observability would you add before shipping to production?',
    },
  ];

  const current = MOCK_QUESTIONS[questionIndex] ?? MOCK_QUESTIONS[0];

  const submitAnswer = useCallback(() => {
    if (!answer.trim()) return;
    setPhase('evaluating');
    setIsEvaluating(true);
    setTimeout(() => {
      setIsEvaluating(false);
      if (questionIndex < MOCK_QUESTIONS.length - 1) {
        setQuestionIndex((i) => i + 1);
        setAnswer('');
        setPhase('asking');
      } else {
        setPhase('complete');
      }
    }, 1800);
  }, [answer, questionIndex]);

  return {
    phase,
    answer,
    setAnswer,
    questionIndex,
    totalQuestions: MOCK_QUESTIONS.length,
    currentQuestion: current,
    isEvaluating,
    submitAnswer,
    candidate,
    coveragePct: candidate
      ? Math.round((candidate.signals.missionsCompleted / 31) * 100)
      : 0,
  };
}
