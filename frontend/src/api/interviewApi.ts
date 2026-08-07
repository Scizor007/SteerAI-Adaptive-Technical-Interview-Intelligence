/**
 * API client layer.
 * All HTTP calls to the backend are centralized here.
 * UI components NEVER make direct API calls.
 */

import type {
  InterviewResponse,
  CandidateProfile,
  CandidatesData,
  Curriculum,
} from '../types';
import { API_BASE_URL } from '../constants/designTokens';

/**
 * Start a new interview session.
 */
export async function startInterview(
  sessionId: string,
  candidate: CandidateProfile
): Promise<InterviewResponse> {
  const response = await fetch(`${API_BASE_URL}/interview`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sessionId, candidate }),
  });

  if (!response.ok) {
    throw new Error(`Interview start failed: ${response.status}`);
  }

  return response.json();
}

/**
 * Continue an interview with a candidate message.
 */
export async function continueInterview(
  sessionId: string,
  message: string
): Promise<InterviewResponse> {
  const response = await fetch(`${API_BASE_URL}/interview`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sessionId, message }),
  });

  if (!response.ok) {
    throw new Error(`Interview continue failed: ${response.status}`);
  }

  return response.json();
}

/**
 * Load candidates from the static JSON.
 */
export async function fetchCandidates(): Promise<CandidatesData> {
  const response = await fetch('/candidates.json');
  if (!response.ok) {
    throw new Error(`Failed to load candidates: ${response.status}`);
  }
  return response.json();
}

/**
 * Load curriculum from the static JSON.
 */
export async function fetchCurriculum(): Promise<Curriculum> {
  const response = await fetch('/curriculum.json');
  if (!response.ok) {
    throw new Error(`Failed to load curriculum: ${response.status}`);
  }
  return response.json();
}

/**
 * Health check.
 */
export async function checkHealth(): Promise<{ status: string }> {
  const response = await fetch('/health');
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`);
  }
  return response.json();
}
