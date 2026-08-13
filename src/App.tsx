import { useState } from 'react';
import { I18nProvider } from '@/lib/i18n';
import { AuthProvider, useAuth } from '@/contexts/AuthContext';
import AuthPage from '@/pages/AuthPage';
import OnboardingPage from '@/pages/OnboardingPage';
import AppLayout from '@/components/AppLayout';
import HomePage from '@/pages/HomePage';
import CalendarPage from '@/pages/CalendarPage';
import ProgressPage from '@/pages/ProgressPage';
import StorePage from '@/pages/StorePage';
import ProfilePage from '@/pages/ProfilePage';
import CheckinPage from '@/pages/CheckinPage';
import KnowledgePage from '@/pages/KnowledgePage';

function AppContent() {
  const { user, profile, loading } = useAuth();
  const [activeTab, setActiveTab] = useState('home');
  const [subPage, setSubPage] = useState<string | null>(null);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-amber-50 flex flex-col items-center justify-center gap-4">
        <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl flex items-center justify-center shadow-xl shadow-emerald-600/30 animate-pulse">
          <svg className="w-8 h-8 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 3l1.912 5.813a2 2 0 001.272 1.278L21 12l-5.816 1.91a2 2 0 00-1.272 1.277L12 21l-1.912-5.813a2 2 0 00-1.272-1.278L3 12l5.816-1.91a2 2 0 001.272-1.277z" />
          </svg>
        </div>
        <p className="text-emerald-700 font-medium">Loading Ihyaa...</p>
      </div>
    );
  }

  if (!user) return <AuthPage />;
  if (profile && !profile.onboarding_completed) return <OnboardingPage />;

  if (subPage === 'checkin') {
    return <CheckinPage onBack={() => setSubPage(null)} />;
  }

  if (subPage === 'knowledge') {
    return <KnowledgePage onBack={() => setSubPage(null)} />;
  }

  function handleNavigate(target: string) {
    if (target === 'checkin' || target === 'knowledge') {
      setSubPage(target);
    } else {
      setActiveTab(target);
    }
  }

  return (
    <AppLayout activeTab={activeTab} onTabChange={setActiveTab}>
      {activeTab === 'home' && <HomePage onNavigate={handleNavigate} />}
      {activeTab === 'calendar' && <CalendarPage />}
      {activeTab === 'progress' && <ProgressPage />}
      {activeTab === 'store' && <StorePage />}
      {activeTab === 'profile' && <ProfilePage />}
    </AppLayout>
  );
}

export default function App() {
  return (
    <I18nProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </I18nProvider>
  );
}
