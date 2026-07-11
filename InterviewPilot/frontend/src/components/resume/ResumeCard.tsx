"use client";

import {
  FileText,
  Download,
  RefreshCw,
  Trash2,
} from "lucide-react";

import Button from "../auth/Button";

interface ResumeCardProps {
  filename: string;
  size: number;
  onDownload: () => void;
  onReplace: () => void;
  onDelete: () => void;
}

export default function ResumeCard({
  filename,
  size,
  onDownload,
  onReplace,
  onDelete,
}: ResumeCardProps) {
  return (
    <div className="rounded-2xl border border-gray-800 bg-gray-900 p-8 shadow-lg">

      <div className="flex items-center gap-4">

        <div className="rounded-xl bg-blue-500/10 p-4">
          <FileText
            size={34}
            className="text-blue-400"
          />
        </div>

        <div>
          <h2 className="text-xl font-semibold text-white">
            {filename}
          </h2>

          <p className="text-sm text-gray-400">
            {(size / 1024).toFixed(2)} KB
          </p>
        </div>

      </div>

      <div className="my-8 h-px bg-gray-800" />

      <div className="space-y-3">

        <Button
          text="Download Resume"
          icon={<Download size={18} />}
          onClick={onDownload}
        />

        <Button
          text="Replace Resume"
          icon={<RefreshCw size={18} />}
          onClick={onReplace}
        />

        <Button
          text="Delete Resume"
          icon={<Trash2 size={18} />}
          className="bg-red-600 hover:bg-red-700"
          onClick={onDelete}
        />

      </div>

    </div>
  );
}