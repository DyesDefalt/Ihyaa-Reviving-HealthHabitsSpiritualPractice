import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { supabase } from '@/lib/supabase';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isToday, isSameDay, startOfWeek, endOfWeek, addMonths, subMonths } from 'date-fns';
import { ChevronLeft, ChevronRight, CheckCircle2, Circle, Clock } from 'lucide-react';
import { useI18n } from '@/lib/i18n';

interface CalendarTask {
  id: string;
  title: string;
  pillar: string;
  duration_minutes: number;
  completed: boolean;
  scheduled_date: string;
  points_reward: number;
}

const pillarEmoji: Record<string, string> = {
  physical: '💪',
  nutrition: '🥗',
  mental: '🧠',
  spiritual: '🕌',
};

export default function CalendarPage() {
  const { user } = useAuth();
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [tasks, setTasks] = useState<CalendarTask[]>([]);
  const [monthTasks, setMonthTasks] = useState<Map<string, { total: number; completed: number }>>(new Map());
  const [loading, setLoading] = useState(true);
  const { t, isRTL } = useI18n();

  useEffect(() => {
    if (user) loadMonthData();
  }, [user, currentMonth]);

  useEffect(() => {
    if (user) loadDayTasks();
  }, [user, selectedDate]);

  async function loadMonthData() {
    if (!user) return;
    const start = format(startOfMonth(currentMonth), 'yyyy-MM-dd');
    const end = format(endOfMonth(currentMonth), 'yyyy-MM-dd');

    const { data } = await supabase
      .from('daily_tasks')
      .select('scheduled_date, completed')
      .eq('user_id', user.id)
      .gte('scheduled_date', start)
      .lte('scheduled_date', end);

    const map = new Map<string, { total: number; completed: number }>();
    (data ?? []).forEach(t => {
      const key = t.scheduled_date;
      const entry = map.get(key) || { total: 0, completed: 0 };
      entry.total++;
      if (t.completed) entry.completed++;
      map.set(key, entry);
    });
    setMonthTasks(map);
  }

  async function loadDayTasks() {
    if (!user) return;
    setLoading(true);
    const dateStr = format(selectedDate, 'yyyy-MM-dd');
    const { data } = await supabase
      .from('daily_tasks')
      .select('*')
      .eq('user_id', user.id)
      .eq('scheduled_date', dateStr)
      .order('pillar');
    setTasks(data ?? []);
    setLoading(false);
  }

  const monthStart = startOfMonth(currentMonth);
  const monthEnd = endOfMonth(currentMonth);
  const calendarStart = startOfWeek(monthStart);
  const calendarEnd = endOfWeek(monthEnd);
  const days = eachDayOfInterval({ start: calendarStart, end: calendarEnd });

  function getDayStatus(date: Date): 'complete' | 'partial' | 'none' | 'empty' {
    const key = format(date, 'yyyy-MM-dd');
    const data = monthTasks.get(key);
    if (!data) return 'empty';
    if (data.completed === data.total) return 'complete';
    if (data.completed > 0) return 'partial';
    return 'none';
  }

  return (
    <div className="max-w-lg mx-auto" dir={isRTL ? 'rtl' : 'ltr'}>
      {/* Header */}
      <div className="px-6 pt-12 pb-4">
        <h1 className="text-2xl font-bold text-gray-900">{t('calendar.title')}</h1>
        <p className="text-gray-500 text-sm">{t('calendar.subtitle')}</p>
      </div>

      {/* Month navigation */}
      <div className="px-6 mb-4">
        <div className="flex items-center justify-between">
          <button onClick={() => setCurrentMonth(subMonths(currentMonth, 1))} className="p-2 hover:bg-gray-100 rounded-xl">
            <ChevronLeft className="w-5 h-5 text-gray-600" />
          </button>
          <h2 className="text-lg font-semibold text-gray-900">{format(currentMonth, 'MMMM yyyy')}</h2>
          <button onClick={() => setCurrentMonth(addMonths(currentMonth, 1))} className="p-2 hover:bg-gray-100 rounded-xl">
            <ChevronRight className="w-5 h-5 text-gray-600" />
          </button>
        </div>
      </div>

      {/* Calendar grid */}
      <div className="px-6 mb-6">
        <div className="bg-white rounded-2xl border border-gray-100 p-4">
          <div className="grid grid-cols-7 gap-1 mb-2">
            {['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'].map(d => (
              <div key={d} className="text-center text-xs font-medium text-gray-400 py-1">{d}</div>
            ))}
          </div>
          <div className="grid grid-cols-7 gap-1">
            {days.map(day => {
              const inMonth = isSameMonth(day, currentMonth);
              const today = isToday(day);
              const selected = isSameDay(day, selectedDate);
              const status = getDayStatus(day);

              return (
                <button
                  key={day.toISOString()}
                  onClick={() => setSelectedDate(day)}
                  className={`relative aspect-square flex flex-col items-center justify-center rounded-xl text-sm transition-all ${
                    !inMonth ? 'text-gray-300' :
                    selected ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-600/25' :
                    today ? 'bg-emerald-50 text-emerald-700 font-semibold' :
                    'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <span className="text-sm">{format(day, 'd')}</span>
                  {inMonth && status !== 'empty' && (
                    <div className={`absolute bottom-1 w-1.5 h-1.5 rounded-full ${
                      selected ? 'bg-white/70' :
                      status === 'complete' ? 'bg-emerald-500' :
                      status === 'partial' ? 'bg-amber-400' :
                      'bg-gray-300'
                    }`} />
                  )}
                </button>
              );
            })}
          </div>

          {/* Legend */}
          <div className="flex items-center justify-center gap-4 mt-3 pt-3 border-t border-gray-50">
            <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-emerald-500" /><span className="text-xs text-gray-500">{t('calendar.legend.done')}</span></div>
            <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-amber-400" /><span className="text-xs text-gray-500">{t('calendar.legend.partial')}</span></div>
            <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-gray-300" /><span className="text-xs text-gray-500">{t('calendar.legend.pending')}</span></div>
          </div>
        </div>
      </div>

      {/* Selected day tasks */}
      <div className="px-6 pb-6">
        <h3 className="font-semibold text-gray-900 mb-3">{format(selectedDate, 'EEEE, MMMM d')}</h3>
        {loading ? (
          <div className="flex justify-center py-8">
            <div className="w-6 h-6 border-2 border-emerald-200 border-t-emerald-600 rounded-full animate-spin" />
          </div>
        ) : tasks.length === 0 ? (
          <div className="bg-white rounded-2xl border border-gray-100 p-8 text-center">
            <p className="text-gray-400 text-sm">{t('calendar.no_tasks')}</p>
          </div>
        ) : (
          <div className="space-y-2">
            {tasks.map(task => (
              <div key={task.id} className={`bg-white rounded-xl border p-3 flex items-center gap-3 ${task.completed ? 'border-emerald-200 bg-emerald-50/50' : 'border-gray-100'}`}>
                {task.completed ? (
                  <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0" />
                ) : (
                  <Circle className="w-5 h-5 text-gray-300 shrink-0" />
                )}
                <div className="flex-1 min-w-0">
                  <p className={`text-sm font-medium ${task.completed ? 'text-gray-400 line-through' : 'text-gray-900'}`}>{task.title}</p>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-xs">{pillarEmoji[task.pillar]}</span>
                    <span className="text-xs text-gray-400">{t('pillar.' + task.pillar)}</span>
                    <Clock className="w-3 h-3 text-gray-400" />
                    <span className="text-xs text-gray-400">{task.duration_minutes}{t('home.min')}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
