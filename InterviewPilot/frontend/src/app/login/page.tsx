import Link from "next/link";

import AuthCard from "@/components/auth/AuthCard";
import LoginForm from "@/components/auth/LoginForm";

export default function LoginPage() {
  return (
    <AuthCard
      title="Welcome Back"
      subtitle="Login to continue your interview preparation."
      footer={
        <>
          Don't have an account?{" "}
          <Link
            href="/signup"
            className="font-medium text-blue-500 transition hover:text-blue-400"
          >
            Create one
          </Link>
        </>
      }
    >
      <LoginForm />
    </AuthCard>
  );
}