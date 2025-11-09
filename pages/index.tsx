import Head from 'next/head';
import { useCallback, useState } from 'react';
import type { GetServerSideProps } from 'next';
import type { AutomationSnapshot } from '../lib/automationStore';
import { getSnapshot } from '../lib/automationStore';
import { AutomationOverview } from '../components/AutomationOverview';
import { TrendChart } from '../components/TrendChart';
import { TrendingAutomations } from '../components/TrendingAutomations';

interface HomeProps {
  initialSnapshot: AutomationSnapshot;
}

export const getServerSideProps: GetServerSideProps<HomeProps> = async () => {
  const snapshot = getSnapshot();
  return {
    props: {
      initialSnapshot: snapshot,
    },
  };
};

export default function Home({ initialSnapshot }: HomeProps) {
  const [snapshot, setSnapshot] = useState<AutomationSnapshot>(initialSnapshot);
  const [triggering, setTriggering] = useState<string | null>(null);

  const triggerPipeline = useCallback(async (pipelineId: string) => {
    setTriggering(pipelineId);
    try {
      const response = await fetch('/api/automation/trigger', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pipelineId }),
      });

      if (!response.ok) {
        throw new Error('Failed to trigger automation');
      }

      const data = await response.json();
      setSnapshot(data.snapshot);
    } catch (error) {
      console.error(error);
    } finally {
      setTriggering(null);
    }
  }, []);

  const refreshDashboard = useCallback(async () => {
    try {
      const response = await fetch('/api/automation/status', {
        method: 'POST',
      });
      const data: AutomationSnapshot = await response.json();
      setSnapshot(data);
    } catch (error) {
      console.error(error);
    }
  }, []);

  return (
    <>
      <Head>
        <title>Branding Automation Control Center</title>
        <meta
          name="description"
          content="Monitor the branding automation pipeline and discover trending campaign ideas."
        />
      </Head>
      <main>
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 style={{ fontSize: '2.5rem', marginBottom: 0 }}>Branding Automation Control Center</h1>
            <p style={{ color: 'rgba(226, 232, 240, 0.75)', maxWidth: 640 }}>
              Track campaign orchestration pipelines, trigger new automation runs, and watch trending
              concepts emerging from Reddit and Twitter.
            </p>
          </div>
          <button
            onClick={refreshDashboard}
            style={{
              background: 'linear-gradient(135deg, #22d3ee, #6366f1)',
              color: '#0f172a',
              border: 'none',
              padding: '0.75rem 1.5rem',
              borderRadius: '9999px',
              fontWeight: 700,
              cursor: 'pointer',
              boxShadow: '0 20px 35px rgba(14, 116, 144, 0.35)',
            }}
          >
            Refresh Insights
          </button>
        </header>

        <section className="dashboard-grid">
          <AutomationOverview
            overallStatus={snapshot.overallStatus}
            lastUpdated={snapshot.lastUpdated}
            pipelines={snapshot.pipelines}
            onTrigger={triggerPipeline}
            triggering={triggering}
          />
          <TrendChart data={snapshot.trends} />
          <TrendingAutomations items={snapshot.trendingAutomations} />
        </section>

        <footer>
          Powered by the 101 Automations branding campaign initiative.
        </footer>
      </main>
    </>
  );
}
