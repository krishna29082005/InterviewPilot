import Link from "next/link";

import AuthCard from "@/components/auth/AuthCard";
import SignupForm from "@/components/auth/SignupForm";

export default function SignupPage() {
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