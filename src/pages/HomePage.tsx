import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useI18n } from '@/lib/i18n';
import { supabase } from '@/lib/supabase';
import { generateChallengeTasks } from '@/lib/challengeGenerator';
import { format, isToday } from 'date-fns';
import { Flame, Star, CheckCircle2, Circle, ChevronRight, BookOpen, Sparkles, Play, Trophy, Zap } from 'lucide-react';

interface DailyTask {
  id: string;
  title: string;
  description: string;
  pillar: string;
  duration_minutes: number;
  points_reward: number;
  completed: boolean;
  quran_reference: string | null;
  hadith_reference: string | null;
  scientific_reference: string | null;
}

interface Challenge {
  id: string;
  challenge_type: string;
  current_day: number;
  start_date: string;
  end_date: string;
  status: string;
}

interface KnowledgeCard {
  id: string;
  title: string;
  content: string;
  quran_verse: string | null;
  hadith_text: string | null;
  pillar: string;
}

const pillarColors: Record<string, { bg: string; text: string; icon: string; labelKey: string }> = {
  physical: { bg: 'bg-rose-50', text: 'text-rose-600', icon: '💪', labelKey: 'pillar.physical' },
  nutrition: { bg: 'bg-amber-50', text: 'text-amber-600', icon: '🥗', labelKey: 'pillar.nutrition' },
  mental: { bg: 'bg-sky-50', text: 'text-sky-600', icon: '🧠', labelKey: 'pillar.mental' },
  spiritual: { bg: 'bg-emerald-50', text: 'text-emerald-600', icon: '🕌', labelKey: 'pillar.spiritual' },
};

function IslamicGeometricPattern() {
  return (
    <svg
      className="absolute inset-0 w-full h-full pointer-events-none"
      xmlns="http://www.w3.org/2000/svg"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
    >
      <defs>
        <pattern
          id="islamic-geo"
          x="0"
          y="0"
          width="60"
          height="60"
          patternUnits="userSpaceOnUse"
        >
          {/* Central octagon */}
          <polygon
            points="20,5 40,5 50,15 50,35 45,45 35,50 25,50 15,45 10,35 10,15"
            fill="none"
            stroke="white"
            strokeWidth="0.5"
            opacity="0.12"
          />
          {/* Inner star – 8-pointed */}
          <polygon
            points="30,8 34,22 48,18 38,28 48,38 34,34 30,48 26,34 12,38 22,28 12,18 26,22"
            fill="none"
            stroke="white"
            strokeWidth="0.4"
            opacity="0.10"
          />
          {/* Diamond accents */}
          <polygon
            points="30,0 35,5 30,10 25,5"
            fill="none"
            stroke="white"
            strokeWidth="0.4"
            opacity="0.08"
          />
          <polygon
            points="0,30 5,25 10,30 5,35"
            fill="none"
            stroke="white"
            strokeWidth="0.4"
            opacity="0.08"
          />
          <polygon
            points="60,30 55,25 50,30 55,35"
            fill="none"
            stroke="white"
            strokeWidth="0.4"
            opacity="0.08"
          />
          <polygon
            points="30,60 35,55 30,50 25,55"
            fill="none"
            stroke="white"
            strokeWidth="0.4"
            opacity="0.08"
          />
          {/* Cross-hatch geometric lines */}
          <line x1="10" y1="10" x2="20" y2="5" stroke="white" strokeWidth="0.3" opacity="0.07" />
          <line x1="50" y1="10" x2="40" y2="5" stroke="white" strokeWidth="0.3" opacity="0.07" />
          <line x1="10" y1="40" x2="15" y2="50" stroke="white" strokeWidth="0.3" opacity="0.07" />
          <line x1="50" y1="40" x2="45" y2="50" stroke="white" strokeWidth="0.3" opacity="0.07" />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#islamic-geo)" />
    </svg>
  );
}

