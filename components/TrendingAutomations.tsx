import type { TrendingAutomation } from '../lib/automationStore';

interface TrendingAutomationsProps {
  items: TrendingAutomation[];
}

const platformColor: Record<TrendingAutomation['platform'], string> = {
  Reddit: '#ff4500',
  Twitter: '#38bdf8',
};

export function TrendingAutomations({ items }: TrendingAutomationsProps) {
  return (
    <div className="card">
      <h2>Trending Automations</h2>
      <p>Emerging ideas sourced from Reddit and Twitter communities.</p>
      <ul className="trending-list">
        {items.map((automation) => (
          <li key={automation.id} className="trending-item">
            <div>
              <span style={{ color: platformColor[automation.platform] }}>{automation.platform}</span>
              <div style={{ fontSize: '1.05rem', fontWeight: 600 }}>{automation.title}</div>
              <p>{automation.summary}</p>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontWeight: 700, color: '#38bdf8' }}>{automation.engagement.toLocaleString()}</div>
              <small style={{ color: 'rgba(226, 232, 240, 0.75)' }}>community engagements</small>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
