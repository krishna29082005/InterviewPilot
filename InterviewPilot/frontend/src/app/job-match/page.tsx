"use client";

import { useEffect, useMemo, useState, type ReactNode } from "react";
import { useRouter } from "next/navigation";
import { Sparkles, BriefcaseBusiness, BadgeCheck, TriangleAlert } from "lucide-react";

import DashboardLayout from "@/components/dashboard/DashboardLayout";
import DashboardCard from "@/components/dashboard/DashboardCard";
import { useAuth } from "@/context/AuthContext";
import { analyzeJobMatch, type JobMatchAnalysis } from "@/lib/api";

function SectionCard({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <section className="rounded-2xl border border-gray-800 bg-gray-900 p-6 shadow-lg">
      <h3 className="text-lg font-semibold text-white">{title}</h3>
      <div className="mt-4">{children}</div>
    </section>
  );
}

function ChipList({
  items,
  emptyText,
  tone = "blue",
}: {
  items: string[];
  emptyText: string;
  tone?: "blue" | "green" | "amber" | "red";
}) {
  const toneClasses = {
    blue: "border-blue-500/20 bg-blue-500/10 text-blue-200",
    green: "border-emerald-500/20 bg-emerald-500/10 text-emerald-200",
    amber: "border-amber-500/20 bg-amber-500/10 text-amber-200",
    red: "border-red-500/20 bg-red-500/10 text-red-200",
  }[tone];

  if (!items.length) {
    return <p className="text-sm text-gray-500">{emptyText}</p>;
  }

  return (
    <div className="flex flex-wrap gap-2">
      {items.map((item) => (
        <span
          key={item}
          className={`rounded-full border px-3 py-1 text-sm ${toneClasses}`}
        >
          {item}
        </span>
      ))}
    </div>
  );
}

function BulletList({
  items,
  emptyText,
}: {
  items: string[];
  emptyText: string;
}) {
  if (!items.length) {
    return <p className="text-sm text-gray-500">{emptyText}</p>;
  }

  return (
    <ul className="space-y-2 text-sm leading-7 text-gray-300">
      {items.map((item) => (
        <li
          key={item}
          className="flex gap-3 rounded-xl border border-gray-800 bg-gray-950/50 p-3"
        >
          <span className="mt-2 h-2 w-2 shrink-0 rounded-full bg-blue-400" />
          <span className="break-words">{item}</span>
        </li>
      ))}
    </ul>
  );
}

