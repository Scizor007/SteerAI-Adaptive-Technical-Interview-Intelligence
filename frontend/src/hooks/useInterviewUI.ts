import { useCallback, useEffect, useState } from 'react';

import { continueInterview, startInterview } from '../api/interviewApi';
import type { CandidateProfile, Feedback, InterviewPhase } from '../types';

const TOTAL_QUESTIONS = 10;

function createSessionId(): string {
  return `interview-${crypto.randomUUID()}`;
}

function questionFromReply(reply: string): string {
  return reply.split('\n\n').filter(Boolean).pop() ?? reply;
}

/** UI state that delegates interview progression and scoring to the backend API. */
export function useInterviewUI(candidate: CandidateProfile | null) {
  const [phase, setPhase] = useState<InterviewPhase>('initializing');
  const [answer, setAnswer] = useState('');
  const [question, setQuestion] = useState('');
  const [questionIndex, setQuestionIndex] = useState(0);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [feedback, setFeedback] = useState<Feedback>();
  const [error, setError] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState('');

  useEffect(() => {
    if (!candidate) return;

    let active = true;
    const id = createSessionId();
    setSessionId(id);
    setPhase('initializing');
    setQuestionIndex(0);
    setQuestion('');
    setFeedback(undefined);
    setError(null);

    startInterview(id, candidate)
      .then((response) => {
        if (!active) return;
        setQuestion(questionFromReply(response.reply));
        setPhase(response.done ? 'complete' : 'asking');
        setFeedback(response.feedback);
      })
      .catch((requestError: unknown) => {
        if (!active) return;
        setError(requestError instanceof Error ? requestError.message : 'Unable to start the interview.');
      });

    return () => {
      active = false;
    };
  }, [candidate]);

  const submitAnswer = useCallback(async () => {
    if (!answer.trim() || !sessionId || isEvaluating) return;

    setPhase('evaluating');
    setIsEvaluating(true);
    setError(null);
    try {
      const response = await continueInterview(sessionId, answer.trim());
      setQuestionIndex((index) => index + 1);
      setAnswer('');
      setFeedback(response.feedback);
      if (response.done) {
        setPhase('complete');
      } else {
        setQuestion(response.reply);
        setPhase('asking');
      }
    } catch (requestError: unknown) {
      setPhase('asking');
      setError(requestError instanceof Error ? requestError.message : 'Unable to evaluate the answer.');
    } finally {
      setIsEvaluating(false);
    }
  }, [answer, isEvaluating, sessionId]);

  return {
    phase,
    answer,
    setAnswer,
    questionIndex,
    totalQuestions: TOTAL_QUESTIONS,
    currentQuestion: { topic: 'Current assessment topic', question },
    isEvaluating,
    submitAnswer,
    candidate,
    feedback,
    error,
  };
}
