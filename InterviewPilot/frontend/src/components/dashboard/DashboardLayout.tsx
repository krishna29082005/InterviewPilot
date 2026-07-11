import { ReactNode } from "react";
import Sidebar from "./Sidebar";

interface DashboardLayoutProps {
  children: ReactNode;
}

export default function DashboardLayout({
  children,
}: DashboardLayoutProps) {
  return (
    <main className="flex min-h-screen bg-gray-950">
      <Sidebar />

      <section className="flex-1 p-8">
        {children}
      </section>
    </main>
  );
}