export default function JobMatchPage() {
  const router = useRouter();
  const { token, isAuthenticated, isLoading } = useAuth();

  const [jobDescription, setJobDescription] = useState("");
  const [analysis, setAnalysis] = useState<JobMatchAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace("/login");
    }
  }, [isLoading, isAuthenticated, router]);

  const scoreLabel = useMemo(() => {
    if (!analysis) return "--";
    return `${analysis.match_score}%`;
  }, [analysis]);

  async function handleAnalyze() {
    if (!jobDescription.trim()) {
      setError("Please paste a job description first.");
      return;
    }

    if (!token) {
      setError("You must be logged in to analyze a match.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await analyzeJobMatch(jobDescription.trim(), token);
      setAnalysis(result);
    } catch (err) {
      setAnalysis(null);
      setError(err instanceof Error ? err.message : "Unable to analyze this job match.");
    } finally {
      setLoading(false);
    }
  }

  if (isLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-gray-950 text-white">
        Loading...
      </main>
    );
  }

  if (!isAuthenticated) return null;

  return (
    <DashboardLayout>
      <div className="mb-10">
        <p className="text-sm uppercase tracking-widest text-blue-400">
          Job Match
        </p>
        <h1 className="mt-2 text-5xl font-bold text-white">
          Job Match Analyzer
        </h1>
        <p className="mt-3 max-w-3xl text-lg text-gray-400">
          Paste a job description and compare it against your saved resume analysis.
        </p>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <SectionCard title="Job Description">
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the full job description here..."
            className="min-h-[320px] w-full rounded-xl border border-gray-800 bg-gray-950/60 p-4 text-sm leading-7 text-white outline-none transition placeholder:text-gray-600 focus:border-blue-500/50"
          />

          {error ? (
            <div className="mt-4 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
              {error}
            </div>
          ) : null}

          <div className="mt-4 flex flex-wrap gap-3">
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="inline-flex items-center gap-2 rounded-xl bg-blue-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-blue-400 disabled:cursor-not-allowed disabled:opacity-60"
            >
              <Sparkles size={18} />
              {loading ? "Analyzing..." : "Analyze Match"}
            </button>
            <button
              onClick={() => {
                setJobDescription("");
                setAnalysis(null);
                setError(null);
              }}
              className="rounded-xl border border-gray-700 px-4 py-3 text-sm font-semibold text-gray-200 transition hover:border-gray-500 hover:bg-gray-800"
            >
              Clear
            </button>
          </div>
        </SectionCard>

        <div className="space-y-6">
          <DashboardCard
            icon={<BriefcaseBusiness size={28} />}
            title="Match Score"
            value={scoreLabel}
            description="How closely the job aligns with your resume."
          />

          <DashboardCard
            icon={<BadgeCheck size={28} />}
            title="Strengths"
            value={analysis?.strengths?.length?.toString() ?? "0"}
            description="Areas where your profile already fits well."
          />

          <DashboardCard
            icon={<TriangleAlert size={28} />}
            title="Gaps"
            value={analysis?.gaps?.length?.toString() ?? "0"}
            description="Missing skills or requirements to close."
          />
        </div>
      </div>

      {analysis ? (
        <div className="mt-10 grid gap-6 xl:grid-cols-2">
          <SectionCard title="Summary">
            <p className="text-sm leading-7 text-gray-300">{analysis.summary}</p>
          </SectionCard>

          <SectionCard title="Matching Skills">
            <ChipList
              items={analysis.matching_skills || []}
              emptyText="No matching skills detected."
              tone="green"
            />
          </SectionCard>

          <SectionCard title="Missing Skills">
            <ChipList
              items={analysis.missing_skills || []}
              emptyText="No missing skills detected."
              tone="amber"
            />
          </SectionCard>

          <SectionCard title="Keywords">
            <div className="space-y-4">
              <div>
                <p className="text-xs uppercase tracking-[0.25em] text-gray-500">
                  Matching Keywords
                </p>
                <div className="mt-3">
                  <ChipList
                    items={analysis.matching_keywords || []}
                    emptyText="No matching keywords detected."
                    tone="green"
                  />
                </div>
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.25em] text-gray-500">
                  Missing Keywords
                </p>
                <div className="mt-3">
                  <ChipList
                    items={analysis.missing_keywords || []}
                    emptyText="No missing keywords detected."
                    tone="red"
                  />
                </div>
              </div>
            </div>
          </SectionCard>

          <SectionCard title="Strengths and Gaps">
            <div className="space-y-6">
              <div>
                <p className="text-xs uppercase tracking-[0.25em] text-gray-500">
                  Strengths
                </p>
                <div className="mt-3">
                  <BulletList
                    items={analysis.strengths || []}
                    emptyText="No strengths listed."
                  />
                </div>
              </div>

              <div>
                <p className="text-xs uppercase tracking-[0.25em] text-gray-500">
                  Gaps
                </p>
                <div className="mt-3">
                  <BulletList
                    items={analysis.gaps || []}
                    emptyText="No gaps listed."
                  />
                </div>
              </div>
            </div>
          </SectionCard>

          <SectionCard title="Recommendations">
            <BulletList
              items={analysis.recommendations || []}
              emptyText="No recommendations available."
            />
          </SectionCard>
        </div>
      ) : null}
    </DashboardLayout>
  );
}
