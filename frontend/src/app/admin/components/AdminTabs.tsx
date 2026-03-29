"use client";

type Tab = "overview" | "users" | "companies" | "system";

export default function AdminTabs({
  tab,
  setTab,
}: {
  tab: Tab;
  setTab: (tab: Tab) => void;
}) {
  const tabs = [
    { id: "overview", label: "Visão Geral" },
    { id: "users", label: "Usuários" },
    { id: "companies", label: "Empresas" },
    { id: "system", label: "Sistema" },
  ];

  return (
    <div className="flex gap-4 border-b border-slate-800 pb-2">
      {tabs.map((t) => (
        <button
          key={t.id}
          onClick={() => setTab(t.id as Tab)}
          className={`px-4 py-2 rounded-lg text-sm ${
            tab === t.id
              ? "bg-slate-800 text-white"
              : "text-slate-400 hover:text-white"
          }`}
        >
          {t.label}
        </button>
      ))}
    </div>
  );
}