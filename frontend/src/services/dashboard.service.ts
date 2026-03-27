import api from "./api";
import { DashboardResponse } from "@/types/dashboard";

export async function getDashboard(clientId: number) {
  const { data } = await api.get<DashboardResponse>(
    `/dashboard/?client_id=${clientId}`
  );

  return data;
}