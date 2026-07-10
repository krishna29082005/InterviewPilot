import { ReactNode } from "react";

interface AuthCardProps {
  title: string;
  subtitle: string;
  footer: ReactNode;
  children: ReactNode;
}

export default function AuthCard({
  title,
  subtitle,
  footer,
  children,
}: AuthCardProps) {
  return (
    <main className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-950 via-gray-950 to-black px-6">

      <div className="w-full max-w-md rounded-3xl border border-gray-800 bg-gray-900/90 p-10 shadow-2xl backdrop-blur">

        <div className="mb-10 text-center">

          <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-600 text-3xl shadow-lg">
            🚀
          </div>

          <h1 className="text-4xl font-bold tracking-tight text-white">
            InterviewPilot
          </h1>

          <p className="mt-3 text-gray-400">
            AI-powered interview preparation
          </p>

        </div>

        <h2 className="mb-2 text-2xl font-semibold text-white">
          {title}
        </h2>

        <p className="mb-8 text-gray-400">
          {subtitle}
        </p>

        {children}

       <div className="mt-8 border-t border-gray-800 pt-6 text-center text-sm text-gray-400">
        {footer}
      </div>

      </div>
    </main>
  );
}