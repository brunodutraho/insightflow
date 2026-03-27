"use client";

import { useQuery } from "@tanstack/react-query";
import { getDashboard } from "@/services/dashboard.service";

import Overview from "@/components/dashboard/Overview";
import KPIGrid from "@/components/dashboard/KPIGrid";
import InsightsList from "@/components/dashboard/InsightsList";
import SocialCard from "@/components/dashboard/SocialCard";

export default function DashboardPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["dashboard"],
    queryFn: () => getDashboard(1),
  });

  if (isLoading) return <p>Loading...</p>;
  if (error || !data) return <p>Error loading dashboard</p>;

  return (
    <div style={{ padding: 24 }}>
      <h1>Dashboard</h1>

      <Overview overview={data.overview} score={data.score} />

      <KPIGrid summary={data.kpis.summary} />

      <InsightsList insights={data.insights} />

      <SocialCard social={data.social} />
    </div>
  );
}