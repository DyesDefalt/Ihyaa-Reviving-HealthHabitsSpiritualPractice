import { useCallback, useEffect, useRef, useState } from 'react';
import { api } from '../api';
import type { Lang } from '../i18n';
import { streamCoach } from './stream';

export type CoachMessage = { id: string; role: 'user' | 'assistant'; content: string; model?: string; safety?: string };
export type CoachSession = { session_id: string; title: string; updated_at: string };
type Config = { model: string; provider: string; consent_required: boolean; consent_version: string; max_message_length: number };

export function useCoach(userId: string | undefined, lang: Lang) {
  const [config, setConfig] = useState<Config | null>(null);
  const [sessions, setSessions] = useState<CoachSession[]>([]);
  const [sessionId, setSessionId] = useState('');
  const [messages, setMessages] = useState<CoachMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const locked = useRef(false);
  const mounted = useRef(true);
  const abort = useRef<AbortController | null>(null);

  const load = useCallback(async () => {
    if (!userId) return;
    setLoading(true);
    setError('');
    try {
      const [cfg, list] = await Promise.all([api('/coach/config'), api('/coach/sessions')]);
      let selected = list[0];
      if (!selected) { selected = await api('/coach/sessions', { method: 'POST' }); list.push(selected); }
      const history = await api(`/coach/history?session_id=${selected.session_id}`);
      if (!mounted.current) return;
      setConfig(cfg); setSessions(list); setSessionId(selected.session_id); setMessages(history);
    } catch { if (mounted.current) setError('load_error'); }
    finally { if (mounted.current) setLoading(false); }
  }, [userId]);

  useEffect(() => {
    mounted.current = true;
    load();
    return () => { mounted.current = false; abort.current?.abort(); };
  }, [load]);

  async function manage(action: () => Promise<void>) {
    if (locked.current || loading) return false;
    locked.current = true; setBusy(true); setError('');
    try { await action(); return true; }
    catch (e: any) { setError(e.detail || e.message || 'coach_unavailable'); return false; }
    finally { locked.current = false; if (mounted.current) setBusy(false); }
  }

  async function select(id: string) {
    return manage(async () => {
      const history = await api(`/coach/history?session_id=${id}`);
      setMessages(history); setSessionId(id); setInput('');
    });
  }

  async function newChat() {
    return manage(async () => {
      const session = await api('/coach/sessions', { method: 'POST' });
      setSessions((list) => [session, ...list]); setSessionId(session.session_id);
      setMessages([]); setInput('');
    });
  }

  async function deleteChat() {
    return manage(async () => {
      await api(`/coach/sessions/${sessionId}`, { method: 'DELETE' });
      const list = await api('/coach/sessions');
      let next = list[0];
      if (!next) { next = await api('/coach/sessions', { method: 'POST' }); list.push(next); }
      const history = await api(`/coach/history?session_id=${next.session_id}`);
      setSessions(list); setSessionId(next.session_id); setMessages(history); setInput('');
    });
  }

  async function consent(accepted: boolean) {
    return manage(async () => {
      await api('/coach/consent', { method: 'POST', body: { accepted, version: config?.consent_version } });
      setConfig((cfg) => cfg ? { ...cfg, consent_required: !accepted } : cfg);
    });
  }

  async function send(text: string) {
    const value = text.trim();
    if (!value || locked.current || loading || !sessionId || config?.consent_required) return;
    locked.current = true; setBusy(true); setError(''); setInput('');
    const userMsg = `pending-user-${Date.now()}`;
    const assistantMsg = `pending-assistant-${Date.now()}`;
    setMessages((old) => [...old, { id: userMsg, role: 'user', content: value }, { id: assistantMsg, role: 'assistant', content: '' }]);
    const controller = new AbortController(); abort.current = controller;
    const timer = setTimeout(() => controller.abort(), 70000);
    try {
      await streamCoach(sessionId, value, lang, controller.signal, ({ type, data }) => {
        if (!mounted.current) return;
        if (type === 'delta') setMessages((old) => old.map((m) => m.id === assistantMsg ? { ...m, content: m.content + data.text } : m));
        if (type === 'done') setMessages((old) => old.map((m) => m.id === userMsg ? { ...m, id: data.user_message_id }
          : m.id === assistantMsg ? { ...m, id: data.assistant_message_id, content: data.reply, model: data.model, safety: data.safety } : m));
      });
      const list = await api('/coach/sessions');
      if (mounted.current) setSessions(list);
    } catch (e: any) {
      if (mounted.current) {
        setMessages((old) => old.filter((m) => m.id !== userMsg && m.id !== assistantMsg));
        setInput(value); setError(typeof e.detail === 'string' ? e.detail : e.message);
      }
    } finally {
      clearTimeout(timer); locked.current = false; abort.current = null;
      if (mounted.current) setBusy(false);
    }
  }

  return { config, sessions, sessionId, messages, input, setInput, loading, busy, error,
    load, select, newChat, deleteChat, consent, send };
}