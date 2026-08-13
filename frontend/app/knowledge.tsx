import Feather from '@expo/vector-icons/Feather';
import { router } from 'expo-router';
import React, { useEffect, useState } from 'react';
import { Platform, Pressable, ScrollView, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { api } from '../src/api';
import { Card, Chip, Loader, Txt, useFonts } from '../src/components/ui';
import { useI18n } from '../src/i18n';
import { pillarColor, radii, space, useTheme } from '../src/theme';

const FILTERS = ['all', 'spiritual', 'physical', 'nutrition', 'mental'];

function Evidence({ label, text, tint }: { label: string; text: string; tint: string }) {
  const { c } = useTheme();
  const { align, lang } = useI18n();
  const f = useFonts();
  return (
    <View style={{ backgroundColor: c.surfaceAlt, borderRadius: radii.sm, padding: 12, gap: 4, borderStartWidth: 3, borderStartColor: tint }}>
      <Text style={{ fontFamily: f.semibold, fontSize: 10.5, letterSpacing: 0.6, color: tint, textAlign: align, textTransform: 'uppercase' }}>
        {label}
      </Text>
      <Text
        style={{
          fontFamily: lang === 'ar' ? 'Amiri_400Regular' : f.regular,
          fontSize: lang === 'ar' ? 16 : 13,
          lineHeight: lang === 'ar' ? 27 : 20,
          color: c.textDim,
          textAlign: align,
        }}
      >
        {text}
      </Text>
    </View>
  );
}

export default function Knowledge() {
  const { c, mode } = useTheme();
  const { t, lang, row, align } = useI18n();
  const insets = useSafeAreaInsets();
  const f = useFonts();

  const [cards, setCards] = useState<any[] | null>(null);
  const [filter, setFilter] = useState('all');
  const [open, setOpen] = useState<string | null>(null);

  useEffect(() => {
    api(`/knowledge?lang=${lang}`)
      .then(setCards)
      .catch(() => setCards([]));
  }, [lang]);

  if (!cards) return <Loader testID="knowledge-loading" />;

  const shown = filter === 'all' ? cards : cards.filter((x) => x.pillar === filter);

  return (
    <ScrollView
      testID="knowledge-screen"
      style={{ flex: 1, backgroundColor: c.background }}
      contentContainerStyle={{ paddingTop: insets.top + space.md, paddingBottom: insets.bottom + space.xxl, gap: space.md }}
      showsVerticalScrollIndicator={false}
    >
      <View style={{ paddingHorizontal: space.lg, flexDirection: row, alignItems: 'center', gap: space.md }}>
        <Pressable
          testID="knowledge-back"
          onPress={() => router.back()}
          style={{
            width: 38,
            height: 38,
            borderRadius: radii.full,
            backgroundColor: c.surface,
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
          <Txt variant="h3" weight="bold">{t('know.title')}</Txt>
          <Txt variant="caption" color={c.textDim}>{t('know.subtitle')}</Txt>
        </View>
      </View>

      <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={{ paddingHorizontal: space.lg, gap: space.sm }}>
        {FILTERS.map((v) => (
          <Chip
            key={v}
            testID={`know-filter-${v}`}
            label={v === 'all' ? t('know.all') : t(`pillar.${v}`)}
            active={filter === v}
            onPress={() => setFilter(v)}
            color={v === 'all' ? undefined : pillarColor[v]}
          />
        ))}
      </ScrollView>

      <View style={{ paddingHorizontal: space.lg, gap: space.sm }}>
        {shown.length === 0 ? (
          <Card><Txt variant="small" color={c.textDim}>{t('know.none')}</Txt></Card>
        ) : (
          shown.map((card) => {
            const tint = pillarColor[card.pillar] ?? c.primary;
            const isOpen = open === card.id;
            return (
              <Card key={card.id} testID={`know-card-${card.id}`} style={{ gap: space.sm }}>
                <Pressable
                  testID={`know-toggle-${card.id}`}
                  onPress={() => setOpen(isOpen ? null : card.id)}
                  style={{ flexDirection: row, gap: space.md, alignItems: 'flex-start', ...(Platform.OS === 'web' ? ({ cursor: 'pointer' } as any) : {}) }}
                >
                  <View style={{ width: 38, height: 38, borderRadius: radii.sm, backgroundColor: tint + '1A', alignItems: 'center', justifyContent: 'center' }}>
                    <Feather name="book-open" size={17} color={tint} />
                  </View>
                  <View style={{ flex: 1, gap: 3 }}>
                    <Text style={{ fontFamily: f.medium, fontSize: 10, letterSpacing: 0.8, color: tint, textTransform: 'uppercase', textAlign: align }}>
                      {card.category}
                    </Text>
                    <Text style={{ fontFamily: f.semibold, fontSize: 16, lineHeight: 23, color: c.text, textAlign: align }}>
                      {card.title}
                    </Text>
                    {!isOpen ? (
                      <Text numberOfLines={2} style={{ fontFamily: f.regular, fontSize: 13, color: c.textDim, textAlign: align }}>
                        {card.content}
                      </Text>
                    ) : null}
                  </View>
                  <Feather name={isOpen ? 'chevron-up' : 'chevron-down'} size={17} color={c.textDim} />
                </Pressable>

                {isOpen ? (
                  <View style={{ gap: space.sm }}>
                    <Text style={{ fontFamily: f.regular, fontSize: 14, lineHeight: 23, color: c.text, textAlign: align }}>
                      {card.content}
                    </Text>
                    {card.quran_verse ? <Evidence label={t('ref.quran')} text={card.quran_verse} tint={c.success} /> : null}
                    {card.hadith_text ? <Evidence label={t('ref.hadith')} text={card.hadith_text} tint={c.secondary} /> : null}
                    {card.scientific_fact ? <Evidence label={t('ref.science')} text={card.scientific_fact} tint="#4A6FA5" /> : null}
                  </View>
                ) : null}
              </Card>
            );
          })
        )}
      </View>
    </ScrollView>
  );
}
