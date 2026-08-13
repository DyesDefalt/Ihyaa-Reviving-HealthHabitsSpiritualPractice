import { Home, Calendar, TrendingUp, Gift, User } from 'lucide-react';
import { useI18n } from '@/lib/i18n';

interface AppLayoutProps {
  children: React.ReactNode;
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export default function AppLayout({ children, activeTab, onTabChange }: AppLayoutProps) {
  const { t } = useI18n();

  const tabs = [
    { id: 'home', label: t('nav.home'), icon: Home },
    { id: 'calendar', label: t('nav.calendar'), icon: Calendar },
    { id: 'progress', label: t('nav.progress'), icon: TrendingUp },
    { id: 'store', label: t('nav.store'), icon: Gift },
    { id: 'profile', label: t('nav.profile'), icon: User },
  ];

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      {children}

      {/* Bottom navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 z-50">
        <div className="max-w-lg mx-auto flex">
          {tabs.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => onTabChange(id)}
              className={`flex-1 flex flex-col items-center py-2 pt-3 transition-colors ${
                activeTab === id
                  ? 'text-emerald-600'
                  : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              <Icon className="w-5 h-5" strokeWidth={activeTab === id ? 2.5 : 1.5} />
              <span className="text-[10px] mt-1 font-medium">{label}</span>
              {activeTab === id && (
                <div className="absolute top-0 w-8 h-0.5 bg-emerald-600 rounded-full" />
              )}
            </button>
          ))}
        </div>
      </nav>
    </div>
  );
}
