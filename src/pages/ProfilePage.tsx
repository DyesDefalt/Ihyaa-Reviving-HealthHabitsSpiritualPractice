import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { supabase } from '@/lib/supabase';
import { useI18n, languageNames, type Language } from '@/lib/i18n';
import { LogOut, Settings, ChevronRight, User, Dumbbell, Moon, Salad, Bed, Target, Save, X, Globe } from 'lucide-react';

export default function ProfilePage() {
  const { user, profile, signOut, refreshProfile } = useAuth();
  const { t, isRTL, lang, setLang } = useI18n();
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({
    display_name: profile?.display_name ?? '',
    fitness_level: profile?.fitness_level ?? 'beginner',
    sleep_habit: profile?.sleep_habit ?? 'moderate',
    spiritual_level: profile?.spiritual_level ?? 'beginner',
    preferred_challenge: profile?.preferred_challenge ?? '30_days',
  });

  async function handleSave() {
    if (!user) return;
    setSaving(true);
    await supabase.from('profiles').update(form).eq('id', user.id);
    await refreshProfile();
    setSaving(false);
    setEditing(false);
  }

  const infoItems = [
    { icon: Dumbbell, label: t('profile.fitness_level'), value: profile?.fitness_level, color: 'text-rose-500 bg-rose-50' },
    { icon: Moon, label: t('profile.spiritual_level'), value: profile?.spiritual_level, color: 'text-emerald-500 bg-emerald-50' },
    { icon: Bed, label: t('profile.sleep_pattern'), value: profile?.sleep_habit, color: 'text-sky-500 bg-sky-50' },
    { icon: Salad, label: t('profile.diet_preferences'), value: profile?.dietary_preferences?.join(', ') || t('profile.none_set'), color: 'text-amber-500 bg-amber-50' },
    { icon: Target, label: t('profile.challenge_type'), value: profile?.preferred_challenge?.replace('_', ' '), color: 'text-teal-500 bg-teal-50' },
  ];

  const languages: Language[] = ['en', 'ar', 'id'];

  return (
    <div className="max-w-lg mx-auto" dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Header */}
      <div className="px-6 pt-12 pb-6">
        <h1 className="text-2xl font-bold text-gray-900">{t('profile.title')}</h1>
      </div>

      {/* User card */}
      <div className="px-6 mb-6">
        <div className="bg-white rounded-2xl border border-gray-100 p-5">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-gradient-to-br from-emerald-400 to-teal-600 rounded-2xl flex items-center justify-center">
              <User className="w-8 h-8 text-white" />
            </div>
            <div className="flex-1">
              <h2 className="text-lg font-bold text-gray-900">{profile?.display_name || 'User'}</h2>
              <p className="text-sm text-gray-500">{user?.email}</p>
              <p className="text-xs text-gray-400 mt-0.5">Joined {profile?.created_at ? new Date(profile.created_at).toLocaleDateString() : 'recently'}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Preferences */}
      <div className="px-6 mb-6">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-semibold text-gray-900">{t('profile.preferences')}</h3>
          <button
            onClick={() => { setEditing(!editing); setForm({ display_name: profile?.display_name ?? '', fitness_level: profile?.fitness_level ?? 'beginner', sleep_habit: profile?.sleep_habit ?? 'moderate', spiritual_level: profile?.spiritual_level ?? 'beginner', preferred_challenge: profile?.preferred_challenge ?? '30_days' }); }}
            className="text-emerald-600 text-sm font-medium flex items-center gap-1"
          >
            {editing ? <><X className="w-4 h-4" />{t('profile.cancel')}</> : <><Settings className="w-4 h-4" />{t('profile.edit')}</>}
          </button>
        </div>

        {editing ? (
          <div className="bg-white rounded-2xl border border-gray-100 p-5 space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{t('profile.display_name')}</label>
              <input
                type="text"
                value={form.display_name}
                onChange={e => setForm(f => ({ ...f, display_name: e.target.value }))}
                className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 outline-none text-sm"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{t('profile.fitness_level')}</label>
              <select
                value={form.fitness_level}
                onChange={e => setForm(f => ({ ...f, fitness_level: e.target.value }))}
                className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-emerald-500 outline-none text-sm bg-white"
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{t('profile.sleep_pattern')}</label>
              <select
                value={form.sleep_habit}
                onChange={e => setForm(f => ({ ...f, sleep_habit: e.target.value }))}
                className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-emerald-500 outline-none text-sm bg-white"
              >
                <option value="early_bird">Early Bird</option>
                <option value="moderate">Moderate</option>
                <option value="night_owl">Night Owl</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{t('profile.spiritual_level')}</label>
              <select
                value={form.spiritual_level}
                onChange={e => setForm(f => ({ ...f, spiritual_level: e.target.value }))}
                className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-emerald-500 outline-none text-sm bg-white"
              >
                <option value="beginner">Starting Out</option>
                <option value="practicing">Practicing</option>
                <option value="devoted">Devoted</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">{t('profile.challenge_type')}</label>
              <select
                value={form.preferred_challenge}
                onChange={e => setForm(f => ({ ...f, preferred_challenge: e.target.value }))}
                className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:border-emerald-500 outline-none text-sm bg-white"
              >
                <option value="30_days">30 Days</option>
                <option value="100_days">100 Days</option>
                <option value="1_year">1 Year</option>
              </select>
            </div>

            <button
              onClick={handleSave}
              disabled={saving}
              className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-3 rounded-xl transition-all flex items-center justify-center gap-2"
            >
              {saving ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <><Save className="w-4 h-4" />{t('profile.save')}</>
              )}
            </button>
          </div>
        ) : (
          <div className="bg-white rounded-2xl border border-gray-100 divide-y divide-gray-50">
            {infoItems.map(({ icon: Icon, label, value, color }) => (
              <div key={label} className="flex items-center gap-3 p-4">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${color}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <div className="flex-1">
                  <p className="text-sm text-gray-500">{label}</p>
                  <p className="text-sm font-medium text-gray-900 capitalize">{value?.toString().replace(/_/g, ' ')}</p>
                </div>
                <ChevronRight className="w-4 h-4 text-gray-300" />
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Language */}
      <div className="px-6 mb-6">
        <div className="flex items-center gap-2 mb-3">
          <Globe className="w-4 h-4 text-gray-500" />
          <h3 className="font-semibold text-gray-900">{t('profile.language')}</h3>
        </div>
        <div className="bg-white rounded-2xl border border-gray-100 p-3">
          <div className="flex gap-2">
            {languages.map((l) => (
              <button
                key={l}
                onClick={() => setLang(l)}
                className={`flex-1 py-2.5 px-3 rounded-xl text-sm font-medium transition-all ${
                  lang === l
                    ? 'bg-emerald-600 text-white shadow-sm'
                    : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
                }`}
              >
                {languageNames[l]}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Health Goals */}
      <div className="px-6 mb-6">
        <h3 className="font-semibold text-gray-900 mb-3">{t('profile.health_goals')}</h3>
        <div className="flex flex-wrap gap-2">
          {(profile?.health_goals ?? []).map(goal => (
            <span
              key={goal}
              className="px-3 py-1.5 bg-emerald-50 text-emerald-700 text-sm font-medium rounded-full capitalize"
            >
              {goal.replace(/_/g, ' ')}
            </span>
          ))}
          {(profile?.health_goals ?? []).length === 0 && (
            <p className="text-sm text-gray-400">{t('profile.no_goals')}</p>
          )}
        </div>
      </div>

      {/* Sign out */}
      <div className="px-6 pb-8">
        <button
          onClick={signOut}
          className="w-full flex items-center justify-center gap-2 py-3 rounded-xl border border-red-200 text-red-600 hover:bg-red-50 transition-all font-medium"
        >
          <LogOut className="w-4 h-4" />
          {t('profile.signout')}
        </button>
      </div>
    </div>
  );
}
