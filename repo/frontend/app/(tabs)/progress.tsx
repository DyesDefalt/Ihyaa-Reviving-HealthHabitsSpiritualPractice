import Feather from '@expo/vector-icons/Feather';
import { LinearGradient } from 'expo-linear-gradient';
import { useFocusEffect } from 'expo-router';
import React, { useCallback, useState } from 'react';
import { ScrollView, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { api } from '../../src/api';
import { GeoPattern } from '../../src/components/GeoPattern';
import { ProgressRings } from '../../src/components/ProgressRings';
import { Card, Loader, Txt, useFonts } from '../../src/components/ui';
import { weekdayShort } from '../../src/dates';
import { useI18n } from '../../src/i18n';
import { pillarColor, radii, space, useTheme } from '../../src/theme';

type Summary = {
  challenge: any;
  points_balance: number;
  lifetime_points: number;
  current_streak: number;
  longest_streak: number;
  total_tasks: number;
  completed_tasks: number;
  completion_rate: number;
  pillars: Record<string, { total: number; done: number }>;
  last_7_days: { date: string; total: number; done: number; rate: number }[];
  total_checkins: number;
};

const PILLARS = ['spiritual', 'physical', 'nutrition', 'mental'];

export default function Progress() {
  const { c, mode } = useTheme();
  const { t, lang, row, align } = useI18n();
  const insets = useSafeAreaInsets();
  const f = useFonts();
  const [s, setS] = useState<Summary | null>(null);

  const load = useCallback(async () => {
    const data = await api('/progress/summary');
    setS(data);
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  if (!s) return <Loader testID="progress-loading" />;

  const rings = PILLARS.map((p) => {
    const row_ = s.pillars[p] ?? { total: 0, done: 0 };
    return { pct: row_.total ? (row_.done / row_.total) * 100 : 0, color: pillarColor[p] };
  });

  const stats = [
    { icon: 'zap' as const, label: t('prog.streak'), value: s.current_streak, id: 'stat-streak' },
    { icon: 'award' as const, label: t('prog.best'), value: s.longest_streak, id: 'stat-best' },
    { icon: 'star' as const, label: t('prog.points'), value: s.points_balance, id: 'stat-points' },
    { icon: 'edit-3' as const, label: t('prog.checkins'), value: s.total_checkins, id: 'stat-checkins' },
  ];

  const maxRate = Math.max(100, ...s.last_7_days.map((d) => d.rate));

  return (
    <ScrollView
      testID="progress-screen"
      style={{ flex: 1, backgroundColor: c.background }}
      contentContainerStyle={{ paddingTop: insets.top + space.lg, paddingBottom: 120, gap: space.md }}
      showsVerticalScrollIndicator={false}
    >
      <View style={{ paddingHorizontal: space.lg, gap: 2 }}>
        <Txt variant="h2" weight="bold">{t('prog.title')}</Txt>
        <Txt variant="small" color={c.textDim}>{t('prog.subtitle')}</Txt>
      </View>

      <View style={{ paddingHorizontal: space.lg }}>
        <LinearGradient
          colors={mode === 'light' ? ['#1B3B36', '#24534A'] : ['#16302C', '#1E463F']}
          style={{ borderRadius: radii.lg, padding: space.lg, flexDirection: row, alignItems: 'center', gap: space.lg, overflow: 'hidden' }}
        >
          <GeoPattern color="#FFFFFF" opacity={0.09} size={50} />
          <ProgressRings rings={rings} size={126} stroke={9} gap={3}>
            <View style={{ alignItems: 'center' }}>
              <Text testID="progress-rate" style={{ fontFamily: f.bold, fontSize: 26, color: '#fff' }}>{s.completion_rate}%</Text>
              <Text style={{ fontFamily: f.regular, fontSize: 10, color: 'rgba(255,255,255,0.6)' }}>{t('prog.rate')}</Text>
            </View>
          </ProgressRings>
          <View style={{ flex: 1, gap: space.sm }}>
            <Text style={{ fontFamily: f.medium, fontSize: 11, letterSpacing: 1, color: '#B5653E', textAlign: align }}>
              {t('prog.overall').toUpperCase()}
            </Text>
            <Text style={{ fontFamily: f.regular, fontSize: 13, color: 'rgba(255,255,255,0.82)', textAlign: align, lineHeight: 20 }}>
              {t('prog.tasks', { done: s.completed_tasks, total: s.total_tasks })}
            </Text>
            {PILLARS.map((p) => (
              <View key={p} style={{ flexDirection: row, alignItems: 'center', gap: 7 }}>
                <View style={{ width: 8, height: 8, borderRadius: 4, backgroundColor: pillarColor[p] }} />
                <Text style={{ fontFamily: f.regular, fontSize: 11.5, color: 'rgba(255,255,255,0.72)' }}>{t(`pillar.${p}`)}</Text>
              </View>
            ))}
          </View>
        </LinearGradient>
      </View>

      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: space.sm, paddingHorizontal: space.lg }}>
        {stats.map((st) => (
          <Card key={st.id} testID={st.id} style={{ width: '48%', gap: 6 }}>
            <Feather name={st.icon} size={16} color={c.secondary} />
            <Text style={{ fontFamily: f.bold, fontSize: 24, color: c.text, textAlign: align }}>{st.value}</Text>
            <Text style={{ fontFamily: f.regular, fontSize: 11.5, color: c.textDim, textAlign: align }}>{st.label}</Text>
          </Card>
        ))}
      </View>

      <View style={{ paddingHorizontal: space.lg, gap: space.sm }}>
        <Txt variant="h3" weight="bold">{t('prog.pillars')}</Txt>
        <Card style={{ gap: space.md }}>
          {PILLARS.map((p) => {
            const r = s.pillars[p] ?? { total: 0, done: 0 };
            const pct = r.total ? Math.round((r.done / r.total) * 100) : 0;
            return (
              <View key={p} style={{ gap: 6 }} testID={`pillar-bar-${p}`}>
                <View style={{ flexDirection: row, justifyContent: 'space-between' }}>
                  <Text style={{ fontFamily: f.medium, fontSize: 13.5, color: c.text }}>{t(`pillar.${p}`)}</Text>
                  <Text style={{ fontFamily: f.medium, fontSize: 13.5, color: pillarColor[p] }}>
                    {r.done}/{r.total}
                  </Text>
                </View>
                <View style={{ height: 7, borderRadius: radii.full, backgroundColor: c.surfaceAlt, overflow: 'hidden' }}>
                  <View style={{ width: `${pct}%`, height: '100%', backgroundColor: pillarColor[p], borderRadius: radii.full }} />
                </View>
              </View>
            );
          })}
        </Card>
      </View>

      <View style={{ paddingHorizontal: space.lg, gap: space.sm }}>
        <Txt variant="h3" weight="bold">{t('prog.week')}</Txt>
        <Card style={{ gap: space.md }}>
          <View style={{ flexDirection: row, alignItems: 'flex-end', justifyContent: 'space-between', height: 118 }}>
            {s.last_7_days.map((d) => (
              <View key={d.date} testID={`week-bar-${d.date}`} style={{ alignItems: 'center', gap: 6, flex: 1 }}>
                <Text style={{ fontFamily: f.medium, fontSize: 9.5, color: c.textDim }}>{d.rate}%</Text>
                <View
                  style={{
                    width: 20,
                    height: Math.max(4, (d.rate / maxRate) * 78),
                    borderTopStartRadius: radii.sm,
                    borderTopEndRadius: radii.sm,
                    backgroundColor: d.rate >= 100 ? c.success : d.rate > 0 ? c.secondary : c.surfaceAlt,
                  }}
                />
                <Text style={{ fontFamily: f.regular, fontSize: 9.5, color: c.textDim }}>{weekdayShort(d.date, lang)}</Text>
              </View>
            ))}
          </View>
        </Card>
      </View>
    </ScrollView>
  );
}
