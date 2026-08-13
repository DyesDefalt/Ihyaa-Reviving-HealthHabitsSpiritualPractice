"""Weekly and monthly milestones — the bigger commitments that sit above the
daily habits on the 100-Day and 1-Year tracks.
"""
from datetime import date, timedelta

from templates_advanced import T

WEEKLY_MILESTONES: list[dict] = [
    {
        "key": "w_fast_mon_thu", "pillar": "nutrition", "points": 150,
        "title": T("Fast Monday and Thursday", "Puasa Senin dan Kamis", "صم الاثنين والخميس"),
        "desc": T(
            "Keep both Sunnah fasts this week. Break each with dates and water. Skip if you are ill, pregnant or nursing.",
            "Jalankan kedua puasa sunnah pekan ini. Berbuka dengan kurma dan air. Lewati jika sakit, hamil, atau menyusui.",
            "صم سنّة الاثنين والخميس هذا الأسبوع، وأفطر على تمر وماء. واترك الصيام إن كنت مريضًا أو حاملًا أو مرضعًا."),
        "evidence": T(
            "Sunan an-Nasa'i 2361 · Two weekly fasting days improve insulin sensitivity without muscle loss (NEJM, 2019).",
            "Sunan an-Nasa'i 2361 · Dua hari puasa per pekan memperbaiki sensitivitas insulin tanpa kehilangan otot (NEJM, 2019).",
            "سنن النسائي ٢٣٦١ · يومان من الصيام أسبوعيًا يحسّنان حساسية الإنسولين دون فقد عضلي."),
    },
    {
        "key": "w_masjid_five", "pillar": "spiritual", "points": 150,
        "title": T("Five Prayers in Congregation", "Lima Shalat Berjamaah", "خمس صلوات في جماعة"),
        "desc": T(
            "Pray at least five of this week's prayers in the masjid with the congregation. Walk there if you can.",
            "Kerjakan minimal lima shalat pekan ini di masjid bersama jamaah. Berjalan ke sana jika memungkinkan.",
            "صلِّ خمس صلوات على الأقل هذا الأسبوع في المسجد مع الجماعة، وامشِ إليه إن استطعت."),
        "evidence": T(
            "Sahih Muslim 650 (congregation is 27 times better) · Walking to the masjid adds a reliable daily movement dose (Circulation).",
            "Sahih Muslim 650 (berjamaah 27 kali lebih baik) · Berjalan ke masjid menambah dosis gerak harian yang andal (Circulation).",
            "صحيح مسلم ٦٥٠ (الجماعة تفضل بسبع وعشرين درجة) · المشي إلى المسجد يضيف جرعة حركة يومية موثوقة."),
    },
    {
        "key": "w_150_minutes", "pillar": "physical", "points": 150,
        "title": T("150 Minutes of Movement", "150 Menit Bergerak", "١٥٠ دقيقة حركة"),
        "desc": T(
            "Accumulate 150 minutes of moderate activity across the week — walking counts, and it does not need to be in one go.",
            "Kumpulkan 150 menit aktivitas sedang sepanjang pekan — jalan kaki dihitung, dan tidak perlu sekali jalan.",
            "اجمع ١٥٠ دقيقة من النشاط المتوسّط خلال الأسبوع؛ المشي محسوب، ولا يلزم أن يكون متّصلًا."),
        "evidence": T(
            "WHO 2020 physical activity guideline · 150 min/week cuts all-cause mortality risk about 31%.",
            "Pedoman aktivitas fisik WHO 2020 · 150 menit/pekan menurunkan risiko mortalitas semua sebab sekitar 31%.",
            "توصية منظمة الصحة العالمية ٢٠٢٠ · ١٥٠ دقيقة أسبوعيًا تقلّل الوفيات لجميع الأسباب نحو ٣١٪."),
    },
    {
        "key": "w_sleep_seven", "pillar": "mental", "points": 150,
        "title": T("Seven Nights of Real Sleep", "Tujuh Malam Tidur Cukup", "سبع ليالٍ من نوم حقيقي"),
        "desc": T(
            "Aim for 7+ hours every night this week with the same wake time. Phone out of the bedroom.",
            "Targetkan 7+ jam setiap malam pekan ini dengan jam bangun yang sama. Ponsel di luar kamar.",
            "استهدف سبع ساعات أو أكثر كل ليلة هذا الأسبوع بوقت استيقاظ ثابت، والهاتف خارج غرفة النوم."),
        "evidence": T(
            "Quran 78:9 (\"We made your sleep for rest\") · Wake-time regularity predicts sleep quality better than total duration (Sleep, 2018).",
            "QS 78:9 (\"Kami jadikan tidurmu untuk istirahat\") · Keteraturan jam bangun memprediksi kualitas tidur lebih baik daripada total durasi (Sleep, 2018).",
            "﴿وَجَعَلْنَا نَوْمَكُمْ سُبَاتًا﴾ (النبأ: ٩) · انتظام وقت الاستيقاظ يتنبّأ بجودة النوم أفضل من مدّته."),
    },
    {
        "key": "w_sadaqah_three", "pillar": "spiritual", "points": 150,
        "title": T("Give Sadaqah Three Times", "Bersedekah Tiga Kali", "تصدّق ثلاث مرات"),
        "desc": T(
            "Three separate acts of giving this week — and let at least one of them be anonymous.",
            "Tiga tindakan memberi terpisah pekan ini — dan setidaknya satu di antaranya secara diam-diam.",
            "ثلاث صدقات متفرّقة هذا الأسبوع، واجعل واحدة منها على الأقل سرًّا."),
        "evidence": T(
            "Sahih al-Bukhari 1421 · Repeated small giving raises wellbeing more than one large gift (Journal of Happiness Studies).",
            "Sahih Bukhari 1421 · Memberi kecil berulang meningkatkan kesejahteraan lebih dari satu pemberian besar (Journal of Happiness Studies).",
            "صحيح البخاري ١٤٢١ · العطاء الصغير المتكرّر يرفع السعادة أكثر من عطاء كبير واحد."),
    },
    {
        "key": "w_family_meals", "pillar": "mental", "points": 150,
        "title": T("Three Screen-Free Family Meals", "Tiga Kali Makan Bersama Tanpa Layar", "ثلاث وجبات أسرية بلا شاشات"),
        "desc": T(
            "Sit and eat with your household three times this week with every screen away and every phone face-down elsewhere.",
            "Duduk dan makan bersama keluarga tiga kali pekan ini tanpa layar apa pun dan ponsel disimpan di tempat lain.",
            "اجلس وكُل مع أهلك ثلاث مرات هذا الأسبوع بلا شاشات، والهواتف بعيدة."),
        "evidence": T(
            "Sahih Muslim 2059 (eat together and you will be satisfied) · Frequent family meals lower adolescent depression and disordered eating (Pediatrics).",
            "Sahih Muslim 2059 (makanlah bersama, niscaya kalian cukup) · Makan keluarga yang rutin menurunkan depresi remaja dan gangguan makan (Pediatrics).",
            "صحيح مسلم ٢٠٥٩ (اجتمعوا على طعامكم يُبارك لكم) · الوجبات الأسرية المتكرّرة تخفّض الاكتئاب واضطرابات الأكل."),
    },
    {
        "key": "w_no_sugar_three", "pillar": "nutrition", "points": 150,
        "title": T("Three No-Added-Sugar Days", "Tiga Hari Tanpa Gula Tambahan", "ثلاثة أيام بلا سكر مضاف"),
        "desc": T(
            "Pick three days this week with zero added sugar. Dates and whole fruit are your sweetness.",
            "Pilih tiga hari pekan ini tanpa gula tambahan sama sekali. Kurma dan buah utuh sebagai pemanisnya.",
            "اختر ثلاثة أيام هذا الأسبوع بلا سكر مضاف مطلقًا، وليكن التمر والفاكهة حلواك."),
        "evidence": T(
            "Sunan Abi Dawud 2355 (break fast with dates) · Added sugar under 25g/day is linked to ~36% lower cardiovascular mortality (JAMA Intern Med, 2014).",
            "Sunan Abu Dawud 2355 (berbuka dengan kurma) · Gula tambahan di bawah 25g/hari dikaitkan mortalitas kardiovaskular ~36% lebih rendah (JAMA Intern Med, 2014).",
            "سنن أبي داود ٢٣٥٥ · السكر المضاف تحت ٢٥غ يوميًا يرتبط بانخفاض وفيات القلب نحو ٣٦٪."),
    },
    {
        "key": "w_memorise_five", "pillar": "spiritual", "points": 150,
        "title": T("Memorise Five New Ayat", "Hafal Lima Ayat Baru", "احفظ خمس آيات جديدة"),
        "desc": T(
            "Five new ayat by the end of the week, revised daily. Understand the meaning before you memorise the words.",
            "Lima ayat baru sampai akhir pekan, dimurajaah harian. Pahami maknanya sebelum menghafal lafalnya.",
            "خمس آيات جديدة بنهاية الأسبوع مع مراجعة يومية، وافهم المعنى قبل حفظ اللفظ."),
        "evidence": T(
            "Sahih al-Bukhari 5027 · Spaced retrieval is the most efficient known memory protocol (Psychological Science).",
            "Sahih Bukhari 5027 · Retrieval terjadwal adalah protokol memori paling efisien yang diketahui (Psychological Science).",
            "صحيح البخاري ٥٠٢٧ · الاسترجاع المتباعد أكفأ بروتوكول معروف للذاكرة."),
    },
    {
        "key": "w_call_kin", "pillar": "mental", "points": 150,
        "title": T("Reconnect With a Relative", "Sambung Silaturahmi", "صِل قريبًا انقطعت عنه"),
        "desc": T(
            "Call or visit one relative you have lost touch with. Do not wait for them to reach out first.",
            "Telepon atau kunjungi satu kerabat yang sudah lama tak berhubungan. Jangan menunggu mereka lebih dulu.",
            "اتّصل أو زُر قريبًا انقطعت عنه، ولا تنتظر أن يبدأ هو."),
        "evidence": T(
            "Sahih al-Bukhari 5986 · Social connection predicts survival more strongly than smoking or obesity (PLOS Medicine).",
            "Sahih Bukhari 5986 · Koneksi sosial memprediksi kelangsungan hidup lebih kuat daripada merokok atau obesitas (PLOS Medicine).",
            "صحيح البخاري ٥٩٨٦ · الترابط الاجتماعي يتنبّأ بالبقاء أقوى من التدخين والسمنة."),
    },
    {
        "key": "w_quran_pages", "pillar": "spiritual", "points": 150,
        "title": T("Ten Pages With Meaning", "Sepuluh Halaman Beserta Makna", "عشر صفحات بتدبّر"),
        "desc": T(
            "Ten pages of Quran this week, each read twice — once in Arabic and once in translation.",
            "Sepuluh halaman Al-Quran pekan ini, tiap halaman dibaca dua kali — sekali Arab, sekali terjemahan.",
            "عشر صفحات من القرآن هذا الأسبوع، كل صفحة مرتين: بالعربية ثم بالمعنى."),
        "evidence": T(
            "Quran 38:29 · Reading for meaning activates comprehension networks and lowers existential anxiety (Neuropsychologia).",
            "QS 38:29 · Membaca untuk memahami mengaktifkan jaringan pemahaman dan menurunkan kecemasan eksistensial (Neuropsychologia).",
            "﴿كِتَابٌ أَنزَلْنَاهُ إِلَيْكَ مُبَارَكٌ لِّيَدَّبَّرُوا آيَاتِهِ﴾ · القراءة للفهم تنشّط شبكات الاستيعاب وتخفّض القلق."),
    },
]

