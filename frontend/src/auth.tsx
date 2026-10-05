import React, { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { api, clearTokens, loadTokens, setTokens } from './api';

export type Prefs = {
  fitness_level: string;
  health_goals: string[];
  dietary_preferences: string[];
  sleep_habit: string;
  spiritual_level: string;
  preferred_challenge: string;
  reminders_enabled: boolean;
};

export type Me = {
  id: string;
  email: string;
  name: string;
  picture: string | null;
  role: string;
  language: string;
  theme: string;
  timezone: string;
  onboarding_completed: boolean;
  is_pro: boolean;
  pro_until: string | null;
  points_balance: number;
  lifetime_points: number;
  current_streak: number;
  longest_streak: number;
  last_checkin_date: string | null;
  prefs: Prefs;
};

type AuthCtx = {
  user: Me | null;
  booting: boolean;
  bootError: boolean;
  retryBootstrap: () => Promise<void>;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, name: string, language: string) => Promise<void>;
  signInGoogle: (sessionId: string) => Promise<void>;
  signOut: () => Promise<void>;
  refresh: () => Promise<void>;
  patchUser: (u: Me) => void;
};

const Ctx = createContext<AuthCtx | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<Me | null>(null);
  const [booting, setBooting] = useState(true);
  const [bootError, setBootError] = useState(false);

  const refresh = useCallback(async () => {
    try {
      const me = await api('/auth/me');
      setUser(me);
      setBootError(false);
    } catch (error: any) {
      if (error.status === 401) { setUser(null); setBootError(false); }
      else setBootError(true);
    }
  }, []);

  const retryBootstrap = useCallback(async () => {
    setBooting(true);
    setBootError(false);
    try {
      const token = await loadTokens();
      if (token) await refresh();
    } catch { setBootError(true); }
    finally { setBooting(false); }
  }, [refresh]);

  useEffect(() => {
    retryBootstrap();
  }, [retryBootstrap]);

  const signIn = async (email: string, password: string) => {
    const data = await api('/auth/login', { method: 'POST', auth: false, body: { email, password } });
    await setTokens(data.access_token, data.refresh_token);
    setUser(data.user);
    setBootError(false);
  };

  const signUp = async (email: string, password: string, name: string, language: string) => {
    const data = await api('/auth/register', {
      method: 'POST',
      auth: false,
      body: { email, password, name, language },
    });
    await setTokens(data.access_token, data.refresh_token);
    setUser(data.user);
    setBootError(false);
  };

  const signInGoogle = async (sessionId: string) => {
    const data = await api('/auth/google/session', {
      method: 'POST',
      auth: false,
      body: { session_id: sessionId },
    });
    await setTokens(data.access_token, data.refresh_token);
    setUser(data.user);
    setBootError(false);
  };

  const signOut = async () => {
    try {
      await api('/auth/logout', { method: 'POST' });
    } catch {
      /* offline sign-out is still a sign-out */
    }
    await clearTokens();
    setUser(null);
    setBootError(false);
  };

  return (
    <Ctx.Provider
      value={{ user, booting, bootError, retryBootstrap, signIn, signUp, signInGoogle, signOut, refresh, patchUser: setUser }}
    >
      {children}
    </Ctx.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('useAuth outside AuthProvider');
  return ctx;
}
