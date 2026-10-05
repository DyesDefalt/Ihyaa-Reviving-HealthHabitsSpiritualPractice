import React from 'react';
import { Redirect } from 'expo-router';
import { View } from 'react-native';
import { useAuth } from '../auth';
import { useI18n } from '../i18n';
import { useTheme } from '../theme';
import { Banner, Btn, Loader } from './ui';

export const SessionGate = ({ children }: { children: React.ReactNode }) => {
  const { user, booting, bootError, retryBootstrap } = useAuth();
  const { lang, t } = useI18n();
  const { c } = useTheme();
  if (booting) return <Loader testID="session-loading" />;
  if (bootError) return <View testID="session-error-screen" style={{ flex: 1, justifyContent: 'center', padding: 24, gap: 20, backgroundColor: c.background }}>
    <Banner testID="session-error" text={lang === 'id' ? 'Profil belum dapat dimuat. Periksa koneksi dan coba lagi.' : 'Your profile could not be loaded. Check your connection and try again.'} />
    <Btn testID="session-retry" label={t('common.retry')} icon="refresh-cw" onPress={retryBootstrap} />
  </View>;
  if (!user) return <Redirect href="/sign-in" />;
  return <>{children}</>;
};