import type { TrendMetric } from '../lib/automationStore';

interface TrendChartProps {
  data: TrendMetric[];
}

export function TrendChart({ data }: TrendChartProps) {
  const maxValue = Math.max(...data.map((metric) => metric.value), 1);
  return (
    <div className="card">
      <h2>Weekly Automation Runs</h2>
      <p>Track how many automation flows executed each day this week.</p>
      <div className="trends-chart">
        {data.map((metric) => (
          <div
            key={metric.label}
            className="bar"
            style={{ height: `${Math.max((metric.value / maxValue) * 100, 8)}%` }}
          >
            <div>
              <div>{metric.value}</div>
              <small style={{ color: '#e2e8f0' }}>{metric.label}</small>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
