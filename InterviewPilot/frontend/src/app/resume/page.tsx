"use client";

import { useEffect, useState } from "react";

import DashboardLayout from "@/components/dashboard/DashboardLayout";
import ResumeUpload from "@/components/resume/ResumeUpload";
import ResumeCard from "@/components/resume/ResumeCard";
import ATSAnalysisCard from "@/components/ats/ATSAnalysis";
import {
  getResumeInfo,
  deleteResume,
  downloadResume,
  getATSAnalysis,
  type ATSAnalysis as ATSAnalysisType,
  type ResumeInfo,
} from "@/lib/api";

import { useAuth } from "@/context/AuthContext";

function DetailCard({
  title,
  children,
  className = "",
}: {
  title: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <section
      className={`rounded-2xl border border-gray-800 bg-gray-900 p-6 shadow-lg ${className}`}
    >
      <h3 className="text-lg font-semibold text-white">{title}</h3>
      <div className="mt-4">{children}</div>
    </section>
  );
}

function ChipList({
  items,
  emptyText = "No items available.",
}: {
  items: string[];
  emptyText?: string;
}) {
  if (!items.length) {
    return (
      <p className="text-sm text-gray-500">
        {emptyText}
      </p>
    );
  }

  return (
    <div className="flex flex-wrap gap-2">
      {items.map((item) => (
        <span
          key={item}
          className="rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-1 text-sm text-blue-200"
        >
          {item}
        </span>
      ))}
    </div>
  );
}

