import type { Lang } from './i18n';

const MONTHS: Record<Lang, string[]> = {
  en: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
  id: ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'],
};

const DAYS: Record<Lang, string[]> = {
  en: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
  id: ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu'],
};

export const todayISO = () => new Date().toLocaleDateString('en-CA');

export function parseISO(iso: string) {
  const [y, m, d] = iso.split('-').map(Number);
  return new Date(y, m - 1, d);
}

export function toISO(d: Date) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

export function addDays(iso: string, n: number) {
  const d = parseISO(iso);
  d.setDate(d.getDate() + n);
  return toISO(d);
}

export function longDate(iso: string, lang: Lang) {
  const d = parseISO(iso);
  return `${DAYS[lang][d.getDay()]}, ${d.getDate()} ${MONTHS[lang][d.getMonth()]}`;
}

export function shortMonth(iso: string, lang: Lang) {
  const d = parseISO(iso);
  return `${MONTHS[lang][d.getMonth()]} ${d.getFullYear()}`;
}

export function dayLetter(weekday: number, lang: Lang) {
  return DAYS[lang][weekday].slice(0, 1);
}

export function weekdayShort(iso: string, lang: Lang) {
  const d = parseISO(iso);
  return DAYS[lang][d.getDay()].slice(0, 3);
}
