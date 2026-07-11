"use client";

import { useRef, useState } from "react";

import { uploadResume } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import Button from "../auth/Button";

export default function ResumeUpload() {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");

  const { token } = useAuth();

  function handleChooseFile() {
    fileInputRef.current?.click();
  }

  function handleFileChange(
    e: React.ChangeEvent<HTMLInputElement>
  ) {
    setError("");

    const file = e.target.files?.[0];

    if (!file) return;

    if (file.type !== "application/pdf") {
      setError("Please select a PDF file.");

      setTimeout(() => {
        setError("");
      }, 3000);

      return;
    }

    setSelectedFile(file);
  }

  async function handleUpload() {
    setError("");
    setSuccess("");

    if (!selectedFile) {
      setError("Please choose a PDF first.");

      setTimeout(() => {
        setError("");
      }, 3000);

      return;
    }

    if (!token) {
      setError("Authentication failed. Please login again.");

      setTimeout(() => {
        setError("");
      }, 3000);

      return;
    }

    try {
      const result = await uploadResume(
        selectedFile,
        token
      );

      setSuccess(result.message);

      setTimeout(() => {
        setSuccess("");
      }, 3000);

      setSelectedFile(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Upload failed.");
      }

      setTimeout(() => {
        setError("");
      }, 3000);
    }
  }

  return (
    <div className="rounded-2xl border border-gray-800 bg-gray-900 p-8">
      <h2 className="text-2xl font-semibold text-white">
        Upload Resume
      </h2>

      <p className="mt-2 text-gray-400">
        Supported format: PDF
      </p>

      {success && (
        <div className="mt-6 rounded-xl border border-green-500/30 bg-green-500/10 p-4">
          <h3 className="font-semibold text-green-400">
            ✅ Resume uploaded successfully!
          </h3>

          <p className="mt-1 text-sm text-green-300">
            Your resume is ready for AI analysis.
          </p>
        </div>
      )}

      {error && (
        <div className="mt-6 rounded-xl border border-red-500/30 bg-red-500/10 p-4">
          <h3 className="font-semibold text-red-400">
            ❌ Upload Failed
          </h3>

          <p className="mt-1 text-sm text-red-300">
            {error}
          </p>
        </div>
      )}

      <div className="mt-8 flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-700 p-16">
        <p className="text-gray-400">
          Drag & Drop your resume here
        </p>

        <p className="my-5 text-gray-500">
          or
        </p>

        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="hidden"
        />

        <Button
          text="Choose File"
          type="button"
          onClick={handleChooseFile}
        />

        {selectedFile && (
          <>
            <div className="mt-6 w-full rounded-xl border border-blue-500/30 bg-blue-500/10 p-4">
              <p className="text-sm text-blue-300">
                📄 Selected File
              </p>

              <p className="mt-1 font-medium text-white">
                {selectedFile.name}
              </p>

              <p className="mt-1 text-sm text-gray-400">
                {(selectedFile.size / 1024).toFixed(2)} KB
              </p>
            </div>

            <div className="mt-6">
              <Button
                text="Upload Resume"
                type="button"
                onClick={handleUpload}
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
}