MONTHLY_MILESTONES: list[dict] = [
    {
        "key": "m_short_surah", "pillar": "spiritual", "points": 400,
        "title": T("Memorise One Short Surah", "Hafal Satu Surah Pendek", "احفظ سورة قصيرة"),
        "desc": T(
            "One complete short surah this month — al-Mulk, al-Waqi'ah, or any from Juz 30 you do not yet know.",
            "Satu surah pendek lengkap bulan ini — Al-Mulk, Al-Waqi'ah, atau surah Juz 30 yang belum Anda hafal.",
            "سورة قصيرة كاملة هذا الشهر: الملك أو الواقعة أو أي سورة من جزء عمّ لم تحفظها."),
        "evidence": T(
            "Jami' at-Tirmidhi 2891 · Memorisation builds working-memory capacity measurable on standard tests (Frontiers in Psychology).",
            "Tirmidzi 2891 · Menghafal membangun kapasitas memori kerja yang terukur pada tes standar (Frontiers in Psychology).",
            "الترمذي ٢٨٩١ · الحفظ يبني سعة الذاكرة العاملة بشكل قابل للقياس."),
    },
    {
        "key": "m_ayyam_bid", "pillar": "nutrition", "points": 400,
        "title": T("Fast the Three White Days", "Puasa Tiga Hari Ayyamul Bidh", "صم الأيام البيض الثلاثة"),
        "desc": T(
            "Fast the 13th, 14th and 15th of this Hijri month. Three days, once a month, for life.",
            "Berpuasa tanggal 13, 14, dan 15 bulan Hijriah ini. Tiga hari, sekali sebulan, seumur hidup.",
            "صم الثالث عشر والرابع عشر والخامس عشر من هذا الشهر الهجري: ثلاثة أيام كل شهر، مدى العمر."),
        "evidence": T(
            "Sunan an-Nasa'i 2422 · Three consecutive monthly fasts trigger measurable autophagy while staying sustainable (NEJM, 2019).",
            "Sunan an-Nasa'i 2422 · Tiga hari puasa berurutan bulanan memicu autofagi terukur dan tetap lestari (NEJM, 2019).",
            "سنن النسائي ٢٤٢٢ · ثلاثة أيام صيام متتالية شهريًا تحفّز البلعمة الذاتية مع الاستدامة."),
    },
    {
        "key": "m_finish_book", "pillar": "mental", "points": 400,
        "title": T("Finish One Beneficial Book", "Tuntaskan Satu Buku Bermanfaat", "أتمم كتابًا نافعًا"),
        "desc": T(
            "One book, cover to cover, this month. Seerah, tafsir, health, or a trade you want to master.",
            "Satu buku, tuntas, bulan ini. Sirah, tafsir, kesehatan, atau keahlian yang ingin Anda kuasai.",
            "كتاب واحد كاملًا هذا الشهر: سيرة أو تفسير أو صحّة أو حرفة تريد إتقانها."),
        "evidence": T(
            "Quran 96:1 · Regular readers show a 20% lower mortality risk over 12 years than non-readers (Social Science & Medicine, 2016).",
            "QS 96:1 · Pembaca rutin menunjukkan risiko mortalitas 20% lebih rendah dalam 12 tahun daripada non-pembaca (Social Science & Medicine, 2016).",
            "﴿اقْرَأْ بِاسْمِ رَبِّكَ﴾ · القرّاء المنتظمون تقلّ وفياتهم ٢٠٪ خلال ١٢ سنة مقارنة بغيرهم."),
    },
    {
        "key": "m_health_check", "pillar": "physical", "points": 400,
        "title": T("Check One Health Marker", "Periksa Satu Penanda Kesehatan", "افحص مؤشّرًا صحّيًا"),
        "desc": T(
            "Get one number measured this month: blood pressure, fasting glucose, HbA1c, vitamin D or a lipid panel. Write it down.",
            "Ukur satu angka bulan ini: tekanan darah, glukosa puasa, HbA1c, vitamin D, atau profil lipid. Catat hasilnya.",
            "قِس رقمًا واحدًا هذا الشهر: ضغط الدم، سكر الصيام، السكر التراكمي، فيتامين د، أو الدهون. وسجّله."),
        "evidence": T(
            "Sahih al-Bukhari 5678 (Allah has sent down a cure for every disease) · Self-monitoring is one of the most effective behaviour-change techniques known (Michie et al., Health Psychology).",
            "Sahih Bukhari 5678 (Allah menurunkan obat bagi setiap penyakit) · Pemantauan diri adalah salah satu teknik perubahan perilaku paling efektif (Health Psychology).",
            "صحيح البخاري ٥٦٧٨ · المراقبة الذاتية من أنجع تقنيات تغيير السلوك المعروفة."),
    },
    {
        "key": "m_recurring_sadaqah", "pillar": "spiritual", "points": 400,
        "title": T("Set Up Monthly Sadaqah", "Atur Sedekah Bulanan", "رتّب صدقة شهرية"),
        "desc": T(
            "Commit a fixed, small, automatic amount every month — small and continuous beats large and rare.",
            "Komitmenkan jumlah kecil tetap secara otomatis setiap bulan — kecil dan berkelanjutan mengalahkan besar dan jarang.",
            "التزم بمبلغ صغير ثابت تلقائي كل شهر؛ فالقليل الدائم خير من الكثير المنقطع."),
        "evidence": T(
            "Sahih al-Bukhari 6464 (the most beloved deeds are consistent ones) · Automating a commitment roughly doubles follow-through (Behavioural Public Policy).",
            "Sahih Bukhari 6464 (amal tercinta adalah yang berkelanjutan) · Mengotomatiskan komitmen hampir menggandakan pelaksanaannya (Behavioural Public Policy).",
            "صحيح البخاري ٦٤٦٤ · أتمتة الالتزام تضاعف تقريبًا الالتزام الفعلي."),
    },
    {
        "key": "m_juz_meaning", "pillar": "spiritual", "points": 400,
        "title": T("One Juz With Tafsir", "Satu Juz Beserta Tafsir", "جزء واحد مع التفسير"),
        "desc": T(
            "Complete one juz of Quran this month reading a short tafsir alongside it. About seven pages a week.",
            "Selesaikan satu juz Al-Quran bulan ini sambil membaca tafsir singkat. Sekitar tujuh halaman per pekan.",
            "أتمم جزءًا من القرآن هذا الشهر مع تفسير موجز، بنحو سبع صفحات في الأسبوع."),
        "evidence": T(
            "Quran 47:24 · Sustained deep reading strengthens the brain's language and empathy networks (Brain Connectivity, 2013).",
            "QS 47:24 · Membaca dalam secara berkelanjutan memperkuat jaringan bahasa dan empati otak (Brain Connectivity, 2013).",
            "﴿أَفَلَا يَتَدَبَّرُونَ الْقُرْآنَ﴾ · القراءة العميقة المستمرّة تقوّي شبكات اللغة والتعاطف في الدماغ."),
    },
    {
        "key": "m_learn_course", "pillar": "mental", "points": 400,
        "title": T("Complete a Short Course", "Selesaikan Satu Kursus Singkat", "أكمل دورة قصيرة"),
        "desc": T(
            "Finish one short beneficial course this month — tajweed, Arabic grammar, first aid, or a work skill.",
            "Tuntaskan satu kursus singkat bermanfaat bulan ini — tajwid, nahwu, pertolongan pertama, atau keahlian kerja.",
            "أتمم دورة قصيرة نافعة هذا الشهر: تجويد، نحو، إسعاف أوّلي، أو مهارة عمل."),
        "evidence": T(
            "Sahih Muslim 2699 · Learning new skills in adulthood measurably increases cognitive reserve and delays decline (Psychological Science, 2019).",
            "Sahih Muslim 2699 · Mempelajari keterampilan baru saat dewasa meningkatkan cadangan kognitif dan menunda penurunan (Psychological Science, 2019).",
            "صحيح مسلم ٢٦٩٩ · تعلّم مهارات جديدة في الكبر يزيد الاحتياط المعرفي ويؤخّر التدهور."),
    },
]

