import Feather from '@expo/vector-icons/Feather';
import { useFocusEffect } from 'expo-router';
import * as Sharing from 'expo-sharing';
import React, { useCallback, useMemo, useRef, useState } from 'react';
import { Platform, Pressable, ScrollView, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { API, api, getAccessToken } from '../../src/api';
import { Task, TaskCard } from '../../src/components/TaskCard';
import { Banner, Btn, Card, Loader, Txt, useFonts } from '../../src/components/ui';
import { addDays, longDate, parseISO, weekdayShort } from '../../src/dates';
import { useI18n } from '../../src/i18n';
import { notificationsSupported, scheduleReminders } from '../../src/notifications';
import { radii, space, useTheme } from '../../src/theme';

const todayISO = () => new Date().toLocaleDateString('en-CA');

export default function CalendarScreen() {
  const { c, mode } = useTheme();
  const { t, lang, row, align } = useI18n();
  const insets = useSafeAreaInsets();
  const f = useFonts();
  const strip = useRef<ScrollView>(null);

  const [tasks, setTasks] = useState<Task[]>([]);
  const [selected, setSelected] = useState(todayISO());
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState('');
  const [note, setNote] = useState('');

  const from = addDays(todayISO(), -7);
  const to = addDays(todayISO(), 34);

  const load = useCallback(async () => {
    try {
      const list = await api(`/tasks?from=${from}&to=${to}&lang=${lang}`);
      setTasks(list);
    } finally {
      setLoading(false);
    }
  }, [lang, from, to]);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  const byDate = useMemo(() => {
    const map: Record<string, Task[]> = {};
    tasks.forEach((x: any) => {
      const key = x.scheduled_date;
      (map[key] ||= []).push(x);
    });
    return map;
  }, [tasks]);

  const days = useMemo(() => {
    const out: string[] = [];
    for (let i = -7; i <= 34; i += 1) out.push(addDays(todayISO(), i));
    return out;
  }, []);

  async function toggle(task: Task) {
    setTasks((prev) => prev.map((x) => (x.id === task.id ? { ...x, completed: !x.completed } : x)));
    try {
      await api(`/tasks/${task.id}/complete`, { method: 'POST', body: { completed: !task.completed } });
    } catch {
      setTasks((prev) => prev.map((x) => (x.id === task.id ? { ...x, completed: task.completed } : x)));
    }
  }

  async function exportIcs() {
    setBusy('ics');
    setNote('');
    try {
      const token = getAccessToken();
      const res = await fetch(`${API}/tasks/calendar.ics?days=35&lang=${lang}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      });
      const text = await res.text();
      if (Platform.OS === 'web') {
        const blob = new Blob([text], { type: 'text/calendar' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'ihyaa.ics';
        a.click();
        URL.revokeObjectURL(url);
      } else {
        const { File, Paths } = require('expo-file-system');
        const file = new File(Paths.cache, 'ihyaa.ics');
        if (file.exists) file.delete();
        file.create();
        file.write(text);
        await Sharing.shareAsync(file.uri, { mimeType: 'text/calendar', UTI: 'com.apple.ical.ics' });
      }
      setNote(t('cal.exported'));
    } finally {
      setBusy('');
    }
  }

  async function turnOnReminders() {
    setBusy('remind');
    setNote('');
    try {
      if (!notificationsSupported) {
        setNote(t('cal.remind.web'));
        return;
      }
      const upcoming = tasks.filter((x: any) => x.scheduled_date >= todayISO() && x.scheduled_date <= addDays(todayISO(), 7));
      const n = await scheduleReminders(
        upcoming.map((x: any) => ({
          id: x.id,
          title: `Ihyaa · ${x.title}`,
          body: x.description?.slice(0, 110) ?? '',
          date: x.scheduled_date,
          time: x.scheduled_time,
        }))
      );
      setNote(n > 0 ? t('cal.remind.ok') : t('cal.remind.web'));
    } finally {
      setBusy('');
    }
  }

  if (loading) return <Loader testID="calendar-loading" />;

  const dayTasks = byDate[selected] ?? [];

  return (
    <ScrollView
      testID="calendar-screen"
      style={{ flex: 1, backgroundColor: c.background }}
      contentContainerStyle={{ paddingTop: insets.top + space.lg, paddingBottom: 120 }}
      showsVerticalScrollIndicator={false}
    >
      <View style={{ paddingHorizontal: space.lg, gap: 2 }}>
        <Txt variant="h2" weight="bold">{t('cal.title')}</Txt>
        <Txt variant="small" color={c.textDim}>{t('cal.subtitle')}</Txt>
      </View>

      <ScrollView
        ref={strip}
        horizontal
        showsHorizontalScrollIndicator={false}
        onLayout={() => strip.current?.scrollTo({ x: Math.max(0, 7 * 62 - 80), animated: false })}
        contentContainerStyle={{ paddingHorizontal: space.lg, gap: space.sm, paddingVertical: space.lg }}
      >
        {days.map((d) => {
          const list = byDate[d] ?? [];
          const doneCount = list.filter((x) => x.completed).length;
          const state = list.length === 0 ? 'none' : doneCount === list.length ? 'done' : doneCount > 0 ? 'partial' : 'pending';
          const isSel = d === selected;
          const isToday = d === todayISO();
          const dotColor = state === 'done' ? c.success : state === 'partial' ? c.warning : state === 'pending' ? c.border : 'transparent';
          return (
            <Pressable
              key={d}
              testID={`cal-day-${d}`}
              onPress={() => setSelected(d)}
              style={{
                width: 54,
                paddingVertical: 10,
                borderRadius: radii.md,
                alignItems: 'center',
                gap: 4,
                backgroundColor: isSel ? c.primary : c.surface,
                borderWidth: 1.5,
                borderColor: isSel ? c.primary : isToday ? c.secondary : c.border,
                ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}),
              }}
            >
              <Text style={{ fontFamily: f.regular, fontSize: 10, color: isSel ? 'rgba(255,255,255,0.75)' : c.textDim }}>
                {weekdayShort(d, lang)}
              </Text>
              <Text style={{ fontFamily: f.bold, fontSize: 17, color: isSel ? '#fff' : c.text }}>{parseISO(d).getDate()}</Text>
              <View style={{ width: 6, height: 6, borderRadius: 3, backgroundColor: isSel ? '#fff' : dotColor }} />
            </Pressable>
          );
        })}
      </ScrollView>

      <View style={{ paddingHorizontal: space.lg, gap: space.md }}>
        <View style={{ flexDirection: row, gap: space.md, flexWrap: 'wrap' }}>
          {[
            { k: 'done', color: c.success },
            { k: 'partial', color: c.warning },
            { k: 'pending', color: c.border },
          ].map((l) => (
            <View key={l.k} style={{ flexDirection: row, alignItems: 'center', gap: 6 }}>
              <View style={{ width: 7, height: 7, borderRadius: 4, backgroundColor: l.color }} />
              <Text style={{ fontFamily: f.regular, fontSize: 11.5, color: c.textDim }}>{t(`cal.legend.${l.k}`)}</Text>
            </View>
          ))}
        </View>

        <Txt variant="body" weight="semibold">{longDate(selected, lang)}</Txt>

        {dayTasks.length === 0 ? (
          <Card testID="cal-empty"><Txt variant="small" color={c.textDim}>{t('cal.none')}</Txt></Card>
        ) : (
          <View style={{ gap: space.sm }}>
            {dayTasks.map((task) => (
              <TaskCard key={task.id} task={task} onToggle={selected <= todayISO() ? toggle : undefined} readOnly={selected > todayISO()} />
            ))}
          </View>
        )}

        {note ? <Banner text={note} tone="ok" testID="cal-note" /> : null}

        <Card style={{ gap: space.md, marginTop: space.sm }}>
          <View style={{ flexDirection: row, alignItems: 'center', gap: space.md }}>
            <View style={{ width: 40, height: 40, borderRadius: radii.sm, backgroundColor: mode === 'light' ? '#EDF2F0' : c.surfaceAlt, alignItems: 'center', justifyContent: 'center' }}>
              <Feather name="bell" size={18} color={c.primary} />
            </View>
            <View style={{ flex: 1 }}>
              <Txt variant="body" weight="semibold">{t('cal.remind')}</Txt>
              <Txt variant="caption" color={c.textDim}>{t('cal.remind.d')}</Txt>
            </View>
          </View>
          <Btn label={t('cal.remind')} onPress={turnOnReminders} loading={busy === 'remind'} variant="outline" icon="bell" testID="enable-reminders" />

          <View style={{ height: 1, backgroundColor: c.border }} />

          <View style={{ flexDirection: row, alignItems: 'center', gap: space.md }}>
            <View style={{ width: 40, height: 40, borderRadius: radii.sm, backgroundColor: mode === 'light' ? '#F6EDE7' : c.surfaceAlt, alignItems: 'center', justifyContent: 'center' }}>
              <Feather name="calendar" size={18} color={c.secondary} />
            </View>
            <View style={{ flex: 1 }}>
              <Txt variant="body" weight="semibold">{t('cal.export')}</Txt>
              <Txt variant="caption" color={c.textDim}>{t('cal.export.d')}</Txt>
            </View>
          </View>
          <Btn label={t('cal.export')} onPress={exportIcs} loading={busy === 'ics'} variant="accent" icon="download" testID="export-ics" />
        </Card>
      </View>
    </ScrollView>
  );
}
