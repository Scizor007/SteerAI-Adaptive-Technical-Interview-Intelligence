import { useState, useEffect, useCallback } from 'react';
import { fetchCandidates } from '../api/interviewApi';
import { analyzeCandidate } from '../utils/candidateUtils';
import type { CandidateProfile } from '../types';

export interface EnrichedCandidate extends CandidateProfile {
  insights: ReturnType<typeof analyzeCandidate>;
}

export function useCandidates() {
  const [candidates, setCandidates] = useState<EnrichedCandidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchCandidates();
      setCandidates(
        data.candidates.map((c) => ({
          ...c,
          insights: analyzeCandidate(c),
        }))
      );
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load candidates');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const getById = useCallback(
    (id: string) => candidates.find((c) => c.member.id === id),
    [candidates]
  );

  return { candidates, loading, error, reload: load, getById };
}
