import Feather from '@expo/vector-icons/Feather';
import * as Haptics from 'expo-haptics';
import React, { useState } from 'react';
import { Platform, Pressable, Text, View } from 'react-native';
import { useI18n } from '../i18n';
import { pillarColor, radii, shadow, space, useTheme } from '../theme';
import { useFonts } from './ui';

export type Task = {
  id: string;
  pillar: string;
  title: string;
  description: string;
  duration_minutes: number;
  points_reward: number;
  completed: boolean;
  scheduled_time: string;
  day_number: number;
  quran_reference: string | null;
  hadith_reference: string | null;
  science_reference: string | null;
};

const PILLAR_ICON: Record<string, keyof typeof Feather.glyphMap> = {
  physical: 'activity',
  nutrition: 'coffee',
  mental: 'cloud',
  spiritual: 'moon',
};

function Evidence({ label, text, tint }: { label: string; text: string; tint: string }) {
  const { c } = useTheme();
  const f = useFonts();
  const { align, lang } = useI18n();
  return (
    <View style={{ backgroundColor: c.surfaceAlt, borderRadius: radii.sm, padding: 12, gap: 4, borderStartWidth: 3, borderStartColor: tint }}>
      <Text style={{ fontFamily: f.semibold, fontSize: 10.5, letterSpacing: 0.6, color: tint, textAlign: align, textTransform: 'uppercase' }}>
        {label}
      </Text>
      <Text
        style={{
          fontFamily: lang === 'ar' ? 'Amiri_400Regular' : f.regular,
          fontSize: lang === 'ar' ? 15.5 : 13,
          lineHeight: lang === 'ar' ? 26 : 20,
          color: c.textDim,
          textAlign: align,
        }}
      >
        {text}
      </Text>
    </View>
  );
}

export function TaskCard({
  task,
  onToggle,
  readOnly,
}: {
  task: Task;
  onToggle?: (task: Task) => void;
  readOnly?: boolean;
}) {
  const { c, mode } = useTheme();
  const { t, row, align } = useI18n();
  const f = useFonts();
  const [open, setOpen] = useState(false);
  const tint = pillarColor[task.pillar] ?? c.primary;

  const toggle = () => {
    if (readOnly || !onToggle) return;
    if (Platform.OS !== 'web') Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light).catch(() => undefined);
    onToggle(task);
  };

  return (
    <View
      testID={`task-card-${task.id}`}
      style={{
        backgroundColor: c.surface,
        borderRadius: radii.md,
        borderWidth: 1,
        borderColor: task.completed ? tint + '55' : c.border,
        overflow: 'hidden',
        ...shadow(mode, 'sm'),
      }}
    >
      <View style={{ flexDirection: row, alignItems: 'flex-start', gap: space.md, padding: space.md }}>
        <Pressable
          testID={`task-toggle-${task.id}`}
          onPress={toggle}
          hitSlop={10}
          style={{
            width: 30,
            height: 30,
            borderRadius: radii.full,
            borderWidth: 2,
            borderColor: task.completed ? tint : c.border,
            backgroundColor: task.completed ? tint : 'transparent',
            alignItems: 'center',
            justifyContent: 'center',
            marginTop: 2,
            ...(Platform.OS === 'web' ? ({ cursor: readOnly ? 'default' : 'pointer' } as any) : {}),
          }}
        >
          {task.completed ? <Feather name="check" size={16} color="#fff" /> : null}
        </Pressable>

        <Pressable
          testID={`task-expand-${task.id}`}
          onPress={() => setOpen((o) => !o)}
          style={{ flex: 1, gap: 6, ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}) }}
        >
          <View style={{ flexDirection: row, alignItems: 'center', gap: space.sm, flexWrap: 'wrap' }}>
            <View
              style={{
                flexDirection: row,
                alignItems: 'center',
                gap: 5,
                backgroundColor: tint + '1A',
                paddingHorizontal: 9,
                paddingVertical: 4,
                borderRadius: radii.full,
              }}
            >
              <Feather name={PILLAR_ICON[task.pillar] ?? 'circle'} size={11} color={tint} />
              <Text style={{ fontFamily: f.medium, fontSize: 10.5, color: tint }}>{t(`pillar.${task.pillar}`)}</Text>
            </View>
            <Text style={{ fontFamily: f.regular, fontSize: 11, color: c.textDim }}>
              {task.duration_minutes} {t('common.min')}
            </Text>
            <Text style={{ fontFamily: f.regular, fontSize: 11, color: c.textDim }}>· {task.scheduled_time}</Text>
          </View>

          <Text
            style={{
              fontFamily: f.semibold,
              fontSize: 16,
              lineHeight: 23,
              color: task.completed ? c.textDim : c.text,
              textDecorationLine: task.completed ? 'line-through' : 'none',
              textAlign: align,
            }}
          >
            {task.title}
          </Text>

          <View style={{ flexDirection: row, alignItems: 'center', gap: 5 }}>
            <Feather name="star" size={11} color={c.warning} />
            <Text style={{ fontFamily: f.medium, fontSize: 11, color: c.textDim }}>
              +{task.points_reward} {t('common.points')}
            </Text>
            <Feather name={open ? 'chevron-up' : 'chevron-down'} size={14} color={c.textDim} style={{ marginStart: 4 }} />
          </View>
        </Pressable>
      </View>

      {open ? (
        <View style={{ paddingHorizontal: space.md, paddingBottom: space.md, gap: space.sm }}>
          <View style={{ height: 1, backgroundColor: c.border, marginBottom: 4 }} />
          <Text style={{ fontFamily: f.regular, fontSize: 14, lineHeight: 22, color: c.text, textAlign: align }}>
            {task.description}
          </Text>
          {task.quran_reference ? <Evidence label={t('ref.quran')} text={task.quran_reference} tint={c.success} /> : null}
          {task.hadith_reference ? <Evidence label={t('ref.hadith')} text={task.hadith_reference} tint={c.secondary} /> : null}
          {task.science_reference ? <Evidence label={t('ref.science')} text={task.science_reference} tint="#4A6FA5" /> : null}
        </View>
      ) : null}
    </View>
  );
}
