import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

export type Reminder = {
  id: string;
  title: string;
  body: string;
  date: string; // YYYY-MM-DD
  time: string; // HH:MM
};

export const notificationsSupported = Platform.OS !== 'web';

export async function requestPermission(): Promise<boolean> {
  if (!notificationsSupported) return false;
  const current = await Notifications.getPermissionsAsync();
  if (current.granted) return true;
  const asked = await Notifications.requestPermissionsAsync();
  return asked.granted;
}

/** Cancel everything and re-schedule alerts 10 minutes before each habit. */
export async function scheduleReminders(reminders: Reminder[]): Promise<number> {
  if (!notificationsSupported) return 0;
  const ok = await requestPermission();
  if (!ok) return 0;

  await Notifications.cancelAllScheduledNotificationsAsync();
  const now = Date.now();
  let count = 0;

  for (const r of reminders) {
    const [hh, mm] = r.time.split(':').map(Number);
    const when = new Date(`${r.date}T00:00:00`);
    when.setHours(hh, mm - 10, 0, 0);
    if (when.getTime() <= now) continue;
    await Notifications.scheduleNotificationAsync({
      content: { title: r.title, body: r.body, sound: true },
      trigger: { type: Notifications.SchedulableTriggerInputTypes.DATE, date: when },
    });
    count += 1;
    if (count >= 60) break; // platform scheduling limits
  }
  return count;
}
