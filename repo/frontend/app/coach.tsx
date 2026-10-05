import Feather from '@expo/vector-icons/Feather';
import { Redirect, router } from 'expo-router';
import React, { useRef, useState } from 'react';
import { ActivityIndicator, KeyboardAvoidingView, Platform, Pressable, ScrollView, TextInput, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useAuth } from '../src/auth';
import { Banner, Btn, Txt, useFonts } from '../src/components/ui';
import { CoachDialog } from '../src/coach/CoachDialog';
import { coachCopy, coachError } from '../src/coach/copy';
import { useCoach } from '../src/coach/useCoach';
import { useI18n } from '../src/i18n';
import { space, useTheme } from '../src/theme';
import { SessionGate } from '../src/components/SessionGate';
import { DecisionLabel } from '../src/coach/DecisionLabel';

export default function Coach() {
  return <SessionGate><CoachContent /></SessionGate>;
}

function CoachContent() {
  const { c } = useTheme();
  const { t, lang } = useI18n();
  const { user, booting } = useAuth();
  const f = useFonts();
  const insets = useSafeAreaInsets();
  const scroller = useRef<ScrollView>(null);
  const chat = useCoach(user?.id, lang);
  const copy = coachCopy(lang);
  const [dialog, setDialog] = useState<'sessions' | 'delete' | 'privacy' | null>(null);
  const locked = chat.busy || chat.loading;
  const title = chat.sessions.find((s) => s.session_id === chat.sessionId)?.title;
  const sending = chat.messages.some((m) => m.id.startsWith('pending-assistant'));

  if (!booting && !user) return <Redirect href="/sign-in" />;

  const icon = (name: keyof typeof Feather.glyphMap, label: string, id: string, action: () => void, disabled = locked) => (
    <Pressable testID={id} accessibilityRole="button" accessibilityLabel={label} disabled={disabled} onPress={action}
      style={({ pressed }) => ({ width: 36, height: 40, alignItems: 'center', justifyContent: 'center', opacity: disabled ? 0.35 : pressed ? 0.5 : 1,
        ...(Platform.OS === 'web' ? { cursor: 'pointer' } as any : {}) })}>
      <Feather name={name} size={20} color={c.primary} />
    </Pressable>
  );
  const privacyText = <>
    <Txt testID="coach-privacy-summary" variant="small" style={{ lineHeight: 22 }}>{copy.consentBody}</Txt>
    <Txt testID="coach-privacy-detail" variant="small" color={c.textDim} style={{ lineHeight: 22 }}>{copy.consentDetail}</Txt>
  </>;

  return <KeyboardAvoidingView style={{ flex: 1, backgroundColor: c.background }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
    <View style={{ paddingTop: insets.top + 10, paddingHorizontal: 14, paddingBottom: 12, borderBottomWidth: 1, borderBottomColor: c.border, backgroundColor: c.surface }}>
      <View style={{ flexDirection: 'row', gap: 4, alignItems: 'center' }}>
        {icon('arrow-left', copy.back, 'coach-back', () => router.canGoBack() ? router.back() : router.replace('/(tabs)'))}
        <View style={{ flex: 1, minWidth: 0, paddingHorizontal: 6 }}>
          <Txt testID="coach-title" weight="bold">{t('coach.title')}</Txt>
          <Txt testID="coach-model" variant="caption" color={c.textDim} numberOfLines={1}>
            {chat.config ? `OpenAI · ${chat.config.model.toUpperCase().replace(/-/g, ' ')}` : t('common.loading')}
          </Txt>
        </View>
        {icon('clock', copy.conversations, 'coach-history', () => setDialog('sessions'))}
        {icon('plus', copy.newChat, 'coach-new', () => { chat.newChat(); })}
      </View>
    </View>

    <ScrollView ref={scroller} testID="coach-screen" style={{ flex: 1 }}
      contentContainerStyle={{ padding: space.lg, gap: space.md, paddingBottom: 28 }}
      onContentSizeChange={() => { if (sending) scroller.current?.scrollToEnd({ animated: false }); }}>
      {chat.loading || booting ? <View testID="coach-loading" style={{ padding: 30, gap: 12 }}>
        <ActivityIndicator color={c.primary} /><Txt variant="small">{copy.loading}</Txt>
      </View> : null}

      {!chat.loading && chat.config?.consent_required ? <View testID="coach-consent" style={{ gap: 22, paddingVertical: 28 }}>
        <Feather name="shield" size={36} color={c.primary} />
        <Txt testID="coach-consent-title" variant="h2" weight="bold">{copy.consentTitle}</Txt>
        {privacyText}
        <Btn testID="coach-consent-accept" label={copy.consentAction} icon="check" loading={chat.busy} onPress={() => chat.consent(true)} />
      </View> : null}

      {!chat.loading && chat.config && !chat.config.consent_required ? <>
        <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8 }}>
          <Txt testID="coach-session-title" variant="caption" color={c.textDim} numberOfLines={1} style={{ flex: 1 }}>{title}</Txt>
          {icon('trash-2', copy.deleteChat, 'coach-clear', () => setDialog('delete'))}
        </View>
        {chat.messages.length === 0 ? <View testID="coach-empty" style={{ gap: 22, paddingVertical: 22 }}>
          <View style={{ width: 52, height: 52, borderRadius: 26, backgroundColor: c.surfaceAlt, alignItems: 'center', justifyContent: 'center' }}>
            <Feather name="message-circle" size={25} color={c.primary} />
          </View>
          <Txt testID="coach-empty-title" variant="h2" weight="semibold">{t('coach.empty')}</Txt>
          <View style={{ gap: 10 }}>
            {[t('coach.s1'), t('coach.s2'), t('coach.s3')].map((suggestion, i) => <Pressable key={suggestion}
              testID={`coach-suggest-${i}`} accessibilityRole="button" disabled={locked} onPress={() => chat.send(suggestion)}
              style={({ pressed }) => ({ borderWidth: 1, borderColor: c.border, borderRadius: 8, padding: 14, flexDirection: 'row', alignItems: 'center', gap: 10,
                backgroundColor: pressed ? c.surfaceAlt : c.surface, opacity: locked ? 0.5 : 1 })}>
              <Feather name={(['sunrise', 'activity', 'moon'] as const)[i]} size={17} color={c.secondary} />
              <Txt variant="small" style={{ flex: 1 }}>{suggestion}</Txt><Feather name="arrow-up-right" size={16} color={c.textDim} />
            </Pressable>)}
          </View>
        </View> : null}
        {chat.messages.map((m) => m.content ? <View key={m.id} testID={`coach-msg-${m.role}-${m.id}`}
          style={{ alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start', maxWidth: '92%', minWidth: 0, gap: 8,
            backgroundColor: m.role === 'user' ? c.primary : c.surface, borderWidth: 1, borderColor: m.role === 'user' ? c.primary : c.border,
            borderRadius: 12, padding: 14 }}>
          {m.role === 'assistant' ? <Txt testID={`coach-label-${m.id}`} variant="caption" color={c.textDim}>
            {m.safety ? copy.safety : copy.suggestion}
          </Txt> : null}
          <Txt testID={`coach-content-${m.id}`} variant="small" color={m.role === 'user' ? '#fff' : c.text}
            style={{ lineHeight: 22, ...(Platform.OS === 'web' ? { overflowWrap: 'anywhere' } as any : {}) }}>{m.content.replace(/\*\*/g, '')}</Txt>
          {m.role === 'assistant' ? <DecisionLabel message={m} /> : null}
        </View> : null)}
        {chat.busy ? <View testID="coach-thinking" style={{ flexDirection: 'row', alignItems: 'center', gap: 10 }}>
          <ActivityIndicator size="small" color={c.primary} /><Txt variant="caption" color={c.textDim}>{chat.messages.at(-1)?.content ? copy.replying : copy.thinking}</Txt>
        </View> : null}
      </> : null}
      {chat.error ? <View style={{ gap: 8 }}>
        <Banner testID="coach-error" text={coachError(chat.error, lang)} />
        <Btn testID="coach-retry" label={copy.retry} variant="outline" disabled={locked} onPress={() => chat.error === 'load_error' ? chat.load() : chat.input ? chat.send(chat.input) : chat.load()} />
      </View> : null}
    </ScrollView>

    {!chat.config?.consent_required && chat.config ? <View style={{ padding: 14, paddingBottom: insets.bottom + 12, backgroundColor: c.surface, borderTopWidth: 1, borderTopColor: c.border, gap: 10 }}>
      <View style={{ flexDirection: 'row', gap: 8, alignItems: 'flex-end' }}>
        <TextInput testID="coach-input" accessibilityLabel={t('coach.ph')} value={chat.input} onChangeText={chat.setInput} multiline maxLength={2000}
          editable={!locked} placeholder={t('coach.ph')} placeholderTextColor={c.textDim}
          style={{ flex: 1, minWidth: 0, minHeight: 46, maxHeight: 110, backgroundColor: c.background, borderWidth: 1, borderColor: c.border,
            borderRadius: 12, padding: 12, fontFamily: f.regular, fontSize: 15, color: c.text }} />
        <Pressable testID="coach-send" accessibilityRole="button" accessibilityLabel={copy.send} disabled={locked || !chat.input.trim()} onPress={() => chat.send(chat.input)}
          style={({ pressed }) => ({ width: 46, height: 46, borderRadius: 23, backgroundColor: c.primary, alignItems: 'center', justifyContent: 'center', opacity: locked || !chat.input.trim() ? 0.4 : pressed ? 0.7 : 1 })}>
          <Feather name="arrow-up" size={22} color="#fff" />
        </Pressable>
      </View>
      {chat.input.length > 1800 ? <Txt testID="coach-character-count" variant="caption" color={c.textDim}>{chat.input.length}/2000</Txt> : null}
      <Txt testID="coach-disclaimer" variant="caption" color={c.textDim} style={{ textAlign: 'center', fontSize: 11 }}>{copy.disclaimer}</Txt>
      <Pressable testID="coach-privacy" accessibilityRole="button" onPress={() => setDialog('privacy')} disabled={locked}>
        <Txt variant="caption" color={c.primary} style={{ textAlign: 'center', textDecorationLine: 'underline' }}>{copy.privacy}</Txt>
      </Pressable>
    </View> : null}

    <CoachDialog id="coach-sessions-dialog" visible={dialog === 'sessions'} title={copy.conversations} onClose={() => setDialog(null)}>
      {chat.error ? <Banner testID="coach-sessions-error" text={coachError(chat.error, lang)} /> : null}
      {chat.sessions.map((session) => <Pressable key={session.session_id} testID={`coach-session-${session.session_id}`} accessibilityRole="button" disabled={locked}
        onPress={async () => { if (await chat.select(session.session_id)) setDialog(null); }}
        style={({ pressed }) => ({ paddingVertical: 14, borderBottomWidth: 1, borderBottomColor: c.border, flexDirection: 'row', gap: 10, opacity: pressed ? 0.6 : 1 })}>
        <Feather name="message-circle" size={17} color={c.primary} />
        <Txt variant="small" style={{ flex: 1 }} numberOfLines={2}>{session.title}</Txt>
        {session.session_id === chat.sessionId ? <Feather name="check" size={17} color={c.primary} /> : null}
      </Pressable>)}
      <Btn testID="coach-dialog-new" label={copy.newChat} icon="plus" disabled={locked} onPress={async () => { if (await chat.newChat()) setDialog(null); }} />
    </CoachDialog>
    <CoachDialog id="coach-delete-dialog" visible={dialog === 'delete'} title={copy.deleteTitle} onClose={() => setDialog(null)}>
      {chat.error ? <Banner testID="coach-delete-error" text={coachError(chat.error, lang)} /> : null}
      <Txt testID="coach-delete-warning" variant="small">{copy.deleteBody}</Txt>
      <Btn testID="coach-delete-confirm" label={copy.delete} icon="trash-2" loading={chat.busy} onPress={async () => { if (await chat.deleteChat()) setDialog(null); }} />
      <Btn testID="coach-delete-cancel" label={copy.cancel} variant="ghost" disabled={locked} onPress={() => setDialog(null)} />
    </CoachDialog>
    <CoachDialog id="coach-privacy-dialog" visible={dialog === 'privacy'} title={copy.privacy} onClose={() => setDialog(null)}>
      {chat.error ? <Banner testID="coach-privacy-error" text={coachError(chat.error, lang)} /> : null}
      {dialog === 'privacy' ? privacyText : null}
      <Btn testID="coach-consent-revoke" label={copy.revoke} variant="outline" loading={chat.busy} onPress={async () => { if (await chat.consent(false)) setDialog(null); }} />
    </CoachDialog>
  </KeyboardAvoidingView>;
}