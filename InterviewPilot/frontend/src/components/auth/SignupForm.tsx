"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Eye, EyeOff } from "lucide-react";

import Input from "./Input";
import Button from "./Button";

import {
  signupUser,
  loginUser,
  getCurrentUser,
} from "@/lib/api";

import { useAuth } from "@/context/AuthContext";

export default function SignupForm() {
  const router = useRouter();
  const { login } = useAuth();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  async function handleSubmit(
    e: React.FormEvent<HTMLFormElement>
  ) {
    e.preventDefault();

    setError("");

    // Validation
    if (!name.trim()) {
      setError("Name is required.");
      return;
    }

    if (!email.trim()) {
      setError("Email is required.");
      return;
    }

    if (!password.trim()) {
      setError("Password is required.");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    setLoading(true);

    try {
      // Create account
      await signupUser({
        name,
        email,
        password,
      });

      // Login automatically
      const loginResponse = await loginUser({
        email,
        password,
      });

      // Fetch current user
      const currentUser = await getCurrentUser(
        loginResponse.access_token
      );

      // Save token & user
      login(
        loginResponse.access_token,
        currentUser
      );

      // Clear form
      setName("");
      setEmail("");
      setPassword("");

      // Go to dashboard
      router.push("/dashboard");
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Something went wrong.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-5"
    >
      <Input
        id="name"
        label="Name"
        placeholder="Enter your name"
        value={name}
        onChange={setName}
      />

      <Input
        id="email"
        label="Email"
        type="email"
        placeholder="Enter your email"
        value={email}
        onChange={setEmail}
      />

      <Input
        id="password"
        label="Password"
        type={showPassword ? "text" : "password"}
        placeholder="Enter your password"
        value={password}
        onChange={setPassword}
        rightElement={
          <button
            type="button"
            onClick={() =>
              setShowPassword((prev) => !prev)
            }
            className="cursor-pointer text-gray-400 transition hover:text-white"
          >
            {showPassword ? (
              <EyeOff size={18} />
            ) : (
              <Eye size={18} />
            )}
          </button>
        }
      />

      {error && (
        <div className="rounded-lg border border-red-500/40 bg-red-500/10 p-3 text-sm text-red-300">
          {error}
        </div>
      )}

      <Button
        text="Create Account"
        type="submit"
        loading={loading}
        loadingText="Creating Account..."
      />
    </form>
  );
}