import Feather from '@expo/vector-icons/Feather';
import { LinearGradient } from 'expo-linear-gradient';
import { useFocusEffect } from 'expo-router';
import React, { useCallback, useState } from 'react';
import { ScrollView, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { api, errText } from '../../src/api';
import { useAuth } from '../../src/auth';
import { GeoPattern } from '../../src/components/GeoPattern';
import { Banner, Btn, Card, Loader, Txt, useFonts } from '../../src/components/ui';
import { useI18n } from '../../src/i18n';
import { radii, space, useTheme } from '../../src/theme';

type Item = { id: string; name: string; description: string; points_cost: number; grants_pro_days: number };

export default function Store() {
  const { c, mode } = useTheme();
  const { t, row, align, lang } = useI18n();
  const { user, patchUser } = useAuth();
  const insets = useSafeAreaInsets();
  const f = useFonts();

  const [items, setItems] = useState<Item[] | null>(null);
  const [busy, setBusy] = useState('');
  const [msg, setMsg] = useState<{ text: string; tone: 'ok' | 'error' } | null>(null);

  const load = useCallback(async () => {
    const list = await api(`/store/items?lang=${lang}`);
    setItems(list);
  }, [lang]);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load])
  );

  async function redeem(item: Item) {
    setBusy(item.id);
    setMsg(null);
    try {
      const res = await api(`/store/redeem/${item.id}`, { method: 'POST' });
      patchUser(res.user);
      setMsg({ text: t('store.redeemed'), tone: 'ok' });
    } catch (e: any) {
      setMsg({ text: errText(e?.detail ?? e?.message), tone: 'error' });
    } finally {
      setBusy('');
    }
  }

  if (!items) return <Loader testID="store-loading" />;

  const balance = user?.points_balance ?? 0;
  const earn = [
    { k: 'task', v: '+10–24' },
    { k: 'checkin', v: '+15' },
    { k: 'all', v: '+50' },
    { k: 'streak', v: '+100' },
  ];

  return (
    <ScrollView
      testID="store-screen"
      style={{ flex: 1, backgroundColor: c.background }}
      contentContainerStyle={{ paddingTop: insets.top + space.lg, paddingBottom: 120, gap: space.md }}
      showsVerticalScrollIndicator={false}
    >
      <View style={{ paddingHorizontal: space.lg, gap: 2 }}>
        <Txt variant="h2" weight="bold">{t('store.title')}</Txt>
        <Txt variant="small" color={c.textDim}>{t('store.subtitle')}</Txt>
      </View>

      <View style={{ paddingHorizontal: space.lg }}>
        <LinearGradient
          colors={['#B5653E', '#8F4B2C']}
          start={{ x: 0, y: 0 }}
          end={{ x: 1, y: 1 }}
          style={{ borderRadius: radii.lg, padding: space.lg, overflow: 'hidden' }}
        >
          <GeoPattern color="#FFFFFF" opacity={0.12} size={46} />
          <View style={{ flexDirection: row, alignItems: 'center', justifyContent: 'space-between' }}>
            <View>
              <Text style={{ fontFamily: f.regular, fontSize: 12, color: 'rgba(255,255,255,0.8)', textAlign: align }}>
                {t('store.balance')}
              </Text>
              <Text testID="store-balance" style={{ fontFamily: f.bold, fontSize: 42, color: '#fff' }}>{balance}</Text>
              <Text style={{ fontFamily: f.regular, fontSize: 11.5, color: 'rgba(255,255,255,0.8)', textAlign: align }}>
                {t('store.available')}
              </Text>
            </View>
            <View style={{ width: 58, height: 58, borderRadius: radii.md, backgroundColor: 'rgba(255,255,255,0.2)', alignItems: 'center', justifyContent: 'center' }}>
              <Feather name="gift" size={26} color="#fff" />
            </View>
          </View>
          {user?.is_pro && user?.pro_until ? (
            <View style={{ marginTop: space.md, backgroundColor: 'rgba(255,255,255,0.18)', borderRadius: radii.sm, paddingVertical: 8, paddingHorizontal: 12 }}>
              <Text testID="pro-badge" style={{ fontFamily: f.semibold, fontSize: 12, color: '#fff', textAlign: align }}>
                {t('store.pro_active', { date: user.pro_until })}
              </Text>
            </View>
          ) : null}
        </LinearGradient>
      </View>

      {msg ? (
        <View style={{ paddingHorizontal: space.lg }}>
          <Banner text={msg.text} tone={msg.tone} testID="store-message" />
        </View>
      ) : null}

      <View style={{ paddingHorizontal: space.lg }}>
        <Card style={{ gap: space.sm }}>
          <Txt variant="small" weight="semibold">{t('store.earn')}</Txt>
          {earn.map((e) => (
            <View key={e.k} style={{ flexDirection: row, justifyContent: 'space-between' }}>
              <Text style={{ fontFamily: f.regular, fontSize: 13, color: c.textDim }}>{t(`store.earn.${e.k}`)}</Text>
              <Text style={{ fontFamily: f.semibold, fontSize: 13, color: c.success }}>{e.v}</Text>
            </View>
          ))}
        </Card>
      </View>

      <View style={{ paddingHorizontal: space.lg, gap: space.sm }}>
        <Txt variant="h3" weight="bold">{t('store.items')}</Txt>
        {items.map((item) => {
          const affordable = balance >= item.points_cost;
          return (
            <Card key={item.id} testID={`store-item-${item.id}`} padded={false} style={{ overflow: 'hidden' }}>
              <LinearGradient
                colors={mode === 'light' ? ['#1B3B36', '#24534A'] : ['#16302C', '#1E463F']}
                style={{ padding: space.md, flexDirection: row, alignItems: 'center', gap: space.md, overflow: 'hidden' }}
              >
                <GeoPattern color="#FFFFFF" opacity={0.1} size={40} />
                <View style={{ width: 42, height: 42, borderRadius: radii.sm, backgroundColor: 'rgba(255,255,255,0.18)', alignItems: 'center', justifyContent: 'center' }}>
                  <Feather name="award" size={20} color="#E9C46A" />
                </View>
                <View style={{ flex: 1 }}>
                  <Text style={{ fontFamily: f.bold, fontSize: 15.5, color: '#fff', textAlign: align }}>{item.name}</Text>
                  <View style={{ flexDirection: row, alignItems: 'center', gap: 5, marginTop: 2 }}>
                    <Feather name="star" size={11} color="#E9C46A" />
                    <Text style={{ fontFamily: f.medium, fontSize: 12, color: 'rgba(255,255,255,0.85)' }}>
                      {item.points_cost.toLocaleString()} {t('common.points')}
                    </Text>
                  </View>
                </View>
              </LinearGradient>
              <View style={{ padding: space.md, gap: space.md }}>
                <Text style={{ fontFamily: f.regular, fontSize: 13.5, lineHeight: 21, color: c.textDim, textAlign: align }}>
                  {item.description}
                </Text>
                <Btn
                  label={affordable ? t('store.redeem') : t('store.need', { n: (item.points_cost - balance).toLocaleString() })}
                  onPress={() => redeem(item)}
                  disabled={!affordable}
                  loading={busy === item.id}
                  icon={affordable ? 'gift' : 'lock'}
                  testID={`redeem-${item.id}`}
                />
              </View>
            </Card>
          );
        })}
      </View>
    </ScrollView>
  );
}
