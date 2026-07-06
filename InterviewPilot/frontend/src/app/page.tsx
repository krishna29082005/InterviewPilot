"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [backendStatus, setBackendStatus] = useState("Checking...");

  useEffect(() => {
    async function checkBackend() {
        try {
            const response = await fetch("http://127.0.0.1:8000/health");

            const data = await response.json();

            setBackendStatus(data.status);
        } catch (error) {
            setBackendStatus("Offline");
        }
    }

    checkBackend();
}, []);

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-white">
          InterviewPilot 🚀
        </h1>

        <p className="mt-6 text-xl text-slate-400">
          Your AI Interview Coach
        </p>
        <p className="mt-4 text-lg text-green-400">
          Backend Status: {backendStatus}
        </p>
      </div>
    </main>
  );
}