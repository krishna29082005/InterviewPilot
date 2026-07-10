"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import Link from "next/link";

import AuthCard from "@/components/auth/AuthCard";
import SignupForm from "@/components/auth/SignupForm";

export default function SignupPage() {
  const router = useRouter();

  useEffect(() => {
    if (localStorage.getItem("access_token")) {
      router.replace("/dashboard");
    }
  }, [router]);

  return (
    <AuthCard
      title="Create your account"
      subtitle="Start preparing for your dream job today."
      footer={
        <>
          Already have an account?{" "}
          <Link
            href="/login"
            className="font-medium text-blue-500 hover:text-blue-400"
          >
            Login
          </Link>
        </>
      }
    >
      <SignupForm />
    </AuthCard>
  );
}