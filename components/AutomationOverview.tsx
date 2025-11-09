import type { AutomationPipeline, PipelineStatus } from '../lib/automationStore';

interface AutomationOverviewProps {
  overallStatus: PipelineStatus;
  lastUpdated: string;
  pipelines: AutomationPipeline[];
  onTrigger: (pipelineId: string) => void;
  triggering: string | null;
}

const statusColorMap: Record<PipelineStatus, string> = {
  idle: '#fbbf24',
  running: '#38bdf8',
  success: '#4ade80',
  error: '#f87171',
};

export function AutomationOverview({
  overallStatus,
  lastUpdated,
  pipelines,
  onTrigger,
  triggering,
}: AutomationOverviewProps) {
  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Automation Status</h2>
        <span className="badge">
          <span
            style={{
              width: 12,
              height: 12,
              borderRadius: '50%',
              display: 'inline-block',
              backgroundColor: statusColorMap[overallStatus],
            }}
          ></span>
          {overallStatus.toUpperCase()}
        </span>
      </div>
      <p>Last updated {new Date(lastUpdated).toLocaleTimeString()}</p>
      <ul className="pipeline-list">
        {pipelines.map((pipeline) => {
          const isTriggering = triggering === pipeline.id;
          return (
            <li key={pipeline.id}>
              <div>
                <strong>{pipeline.name}</strong>
                <div style={{ color: 'rgba(226, 232, 240, 0.75)', fontSize: '0.875rem' }}>
                  Last run {new Date(pipeline.lastRun).toLocaleTimeString()} · Success Rate{' '}
                  {(pipeline.successRate * 100).toFixed(0)}%
                </div>
              </div>
              <button onClick={() => onTrigger(pipeline.id)} disabled={isTriggering}>
                {isTriggering ? 'Triggering…' : 'Trigger'}
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
