"use client";
import { Eye, EyeOff } from "lucide-react";
import { useState } from "react";
import { useRouter } from "next/navigation";

import Input from "./Input";
import Button from "./Button";

import {
  loginUser,
  getCurrentUser,
} from "@/lib/api";

import { useAuth } from "@/context/AuthContext";

export default function LoginForm() {
  const router = useRouter();
  const { login } = useAuth();

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

    if (!email.trim()) {
      setError("Email is required.");
      return;
    }

    if (!password.trim()) {
      setError("Password is required.");
      return;
    }

    setLoading(true);

    try {
      const response = await loginUser({
        email,
        password,
      });

      const currentUser = await getCurrentUser(
        response.access_token
      );

      login(response.access_token, currentUser);

      setEmail("");
      setPassword("");

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
            onMouseDown={(e) => e.preventDefault()}
            onClick={() => {
              console.log("clicked", showPassword);
              setShowPassword((prev) => !prev);
            }}
            className="cursor-pointer select-none text-gray-400 transition hover:text-white"
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
        text="Login"
        type="submit"
        loading={loading}
        loadingText="Signing In..."
      />
    </form>
  );
}