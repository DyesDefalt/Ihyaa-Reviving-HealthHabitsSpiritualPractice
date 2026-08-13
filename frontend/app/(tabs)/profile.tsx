import Feather from '@expo/vector-icons/Feather';
import { router } from 'expo-router';
import React, { useState } from 'react';
import { Platform, Pressable, ScrollView, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { api, errText } from '../../src/api';
import { useAuth } from '../../src/auth';
import { Banner, Btn, Card, Chip, Field, SelectRow, Txt, useFonts } from '../../src/components/ui';
import { LANGS, useI18n } from '../../src/i18n';
import { radii, space, useTheme } from '../../src/theme';

const FITNESS = ['beginner', 'intermediate', 'advanced'];
const SLEEP = ['early_bird', 'moderate', 'night_owl'];
const SPIRITUAL = ['beginner', 'practicing', 'devoted'];
const GOALS = ['weight_loss', 'build_strength', 'better_sleep', 'reduce_stress', 'healthy_eating', 'spiritual_growth', 'mental_clarity', 'more_energy'];
const DIETS = ['no_restriction', 'low_sugar', 'high_protein', 'plant_forward', 'sunnah_diet'];
const TRACKS = ['30_days', '100_days', '1_year'];

export default function Profile() {
  const { c, mode, setMode } = useTheme();
  const { t, lang, setLang, row, align } = useI18n();
  const { user, patchUser, signOut } = useAuth();
  const insets = useSafeAreaInsets();
  const f = useFonts();

  const [editing, setEditing] = useState(false);
  const [name, setName] = useState(user?.name ?? '');
  const [prefs, setPrefs] = useState(user?.prefs);
  const [busy, setBusy] = useState('');
  const [msg, setMsg] = useState<{ text: string; tone: 'ok' | 'error' } | null>(null);

  if (!user || !prefs) return null;

  const toggleArr = (key: 'health_goals' | 'dietary_preferences', v: string) =>
    setPrefs((p) => (p ? { ...p, [key]: p[key].includes(v) ? p[key].filter((x) => x !== v) : [...p[key], v] } : p));

  async function save() {
    setBusy('save');
    setMsg(null);
    try {
      const res = await api('/profile', { method: 'PUT', body: { name: name.trim(), language: lang, theme: mode, prefs } });
      patchUser(res);
      setEditing(false);
      setMsg({ text: t('prof.saved'), tone: 'ok' });
    } catch (e: any) {
      setMsg({ text: errText(e?.detail ?? e?.message), tone: 'error' });
    } finally {
      setBusy('');
    }
  }

  async function replan() {
    setBusy('replan');
    setMsg(null);
    try {
      await api('/challenges/regenerate', { method: 'POST' });
      setMsg({ text: t('prof.replan.ok'), tone: 'ok' });
    } catch (e: any) {
      setMsg({ text: errText(e?.detail ?? e?.message), tone: 'error' });
    } finally {
      setBusy('');
    }
  }

  return (
    <ScrollView
      testID="profile-screen"
      style={{ flex: 1, backgroundColor: c.background }}
      contentContainerStyle={{ paddingTop: insets.top + space.lg, paddingBottom: 120, gap: space.md }}
      showsVerticalScrollIndicator={false}
    >
      <View style={{ paddingHorizontal: space.lg, flexDirection: row, alignItems: 'center', gap: space.md }}>
        <View
          style={{
            width: 58,
            height: 58,
            borderRadius: radii.full,
            backgroundColor: c.primary,
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Text style={{ fontFamily: f.bold, fontSize: 24, color: '#fff' }}>
            {(user.name || user.email)[0]?.toUpperCase()}
          </Text>
        </View>
        <View style={{ flex: 1 }}>
          <Txt variant="h3" weight="bold" testID="profile-name">{user.name || user.email}</Txt>
          <Txt variant="caption" color={c.textDim}>{user.email}</Txt>
          <View style={{ flexDirection: row, alignItems: 'center', gap: 5, marginTop: 4 }}>
            <Feather name={user.is_pro ? 'award' : 'user'} size={11} color={user.is_pro ? c.secondary : c.textDim} />
            <Text testID="plan-label" style={{ fontFamily: f.medium, fontSize: 11, color: user.is_pro ? c.secondary : c.textDim }}>
              {user.is_pro ? t('prof.pro') : t('prof.free')}
            </Text>
          </View>
        </View>
      </View>

      {msg ? (
        <View style={{ paddingHorizontal: space.lg }}>
          <Banner text={msg.text} tone={msg.tone} testID="profile-message" />
        </View>
      ) : null}

      <View style={{ paddingHorizontal: space.lg, gap: space.sm }}>
        <Card style={{ gap: space.md }}>
          <Txt variant="small" weight="semibold" color={c.textDim}>{t('prof.language')}</Txt>
          <View style={{ flexDirection: 'row', gap: space.sm, flexWrap: 'wrap' }}>
            {LANGS.map((l) => (
              <Chip key={l.code} testID={`prof-lang-${l.code}`} label={l.native} active={lang === l.code} onPress={() => setLang(l.code)} />
            ))}
          </View>

          <View style={{ height: 1, backgroundColor: c.border }} />

          <Txt variant="small" weight="semibold" color={c.textDim}>{t('prof.theme')}</Txt>
          <View style={{ flexDirection: 'row', gap: space.sm }}>
            <Chip testID="theme-light" label={t('prof.theme.light')} active={mode === 'light'} onPress={() => setMode('light')} />
            <Chip testID="theme-dark" label={t('prof.theme.dark')} active={mode === 'dark'} onPress={() => setMode('dark')} />
          </View>
        </Card>
      </View>

      <View style={{ paddingHorizontal: space.lg, gap: space.sm }}>
        <View style={{ flexDirection: row, alignItems: 'center', justifyContent: 'space-between' }}>
          <Txt variant="h3" weight="bold">{t('prof.prefs')}</Txt>
          <Pressable
            testID="profile-edit-toggle"
            onPress={() => setEditing((e) => !e)}
            style={Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : undefined}
          >
            <Text style={{ fontFamily: f.medium, fontSize: 13, color: c.primary }}>
              {editing ? t('common.cancel') : t('common.edit')}
            </Text>
          </Pressable>
        </View>

        {editing ? (
          <View style={{ gap: space.md }}>
            <Field label={t('auth.name')} value={name} onChangeText={setName} testID="profile-name-input" />

            <Txt variant="small" weight="semibold" color={c.textDim}>{t('onb.fitness')}</Txt>
            {FITNESS.map((v) => (
              <SelectRow
                key={v}
                testID={`pref-fitness-${v}`}
                title={t(`fitness.${v}`)}
                subtitle={t(`fitness.${v}.d`)}
                selected={prefs.fitness_level === v}
                onPress={() => setPrefs((p) => (p ? { ...p, fitness_level: v } : p))}
              />
            ))}

            <Txt variant="small" weight="semibold" color={c.textDim}>{t('onb.sleep')}</Txt>
            {SLEEP.map((v) => (
              <SelectRow
                key={v}
                testID={`pref-sleep-${v}`}
                title={t(`sleep.${v}`)}
                subtitle={t(`sleep.${v}.d`)}
                selected={prefs.sleep_habit === v}
                onPress={() => setPrefs((p) => (p ? { ...p, sleep_habit: v } : p))}
              />
            ))}

            <Txt variant="small" weight="semibold" color={c.textDim}>{t('onb.spiritual')}</Txt>
            {SPIRITUAL.map((v) => (
              <SelectRow
                key={v}
                testID={`pref-spiritual-${v}`}
                title={t(`spiritual.${v}`)}
                subtitle={t(`spiritual.${v}.d`)}
                selected={prefs.spiritual_level === v}
                onPress={() => setPrefs((p) => (p ? { ...p, spiritual_level: v } : p))}
              />
            ))}

            <Txt variant="small" weight="semibold" color={c.textDim}>{t('onb.goals')}</Txt>
            <View style={{ flexDirection: 'row', gap: space.sm, flexWrap: 'wrap' }}>
              {GOALS.map((v) => (
                <Chip
                  key={v}
                  testID={`pref-goal-${v}`}
                  label={t(`goal.${v}`)}
                  active={prefs.health_goals.includes(v)}
                  onPress={() => toggleArr('health_goals', v)}
                />
              ))}
            </View>

            <Txt variant="small" weight="semibold" color={c.textDim}>{t('onb.diet')}</Txt>
            <View style={{ flexDirection: 'row', gap: space.sm, flexWrap: 'wrap' }}>
              {DIETS.map((v) => (
                <Chip
                  key={v}
                  testID={`pref-diet-${v}`}
                  label={t(`diet.${v}`)}
                  active={prefs.dietary_preferences.includes(v)}
                  onPress={() => toggleArr('dietary_preferences', v)}
                />
              ))}
            </View>

            <Txt variant="small" weight="semibold" color={c.textDim}>{t('onb.challenge')}</Txt>
            <View style={{ flexDirection: 'row', gap: space.sm, flexWrap: 'wrap' }}>
              {TRACKS.map((v) => (
                <Chip
                  key={v}
                  testID={`pref-track-${v}`}
                  label={t(`track.${v}`)}
                  active={prefs.preferred_challenge === v}
                  onPress={() => setPrefs((p) => (p ? { ...p, preferred_challenge: v } : p))}
                  color={v !== '30_days' && !user.is_pro ? c.textDim : undefined}
                />
              ))}
            </View>

            <Btn label={t('common.save')} onPress={save} loading={busy === 'save'} icon="check" testID="profile-save" />
          </View>
        ) : (
          <Card style={{ gap: space.sm }}>
            {[
              [t('onb.fitness'), t(`fitness.${prefs.fitness_level}`)],
              [t('onb.sleep'), t(`sleep.${prefs.sleep_habit}`)],
              [t('onb.spiritual'), t(`spiritual.${prefs.spiritual_level}`)],
              [t('onb.challenge'), t(`track.${prefs.preferred_challenge}`)],
              [t('onb.goals'), prefs.health_goals.map((g) => t(`goal.${g}`)).join(', ') || '—'],
              [t('onb.diet'), prefs.dietary_preferences.map((d) => t(`diet.${d}`)).join(', ') || '—'],
            ].map(([k, v]) => (
              <View key={k} style={{ flexDirection: row, justifyContent: 'space-between', gap: space.md }}>
                <Text style={{ fontFamily: f.regular, fontSize: 13, color: c.textDim }}>{k}</Text>
                <Text style={{ fontFamily: f.medium, fontSize: 13, color: c.text, flex: 1, textAlign: align === 'left' ? 'right' : 'left' }}>
                  {v}
                </Text>
              </View>
            ))}
          </Card>
        )}
      </View>

      <View style={{ paddingHorizontal: space.lg, gap: space.sm }}>
        <Card style={{ gap: space.md }}>
          <View style={{ flexDirection: row, alignItems: 'center', gap: space.md }}>
            <View style={{ width: 40, height: 40, borderRadius: radii.sm, backgroundColor: mode === 'light' ? '#EDF2F0' : c.surfaceAlt, alignItems: 'center', justifyContent: 'center' }}>
              <Feather name="refresh-cw" size={17} color={c.primary} />
            </View>
            <View style={{ flex: 1 }}>
              <Txt variant="body" weight="semibold">{t('prof.replan')}</Txt>
              <Txt variant="caption" color={c.textDim}>{t('prof.replan.d')}</Txt>
            </View>
          </View>
          <Btn label={t('prof.replan')} onPress={replan} loading={busy === 'replan'} variant="outline" icon="refresh-cw" testID="profile-replan" />
        </Card>

        <Pressable testID="profile-knowledge" onPress={() => router.push('/knowledge')} style={Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : undefined}>
          <Card style={{ flexDirection: row, alignItems: 'center', gap: space.md }}>
            <Feather name="book-open" size={18} color={c.primary} />
            <Txt variant="body" weight="medium" style={{ flex: 1 }}>{t('prof.knowledge')}</Txt>
            <Feather name="chevron-right" size={18} color={c.textDim} />
          </Card>
        </Pressable>

        <Pressable testID="profile-coach" onPress={() => router.push('/coach')} style={Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : undefined}>
          <Card style={{ flexDirection: row, alignItems: 'center', gap: space.md }}>
            <Feather name="message-circle" size={18} color={c.primary} />
            <Txt variant="body" weight="medium" style={{ flex: 1 }}>{t('prof.coach')}</Txt>
            <Feather name="chevron-right" size={18} color={c.textDim} />
          </Card>
        </Pressable>

        <Btn
          label={t('prof.signout')}
          variant="ghost"
          icon="log-out"
          testID="sign-out"
          onPress={async () => {
            await signOut();
            router.replace('/sign-in');
          }}
        />
      </View>
    </ScrollView>
  );
}
