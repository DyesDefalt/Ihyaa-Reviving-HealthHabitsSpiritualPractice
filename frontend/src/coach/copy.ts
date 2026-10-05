import type { Lang } from '../i18n';

const en = {
  conversations: 'Conversations', newChat: 'New conversation', deleteChat: 'Delete conversation',
  deleteTitle: 'Delete this conversation?', deleteBody: 'Its saved messages will be permanently removed from Ihyaa.',
  delete: 'Delete', cancel: 'Cancel', close: 'Close', back: 'Back', send: 'Send message',
  privacy: 'AI privacy', consentTitle: 'A small step, on your terms.',
  consentBody: 'Your messages and basic preferences are sent to OpenAI through the Emergent AI service. Your saved health records, name, email and location are not included in the profile context.',
  consentDetail: 'Avoid sharing sensitive or identifying details in chat. Conversations are saved in Ihyaa until you delete them. AI replies can be wrong and are not reviewed by a doctor or scholar.',
  consentAction: 'Agree and continue', revoke: 'Turn off AI access',
  suggestion: 'Wellbeing suggestion', safety: 'Safety guidance',
  emptyHistory: 'No conversations yet.', loading: 'Loading conversation…',
  thinking: 'Thinking…', replying: 'Replying…', retry: 'Try again',
  unavailable: 'The coach is unavailable right now. Your message is ready to try again.',
  loadError: 'We couldn’t load your conversations. Please try again.',
  busy: 'A reply is still in progress. Please wait a moment.',
  rate: 'You’ve sent several messages. Please wait a minute before trying again.',
  sessionLimit: 'You have 100 conversations. Delete an older one to start a new chat.',
  consentError: 'Please review and accept AI privacy before sending a message.',
  privacySaved: 'Your AI privacy preference has been updated.',
  notFound: 'This conversation is no longer available. Start a new conversation.',
  disclaimer: 'AI suggestions, not medical advice or religious rulings.',
};
const id: typeof en = {
  conversations: 'Percakapan', newChat: 'Percakapan baru', deleteChat: 'Hapus percakapan',
  deleteTitle: 'Hapus percakapan ini?', deleteBody: 'Pesan tersimpan akan dihapus permanen dari Ihyaa.',
  delete: 'Hapus', cancel: 'Batal', close: 'Tutup', back: 'Kembali', send: 'Kirim pesan',
  privacy: 'Privasi AI', consentTitle: 'Langkah kecil, pilihan Anda.',
  consentBody: 'Pesan dan preferensi dasar Anda dikirim ke OpenAI melalui layanan AI Emergent. Catatan kesehatan, nama, email, dan lokasi yang tersimpan tidak disertakan dalam konteks profil.',
  consentDetail: 'Hindari membagikan informasi sensitif atau identitas di chat. Percakapan disimpan di Ihyaa sampai Anda menghapusnya. Jawaban AI bisa keliru dan tidak ditinjau dokter atau ulama.',
  consentAction: 'Setuju dan lanjutkan', revoke: 'Nonaktifkan akses AI',
  suggestion: 'Saran kebugaran', safety: 'Panduan keselamatan',
  emptyHistory: 'Belum ada percakapan.', loading: 'Memuat percakapan…',
  thinking: 'Memikirkan…', replying: 'Menjawab…', retry: 'Coba lagi',
  unavailable: 'Pelatih belum tersedia. Pesan Anda siap dicoba lagi.',
  loadError: 'Percakapan tidak dapat dimuat. Silakan coba lagi.',
  busy: 'Jawaban masih diproses. Tunggu sebentar, ya.',
  rate: 'Anda telah mengirim beberapa pesan. Tunggu satu menit sebelum mencoba lagi.',
  sessionLimit: 'Anda memiliki 100 percakapan. Hapus percakapan lama untuk memulai yang baru.',
  consentError: 'Tinjau dan setujui privasi AI sebelum mengirim pesan.',
  privacySaved: 'Preferensi privasi AI Anda telah diperbarui.',
  notFound: 'Percakapan ini tidak tersedia lagi. Mulai percakapan baru.',
  disclaimer: 'Saran AI, bukan nasihat medis atau fatwa.',
};
export const coachCopy = (lang: Lang) => lang === 'id' ? id : en;
export const coachError = (code: string, lang: Lang) => {
  const c = coachCopy(lang);
  return ({ coach_rate_limit: c.rate, conversation_busy: c.busy, session_limit: c.sessionLimit,
    coach_consent_required: c.consentError, session_not_found: c.notFound,
    load_error: c.loadError } as Record<string, string>)[code] ?? c.unavailable;
};