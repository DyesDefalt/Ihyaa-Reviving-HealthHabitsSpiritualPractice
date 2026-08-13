import Feather from '@expo/vector-icons/Feather';
import { LinearGradient } from 'expo-linear-gradient';
import { router } from 'expo-router';
import * as WebBrowser from 'expo-web-browser';
import * as Linking from 'expo-linking';
import React, { useState } from 'react';
import { KeyboardAvoidingView, Platform, Pressable, ScrollView, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { errText } from '../src/api';
import { useAuth } from '../src/auth';
import { GeoPattern } from '../src/components/GeoPattern';
import { Banner, Btn, Field, Txt, useFonts } from '../src/components/ui';
import { LANGS, useI18n } from '../src/i18n';
import { radii, space, useTheme } from '../src/theme';

export default function SignIn() {
  const { c } = useTheme();
  const { t, lang, setLang, row, align } = useI18n();
  const { signIn, signUp, signInGoogle } = useAuth();
  const insets = useSafeAreaInsets();
  const f = useFonts();

  const [mode, setMode] = useState<'in' | 'up'>('in');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  async function submit() {
    setError('');
    setBusy(true);
    try {
      if (mode === 'up') await signUp(email.trim(), password, name.trim(), lang);
      else await signIn(email.trim(), password);
      router.replace('/');
    } catch (e: any) {
      setError(errText(e?.detail ?? e?.message));
    } finally {
      setBusy(false);
    }
  }

  async function google() {
    setError('');
    try {
      // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
      if (Platform.OS === 'web') {
        const redirectUrl = window.location.origin + '/';
        window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
        return;
      }
      const redirectUrl = Linking.createURL('/');
      const result = await WebBrowser.openAuthSessionAsync(
        `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`,
        redirectUrl
      );
      if (result.type === 'success' && result.url.includes('session_id=')) {
        const sessionId = result.url.split('session_id=')[1].split(/[&#]/)[0];
        await signInGoogle(sessionId);
        router.replace('/');
      }
    } catch (e: any) {
      setError(errText(e?.detail ?? e?.message));
    }
  }

  const pills = [t('auth.pill1'), t('auth.pill2'), t('auth.pill3')];

  return (
    <View style={{ flex: 1, backgroundColor: c.background }}>
      <LinearGradient
        colors={['#1B3B36', '#24534A']}
        style={{ paddingTop: insets.top + space.xl, paddingBottom: space.xxl, paddingHorizontal: space.lg }}
      >
        <GeoPattern color="#FFFFFF" opacity={0.1} size={58} />
        <View style={{ flexDirection: row, justifyContent: 'flex-end', gap: space.sm, marginBottom: space.lg }}>
          {LANGS.map((l) => (
            <Pressable
              key={l.code}
              testID={`lang-${l.code}`}
              onPress={() => setLang(l.code)}
              style={{
                paddingHorizontal: 12,
                paddingVertical: 6,
                borderRadius: radii.full,
                backgroundColor: lang === l.code ? 'rgba(255,255,255,0.22)' : 'rgba(255,255,255,0.07)',
                borderWidth: 1,
                borderColor: lang === l.code ? 'rgba(255,255,255,0.5)' : 'transparent',
                ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}),
              }}
            >
              <Text style={{ fontFamily: f.medium, fontSize: 12, color: '#fff' }}>
                {l.code === 'ar' ? 'ع' : l.code.toUpperCase()}
              </Text>
            </Pressable>
          ))}
        </View>

        <Text style={{ fontFamily: 'Amiri_700Bold', fontSize: 54, color: '#FFFFFF', lineHeight: 66, textAlign: align }}>إحياء</Text>
        <Text style={{ fontFamily: f.bold, fontSize: 26, color: '#FFFFFF', marginTop: -4, textAlign: align }}>Ihyaa</Text>
        <Text style={{ fontFamily: f.regular, fontSize: 15, color: 'rgba(255,255,255,0.72)', marginTop: space.sm, maxWidth: 320, textAlign: align }}>
          {t('auth.subtitle')}
        </Text>

        <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: space.sm, marginTop: space.lg }}>
          {pills.map((p) => (
            <View
              key={p}
              style={{
                flexDirection: row,
                alignItems: 'center',
                gap: 6,
                backgroundColor: 'rgba(255,255,255,0.1)',
                paddingHorizontal: 11,
                paddingVertical: 6,
                borderRadius: radii.full,
              }}
            >
              <Feather name="check" size={12} color="#B5653E" />
              <Text style={{ fontFamily: f.medium, fontSize: 11.5, color: 'rgba(255,255,255,0.9)' }}>{p}</Text>
            </View>
          ))}
        </View>
      </LinearGradient>

      <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={{ flex: 1 }}>
        <ScrollView
          contentContainerStyle={{ padding: space.lg, gap: space.md, paddingBottom: insets.bottom + space.xl }}
          keyboardShouldPersistTaps="handled"
        >
          <Txt variant="h3" weight="bold" testID="auth-heading">
            {mode === 'in' ? t('auth.signin') : t('auth.signup')}
          </Txt>

          {mode === 'up' ? (
            <Field label={t('auth.name')} value={name} onChangeText={setName} placeholder={t('auth.name.ph')} testID="name-input" />
          ) : null}
          <Field
            label={t('auth.email')}
            value={email}
            onChangeText={setEmail}
            placeholder={t('auth.email.ph')}
            keyboardType="email-address"
            testID="email-input"
          />
          <Field
            label={t('auth.password')}
            value={password}
            onChangeText={setPassword}
            placeholder={t('auth.password.ph')}
            secure
            testID="password-input"
          />

          {error ? <Banner text={error} testID="auth-error" /> : null}

          <Btn
            label={mode === 'in' ? t('auth.signin') : t('auth.signup')}
            onPress={submit}
            loading={busy}
            icon="arrow-right"
            testID="auth-submit"
          />

          <View style={{ flexDirection: 'row', alignItems: 'center', gap: space.md }}>
            <View style={{ flex: 1, height: 1, backgroundColor: c.border }} />
            <Text style={{ fontFamily: f.regular, fontSize: 12, color: c.textDim }}>{t('auth.or')}</Text>
            <View style={{ flex: 1, height: 1, backgroundColor: c.border }} />
          </View>

          <Btn label={t('auth.google')} onPress={google} variant="outline" icon="log-in" testID="google-signin" />

          <Pressable
            testID="auth-toggle"
            onPress={() => {
              setMode(mode === 'in' ? 'up' : 'in');
              setError('');
            }}
            style={{ paddingVertical: space.sm, ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}) }}
          >
            <Text style={{ fontFamily: f.medium, fontSize: 14, color: c.primary, textAlign: 'center' }}>
              {mode === 'in' ? t('auth.new') : t('auth.have')}
            </Text>
          </Pressable>
        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
}
