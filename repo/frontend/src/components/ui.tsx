import Feather from '@expo/vector-icons/Feather';
import React from 'react';
import {
  ActivityIndicator,
  Platform,
  Pressable,
  StyleProp,
  Text,
  TextStyle,
  View,
  ViewStyle,
} from 'react-native';
import { useI18n } from '../i18n';
import { fontsFor, radii, shadow, space, type as ty, useTheme } from '../theme';

export function useFonts() {
  const { lang } = useI18n();
  return fontsFor(lang);
}

export function Txt({
  children,
  variant = 'body',
  weight = 'regular',
  color,
  style,
  testID,
  numberOfLines,
}: {
  children: React.ReactNode;
  variant?: keyof typeof ty;
  weight?: 'regular' | 'medium' | 'semibold' | 'bold' | 'scripture';
  color?: string;
  style?: StyleProp<TextStyle>;
  testID?: string;
  numberOfLines?: number;
}) {
  const { c } = useTheme();
  const { align } = useI18n();
  const f = useFonts();
  return (
    <Text
      testID={testID}
      numberOfLines={numberOfLines}
      style={[
        ty[variant],
        { fontFamily: f[weight], color: color ?? c.text, textAlign: align },
        style,
      ]}
    >
      {children}
    </Text>
  );
}

export function Card({
  children,
  style,
  testID,
  padded = true,
}: {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  testID?: string;
  padded?: boolean;
}) {
  const { c, mode } = useTheme();
  return (
    <View
      testID={testID}
      style={[
        {
          backgroundColor: c.surface,
          borderRadius: radii.md,
          borderWidth: 1,
          borderColor: c.border,
          padding: padded ? space.md : 0,
          ...shadow(mode, 'sm'),
        },
        style,
      ]}
    >
      {children}
    </View>
  );
}

export function Btn({
  label,
  onPress,
  variant = 'primary',
  icon,
  loading,
  disabled,
  style,
  testID,
}: {
  label: string;
  onPress: () => void;
  variant?: 'primary' | 'outline' | 'ghost' | 'accent';
  icon?: keyof typeof Feather.glyphMap;
  loading?: boolean;
  disabled?: boolean;
  style?: StyleProp<ViewStyle>;
  testID?: string;
}) {
  const { c, mode } = useTheme();
  const { row } = useI18n();
  const f = useFonts();
  const bg =
    variant === 'primary' ? c.primary : variant === 'accent' ? c.secondary : 'transparent';
  const fg =
    variant === 'primary' || variant === 'accent' ? c.onPrimary : c.primary;
  const off = disabled || loading;

  return (
    <Pressable
      testID={testID}
      onPress={onPress}
      disabled={off}
      style={({ pressed }) => [
        {
          backgroundColor: bg,
          borderRadius: radii.full,
          borderWidth: variant === 'outline' ? 1.5 : 0,
          borderColor: c.border,
          paddingVertical: 15,
          paddingHorizontal: space.lg,
          flexDirection: row,
          alignItems: 'center',
          justifyContent: 'center',
          gap: space.sm,
          opacity: off ? 0.5 : pressed ? 0.86 : 1,
          transform: [{ scale: pressed && !off ? 0.985 : 1 }],
          ...(variant === 'primary' || variant === 'accent' ? shadow(mode, 'md') : {}),
          ...(Platform.OS === 'web' ? ({ cursor: off ? 'default' : 'pointer', transitionDuration: '140ms' } as any) : {}),
        },
        style,
      ]}
    >
      {loading ? (
        <ActivityIndicator color={fg} size="small" />
      ) : (
        <>
          {icon ? <Feather name={icon} size={17} color={fg} /> : null}
          <Text style={{ color: fg, fontFamily: f.semibold, fontSize: 16 }}>{label}</Text>
        </>
      )}
    </Pressable>
  );
}

export function Chip({
  label,
  active,
  onPress,
  color,
  testID,
}: {
  label: string;
  active?: boolean;
  onPress?: () => void;
  color?: string;
  testID?: string;
}) {
  const { c } = useTheme();
  const f = useFonts();
  const tint = color ?? c.primary;
  return (
    <Pressable
      testID={testID}
      onPress={onPress}
      style={({ pressed }) => ({
        paddingHorizontal: 14,
        paddingVertical: 8,
        borderRadius: radii.full,
        backgroundColor: active ? tint : c.surfaceAlt,
        borderWidth: 1,
        borderColor: active ? tint : c.border,
        opacity: pressed ? 0.85 : 1,
        ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}),
      })}
    >
      <Text
        style={{
          fontFamily: f.medium,
          fontSize: 13,
          color: active ? '#FFFFFF' : c.textDim,
        }}
      >
        {label}
      </Text>
    </Pressable>
  );
}

