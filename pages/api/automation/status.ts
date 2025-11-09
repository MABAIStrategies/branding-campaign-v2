import type { NextApiRequest, NextApiResponse } from 'next';
import { getSnapshot, refreshSnapshot } from '../../../lib/automationStore';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const snapshot = refreshSnapshot();
    return res.status(200).json(snapshot);
  }

  const snapshot = getSnapshot();
  return res.status(200).json(snapshot);
}
