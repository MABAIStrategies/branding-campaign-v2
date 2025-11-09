export type PipelineStatus = 'idle' | 'running' | 'success' | 'error';

export interface AutomationPipeline {
  id: string;
  name: string;
  status: PipelineStatus;
  lastRun: string;
  successRate: number;
  campaignsGenerated: number;
}

export interface TrendMetric {
  label: string;
  value: number;
}

export interface TrendingAutomation {
  id: string;
  title: string;
  platform: 'Reddit' | 'Twitter';
  summary: string;
  engagement: number;
}

export interface AutomationSnapshot {
  overallStatus: PipelineStatus;
  pipelines: AutomationPipeline[];
  trends: TrendMetric[];
  trendingAutomations: TrendingAutomation[];
  lastUpdated: string;
}

let snapshot: AutomationSnapshot = {
  overallStatus: 'idle',
  lastUpdated: new Date().toISOString(),
  pipelines: [
    {
      id: 'campaign-orchestrator',
      name: 'Campaign Orchestrator',
      status: 'success',
      lastRun: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
      successRate: 0.92,
      campaignsGenerated: 12,
    },
    {
      id: 'asset-designer',
      name: 'Asset Designer',
      status: 'running',
      lastRun: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
      successRate: 0.87,
      campaignsGenerated: 7,
    },
    {
      id: 'insight-miner',
      name: 'Insight Miner',
      status: 'idle',
      lastRun: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString(),
      successRate: 0.8,
      campaignsGenerated: 18,
    },
  ],
  trends: [
    { label: 'Mon', value: 4 },
    { label: 'Tue', value: 6 },
    { label: 'Wed', value: 7 },
    { label: 'Thu', value: 10 },
    { label: 'Fri', value: 9 },
  ],
  trendingAutomations: [
    {
      id: 'reddit-ai-storyteller',
      title: 'AI Storyteller Challenge',
      platform: 'Reddit',
      summary: 'Community crowdsourcing brand stories with AI-assisted prompts.',
      engagement: 6400,
    },
    {
      id: 'twitter-brandwave',
      title: '#BrandWave Launch Sequencer',
      platform: 'Twitter',
      summary: 'Real-time sequencing of campaign drops with live sentiment tracking.',
      engagement: 5400,
    },
    {
      id: 'reddit-visualizer',
      title: 'Immersive Visualizer Loop',
      platform: 'Reddit',
      summary: 'Generative mood boards for weekly product drops.',
      engagement: 4200,
    },
  ],
};

function computeOverallStatus(pipelines: AutomationPipeline[]): PipelineStatus {
  if (pipelines.some((pipeline) => pipeline.status === 'running')) {
    return 'running';
  }
  if (pipelines.some((pipeline) => pipeline.status === 'error')) {
    return 'error';
  }
  if (pipelines.every((pipeline) => pipeline.status === 'success')) {
    return 'success';
  }
  return 'idle';
}

export function getSnapshot(): AutomationSnapshot {
  return snapshot;
}

export function triggerPipeline(pipelineId: string): AutomationSnapshot {
  snapshot = {
    ...snapshot,
    pipelines: snapshot.pipelines.map((pipeline) => {
      if (pipeline.id === pipelineId) {
        const updatedStatus: PipelineStatus = pipeline.status === 'running' ? 'success' : 'running';
        return {
          ...pipeline,
          status: updatedStatus,
          lastRun: new Date().toISOString(),
          campaignsGenerated:
            updatedStatus === 'success'
              ? pipeline.campaignsGenerated + Math.ceil(Math.random() * 3)
              : pipeline.campaignsGenerated,
        };
      }
      return pipeline;
    }),
    lastUpdated: new Date().toISOString(),
  };

  snapshot = {
    ...snapshot,
    overallStatus: computeOverallStatus(snapshot.pipelines),
  };

  return snapshot;
}

export function refreshSnapshot(): AutomationSnapshot {
  snapshot = {
    ...snapshot,
    lastUpdated: new Date().toISOString(),
    pipelines: snapshot.pipelines.map((pipeline) => ({
      ...pipeline,
      campaignsGenerated: Math.max(pipeline.campaignsGenerated, 1),
    })),
  };

  snapshot = {
    ...snapshot,
    overallStatus: computeOverallStatus(snapshot.pipelines),
  };

  return snapshot;
}
