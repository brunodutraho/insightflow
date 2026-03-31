interface StatCardProps {
  label: string;
  value: string | number | undefined;
  loading?: boolean;
  prefix?: string;

  // NOVO
  change?: number; // ex: 12.5 ou -8.2
  isPercentage?: boolean; // define se value já é %
}

export function StatCard({
  label,
  value,
  loading,
  prefix,
  change,
  isPercentage,
}: StatCardProps) {
  // =========================
  // TREND (↑ ↓)
  // =========================
  const isPositive = (change ?? 0) >= 0;

  const trendIcon = change === undefined
    ? null
    : isPositive
    ? "↑"
    : "↓";

  const trendColor =
    change === undefined
      ? "text-gray-400"
      : isPositive
      ? "text-green-600"
      : "text-red-500";

  return (
    <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 p-6 rounded-xl shadow-sm hover:shadow-md transition">
      {/* LABEL */}
      <p className="text-sm font-medium text-gray-500 dark:text-slate-400 mb-1">
        {label}
      </p>

      {loading ? (
        <div className="h-8 w-24 bg-gray-200 dark:bg-slate-800 animate-pulse rounded" />
      ) : (
        <div className="flex items-end justify-between">
          {/* VALUE */}
          <h2 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
            {prefix} {value ?? 0}
            {isPercentage && "%"}
          </h2>

          {/* TREND */}
          {change !== undefined && (
            <span className={`text-sm font-semibold ${trendColor}`}>
              {trendIcon} {Math.abs(change).toFixed(2)}%
            </span>
          )}
        </div>
      )}
    </div>
  );
}