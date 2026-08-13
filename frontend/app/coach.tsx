import Feather from '@expo/vector-icons/Feather';
import { router } from 'expo-router';
import React, { useEffect, useRef, useState } from 'react';
import {
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  ScrollView,
  Text,
  TextInput,
  View,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { api, errText } from '../src/api';
import { Banner, Chip, Txt, useFonts } from '../src/components/ui';
import { useI18n } from '../src/i18n';
import { radii, space, useTheme } from '../src/theme';

type Msg = { id: string; role: 'user' | 'assistant'; content: string };

/** Renders **bold** segments; the coach otherwise replies in plain text. */
function RichText({ content, color, align }: { content: string; color: string; align: 'left' | 'right' }) {
  const { lang } = useI18n();
  const f = useFonts();
  const parts = content.split(/(\*\*[^*]+\*\*)/g).filter(Boolean);
  return (
    <Text
      style={{
        fontFamily: f.regular,
        fontSize: 14.5,
        lineHeight: lang === 'ar' ? 26 : 22,
        color,
        textAlign: align,
      }}
    >
      {parts.map((p, i) =>
        p.startsWith('**') && p.endsWith('**') ? (
          <Text key={i} style={{ fontFamily: f.semibold }}>
            {p.slice(2, -2)}
          </Text>
        ) : (
          p
        )
      )}
    </Text>
  );
}

export default function Coach() {
  const { c, mode } = useTheme();
  const { t, row, align, lang } = useI18n();
  const insets = useSafeAreaInsets();
  const f = useFonts();
  const scroller = useRef<ScrollView>(null);

  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    api('/coach/history')
      .then(setMessages)
      .catch(() => undefined);
  }, []);

  async function send(text: string) {
    const value = text.trim();
    if (!value || busy) return;
    setError('');
    setInput('');
    setMessages((m) => [...m, { id: `local-${Date.now()}`, role: 'user', content: value }]);
    setBusy(true);
    setTimeout(() => scroller.current?.scrollToEnd({ animated: true }), 60);
    try {
      const res = await api('/coach/chat-sync', { method: 'POST', body: { message: value } });
      setMessages((m) => [...m, { id: `reply-${Date.now()}`, role: 'assistant', content: res.reply }]);
    } catch (e: any) {
      setError(errText(e?.detail ?? e?.message));
    } finally {
      setBusy(false);
      setTimeout(() => scroller.current?.scrollToEnd({ animated: true }), 80);
    }
  }

  async function clear() {
    await api('/coach/history', { method: 'DELETE' });
    setMessages([]);
  }

  const suggestions = [t('coach.s1'), t('coach.s2'), t('coach.s3')];

  return (
    <KeyboardAvoidingView
      style={{ flex: 1, backgroundColor: c.background }}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <View
        style={{
          paddingTop: insets.top + space.md,
          paddingHorizontal: space.lg,
          paddingBottom: space.md,
          flexDirection: row,
          alignItems: 'center',
          gap: space.md,
          borderBottomWidth: 1,
          borderBottomColor: c.border,
          backgroundColor: c.surface,
        }}
      >
        <Pressable
          testID="coach-back"
          onPress={() => router.back()}
          style={{
            width: 38,
            height: 38,
            borderRadius: radii.full,
            backgroundColor: c.background,
            borderWidth: 1,
            borderColor: c.border,
            alignItems: 'center',
            justifyContent: 'center',
            ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}),
          }}
        >
          <Feather name="arrow-left" size={18} color={c.text} />
        </Pressable>
        <View style={{ flex: 1 }}>
          <Txt variant="body" weight="bold">{t('coach.title')}</Txt>
          <Txt variant="caption" color={c.textDim}>{t('coach.subtitle')}</Txt>
        </View>
        {messages.length > 0 ? (
          <Pressable testID="coach-clear" onPress={clear} hitSlop={8} style={Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : undefined}>
            <Feather name="trash-2" size={17} color={c.textDim} />
          </Pressable>
        ) : null}
      </View>

      <ScrollView
        ref={scroller}
        testID="coach-screen"
        contentContainerStyle={{ padding: space.lg, gap: space.md, paddingBottom: space.xl }}
        showsVerticalScrollIndicator={false}
      >
        {messages.length === 0 ? (
          <View style={{ gap: space.md, alignItems: 'center', paddingVertical: space.xl }}>
            <View style={{ width: 58, height: 58, borderRadius: radii.full, backgroundColor: mode === 'light' ? '#EDF2F0' : c.surfaceAlt, alignItems: 'center', justifyContent: 'center' }}>
              <Feather name="message-circle" size={26} color={c.primary} />
            </View>
            <Txt variant="small" color={c.textDim} style={{ textAlign: 'center', maxWidth: 300 }}>
              {t('coach.empty')}
            </Txt>
            <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: space.sm, justifyContent: 'center' }}>
              {suggestions.map((s, i) => (
                <Chip key={s} testID={`coach-suggest-${i}`} label={s} onPress={() => send(s)} />
              ))}
            </View>
          </View>
        ) : null}

        {messages.map((m) => {
          const mine = m.role === 'user';
          return (
            <View
              key={m.id}
              testID={`coach-msg-${m.role}`}
              style={{
                alignSelf: mine ? 'flex-end' : 'flex-start',
                maxWidth: '88%',
                backgroundColor: mine ? c.primary : c.surface,
                borderWidth: mine ? 0 : 1,
                borderColor: c.border,
                borderRadius: radii.md,
                borderBottomEndRadius: mine ? 4 : radii.md,
                borderBottomStartRadius: mine ? radii.md : 4,
                padding: space.md,
              }}
            >
              <RichText content={m.content} color={mine ? '#fff' : c.text} align={align} />
            </View>
          );
        })}

        {busy ? (
          <View style={{ flexDirection: row, alignItems: 'center', gap: space.sm, alignSelf: 'flex-start' }}>
            <ActivityIndicator size="small" color={c.primary} />
            <Text style={{ fontFamily: f.regular, fontSize: 13, color: c.textDim }}>{t('coach.thinking')}…</Text>
          </View>
        ) : null}

        {error ? <Banner text={error} testID="coach-error" /> : null}
      </ScrollView>

      <View
        style={{
          padding: space.md,
          paddingBottom: insets.bottom + space.md,
          borderTopWidth: 1,
          borderTopColor: c.border,
          backgroundColor: c.surface,
          gap: 6,
        }}
      >
        <View style={{ flexDirection: row, alignItems: 'flex-end', gap: space.sm }}>
          <TextInput
            testID="coach-input"
            value={input}
            onChangeText={setInput}
            placeholder={t('coach.ph')}
            placeholderTextColor={c.textDim}
            multiline
            onSubmitEditing={() => send(input)}
            style={{
              flex: 1,
              maxHeight: 110,
              minHeight: 46,
              backgroundColor: c.background,
              borderWidth: 1.5,
              borderColor: c.border,
              borderRadius: radii.md,
              paddingHorizontal: space.md,
              paddingTop: 12,
              paddingBottom: 12,
              fontFamily: f.regular,
              fontSize: 15,
              color: c.text,
              textAlign: align,
              ...(Platform.OS === 'web' ? ({ outlineStyle: 'none' } as any) : {}),
            }}
          />
          <Pressable
            testID="coach-send"
            onPress={() => send(input)}
            disabled={busy || !input.trim()}
            style={{
              width: 46,
              height: 46,
              borderRadius: radii.full,
              backgroundColor: c.primary,
              alignItems: 'center',
              justifyContent: 'center',
              opacity: busy || !input.trim() ? 0.45 : 1,
              ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}),
            }}
          >
            <Feather name="send" size={18} color="#fff" />
          </Pressable>
        </View>
        <Text style={{ fontFamily: f.regular, fontSize: 10.5, color: c.textDim, textAlign: 'center' }}>
          {t('coach.disclaimer')}
        </Text>
      </View>
    </KeyboardAvoidingView>
  );
}
