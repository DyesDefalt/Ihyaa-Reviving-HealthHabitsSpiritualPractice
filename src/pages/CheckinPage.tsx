import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { supabase } from '@/lib/supabase';
import { format } from 'date-fns';
import { Heart, Zap, Smile, Meh, Frown, ArrowLeft, Sparkles, Check } from 'lucide-react';
import { useI18n } from '@/lib/i18n';

interface CheckinPageProps {
  onBack: () => void;
}

export default function CheckinPage({ onBack }: CheckinPageProps) {
  const { user, profile, refreshProfile } = useAuth();
  const [mood, setMood] = useState(3);
  const [energy, setEnergy] = useState(3);
  const [gratitude, setGratitude] = useState('');
  const [reflection, setReflection] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [alreadyCheckedIn, setAlreadyCheckedIn] = useState(false);
  const { t, isRTL } = useI18n();

  const moodOptions = [
    { value: 1, label: t('checkin.mood.1'), icon: Frown, color: 'text-red-500 bg-red-50 border-red-200' },
    { value: 2, label: t('checkin.mood.2'), icon: Frown, color: 'text-orange-500 bg-orange-50 border-orange-200' },
    { value: 3, label: t('checkin.mood.3'), icon: Meh, color: 'text-amber-500 bg-amber-50 border-amber-200' },
    { value: 4, label: t('checkin.mood.4'), icon: Smile, color: 'text-emerald-500 bg-emerald-50 border-emerald-200' },
    { value: 5, label: t('checkin.mood.5'), icon: Smile, color: 'text-green-500 bg-green-50 border-green-200' },
  ];

  const energyOptions = [
    { value: 1, label: t('checkin.energy.1') },
    { value: 2, label: t('checkin.energy.2') },
    { value: 3, label: t('checkin.energy.3') },
    { value: 4, label: t('checkin.energy.4') },
    { value: 5, label: t('checkin.energy.5') },
  ];

  useEffect(() => {
    checkExisting();
  }, [user]);

  async function checkExisting() {
    if (!user) return;
    const today = format(new Date(), 'yyyy-MM-dd');
    const { data } = await supabase
      .from('daily_checkins')
      .select('id')
      .eq('user_id', user.id)
      .eq('checkin_date', today)
      .limit(1);
    if (data && data.length > 0) setAlreadyCheckedIn(true);
  }

  async function handleSubmit() {
    if (!user) return;
    setSubmitting(true);

    const today = format(new Date(), 'yyyy-MM-dd');

    const { data: challenges } = await supabase
      .from('challenges')
      .select('id')
      .eq('user_id', user.id)
      .eq('status', 'active')
      .limit(1);

    const challengeId = challenges?.[0]?.id;
    if (!challengeId) {
      setSubmitting(false);
      return;
    }

    const { data: todayTasks } = await supabase
      .from('daily_tasks')
      .select('completed')
      .eq('user_id', user.id)
      .eq('scheduled_date', today);

    const tasksCompleted = (todayTasks ?? []).filter(t => t.completed).length;
    const tasksTotal = todayTasks?.length ?? 0;

    const checkinPoints = 15;
    const allDoneBonus = tasksCompleted === tasksTotal && tasksTotal > 0 ? 50 : 0;
    const totalPoints = checkinPoints + allDoneBonus;

    await supabase.from('daily_checkins').upsert({
      user_id: user.id,
      challenge_id: challengeId,
      checkin_date: today,
      mood_rating: mood,
      energy_rating: energy,
      gratitude_note: gratitude || null,
      reflection_note: reflection || null,
      tasks_completed: tasksCompleted,
      tasks_total: tasksTotal,
      points_earned: totalPoints,
    }, { onConflict: 'user_id,challenge_id,checkin_date' });

    await supabase.from('point_transactions').insert({
      amount: totalPoints,
      type: 'earned',
      source: 'checkin',
      description: `Daily check-in${allDoneBonus > 0 ? ' + all tasks bonus' : ''}`,
    });

    const newBalance = (profile?.points_balance ?? 0) + totalPoints;
    const newStreak = (profile?.current_streak ?? 0) + 1;
    const newLongest = Math.max(newStreak, profile?.longest_streak ?? 0);

    await supabase.from('profiles').update({
      points_balance: newBalance,
      current_streak: newStreak,
      longest_streak: newLongest,
    }).eq('id', user.id);

    await refreshProfile();
    setSubmitted(true);
    setSubmitting(false);
  }

  if (submitted) {
    const allDoneBonus = 50;
    return (
      <div dir={isRTL ? 'rtl' : 'ltr'} className="max-w-lg mx-auto min-h-screen flex flex-col items-center justify-center px-6">
        <div className="w-20 h-20 bg-emerald-100 rounded-full flex items-center justify-center mb-6">
          <Check className="w-10 h-10 text-emerald-600" />
        </div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">{t('checkin.done')}</h1>
        <p className="text-gray-500 text-center mb-6">
          {t('checkin.done.desc')}
        </p>
        <div className="bg-amber-50 rounded-2xl p-4 w-full text-center mb-6">
          <p className="text-amber-700 text-sm font-medium">{t('checkin.points_earned')}</p>
          <p className="text-3xl font-bold text-amber-600">+{15 + allDoneBonus}</p>
        </div>
        <button
          onClick={onBack}
          className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-3.5 rounded-xl transition-all"
        >
          {t('checkin.back')}
        </button>
      </div>
    );
  }

  if (alreadyCheckedIn) {
    return (
      <div dir={isRTL ? 'rtl' : 'ltr'} className="max-w-lg mx-auto min-h-screen flex flex-col items-center justify-center px-6">
        <div className="w-20 h-20 bg-emerald-100 rounded-full flex items-center justify-center mb-6">
          <Sparkles className="w-10 h-10 text-emerald-600" />
        </div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">{t('checkin.already')}</h1>
        <p className="text-gray-500 text-center mb-6">{t('checkin.already.desc')}</p>
        <button onClick={onBack} className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-3.5 rounded-xl">
          {t('checkin.back')}
        </button>
      </div>
    );
  }

  return (
    <div dir={isRTL ? 'rtl' : 'ltr'} className="max-w-lg mx-auto min-h-screen bg-white">
      {/* Header */}
      <div className="px-6 pt-6 pb-4 flex items-center gap-3">
        <button onClick={onBack} className="p-2 hover:bg-gray-100 rounded-xl">
          <ArrowLeft className="w-5 h-5 text-gray-600" />
        </button>
        <div>
          <h1 className="text-xl font-bold text-gray-900">{t('checkin.title')}</h1>
          <p className="text-sm text-gray-500">{format(new Date(), 'EEEE, MMMM d')}</p>
        </div>
      </div>

      <div className="px-6 space-y-8 pb-32">
        {/* Mood */}
        <div>
          <div className="flex items-center gap-2 mb-3">
            <Heart className="w-5 h-5 text-rose-500" />
            <h2 className="font-semibold text-gray-900">{t('checkin.mood')}</h2>
          </div>
          <div className="flex gap-2">
            {moodOptions.map(opt => {
              const Icon = opt.icon;
              const selected = mood === opt.value;
              return (
                <button
                  key={opt.value}
                  onClick={() => setMood(opt.value)}
                  className={`flex-1 flex flex-col items-center gap-1 p-3 rounded-xl border-2 transition-all ${
                    selected ? opt.color : 'border-gray-100 bg-white'
                  }`}
                >
                  <Icon className={`w-6 h-6 ${selected ? '' : 'text-gray-300'}`} />
                  <span className={`text-xs font-medium ${selected ? '' : 'text-gray-400'}`}>{opt.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Energy */}
        <div>
          <div className="flex items-center gap-2 mb-3">
            <Zap className="w-5 h-5 text-amber-500" />
            <h2 className="font-semibold text-gray-900">{t('checkin.energy')}</h2>
          </div>
          <div className="flex gap-2">
            {energyOptions.map(opt => {
              const selected = energy === opt.value;
              return (
                <button
                  key={opt.value}
                  onClick={() => setEnergy(opt.value)}
                  className={`flex-1 flex flex-col items-center gap-1 p-3 rounded-xl border-2 transition-all ${
                    selected ? 'border-amber-400 bg-amber-50 text-amber-600' : 'border-gray-100 text-gray-400'
                  }`}
                >
                  <span className="text-lg font-bold">{opt.value}</span>
                  <span className="text-[10px] font-medium leading-tight text-center">{opt.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Gratitude */}
        <div>
          <h2 className="font-semibold text-gray-900 mb-1">{t('checkin.gratitude')}</h2>
          <p className="text-xs text-gray-400 mb-3 italic">{t('checkin.gratitude.quran')}</p>
          <textarea
            value={gratitude}
            onChange={e => setGratitude(e.target.value)}
            placeholder={t('checkin.gratitude.placeholder')}
            rows={3}
            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 outline-none text-sm resize-none"
          />
        </div>

        {/* Reflection */}
        <div>
          <h2 className="font-semibold text-gray-900 mb-1">{t('checkin.reflection')}</h2>
          <p className="text-xs text-gray-400 mb-3">{t('checkin.reflection.desc')}</p>
          <textarea
            value={reflection}
            onChange={e => setReflection(e.target.value)}
            placeholder={t('checkin.reflection.placeholder')}
            rows={3}
            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 outline-none text-sm resize-none"
          />
        </div>
      </div>

      {/* Submit button */}
      <div className="fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-lg border-t border-gray-100 p-4">
        <div className="max-w-lg mx-auto">
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-3.5 rounded-xl transition-all flex items-center justify-center gap-2 shadow-lg shadow-emerald-600/25"
          >
            {submitting ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <>{t('checkin.submit')}<Sparkles className="w-4 h-4" /></>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
