"use client";

import type { ReactNode } from "react";
import type { ATSAnalysis as ATSAnalysisType } from "@/lib/api";

import {
  AlertTriangle,
  BadgeCheck,
  BarChart3,
  FileWarning,
  Lightbulb,
  Target,
} from "lucide-react";

type Tone = "gray" | "green" | "yellow" | "red" | "blue";

interface ATSAnalysisProps {
  analysis: ATSAnalysisType;
}

interface SectionCardProps {
  title: string;
  icon: ReactNode;
  items: string[];
  tone?: Tone;
  emptyText?: string;
}

function SectionCard({
  title,
  icon,
  items,
  tone = "gray",
  emptyText = "No items to show.",
}: SectionCardProps) {
  const toneClasses: Record<Tone, string> = {
    gray: "border-gray-800 bg-gray-900",
    green: "border-green-500/20 bg-green-500/5",
    yellow: "border-yellow-500/20 bg-yellow-500/5",
    red: "border-red-500/20 bg-red-500/5",
    blue: "border-blue-500/20 bg-blue-500/5",
  };

  const iconClasses: Record<Tone, string> = {
    gray: "bg-blue-500/10 text-blue-400",
    green: "bg-green-500/10 text-green-400",
    yellow: "bg-yellow-500/10 text-yellow-400",
    red: "bg-red-500/10 text-red-400",
    blue: "bg-blue-500/10 text-blue-400",
  };

  return (
    <div className={`rounded-2xl border p-6 ${toneClasses[tone]}`}>
      <div className="flex items-center gap-3">
        <div className={`rounded-xl p-3 ${iconClasses[tone]}`}>
          {icon}
        </div>

        <h3 className="text-xl font-semibold text-white">
          {title}
        </h3>
      </div>

      <div className="mt-5 space-y-3">
        {items.length > 0 ? (
          items.map((item) => (
            <div
              key={item}
              className="rounded-xl border border-gray-800 bg-gray-950/60 p-4 text-sm text-gray-300"
            >
              {item}
            </div>
          ))
        ) : (
          <div className="rounded-xl border border-dashed border-gray-700 bg-gray-950/40 p-4 text-sm text-gray-500">
            {emptyText}
          </div>
        )}
      </div>
    </div>
  );
}

export default function ATSAnalysis({
  analysis,
}: ATSAnalysisProps) {
  const score = Math.max(
    0,
    Math.min(100, analysis.ats_score)
  );

  const scoreColor =
    score >= 80
      ? "text-green-400"
      : score >= 60
      ? "text-yellow-400"
      : "text-red-400";

  const scoreRing =
    score >= 80
      ? "from-green-500 to-emerald-400"
      : score >= 60
      ? "from-yellow-500 to-amber-400"
      : "from-red-500 to-rose-400";

  return (
    <div className="mt-10 space-y-8">
      <div className="rounded-3xl border border-gray-800 bg-gray-900 p-8">
        <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-widest text-blue-400">
              ATS Analysis
            </p>

            <h2 className="mt-2 text-3xl font-bold text-white">
              Resume Readiness Snapshot
            </h2>

            <p className="mt-4 text-lg leading-8 text-gray-300">
              {analysis.summary}
            </p>
          </div>

          <div className="flex items-center gap-5 rounded-3xl border border-gray-800 bg-gray-950/70 p-5">
            <div
              className={`flex h-28 w-28 items-center justify-center rounded-full bg-gradient-to-br ${scoreRing} p-1`}
            >
              <div className="flex h-full w-full items-center justify-center rounded-full bg-gray-950">
                <div className="text-center">
                  <div className={`text-3xl font-bold ${scoreColor}`}>
                    {score}
                  </div>

                  <div className="text-xs uppercase tracking-[0.3em] text-gray-500">
                    Score
                  </div>
                </div>
              </div>
            </div>

            <div>
              <div className="flex items-center gap-2 text-sm text-gray-400">
                <BarChart3
                  size={16}
                  className="text-blue-400"
                />

                ATS Compatibility
              </div>

              <p className="mt-2 max-w-xs text-sm leading-6 text-gray-300">
                Higher scores indicate that your resume is easier for Applicant
                Tracking Systems to parse and match against job descriptions.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <SectionCard
          title="Strengths"
          icon={<BadgeCheck size={20} />}
          items={analysis.strengths}
          tone="green"
          emptyText="No strengths were detected."
        />

        <SectionCard
          title="Weaknesses"
          icon={<AlertTriangle size={20} />}
          items={analysis.weaknesses}
          tone="red"
          emptyText="No weaknesses were detected."
        />

        <SectionCard
          title="Missing Keywords"
          icon={<Target size={20} />}
          items={analysis.missing_keywords}
          tone="yellow"
          emptyText="No missing keywords were detected."
        />

        <SectionCard
          title="Formatting Issues"
          icon={<FileWarning size={20} />}
          items={analysis.formatting_issues}
          tone="blue"
          emptyText="No formatting issues were detected."
        />
      </div>

      <div className="rounded-2xl border border-gray-800 bg-gray-900 p-8">
        <div className="flex items-center gap-3">
          <div className="rounded-xl bg-blue-500/10 p-3 text-blue-400">
            <Lightbulb size={20} />
          </div>

          <h3 className="text-2xl font-semibold text-white">
            Improvement Suggestions
          </h3>
        </div>

        <div className="mt-6 space-y-3">
          {(analysis.recommendations ?? analysis.improvement_suggestions ?? []).length > 0 ? (
            (analysis.recommendations ?? analysis.improvement_suggestions ?? []).map((suggestion) => (
              <div
                key={suggestion}
                className="rounded-xl border border-gray-800 bg-gray-950/60 p-4 text-sm leading-6 text-gray-300"
              >
                {suggestion}
              </div>
            ))
          ) : (
            <div className="rounded-xl border border-dashed border-gray-700 bg-gray-950/40 p-4 text-sm text-gray-500">
              No improvement suggestions available.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
