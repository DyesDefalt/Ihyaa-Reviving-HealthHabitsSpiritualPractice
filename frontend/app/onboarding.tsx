import Feather from '@expo/vector-icons/Feather';
import { LinearGradient } from 'expo-linear-gradient';
import { router } from 'expo-router';
import React, { useState } from 'react';
import { Platform, Pressable, ScrollView, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { api, errText } from '../src/api';
import { useAuth } from '../src/auth';
import { GeoPattern } from '../src/components/GeoPattern';
import { Banner, Btn, Field, SelectRow, Txt, useFonts } from '../src/components/ui';
import { LANGS, useI18n } from '../src/i18n';
import { radii, space, useTheme } from '../src/theme';

const STEPS = ['lang', 'welcome', 'name', 'fitness', 'goals', 'diet', 'sleep', 'spiritual', 'track'] as const;

const FITNESS = ['beginner', 'intermediate', 'advanced'] as const;
const GOALS: { v: string; i: keyof typeof Feather.glyphMap }[] = [
  { v: 'weight_loss', i: 'trending-down' },
  { v: 'build_strength', i: 'award' },
  { v: 'better_sleep', i: 'moon' },
  { v: 'reduce_stress', i: 'wind' },
  { v: 'healthy_eating', i: 'coffee' },
  { v: 'spiritual_growth', i: 'sunrise' },
  { v: 'mental_clarity', i: 'cloud' },
  { v: 'more_energy', i: 'zap' },
];
const DIETS = ['no_restriction', 'low_sugar', 'high_protein', 'plant_forward', 'sunnah_diet'] as const;
const SLEEP: { v: string; i: keyof typeof Feather.glyphMap }[] = [
  { v: 'early_bird', i: 'sunrise' },
  { v: 'moderate', i: 'sun' },
  { v: 'night_owl', i: 'moon' },
];
const SPIRITUAL = ['beginner', 'practicing', 'devoted'] as const;
const TRACKS = [
  { v: '30_days', days: 30, pro: false },
  { v: '100_days', days: 100, pro: true },
  { v: '1_year', days: 365, pro: true },
];

export default function Onboarding() {
  const { c, mode } = useTheme();
  const { t, lang, setLang, row, align } = useI18n();
  const { user, patchUser } = useAuth();
  const insets = useSafeAreaInsets();
  const f = useFonts();

  const [step, setStep] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [name, setName] = useState(user?.name ?? '');
  const [prefs, setPrefs] = useState({
    fitness_level: 'beginner',
    health_goals: [] as string[],
    dietary_preferences: [] as string[],
    sleep_habit: 'moderate',
    spiritual_level: 'beginner',
    preferred_challenge: '30_days',
    reminders_enabled: true,
  });

  const id = STEPS[step];
  const isLast = step === STEPS.length - 1;

  const toggle = (key: 'health_goals' | 'dietary_preferences', v: string) =>
    setPrefs((p) => ({
      ...p,
      [key]: p[key].includes(v) ? p[key].filter((x) => x !== v) : [...p[key], v],
    }));

  const canNext = id !== 'goals' || prefs.health_goals.length > 0;

  async function finish() {
    setBusy(true);
    setError('');
    try {
      const res = await api('/onboarding', {
        method: 'POST',
        body: { name: name.trim(), language: lang, prefs, start_challenge: true },
      });
      patchUser(res.user);
      router.replace('/(tabs)');
    } catch (e: any) {
      setError(errText(e?.detail ?? e?.message));
    } finally {
      setBusy(false);
    }
  }

  const titles: Record<string, [string, string]> = {
    lang: [t('onb.lang'), t('onb.lang.sub')],
    welcome: [t('onb.welcome'), t('onb.welcome.sub')],
    name: [t('onb.name'), t('onb.name.sub')],
    fitness: [t('onb.fitness'), t('onb.fitness.sub')],
    goals: [t('onb.goals'), t('onb.goals.sub')],
    diet: [t('onb.diet'), t('onb.diet.sub')],
    sleep: [t('onb.sleep'), t('onb.sleep.sub')],
    spiritual: [t('onb.spiritual'), t('onb.spiritual.sub')],
    track: [t('onb.challenge'), t('onb.challenge.sub')],
  };

  return (
    <View style={{ flex: 1, backgroundColor: c.background }}>
      <View style={{ paddingTop: insets.top + space.md, paddingHorizontal: space.lg, paddingBottom: space.sm }}>
        <View style={{ flexDirection: row, gap: 5 }}>
          {STEPS.map((_, i) => (
            <View
              key={i}
              style={{
                flex: 1,
                height: 4,
                borderRadius: radii.full,
                backgroundColor: i <= step ? c.primary : c.border,
              }}
            />
          ))}
        </View>
        <Txt variant="h2" weight="bold" style={{ marginTop: space.lg }} testID="onb-title">
          {titles[id][0]}
        </Txt>
        <Txt variant="small" color={c.textDim}>
          {titles[id][1]}
        </Txt>
      </View>

      <ScrollView
        contentContainerStyle={{ padding: space.lg, gap: space.sm, paddingBottom: 140 }}
        showsVerticalScrollIndicator={false}
      >
        {id === 'lang'
          ? LANGS.map((l) => (
              <SelectRow
                key={l.code}
                testID={`onb-lang-${l.code}`}
                title={l.native}
                subtitle={l.label}
                selected={lang === l.code}
                onPress={() => setLang(l.code)}
                emblem="globe"
              />
            ))
          : null}

        {id === 'welcome' ? (
          <View style={{ gap: space.lg }}>
            <LinearGradient
              colors={['#1B3B36', '#24534A']}
              style={{ borderRadius: radii.lg, padding: space.lg, overflow: 'hidden' }}
            >
              <GeoPattern color="#FFFFFF" opacity={0.11} size={52} />
              <Text style={{ fontFamily: 'Amiri_700Bold', fontSize: 40, color: '#fff', textAlign: align }}>إحياء</Text>
              <Text style={{ fontFamily: f.bold, fontSize: 20, color: '#fff', marginTop: space.sm, textAlign: align }}>
                {t('onb.welcome.title')}
              </Text>
              <Text style={{ fontFamily: f.regular, fontSize: 14, color: 'rgba(255,255,255,0.75)', marginTop: 6, textAlign: align, lineHeight: 21 }}>
                {t('onb.welcome.desc')}
              </Text>
            </LinearGradient>

            <View style={{ gap: space.md }}>
              <Txt variant="small" weight="semibold" color={c.textDim}>
                {t('onb.expect')}
              </Txt>
              {[1, 2, 3, 4].map((n) => (
                <View key={n} style={{ flexDirection: row, alignItems: 'center', gap: space.md }}>
                  <View
                    style={{
                      width: 28,
                      height: 28,
                      borderRadius: radii.full,
                      backgroundColor: mode === 'light' ? '#EDF2F0' : c.surfaceAlt,
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    <Feather name="check" size={14} color={c.primary} />
                  </View>
                  <Txt variant="body" style={{ flex: 1 }}>
                    {t(`onb.expect.${n}`)}
                  </Txt>
                </View>
              ))}
            </View>
          </View>
        ) : null}

        {id === 'name' ? (
          <Field label={t('auth.name')} value={name} onChangeText={setName} placeholder={t('auth.name.ph')} testID="onb-name" />
        ) : null}

        {id === 'fitness'
          ? FITNESS.map((v) => (
              <SelectRow
                key={v}
                testID={`onb-fitness-${v}`}
                title={t(`fitness.${v}`)}
                subtitle={t(`fitness.${v}.d`)}
                selected={prefs.fitness_level === v}
                onPress={() => setPrefs((p) => ({ ...p, fitness_level: v }))}
                emblem="activity"
              />
            ))
          : null}

        {id === 'goals' ? (
          <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: space.sm }}>
            {GOALS.map(({ v, i }) => {
              const on = prefs.health_goals.includes(v);
              return (
                <Pressable
                  key={v}
                  testID={`onb-goal-${v}`}
                  onPress={() => toggle('health_goals', v)}
                  style={{
                    width: '48%',
                    padding: space.md,
                    borderRadius: radii.md,
                    borderWidth: 1.5,
                    borderColor: on ? c.primary : c.border,
                    backgroundColor: on ? (mode === 'light' ? '#EDF2F0' : c.surfaceAlt) : c.surface,
                    gap: space.sm,
                    ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}),
                  }}
                >
                  <Feather name={i} size={20} color={on ? c.primary : c.textDim} />
                  <Text style={{ fontFamily: f.semibold, fontSize: 14, color: on ? c.primary : c.text, textAlign: align }}>
                    {t(`goal.${v}`)}
                  </Text>
                </Pressable>
              );
            })}
            <Txt variant="caption" color={c.textDim} style={{ width: '100%', textAlign: 'center', marginTop: 4 }}>
              {t('onb.goals.hint')}
            </Txt>
          </View>
        ) : null}

        {id === 'diet'
          ? DIETS.map((v) => (
              <SelectRow
                key={v}
                testID={`onb-diet-${v}`}
                title={t(`diet.${v}`)}
                subtitle={t(`diet.${v}.d`)}
                selected={prefs.dietary_preferences.includes(v)}
                onPress={() => toggle('dietary_preferences', v)}
                emblem="coffee"
              />
            ))
          : null}

        {id === 'sleep'
          ? SLEEP.map(({ v, i }) => (
              <SelectRow
                key={v}
                testID={`onb-sleep-${v}`}
                title={t(`sleep.${v}`)}
                subtitle={t(`sleep.${v}.d`)}
                selected={prefs.sleep_habit === v}
                onPress={() => setPrefs((p) => ({ ...p, sleep_habit: v }))}
                emblem={i}
              />
            ))
          : null}

        {id === 'spiritual'
          ? SPIRITUAL.map((v) => (
              <SelectRow
                key={v}
                testID={`onb-spiritual-${v}`}
                title={t(`spiritual.${v}`)}
                subtitle={t(`spiritual.${v}.d`)}
                selected={prefs.spiritual_level === v}
                onPress={() => setPrefs((p) => ({ ...p, spiritual_level: v }))}
                emblem="moon"
              />
            ))
          : null}

        {id === 'track'
          ? TRACKS.map((tr) => {
              const locked = tr.pro && !user?.is_pro;
              const on = prefs.preferred_challenge === tr.v;
              return (
                <Pressable
                  key={tr.v}
                  testID={`onb-track-${tr.v}`}
                  disabled={locked}
                  onPress={() => setPrefs((p) => ({ ...p, preferred_challenge: tr.v }))}
                  style={{
                    borderRadius: radii.md,
                    borderWidth: 1.5,
                    borderColor: on ? c.primary : c.border,
                    overflow: 'hidden',
                    opacity: locked ? 0.55 : 1,
                    ...(Platform.OS === 'web' ? ({ cursor: locked ? 'default' : 'pointer' } as any) : {}),
                  }}
                >
                  <LinearGradient
                    colors={on ? ['#1B3B36', '#24534A'] : [c.surfaceAlt, c.surfaceAlt]}
                    style={{ padding: space.md, flexDirection: row, alignItems: 'center', gap: space.md }}
                  >
                    {on ? <GeoPattern color="#FFFFFF" opacity={0.1} size={44} /> : null}
                    <View style={{ flex: 1 }}>
                      <Text style={{ fontFamily: f.bold, fontSize: 19, color: on ? '#fff' : c.text, textAlign: align }}>
                        {t(`track.${tr.v}`)}
                      </Text>
                      <Text
                        style={{
                          fontFamily: f.regular,
                          fontSize: 13,
                          color: on ? 'rgba(255,255,255,0.75)' : c.textDim,
                          textAlign: align,
                        }}
                      >
                        {t(`track.${tr.v}.d`)}
                      </Text>
                    </View>
                    {locked ? (
                      <View style={{ alignItems: 'center', gap: 2 }}>
                        <Feather name="lock" size={16} color={c.textDim} />
                        <Text style={{ fontFamily: f.medium, fontSize: 9, color: c.textDim }}>{t('track.pro')}</Text>
                      </View>
                    ) : (
                      <Text style={{ fontFamily: f.bold, fontSize: 22, color: on ? '#B5653E' : c.textDim }}>{tr.days}</Text>
                    )}
                  </LinearGradient>
                </Pressable>
              );
            })
          : null}

        {id === 'track' && !user?.is_pro ? (
          <Txt variant="caption" color={c.textDim} style={{ marginTop: space.sm }}>
            {t('onb.pro_locked')}
          </Txt>
        ) : null}

        {error ? <Banner text={error} testID="onb-error" /> : null}
      </ScrollView>

      <View
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          bottom: 0,
          paddingHorizontal: space.lg,
          paddingTop: space.md,
          paddingBottom: insets.bottom + space.md,
          backgroundColor: c.background,
          borderTopWidth: 1,
          borderTopColor: c.border,
          flexDirection: row,
          gap: space.sm,
        }}
      >
        {step > 0 ? (
          <Btn label={t('common.back')} onPress={() => setStep((s) => s - 1)} variant="outline" testID="onb-back" />
        ) : null}
        <Btn
          style={{ flex: 1 }}
          label={isLast ? t('onb.start') : t('common.next')}
          icon={isLast ? 'sunrise' : 'arrow-right'}
          onPress={isLast ? finish : () => setStep((s) => s + 1)}
          disabled={!canNext}
          loading={busy}
          testID="onb-next"
        />
      </View>
    </View>
  );
}