export function SelectRow({
  title,
  subtitle,
  selected,
  onPress,
  emblem,
  testID,
  badge,
}: {
  title: string;
  subtitle?: string;
  selected?: boolean;
  onPress: () => void;
  emblem?: keyof typeof Feather.glyphMap;
  testID?: string;
  badge?: string;
}) {
  const { c, mode } = useTheme();
  const { row, align } = useI18n();
  const f = useFonts();
  return (
    <Pressable
      testID={testID}
      onPress={onPress}
      style={({ pressed }) => ({
        flexDirection: row,
        alignItems: 'center',
        gap: space.md,
        padding: space.md,
        borderRadius: radii.md,
        borderWidth: 1.5,
        borderColor: selected ? c.primary : c.border,
        backgroundColor: selected ? (mode === 'light' ? '#EDF2F0' : c.surfaceAlt) : c.surface,
        opacity: pressed ? 0.9 : 1,
        ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}),
      })}
    >
      {emblem ? (
        <View
          style={{
            width: 40,
            height: 40,
            borderRadius: radii.sm,
            backgroundColor: selected ? c.primary : c.surfaceAlt,
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Feather name={emblem} size={18} color={selected ? c.onPrimary : c.textDim} />
        </View>
      ) : null}
      <View style={{ flex: 1 }}>
        <Text style={{ fontFamily: f.semibold, fontSize: 16, color: c.text, textAlign: align }}>
          {title}
        </Text>
        {subtitle ? (
          <Text style={{ fontFamily: f.regular, fontSize: 13, color: c.textDim, textAlign: align, marginTop: 2 }}>
            {subtitle}
          </Text>
        ) : null}
      </View>
      {badge ? (
        <View style={{ backgroundColor: c.secondary, paddingHorizontal: 8, paddingVertical: 3, borderRadius: radii.full }}>
          <Text style={{ fontFamily: f.semibold, fontSize: 10, color: '#fff' }}>{badge}</Text>
        </View>
      ) : null}
      {selected ? <Feather name="check" size={20} color={c.primary} /> : null}
    </Pressable>
  );
}

export function Field({
  label,
  value,
  onChangeText,
  placeholder,
  secure,
  keyboardType,
  testID,
  multiline,
}: {
  label: string;
  value: string;
  onChangeText: (v: string) => void;
  placeholder?: string;
  secure?: boolean;
  keyboardType?: 'default' | 'email-address';
  testID?: string;
  multiline?: boolean;
}) {
  const { c } = useTheme();
  const { align } = useI18n();
  const f = useFonts();
  const { TextInput } = require('react-native');
  return (
    <View style={{ gap: 6 }}>
      <Text style={{ fontFamily: f.medium, fontSize: 13, color: c.textDim, textAlign: align }}>
        {label}
      </Text>
      <TextInput
        testID={testID}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor={c.textDim}
        secureTextEntry={secure}
        autoCapitalize={keyboardType === 'email-address' ? 'none' : 'sentences'}
        keyboardType={keyboardType ?? 'default'}
        multiline={multiline}
        style={{
          backgroundColor: c.surface,
          borderWidth: 1.5,
          borderColor: c.border,
          borderRadius: radii.md,
          paddingHorizontal: space.md,
          paddingVertical: 13,
          fontFamily: f.regular,
          fontSize: 16,
          color: c.text,
          textAlign: align,
          minHeight: multiline ? 92 : undefined,
          textAlignVertical: multiline ? 'top' : 'center',
          ...(Platform.OS === 'web' ? ({ outlineStyle: 'none' } as any) : {}),
        }}
      />
    </View>
  );
}

export function Divider() {
  const { c } = useTheme();
  return <View style={{ height: 1, backgroundColor: c.border }} />;
}

export function Loader({ testID }: { testID?: string }) {
  const { c } = useTheme();
  return (
    <View testID={testID} style={{ flex: 1, alignItems: 'center', justifyContent: 'center', padding: space.xl }}>
      <ActivityIndicator color={c.primary} size="large" />
    </View>
  );
}

export function Banner({ text, tone = 'error', testID }: { text: string; tone?: 'error' | 'ok'; testID?: string }) {
  const { c } = useTheme();
  const f = useFonts();
  const { align } = useI18n();
  const bg = tone === 'error' ? 'rgba(231,111,81,0.12)' : 'rgba(42,157,143,0.12)';
  const fg = tone === 'error' ? c.error : c.success;
  return (
    <View testID={testID} style={{ backgroundColor: bg, borderRadius: radii.sm, padding: 12 }}>
      <Text style={{ fontFamily: f.medium, fontSize: 13, color: fg, textAlign: align }}>{text}</Text>
    </View>
  );
}
