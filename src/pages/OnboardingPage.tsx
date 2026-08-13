import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useI18n } from '@/lib/i18n';
import { supabase } from '@/lib/supabase';
import { ArrowRight, ArrowLeft, Check, Dumbbell, Salad, Moon, Brain, Bed, Clock, Heart, Sparkles } from 'lucide-react';

const stepIds = ['welcome', 'fitness', 'goals', 'diet', 'sleep', 'spiritual', 'challenge'] as const;

const fitnessLevelValues = ['beginner', 'intermediate', 'advanced'] as const;
const fitnessIcons = { beginner: '🌱', intermediate: '🌿', advanced: '🌳' };

const goalOptionValues = [
  { value: 'weight_loss', icon: Dumbbell },
  { value: 'build_strength', icon: Dumbbell },
  { value: 'better_sleep', icon: Bed },
  { value: 'reduce_stress', icon: Brain },
  { value: 'healthy_eating', icon: Salad },
  { value: 'spiritual_growth', icon: Moon },
  { value: 'mental_clarity', icon: Brain },
  { value: 'more_energy', icon: Heart },
];

const dietaryValues = ['no_restriction', 'low_sugar', 'high_protein', 'plant_forward', 'sunnah_diet'] as const;

const sleepValues = ['early_bird', 'moderate', 'night_owl'] as const;
const sleepIcons = { early_bird: '🌅', moderate: '🌤️', night_owl: '🌙' };

const spiritualValues = ['beginner', 'practicing', 'devoted'] as const;

const challengeValues = [
  { value: '30_days', days: 30, color: 'from-amber-500 to-orange-500' },
  { value: '100_days', days: 100, color: 'from-emerald-500 to-teal-600' },
  { value: '1_year', days: 365, color: 'from-teal-600 to-cyan-600' },
] as const;

