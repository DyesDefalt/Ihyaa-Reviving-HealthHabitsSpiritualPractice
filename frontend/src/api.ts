import { storeDel, storeGet, storeSet } from './storage';

const BASE = process.env.EXPO_PUBLIC_BACKEND_URL;
export const API = `${BASE}/api`;

const ACCESS = 'ihyaa_access';
const REFRESH = 'ihyaa_refresh';

let accessToken: string | null = null;
let refreshTokenValue: string | null = null;

export async function loadTokens() {
  accessToken = await storeGet(ACCESS);
  refreshTokenValue = await storeGet(REFRESH);
  return accessToken;
}

export async function setTokens(access: string, refresh?: string) {
  accessToken = access;
  await storeSet(ACCESS, access);
  if (refresh) {
    refreshTokenValue = refresh;
    await storeSet(REFRESH, refresh);
  }
}

export async function clearTokens() {
  accessToken = null;
  refreshTokenValue = null;
  await storeDel(ACCESS);
  await storeDel(REFRESH);
}

export function getAccessToken() {
  return accessToken;
}

export function errText(detail: any): string {
  if (detail == null) return 'Something went wrong. Please try again.';
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail))
    return detail.map((e) => (e && typeof e.msg === 'string' ? e.msg : JSON.stringify(e))).join(' ');
  if (detail && typeof detail.msg === 'string') return detail.msg;
  return String(detail);
}

export class ApiError extends Error {
  status: number;
  detail: any;
  constructor(status: number, detail: any) {
    super(errText(detail));
    this.status = status;
    this.detail = detail;
  }
}

async function tryRefresh(): Promise<boolean> {
  if (!refreshTokenValue) return false;
  const res = await fetch(`${API}/auth/refresh`, {
    method: 'POST',
    headers: { 'X-Refresh-Token': refreshTokenValue },
  });
  if (!res.ok) return false;
  const data = await res.json();
  await setTokens(data.access_token, data.refresh_token);
  return true;
}

type Opts = { method?: string; body?: any; auth?: boolean; raw?: boolean; retry?: boolean };

export async function api(path: string, opts: Opts = {}): Promise<any> {
  const { method = 'GET', body, auth = true, raw = false, retry = true } = opts;
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (auth && accessToken) headers.Authorization = `Bearer ${accessToken}`;

  const res = await fetch(`${API}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (res.status === 401 && auth && retry && (await tryRefresh())) {
    return api(path, { ...opts, retry: false });
  }

  if (raw) {
    if (!res.ok) throw new ApiError(res.status, await res.text());
    return res.text();
  }

  const text = await res.text();
  const data = text ? JSON.parse(text) : null;
  if (!res.ok) throw new ApiError(res.status, data?.detail ?? text);
  return data;
}
