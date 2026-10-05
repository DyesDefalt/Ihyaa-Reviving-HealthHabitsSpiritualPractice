import React from 'react';
import { Txt } from '../components/ui';
import { useI18n } from '../i18n';
import { useTheme } from '../theme';
import type { CoachMessage } from './useCoach';

export const DecisionLabel = ({ message }: { message: CoachMessage }) => {
  const { lang } = useI18n();
  const { c } = useTheme();
  const d = message.decision;
  if (!d) return null;
  const labels: Record<string, string[]> = {
    nutrition: ['Food', 'Makanan'], movement: ['Movement', 'Gerak'], sleep: ['Sleep', 'Tidur'],
    motivation: ['Motivation', 'Motivasi'], medical_request: ['Medical referral', 'Rujukan medis'],
    religious_ruling: ['Scholar referral', 'Rujukan ulama'], emergency: ['Urgent support', 'Bantuan darurat'],
    other: ['General', 'Umum'], unclassified: ['Uncertain request', 'Pertanyaan belum jelas'],
  };
  const label = labels[d.intent]?.[lang === 'id' ? 1 : 0] ?? d.intent;
  const source = d.source === 'jev' ? 'Jev' : d.source === 'fallback'
    ? (lang === 'id' ? 'AI tidak tersedia' : 'AI unavailable') : (lang === 'id' ? 'Aturan keselamatan' : 'Safety rules');
  return <Txt testID={`coach-decision-${message.id}`} variant="caption" color={c.textDim}>{label} · {source}</Txt>;
};