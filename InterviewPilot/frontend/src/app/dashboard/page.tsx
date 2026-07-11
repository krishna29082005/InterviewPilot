"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import DashboardLayout from "@/components/dashboard/DashboardLayout";
import DashboardCard from "@/components/dashboard/DashboardCard";
import { useAuth } from "@/context/AuthContext";
import {
  FileText,
  BrainCircuit,
  BarChart3,
  Rocket,
} from "lucide-react";


export default function DashboardPage() {
  const router = useRouter();

 const {
  user,
  isAuthenticated,
  isLoading,
} = useAuth();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.replace("/login");
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-gray-950 text-white">
        Loading...
      </main>
    );
  }

  if (!isAuthenticated) return null;

  return (
    <DashboardLayout>
      <div className="mb-10">

  <p className="text-sm uppercase tracking-widest text-blue-400">
    Interview Pilot
  </p>

  <h1 className="mt-2 text-5xl font-bold text-white">
    Welcome back, {user?.username} 👋
  </h1>

  <p className="mt-3 text-lg text-gray-400">
    Ready to ace your next interview today?
  </p>

</div>

     <div className="mt-10 grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">

  <DashboardCard
    icon={<FileText size={28} />}
    title="Resume"
    value="0"
    description="Upload your resume."
  />

  <DashboardCard
    icon={<BrainCircuit size={28} />}
    title="Interviews"
    value="0"
    description="Mock interviews completed."
  />

  <DashboardCard
    icon={<BarChart3 size={28} />}
    title="Analytics"
    value="--"
    description="Performance insights."
  />

  <DashboardCard
    icon={<Rocket size={28} />}
    title="Get Started"
    value="🚀"
    description="Begin your preparation."
  />

</div>
    </DashboardLayout>
  );
}