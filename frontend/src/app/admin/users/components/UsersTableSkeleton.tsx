export function UsersTableSkeleton() {
  return (
    <div className="bg-white dark:bg-slate-900 p-8 rounded-2xl border border-slate-200 dark:border-slate-800 animate-pulse space-y-6 shadow-sm">
      {/* Header do Skeleton */}
      <div className="flex gap-4 border-b border-slate-100 dark:border-slate-800 pb-4">
        <div className="h-4 bg-slate-100 dark:bg-slate-800 rounded w-1/4" />
        <div className="h-4 bg-slate-100 dark:bg-slate-800 rounded w-1/4" />
        <div className="h-4 bg-slate-100 dark:bg-slate-800 rounded w-1/4" />
      </div>

      {/* Linhas do Skeleton */}
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="flex items-center justify-between gap-4 py-2">
          <div className="space-y-2 flex-1">
             <div className="h-4 bg-slate-100 dark:bg-slate-800 rounded w-3/4" />
             <div className="h-3 bg-slate-50 dark:bg-slate-800/50 rounded w-1/2" />
          </div>
          <div className="h-8 bg-slate-100 dark:bg-slate-800 rounded-full w-20" />
          <div className="h-8 bg-slate-100 dark:bg-slate-800 rounded-lg w-10" />
        </div>
      ))}
    </div>
  );
}
