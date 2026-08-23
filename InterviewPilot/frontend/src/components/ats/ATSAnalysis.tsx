"use client";

import type { ReactNode } from "react";
import type {
  ATSAnalysis as ATSAnalysisType,
  RecommendedRole,
} from "@/lib/api";

import {
  AlertTriangle,
  ArrowUpRight,
  BadgeCheck,
  BarChart3,
  BriefcaseBusiness,
  Check,
  FileWarning,
  Lightbulb,
  Sparkles,
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
    <div
      className={`rounded-2xl border p-6 ${toneClasses[tone]}`}
    >
      <div className="flex items-center gap-3">
        <div
          className={`rounded-xl p-3 ${iconClasses[tone]}`}
        >
          {icon}
        </div>

        <h3 className="text-xl font-semibold text-white">
          {title}
        </h3>
      </div>

      <div className="mt-5 space-y-3">
        {items.length > 0 ? (
          items.map((item, index) => (
            <div
              key={`${item}-${index}`}
              className="rounded-xl border border-gray-800 bg-gray-950/60 p-4 text-sm leading-6 text-gray-300"
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

/* =========================================================
   Recommended Role Card
========================================================= */

function RecommendedRoleCard({
  recommendation,
}: {
  recommendation: RecommendedRole;
}) {
  const normalizedLevel =
    recommendation.match_level.toLowerCase();

  const isHigh = normalizedLevel === "high";
  const isMedium = normalizedLevel === "medium";

  const levelConfig = isHigh
    ? {
        label: "High Match",
        badge:
          "border-green-500/20 bg-green-500/10 text-green-400",
        icon: "text-green-400",
        bar: "bg-green-400",
        width: "w-full",
      }
    : isMedium
    ? {
        label: "Medium Match",
        badge:
          "border-yellow-500/20 bg-yellow-500/10 text-yellow-400",
        icon: "text-yellow-400",
        bar: "bg-yellow-400",
        width: "w-2/3",
      }
    : {
        label: `${recommendation.match_level || "Low"} Match`,
        badge:
          "border-gray-700 bg-gray-800/70 text-gray-400",
        icon: "text-gray-400",
        bar: "bg-gray-500",
        width: "w-1/3",
      };

  return (
    <div className="group relative overflow-hidden rounded-2xl border border-gray-800 bg-gray-950/70 p-6 transition-all duration-200 hover:border-gray-700 hover:bg-gray-950">
      {/* Subtle top accent */}
      <div
        className={`absolute inset-x-0 top-0 h-px ${levelConfig.bar} opacity-60`}
      />

      <div className="flex items-start justify-between gap-4">
        <div className="flex min-w-0 items-start gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl border border-gray-800 bg-gray-900 text-blue-400">
            <BriefcaseBusiness size={21} />
          </div>

          <div className="min-w-0">
            <h4 className="truncate text-lg font-semibold text-white">
              {recommendation.role}
            </h4>

            <div
              className={`mt-2 inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium ${levelConfig.badge}`}
            >
              <span
                className={`h-1.5 w-1.5 rounded-full ${levelConfig.bar}`}
              />

              {levelConfig.label}
            </div>
          </div>
        </div>

        <ArrowUpRight
          size={18}
          className="shrink-0 text-gray-600 transition-colors group-hover:text-gray-400"
        />
      </div>

      {/* Match indicator */}
      <div className="mt-6">
        <div className="flex items-center justify-between text-xs">
          <span className="text-gray-500">
            Resume alignment
          </span>

          <span className={`font-medium ${levelConfig.icon}`}>
            {recommendation.match_level}
          </span>
        </div>

        <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-gray-800">
          <div
            className={`h-full rounded-full ${levelConfig.bar} ${levelConfig.width} transition-all duration-500`}
          />
        </div>
      </div>

      {/* Evidence */}
      {recommendation.reasons.length > 0 && (
        <div className="mt-6">
          <p className="mb-3 text-xs font-medium uppercase tracking-wider text-gray-500">
            Why this role fits
          </p>

          <div className="space-y-2.5">
            {recommendation.reasons.map(
              (reason, index) => (
                <div
                  key={`${reason}-${index}`}
                  className="flex items-start gap-2.5 text-sm leading-5 text-gray-300"
                >
                  <div className="mt-0.5 flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-blue-500/10 text-blue-400">
                    <Check size={10} strokeWidth={3} />
                  </div>

                  <span>{reason}</span>
                </div>
              )
            )}
          </div>
        </div>
      )}
    </div>
  );
}

/* =========================================================
   Recommended Roles Section
========================================================= */

function RecommendedRoles({
  roles,
}: {
  roles: RecommendedRole[];
}) {
  return (
    <section className="overflow-hidden rounded-3xl border border-gray-800 bg-gray-900">
      <div className="border-b border-gray-800 px-6 py-7 sm:px-8">
        <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
          <div className="flex items-start gap-4">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400">
              <Sparkles size={22} />
            </div>

            <div>
              <p className="text-xs font-medium uppercase tracking-[0.2em] text-blue-400">
                Career Fit
              </p>

              <h3 className="mt-1 text-2xl font-bold text-white">
                Recommended Roles
              </h3>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-gray-400">
                Roles that align with the skills, projects, and
                experience found in your resume.
              </p>
            </div>
          </div>

          {roles.length > 0 && (
            <div className="flex shrink-0 items-center gap-2 rounded-full border border-gray-800 bg-gray-950/60 px-3 py-1.5 text-xs text-gray-400">
              <Target size={13} className="text-blue-400" />
              {roles.length}{" "}
              {roles.length === 1 ? "role" : "roles"} found
            </div>
          )}
        </div>
      </div>

      {roles.length > 0 ? (
        <div className="grid gap-4 p-6 sm:p-8 lg:grid-cols-2">
          {roles.map((role, index) => (
            <RecommendedRoleCard
              key={`${role.role}-${index}`}
              recommendation={role}
            />
          ))}
        </div>
      ) : (
        <div className="px-6 py-12 text-center sm:px-8">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-gray-800 text-gray-500">
            <BriefcaseBusiness size={20} />
          </div>

          <h4 className="mt-4 text-sm font-semibold text-white">
            No role recommendations available
          </h4>

          <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-gray-500">
            Add more technical skills, projects, or experience
            to help InterviewPilot identify suitable career paths.
          </p>
        </div>
      )}
    </section>
  );
}

/* =========================================================
   Main ATS Analysis
========================================================= */

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

  const suggestions =
    analysis.recommendations ??
    analysis.improvement_suggestions ??
    [];

  return (
    <div className="mt-10 space-y-8">
      {/* =====================================================
          Header / Score
      ===================================================== */}

      <div className="rounded-3xl border border-gray-800 bg-gray-900 p-8">
        <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
          <div className="max-w-3xl">
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

          <div className="flex shrink-0 items-center gap-5 rounded-3xl border border-gray-800 bg-gray-950/70 p-5">
            <div
              className={`flex h-28 w-28 items-center justify-center rounded-full bg-gradient-to-br ${scoreRing} p-1`}
            >
              <div className="flex h-full w-full items-center justify-center rounded-full bg-gray-950">
                <div className="text-center">
                  <div
                    className={`text-3xl font-bold ${scoreColor}`}
                  >
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
                Higher scores indicate that your resume is
                easier for Applicant Tracking Systems to parse
                and match against job descriptions.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* =====================================================
          Recommended Roles
      ===================================================== */}

      <RecommendedRoles
        roles={analysis.recommended_roles ?? []}
      />

      {/* =====================================================
          Strengths / Weaknesses / Keywords / Formatting
      ===================================================== */}

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

      {/* =====================================================
          Improvement Suggestions
      ===================================================== */}

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
          {suggestions.length > 0 ? (
            suggestions.map(
              (suggestion, index) => (
                <div
                  key={`${suggestion}-${index}`}
                  className="flex items-start gap-3 rounded-xl border border-gray-800 bg-gray-950/60 p-4 text-sm leading-6 text-gray-300"
                >
                  <Lightbulb
                    size={16}
                    className="mt-1 shrink-0 text-blue-400"
                  />

                  <span>{suggestion}</span>
                </div>
              )
            )
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