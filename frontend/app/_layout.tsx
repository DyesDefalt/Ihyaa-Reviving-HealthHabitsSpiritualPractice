import {
  Amiri_400Regular,
  Amiri_700Bold,
} from '@expo-google-fonts/amiri';
import {
  Outfit_400Regular,
  Outfit_500Medium,
  Outfit_600SemiBold,
  Outfit_700Bold,
} from '@expo-google-fonts/outfit';
import {
  Tajawal_400Regular,
  Tajawal_500Medium,
  Tajawal_700Bold,
} from '@expo-google-fonts/tajawal';
import { useFonts } from 'expo-font';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import React, { useEffect, useRef } from 'react';
import { ActivityIndicator, Platform, View } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { AuthProvider, useAuth } from '../src/auth';
import { I18nProvider } from '../src/i18n';
import { ThemeProvider, useTheme } from '../src/theme';

function GoogleCallbackHandler() {
  // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
  const { signInGoogle } = useAuth();
  const handled = useRef(false);

  useEffect(() => {
    if (Platform.OS !== 'web' || handled.current) return;
    const hash = window.location.hash || '';
    if (!hash.includes('session_id=')) return;
    handled.current = true;
    const sessionId = new URLSearchParams(hash.replace(/^#/, '')).get('session_id');
    if (!sessionId) return;
    window.history.replaceState(null, '', window.location.pathname);
    signInGoogle(sessionId).catch(() => undefined);
  }, [signInGoogle]);

  return null;
}

function Shell() {
  const { c, mode } = useTheme();
  return (
    <>
      <StatusBar style={mode === 'light' ? 'dark' : 'light'} />
      <GoogleCallbackHandler />
      <View
        style={{
          flex: 1,
          backgroundColor: Platform.OS === 'web' ? (mode === 'light' ? '#E4E0D6' : '#0A0C0B') : c.background,
          alignItems: 'center',
        }}
      >
        <View
          style={{
            flex: 1,
            width: '100%',
            maxWidth: Platform.OS === 'web' ? 460 : undefined,
            backgroundColor: c.background,
            overflow: 'hidden',
            ...(Platform.OS === 'web'
              ? ({ boxShadow: '0 0 60px rgba(0,0,0,0.14)' } as any)
              : {}),
          }}
        >
          <Stack
            screenOptions={{
              headerShown: false,
              contentStyle: { backgroundColor: c.background },
              animation: 'fade',
            }}
          />
        </View>
      </View>
    </>
  );
}

export default function RootLayout() {
  const [loaded] = useFonts({
    Outfit_400Regular,
    Outfit_500Medium,
    Outfit_600SemiBold,
    Outfit_700Bold,
    Tajawal_400Regular,
    Tajawal_500Medium,
    Tajawal_700Bold,
    Amiri_400Regular,
    Amiri_700Bold,
  });

  if (!loaded) {
    return (
      <View style={{ flex: 1, backgroundColor: '#1B3B36', alignItems: 'center', justifyContent: 'center' }}>
        <ActivityIndicator color="#FFFFFF" size="large" />
      </View>
    );
  }

  return (
    <SafeAreaProvider>
      <ThemeProvider>
        <I18nProvider>
          <AuthProvider>
            <Shell />
          </AuthProvider>
        </I18nProvider>
      </ThemeProvider>
    </SafeAreaProvider>
  );
}
