import type { NextApiRequest, NextApiResponse } from 'next';
import { triggerPipeline } from '../../../lib/automationStore';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method Not Allowed' });
  }

  const { pipelineId } = req.body as { pipelineId?: string };

  if (!pipelineId) {
    return res.status(400).json({ message: 'pipelineId is required' });
  }

  const snapshot = triggerPipeline(pipelineId);
  return res.status(200).json({
    message: `Pipeline ${pipelineId} triggered`,
    snapshot,
  });
}
