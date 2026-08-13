import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { ArrowLeft, BookOpen, FlaskConical, Search } from 'lucide-react';
import { useI18n } from '@/lib/i18n';

interface KnowledgeCard {
  id: string;
  title: string;
  content: string;
  quran_verse: string | null;
  hadith_text: string | null;
  scientific_fact: string | null;
  category: string;
  pillar: string;
}

export default function KnowledgePage({ onBack }: { onBack: () => void }) {
  const [cards, setCards] = useState<KnowledgeCard[]>([]);
  const [filter, setFilter] = useState('all');
  const [expandedCard, setExpandedCard] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const { t, isRTL } = useI18n();

  const pillarFilters = [
    { value: 'all', label: t('knowledge.filter.all') },
    { value: 'physical', label: t('pillar.physical') },
    { value: 'nutrition', label: t('pillar.nutrition') },
    { value: 'mental', label: t('pillar.mental') },
    { value: 'spiritual', label: t('pillar.spiritual') },
  ];

  useEffect(() => {
    loadCards();
  }, []);

  async function loadCards() {
    setLoading(true);
    const { data } = await supabase
      .from('knowledge_cards')
      .select('*')
      .order('created_at', { ascending: false });
    setCards(data ?? []);
    setLoading(false);
  }

  const filtered = filter === 'all' ? cards : cards.filter(c => c.pillar === filter);

  return (
    <div className="max-w-lg mx-auto min-h-screen bg-gray-50" dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Header */}
      <div className="bg-white px-6 pt-6 pb-4 border-b border-gray-100">
        <div className="flex items-center gap-3 mb-4">
          <button onClick={onBack} className="p-2 hover:bg-gray-100 rounded-xl">
            <ArrowLeft className="w-5 h-5 text-gray-600" />
          </button>
          <div>
            <h1 className="text-xl font-bold text-gray-900">{t('knowledge.title')}</h1>
            <p className="text-sm text-gray-500">{t('knowledge.subtitle')}</p>
          </div>
        </div>

        {/* Filters */}
        <div className="flex gap-2 overflow-x-auto pb-1 -mx-1 px-1">
          {pillarFilters.map(f => (
            <button
              key={f.value}
              onClick={() => setFilter(f.value)}
              className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all ${
                filter === f.value
                  ? 'bg-emerald-600 text-white shadow-sm'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      {/* Cards */}
      <div className="px-6 py-6 space-y-4">
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="w-6 h-6 border-2 border-emerald-200 border-t-emerald-600 rounded-full animate-spin" />
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-12">
            <Search className="w-8 h-8 text-gray-300 mx-auto mb-2" />
            <p className="text-gray-400 text-sm">{t('knowledge.no_cards')}</p>
          </div>
        ) : (
          filtered.map(card => {
            const expanded = expandedCard === card.id;
            return (
              <div
                key={card.id}
                className="bg-white rounded-2xl border border-gray-100 overflow-hidden transition-all"
              >
                <button
                  onClick={() => setExpandedCard(expanded ? null : card.id)}
                  className="w-full text-left p-5"
                >
                  <div className="flex items-start gap-3">
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${
                      card.pillar === 'physical' ? 'bg-rose-50 text-rose-500' :
                      card.pillar === 'nutrition' ? 'bg-amber-50 text-amber-500' :
                      card.pillar === 'mental' ? 'bg-sky-50 text-sky-500' :
                      'bg-emerald-50 text-emerald-500'
                    }`}>
                      <BookOpen className="w-5 h-5" />
                    </div>
                    <div className="flex-1">
                      <span className={`text-xs font-medium uppercase tracking-wide ${
                        card.pillar === 'physical' ? 'text-rose-500' :
                        card.pillar === 'nutrition' ? 'text-amber-500' :
                        card.pillar === 'mental' ? 'text-sky-500' :
                        'text-emerald-500'
                      }`}>
                        {card.category.replace(/_/g, ' ')}
                      </span>
                      <h3 className="font-semibold text-gray-900 mt-0.5">{card.title}</h3>
                      {!expanded && (
                        <p className="text-sm text-gray-500 mt-1 line-clamp-2">{card.content}</p>
                      )}
                    </div>
                  </div>
                </button>

                {expanded && (
                  <div className="px-5 pb-5 space-y-3">
                    <p className="text-sm text-gray-700 leading-relaxed">{card.content}</p>

                    {card.quran_verse && (
                      <div className="bg-emerald-50 rounded-xl p-4 border border-emerald-100">
                        <div className="flex items-center gap-2 mb-2">
                          <BookOpen className="w-4 h-4 text-emerald-600" />
                          <p className="text-xs font-semibold text-emerald-700 uppercase tracking-wide">{t('knowledge.source.quran')}</p>
                        </div>
                        <p className="text-sm text-emerald-800 italic leading-relaxed">{card.quran_verse}</p>
                      </div>
                    )}

                    {card.hadith_text && (
                      <div className="bg-amber-50 rounded-xl p-4 border border-amber-100">
                        <div className="flex items-center gap-2 mb-2">
                          <BookOpen className="w-4 h-4 text-amber-600" />
                          <p className="text-xs font-semibold text-amber-700 uppercase tracking-wide">{t('knowledge.source.hadith')}</p>
                        </div>
                        <p className="text-sm text-amber-800 italic leading-relaxed">{card.hadith_text}</p>
                      </div>
                    )}

                    {card.scientific_fact && (
                      <div className="bg-sky-50 rounded-xl p-4 border border-sky-100">
                        <div className="flex items-center gap-2 mb-2">
                          <FlaskConical className="w-4 h-4 text-sky-600" />
                          <p className="text-xs font-semibold text-sky-700 uppercase tracking-wide">{t('knowledge.source.science')}</p>
                        </div>
                        <p className="text-sm text-sky-800 leading-relaxed">{card.scientific_fact}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