BY_KEY = {m["key"]: m for m in WEEKLY_MILESTONES + MONTHLY_MILESTONES}

# Only the Pro tracks get milestones.
MILESTONE_TRACKS = {"100_days", "1_year"}


def localize_milestone(doc: dict, lang: str) -> dict:
    lang = lang if lang in ("en", "id", "ar") else "en"
    tpl = BY_KEY.get(doc["template_key"])

    def pick(field: str):
        v = tpl.get(field) if tpl else None
        return (v.get(lang) or v.get("en")) if v else None

    return {
        "id": str(doc["_id"]) if doc.get("_id") is not None else None,
        "template_key": doc["template_key"],
        "kind": doc["kind"],
        "index": doc["index"],
        "pillar": tpl["pillar"] if tpl else "spiritual",
        "start_date": doc["start_date"],
        "end_date": doc["end_date"],
        "points_reward": doc["points_reward"],
        "completed": doc.get("completed", False),
        "title": pick("title") or doc["template_key"],
        "description": pick("desc") or "",
        "evidence": pick("evidence"),
    }


def build_milestones(challenge_type: str, total_days: int, start: date) -> list[dict]:
    if challenge_type not in MILESTONE_TRACKS:
        return []

    out: list[dict] = []
    weeks = max(1, -(-total_days // 7))
    for i in range(weeks):
        tpl = WEEKLY_MILESTONES[i % len(WEEKLY_MILESTONES)]
        first = start + timedelta(days=i * 7)
        last = min(first + timedelta(days=6), start + timedelta(days=total_days - 1))
        out.append({
            "kind": "weekly", "index": i + 1, "template_key": tpl["key"],
            "start_date": first.isoformat(), "end_date": last.isoformat(),
            "points_reward": tpl["points"], "completed": False,
        })

    months = max(1, total_days // 28)
    for i in range(months):
        tpl = MONTHLY_MILESTONES[i % len(MONTHLY_MILESTONES)]
        first = start + timedelta(days=i * 28)
        last = min(first + timedelta(days=27), start + timedelta(days=total_days - 1))
        out.append({
            "kind": "monthly", "index": i + 1, "template_key": tpl["key"],
            "start_date": first.isoformat(), "end_date": last.isoformat(),
            "points_reward": tpl["points"], "completed": False,
        })

    return out
