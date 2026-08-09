import { Link, useParams, useNavigate, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Download, TrendingUp, AlertTriangle } from 'lucide-react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  ResponsiveContainer,
} from 'recharts';
import { useEffect, useMemo } from 'react';
import { AppLayout } from '../../layouts';
import { useCandidates } from '../../hooks';
import { Badge, Button, LoadingState, Timeline } from '../../components/ui';
import { COLORS } from '../../constants/designTokens';
import type { Feedback } from '../../types';

export function FeedbackPage() {
  const { candidateId } = useParams<{ candidateId: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { getById, loading } = useCandidates();
  const candidate = candidateId ? getById(candidateId) : undefined;

  const report = useMemo(() => {
    const navigationFeedback = (location.state as { feedback?: Feedback } | null)?.feedback;
    if (navigationFeedback) return navigationFeedback;
    if (!candidateId) return null;
    const saved = sessionStorage.getItem(`steerai-feedback-${candidateId}`);
    return saved ? (JSON.parse(saved) as Feedback) : null;
  }, [candidateId, location.state]);

  useEffect(() => {
    if (!loading && candidateId && !candidate) {
      navigate('/candidates', { replace: true });
    }
  }, [loading, candidateId, candidate, navigate]);

  if (loading || !candidate) {
    return (
      <AppLayout>
        <LoadingState message="Finalizing assessment report…" />
      </AppLayout>
    );
  }

  if (!report) {
    return (
      <AppLayout>
        <LoadingState message="No completed assessment is available for this candidate." />
      </AppLayout>
    );
  }

  const { member } = candidate;
  const radarData = [
    ['Accuracy', report.accuracy],
    ['Reasoning', report.reasoning],
    ['Depth', report.depth],
    ['Completeness', report.completeness],
    ['Communication', report.communication],
    ['Confidence', report.confidence],
  ].map(([subject, score]) => ({ subject, score }));

  const handleDownload = () => {
    const blob = new Blob([JSON.stringify({ candidate: member, report }, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `steerai-report-${member.id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <AppLayout>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
        className="min-h-screen"
      >
        {/* Hero Section - Score */}
        <div className="border-b border-white/[0.08] bg-gradient-to-b from-indigo-500/5 to-transparent">
          <div className="mx-auto max-w-6xl px-6 py-20 md:py-32">
            <div className="flex flex-col items-center text-center">
              <Badge variant="accent" size="sm" className="mb-8">
                Assessment Complete
              </Badge>
              
              {/* Massive Score */}
              <div className="mb-10 flex items-end justify-center gap-3">
                <motion.span
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ delay: 0.2, duration: 0.5 }}
                  className="font-display text-[120px] font-bold leading-none tracking-[-0.04em] text-white md:text-[160px]"
                >
                  {report.overall_score}
                </motion.span>
                <span className="mb-6 text-4xl font-light text-gray-500 md:mb-8 md:text-5xl">
                  / 100
                </span>
              </div>

              {/* Candidate Info */}
              <h1 className="mb-3 font-display text-3xl font-semibold tracking-tight text-white md:text-4xl">
                {member.name}
              </h1>
              <p className="mb-12 text-lg text-gray-400">
                {member.jobRole} · {member.yearsExperience} years experience
              </p>

              {/* Actions */}
              <div className="flex flex-wrap items-center justify-center gap-4">
                <Button
                  variant="secondary"
                  size="lg"
                  className="rounded-full px-8"
                  leftIcon={<Download size={18} />}
                  onClick={handleDownload}
                >
                  Download Report
                </Button>
                <Link to="/candidates">
                  <Button variant="ghost" size="lg" className="rounded-full px-8">
                    View All Candidates
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* Executive Summary */}
        <div className="border-b border-white/[0.08] bg-white/[0.01]">
          <div className="mx-auto max-w-4xl px-6 py-20 text-center">
            <h2 className="mb-8 text-xs font-semibold uppercase tracking-[0.15em] text-gray-500">
              Executive Summary
            </h2>
            <p className="text-xl leading-relaxed text-gray-300 md:text-2xl md:leading-relaxed">
              {report.summary}
            </p>
          </div>
        </div>

        {/* Radar Chart + Strengths/Gaps */}
        <div className="border-b border-white/[0.08]">
          <div className="mx-auto max-w-6xl px-6 py-20">
            <h2 className="mb-12 text-center text-xs font-semibold uppercase tracking-[0.15em] text-gray-500">
              Performance Analysis
            </h2>
            
            <div className="grid gap-12 lg:grid-cols-[500px_1fr] lg:gap-16">
              {/* Radar Chart */}
              <div className="flex flex-col items-center">
                <div className="h-[400px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart data={radarData} outerRadius="75%">
                      <PolarGrid stroke={COLORS.border} strokeDasharray="3 3" />
                      <PolarAngleAxis
                        dataKey="subject"
                        tick={{ fill: COLORS.textSecondary, fontSize: 13, fontWeight: 500 }}
                      />
                      <Radar
                        dataKey="score"
                        stroke={COLORS.accent}
                        fill={COLORS.accent}
                        fillOpacity={0.2}
                        strokeWidth={2.5}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
                <p className="mt-4 text-center text-sm text-gray-500">
                  Six-dimensional skill assessment
                </p>
              </div>

              {/* Strengths & Gaps */}
              <div className="space-y-10">
                {/* Strengths */}
                <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-8">
                  <div className="mb-6 flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/10">
                      <TrendingUp size={20} className="text-emerald-400" />
                    </div>
                    <h3 className="text-lg font-semibold text-white">Demonstrated Strengths</h3>
                  </div>
                  <ul className="space-y-3">
                    {report.strengths.map((s) => (
                      <li key={s} className="flex gap-3 text-[15px] leading-relaxed text-gray-300">
                        <span className="mt-1 text-emerald-400">✓</span>
                        <span>{s}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Gaps */}
                <div className="rounded-2xl border border-amber-500/20 bg-amber-500/5 p-8">
                  <div className="mb-6 flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-500/10">
                      <AlertTriangle size={20} className="text-amber-400" />
                    </div>
                    <h3 className="text-lg font-semibold text-white">Areas for Development</h3>
                  </div>
                  <ul className="space-y-3">
                    {report.gaps.map((w) => (
                      <li key={w} className="flex gap-3 text-[15px] leading-relaxed text-gray-300">
                        <span className="mt-1 text-amber-400">!</span>
                        <span>{w}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Topic Mastery */}
        <div className="border-b border-white/[0.08] bg-white/[0.01]">
          <div className="mx-auto max-w-6xl px-6 py-20">
            <h2 className="mb-12 text-center text-xs font-semibold uppercase tracking-[0.15em] text-gray-500">
              Topic Mastery
            </h2>
            <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {Object.entries(report.topic_mastery).map(([topic, score]) => (
                <div
                  key={topic}
                  className="group rounded-2xl border border-white/[0.08] bg-white/[0.02] p-6 transition-all hover:border-indigo-500/30 hover:bg-white/[0.04]"
                >
                  <p className="mb-4 text-sm text-gray-400">{topic}</p>
                  <div className="flex items-baseline gap-2">
                    <p className="font-mono text-4xl font-bold tracking-tight text-white">{score}</p>
                    <span className="text-lg text-gray-600">%</span>
                  </div>
                  {/* Progress bar */}
                  <div className="mt-4 h-1.5 w-full overflow-hidden rounded-full bg-white/[0.05]">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${score}%` }}
                      transition={{ delay: 0.3, duration: 0.8 }}
                      className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-purple-500"
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recommended Path & Timeline */}
        <div className="border-b border-white/[0.08]">
          <div className="mx-auto max-w-6xl px-6 py-20">
            <div className="grid gap-16 lg:grid-cols-2">
              {/* Recommended Path */}
              <div>
                <h2 className="mb-10 text-xs font-semibold uppercase tracking-[0.15em] text-gray-500">
                  Recommended Learning Path
                </h2>
                <div className="space-y-6">
                  {report.next.map((step, i) => (
                    <div
                      key={step}
                      className="group flex gap-5 rounded-xl border border-white/[0.05] bg-white/[0.01] p-5 transition-all hover:border-indigo-500/20 hover:bg-white/[0.02]"
                    >
                      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-indigo-500/10 font-mono text-sm font-semibold text-indigo-400">
                        {(i + 1).toString().padStart(2, '0')}
                      </div>
                      <p className="text-[15px] leading-relaxed text-gray-300">{step}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Interview Timeline */}
              <div>
                <h2 className="mb-10 text-xs font-semibold uppercase tracking-[0.15em] text-gray-500">
                  Interview Evidence
                </h2>
                <Timeline
                  items={report.evidence.map((evidence, i) => ({
                    id: `${i}`,
                    label: `Response ${i + 1}`,
                    detail: evidence,
                    time: 'Recorded',
                    status: i === report.evidence.length - 1 ? 'active' : 'completed',
                  }))}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Footer CTA */}
        <div className="bg-gradient-to-b from-transparent to-indigo-500/5">
          <div className="mx-auto max-w-4xl px-6 py-20 text-center">
            <h2 className="mb-4 font-display text-2xl font-semibold text-white md:text-3xl">
              Assessment complete
            </h2>
            <p className="mb-8 text-lg text-gray-400">
              Download this report or review other candidates
            </p>
            <div className="flex flex-wrap items-center justify-center gap-4">
              <Button
                variant="secondary"
                size="lg"
                className="rounded-full px-8"
                leftIcon={<Download size={18} />}
                onClick={handleDownload}
              >
                Download JSON Report
              </Button>
              <Link to="/candidates">
                <Button variant="ghost" size="lg" className="rounded-full px-8">
                  Back to Roster
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </motion.div>
    </AppLayout>
  );
}
