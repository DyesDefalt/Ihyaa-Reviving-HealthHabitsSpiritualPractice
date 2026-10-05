import { api } from '../api';
import type { Lang } from '../i18n';

export type CoachEvent = { type: string; data: any };

export async function streamCoach(sessionId: string, message: string, language: Lang,
  signal: AbortSignal, receive: (event: CoachEvent) => void) {
  const response = await api('/coach/chat', {
    method: 'POST', stream: true, signal, body: { session_id: sessionId, message, language },
  });
  const reader = response.body?.getReader();
  if (!reader) throw new Error('coach_unavailable');
  const decoder = new TextDecoder();
  let buffer = '';
  let complete = false;
  try {
    while (true) {
      const { value, done } = await reader.read();
      buffer += decoder.decode(value, { stream: !done });
      let boundary: number;
      while ((boundary = buffer.indexOf('\n\n')) >= 0) {
        const frame = buffer.slice(0, boundary);
        buffer = buffer.slice(boundary + 2);
        const lines = frame.split('\n');
        const type = lines.find((line) => line.startsWith('event: '))?.slice(7);
        const payload = lines.filter((line) => line.startsWith('data: ')).map((line) => line.slice(6)).join('\n');
        if (!type || !payload) continue;
        const data = JSON.parse(payload);
        if (type === 'error') throw new Error(data.code);
        if (type === 'done') complete = true;
        receive({ type, data });
      }
      if (done) break;
    }
    if (!complete) throw new Error('coach_unavailable');
  } finally {
    await reader.cancel().catch(() => undefined);
    reader.releaseLock();
  }
}