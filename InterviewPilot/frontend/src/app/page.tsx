import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-white">
          InterviewPilot 🚀
        </h1>

        <p className="mt-6 text-xl text-slate-400">
          Your AI Interview Coach
        </p>
      </div>
    </main>
  );
}