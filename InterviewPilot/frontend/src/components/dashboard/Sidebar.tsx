"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

import {
  LayoutDashboard,
  FileText,
  BrainCircuit,
  BarChart3,
  Settings,
  LogOut,
} from "lucide-react";

import { useAuth } from "@/context/AuthContext";

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  const { logout, user } = useAuth();

  function handleLogout() {
    logout();
    router.replace("/login");
  }

  const links = [
    {
      href: "/dashboard",
      label: "Dashboard",
      icon: LayoutDashboard,
    },
    {
      href: "/resume",
      label: "Resume",
      icon: FileText,
    },
    {
      href: "/interviews",
      label: "Interviews",
      icon: BrainCircuit,
    },
    {
      href: "/analytics",
      label: "Analytics",
      icon: BarChart3,
    },
    {
      href: "/settings",
      label: "Settings",
      icon: Settings,
    },
  ];

  return (
    <aside className="flex w-72 flex-col justify-between border-r border-gray-800 bg-gray-900 px-6 py-8">

      <div>

        <div className="mb-12">
          <h1 className="text-3xl font-bold text-white">
            🚀 InterviewPilot
          </h1>

          <p className="mt-2 text-sm text-gray-400">
            AI Interview Preparation
          </p>
        </div>

        <nav className="space-y-2">
          {links.map((link) => {
            const Icon = link.icon;
            const active = pathname === link.href;

            return (
              <Link
                key={link.href}
                href={link.href}
                className={`flex items-center gap-3 rounded-xl px-4 py-3 transition-all ${
                  active
                    ? "bg-blue-600 text-white"
                    : "text-gray-400 hover:bg-gray-800 hover:text-white"
                }`}
              >
                <Icon size={20} />
                {link.label}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="border-t border-gray-800 pt-6">

        <div className="mb-4">
          <p className="font-medium text-white">
            {user?.username}
          </p>

          <p className="text-sm text-gray-400">
            {user?.email}
          </p>
        </div>

        <button
          onClick={handleLogout}
          className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-red-400 transition hover:bg-red-500/10"
        >
          <LogOut size={20} />
          Logout
        </button>

      </div>
    </aside>
  );
}