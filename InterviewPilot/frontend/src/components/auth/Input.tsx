"use client";

import { ReactNode } from "react";

type Props = {
  id: string;
  label: string;
  type?: string;
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  errorMessage?: string;
  disabled?: boolean;
  rightElement?: ReactNode;
};

export default function Input({
  id,
  label,
  type = "text",
  placeholder,
  value,
  onChange,
  errorMessage,
  disabled = false,
  rightElement,
}: Props) {
  return (
    <div className="space-y-2">
      <label
        htmlFor={id}
        className="block text-sm font-medium text-gray-300"
      >
        {label}
      </label>

      <div className="relative">
        <input
          id={id}
          type={type}
          placeholder={placeholder}
          value={value}
          disabled={disabled}
          onChange={(e) => onChange(e.target.value)}
          className={`
            w-full
            rounded-xl
            border
            ${
              errorMessage
                ? "border-red-500"
                : "border-gray-700"
            }
            bg-gray-900
            px-4
            py-3
            ${
              rightElement
                ? "pr-12"
                : ""
            }
            text-white
            placeholder:text-gray-500
            outline-none
            transition-all
            duration-200
            focus:border-blue-500
            focus:ring-2
            focus:ring-blue-500/30
            disabled:opacity-50
          `}
        />

        {rightElement && (
          <div className="absolute inset-y-0 right-3 flex items-center">
            {rightElement}
          </div>
        )}
      </div>

      {errorMessage && (
        <p className="text-sm text-red-400">
          {errorMessage}
        </p>
      )}
    </div>
  );
}