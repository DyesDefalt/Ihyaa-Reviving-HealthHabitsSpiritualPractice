import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { supabase } from '@/lib/supabase';
import { format, subDays } from 'date-fns';
import { Flame, Trophy, Target, TrendingUp, Star, Heart, Brain, Salad, BookOpen } from 'lucide-react';
import { useI18n } from '@/lib/i18n';

interface CheckinData {
  checkin_date: string;
  mood_rating: number;
  energy_rating: number;
  tasks_completed: number;
  tasks_total: number;
}

interface PillarStats {
  pillar: string;
  completed: number;
  total: number;
}

export default function ProgressPage() {
  const { user, profile } = useAuth();
  const [checkins, setCheckins] = useState<CheckinData[]>([]);
  const [pillarStats, setPillarStats] = useState<PillarStats[]>([]);
  const [totalCompleted, setTotalCompleted] = useState(0);
  const [totalTasks, setTotalTasks] = useState(0);
  const { t, isRTL } = useI18n();

  useEffect(() => {
    if (user) loadStats();
  }, [user]);

  async function loadStats() {
    if (!user) return;

    const [checkinsRes, tasksRes] = await Promise.all([
      supabase
        .from('daily_checkins')
        .select('checkin_date, mood_rating, energy_rating, tasks_completed, tasks_total')
        .eq('user_id', user.id)
        .order('checkin_date', { ascending: false })
        .limit(30),
      supabase
        .from('daily_tasks')
        .select('pillar, completed')
        .eq('user_id', user.id),
    ]);

    setCheckins(checkinsRes.data ?? []);

    const tasks = tasksRes.data ?? [];
    const pillarMap: Record<string, { completed: number; total: number }> = {};
    let done = 0;
    tasks.forEach(t => {
      if (!pillarMap[t.pillar]) pillarMap[t.pillar] = { completed: 0, total: 0 };
      pillarMap[t.pillar].total++;
      if (t.completed) {
        pillarMap[t.pillar].completed++;
        done++;
      }
    });

    setTotalCompleted(done);
    setTotalTasks(tasks.length);
    setPillarStats(Object.entries(pillarMap).map(([pillar, stats]) => ({ pillar, ...stats })));
  }

  const pillarIcons: Record<string, { icon: typeof Heart; color: string; bg: string }> = {
    physical: { icon: Heart, color: 'text-rose-500', bg: 'bg-rose-50' },
    nutrition: { icon: Salad, color: 'text-amber-500', bg: 'bg-amber-50' },
    mental: { icon: Brain, color: 'text-sky-500', bg: 'bg-sky-50' },
    spiritual: { icon: BookOpen, color: 'text-emerald-500', bg: 'bg-emerald-50' },
  };

  const last7Days = Array.from({ length: 7 }, (_, i) => {
    const date = subDays(new Date(), 6 - i);
    const dateStr = format(date, 'yyyy-MM-dd');
    const checkin = checkins.find(c => c.checkin_date === dateStr);
    return {
      day: format(date, 'EEE'),
      mood: checkin?.mood_rating ?? 0,
      energy: checkin?.energy_rating ?? 0,
      completion: checkin && checkin.tasks_total > 0 ? (checkin.tasks_completed / checkin.tasks_total) * 100 : 0,
    };
  });

  return (
    <div className="max-w-lg mx-auto" dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Header */}
      <div className="px-6 pt-12 pb-6">
        <h1 className="text-2xl font-bold text-gray-900">{t('progress.title')}</h1>
        <p className="text-gray-500 text-sm">{t('progress.subtitle')}</p>
      </div>

      {/* Stats cards */}
      <div className="px-6 mb-6">
        <div className="grid grid-cols-3 gap-3">
          <div className="bg-white rounded-2xl border border-gray-100 p-4 text-center">
            <Flame className="w-6 h-6 text-orange-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-gray-900">{profile?.current_streak ?? 0}</p>
            <p className="text-xs text-gray-500">{t('progress.streak')}</p>
          </div>
          <div className="bg-white rounded-2xl border border-gray-100 p-4 text-center">
            <Trophy className="w-6 h-6 text-amber-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-gray-900">{profile?.longest_streak ?? 0}</p>
            <p className="text-xs text-gray-500">{t('progress.best_streak')}</p>
          </div>
          <div className="bg-white rounded-2xl border border-gray-100 p-4 text-center">
            <Star className="w-6 h-6 text-emerald-500 mx-auto mb-2" />
            <p className="text-2xl font-bold text-gray-900">{profile?.points_balance ?? 0}</p>
            <p className="text-xs text-gray-500">{t('progress.points')}</p>
          </div>
        </div>
      </div>

      {/* Overall completion */}
      <div className="px-6 mb-6">
        <div className="bg-white rounded-2xl border border-gray-100 p-5">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold text-gray-900">{t('progress.overall')}</h3>
            <span className="text-emerald-600 font-bold text-lg">
              {totalTasks > 0 ? Math.round((totalCompleted / totalTasks) * 100) : 0}%
            </span>
          </div>
          <div className="h-3 bg-gray-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-emerald-500 to-teal-500 rounded-full transition-all"
              style={{ width: `${totalTasks > 0 ? (totalCompleted / totalTasks) * 100 : 0}%` }}
            />
          </div>
          <p className="text-xs text-gray-400 mt-2">{totalCompleted} of {totalTasks} tasks completed</p>
        </div>
      </div>

      {/* Pillar breakdown */}
      <div className="px-6 mb-6">
        <h3 className="font-semibold text-gray-900 mb-3">{t('progress.pillar_breakdown')}</h3>
        <div className="space-y-3">
          {pillarStats.map(stat => {
            const config = pillarIcons[stat.pillar] || pillarIcons.spiritual;
            const Icon = config.icon;
            const pct = stat.total > 0 ? (stat.completed / stat.total) * 100 : 0;

            return (
              <div key={stat.pillar} className="bg-white rounded-2xl border border-gray-100 p-4">
                <div className="flex items-center gap-3 mb-3">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${config.bg}`}>
                    <Icon className={`w-5 h-5 ${config.color}`} />
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{t('pillar.' + stat.pillar)}</p>
                    <p className="text-xs text-gray-400">{stat.completed}/{stat.total} tasks</p>
                  </div>
                  <span className={`text-sm font-bold ${config.color}`}>{Math.round(pct)}%</span>
                </div>
                <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div className={`h-full rounded-full transition-all ${
                    stat.pillar === 'physical' ? 'bg-rose-400' :
                    stat.pillar === 'nutrition' ? 'bg-amber-400' :
                    stat.pillar === 'mental' ? 'bg-sky-400' :
                    'bg-emerald-400'
                  }`} style={{ width: `${pct}%` }} />
                </div>
              </div>
            );
          })}
          {pillarStats.length === 0 && (
            <div className="bg-white rounded-2xl border border-gray-100 p-8 text-center">
              <Target className="w-8 h-8 text-gray-300 mx-auto mb-2" />
              <p className="text-gray-400 text-sm">{t('progress.start_to_see')}</p>
            </div>
          )}
        </div>
      </div>

      {/* Weekly mood chart */}
      <div className="px-6 pb-6">
        <h3 className="font-semibold text-gray-900 mb-3">{t('progress.last_7')}</h3>
        <div className="bg-white rounded-2xl border border-gray-100 p-5">
          <div className="flex items-end justify-between gap-2">
            {last7Days.map((day, i) => (
              <div key={i} className="flex-1 flex flex-col items-center gap-2">
                <div className="w-full flex flex-col items-center gap-1">
                  <div
                    className="w-full max-w-[32px] bg-emerald-100 rounded-lg transition-all"
                    style={{ height: `${Math.max(4, day.completion * 0.6)}px` }}
                  >
                    <div
                      className="w-full bg-emerald-500 rounded-lg"
                      style={{ height: `${day.completion}%` }}
                    />
                  </div>
                </div>
                <span className="text-xs text-gray-400">{day.day}</span>
              </div>
            ))}
          </div>
          <div className="flex items-center gap-2 mt-3 pt-3 border-t border-gray-50">
            <TrendingUp className="w-4 h-4 text-emerald-500" />
            <span className="text-xs text-gray-500">{t('progress.completion_rate')}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
