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
    if (!token) return;

    try {
      const data = await getResumeInfo(token);

      setResume(data);
    } catch {
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
    </DashboardLayout>
  );
}