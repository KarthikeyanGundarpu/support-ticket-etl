import json
import os
from typing import List, Dict, Any
import pandas as pd


class AnalyticsEngine:
    def __init__(self, records: List[Dict[str, Any]], output_dir: str = "output") -> None:
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.df = pd.DataFrame(records)

    def summarize_by_endpoint(self) -> pd.DataFrame:
        if self.df.empty:
            return pd.DataFrame()

        self.df["is_error"] = (self.df["level"] == "ERROR").astype(int)

        summary = (
            self.df.groupby("endpoint", as_index=False)
            .agg(
                total_requests=("id", "count"),
                error_count=("is_error", "sum"),
                avg_latency_ms=("latency_ms", "mean"),
                p95_latency_ms=("latency_ms", lambda s: s.quantile(0.95)),
            )
            .assign(
                error_rate_pct=lambda d: (d["error_count"] / d["total_requests"] * 100).round(2),
                avg_latency_ms=lambda d: d["avg_latency_ms"].round(2),
                p95_latency_ms=lambda d: d["p95_latency_ms"].round(2),
            )
            .sort_values(by="error_rate_pct", ascending=False)
        )
        return summary

    def export_reports(self, malformed_count: int) -> Dict[str, str]:
        summary_df = self.summarize_by_endpoint()
        csv_path = os.path.join(self.output_dir, "endpoint_metrics.csv")
        json_path = os.path.join(self.output_dir, "pipeline_summary.json")

        # 1. Export endpoint table to CSV
        summary_df.to_csv(csv_path, index=False)

        # 2. Export executive JSON summary
        report_payload = {
            "total_valid_logs": int(len(self.df)),
            "malformed_lines_skipped": malformed_count,
            "overall_error_count": int((self.df["level"] == "ERROR").sum()) if not self.df.empty else 0,
            "slow_requests_count": int(self.df["is_slow"].sum()) if not self.df.empty else 0,
            "endpoint_breakdown": summary_df.to_dict(orient="records"),
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_payload, f, indent=4)

        return {"csv": csv_path, "json": json_path}