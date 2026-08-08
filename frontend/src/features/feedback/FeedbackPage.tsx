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
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
        className="mx-auto max-w-5xl px-4 py-8 md:py-16"
      >
        {/* Clean Header & Massive Hero Score */}
        <div className="mb-20 flex flex-col items-center text-center">
          <Badge variant="accent" size="sm" className="mb-6">
            Assessment Complete
          </Badge>
          
          <div className="mb-8 flex items-center justify-center gap-4 text-text-primary">
            <span className="font-display text-8xl md:text-[140px] font-bold tracking-tighter leading-none">
              {report.overall_score}
            </span>
            <span className="text-2xl md:text-4xl font-light text-text-secondary mt-auto pb-4 md:pb-8">
              / 100
            </span>
          </div>

          <h1 className="font-display text-3xl font-semibold text-text-primary mb-4">
            {member.name}
          </h1>
          <p className="text-text-secondary text-lg font-light flex items-center gap-2">
            {member.jobRole} · {member.yearsExperience} yrs experience
          </p>

          <div className="mt-10 flex gap-4">
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
              <Button variant="ghost" size="lg" className="rounded-full px-8 text-text-secondary">
                View Roster
              </Button>
            </Link>
          </div>
        </div>

        {/* Executive Summary (No Card, just typography) */}
        <section className="mb-24 text-center max-w-3xl mx-auto">
          <h2 className="mb-6 text-sm font-medium tracking-widest uppercase text-text-secondary">
            Executive Summary
          </h2>
          <p className="text-xl leading-relaxed text-text-primary font-light">
            {report.summary}
          </p>
        </section>

        <hr className="border-border/40 mb-24" />

        {/* Core Analysis (Radar + Strengths/Weaknesses) */}
        <div className="grid gap-16 lg:grid-cols-[1fr_400px] mb-24">
          <div>
            <h2 className="mb-10 text-sm font-medium tracking-widest uppercase text-text-secondary">
              Skill Breakdown
            </h2>
            <div className="h-80 w-full mb-8">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData} outerRadius="70%">
                  <PolarGrid stroke={COLORS.border} strokeDasharray="3 3" />
                  <PolarAngleAxis
                    dataKey="subject"
                    tick={{ fill: COLORS.textSecondary, fontSize: 12, fontWeight: 300 }}
                  />
                  <Radar
                    dataKey="score"
                    stroke={COLORS.accent}
                    fill={COLORS.accent}
                    fillOpacity={0.15}
                    strokeWidth={2}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="space-y-12">
            <div>
              <h3 className="mb-4 flex items-center gap-3 font-display text-lg font-semibold text-text-primary">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-signal/10 text-signal">
                  <TrendingUp size={16} />
                </span>
                Demonstrated Strengths
              </h3>
              <ul className="space-y-3">
                {report.strengths.map((s) => (
                  <li key={s} className="text-base text-text-secondary font-light">
                    {s}
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="mb-4 flex items-center gap-3 font-display text-lg font-semibold text-text-primary">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-warning/10 text-warning">
                  <AlertTriangle size={16} />
                </span>
                Identified Gaps
              </h3>
              <ul className="space-y-3">
              {report.gaps.map((w) => (
                  <li key={w} className="text-base text-text-secondary font-light">
                    {w}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <hr className="border-border/40 mb-24" />

        {/* Learning & Timeline (Side by side) */}
        <div className="grid gap-16 lg:grid-cols-2 mb-24">
          <div>
            <h2 className="mb-8 text-sm font-medium tracking-widest uppercase text-text-secondary">
              Recommended Path
            </h2>
            <div className="space-y-6">
              {report.next.map((step, i) => (
                <div key={step} className="flex gap-4">
                  <span className="font-mono text-sm text-text-secondary opacity-50 mt-1">
                    {(i + 1).toString().padStart(2, '0')}
                  </span>
                  <span className="text-base text-text-primary font-light">{step}</span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="mb-8 text-sm font-medium tracking-widest uppercase text-text-secondary">
              Interview Timeline
            </h2>
            <Timeline
              items={report.evidence.map((evidence, i) => ({
                id: `${i}`,
                label: `Interview evidence ${i + 1}`,
                detail: evidence,
                time: 'Recorded',
                status: i === report.evidence.length - 1 ? 'active' : 'completed',
              }))}
            />
          </div>
        </div>
        
        {/* Evidence-based topic mastery */}
        <div className="rounded-3xl bg-surface/30 p-10 text-center">
          <h2 className="mb-8 text-sm font-medium tracking-widest uppercase text-text-secondary">
            Topic Mastery
          </h2>
          <div className="mx-auto grid max-w-3xl gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {Object.entries(report.topic_mastery).map(([topic, score]) => (
              <div key={topic} className="rounded-2xl border border-border/60 px-5 py-4 text-left">
                <p className="text-sm text-text-secondary">{topic}</p>
                <p className="mt-2 font-mono text-2xl text-text-primary">{score}%</p>
              </div>
            ))}
          </div>
        </div>
      </motion.div>
    </AppLayout>
  );
}
