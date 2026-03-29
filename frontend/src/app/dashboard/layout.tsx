// src/app/dashboard/layout.tsx
import Sidebar from "@/components/dashboard/Sidebar";
import Navbar from "@/components/dashboard/Navbar";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen w-full bg-slate-950 border-4 border-red-500"> {/* Borda para teste */}
      <div className="w-64 shrink-0 border-r border-white/10">
        <Sidebar />
      </div>

      <div className="flex flex-col flex-1 min-w-0">
        <Navbar />
        <main className="flex-1 overflow-y-auto p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
