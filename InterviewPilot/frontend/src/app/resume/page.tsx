"use client";

import { useEffect, useState } from "react";

import DashboardLayout from "@/components/dashboard/DashboardLayout";
import ResumeUpload from "@/components/resume/ResumeUpload";
import ResumeCard from "@/components/resume/ResumeCard";

import {
  getResumeInfo,
  deleteResume,
  downloadResume,
  ResumeInfo,
} from "@/lib/api";

import { useAuth } from "@/context/AuthContext";

export default function ResumePage() {
  const { token } = useAuth();

  const [resume, setResume] = useState<ResumeInfo | null>(null);
  const [loading, setLoading] = useState(true);

  async function fetchResume() {
  console.log("🔥 fetchResume called");
  console.log("Token:", token);

  if (!token) {
    console.log("❌ No token");
    return;
  }

  try {
    const data = await getResumeInfo(token);

    console.log("✅ Resume Data:", data);

    setResume(data);
  } catch (err) {
    console.error("❌ Error:", err);
    setResume(null);
  } finally {
    setLoading(false);
  }
}

  useEffect(() => {
    fetchResume();
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
          onUploadSuccess={fetchResume}
        />

        {loading ? null : resume ? (
          <ResumeCard
            filename={resume.filename}
            size={resume.size}
            uploadedAt={resume.uploaded_at}
            onDownload={handleDownload}
            onReplace={() => {}}
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

      {/* ================= AI Resume Analysis ================= */}

      {resume?.analysis && (
        <div className="mt-10 space-y-8">

          {/* Header */}

          <div className="rounded-2xl bg-gray-900 border border-gray-800 p-8">
            <h2 className="text-3xl font-bold text-white">
              {resume.analysis.personal_info.full_name}
            </h2>

            <p className="mt-2 text-gray-400">
              {resume.analysis.personal_info.email}
            </p>

            <p className="mt-4 text-lg text-gray-300">
              {resume.analysis.summary}
            </p>
          </div>

          {/* Skills */}

          <div className="rounded-2xl bg-gray-900 border border-gray-800 p-8">
            <h3 className="text-2xl font-semibold text-white">
              Programming Languages
            </h3>

            <div className="mt-5 flex flex-wrap gap-3">
              {resume.analysis.technical_skills.programming_languages.map(
                (skill: string) => (
                  <span
                    key={skill}
                    className="rounded-full bg-blue-600 px-4 py-2 text-sm font-medium text-white"
                  >
                    {skill}
                  </span>
                )
              )}
            </div>
          </div>

          {/* Education */}

          <div className="rounded-2xl bg-gray-900 border border-gray-800 p-8">
            <h3 className="text-2xl font-semibold text-white">
              Education
            </h3>

            <div className="mt-6 space-y-5">
              {resume.analysis.education.map((edu: any) => (
                <div
                  key={edu.institution}
                  className="rounded-xl bg-gray-800 p-5"
                >
                  <h4 className="text-xl font-bold text-white">
                    {edu.institution}
                  </h4>

                  <p className="text-gray-300">
                    {edu.degree}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Experience */}

          <div className="rounded-2xl bg-gray-900 border border-gray-800 p-8">
            <h3 className="text-2xl font-semibold text-white">
              Experience
            </h3>

            <div className="mt-6 space-y-5">
              {resume.analysis.experience.map((exp: any) => (
                <div
                  key={`${exp.company}-${exp.title}`}
                  className="rounded-xl bg-gray-800 p-5"
                >
                  <h4 className="text-xl font-bold text-white">
                    {exp.title}
                  </h4>

                  <p className="text-blue-400">
                    {exp.company}
                  </p>

                  <p className="mt-1 text-sm text-gray-400">
                    {exp.start_date} - {exp.end_date}
                  </p>

                  <ul className="mt-4 list-disc pl-5 text-gray-300 space-y-2">
                    {exp.description.map((point: string) => (
                      <li key={point}>{point}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          {/* Projects */}

          <div className="rounded-2xl bg-gray-900 border border-gray-800 p-8">
            <h3 className="text-2xl font-semibold text-white">
              Projects
            </h3>

            <div className="mt-6 space-y-5">
              {resume.analysis.projects.map((project: any) => (
                <div
                  key={project.title}
                  className="rounded-xl bg-gray-800 p-5"
                >
                  <h4 className="text-xl font-bold text-white">
                    {project.title}
                  </h4>

                  <p className="mt-2 text-gray-300">
                    {project.description}
                  </p>

                  <div className="mt-4 flex flex-wrap gap-2">
                    {project.technologies.map((tech: string) => (
                      <span
                        key={tech}
                        className="rounded-full bg-gray-700 px-3 py-1 text-sm text-white"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}
    </DashboardLayout>
  );
}