"use client";

import { ReactNode } from "react";

type Props = {
  text: string;
  type?: "button" | "submit" | "reset";
  onClick?: () => void;
  disabled?: boolean;
  loading?: boolean;
  loadingText?: string;
  className?: string;
  icon?: ReactNode;
};

export default function Button({
  text,
  type = "button",
  onClick,
  disabled = false,
  loading = false,
  loadingText = "Loading...",
  className = "",
  icon,
}: Props) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`
        flex
        w-full
        items-center
        justify-center
        gap-2
        rounded-xl
        bg-blue-600
        px-4
        py-3
        font-semibold
        text-white
        transition-all
        duration-200
        hover:bg-blue-700
        hover:scale-[1.02]
        active:scale-[0.98]
        focus:outline-none
        focus:ring-2
        focus:ring-blue-500/40
        disabled:cursor-not-allowed
        disabled:opacity-60
        disabled:hover:scale-100
        ${className}
      `}
    >
      {loading ? (
        <>
          <svg
            className="h-5 w-5 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-20"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-100"
              fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            />
          </svg>

          {loadingText}
        </>
      ) : (
        <>
          {icon}
          <span>{text}</span>
        </>
      )}
    </button>
  );
}