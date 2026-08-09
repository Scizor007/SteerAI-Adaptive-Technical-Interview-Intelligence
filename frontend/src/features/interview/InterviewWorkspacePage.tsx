import { Link, useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ArrowLeft,
  CheckCircle2,
  Circle,
  Clock,
  HelpCircle,
  Loader2,
  Menu,
  Mic,
  MicOff,
  Paperclip,
  Radar,
  Send,
  Sparkles,
  ChevronLeft,
  Shield,
  Info,
  Lightbulb,
  BookOpen,
  ChevronRight,
  Zap,
  X,
} from 'lucide-react';
import { useEffect, useState } from 'react';
import { AppLayout } from '../../layouts';
import { useCandidates, useInterviewUI, useVoiceRecording } from '../../hooks';
import {
  Avatar,
  Textarea,
} from '../../components/ui';

const EVALUATION_STEPS = [
  'Analyzing your response...',
  'Checking technical depth...',
  'Evaluating architecture...',
  'Looking for trade-offs...',
  'Generating follow-up...',
];

const AVG_SECONDS_PER_QUESTION = 90;

function formatElapsed(totalSeconds: number) {
  const mins = Math.floor(totalSeconds / 60);
  const secs = totalSeconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Persistent right-hand "Live Evaluation" panel content (the panel's own
 * header/toolbar lives in the parent so it lines up with the main header).
 * Purely presentational — visualizes `isEvaluating` and the existing step
 * sequence. Never fabricates scores or results.
 */
function EvaluationPanel({
  isEvaluating,
  topic,
}: {
  isEvaluating: boolean;
  topic?: string;
}) {
  const [stepIndex, setStepIndex] = useState(0);
  const [dotIndex, setDotIndex] = useState(0);

  useEffect(() => {
    if (!isEvaluating) {
      setStepIndex(0);
      return;
    }
    const interval = setInterval(() => {
      setStepIndex((prev) => Math.min(prev + 1, EVALUATION_STEPS.length - 1));
    }, 800);
    return () => clearInterval(interval);
  }, [isEvaluating]);

  useEffect(() => {
    if (!isEvaluating) return;
    const interval = setInterval(() => {
      setDotIndex((prev) => (prev + 1) % 4);
    }, 400);
    return () => clearInterval(interval);
  }, [isEvaluating]);

  return (
    <div className="flex h-full w-full flex-col gap-5 overflow-y-auto p-5">
      {/* AI Orb */}
      <div
        className="flex flex-col items-center gap-5 rounded-2xl border px-5 py-9"
        style={{
          borderColor: 'rgba(129,140,248,0.18)',
          background: 'linear-gradient(180deg, rgba(99,102,241,0.10) 0%, rgba(255,255,255,0.02) 100%)',
        }}
      >
        <div className="relative flex h-24 w-24 items-center justify-center">
          <motion.div
            animate={isEvaluating ? { scale: [1, 1.25, 1], opacity: [0.35, 0.75, 0.35] } : { scale: 1, opacity: 0.22 }}
            transition={isEvaluating ? { duration: 2, repeat: Infinity, ease: 'easeInOut' } : {}}
            className="absolute inset-0 rounded-full border"
            style={{ borderColor: 'rgba(129,140,248,0.55)', background: 'rgba(99,102,241,0.10)' }}
          />
          <motion.div
            animate={isEvaluating ? { scale: [1, 1.12, 1] } : { scale: 1 }}
            transition={isEvaluating ? { duration: 1.6, repeat: Infinity, ease: 'easeInOut', delay: 0.3 } : {}}
            className="absolute inset-2 rounded-full border"
            style={{ borderColor: 'rgba(129,140,248,0.3)' }}
          />
          <div
            className="relative flex h-14 w-14 items-center justify-center rounded-full border"
            style={{ borderColor: 'rgba(165,180,252,0.5)', background: 'rgba(99,102,241,0.22)' }}
          >
            <Sparkles className={`h-6 w-6 text-indigo-300 ${isEvaluating ? 'animate-pulse' : 'opacity-60'}`} />
          </div>
        </div>

        <div className="text-center">
          <AnimatePresence mode="wait">
            <motion.p
              key={isEvaluating ? stepIndex : 'waiting'}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.3 }}
              className="text-[17px] font-semibold leading-snug tracking-[-0.01em] text-white"
            >
              {isEvaluating ? EVALUATION_STEPS[stepIndex] : 'Waiting for your answer'}
            </motion.p>
          </AnimatePresence>

          {isEvaluating && (
            <div className="mt-4 flex items-center justify-center gap-2">
              {[0, 1, 2, 3].map((i) => (
                <motion.div
                  key={i}
                  animate={{ opacity: dotIndex === i ? 1 : 0.25, scale: dotIndex === i ? 1.3 : 1 }}
                  transition={{ duration: 0.2 }}
                  className="h-1.5 w-1.5 rounded-full bg-indigo-400"
                />
              ))}
            </div>
          )}

          <p className="mt-3 text-[12.5px] leading-relaxed text-gray-500">
            {isEvaluating
              ? 'SteerAI is reviewing your response'
              : 'Analysis will begin once you send an answer'}
          </p>
        </div>
      </div>

      {/* Evaluation Steps */}
      <div
        className="rounded-2xl border p-4"
        style={{ borderColor: 'rgba(255,255,255,0.09)', background: 'rgba(255,255,255,0.035)' }}
      >
        <p className="mb-3.5 text-[10.5px] font-semibold uppercase tracking-[0.14em] text-gray-500">
          Evaluation Stages
        </p>
        <div className="flex flex-col gap-3.5">
          {EVALUATION_STEPS.map((step, i) => {
            const done = isEvaluating && i < stepIndex;
            const current = isEvaluating && i === stepIndex;
            const label = step.replace(/\.\.\.$/, '');
            return (
              <div key={step} className="flex items-center gap-3">
                <div className="flex h-5 w-5 shrink-0 items-center justify-center">
                  {done ? (
                    <CheckCircle2 size={16} className="text-indigo-400" />
                  ) : current ? (
                    <motion.div
                      animate={{ opacity: [0.5, 1, 0.5] }}
                      transition={{ duration: 1, repeat: Infinity }}
                      className="h-2 w-2 rounded-full bg-indigo-400"
                    />
                  ) : (
                    <Circle size={15} className="text-white/20" />
                  )}
                </div>
                <span
                  className={`text-[13px] transition-colors duration-300 ${
                    done
                      ? 'text-gray-500 line-through decoration-gray-600'
                      : current
                        ? 'font-medium text-white'
                        : 'text-gray-600'
                  }`}
                >
                  {label}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Evaluation status footer */}
      <AnimatePresence>
        {isEvaluating && (
          <motion.div
            initial={{ opacity: 0, y: 8, height: 0 }}
            animate={{ opacity: 1, y: 0, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="flex items-start gap-3 overflow-hidden rounded-xl border p-3.5"
            style={{ borderColor: 'rgba(129,140,248,0.25)', background: 'rgba(99,102,241,0.08)' }}
          >
            <Shield size={15} className="mt-0.5 shrink-0 text-indigo-400" />
            <div>
              <p className="text-xs font-medium text-indigo-300">Evaluation is in progress</p>
              <p className="mt-0.5 text-[11px] text-gray-500">This may take a few seconds.</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Topic */}
      {topic && (
        <div
          className="rounded-xl border p-3.5"
          style={{ borderColor: 'rgba(255,255,255,0.08)', background: 'rgba(255,255,255,0.03)' }}
        >
          <p className="mb-1 text-[10px] font-semibold uppercase tracking-widest text-gray-600">
            Assessing
          </p>
          <p className="text-xs font-medium text-gray-300">{topic}</p>
        </div>
      )}

      <div className="flex-1" />
    </div>
  );
}

export function InterviewWorkspacePage() {
  const { candidateId } = useParams<{ candidateId: string }>();
  const navigate = useNavigate();
  const { getById, loading } = useCandidates();
  const candidate = candidateId ? getById(candidateId) : undefined;
  const interview = useInterviewUI(candidate ?? null);

  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [elapsedSeconds, setElapsedSeconds] = useState(0);
  const [charCount, setCharCount] = useState(0);

  // Voice recording state
  const voice = useVoiceRecording();

  // Effect to update answer when voice transcript changes
  useEffect(() => {
    if (voice.transcript && voice.state === 'processing') {
      interview.setAnswer(voice.transcript.trim());
      voice.resetTranscript();
    }
  }, [voice.transcript, voice.state]);

  useEffect(() => {
    const interval = setInterval(() => setElapsedSeconds((s) => s + 1), 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    setCharCount(interview.answer.length);
  }, [interview.answer]);

  useEffect(() => {
    if (!loading && candidateId && !candidate) {
      navigate('/candidates', { replace: true });
    }
  }, [loading, candidateId, candidate, navigate]);

  if (loading || !candidate) {
    return (
      <div
        className="flex h-screen flex-col items-center justify-center gap-4"
        style={{ background: '#08080d' }}
      >
        <div className="relative">
          <div className="absolute inset-0 rounded-full bg-indigo-500/20 blur-xl" />
          <Loader2 className="relative h-8 w-8 animate-spin text-indigo-400" />
        </div>
        <p className="font-mono text-xs uppercase tracking-widest text-gray-600">
          Loading session...
        </p>
      </div>
    );
  }

  const { member } = candidate;

  if (interview.phase === 'complete') {
    if (interview.feedback) {
      sessionStorage.setItem(`steerai-feedback-${member.id}`, JSON.stringify(interview.feedback));
    }
    navigate(`/feedback/${member.id}`, { replace: true, state: { feedback: interview.feedback } });
    return null;
  }

  const currentQuestionNumber = interview.questionIndex + 1;
  const progressPercent = (currentQuestionNumber / interview.totalQuestions) * 100;
  const remainingQuestions = interview.totalQuestions - currentQuestionNumber;
  const estimatedMinutesLeft = Math.max(
    1,
    Math.round((remainingQuestions * AVG_SECONDS_PER_QUESTION) / 60)
  );

  const difficulty = (interview.currentQuestion as { difficulty?: string })?.difficulty;
  const questionDescription = (interview.currentQuestion as { description?: string })?.description;
  const experienceTag = (member as { experienceLevel?: string })?.experienceLevel;
  const yoeTag = (member as { yearsOfExperience?: string | number })?.yearsOfExperience;
  const email = (member as { email?: string })?.email;

  const difficultyStyle =
    difficulty === 'Hard'
      ? { borderColor: 'rgba(248,113,113,0.35)', background: 'rgba(248,113,113,0.10)', color: '#fca5a5' }
      : difficulty === 'Medium'
        ? { borderColor: 'rgba(251,191,36,0.35)', background: 'rgba(251,191,36,0.10)', color: '#fcd34d' }
        : { borderColor: 'rgba(52,211,153,0.35)', background: 'rgba(52,211,153,0.10)', color: '#6ee7b7' };

  return (
    <AppLayout fullBleed hideNav>
      <div
        className="relative flex h-screen overflow-hidden"
        style={{ background: '#08080d' }}
      >
        {/* Ambient glows */}
        <div className="pointer-events-none absolute inset-0 overflow-hidden">
          <div
            className="absolute -left-56 -top-56 h-[480px] w-[480px] rounded-full"
            style={{ background: 'radial-gradient(circle, rgba(99,102,241,0.14), transparent 70%)', filter: 'blur(50px)' }}
          />
          <div
            className="absolute -bottom-56 -right-56 h-[480px] w-[480px] rounded-full"
            style={{ background: 'radial-gradient(circle, rgba(139,92,246,0.10), transparent 70%)', filter: 'blur(50px)' }}
          />
          {/* Faint technical grid — signature texture, kept very subtle */}
          <div
            className="absolute inset-0 opacity-[0.035]"
            style={{
              backgroundImage:
                'linear-gradient(rgba(255,255,255,0.6) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.6) 1px, transparent 1px)',
              backgroundSize: '56px 56px',
            }}
          />
        </div>

        {/* ── Left Sidebar ── */}
        <AnimatePresence initial={false}>
          {sidebarOpen && (
            <motion.aside
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: 252, opacity: 1 }}
              exit={{ width: 0, opacity: 0 }}
              transition={{ type: 'spring', stiffness: 300, damping: 32 }}
              className="relative z-20 flex h-full shrink-0 flex-col overflow-hidden border-r"
              style={{ borderColor: 'rgba(255,255,255,0.08)', background: 'rgba(255,255,255,0.025)' }}
            >
              <div className="flex w-[252px] flex-1 flex-col overflow-hidden">
                {/* Brand — matches header height on the right for alignment */}
                <div
                  className="flex h-[65px] shrink-0 items-center justify-between border-b px-4"
                  style={{ borderColor: 'rgba(255,255,255,0.06)' }}
                >
                  <Link to="/" className="flex items-center gap-2">
                    <div
                      className="flex h-7 w-7 items-center justify-center rounded-lg border"
                      style={{ borderColor: 'rgba(129,140,248,0.35)', background: 'rgba(99,102,241,0.12)' }}
                    >
                      <Sparkles className="h-3.5 w-3.5 text-indigo-400" />
                    </div>
                    <span className="text-sm font-bold tracking-tight text-white">SteerAI</span>
                  </Link>
                  <button
                    onClick={() => setSidebarOpen(false)}
                    className="rounded-lg p-1.5 text-gray-500 transition-colors hover:bg-white/5 hover:text-gray-300"
                    title="Collapse sidebar"
                  >
                    <ChevronLeft size={15} />
                  </button>
                </div>

                <div className="flex flex-1 flex-col gap-4 overflow-y-auto p-4">
                  {/* Candidate Card */}
                  <div
                    className="rounded-2xl border p-4"
                    style={{ borderColor: 'rgba(255,255,255,0.09)', background: 'rgba(255,255,255,0.035)' }}
                  >
                    <div className="flex items-center gap-3">
                      <div className="relative shrink-0">
                        <div className="absolute inset-0 rounded-full bg-indigo-500/30 blur-md" />
                        <Avatar name={member.name} size="md" className="relative" />
                      </div>
                      <div className="min-w-0">
                        <p className="truncate text-[16px] font-semibold tracking-[-0.01em] text-white">
                          {member.name}
                        </p>
                        <p className="truncate text-[12.5px] text-gray-500">{member.jobRole}</p>
                      </div>
                    </div>
                    {email && (
                      <p className="mt-3 truncate text-[11.5px] text-gray-600">{email}</p>
                    )}
                    <div className="mt-3.5 flex items-center gap-2">
                      <span className="relative flex h-2 w-2">
                        <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-60" />
                        <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
                      </span>
                      <span className="text-[12.5px] font-medium text-emerald-400">
                        {experienceTag ?? 'Active Session'}
                      </span>
                    </div>
                    {yoeTag && (
                      <div
                        className="mt-3 rounded-lg border px-3 py-2 text-center"
                        style={{ borderColor: 'rgba(255,255,255,0.07)', background: 'rgba(255,255,255,0.03)' }}
                      >
                        <span className="text-[12.5px] text-gray-400">{yoeTag} Years Experience</span>
                      </div>
                    )}
                  </div>

                  {/* Progress */}
                  <div
                    className="rounded-2xl border p-4"
                    style={{ borderColor: 'rgba(255,255,255,0.09)', background: 'rgba(255,255,255,0.035)' }}
                  >
                    <div className="flex items-center justify-between">
                      <p className="text-[10.5px] font-semibold uppercase tracking-[0.13em] text-gray-500">
                        Progress
                      </p>
                      <p className="text-[12px] text-gray-500">
                        {currentQuestionNumber} / {interview.totalQuestions}
                      </p>
                    </div>
                    <div className="mt-3 h-1.5 w-full overflow-hidden rounded-full" style={{ background: 'rgba(255,255,255,0.08)' }}>
                      <motion.div
                        className="h-full rounded-full"
                        style={{ background: 'linear-gradient(90deg, #6366f1, #a78bfa)' }}
                        initial={{ width: 0 }}
                        animate={{ width: `${progressPercent}%` }}
                        transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
                      />
                    </div>
                    <p className="mt-2.5 text-[12px] text-gray-500">{Math.round(progressPercent)}% complete</p>
                  </div>

                  {/* Session Info */}
                  <div
                    className="rounded-2xl border p-4"
                    style={{ borderColor: 'rgba(255,255,255,0.09)', background: 'rgba(255,255,255,0.035)' }}
                  >
                    <p className="mb-3.5 text-[10.5px] font-semibold uppercase tracking-[0.13em] text-gray-500">
                      Session Info
                    </p>
                    <div className="space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="flex items-center gap-1.5 text-[12.5px] text-gray-500">
                          <Clock size={13} /> Total Time
                        </span>
                        <span className="font-mono text-[12.5px] font-medium text-gray-300">
                          {formatElapsed(elapsedSeconds)}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-[12.5px] text-gray-500">Questions Left</span>
                        <span className="font-mono text-[12.5px] font-medium text-gray-300">
                          {remainingQuestions}
                        </span>
                      </div>
                      <div className="flex items-center justify-between">
                        <span className="text-[12.5px] text-gray-500">Est. Time Left</span>
                        <span className="font-mono text-[12.5px] font-medium text-gray-300">
                          {estimatedMinutesLeft} min
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Quick Tips */}
                  <div
                    className="rounded-2xl border p-4"
                    style={{ borderColor: 'rgba(255,255,255,0.09)', background: 'rgba(255,255,255,0.035)' }}
                  >
                    <div className="mb-2 flex items-center gap-2">
                      <Lightbulb size={14} className="text-amber-400" />
                      <p className="text-[12.5px] font-semibold text-white">Quick Tips</p>
                    </div>
                    <p className="text-[12.5px] leading-relaxed text-gray-500">
                      Think out loud. Discuss trade-offs, assumptions, and alternatives. We value
                      your reasoning.
                    </p>
                  </div>

                  <button
                    className="flex items-center justify-between rounded-xl border px-4 py-3 text-xs text-gray-500 transition-colors hover:text-gray-300"
                    style={{ borderColor: 'rgba(255,255,255,0.07)', background: 'rgba(255,255,255,0.02)' }}
                  >
                    <div className="flex items-center gap-2">
                      <BookOpen size={13} />
                      <span>Interview Guidelines</span>
                    </div>
                    <ChevronRight size={13} />
                  </button>
                </div>
              </div>
            </motion.aside>
          )}
        </AnimatePresence>

        {/* ── Main Area ── */}
        <div className="relative z-10 flex min-w-0 flex-1 flex-col">
          <header
            className="flex h-[65px] shrink-0 items-center gap-4 border-b px-6"
            style={{ borderColor: 'rgba(255,255,255,0.07)', background: 'rgba(255,255,255,0.015)' }}
          >
            <Link
              to="/candidates"
              className="flex shrink-0 items-center gap-2 text-sm text-gray-500 transition-colors hover:text-white"
            >
              <ArrowLeft size={15} />
              <span className="hidden sm:inline">Back to Candidates</span>
            </Link>

            <div className="flex min-w-0 flex-1 flex-col items-center gap-1.5">
              <p className="text-xs font-medium text-gray-400">
                Question {currentQuestionNumber} of {interview.totalQuestions}
              </p>
              <div className="w-full max-w-xs">
                <div className="h-1 w-full overflow-hidden rounded-full" style={{ background: 'rgba(255,255,255,0.08)' }}>
                  <motion.div
                    className="h-full rounded-full"
                    style={{ background: 'linear-gradient(90deg, #6366f1, #a78bfa)' }}
                    initial={{ width: 0 }}
                    animate={{ width: `${progressPercent}%` }}
                    transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
                  />
                </div>
              </div>
            </div>

            <div className="flex shrink-0 items-center gap-4">
              <div className="hidden items-center gap-1.5 text-gray-500 sm:flex">
                <Clock size={13} />
                <span className="font-mono text-xs">{formatElapsed(elapsedSeconds)}</span>
              </div>
              <div className="hidden items-center gap-1.5 text-gray-500 md:flex">
                <Clock size={13} />
                <span className="font-mono text-xs">{estimatedMinutesLeft} min left</span>
              </div>
              <button
                onClick={() => setSidebarOpen((v) => !v)}
                className="rounded-lg p-1.5 text-gray-500 transition-colors hover:bg-white/5 hover:text-gray-300"
                title="Toggle sidebar"
              >
                <Menu size={16} />
              </button>
            </div>
          </header>

          <div className="flex min-h-0 flex-1">
            {/* Main content */}
            <main className="min-w-0 flex-1 overflow-y-auto px-8 py-6">
              <div className="mx-auto flex w-full max-w-3xl flex-col gap-5">
                {/* Question Card */}
                <AnimatePresence mode="wait">
                  <motion.div
                    key={interview.questionIndex}
                    initial={{ opacity: 0, y: 16 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -16 }}
                    transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
                    className="relative overflow-hidden rounded-2xl border p-6"
                    style={{
                      borderColor: 'rgba(255,255,255,0.09)',
                      background: 'linear-gradient(150deg, rgba(99,102,241,0.09) 0%, rgba(255,255,255,0.025) 55%)',
                    }}
                  >
                    <div
                      className="pointer-events-none absolute -right-16 -top-16 h-44 w-44 rounded-full"
                      style={{ background: 'radial-gradient(circle, rgba(99,102,241,0.28), transparent 70%)', filter: 'blur(30px)' }}
                    />

                    <div className="relative flex flex-wrap items-center gap-2">
                      <span
                        className="rounded-md border px-2.5 py-1 text-[11px] font-medium"
                        style={{ borderColor: 'rgba(129,140,248,0.35)', background: 'rgba(99,102,241,0.12)', color: '#a5b4fc' }}
                      >
                        {interview.currentQuestion.topic}
                      </span>
                      {difficulty && (
                        <span
                          className="rounded-md border px-2.5 py-1 text-[11px] font-medium"
                          style={difficultyStyle}
                        >
                          {difficulty}
                        </span>
                      )}
                    </div>

                    <div className="relative mt-4 flex items-center gap-2">
                      <span className="font-mono text-[11px] font-bold uppercase tracking-[0.14em] text-indigo-400">
                        Question {currentQuestionNumber}
                      </span>
                      <span className="text-gray-700">/</span>
                      <span className="font-mono text-[11px] uppercase tracking-[0.12em] text-gray-600">
                        of {interview.totalQuestions}
                      </span>
                    </div>

                    <h2 className="relative mt-3 break-words text-[1.6rem] font-semibold leading-[1.28] tracking-[-0.015em] text-white sm:text-[1.85rem]">
                      {interview.currentQuestion.question}
                    </h2>

                    {questionDescription && (
                      <p className="relative mt-3 text-[14.5px] leading-relaxed text-gray-400">
                        {questionDescription}
                      </p>
                    )}

                    <div
                      className="relative mt-5 flex items-center gap-4 border-t pt-4"
                      style={{ borderColor: 'rgba(255,255,255,0.06)' }}
                    >
                      <div className="flex items-center gap-1.5 text-gray-600">
                        <Clock size={13} />
                        <span className="text-xs">~90 sec avg.</span>
                      </div>
                      <div className="flex items-center gap-1.5 text-gray-600">
                        <Zap size={13} />
                        <span className="text-xs">AI evaluated</span>
                      </div>
                    </div>

                    {interview.error && (
                      <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="relative mt-4 rounded-lg border px-3 py-2 text-sm"
                        style={{ borderColor: 'rgba(248,113,113,0.3)', background: 'rgba(248,113,113,0.1)', color: '#fca5a5' }}
                      >
                        {interview.error}
                      </motion.p>
                    )}
                  </motion.div>
                </AnimatePresence>

                {/* Answer Composer */}
                <div
                  className={`relative flex flex-col overflow-hidden rounded-2xl border transition-all duration-300 ${
                    interview.isEvaluating ? 'opacity-60' : ''
                  }`}
                  style={{
                    borderColor: interview.isEvaluating ? 'rgba(255,255,255,0.07)' : 'rgba(255,255,255,0.1)',
                    background: 'rgba(255,255,255,0.03)',
                  }}
                >
                  <div
                    className="flex items-center justify-between border-b px-5 py-3.5"
                    style={{ borderColor: 'rgba(255,255,255,0.06)' }}
                  >
                    <span className="text-[14px] font-semibold tracking-[-0.01em] text-indigo-200">
                      Your Answer
                    </span>
                    <div className="flex items-center gap-3">
                      {/* Voice Recording Indicator */}
                      {voice.state === 'listening' && (
                        <motion.div
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          className="flex items-center gap-2 rounded-full border border-red-500/30 bg-red-500/10 px-3 py-1.5"
                        >
                          <motion.div
                            animate={{ scale: [1, 1.2, 1] }}
                            transition={{ repeat: Infinity, duration: 1.5 }}
                            className="h-2 w-2 rounded-full bg-red-500"
                          />
                          <span className="text-xs font-medium text-red-400">
                            Recording {formatElapsed(voice.duration)}
                          </span>
                        </motion.div>
                      )}
                      
                      {voice.state === 'processing' && (
                        <motion.div
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          className="flex items-center gap-2 text-indigo-400"
                        >
                          <Loader2 size={14} className="animate-spin" />
                          <span className="text-xs font-medium">Transcribing...</span>
                        </motion.div>
                      )}
                      
                      <div className="hidden items-center gap-1.5 text-gray-600 sm:flex">
                        <Info size={13} />
                        <span className="text-[11.5px]">Markdown is supported</span>
                      </div>
                    </div>
                  </div>

                  <Textarea
                    placeholder="Type your answer here..."
                    value={interview.answer}
                    onChange={(e) => interview.setAnswer(e.target.value)}
                    className="min-h-[220px] w-full resize-none border-0 bg-transparent px-5 py-5 text-[15px] leading-relaxed text-gray-200 placeholder:text-gray-700 focus:ring-0"
                    autoFocus
                    disabled={interview.isEvaluating}
                  />

                  <div
                    className="flex flex-wrap items-center justify-between gap-3 border-t px-4 py-3"
                    style={{ borderColor: 'rgba(255,255,255,0.06)', background: 'rgba(255,255,255,0.015)' }}
                  >
                    <div className="flex items-center gap-3">
                      {/* Voice Recording Controls */}
                      {voice.isSupported ? (
                        <>
                          {voice.state === 'idle' && (
                            <motion.button
                              whileHover={{ scale: 1.05 }}
                              whileTap={{ scale: 0.95 }}
                              onClick={voice.startRecording}
                              disabled={interview.isEvaluating}
                              className="flex items-center gap-2 rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-[13px] text-gray-300 transition-all hover:border-indigo-500/30 hover:bg-indigo-500/10 hover:text-indigo-300 disabled:opacity-40"
                              title="Use voice input"
                            >
                              <Mic size={14} />
                              <span>Speak</span>
                            </motion.button>
                          )}
                          
                          {voice.state === 'listening' && (
                            <div className="flex items-center gap-2">
                              <motion.button
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={voice.stopRecording}
                                className="flex items-center gap-2 rounded-lg border border-emerald-500/30 bg-emerald-500/10 px-3 py-2 text-[13px] text-emerald-300 transition-all hover:bg-emerald-500/20"
                              >
                                <MicOff size={14} />
                                <span>Stop</span>
                              </motion.button>
                              
                              <button
                                onClick={voice.cancelRecording}
                                className="flex items-center gap-1.5 rounded-lg px-2 py-2 text-gray-500 transition-colors hover:text-gray-300"
                                title="Cancel recording"
                              >
                                <X size={14} />
                              </button>
                            </div>
                          )}
                          
                          {voice.state === 'error' && (
                            <div className="flex items-center gap-2 text-xs text-red-400">
                              <MicOff size={14} />
                              <span>{voice.error}</span>
                              <button
                                onClick={voice.resetTranscript}
                                className="ml-1 text-gray-500 hover:text-gray-300"
                              >
                                <X size={12} />
                              </button>
                            </div>
                          )}
                        </>
                      ) : null}
                      
                      <button
                        disabled
                        className="flex items-center gap-1.5 rounded-lg px-3 py-2 text-[13px] text-gray-600 transition-colors disabled:opacity-40"
                      >
                        <Paperclip size={14} />
                        Attach Diagram
                      </button>
                      <span className="text-[12.5px] text-gray-700">{charCount} chars</span>
                    </div>

                    <motion.button
                      whileHover={!interview.isEvaluating && interview.answer.trim() ? { scale: 1.03 } : {}}
                      whileTap={!interview.isEvaluating && interview.answer.trim() ? { scale: 0.97 } : {}}
                      onClick={interview.submitAnswer}
                      disabled={!interview.answer.trim() || interview.isEvaluating}
                      className="flex items-center gap-2.5 rounded-xl px-5 py-2.5 text-[14px] font-semibold text-white transition-all duration-200 disabled:opacity-40"
                      style={{
                        background:
                          interview.answer.trim() && !interview.isEvaluating
                            ? 'linear-gradient(135deg, #6366f1, #8b5cf6)'
                            : 'rgba(255,255,255,0.07)',
                        boxShadow:
                          interview.answer.trim() && !interview.isEvaluating
                            ? '0 4px 20px rgba(99,102,241,0.3)'
                            : 'none',
                      }}
                    >
                      {interview.isEvaluating ? (
                        <>
                          <Loader2 size={16} className="animate-spin" />
                          <span>Evaluating...</span>
                        </>
                      ) : (
                        <>
                          <Send size={16} />
                          <span>Send Answer</span>
                        </>
                      )}
                    </motion.button>
                  </div>
                </div>

                {/* Need Help */}
                <div
                  className="flex items-center justify-between rounded-xl border px-4 py-3"
                  style={{ borderColor: 'rgba(255,255,255,0.07)', background: 'rgba(255,255,255,0.025)' }}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full border"
                      style={{ borderColor: 'rgba(255,255,255,0.1)', background: 'rgba(255,255,255,0.04)' }}
                    >
                      <HelpCircle size={14} className="text-gray-500" />
                    </div>
                    <div>
                      <p className="text-xs font-medium text-gray-400">Need help?</p>
                      <p className="text-[11px] text-gray-600">You can request a hint or clarification.</p>
                    </div>
                  </div>
                  <button
                    className="flex shrink-0 items-center gap-1.5 rounded-lg border px-3 py-1.5 text-xs font-medium transition-all"
                    style={{ borderColor: 'rgba(129,140,248,0.3)', background: 'rgba(99,102,241,0.08)', color: '#a5b4fc' }}
                  >
                    <HelpCircle size={12} />
                    Request Hint
                  </button>
                </div>
              </div>
            </main>

            {/* Right Evaluation Panel */}
            <aside
              className="hidden w-[320px] shrink-0 flex-col border-l xl:flex"
              style={{ borderColor: 'rgba(255,255,255,0.08)', background: 'rgba(255,255,255,0.02)' }}
            >
              <div
                className="flex h-[65px] shrink-0 items-center justify-between border-b px-5"
                style={{ borderColor: 'rgba(255,255,255,0.07)' }}
              >
                <div className="flex items-center gap-2.5">
                  <Radar size={15} className="text-indigo-400" />
                  <p className="text-[15px] font-semibold tracking-[-0.01em] text-white">Live Evaluation</p>
                </div>
                <div
                  className="flex items-center gap-2 rounded-full border px-2.5 py-1"
                  style={{ borderColor: 'rgba(255,255,255,0.1)', background: 'rgba(255,255,255,0.04)' }}
                >
                  <motion.span
                    className="h-1.5 w-1.5 rounded-full"
                    style={{ background: interview.isEvaluating ? '#818cf8' : '#6b7280' }}
                    animate={interview.isEvaluating ? { opacity: [0.4, 1, 0.4] } : { opacity: 0.6 }}
                    transition={interview.isEvaluating ? { duration: 1.2, repeat: Infinity, ease: 'easeInOut' } : undefined}
                  />
                  <span className="font-mono text-[10px] uppercase tracking-[0.1em] text-gray-400">
                    {interview.isEvaluating ? 'Analyzing' : 'Ready'}
                  </span>
                </div>
              </div>

              <EvaluationPanel
                isEvaluating={interview.isEvaluating}
                topic={interview.currentQuestion.topic}
              />
            </aside>
          </div>
        </div>
      </div>
    </AppLayout>
  );
}