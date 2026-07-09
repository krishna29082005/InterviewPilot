"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import Button from "@/components/auth/Button";
import { useAuth } from "@/context/AuthContext";

export default function Dashboard() {
  const router = useRouter();

  const {
    isAuthenticated,
    isLoading,
    logout,
  } = useAuth();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isLoading, isAuthenticated, router]);

  function handleLogout() {
    logout();
    router.push("/login");
  }

  if (isLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-gray-950 text-white">
        Loading...
      </main>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-950">
      <div className="w-full max-w-lg rounded-xl bg-gray-900 p-10 text-center shadow-xl">
        <h1 className="mb-4 text-4xl font-bold text-white">
          Welcome to InterviewPilot 🚀
        </h1>

        <p className="mb-8 text-gray-400">
          Authentication completed successfully.
        </p>

        <Button
          text="Logout"
          onClick={handleLogout}
          className="bg-red-600 hover:bg-red-700"
        />
      </div>
    </main>
  );
}