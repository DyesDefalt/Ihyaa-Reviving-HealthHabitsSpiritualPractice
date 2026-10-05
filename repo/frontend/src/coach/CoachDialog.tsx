import Feather from '@expo/vector-icons/Feather';
import React from 'react';
import { Modal, Pressable, ScrollView, View } from 'react-native';
import { Txt } from '../components/ui';
import { useTheme, space } from '../theme';
import { useI18n } from '../i18n';
import { coachCopy } from './copy';

export const CoachDialog = ({ visible, title, onClose, children, id }: {
  visible: boolean; title: string; onClose: () => void; children: React.ReactNode; id: string;
}) => {
  const { c } = useTheme();
  const { lang } = useI18n();
  return <Modal visible={visible} transparent animationType="fade" onRequestClose={onClose}>
    <View testID={id} style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.4)', justifyContent: 'center', alignItems: 'center' }}>
      <View style={{ width: '90%', maxWidth: 420, maxHeight: '80%', backgroundColor: c.surface, borderRadius: 16, padding: space.lg, gap: space.md }}>
        <View style={{ flexDirection: 'row', alignItems: 'center', gap: 12 }}>
          <Txt testID={`${id}-title`} weight="semibold" style={{ flex: 1 }}>{title}</Txt>
          <Pressable testID={`${id}-close`} accessibilityRole="button" accessibilityLabel={coachCopy(lang).close} onPress={onClose}
            style={({ pressed }) => ({ padding: 8, opacity: pressed ? 0.5 : 1 })}>
            <Feather name="x" size={20} color={c.text} />
          </Pressable>
        </View>
        <ScrollView contentContainerStyle={{ gap: 12 }} showsVerticalScrollIndicator={false}>{children}</ScrollView>
      </View>
    </View>
  </Modal>;
};