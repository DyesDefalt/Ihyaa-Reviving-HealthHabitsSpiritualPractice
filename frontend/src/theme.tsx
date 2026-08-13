import React, { createContext, useContext, useMemo, useState } from 'react';
import { Platform } from 'react-native';

export const palette = {
  light: {
    background: '#F7F5F0',
    surface: '#FFFFFF',
    surfaceAlt: '#F0EBE1',
    primary: '#1B3B36',
    primarySoft: '#2D6058',
    onPrimary: '#FFFFFF',
    secondary: '#B5653E',
    text: '#1A1A1A',
    textDim: '#5C5F5E',
    border: '#E8E4DB',
    success: '#2A9D8F',
    error: '#E76F51',
    warning: '#E9C46A',
    overlay: 'rgba(27,59,54,0.06)',
  },
  dark: {
    background: '#121413',
    surface: '#1A201E',
    surfaceAlt: '#242A28',
    primary: '#2D6058',
    primarySoft: '#37766C',
    onPrimary: '#FFFFFF',
    secondary: '#CF8460',
    text: '#F2F2F2',
    textDim: '#A0A4A3',
    border: '#2C3331',
    success: '#45B6A8',
    error: '#F28C74',
    warning: '#F4D58D',
    overlay: 'rgba(255,255,255,0.05)',
  },
};

export const pillarColor: Record<string, string> = {
  physical: '#B5653E',
  nutrition: '#D99B29',
  mental: '#4A6FA5',
  spiritual: '#2A9D8F',
};

export const pillarIcon: Record<string, string> = {
  physical: 'activity',
  nutrition: 'coffee',
  mental: 'cloud',
  spiritual: 'moon',
};

export const space = { xs: 4, sm: 8, md: 16, lg: 24, xl: 32, xxl: 48 };
export const radii = { sm: 8, md: 16, lg: 24, full: 9999 };

export const type = {
  h1: { fontSize: 32, lineHeight: 40, letterSpacing: -0.5 },
  h2: { fontSize: 24, lineHeight: 32, letterSpacing: -0.3 },
  h3: { fontSize: 20, lineHeight: 28, letterSpacing: -0.2 },
  bodyLg: { fontSize: 18, lineHeight: 26 },
  body: { fontSize: 16, lineHeight: 24 },
  small: { fontSize: 14, lineHeight: 20 },
  caption: { fontSize: 12, lineHeight: 16, letterSpacing: 0.2 },
};

export const shadow = (mode: 'light' | 'dark', size: 'sm' | 'md' = 'sm') => {
  const conf = {
    light: {
      sm: { shadowColor: '#1A1A1A', shadowOpacity: 0.05, shadowRadius: 4, elevation: 2 },
      md: { shadowColor: '#1A1A1A', shadowOpacity: 0.09, shadowRadius: 16, elevation: 5 },
    },
    dark: {
      sm: { shadowColor: '#000000', shadowOpacity: 0.25, shadowRadius: 4, elevation: 2 },
      md: { shadowColor: '#000000', shadowOpacity: 0.35, shadowRadius: 16, elevation: 5 },
    },
  }[mode][size];
  return {
    ...conf,
    shadowOffset: { width: 0, height: size === 'sm' ? 2 : 8 },
  };
};

export type Fonts = {
  regular: string;
  medium: string;
  semibold: string;
  bold: string;
  scripture: string;
};

export const fontsFor = (lang: string): Fonts =>
  lang === 'ar'
    ? {
        regular: 'Tajawal_400Regular',
        medium: 'Tajawal_500Medium',
        semibold: 'Tajawal_500Medium',
        bold: 'Tajawal_700Bold',
        scripture: 'Amiri_400Regular',
      }
    : {
        regular: 'Outfit_400Regular',
        medium: 'Outfit_500Medium',
        semibold: 'Outfit_600SemiBold',
        bold: 'Outfit_700Bold',
        scripture: 'Amiri_400Regular',
      };

type ThemeCtx = {
  mode: 'light' | 'dark';
  c: typeof palette.light;
  setMode: (m: 'light' | 'dark') => void;
  toggle: () => void;
};

const Ctx = createContext<ThemeCtx | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [mode, setMode] = useState<'light' | 'dark'>('light');
  const value = useMemo(
    () => ({ mode, c: palette[mode], setMode, toggle: () => setMode((m) => (m === 'light' ? 'dark' : 'light')) }),
    [mode]
  );
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useTheme() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('useTheme outside ThemeProvider');
  return ctx;
}

export const webFix = Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {};
