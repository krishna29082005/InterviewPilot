"use client";

import DashboardLayout from "@/components/dashboard/DashboardLayout";
import ResumeUpload from "@/components/resume/ResumeUpload";
import ResumeCard from "@/components/resume/ResumeCard";

export default function ResumePage() {
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

        <ResumeUpload />

        <ResumeCard
          filename="resume.pdf"
          size={245760}
          onDownload={() => {}}
          onReplace={() => {}}
          onDelete={() => {}}
        />

      </div>
    </DashboardLayout>
  );
}