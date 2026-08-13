import Feather from '@expo/vector-icons/Feather';
import { BlurView } from 'expo-blur';
import { Tabs } from 'expo-router';
import React from 'react';
import { Platform, Text, View } from 'react-native';
import { useI18n } from '../../src/i18n';
import { fontsFor, radii, useTheme } from '../../src/theme';

export default function TabsLayout() {
  const { c, mode } = useTheme();
  const { t, lang } = useI18n();
  const f = fontsFor(lang);

  const items: { name: string; label: string; icon: keyof typeof Feather.glyphMap }[] = [
    { name: 'index', label: t('nav.today'), icon: 'sunrise' },
    { name: 'calendar', label: t('nav.calendar'), icon: 'calendar' },
    { name: 'progress', label: t('nav.progress'), icon: 'trending-up' },
    { name: 'store', label: t('nav.store'), icon: 'gift' },
    { name: 'profile', label: t('nav.profile'), icon: 'user' },
  ];

  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: c.primary,
        tabBarInactiveTintColor: c.textDim,
        tabBarShowLabel: false,
        sceneStyle: { backgroundColor: c.background },
        tabBarStyle: {
          position: 'absolute',
          left: 14,
          right: 14,
          bottom: Platform.OS === 'ios' ? 24 : 12,
          height: 62,
          paddingTop: 6,
          paddingBottom: 6,
          borderRadius: radii.lg,
          borderTopWidth: 0,
          borderWidth: 1,
          borderColor: c.border,
          backgroundColor: Platform.OS === 'android' ? c.surface : 'transparent',
          elevation: 8,
          shadowColor: '#000',
          shadowOpacity: mode === 'light' ? 0.1 : 0.35,
          shadowRadius: 18,
          shadowOffset: { width: 0, height: 6 },
        },
        tabBarBackground: () =>
          Platform.OS === 'android' ? null : (
            <BlurView
              tint={mode === 'light' ? 'light' : 'dark'}
              intensity={70}
              style={{ flex: 1, borderRadius: radii.lg, overflow: 'hidden', backgroundColor: mode === 'light' ? 'rgba(247,245,240,0.72)' : 'rgba(18,20,19,0.7)' }}
            />
          ),
      }}
    >
      {items.map((it) => (
        <Tabs.Screen
          key={it.name}
          name={it.name}
          options={{
            title: it.label,
            tabBarButtonTestID: `tab-${it.name}`,
            tabBarIcon: ({ color, focused }) => (
              <View style={{ alignItems: 'center', justifyContent: 'center', gap: 3, width: 62 }}>
                <Feather name={it.icon} size={focused ? 20 : 18} color={color} />
                <Text
                  numberOfLines={1}
                  style={{ fontFamily: focused ? f.semibold : f.medium, fontSize: 9.5, color }}
                >
                  {it.label}
                </Text>
              </View>
            ),
          }}
        />
      ))}
    </Tabs>
  );
}