export default function HomePage({ onNavigate }: { onNavigate: (tab: string) => void }) {
  const { user, profile, refreshProfile } = useAuth();
  const { t, dir, isRTL } = useI18n();
  const [tasks, setTasks] = useState<DailyTask[]>([]);
  const [challenge, setChallenge] = useState<Challenge | null>(null);
  const [knowledgeCard, setKnowledgeCard] = useState<KnowledgeCard | null>(null);
  const [expandedTask, setExpandedTask] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    if (user) loadData();
  }, [user]);

  async function loadData() {
    setLoading(true);
    await Promise.all([loadChallenge(), loadKnowledgeCard()]);
    setLoading(false);
  }

  async function loadChallenge() {
    if (!user) return;
    const { data: challenges } = await supabase
      .from('challenges')
      .select('*')
      .eq('user_id', user.id)
      .eq('status', 'active')
      .order('created_at', { ascending: false })
      .limit(1);

    if (challenges && challenges.length > 0) {
      setChallenge(challenges[0]);
      await loadTodayTasks(challenges[0].id);
    }
  }

  async function loadTodayTasks(challengeId: string) {
    if (!user) return;
    const today = format(new Date(), 'yyyy-MM-dd');
    const { data } = await supabase
      .from('daily_tasks')
      .select('*')
      .eq('challenge_id', challengeId)
      .eq('scheduled_date', today)
      .order('pillar');
    setTasks(data ?? []);
  }

  async function loadKnowledgeCard() {
    const { data } = await supabase
      .from('knowledge_cards')
      .select('*')
      .limit(8);
    if (data && data.length > 0) {
      const idx = new Date().getDay() % data.length;
      setKnowledgeCard(data[idx]);
    }
  }

  async function startChallenge() {
    if (!user || !profile) return;
    setStarting(true);

    const challengeType = profile.preferred_challenge;
    const days = challengeType === '30_days' ? 30 : challengeType === '100_days' ? 100 : 365;
    const startDate = new Date();
    const endDate = new Date(startDate);
    endDate.setDate(endDate.getDate() + days);

    const { data: newChallenge, error } = await supabase
      .from('challenges')
      .insert({
        challenge_type: challengeType,
        start_date: format(startDate, 'yyyy-MM-dd'),
        end_date: format(endDate, 'yyyy-MM-dd'),
        current_day: 1,
      })
      .select()
      .single();

    if (error || !newChallenge) {
      setStarting(false);
      return;
    }

    const generatedTasks = generateChallengeTasks(
      newChallenge.id,
      challengeType,
      startDate,
      profile.fitness_level,
      profile.spiritual_level
    );

    const batchSize = 100;
    for (let i = 0; i < generatedTasks.length; i += batchSize) {
      await supabase.from('daily_tasks').insert(generatedTasks.slice(i, i + batchSize));
    }

    setChallenge(newChallenge);
    await loadTodayTasks(newChallenge.id);
    setStarting(false);
  }

  async function toggleTask(taskId: string, completed: boolean) {
    if (!user || !challenge) return;

    const now = new Date().toISOString();
    await supabase
      .from('daily_tasks')
      .update({
        completed: !completed,
        completed_at: !completed ? now : null,
      })
      .eq('id', taskId);

    if (!completed) {
      const task = tasks.find(t => t.id === taskId);
      if (task) {
        await supabase.from('point_transactions').insert({
          amount: task.points_reward,
          type: 'earned',
          source: 'task_complete',
          description: `Completed: ${task.title}`,
        });
        await supabase
          .from('profiles')
          .update({ points_balance: (profile?.points_balance ?? 0) + task.points_reward })
          .eq('id', user.id);
        await refreshProfile();
      }
    }

    setTasks(prev =>
      prev.map(t => t.id === taskId ? { ...t, completed: !completed } : t)
    );
  }

  const completedCount = tasks.filter(t => t.completed).length;
  const totalCount = tasks.length;
  const progress = totalCount > 0 ? (completedCount / totalCount) * 100 : 0;

  const chevronClass = isRTL ? 'rotate-180' : '';

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="w-8 h-8 border-3 border-emerald-200 border-t-emerald-600 rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-lg mx-auto" dir={dir}>
      {/* Header with Islamic geometric pattern */}
      <div className="bg-gradient-to-br from-emerald-600 to-teal-700 px-6 pt-12 pb-8 rounded-b-3xl relative overflow-hidden">
        <IslamicGeometricPattern />

        <div className="relative z-10">
          <div className="flex items-center justify-between mb-6">
            <div>
              <p className="text-emerald-100 text-sm">{t('home.greeting')}</p>
              <h1 className="text-white text-xl font-bold">{profile?.display_name || 'Friend'}</h1>
            </div>
            <div className={`flex items-center gap-3 ${isRTL ? 'flex-row-reverse' : ''}`}>
              <div className="flex items-center gap-1.5 bg-white/15 backdrop-blur-sm rounded-full px-3 py-1.5">
                <Flame className="w-4 h-4 text-orange-300" />
                <span className="text-white text-sm font-semibold">{profile?.current_streak ?? 0}</span>
              </div>
              <div className="flex items-center gap-1.5 bg-white/15 backdrop-blur-sm rounded-full px-3 py-1.5">
                <Star className="w-4 h-4 text-amber-300" />
                <span className="text-white text-sm font-semibold">{profile?.points_balance ?? 0}</span>
              </div>
            </div>
          </div>

          {challenge && (
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-4">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <p className="text-emerald-100 text-xs">
                    {t('home.day_of')
                      .replace('{day}', String(challenge.current_day))
                      .replace('{type}', challenge.challenge_type.replace('_', ' '))}
                  </p>
                  <p className="text-white font-semibold">{format(new Date(), 'EEEE, MMMM d')}</p>
                </div>
                <div className={isRTL ? 'text-left' : 'text-right'}>
                  <p className="text-white text-lg font-bold">{completedCount}/{totalCount}</p>
                  <p className="text-emerald-200 text-xs">{t('home.tasks_done')}</p>
                </div>
              </div>
              <div className="h-2 bg-white/20 rounded-full overflow-hidden">
                <div
                  className={`h-full bg-gradient-to-r from-amber-400 to-amber-300 rounded-full transition-all duration-500 ${isRTL ? 'ms-auto' : ''}`}
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          )}
        </div>
      </div>

      {/* No challenge state */}
      {!challenge && (
        <div className="px-6 py-8">
          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 text-center">
            <div className="w-16 h-16 bg-emerald-50 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <Play className="w-8 h-8 text-emerald-600" />
            </div>
            <h2 className="text-lg font-bold text-gray-900 mb-2">{t('home.ready')}</h2>
            <p className="text-gray-500 text-sm mb-6">
              {t('home.ready.desc').replace('{type}', profile?.preferred_challenge?.replace('_', ' ') ?? '30 day')}
            </p>
            <button
              onClick={startChallenge}
              disabled={starting}
              className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-3.5 rounded-xl transition-all shadow-lg shadow-emerald-600/25 flex items-center justify-center gap-2"
            >
              {starting ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  {t('home.start_challenge')}
                  <Sparkles className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Today's Tasks */}
      {challenge && (
        <div className="px-6 py-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-gray-900">{t('home.today_tasks')}</h2>
            {completedCount === totalCount && totalCount > 0 && (
              <div className="flex items-center gap-1 text-emerald-600 text-sm font-medium">
                <Trophy className="w-4 h-4" />
                {t('home.all_done')}
              </div>
            )}
          </div>

          <div className="space-y-3">
            {tasks.map(task => {
              const colors = pillarColors[task.pillar] || pillarColors.spiritual;
              const isExpanded = expandedTask === task.id;

              return (
                <div
                  key={task.id}
                  className={`bg-white rounded-2xl border transition-all ${
                    task.completed ? 'border-emerald-200 bg-emerald-50/50' : 'border-gray-100'
                  }`}
                >
                  <div className="p-4">
                    <div className="flex items-start gap-3">
                      <button
                        onClick={() => toggleTask(task.id, task.completed)}
                        className="mt-0.5 shrink-0"
                      >
                        {task.completed ? (
                          <CheckCircle2 className="w-6 h-6 text-emerald-500" />
                        ) : (
                          <Circle className="w-6 h-6 text-gray-300" />
                        )}
                      </button>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium ${colors.bg} ${colors.text}`}>
                            {colors.icon} {t(colors.labelKey)}
                          </span>
                          <span className="text-xs text-gray-400">{task.duration_minutes} {t('home.min')}</span>
                        </div>
                        <p className={`font-medium ${task.completed ? 'text-gray-400 line-through' : 'text-gray-900'}`}>
                          {task.title}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                          <Zap className="w-3 h-3 text-amber-500" />
                          <span className="text-xs text-gray-400">+{task.points_reward} {t('home.points')}</span>
                        </div>
                      </div>
                      <button
                        onClick={() => setExpandedTask(isExpanded ? null : task.id)}
                        className="shrink-0 text-gray-400 hover:text-gray-600"
                      >
                        <ChevronRight className={`w-5 h-5 transition-transform ${isExpanded ? 'rotate-90' : chevronClass}`} />
                      </button>
                    </div>
                  </div>

                  {isExpanded && (
                    <div className="px-4 pb-4 pt-0 border-t border-gray-50">
                      <p className="text-sm text-gray-600 mb-3 mt-3">{task.description}</p>
                      {task.quran_reference && (
                        <div className="bg-emerald-50 rounded-xl p-3 mb-2">
                          <p className="text-xs font-medium text-emerald-700 mb-1">{t('ref.quran')}</p>
                          <p className="text-xs text-emerald-600 italic">{task.quran_reference}</p>
                        </div>
                      )}
                      {task.hadith_reference && (
                        <div className="bg-amber-50 rounded-xl p-3 mb-2">
                          <p className="text-xs font-medium text-amber-700 mb-1">{t('ref.hadith')}</p>
                          <p className="text-xs text-amber-600 italic">{task.hadith_reference}</p>
                        </div>
                      )}
                      {task.scientific_reference && (
                        <div className="bg-sky-50 rounded-xl p-3">
                          <p className="text-xs font-medium text-sky-700 mb-1">{t('ref.science')}</p>
                          <p className="text-xs text-sky-600">{task.scientific_reference}</p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {tasks.length === 0 && (
            <div className="text-center py-8 text-gray-400">
              <p className="text-sm">{t('home.no_tasks')}</p>
            </div>
          )}
        </div>
      )}

      {/* Daily Check-in CTA */}
      {challenge && (
        <div className="px-6 pb-6">
          <button
            onClick={() => onNavigate('checkin')}
            className={`w-full bg-gradient-to-r from-teal-500 to-emerald-600 rounded-2xl p-5 text-white flex items-center gap-4 shadow-lg shadow-emerald-600/20 hover:shadow-xl transition-all ${isRTL ? 'text-right' : 'text-left'}`}
          >
            <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center shrink-0">
              <Sparkles className="w-6 h-6" />
            </div>
            <div className="flex-1">
              <p className="font-bold">{t('home.checkin')}</p>
              <p className="text-emerald-100 text-sm">{t('home.checkin.desc')}</p>
            </div>
            <ChevronRight className={`w-5 h-5 text-emerald-200 ${chevronClass}`} />
          </button>
        </div>
      )}

      {/* Knowledge Card */}
      {knowledgeCard && (
        <div className="px-6 pb-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-gray-900">{t('home.wisdom')}</h2>
            <button onClick={() => onNavigate('knowledge')} className="text-emerald-600 text-sm font-medium flex items-center gap-1">
              {t('home.see_all')} <ChevronRight className={`w-4 h-4 ${chevronClass}`} />
            </button>
          </div>
          <div className="bg-gradient-to-br from-emerald-600 to-teal-700 rounded-2xl p-5 text-white">
            <div className="flex items-center gap-2 mb-3">
              <BookOpen className="w-4 h-4 text-emerald-200" />
              <span className="text-emerald-200 text-xs font-medium uppercase tracking-wide">
                {t(`pillar.${knowledgeCard.pillar}`)}
              </span>
            </div>
            <h3 className="font-bold text-lg mb-2">{knowledgeCard.title}</h3>
            {knowledgeCard.quran_verse && (
              <p className="text-emerald-100 text-sm italic mb-3">"{knowledgeCard.quran_verse}"</p>
            )}
            <p className="text-emerald-50/90 text-sm leading-relaxed line-clamp-3">{knowledgeCard.content}</p>
          </div>
        </div>
      )}
    </div>
  );
}
