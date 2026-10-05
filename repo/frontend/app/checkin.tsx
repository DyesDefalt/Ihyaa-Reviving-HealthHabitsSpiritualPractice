import Feather from '@expo/vector-icons/Feather';
import { LinearGradient } from 'expo-linear-gradient';
import { router } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { Platform, Pressable, ScrollView, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { api, errText } from '../src/api';
import { useAuth } from '../src/auth';
import { GeoPattern } from '../src/components/GeoPattern';
import { Banner, Btn, Card, Field, Loader, Txt, useFonts } from '../src/components/ui';
import { useI18n } from '../src/i18n';
import { radii, space, useTheme } from '../src/theme';

function Scale({
  value,
  onChange,
  labelKey,
  testPrefix,
}: {
  value: number;
  onChange: (n: number) => void;
  labelKey: string;
  testPrefix: string;
}) {
  const { c } = useTheme();
  const { t, row } = useI18n();
  const f = useFonts();
  return (
    <View style={{ flexDirection: row, gap: space.sm }}>
      {[1, 2, 3, 4, 5].map((n) => {
        const on = value === n;
        return (
          <Pressable
            key={n}
            testID={`${testPrefix}-${n}`}
            onPress={() => onChange(n)}
            style={{
              flex: 1,
              paddingVertical: 12,
              borderRadius: radii.md,
              borderWidth: 1.5,
              borderColor: on ? c.primary : c.border,
              backgroundColor: on ? c.primary : c.surface,
              alignItems: 'center',
              gap: 3,
              ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}),
            }}
          >
            <Text style={{ fontFamily: f.bold, fontSize: 17, color: on ? '#fff' : c.text }}>{n}</Text>
            <Text
              numberOfLines={1}
              style={{ fontFamily: f.regular, fontSize: 8.5, color: on ? 'rgba(255,255,255,0.85)' : c.textDim }}
            >
              {t(`${labelKey}.${n}`)}
            </Text>
          </Pressable>
        );
      })}
    </View>
  );
}

export default function Checkin() {
  const { c, mode } = useTheme();
  const { t, row } = useI18n();
  const { patchUser } = useAuth();
  const insets = useSafeAreaInsets();
  const f = useFonts();

  const [existing, setExisting] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [mood, setMood] = useState(3);
  const [energy, setEnergy] = useState(3);
  const [gratitude, setGratitude] = useState('');
  const [reflection, setReflection] = useState('');
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api('/checkins/today')
      .then(setExisting)
      .catch(() => undefined)
      .finally(() => setLoading(false));
  }, []);

  async function submit() {
    setBusy(true);
    setError('');
    try {
      const res = await api('/checkins', {
        method: 'POST',
        body: { mood_rating: mood, energy_rating: energy, gratitude_note: gratitude, reflection_note: reflection },
      });
      patchUser(res.user);
      setResult(res);
    } catch (e: any) {
      setError(errText(e?.detail ?? e?.message));
    } finally {
      setBusy(false);
    }
  }

  if (loading) return <Loader testID="checkin-loading" />;

  const finished = result || existing;

  return (
    <ScrollView
      testID="checkin-screen"
      style={{ flex: 1, backgroundColor: c.background }}
      contentContainerStyle={{ paddingTop: insets.top + space.md, paddingBottom: insets.bottom + space.xxl, gap: space.md }}
      showsVerticalScrollIndicator={false}
    >
      <View style={{ paddingHorizontal: space.lg, flexDirection: row, alignItems: 'center', gap: space.md }}>
        <Pressable
          testID="checkin-back"
          onPress={() => router.back()}
          style={{
            width: 38,
            height: 38,
            borderRadius: radii.full,
            backgroundColor: c.surface,
            borderWidth: 1,
            borderColor: c.border,
            alignItems: 'center',
            justifyContent: 'center',
            ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}),
          }}
        >
          <Feather name="arrow-left" size={18} color={c.text} />
        </Pressable>
        <Txt variant="h3" weight="bold" style={{ flex: 1 }}>{t('check.title')}</Txt>
      </View>

      {finished ? (
        <View style={{ paddingHorizontal: space.lg, gap: space.md }}>
          <LinearGradient
            colors={['#2A9D8F', '#1B3B36']}
            style={{ borderRadius: radii.lg, padding: space.xl, alignItems: 'center', gap: space.sm, overflow: 'hidden' }}
          >
            <GeoPattern color="#FFFFFF" opacity={0.12} size={44} />
            <View style={{ width: 62, height: 62, borderRadius: radii.full, backgroundColor: 'rgba(255,255,255,0.2)', alignItems: 'center', justifyContent: 'center' }}>
              <Feather name="check" size={30} color="#fff" />
            </View>
            <Text style={{ fontFamily: f.bold, fontSize: 20, color: '#fff', textAlign: 'center' }}>
              {result ? t('check.done') : t('check.already')}
            </Text>
            <Text style={{ fontFamily: f.regular, fontSize: 13.5, color: 'rgba(255,255,255,0.8)', textAlign: 'center' }}>
              {result ? t('check.done.d') : t('check.already.d')}
            </Text>
            {result ? (
              <View style={{ marginTop: space.md, alignItems: 'center' }}>
                <Text testID="checkin-points" style={{ fontFamily: f.bold, fontSize: 38, color: '#E9C46A' }}>
                  +{result.points_earned}
                </Text>
                <Text style={{ fontFamily: f.regular, fontSize: 12, color: 'rgba(255,255,255,0.75)' }}>{t('check.earned')}</Text>
              </View>
            ) : null}
          </LinearGradient>
          <Btn label={t('common.done')} onPress={() => router.replace('/(tabs)')} icon="home" testID="checkin-home" />
        </View>
      ) : (
        <View style={{ paddingHorizontal: space.lg, gap: space.lg }}>
          <View style={{ gap: space.sm }}>
            <Txt variant="body" weight="semibold">{t('check.mood')}</Txt>
            <Scale value={mood} onChange={setMood} labelKey="check.mood" testPrefix="mood" />
          </View>

          <View style={{ gap: space.sm }}>
            <Txt variant="body" weight="semibold">{t('check.energy')}</Txt>
            <Scale value={energy} onChange={setEnergy} labelKey="check.energy" testPrefix="energy" />
          </View>

          <Card style={{ gap: space.sm, backgroundColor: mode === 'light' ? '#EDF2F0' : c.surfaceAlt }}>
            <Txt variant="body" weight="semibold">{t('check.gratitude')}</Txt>
            <Txt variant="caption" color={c.textDim} style={{ fontStyle: 'italic' }}>{t('check.gratitude.q')}</Txt>
          </Card>
          <Field
            label={t('check.gratitude')}
            value={gratitude}
            onChangeText={setGratitude}
            placeholder={t('check.gratitude.ph')}
            multiline
            testID="gratitude-input"
          />

          <Field
            label={t('check.reflect')}
            value={reflection}
            onChangeText={setReflection}
            placeholder={t('check.reflect.ph')}
            multiline
            testID="reflection-input"
          />

          {error ? <Banner text={error} testID="checkin-error" /> : null}

          <Btn label={t('check.submit')} onPress={submit} loading={busy} icon="check-circle" testID="checkin-submit" />
        </View>
      )}
    </ScrollView>
  );
}