export default function OnboardingPage() {
  const { user, refreshProfile } = useAuth();
  const { t, isRTL } = useI18n();
  const [step, setStep] = useState(0);
  const [saving, setSaving] = useState(false);
  const [formData, setFormData] = useState({
    fitness_level: 'beginner',
    health_goals: [] as string[],
    dietary_preferences: [] as string[],
    sleep_habit: 'moderate',
    spiritual_level: 'beginner',
    preferred_challenge: '30_days',
  });

  const steps = [
    { id: 'welcome', title: t('onboarding.welcome'), subtitle: t('onboarding.welcome.sub') },
    { id: 'fitness', title: t('onboarding.fitness'), subtitle: t('onboarding.fitness.sub') },
    { id: 'goals', title: t('onboarding.goals'), subtitle: t('onboarding.goals.sub') },
    { id: 'diet', title: t('onboarding.diet'), subtitle: t('onboarding.diet.sub') },
    { id: 'sleep', title: t('onboarding.sleep'), subtitle: t('onboarding.sleep.sub') },
    { id: 'spiritual', title: t('onboarding.spiritual'), subtitle: t('onboarding.spiritual.sub') },
    { id: 'challenge', title: t('onboarding.challenge'), subtitle: t('onboarding.challenge.sub') },
  ];

  function toggleGoal(goal: string) {
    setFormData(prev => ({
      ...prev,
      health_goals: prev.health_goals.includes(goal)
        ? prev.health_goals.filter(g => g !== goal)
        : [...prev.health_goals, goal],
    }));
  }

  function toggleDiet(diet: string) {
    setFormData(prev => ({
      ...prev,
      dietary_preferences: prev.dietary_preferences.includes(diet)
        ? prev.dietary_preferences.filter(d => d !== diet)
        : [...prev.dietary_preferences, diet],
    }));
  }

  async function handleFinish() {
    if (!user) return;
    setSaving(true);

    await supabase.from('profiles').update({
      ...formData,
      onboarding_completed: true,
    }).eq('id', user.id);

    await refreshProfile();
    setSaving(false);
  }

  const canProceed = () => {
    if (step === 2) return formData.health_goals.length > 0;
    return true;
  };

  function renderStep() {
    switch (steps[step].id) {
      case 'welcome':
        return (
          <div className="text-center py-8">
            <div className="w-24 h-24 bg-gradient-to-br from-emerald-400 to-teal-600 rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-xl shadow-emerald-600/30">
              <Sparkles className="w-12 h-12 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-3">{t('onboarding.welcome.title')}</h2>
            <p className="text-gray-500 leading-relaxed max-w-xs mx-auto">
              {t('onboarding.welcome.desc')}
            </p>
            <div className={`mt-8 bg-emerald-50 rounded-2xl p-5 ${isRTL ? 'text-right' : 'text-left'}`}>
              <p className="text-emerald-800 text-sm font-medium mb-2">{t('onboarding.expect')}</p>
              <ul className="space-y-2 text-sm text-emerald-700">
                <li className={`flex items-start gap-2 ${isRTL ? 'flex-row-reverse' : ''}`}>
                  <Check className="w-4 h-4 mt-0.5 shrink-0" /> {t('onboarding.expect.1')}
                </li>
                <li className={`flex items-start gap-2 ${isRTL ? 'flex-row-reverse' : ''}`}>
                  <Check className="w-4 h-4 mt-0.5 shrink-0" /> {t('onboarding.expect.2')}
                </li>
                <li className={`flex items-start gap-2 ${isRTL ? 'flex-row-reverse' : ''}`}>
                  <Check className="w-4 h-4 mt-0.5 shrink-0" /> {t('onboarding.expect.3')}
                </li>
                <li className={`flex items-start gap-2 ${isRTL ? 'flex-row-reverse' : ''}`}>
                  <Check className="w-4 h-4 mt-0.5 shrink-0" /> {t('onboarding.expect.4')}
                </li>
              </ul>
            </div>
          </div>
        );

      case 'fitness':
        return (
          <div className="space-y-3">
            {fitnessLevelValues.map(value => (
              <button
                key={value}
                onClick={() => setFormData(prev => ({ ...prev, fitness_level: value }))}
                className={`w-full p-4 rounded-2xl border-2 ${isRTL ? 'text-right' : 'text-left'} transition-all ${
                  formData.fitness_level === value
                    ? 'border-emerald-500 bg-emerald-50'
                    : 'border-gray-100 hover:border-gray-200 bg-white'
                }`}
              >
                <div className={`flex items-center gap-3 ${isRTL ? 'flex-row-reverse' : ''}`}>
                  <span className="text-2xl">{fitnessIcons[value]}</span>
                  <div>
                    <p className="font-semibold text-gray-900">{t(`fitness.${value}`)}</p>
                    <p className="text-sm text-gray-500">{t(`fitness.${value}.desc`)}</p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        );

      case 'goals':
        return (
          <div className="grid grid-cols-2 gap-3">
            {goalOptionValues.map(({ value, icon: Icon }) => {
              const selected = formData.health_goals.includes(value);
              return (
                <button
                  key={value}
                  onClick={() => toggleGoal(value)}
                  className={`p-4 rounded-2xl border-2 ${isRTL ? 'text-right' : 'text-left'} transition-all ${
                    selected
                      ? 'border-emerald-500 bg-emerald-50'
                      : 'border-gray-100 hover:border-gray-200 bg-white'
                  }`}
                >
                  <Icon className={`w-5 h-5 mb-2 ${selected ? 'text-emerald-600' : 'text-gray-400'}`} />
                  <p className={`text-sm font-medium ${selected ? 'text-emerald-700' : 'text-gray-700'}`}>{t(`goal.${value}`)}</p>
                </button>
              );
            })}
            <p className="col-span-2 text-xs text-gray-400 text-center mt-1">{t('onboarding.goals.hint')}</p>
          </div>
        );

      case 'diet':
        return (
          <div className="space-y-3">
            {dietaryValues.map(value => {
              const selected = formData.dietary_preferences.includes(value);
              return (
                <button
                  key={value}
                  onClick={() => toggleDiet(value)}
                  className={`w-full p-4 rounded-2xl border-2 ${isRTL ? 'text-right' : 'text-left'} transition-all ${
                    selected
                      ? 'border-emerald-500 bg-emerald-50'
                      : 'border-gray-100 hover:border-gray-200 bg-white'
                  }`}
                >
                  <div className={`flex items-center justify-between ${isRTL ? 'flex-row-reverse' : ''}`}>
                    <div>
                      <p className="font-semibold text-gray-900">{t(`diet.${value}`)}</p>
                      <p className="text-sm text-gray-500">{t(`diet.${value}.desc`)}</p>
                    </div>
                    {selected && <Check className="w-5 h-5 text-emerald-600 shrink-0" />}
                  </div>
                </button>
              );
            })}
          </div>
        );

      case 'sleep':
        return (
          <div className="space-y-3">
            {sleepValues.map(value => (
              <button
                key={value}
                onClick={() => setFormData(prev => ({ ...prev, sleep_habit: value }))}
                className={`w-full p-4 rounded-2xl border-2 ${isRTL ? 'text-right' : 'text-left'} transition-all ${
                  formData.sleep_habit === value
                    ? 'border-emerald-500 bg-emerald-50'
                    : 'border-gray-100 hover:border-gray-200 bg-white'
                }`}
              >
                <div className={`flex items-center gap-3 ${isRTL ? 'flex-row-reverse' : ''}`}>
                  <span className="text-2xl">{sleepIcons[value]}</span>
                  <div>
                    <p className="font-semibold text-gray-900">{t(`sleep.${value}`)}</p>
                    <p className="text-sm text-gray-500">{t(`sleep.${value}.desc`)}</p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        );

      case 'spiritual':
        return (
          <div className="space-y-3">
            {spiritualValues.map(value => (
              <button
                key={value}
                onClick={() => setFormData(prev => ({ ...prev, spiritual_level: value }))}
                className={`w-full p-4 rounded-2xl border-2 ${isRTL ? 'text-right' : 'text-left'} transition-all ${
                  formData.spiritual_level === value
                    ? 'border-emerald-500 bg-emerald-50'
                    : 'border-gray-100 hover:border-gray-200 bg-white'
                }`}
              >
                <p className="font-semibold text-gray-900">{t(`spiritual.${value}`)}</p>
                <p className="text-sm text-gray-500">{t(`spiritual.${value}.desc`)}</p>
              </button>
            ))}
          </div>
        );

      case 'challenge':
        return (
          <div className="space-y-4">
            {challengeValues.map(opt => (
              <button
                key={opt.value}
                onClick={() => setFormData(prev => ({ ...prev, preferred_challenge: opt.value }))}
                className={`w-full rounded-2xl border-2 overflow-hidden ${isRTL ? 'text-right' : 'text-left'} transition-all ${
                  formData.preferred_challenge === opt.value
                    ? 'border-emerald-500'
                    : 'border-gray-100 hover:border-gray-200'
                }`}
              >
                <div className={`bg-gradient-to-r ${opt.color} p-4 text-white`}>
                  <div className={`flex items-center justify-between ${isRTL ? 'flex-row-reverse' : ''}`}>
                    <div>
                      <p className="text-xl font-bold">{t(`challenge.${opt.value}`)}</p>
                      <p className="text-white/80 text-sm">{t(`challenge.${opt.value}.detail`)}</p>
                    </div>
                    <Clock className="w-8 h-8 text-white/60" />
                  </div>
                </div>
                <div className="p-4 bg-white">
                  <p className="text-sm text-gray-600">{t(`challenge.${opt.value}.desc`)}</p>
                </div>
              </button>
            ))}
          </div>
        );
    }
  }

  const isLast = step === steps.length - 1;

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-teal-50 flex flex-col" dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Progress bar */}
      <div className="px-6 pt-6 pb-2">
        <div className={`flex gap-1.5 ${isRTL ? 'flex-row-reverse' : ''}`}>
          {steps.map((_, i) => (
            <div
              key={i}
              className={`h-1.5 rounded-full flex-1 transition-all ${
                i <= step ? 'bg-emerald-500' : 'bg-gray-200'
              }`}
            />
          ))}
        </div>
      </div>

      {/* Header */}
      <div className={`px-6 py-4 ${isRTL ? 'text-right' : 'text-left'}`}>
        <h1 className="text-xl font-bold text-gray-900">{steps[step].title}</h1>
        <p className="text-sm text-gray-500">{steps[step].subtitle}</p>
      </div>

      {/* Content */}
      <div className="flex-1 px-6 overflow-y-auto pb-32">
        {renderStep()}
      </div>

      {/* Footer buttons */}
      <div className="fixed bottom-0 left-0 right-0 bg-white/80 backdrop-blur-lg border-t border-gray-100 p-4">
        <div className={`flex gap-3 max-w-md mx-auto ${isRTL ? 'flex-row-reverse' : ''}`}>
          {step > 0 && (
            <button
              onClick={() => setStep(s => s - 1)}
              className={`px-6 py-3.5 rounded-xl border border-gray-200 text-gray-700 font-medium flex items-center gap-2 ${isRTL ? 'flex-row-reverse' : ''}`}
            >
              {isRTL ? <ArrowRight className="w-4 h-4" /> : <ArrowLeft className="w-4 h-4" />}
              {t('onboarding.back')}
            </button>
          )}
          <button
            onClick={isLast ? handleFinish : () => setStep(s => s + 1)}
            disabled={!canProceed() || saving}
            className={`flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-3.5 rounded-xl transition-all flex items-center justify-center gap-2 disabled:opacity-50 shadow-lg shadow-emerald-600/25 ${isRTL ? 'flex-row-reverse' : ''}`}
          >
            {saving ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : isLast ? (
              <>{t('onboarding.start')}<Sparkles className="w-4 h-4" /></>
            ) : (
              <>{t('onboarding.continue')}{isRTL ? <ArrowLeft className="w-4 h-4" /> : <ArrowRight className="w-4 h-4" />}</>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
