import { Link, useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, Download, TrendingUp, AlertTriangle, BookOpen, Route } from 'lucide-react';
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
import { generateMockFeedback } from '../../utils';
import { Avatar, Badge, Button, LoadingState, Progress, Timeline } from '../../components/ui';
import { COLORS } from '../../constants/designTokens';

function CurriculumHeatmap({ heatmap }: { heatmap: { day: number; status: string }[] }) {
  return (
    <div className="grid grid-cols-[repeat(31,minmax(0,1fr))] gap-1">
      {heatmap.map((cell) => (
        <div
          key={cell.day}
          title={`Day ${cell.day}: ${cell.status}`}
          className={`aspect-square rounded-[2px] ${
            cell.status === 'passed'
              ? 'bg-signal'
              : cell.status === 'struggled'
                ? 'bg-warning'
                : cell.status === 'skipped'
                  ? 'bg-error'
                  : 'bg-surface'
          }`}
        />
      ))}
    </div>
  );
}

export function FeedbackPage() {
  const { candidateId } = useParams<{ candidateId: string }>();
  const navigate = useNavigate();
  const { getById, loading } = useCandidates();
  const candidate = candidateId ? getById(candidateId) : undefined;

  const report = useMemo(
    () => (candidate ? generateMockFeedback(candidate) : null),
    [candidate]
  );

  useEffect(() => {
    if (!loading && candidateId && !candidate) {
      navigate('/candidates', { replace: true });
    }
  }, [loading, candidateId, candidate, navigate]);

  if (loading || !candidate || !report) {
    return (
      <AppLayout>
        <LoadingState message="Finalizing assessment report…" />
      </AppLayout>
    );
  }

  const { member } = candidate;
  const radarData = report.skills.map((s) => ({ subject: s.skill, score: s.score }));

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
              {report.overallScore}
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
                {report.weaknesses.map((w) => (
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
              {report.improvementPath.map((step, i) => (
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
              items={report.timeline.map((e, i) => ({
                id: e.id,
                label: e.label,
                detail: e.detail,
                time: e.time,
                status: i === report.timeline.length - 1 ? 'active' : 'completed',
              }))}
            />
          </div>
        </div>
        
        {/* Heatmap Footer */}
        <div className="rounded-3xl bg-surface/30 p-10 text-center">
          <h2 className="mb-8 text-sm font-medium tracking-widest uppercase text-text-secondary">
            Curriculum Footprint
          </h2>
          <div className="mx-auto max-w-xl">
             <CurriculumHeatmap heatmap={candidate.insights.heatmap} />
          </div>
        </div>
      </motion.div>
    </AppLayout>
  );
}
