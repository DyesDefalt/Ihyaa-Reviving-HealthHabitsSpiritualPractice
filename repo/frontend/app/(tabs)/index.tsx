import Feather from '@expo/vector-icons/Feather';
import { LinearGradient } from 'expo-linear-gradient';
import { router, useFocusEffect } from 'expo-router';
import React, { useCallback, useState } from 'react';
import { Platform, Pressable, RefreshControl, ScrollView, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { api } from '../../src/api';
import { useAuth } from '../../src/auth';
import { GeoPattern } from '../../src/components/GeoPattern';
import { ProgressRings } from '../../src/components/ProgressRings';
import { Task, TaskCard } from '../../src/components/TaskCard';
import { Banner, Btn, Card, Loader, Txt, useFonts } from '../../src/components/ui';
import { longDate } from '../../src/dates';
import { useI18n } from '../../src/i18n';
import { pillarColor, radii, space, useTheme } from '../../src/theme';

type Challenge = { id: string; challenge_type: string; current_day: number; total_days: number };

export default function Today() {
  const { c, mode } = useTheme();
  const { t, lang, row, align } = useI18n();
  const { user, patchUser } = useAuth();
  const insets = useSafeAreaInsets();
  const f = useFonts();

  const [challenge, setChallenge] = useState<Challenge | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [card, setCard] = useState<any>(null);
  const [checkedIn, setCheckedIn] = useState(false);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [busy, setBusy] = useState(false);
  const [toast, setToast] = useState('');

  const load = useCallback(async () => {
    try {
      const [today, know, checkin] = await Promise.all([
        api(`/tasks/today?lang=${lang}`),
        api(`/knowledge?lang=${lang}`),
        api('/checkins/today'),
      ]);
      setChallenge(today.challenge);
      setTasks(today.tasks);
      setCheckedIn(!!checkin);
      if (know?.length) setCard(know[new Date().getDate() % know.length]);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [lang]);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  async function startTrack() {
    setBusy(true);
    try {
      await api('/challenges', { method: 'POST', body: { challenge_type: user?.prefs.preferred_challenge ?? '30_days' } });
      await load();
    } finally {
      setBusy(false);
    }
  }

  async function toggle(task: Task) {
    setTasks((prev) => prev.map((x) => (x.id === task.id ? { ...x, completed: !x.completed } : x)));
    try {
      const res = await api(`/tasks/${task.id}/complete`, { method: 'POST', body: { completed: !task.completed } });
      patchUser(res.user);
      if (res.bonus > 0) setToast(`+${res.bonus} ${t('common.points')} — ${t('home.alldone')}`);
    } catch {
      setTasks((prev) => prev.map((x) => (x.id === task.id ? { ...x, completed: task.completed } : x)));
    }
  }

  if (loading) return <Loader testID="today-loading" />;

  const done = tasks.filter((x) => x.completed).length;
  const pillarPct = ['spiritual', 'physical', 'nutrition', 'mental']
    .map((p) => {
      const list = tasks.filter((x) => x.pillar === p);
      return { total: list.length, pct: list.length ? (list.filter((x) => x.completed).length / list.length) * 100 : 0, color: pillarColor[p] };
    })
    .filter((r) => r.total > 0);

  return (
    <ScrollView
      testID="today-screen"
      style={{ flex: 1, backgroundColor: c.background }}
      contentContainerStyle={{ paddingBottom: 120 }}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={() => { setRefreshing(true); load(); }} tintColor={c.primary} />}
      showsVerticalScrollIndicator={false}
    >
      <LinearGradient
        colors={mode === 'light' ? ['#1B3B36', '#24534A'] : ['#16302C', '#1E463F']}
        style={{
          paddingTop: insets.top + space.lg,
          paddingBottom: space.xl,
          paddingHorizontal: space.lg,
          borderBottomStartRadius: 30,
          borderBottomEndRadius: 30,
          overflow: 'hidden',
        }}
      >
        <GeoPattern color="#FFFFFF" opacity={0.1} size={54} />

        <View style={{ flexDirection: row, alignItems: 'center', justifyContent: 'space-between' }}>
          <View style={{ flex: 1 }}>
            <Text style={{ fontFamily: f.regular, fontSize: 13, color: 'rgba(255,255,255,0.7)', textAlign: align }}>
              {t('home.greeting')}
            </Text>
            <Text testID="today-username" style={{ fontFamily: f.bold, fontSize: 22, color: '#fff', textAlign: align }}>
              {user?.name || 'Ihyaa'}
            </Text>
          </View>
          <View style={{ flexDirection: row, gap: space.sm }}>
            <View style={{ flexDirection: row, alignItems: 'center', gap: 5, backgroundColor: 'rgba(255,255,255,0.14)', paddingHorizontal: 11, paddingVertical: 7, borderRadius: radii.full }}>
              <Feather name="zap" size={13} color="#E9C46A" />
              <Text testID="header-streak" style={{ fontFamily: f.semibold, fontSize: 13, color: '#fff' }}>{user?.current_streak ?? 0}</Text>
            </View>
            <View style={{ flexDirection: row, alignItems: 'center', gap: 5, backgroundColor: 'rgba(255,255,255,0.14)', paddingHorizontal: 11, paddingVertical: 7, borderRadius: radii.full }}>
              <Feather name="star" size={13} color="#E9C46A" />
              <Text testID="header-points" style={{ fontFamily: f.semibold, fontSize: 13, color: '#fff' }}>{user?.points_balance ?? 0}</Text>
            </View>
          </View>
        </View>

        {challenge ? (
          <View style={{ flexDirection: row, alignItems: 'center', gap: space.lg, marginTop: space.lg }}>
            <ProgressRings rings={pillarPct} size={112} stroke={9} gap={4}>
              <View style={{ alignItems: 'center' }}>
                <Text style={{ fontFamily: f.bold, fontSize: 26, color: '#fff' }}>{done}</Text>
                <Text style={{ fontFamily: f.regular, fontSize: 11, color: 'rgba(255,255,255,0.6)' }}>/ {tasks.length}</Text>
              </View>
            </ProgressRings>
            <View style={{ flex: 1, gap: 4 }}>
              <Text style={{ fontFamily: f.medium, fontSize: 12, color: '#B5653E', letterSpacing: 1, textAlign: align }}>
                {t('common.day').toUpperCase()} {challenge.current_day} {t('common.of').toUpperCase()} {challenge.total_days}
              </Text>
              <Text style={{ fontFamily: f.semibold, fontSize: 16, color: '#fff', textAlign: align }}>
                {longDate(new Date().toLocaleDateString('en-CA'), lang)}
              </Text>
              <View style={{ height: 5, borderRadius: radii.full, backgroundColor: 'rgba(255,255,255,0.18)', marginTop: 6, overflow: 'hidden' }}>
                <View
                  style={{
                    width: `${(challenge.current_day / challenge.total_days) * 100}%`,
                    height: '100%',
                    backgroundColor: '#B5653E',
                    borderRadius: radii.full,
                  }}
                />
              </View>
            </View>
          </View>
        ) : null}
      </LinearGradient>

      <View style={{ padding: space.lg, gap: space.md }}>
        {toast ? <Banner text={toast} tone="ok" testID="today-toast" /> : null}

        {!challenge ? (
          <Card testID="no-challenge-card" style={{ gap: space.md, alignItems: 'center', paddingVertical: space.xl }}>
            <View style={{ width: 56, height: 56, borderRadius: radii.full, backgroundColor: mode === 'light' ? '#EDF2F0' : c.surfaceAlt, alignItems: 'center', justifyContent: 'center' }}>
              <Feather name="sunrise" size={26} color={c.primary} />
            </View>
            <Txt variant="h3" weight="bold" style={{ textAlign: 'center' }}>{t('home.ready')}</Txt>
            <Txt variant="small" color={c.textDim} style={{ textAlign: 'center' }}>{t('home.ready.d')}</Txt>
            <Btn label={t('home.start')} onPress={startTrack} loading={busy} icon="play" style={{ alignSelf: 'stretch' }} testID="start-challenge" />
          </Card>
        ) : (
          <>
            <View style={{ flexDirection: row, alignItems: 'center', justifyContent: 'space-between' }}>
              <Txt variant="h3" weight="bold">{t('home.today')}</Txt>
              {tasks.length > 0 && done === tasks.length ? (
                <View style={{ flexDirection: row, alignItems: 'center', gap: 5 }}>
                  <Feather name="award" size={15} color={c.success} />
                  <Text style={{ fontFamily: f.medium, fontSize: 12, color: c.success }}>{t('home.alldone')}</Text>
                </View>
              ) : null}
            </View>

            {tasks.length === 0 ? (
              <Card><Txt variant="small" color={c.textDim}>{t('home.none')}</Txt></Card>
            ) : (
              <View style={{ gap: space.sm }}>
                {tasks.map((task) => (
                  <TaskCard key={task.id} task={task} onToggle={toggle} />
                ))}
              </View>
            )}

            <Pressable
              testID="checkin-cta"
              onPress={() => router.push('/checkin')}
              style={({ pressed }) => ({ opacity: pressed ? 0.9 : 1, ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}) })}
            >
              <LinearGradient
                colors={checkedIn ? ['#2A9D8F', '#20857A'] : ['#B5653E', '#9C5233']}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={{ borderRadius: radii.md, padding: space.md, flexDirection: row, alignItems: 'center', gap: space.md, overflow: 'hidden' }}
              >
                <GeoPattern color="#FFFFFF" opacity={0.12} size={40} />
                <View style={{ width: 42, height: 42, borderRadius: radii.sm, backgroundColor: 'rgba(255,255,255,0.2)', alignItems: 'center', justifyContent: 'center' }}>
                  <Feather name={checkedIn ? 'check-circle' : 'edit-3'} size={20} color="#fff" />
                </View>
                <View style={{ flex: 1 }}>
                  <Text style={{ fontFamily: f.bold, fontSize: 15, color: '#fff', textAlign: align }}>{t('home.checkin')}</Text>
                  <Text style={{ fontFamily: f.regular, fontSize: 12, color: 'rgba(255,255,255,0.8)', textAlign: align }}>
                    {checkedIn ? t('home.checkin.done') : t('home.checkin.d')}
                  </Text>
                </View>
                <Feather name="chevron-right" size={18} color="rgba(255,255,255,0.8)" />
              </LinearGradient>
            </Pressable>
          </>
        )}

        <Pressable
          testID="coach-cta"
          onPress={() => router.push('/coach')}
          style={({ pressed }) => ({ opacity: pressed ? 0.9 : 1, ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}) })}
        >
          <Card style={{ flexDirection: row, alignItems: 'center', gap: space.md }}>
            <View style={{ width: 42, height: 42, borderRadius: radii.sm, backgroundColor: mode === 'light' ? '#EDF2F0' : c.surfaceAlt, alignItems: 'center', justifyContent: 'center' }}>
              <Feather name="message-circle" size={20} color={c.primary} />
            </View>
            <View style={{ flex: 1 }}>
              <Txt variant="body" weight="semibold">{t('home.coach')}</Txt>
              <Txt variant="caption" color={c.textDim}>{t('home.coach.d')}</Txt>
            </View>
            <Feather name="chevron-right" size={18} color={c.textDim} />
          </Card>
        </Pressable>

        {card ? (
          <>
            <View style={{ flexDirection: row, alignItems: 'center', justifyContent: 'space-between', marginTop: space.sm }}>
              <Txt variant="h3" weight="bold">{t('home.wisdom')}</Txt>
              <Pressable testID="knowledge-link" onPress={() => router.push('/knowledge')} style={Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : undefined}>
                <Text style={{ fontFamily: f.medium, fontSize: 13, color: c.primary }}>{t('home.seeall')}</Text>
              </Pressable>
            </View>
            <Pressable testID="knowledge-card" onPress={() => router.push('/knowledge')} style={Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : undefined}>
              <LinearGradient
                colors={['#24534A', '#1B3B36']}
                style={{ borderRadius: radii.md, padding: space.lg, overflow: 'hidden', gap: space.sm }}
              >
                <GeoPattern color="#FFFFFF" opacity={0.09} size={48} />
                <Text style={{ fontFamily: f.medium, fontSize: 10.5, letterSpacing: 1, color: '#B5653E', textTransform: 'uppercase', textAlign: align }}>
                  {card.category}
                </Text>
                <Text style={{ fontFamily: f.bold, fontSize: 18, color: '#fff', textAlign: align }}>{card.title}</Text>
                {card.quran_verse ? (
                  <Text style={{ fontFamily: 'Amiri_400Regular', fontSize: 16, lineHeight: 28, color: 'rgba(255,255,255,0.85)', textAlign: align }}>
                    {card.quran_verse}
                  </Text>
                ) : null}
                <Text numberOfLines={3} style={{ fontFamily: f.regular, fontSize: 13.5, lineHeight: 21, color: 'rgba(255,255,255,0.75)', textAlign: align }}>
                  {card.content}
                </Text>
              </LinearGradient>
            </Pressable>
          </>
        ) : null}
      </View>
    </ScrollView>
  );
}
