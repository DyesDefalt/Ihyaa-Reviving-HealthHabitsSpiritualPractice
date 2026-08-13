import { Redirect } from 'expo-router';
import React from 'react';
import { ActivityIndicator, View } from 'react-native';
import { useAuth } from '../src/auth';
import { GeoPattern } from '../src/components/GeoPattern';
import { useI18n } from '../src/i18n';
import { fontsFor } from '../src/theme';
import { Text } from 'react-native';

export default function Index() {
  const { user, booting } = useAuth();
  const { lang, t } = useI18n();

  if (booting) {
    const f = fontsFor(lang);
    return (
      <View
        testID="boot-splash"
        style={{ flex: 1, backgroundColor: '#1B3B36', alignItems: 'center', justifyContent: 'center', gap: 20 }}
      >
        <GeoPattern color="#FFFFFF" opacity={0.08} size={64} />
        <Text style={{ fontFamily: 'Amiri_700Bold', fontSize: 46, color: '#FFFFFF' }}>إحياء</Text>
        <Text style={{ fontFamily: f.medium, fontSize: 15, color: 'rgba(255,255,255,0.65)', letterSpacing: 2 }}>
          {t('app.tagline')}
        </Text>
        <ActivityIndicator color="#B5653E" />
      </View>
    );
  }

  if (!user) return <Redirect href="/sign-in" />;
  if (!user.onboarding_completed) return <Redirect href="/onboarding" />;
  return <Redirect href="/(tabs)" />;
}
