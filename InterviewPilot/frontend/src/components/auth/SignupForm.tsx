"use client";

import { useState } from "react";

import Input from "./Input";
import Button from "./Button";

import { signupUser } from "@/lib/api";

export default function SignupForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  async function handleSubmit(
    e: React.FormEvent<HTMLFormElement>
  ) {
    e.preventDefault();

    setError("");
    setSuccess("");

    // Frontend Validation
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
      const response = await signupUser({
        name,
        email,
        password,
      });

      setSuccess(response.message);

      setName("");
      setEmail("");
      setPassword("");
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
        onClick={() => setShowPassword(!showPassword)}
        className="text-gray-400 transition hover:text-white"
    >
      {showPassword ? "🙈" : "👁️"}
    </button>
  }
/>


      {error && (
        <div className="rounded-lg border border-red-500/40 bg-red-500/10 p-3 text-sm text-red-300">
          {error}
        </div>
      )}

      {success && (
        <div className="rounded-lg border border-green-500/40 bg-green-500/10 p-3 text-sm text-green-300">
          {success}
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