import { ReactNode } from "react";

interface DashboardCardProps {
  icon: ReactNode;
  title: string;
  value: string;
  description: string;
}

export default function DashboardCard({
  icon,
  title,
  value,
  description,
}: DashboardCardProps) {
  return (
    <div className="rounded-2xl border border-gray-800 bg-gray-900 p-6 transition hover:border-blue-500 hover:shadow-xl">
      <div className="mb-4 flex items-center justify-between">
        <div className="rounded-xl bg-blue-500/10 p-3 text-blue-400">
          {icon}
        </div>

        <span className="text-3xl font-bold text-white">
          {value}
        </span>
      </div>

      <h2 className="text-xl font-semibold text-white">
        {title}
      </h2>

      <p className="mt-2 text-sm text-gray-400">
        {description}
      </p>
    </div>
  );
}