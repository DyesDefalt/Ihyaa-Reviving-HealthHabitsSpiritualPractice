import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useI18n, languageNames, type Language } from '@/lib/i18n';
import { Moon, Sun, Heart, Sparkles, Eye, EyeOff, ArrowRight } from 'lucide-react';

function IslamicGeometricPattern() {
  return (
    <svg
      className="absolute inset-0 w-full h-full"
      viewBox="0 0 400 200"
      preserveAspectRatio="xMidYMid slice"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <pattern
          id="geo-pattern"
          x="0"
          y="0"
          width="60"
          height="60"
          patternUnits="userSpaceOnUse"
        >
          {/* Eight-pointed star (two overlapping squares rotated 45°) */}
          <rect
            x="13"
            y="13"
            width="34"
            height="34"
            fill="none"
            stroke="white"
            strokeWidth="0.4"
            transform="rotate(45 30 30)"
          />
          <rect
            x="13"
            y="13"
            width="34"
            height="34"
            fill="none"
            stroke="white"
            strokeWidth="0.4"
          />
          {/* Inner octagon */}
          <polygon
            points="30,10 44,16 50,30 44,44 30,50 16,44 10,30 16,16"
            fill="none"
            stroke="white"
            strokeWidth="0.3"
          />
          {/* Center circle */}
          <circle cx="30" cy="30" r="6" fill="none" stroke="white" strokeWidth="0.3" />
          {/* Connecting lines from star tips to octagon vertices */}
          <line x1="30" y1="6" x2="30" y2="10" stroke="white" strokeWidth="0.25" />
          <line x1="54" y1="30" x2="50" y2="30" stroke="white" strokeWidth="0.25" />
          <line x1="30" y1="54" x2="30" y2="50" stroke="white" strokeWidth="0.25" />
          <line x1="6" y1="30" x2="10" y2="30" stroke="white" strokeWidth="0.25" />
        </pattern>
      </defs>
      <rect width="400" height="200" fill="url(#geo-pattern)" opacity="0.12" />
    </svg>
  );
}

const languages: Language[] = ['en', 'ar', 'id'];
const languageLabels: Record<Language, string> = { en: 'EN', ar: 'AR', id: 'ID' };

export default function AuthPage() {
  const { signIn, signUp } = useAuth();
  const { t, lang, setLang, isRTL } = useI18n();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError('');
    setSubmitting(true);

    const result = isLogin
      ? await signIn(email, password)
      : await signUp(email, password, displayName);

    if (result.error) setError(result.error);
    setSubmitting(false);
  }

  return (
    <div
      dir={isRTL ? 'rtl' : 'ltr'}
      className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-amber-50 flex flex-col"
    >
      {/* Decorative header with geometric pattern */}
      <div className="relative h-64 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-600 to-teal-700" />
        <IslamicGeometricPattern />
        <div className="relative z-10 flex flex-col items-center justify-center h-full text-white px-6">
          <div className="w-16 h-16 bg-white/20 backdrop-blur-sm rounded-2xl flex items-center justify-center mb-4">
            <Sparkles className="w-8 h-8" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight">{t('app.name')}</h1>
          <p className="text-emerald-100 mt-1 text-sm">{t('app.tagline')}</p>
        </div>
      </div>

      {/* Form card */}
      <div className="flex-1 -mt-8 relative z-20">
        <div className="mx-4 bg-white rounded-2xl shadow-xl p-6 max-w-md sm:mx-auto">
          {/* Toggle */}
          <div className="flex bg-gray-100 rounded-xl p-1 mb-6">
            <button
              onClick={() => { setIsLogin(true); setError(''); }}
              className={`flex-1 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isLogin ? 'bg-white shadow-sm text-emerald-700' : 'text-gray-500'
              }`}
            >
              {t('auth.signin')}
            </button>
            <button
              onClick={() => { setIsLogin(false); setError(''); }}
              className={`flex-1 py-2.5 rounded-lg text-sm font-medium transition-all ${
                !isLogin ? 'bg-white shadow-sm text-emerald-700' : 'text-gray-500'
              }`}
            >
              {t('auth.signup')}
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1.5">
                  {t('auth.name')}
                </label>
                <input
                  type="text"
                  required
                  value={displayName}
                  onChange={e => setDisplayName(e.target.value)}
                  placeholder={t('auth.name.placeholder')}
                  className={`w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 outline-none transition-all text-sm ${isRTL ? 'text-right' : 'text-left'}`}
                />
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">
                {t('auth.email')}
              </label>
              <input
                type="email"
                required
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder={t('auth.email.placeholder')}
                dir="ltr"
                className={`w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 outline-none transition-all text-sm ${isRTL ? 'text-right' : 'text-left'}`}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1.5">
                {t('auth.password')}
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  required
                  minLength={6}
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  placeholder={t('auth.password.placeholder')}
                  dir="ltr"
                  className={`w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-emerald-500 focus:ring-2 focus:ring-emerald-500/20 outline-none transition-all text-sm ${isRTL ? 'pl-12 text-right' : 'pr-12 text-left'}`}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className={`absolute top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 ${isRTL ? 'left-3' : 'right-3'}`}
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {error && (
              <div className="bg-red-50 text-red-600 text-sm px-4 py-3 rounded-xl">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-3.5 rounded-xl transition-all flex items-center justify-center gap-2 disabled:opacity-50 shadow-lg shadow-emerald-600/25"
            >
              {submitting ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  {isLogin ? t('auth.signin') : t('auth.signup')}
                  <ArrowRight className={`w-4 h-4 ${isRTL ? 'rotate-180' : ''}`} />
                </>
              )}
            </button>
          </form>
        </div>

        {/* Features preview */}
        <div className="px-6 py-8 max-w-md mx-auto">
          <div className="grid grid-cols-3 gap-4">
            {[
              { icon: Heart, label: t('auth.feature.physical'), color: 'text-rose-500 bg-rose-50' },
              { icon: Moon, label: t('auth.feature.spiritual'), color: 'text-emerald-600 bg-emerald-50' },
              { icon: Sun, label: t('auth.feature.mental'), color: 'text-amber-500 bg-amber-50' },
            ].map(({ icon: Icon, label, color }) => (
              <div key={label} className="flex flex-col items-center gap-2 p-3 rounded-xl bg-white/60 backdrop-blur-sm">
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${color}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <span className="text-xs text-gray-600 text-center leading-tight">{label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Language selector */}
        <div className="flex items-center justify-center gap-3 pb-8">
          {languages.map((code) => (
            <button
              key={code}
              onClick={() => setLang(code)}
              className={`w-9 h-9 rounded-full text-xs font-semibold transition-all ${
                lang === code
                  ? 'bg-emerald-600 text-white shadow-md shadow-emerald-600/30'
                  : 'bg-white/70 text-gray-500 hover:bg-white hover:text-gray-700 border border-gray-200'
              }`}
              title={languageNames[code]}
            >
              {languageLabels[code]}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
