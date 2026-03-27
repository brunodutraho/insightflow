export interface DashboardResponse {
  overview: {
    score: number | null;
    level: string | null;
    status: string;
  };
  kpis: {
    summary: Record<string, number>;
    timeseries: any[];
  };
  insights: {
    message: string;
    type?: string;
    impact?: string;
  }[];
  social: {
    followers: number;
    engagement: number;
    posts: number;
    growth_rate: number;
  } | null;
  score: {
    value?: number;
    level?: string;
    available?: boolean;
    message?: string;
  };
  features: {
    score_enabled: boolean;
  };
}