function BulletList({
  items,
  emptyText = "No details available.",
}: {
  items: string[];
  emptyText?: string;
}) {
  if (!items.length) {
    return (
      <p className="text-sm text-gray-500">
        {emptyText}
      </p>
    );
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

function LinkItem({
  label,
  value,
  fallbackLabel,
}: {
  label: string;
  value?: string | null;
  fallbackLabel: string;
}) {
  const displayValue = value?.trim();

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-950/50 p-4">
      <p className="text-[11px] uppercase tracking-[0.3em] text-gray-500">
        {label}
      </p>

      {displayValue ? (
        <>
          <p className="mt-2 break-words text-sm font-semibold text-white">
            {fallbackLabel}
          </p>
          <a
            href={displayValue}
            target="_blank"
            rel="noreferrer"
            className="mt-1 block break-words text-sm text-blue-400 underline decoration-blue-400/40 underline-offset-4 transition hover:text-blue-300"
          >
            {displayValue}
          </a>
        </>
      ) : (
        <p className="mt-2 text-sm font-semibold text-gray-400">
          {fallbackLabel}
        </p>
      )}
    </div>
  );
}

export default function ResumePage() {
  const { token } = useAuth();

  const [resume, setResume] = useState<ResumeInfo | null>(null);
  const [ats, setATS] = useState<ATSAnalysisType | null>(null);
  const [atsError, setATSError] = useState<string | null>(null);
  const [atsLoading, setATSLoading] = useState(false);
  const [loading, setLoading] = useState(true);

  async function fetchResume() {
  if (!token) {
    return;
  }

  try {
    const data = await getResumeInfo(token);

    setResume(data);
  } catch {
    setResume(null);
  } finally {
    setLoading(false);
  }
}

  async function fetchATS() {
    if (!token) return;

    try {
        setATSLoading(true);
        setATSError(null);

        const data = await getATSAnalysis(token);

        setATS(data);
    } catch (err) {
        setATS(null);
        setATSError(
          err instanceof Error
            ? err.message
            : "Unable to load ATS analysis. Please try again."
        );
    } finally {
        setATSLoading(false);
    }
}

  useEffect(() => {
  if (!token) return;

  fetchResume();
  fetchATS();
}, [token]);

  async function handleDelete() {
    if (!token || !resume) return;

    const confirmed = window.confirm(
      "Are you sure you want to delete your resume?"
    );

    if (!confirmed) return;

    try {
      await deleteResume(token);

      setResume(null);
      setATS(null);
    } catch (err) {
      if (err instanceof Error) {
        alert(err.message);
      }
    }
  }

  async function handleDownload() {
    if (!token) return;

    try {
      await downloadResume(token);
    } catch (err) {
      if (err instanceof Error) {
        alert(err.message);
      }
    }
  }

  const resumeSummary =
    resume?.analysis?.summary ||
    [
      resume?.analysis?.personal_info?.full_name
        ? `${resume.analysis.personal_info.full_name}'s resume has been parsed successfully.`
        : "Your resume has been parsed successfully.",
      resume?.analysis?.technical_skills?.programming_languages?.length
        ? `Key programming languages include ${resume.analysis.technical_skills.programming_languages.join(", ")}.`
        : "Technical skills are available in the parsed analysis.",
      resume?.analysis?.projects?.length
        ? `The resume includes ${resume.analysis.projects.length} project${resume.analysis.projects.length > 1 ? "s" : ""}, which helps ATS scoring and screening.`
        : "Add more project detail to strengthen ATS matching.",
    ]
      .filter(Boolean)
      .join(" ");

  const resumeSummaryLines =
    resumeSummary
      .split(/(?<=[.!?])\s+/)
      .map((line: string) => line.trim())
      .filter((line: string) => Boolean(line));

  const analysis = resume?.analysis;

  return (
    <DashboardLayout>
      <div className="mb-10">
        <p className="text-sm uppercase tracking-widest text-blue-400">
          Resume
        </p>

        <h1 className="mt-2 text-5xl font-bold text-white">
          Resume Management
        </h1>

        <p className="mt-3 text-lg text-gray-400">
          Upload your latest resume for AI analysis.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <ResumeUpload
         hasResume={!!resume}
         onUploadSuccess={async () => {
         await fetchResume();
         await fetchATS();
        }}
/>

        {loading ? null : resume ? (
          <ResumeCard
            filename={resume.filename}
            size={resume.size}
            uploadedAt={resume.uploaded_at}
            onDownload={handleDownload}
            onDelete={handleDelete}
          />
        ) : (
          <div className="rounded-2xl border border-dashed border-gray-700 bg-gray-900 p-10 text-center">
            <h2 className="text-2xl font-semibold text-white">
              No Resume Uploaded
            </h2>

            <p className="mt-3 text-gray-400">
              Upload your first resume to begin AI analysis.
            </p>
          </div>
        )}
      </div>

      {/* ================= ATS Analysis ================= */}

      {atsLoading ? (
        <div className="mt-10 rounded-2xl border border-gray-800 bg-gray-900 p-8 text-center text-gray-400">
          Generating ATS Analysis...
        </div>
      ) : atsError ? (
        <div className="mt-10 rounded-2xl border border-red-500/30 bg-red-500/10 p-8 text-center">
          <h2 className="text-xl font-semibold text-red-400">
            ATS analysis could not be loaded
          </h2>

          <p className="mt-2 text-sm text-red-200">
            {atsError}
          </p>
        </div>
      ) : (
        ats && (
          <div className="mt-10">
            <ATSAnalysisCard analysis={ats} />
          </div>
        )
      )}


      {/* ================= AI Resume Analysis ================= */}

      {resume && (
        <div className="mt-10 space-y-8">
          <section className="rounded-2xl border border-gray-800 bg-gray-900 p-8 shadow-lg">
            <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
              <div className="max-w-3xl">
                <p className="text-sm uppercase tracking-widest text-blue-400">
                  Resume Summary
                </p>

                <h2 className="mt-2 text-3xl font-bold text-white break-words">
                  {analysis?.personal_info?.full_name || resume.filename.replace(/\.pdf$/i, "")}
                </h2>

                <p className="mt-2 text-gray-400 break-words">
                  {analysis?.personal_info?.email ||
                    "Analysis details will appear after parsing completes."}
                </p>

                <div className="mt-5 space-y-3 text-base leading-7 text-gray-200">
                  {resumeSummaryLines.map((line: string, index: number) => (
                    <p
                      key={`${index}-${line}`}
                      className="rounded-xl border border-gray-800 bg-gray-950/50 px-4 py-3 break-words whitespace-pre-wrap"
                    >
                      {line}
                    </p>
                  ))}
                </div>
              </div>

              <div className="grid min-w-[220px] gap-3 sm:grid-cols-2 lg:grid-cols-1">
                <div className="rounded-xl border border-gray-800 bg-gray-950/50 p-4">
                  <p className="text-xs uppercase tracking-[0.3em] text-gray-500">
                    File
                  </p>
                  <p className="mt-2 break-words text-sm font-medium text-white">
                    {resume.filename}
                  </p>
                </div>

                <div className="rounded-xl border border-gray-800 bg-gray-950/50 p-4">
                  <p className="text-xs uppercase tracking-[0.3em] text-gray-500">
                    Status
                  </p>
                  <p className="mt-2 text-sm font-medium text-green-400">
                    Parsed successfully
                  </p>
                </div>
              </div>
            </div>
          </section>

          {analysis ? (
            <div className="grid gap-6 xl:grid-cols-2">
              <DetailCard title="Personal Information">
                <dl className="grid gap-4 sm:grid-cols-2">
                  <div>
                    <dt className="text-xs uppercase tracking-[0.25em] text-gray-500">Name</dt>
                    <dd className="mt-1 break-words text-sm text-white">
                      {analysis.personal_info.full_name || "Not available"}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-xs uppercase tracking-[0.25em] text-gray-500">Email</dt>
                    <dd className="mt-1 break-words text-sm text-white">
                      {analysis.personal_info.email || "Not available"}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-xs uppercase tracking-[0.25em] text-gray-500">Phone</dt>
                    <dd className="mt-1 break-words text-sm text-white">
                      {analysis.personal_info.phone || "Not available"}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-xs uppercase tracking-[0.25em] text-gray-500">Location</dt>
                    <dd className="mt-1 break-words text-sm text-white">
                      {analysis.personal_info.location || "Not available"}
                    </dd>
                  </div>
                </dl>
              </DetailCard>

              <DetailCard title="Links">
                <div className="space-y-3 text-sm">
                  <LinkItem
                    label="LinkedIn"
                    value={analysis.personal_info.linkedin}
                    fallbackLabel="LinkedIn"
                  />
                  <LinkItem
                    label="GitHub"
                    value={analysis.personal_info.github}
                    fallbackLabel="GitHub"
                  />
                  <LinkItem
                    label="LeetCode"
                    value={analysis.personal_info.leetcode}
                    fallbackLabel="LeetCode"
                  />
                  <LinkItem
                    label="Portfolio"
                    value={analysis.personal_info.portfolio}
                    fallbackLabel="Live Demo"
                  />
                </div>
              </DetailCard>

              <DetailCard title="Technical Skills">
                <div className="space-y-4">
                  <ChipList items={analysis.technical_skills.programming_languages} emptyText="No programming languages detected." />
                  <ChipList items={analysis.technical_skills.frameworks} emptyText="No frameworks detected." />
                  <ChipList items={analysis.technical_skills.libraries} emptyText="No libraries detected." />
                  <ChipList items={analysis.technical_skills.databases} emptyText="No databases detected." />
                  <ChipList items={analysis.technical_skills.tools} emptyText="No tools detected." />
                </div>
              </DetailCard>

              <DetailCard title="Projects" className="xl:col-span-2">
                <div className="grid gap-4 lg:grid-cols-2">
                  {analysis.projects.length > 0 ? (
                    analysis.projects.map((project: any) => (
                      <article
                        key={project.title}
                        className="rounded-xl border border-gray-800 bg-gray-950/50 p-5"
                      >
                        <h4 className="text-lg font-semibold text-white">
                          {project.title}
                        </h4>
                        {project.description ? (
                          <p className="mt-2 text-sm leading-7 text-gray-300">
                            {project.description}
                          </p>
                        ) : null}
                        <div className="mt-4">
                          <ChipList
                            items={project.technologies || []}
                            emptyText="No technologies listed."
                          />
                        </div>
                        <div className="mt-4">
                          <BulletList
                            items={project.bullet_points || []}
                            emptyText="No bullet points extracted."
                          />
                        </div>
                      </article>
                    ))
                  ) : (
                    <p className="text-sm text-gray-500">
                      No projects detected.
                    </p>
                  )}
                </div>
              </DetailCard>

              <DetailCard title="Education" className="xl:col-span-2">
                <div className="grid gap-4 md:grid-cols-2">
                  {analysis.education.length > 0 ? (
                    analysis.education.map((edu: any) => (
                      <article
                        key={`${edu.institution}-${edu.degree}`}
                        className="rounded-xl border border-gray-800 bg-gray-950/50 p-5"
                      >
                        <h4 className="text-lg font-semibold text-white">
                          {edu.institution || "Institution not available"}
                        </h4>
                        <p className="mt-1 text-sm text-blue-400">
                          {edu.degree || "Degree not available"}
                        </p>
                        <dl className="mt-4 grid gap-3 text-sm text-gray-300 sm:grid-cols-2">
                          <div>
                            <dt className="text-xs uppercase tracking-[0.2em] text-gray-500">Field</dt>
                            <dd className="mt-1">{edu.field_of_study || "N/A"}</dd>
                          </div>
                          <div>
                            <dt className="text-xs uppercase tracking-[0.2em] text-gray-500">CGPA</dt>
                            <dd className="mt-1">{edu.cgpa || "N/A"}</dd>
                          </div>
                          <div>
                            <dt className="text-xs uppercase tracking-[0.2em] text-gray-500">Start</dt>
                            <dd className="mt-1">{edu.start_date || "N/A"}</dd>
                          </div>
                          <div>
                            <dt className="text-xs uppercase tracking-[0.2em] text-gray-500">End</dt>
                            <dd className="mt-1">{edu.end_date || "N/A"}</dd>
                          </div>
                        </dl>
                      </article>
                    ))
                  ) : (
                    <p className="text-sm text-gray-500">
                      No education entries detected.
                    </p>
                  )}
                </div>
              </DetailCard>

              <DetailCard title="Experience" className="xl:col-span-2">
                <div className="space-y-4">
                  {analysis.experience.length > 0 ? (
                    analysis.experience.map((exp: any) => (
                      <article
                        key={`${exp.company}-${exp.title}`}
                        className="rounded-xl border border-gray-800 bg-gray-950/50 p-5"
                      >
                        <div className="flex flex-col gap-1 sm:flex-row sm:items-start sm:justify-between">
                          <div>
                            <h4 className="text-lg font-semibold text-white">
                              {exp.title || "Title not available"}
                            </h4>
                            <p className="mt-1 text-sm text-blue-400">
                              {exp.company || "Company not available"}
                            </p>
                          </div>
                          <p className="text-sm text-gray-400">
                            {(exp.start_date || "N/A")} - {(exp.end_date || "N/A")}
                          </p>
                        </div>
                        <div className="mt-4">
                          <BulletList
                            items={exp.description || []}
                            emptyText="No bullet points extracted."
                          />
                        </div>
                      </article>
                    ))
                  ) : (
                    <p className="text-sm text-gray-500">
                      No experience entries detected.
                    </p>
                  )}
                </div>
              </DetailCard>

              <DetailCard title="Additional Information">
                <div className="space-y-6">
                  <div>
                    <p className="text-xs uppercase tracking-[0.25em] text-gray-500">
                      Certifications
                    </p>
                    <div className="mt-3">
                      <ChipList items={analysis.certifications || []} emptyText="No certifications detected." />
                    </div>
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-[0.25em] text-gray-500">
                      Achievements
                    </p>
                    <div className="mt-3">
                      <BulletList items={analysis.achievements || []} emptyText="No achievements detected." />
                    </div>
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-[0.25em] text-gray-500">
                      Languages
                    </p>
                    <div className="mt-3">
                      <ChipList items={analysis.languages || []} emptyText="No languages detected." />
                    </div>
                  </div>
                </div>
              </DetailCard>
            </div>
          ) : null}
        </div>
      )}
    </DashboardLayout>
  );
}
