"""Ihyaa curriculum: halal, evidence-backed daily micro-habits.

Every template carries Quran / Hadith grounding and a clinical-science note.
Content is trilingual (en / id / ar). Nothing here involves haram substances,
riba, or practices outside mainstream Sunni fiqh.
"""
from datetime import date, timedelta
import hashlib

from templates_advanced import ADVANCED_TEMPLATES
from templates_lifestyle import LIFESTYLE_TEMPLATES

PILLARS = ["spiritual", "physical", "nutrition", "mental"]

LEVELS = {"beginner": 1, "practicing": 2, "devoted": 3,
          "intermediate": 2, "advanced": 3}

# Prayer-anchored default reminder slots (local clock, 24h)
ANCHOR_TIMES = {
    "fajr": "05:15",
    "morning": "07:00",
    "dhuhr": "12:30",
    "asr": "15:45",
    "maghrib": "18:20",
    "isha": "19:45",
    "night": "21:30",
    "anytime": "09:30",
}

SLEEP_SHIFT = {"early_bird": -30, "moderate": 0, "night_owl": 45}


def T(en: str, idn: str, ar: str) -> dict:
    return {"en": en, "id": idn, "ar": ar}


TEMPLATES: list[dict] = [
    # ---------------------------------------------------------------- SPIRITUAL
    {
        "key": "s_morning_adhkar", "pillar": "spiritual", "anchor": "fajr",
        "minutes": 8, "level": 1,
        "title": T("Morning Adhkar", "Dzikir Pagi", "أذكار الصباح"),
        "desc": T(
            "After Fajr, say SubhanAllah 33x, Alhamdulillah 33x, Allahu Akbar 33x, then complete 100 with La ilaha illallah. Count on your fingers, unhurried.",
            "Setelah Subuh, ucapkan SubhanAllah 33x, Alhamdulillah 33x, Allahu Akbar 33x, lalu sempurnakan 100 dengan La ilaha illallah. Hitung dengan jari, tanpa terburu-buru.",
            "بعد الفجر: سبحان الله ٣٣، الحمد لله ٣٣، الله أكبر ٣٣، ثم أكمل المئة بلا إله إلا الله. عُدّ بأصابعك بتمهّل."),
        "hadith": T(
            "Whoever glorifies Allah 33 times, praises Him 33 times and magnifies Him 33 times after every prayer, then completes a hundred with La ilaha illallah — his sins are forgiven. (Sahih Muslim 597)",
            "Barangsiapa bertasbih 33x, bertahmid 33x, bertakbir 33x setelah setiap shalat, lalu menyempurnakan seratus dengan La ilaha illallah, diampuni dosanya. (Sahih Muslim 597)",
            "«مَن سبَّح الله ثلاثًا وثلاثين، وحمِد الله ثلاثًا وثلاثين، وكبَّر الله ثلاثًا وثلاثين، وقال تمام المئة: لا إله إلا الله... غُفرت خطاياه». (صحيح مسلم ٥٩٧)"),
        "science": T(
            "Rhythmic devotional repetition triggers Benson's relaxation response: measurable drops in cortisol (~20%) and resting blood pressure (Psychosomatic Medicine; Journal of Religion & Health, 2019).",
            "Pengulangan dzikir yang berirama memicu relaxation response Benson: penurunan kortisol terukur (~20%) dan tekanan darah istirahat (Psychosomatic Medicine; Journal of Religion & Health, 2019).",
            "التكرار الذكري المنتظم يُحدث «استجابة الاسترخاء» لبنسون: انخفاض قابل للقياس في الكورتيزول (نحو ٢٠٪) وضغط الدم (Journal of Religion & Health, 2019)."),
    },
    {
        "key": "s_quran_page", "pillar": "spiritual", "anchor": "fajr",
        "minutes": 10, "level": 1,
        "title": T("One Page of Quran, With Meaning", "Satu Halaman Al-Quran Beserta Makna", "صفحة من القرآن بتدبّر"),
        "desc": T(
            "Read one page only — then read its translation. Ask: what is Allah asking of me in this page today? Quality over quantity.",
            "Baca satu halaman saja — lalu baca terjemahannya. Tanyakan: apa yang Allah minta dariku di halaman ini hari ini? Kualitas di atas kuantitas.",
            "اقرأ صفحة واحدة فقط، ثم اقرأ معناها. واسأل: ماذا يريد الله منّي في هذه الصفحة اليوم؟ الكيف قبل الكم."),
        "quran": T(
            "\"A blessed Book We revealed to you, that they may reflect upon its verses.\" (Sad 38:29)",
            "\"Kitab yang penuh berkah Kami turunkan kepadamu agar mereka merenungkan ayat-ayatnya.\" (QS Sad 38:29)",
            "﴿كِتَابٌ أَنزَلْنَاهُ إِلَيْكَ مُبَارَكٌ لِّيَدَّبَّرُوا آيَاتِهِ﴾ (ص: ٢٩)"),
        "science": T(
            "Slow reading for meaning activates the default-mode network, improving comprehension and empathy; sacred-text reading specifically lowers existential anxiety (Neuropsychologia; Journal of Religion & Health).",
            "Membaca lambat untuk memahami mengaktifkan default-mode network, meningkatkan pemahaman dan empati; membaca kitab suci menurunkan kecemasan eksistensial (Neuropsychologia; Journal of Religion & Health).",
            "القراءة المتأنّية للفهم تُنشّط شبكة الوضع الافتراضي في الدماغ فتحسّن الاستيعاب والتعاطف، وقراءة النص المقدّس تخفّض القلق الوجودي."),
    },
    {
        "key": "s_2rakat", "pillar": "spiritual", "anchor": "dhuhr",
        "minutes": 6, "level": 1,
        "title": T("Two Rakat Sunnah", "Dua Rakaat Sunnah", "ركعتان من السنّة"),
        "desc": T(
            "Add two voluntary rakat to one fard prayer today. Two is enough — consistency beats volume.",
            "Tambahkan dua rakaat sunnah pada salah satu shalat fardhu hari ini. Dua sudah cukup — konsistensi mengalahkan jumlah.",
            "أضف ركعتين نافلة إلى إحدى فرائض اليوم. ركعتان تكفي؛ فالمداومة خير من الكثرة."),
        "hadith": T(
            "Whoever prays twelve rakat of Sunnah in a day and night, Allah will build for him a house in Paradise. (Sahih Muslim 728)",
            "Barangsiapa shalat dua belas rakaat sunnah dalam sehari-malam, Allah bangunkan untuknya rumah di surga. (Sahih Muslim 728)",
            "«مَن صلّى في يومٍ وليلةٍ ثنتَي عشرة ركعةً تطوّعًا بنى الله له بيتًا في الجنّة». (صحيح مسلم ٧٢٨)"),
        "science": T(
            "Salah's cycle of standing, bowing and prostration is graded low-impact loading: it improves lumbar flexibility, knee proprioception and balance in adults (Journal of Physical Therapy Science, 2017).",
            "Siklus berdiri, ruku', dan sujud dalam shalat adalah pembebanan bertingkat berdampak rendah: meningkatkan fleksibilitas lumbal, proprioseptif lutut, dan keseimbangan (Journal of Physical Therapy Science, 2017).",
            "حركات الصلاة (قيام، ركوع، سجود) تمرين تدريجي منخفض الأثر يحسّن مرونة أسفل الظهر والتوازن (Journal of Physical Therapy Science, 2017)."),
    },
    {
        "key": "s_istighfar", "pillar": "spiritual", "anchor": "anytime",
        "minutes": 7, "level": 1,
        "title": T("Istighfar, Spread Across the Day", "Istighfar Sepanjang Hari", "الاستغفار موزّعًا على اليوم"),
        "desc": T(
            "Say Astaghfirullah 100 times — but scattered: in traffic, in queues, between tasks. Turn dead time into worship.",
            "Ucapkan Astaghfirullah 100x — namun tersebar: saat di jalan, mengantre, di antara pekerjaan. Ubah waktu kosong menjadi ibadah.",
            "قل «أستغفر الله» مئة مرة موزّعة: في الطريق، في الانتظار، بين الأعمال. حوّل الوقت الضائع إلى عبادة."),
        "hadith": T(
            "By Allah, I seek Allah's forgiveness and repent to Him more than seventy times a day. (Sahih al-Bukhari 6307)",
            "Demi Allah, sungguh aku beristighfar dan bertaubat kepada-Nya lebih dari tujuh puluh kali sehari. (Sahih Bukhari 6307)",
            "«والله إنّي لأستغفر الله وأتوب إليه في اليوم أكثر من سبعين مرة». (صحيح البخاري ٦٣٠٧)"),
        "science": T(
            "Brief repeated phrases distributed through the day reduce amygdala reactivity and rumination more than one long session (Neuroscience & Biobehavioral Reviews, 2018).",
            "Frasa singkat berulang yang tersebar sepanjang hari menurunkan reaktivitas amigdala dan overthinking lebih baik daripada satu sesi panjang (Neuroscience & Biobehavioral Reviews, 2018).",
            "العبارات القصيرة المتكرّرة الموزّعة على اليوم تخفّض تفاعل اللوزة الدماغية والتفكير القهري أكثر من جلسة واحدة طويلة."),
    },
    {
        "key": "s_sleep_adhkar", "pillar": "spiritual", "anchor": "night",
        "minutes": 5, "level": 1,
        "title": T("Sleep Adhkar Ritual", "Ritual Dzikir Sebelum Tidur", "أذكار النوم"),
        "desc": T(
            "Make wudu, recite Ayat al-Kursi, then al-Ikhlas, al-Falaq and an-Nas into your palms and wipe over yourself. Then phone down.",
            "Berwudhu, baca Ayat Kursi, lalu al-Ikhlas, al-Falaq, an-Nas ke kedua tangan lalu usapkan ke tubuh. Setelah itu simpan ponsel.",
            "توضّأ، واقرأ آية الكرسي، ثم الإخلاص والفلق والناس في كفّيك وامسح بهما جسدك. ثم ضع الهاتف جانبًا."),
        "hadith": T(
            "The Prophet ﷺ would cup his hands, recite the three surahs, then wipe over his body — three times before sleeping. (Sahih al-Bukhari 5017)",
            "Nabi ﷺ menyatukan kedua tangannya, membaca tiga surah, lalu mengusapkannya ke tubuhnya — tiga kali sebelum tidur. (Sahih Bukhari 5017)",
            "كان النبي ﷺ يجمع كفّيه فيقرأ المعوّذات ثم يمسح بهما جسده، ثلاث مرات قبل النوم. (صحيح البخاري ٥٠١٧)"),
        "science": T(
            "A fixed pre-sleep ritual is the single strongest behavioural predictor of sleep quality: ~30% faster sleep onset and more slow-wave sleep (Sleep Medicine Reviews, 2015).",
            "Ritual tetap sebelum tidur adalah prediktor perilaku terkuat kualitas tidur: onset tidur ~30% lebih cepat dan slow-wave sleep lebih banyak (Sleep Medicine Reviews, 2015).",
            "الروتين الثابت قبل النوم أقوى مؤشّر سلوكي لجودة النوم: سرعة الغفو أعلى بنحو ٣٠٪ ونوم عميق أكثر (Sleep Medicine Reviews, 2015)."),
    },
    {
        "key": "s_dhikr_walk", "pillar": "spiritual", "anchor": "maghrib",
        "minutes": 12, "level": 1,
        "title": T("Walking Dhikr", "Dzikir Sambil Berjalan", "ذكر أثناء المشي"),
        "desc": T(
            "Walk and sync dhikr to your steps: left foot \"La ilaha\", right foot \"illallah\". Cardio and remembrance in one.",
            "Berjalan sambil menyelaraskan dzikir dengan langkah: kaki kiri \"La ilaha\", kaki kanan \"illallah\". Kardio dan dzikir sekaligus.",
            "امشِ ووافق الذكر خطواتك: القدم اليسرى «لا إله»، اليمنى «إلا الله». رياضة وذكر في وقت واحد."),
        "quran": T(
            "\"Those who remember Allah standing, sitting and lying on their sides.\" (Ali 'Imran 3:191)",
            "\"(Yaitu) orang-orang yang mengingat Allah sambil berdiri, duduk, atau berbaring.\" (QS Ali Imran 3:191)",
            "﴿الَّذِينَ يَذْكُرُونَ اللَّهَ قِيَامًا وَقُعُودًا وَعَلَىٰ جُنُوبِهِمْ﴾ (آل عمران: ١٩١)"),
        "science": T(
            "Mantra-synchronised walking lowers stress hormones ~25% more than walking or sitting meditation alone, while delivering the same cardiovascular dose (Mindfulness, 2020).",
            "Berjalan yang diselaraskan dengan dzikir menurunkan hormon stres ~25% lebih baik daripada berjalan atau meditasi duduk saja, dengan manfaat kardio yang sama (Mindfulness, 2020).",
            "المشي المتزامن مع الذكر يخفض هرمونات التوتر بنحو ٢٥٪ أكثر من المشي أو التأمّل وحده، مع الفائدة القلبية نفسها."),
    },
    {
        "key": "s_salawat", "pillar": "spiritual", "anchor": "anytime",
        "minutes": 7, "level": 1,
        "title": T("One Hundred Salawat", "Seratus Kali Shalawat", "مئة صلاة على النبي"),
        "desc": T(
            "Send salawat on the Prophet ﷺ 100 times today, scattered through commutes and waiting time.",
            "Bershalawat kepada Nabi ﷺ 100x hari ini, tersebar saat perjalanan dan waktu menunggu.",
            "صلِّ على النبي ﷺ مئة مرة اليوم، موزّعة في التنقّل وأوقات الانتظار."),
        "hadith": T(
            "Whoever sends one blessing upon me, Allah sends ten blessings upon him. (Sahih Muslim 408)",
            "Barangsiapa bershalawat kepadaku sekali, Allah bershalawat untuknya sepuluh kali. (Sahih Muslim 408)",
            "«مَن صلّى عليَّ صلاةً صلّى الله عليه بها عشرًا». (صحيح مسلم ٤٠٨)"),
        "science": T(
            "Repeating a short affirming phrase raises prefrontal activity linked to wellbeing and reduces amygdala threat response by ~15% (NeuroImage, 2016).",
            "Mengulang frasa positif singkat meningkatkan aktivitas prefrontal terkait kesejahteraan dan menurunkan respons ancaman amigdala ~15% (NeuroImage, 2016).",
            "تكرار عبارة قصيرة مطمئنة يرفع نشاط القشرة الجبهية المرتبط بالسكينة ويخفض استجابة التهديد نحو ١٥٪."),
    },
    {
        "key": "s_sadaqah", "pillar": "spiritual", "anchor": "anytime",
        "minutes": 5, "level": 1,
        "title": T("Give Sadaqah Today", "Bersedekah Hari Ini", "صدقة اليوم"),
        "desc": T(
            "Give something today — money, food, a lift, removing a hazard from the road, or simply a sincere smile.",
            "Berikan sesuatu hari ini — uang, makanan, tumpangan, memindahkan gangguan dari jalan, atau sekadar senyum yang tulus.",
            "تصدّق اليوم بشيء: مال، طعام، توصيل، إزالة أذى من الطريق، أو ابتسامة صادقة."),
        "hadith": T(
            "Your smile in your brother's face is charity; removing a hazard from the road is charity. (Jami' at-Tirmidhi 1956)",
            "Senyummu di hadapan saudaramu adalah sedekah; menyingkirkan bahaya dari jalan adalah sedekah. (Tirmidzi 1956)",
            "«تبسّمك في وجه أخيك صدقة، وإزالتك الأذى عن الطريق صدقة». (سنن الترمذي ١٩٥٦)"),
        "science": T(
            "Prosocial giving activates ventral striatum reward circuits and correlates with lower blood pressure and 24% higher reported happiness (Nature Communications, 2017).",
            "Memberi secara prososial mengaktifkan sirkuit penghargaan ventral striatum dan berkorelasi dengan tekanan darah lebih rendah serta kebahagiaan 24% lebih tinggi (Nature Communications, 2017).",
            "العطاء الاجتماعي يُنشّط دوائر المكافأة في المخ ويرتبط بانخفاض ضغط الدم وارتفاع السعادة نحو ٢٤٪."),
    },
    {
        "key": "s_mulk", "pillar": "spiritual", "anchor": "night",
        "minutes": 7, "level": 2,
        "title": T("Surah Al-Mulk Before Sleep", "Surah Al-Mulk Sebelum Tidur", "سورة الملك قبل النوم"),
        "desc": T(
            "Recite Surah Al-Mulk (67) — thirty verses, about seven minutes. Make it your nightly anchor.",
            "Bacalah Surah Al-Mulk (67) — tiga puluh ayat, sekitar tujuh menit. Jadikan ini penanda malam Anda.",
            "اقرأ سورة الملك (٦٧): ثلاثون آية في نحو سبع دقائق. اجعلها موعدك الليلي الثابت."),
        "hadith": T(
            "There is a surah of thirty verses that will plead for its companion until he is forgiven — Surah al-Mulk. (Jami' at-Tirmidhi 2891)",
            "Ada satu surah tiga puluh ayat yang akan memberi syafaat bagi pembacanya sampai ia diampuni — Surah al-Mulk. (Tirmidzi 2891)",
            "«سورةٌ من القرآن ما هي إلا ثلاثون آية خاصمت عن صاحبها حتى أدخلته الجنة، وهي سورة تبارك». (الترمذي ٢٨٩١)"),
        "science": T(
            "Reciting familiar text before bed reduces pre-sleep cognitive arousal, the main driver of insomnia, and shortens sleep latency (Journal of Religion & Health, 2021).",
            "Membaca teks yang sudah dikenal sebelum tidur menurunkan cognitive arousal pra-tidur, pemicu utama insomnia, dan mempercepat tertidur (Journal of Religion & Health, 2021).",
            "قراءة نص مألوف قبل النوم تخفّض الاستثارة الذهنية، وهي السبب الأول للأرق، وتسرّع الغفو."),
    },
    {
        "key": "s_tahajjud", "pillar": "spiritual", "anchor": "night",
        "minutes": 15, "level": 3,
        "title": T("Tahajjud: Two Rakat", "Tahajjud: Dua Rakaat", "التهجّد: ركعتان"),
        "desc": T(
            "Set your alarm 20 minutes before Fajr. Pray two unhurried rakat and make dua in the last third of the night.",
            "Setel alarm 20 menit sebelum Subuh. Shalat dua rakaat dengan tenang dan berdoa di sepertiga malam terakhir.",
            "اضبط منبّهك عشرين دقيقة قبل الفجر. صلِّ ركعتين بتمهّل وادعُ في الثلث الأخير من الليل."),
        "quran": T(
            "\"And rise at night for prayer — an extra act of worship for you.\" (Al-Isra 17:79)",
            "\"Dan bangunlah pada sebagian malam untuk shalat sebagai ibadah tambahan bagimu.\" (QS Al-Isra 17:79)",
            "﴿وَمِنَ اللَّيْلِ فَتَهَجَّدْ بِهِ نَافِلَةً لَّكَ﴾ (الإسراء: ٧٩)"),
        "science": T(
            "The 3–5am window coincides with the cortisol awakening rise, so brief structured practice then improves alertness without the sleep debt of full early rising, provided total sleep stays ≥6.5h (Chronobiology International).",
            "Rentang 03.00–05.00 bertepatan dengan naiknya kortisol pagi, sehingga praktik singkat terstruktur meningkatkan kewaspadaan tanpa utang tidur, asalkan total tidur tetap ≥6,5 jam (Chronobiology International).",
            "الفترة ٣–٥ صباحًا تتوافق مع ارتفاع الكورتيزول الصباحي، فتُحسّن الممارسة القصيرة اليقظة دون دَين نوم، بشرط ألا يقلّ النوم عن ٦٫٥ ساعة."),
    },

    # ---------------------------------------------------------------- PHYSICAL
    {
        "key": "p_walk_fajr", "pillar": "physical", "anchor": "fajr",
        "minutes": 10, "level": 1,
        "title": T("Walk After Fajr", "Jalan Kaki Setelah Subuh", "المشي بعد الفجر"),
        "desc": T(
            "A gentle 10-minute walk after Fajr in early daylight. No phone, no pace target — just move and breathe.",
            "Jalan santai 10 menit setelah Subuh di cahaya pagi. Tanpa ponsel, tanpa target kecepatan — bergerak dan bernapas saja.",
            "امشِ بلطف عشر دقائق بعد الفجر في ضوء الصباح. بلا هاتف ولا هدف سرعة؛ تحرّك وتنفّس فقط."),
        "hadith": T(
            "O Allah, bless my Ummah in their early mornings. (Sunan Abi Dawud 2606)",
            "Ya Allah, berkahilah umatku pada waktu pagi mereka. (Sunan Abu Dawud 2606)",
            "«اللهم بارك لأمّتي في بكورها». (سنن أبي داود ٢٦٠٦)"),
        "science": T(
            "10–20 minutes of morning outdoor light advances the circadian clock, raising daytime alertness and improving sleep onset the same night (Sleep Health, 2017).",
            "10–20 menit cahaya pagi di luar ruangan memajukan jam sirkadian, meningkatkan kewaspadaan siang dan mempercepat tidur malam yang sama (Sleep Health, 2017).",
            "التعرّض للضوء الطبيعي ١٠–٢٠ دقيقة صباحًا يُقدّم الساعة البيولوجية فيرفع اليقظة نهارًا ويسرّع النوم ليلًا."),
    },
    {
        "key": "p_stretch", "pillar": "physical", "anchor": "morning",
        "minutes": 5, "level": 1,
        "title": T("Five-Minute Mobility", "Mobilitas Lima Menit", "خمس دقائق مرونة"),
        "desc": T(
            "Neck rolls, shoulder circles, hamstring reach, hip-flexor lunge. Hold each 20 seconds, breathe out into the stretch.",
            "Putar leher, lingkarkan bahu, jangkau hamstring, lunge hip-flexor. Tahan 20 detik, buang napas saat meregang.",
            "لفّ الرقبة، دوائر الكتف، مدّ أوتار الركبة، فتح مثنية الورك. اثبت ٢٠ ثانية مع إخراج النفس."),
        "science": T(
            "Daily static stretching raises range of motion 15–25% within four weeks and cuts musculoskeletal injury risk about 30% (ACSM Position Stand).",
            "Peregangan statis harian meningkatkan rentang gerak 15–25% dalam empat minggu dan menurunkan risiko cedera muskuloskeletal sekitar 30% (ACSM).",
            "التمدّد الثابت اليومي يرفع مدى الحركة ١٥–٢٥٪ خلال أربعة أسابيع ويقلّل خطر الإصابات نحو ٣٠٪."),
    },
    {
        "key": "p_wudu_mobility", "pillar": "physical", "anchor": "dhuhr",
        "minutes": 4, "level": 1,
        "title": T("Wudu Joint Reset", "Reset Sendi Saat Wudhu", "تحرير المفاصل مع الوضوء"),
        "desc": T(
            "Attach mobility to wudu: 5 slow neck rolls each way, 10 shoulder shrugs, 10 wrist circles. Habit stacking on an existing habit.",
            "Tempelkan mobilitas pada wudhu: 5 putaran leher tiap arah, 10 angkat bahu, 10 putaran pergelangan. Menumpuk kebiasaan baru pada kebiasaan lama.",
            "اربط المرونة بالوضوء: ٥ لفّات رقبة لكل جهة، ١٠ رفعات كتف، ١٠ دورات معصم. بناء عادة على عادة قائمة."),
        "science": T(
            "Anchoring a new micro-behaviour to an existing cue ('habit stacking') roughly doubles 8-week adherence versus time-based reminders (Health Psychology Review, 2016).",
            "Menautkan perilaku mikro baru pada pemicu yang sudah ada ('habit stacking') hampir menggandakan kepatuhan 8 minggu dibanding pengingat berbasis waktu (Health Psychology Review, 2016).",
            "ربط سلوك صغير جديد بمحفّز قائم يضاعف تقريبًا الالتزام خلال ثمانية أسابيع مقارنة بالتنبيهات الزمنية."),
    },
    {
        "key": "p_walk_mosque", "pillar": "physical", "anchor": "maghrib",
        "minutes": 15, "level": 1,
        "title": T("Walk to the Masjid", "Berjalan ke Masjid", "المشي إلى المسجد"),
        "desc": T(
            "Walk to the masjid for one prayer today (or walk 15 minutes toward a longer route home). Every step counts twice.",
            "Berjalan ke masjid untuk satu shalat hari ini (atau berjalan 15 menit lewat rute lebih panjang). Setiap langkah bernilai dua kali.",
            "امشِ إلى المسجد لصلاة واحدة اليوم (أو امشِ ١٥ دقيقة في طريق أطول). كل خطوة تُحسب مرتين."),
        "hadith": T(
            "For every step he takes toward the mosque a good deed is written for him. (Sahih Muslim 654)",
            "Setiap langkah menuju masjid dicatat sebagai satu kebaikan. (Sahih Muslim 654)",
            "«ما خطا خطوةً إلا رُفعت له بها درجةٌ وحُطّت عنه بها خطيئة». (صحيح مسلم ٦٥٤)"),
        "science": T(
            "Roughly 30 minutes of daily walking cuts cardiovascular event risk 30–40% and is the most sustainable dose for beginners (Harvard Nurses' Health Study; Circulation).",
            "Sekitar 30 menit jalan kaki harian menurunkan risiko kejadian kardiovaskular 30–40% dan merupakan dosis paling lestari bagi pemula (Circulation).",
            "نحو ٣٠ دقيقة مشي يوميًا تقلّل خطر أحداث القلب ٣٠–٤٠٪، وهي الجرعة الأكثر استدامة للمبتدئين."),
    },
    {
        "key": "p_bodyweight", "pillar": "physical", "anchor": "asr",
        "minutes": 12, "level": 2,
        "title": T("Bodyweight Circuit", "Sirkuit Berat Badan", "دائرة تمارين بوزن الجسم"),
        "desc": T(
            "Three rounds: 10 squats, 8 push-ups (knees are fine), 20-second plank. Rest 30 seconds between rounds.",
            "Tiga putaran: 10 squat, 8 push-up (boleh lutut menyentuh), plank 20 detik. Istirahat 30 detik antar putaran.",
            "ثلاث دورات: ١٠ قرفصاء، ٨ ضغط (على الركبتين مقبول)، ٢٠ ثانية بلانك. راحة ٣٠ ثانية بين الدورات."),
        "hadith": T(
            "The strong believer is better and more beloved to Allah than the weak believer — though both are good. (Sahih Muslim 2664)",
            "Mukmin yang kuat lebih baik dan lebih dicintai Allah daripada mukmin yang lemah — meski keduanya baik. (Sahih Muslim 2664)",
            "«المؤمن القويّ خير وأحبّ إلى الله من المؤمن الضعيف، وفي كلٍّ خير». (صحيح مسلم ٢٦٦٤)"),
        "science": T(
            "30–60 minutes of resistance training per week — not per day — is associated with ~20% lower all-cause mortality (British Journal of Sports Medicine, 2022 meta-analysis).",
            "Latihan beban 30–60 menit per minggu — bukan per hari — dikaitkan dengan mortalitas semua sebab ~20% lebih rendah (British Journal of Sports Medicine, 2022).",
            "٣٠–٦٠ دقيقة تدريب مقاومة أسبوعيًا (لا يوميًا) ترتبط بانخفاض الوفيات لجميع الأسباب نحو ٢٠٪."),
    },
    {
        "key": "p_core", "pillar": "physical", "anchor": "asr",
        "minutes": 9, "level": 2,
        "title": T("Core for a Stronger Sujud", "Inti Tubuh untuk Sujud Lebih Kuat", "تقوية الجذع لسجود أقوى"),
        "desc": T(
            "Three rounds: 20-second plank, 10 bird-dogs, 10 dead bugs. Your lower back carries you through long qiyam.",
            "Tiga putaran: plank 20 detik, 10 bird-dog, 10 dead bug. Punggung bawah Anda menopang qiyam yang panjang.",
            "ثلاث دورات: بلانك ٢٠ ثانية، ١٠ «بيرد دوج»، ١٠ «ديد باغ». أسفل ظهرك هو ما يحملك في القيام الطويل."),
        "science": T(
            "Targeted core stabilisation reduces chronic low-back pain intensity by ~43% and improves standing endurance (Journal of Physical Therapy Science, 2019).",
            "Stabilisasi inti tubuh terarah menurunkan intensitas nyeri punggung bawah kronis ~43% dan meningkatkan daya tahan berdiri (Journal of Physical Therapy Science, 2019).",
            "تمارين تثبيت الجذع تقلّل شدّة آلام أسفل الظهر المزمنة نحو ٤٣٪ وتزيد تحمّل الوقوف."),
    },
    {
        "key": "p_stairs", "pillar": "physical", "anchor": "anytime",
        "minutes": 8, "level": 1,
        "title": T("Stairs & Movement Snacks", "Tangga & Gerak Selingan", "السلالم ووجبات الحركة"),
        "desc": T(
            "No lifts today. Plus: stand and move for two minutes for every 30 minutes you sit.",
            "Hindari lift hari ini. Tambahan: berdiri dan bergerak dua menit setiap 30 menit duduk.",
            "لا مصاعد اليوم. وأيضًا: قف وتحرّك دقيقتين مقابل كل ثلاثين دقيقة جلوس."),
        "science": T(
            "Breaking up sitting every 30 minutes flattens post-meal glucose spikes by ~24% and lowers inflammatory markers (Diabetes Care, 2016).",
            "Memecah waktu duduk setiap 30 menit meratakan lonjakan glukosa pascamakan ~24% dan menurunkan penanda inflamasi (Diabetes Care, 2016).",
            "تقطيع الجلوس كل ثلاثين دقيقة يخفّض قفزات السكر بعد الأكل نحو ٢٤٪ ويقلّل مؤشّرات الالتهاب."),
    },
    {
        "key": "p_breath", "pillar": "physical", "anchor": "dhuhr",
        "minutes": 5, "level": 1,
        "title": T("4-7-8 Breathing After Salah", "Napas 4-7-8 Setelah Shalat", "تنفّس ٤-٧-٨ بعد الصلاة"),
        "desc": T(
            "Still on the prayer mat: inhale 4 counts, hold 7, exhale slowly for 8. Four rounds, then dua.",
            "Masih di sajadah: tarik napas 4 hitungan, tahan 7, buang perlahan 8. Empat putaran, lalu berdoa.",
            "وأنت على السجّادة: شهيق ٤، حبس ٧، زفير بطيء ٨. أربع دورات، ثم دعاء."),
        "quran": T(
            "\"Surely in the remembrance of Allah do hearts find rest.\" (Ar-Ra'd 13:28)",
            "\"Ingatlah, hanya dengan mengingat Allah hati menjadi tenang.\" (QS Ar-Ra'd 13:28)",
            "﴿أَلَا بِذِكْرِ اللَّهِ تَطْمَئِنُّ الْقُلُوبُ﴾ (الرعد: ٢٨)"),
        "science": T(
            "Extended-exhale breathing raises vagal tone, cutting state anxiety up to 37% and lowering resting heart rate within minutes (Frontiers in Human Neuroscience, 2018).",
            "Napas dengan hembusan panjang meningkatkan tonus vagal, menurunkan kecemasan hingga 37% dan menurunkan denyut jantung dalam beberapa menit (Frontiers in Human Neuroscience, 2018).",
            "التنفّس بزفير مُطوّل يرفع النغمة المبهمية فيخفّض القلق حتى ٣٧٪ ويهدّئ النبض في دقائق."),
    },
    {
        "key": "p_balance", "pillar": "physical", "anchor": "anytime",
        "minutes": 5, "level": 2,
        "title": T("Balance & Ankle Strength", "Keseimbangan & Kekuatan Pergelangan Kaki", "التوازن وقوّة الكاحل"),
        "desc": T(
            "Stand on one leg for 30 seconds, switch. Three rounds each side. Brush your teeth while doing it.",
            "Berdiri satu kaki 30 detik, lalu ganti. Tiga putaran tiap sisi. Bisa dilakukan sambil menyikat gigi.",
            "قف على قدم واحدة ٣٠ ثانية ثم بدّل. ثلاث دورات لكل جهة. يمكنك فعلها أثناء تنظيف الأسنان."),
        "science": T(
            "Single-leg balance capacity independently predicts all-cause mortality; balance training cuts fall risk about 40% (British Journal of Sports Medicine, 2022).",
            "Kemampuan berdiri satu kaki secara independen memprediksi mortalitas; latihan keseimbangan menurunkan risiko jatuh sekitar 40% (British Journal of Sports Medicine, 2022).",
            "القدرة على الوقوف على قدم واحدة مؤشّر مستقل للوفيات، وتدريب التوازن يقلّل خطر السقوط نحو ٤٠٪."),
    },
    {
        "key": "p_interval", "pillar": "physical", "anchor": "asr",
        "minutes": 15, "level": 3,
        "title": T("Interval Brisk Walk", "Jalan Cepat Interval", "مشي متقطّع سريع"),
        "desc": T(
            "Alternate 3 minutes easy with 2 minutes brisk, three times. You should be slightly breathless but able to talk.",
            "Bergantian 3 menit santai dan 2 menit cepat, tiga kali. Sedikit terengah namun masih bisa berbicara.",
            "بادل بين ٣ دقائق هادئة و٢ دقيقة سريعة، ثلاث مرات. يكون النفس أعلى قليلًا مع القدرة على الكلام."),
        "science": T(
            "Interval walking training improves VO2max about 20% more than continuous walking of equal duration (British Journal of Sports Medicine).",
            "Latihan jalan interval meningkatkan VO2max sekitar 20% lebih besar daripada jalan kontinu dengan durasi sama (British Journal of Sports Medicine).",
            "المشي المتقطّع يحسّن السعة الهوائية نحو ٢٠٪ أكثر من المشي المتواصل بالمدّة نفسها."),
    },

    # ---------------------------------------------------------------- NUTRITION
    {
        "key": "n_water_sips", "pillar": "nutrition", "anchor": "fajr",
        "minutes": 2, "level": 1,
        "title": T("Water, Seated, in Three Sips", "Air, Duduk, Tiga Tegukan", "الماء جالسًا على ثلاث دفعات"),
        "desc": T(
            "First thing after waking: sit, say Bismillah, drink a glass in three unhurried sips, say Alhamdulillah.",
            "Hal pertama setelah bangun: duduk, ucapkan Bismillah, minum segelas dalam tiga tegukan tenang, ucapkan Alhamdulillah.",
            "أول ما تستيقظ: اجلس، وقل بسم الله، واشرب كأسًا على ثلاث دفعات بتمهّل، ثم قل الحمد لله."),
        "hadith": T(
            "Do not gulp like a camel; drink in two or three breaths, saying Bismillah and Alhamdulillah. (Jami' at-Tirmidhi 1885)",
            "Jangan minum sekali teguk seperti unta; minumlah dua atau tiga kali tarikan napas, dengan Bismillah dan Alhamdulillah. (Tirmidzi 1885)",
            "«لا تشربوا واحدًا كشرب البعير، ولكن اشربوا مثنى وثلاثًا، وسمّوا إذا شربتم واحمدوا إذا رفعتم». (الترمذي ١٨٨٥)"),
        "science": T(
            "Rehydrating on waking raises metabolic rate around 24% for the next 90 minutes and reverses the 2% overnight deficit that impairs cognition (Journal of Clinical Endocrinology & Metabolism).",
            "Rehidrasi saat bangun meningkatkan laju metabolisme sekitar 24% selama 90 menit dan memulihkan defisit 2% semalam yang menurunkan kognisi (J Clin Endocrinol Metab).",
            "شرب الماء عند الاستيقاظ يرفع معدّل الأيض نحو ٢٤٪ لتسعين دقيقة ويعوّض نقص ٢٪ الليلي الذي يضعف التركيز."),
    },
    {
        "key": "n_dates", "pillar": "nutrition", "anchor": "maghrib",
        "minutes": 3, "level": 1,
        "title": T("Three Dates Instead of a Sweet", "Tiga Kurma Ganti Camilan Manis", "ثلاث تمرات بدل الحلوى"),
        "desc": T(
            "Swap today's sugary snack for three dates and water. Odd number, unhurried, with gratitude.",
            "Gantikan camilan manis hari ini dengan tiga kurma dan air. Jumlah ganjil, tanpa tergesa, dengan syukur.",
            "استبدل حلوى اليوم بثلاث تمرات وماء. عدد وتر، بتمهّل، وبشكر."),
        "hadith": T(
            "When one of you breaks his fast, let him break it with dates, for they are a blessing. (Sunan Abi Dawud 2355)",
            "Apabila salah seorang berbuka, berbukalah dengan kurma, karena ia berkah. (Sunan Abu Dawud 2355)",
            "«إذا أفطر أحدكم فليُفطر على التمر فإنه بركة». (سنن أبي داود ٢٣٥٥)"),
        "science": T(
            "Dates deliver ~6.7g fibre per 100g with a low-to-moderate glycaemic index, so they blunt the glucose spike a refined-sugar snack causes (Nutrition Journal, 2011).",
            "Kurma menyediakan ~6,7g serat per 100g dengan indeks glikemik rendah-sedang, sehingga menumpulkan lonjakan glukosa dibanding camilan gula olahan (Nutrition Journal, 2011).",
            "التمر يقدّم نحو ٦٫٧غ ألياف لكل ١٠٠غ بمؤشّر سكري منخفض إلى متوسط، فيخفّف قفزة السكر مقارنة بالحلوى المصنّعة."),
    },
    {
        "key": "n_third_rule", "pillar": "nutrition", "anchor": "dhuhr",
        "minutes": 12, "level": 1,
        "title": T("The One-Third Rule", "Aturan Sepertiga", "قاعدة الثلث"),
        "desc": T(
            "At one meal today: one third food, one third water, one third air. Stop while you could still eat more.",
            "Pada satu waktu makan hari ini: sepertiga makanan, sepertiga air, sepertiga udara. Berhenti saat masih bisa makan lagi.",
            "في وجبة واحدة اليوم: ثلث طعام، ثلث شراب، ثلث للنَّفس. توقّف وأنت قادر على الزيادة."),
        "hadith": T(
            "If he must eat more, then one third for food, one third for drink and one third for breath. (Jami' at-Tirmidhi 2380)",
            "Jika harus lebih, maka sepertiga untuk makanan, sepertiga untuk minuman, sepertiga untuk napas. (Tirmidzi 2380)",
            "«فإن كان لا بدّ فاعلًا فثلثٌ لطعامه وثلثٌ لشرابه وثلثٌ لنفسه». (الترمذي ٢٣٨٠)"),
        "science": T(
            "Eating to ~80% fullness (hara hachi bu) is the core caloric-restriction behaviour linked to lower metabolic-syndrome prevalence in Okinawan cohorts (Ageing Research Reviews).",
            "Makan hingga ~80% kenyang (hara hachi bu) adalah inti perilaku pembatasan kalori yang dikaitkan dengan sindrom metabolik lebih rendah pada kohort Okinawa (Ageing Research Reviews).",
            "الأكل حتى ٨٠٪ من الشبع هو جوهر تقييد السعرات المرتبط بانخفاض متلازمة التمثيل الغذائي في دراسات أوكيناوا."),
    },
    {
        "key": "n_olive", "pillar": "nutrition", "anchor": "dhuhr",
        "minutes": 2, "level": 1,
        "title": T("Add Olive Oil", "Tambahkan Minyak Zaitun", "أضف زيت الزيتون"),
        "desc": T(
            "One tablespoon of extra-virgin olive oil over your salad, rice or bread today. Raw, not fried.",
            "Satu sendok makan minyak zaitun extra virgin pada salad, nasi, atau roti hari ini. Mentah, bukan digoreng.",
            "ملعقة كبيرة من زيت الزيتون البكر على السلطة أو الأرز أو الخبز اليوم. نيّئًا لا مقليًّا."),
        "quran": T(
            "\"...lit from a blessed tree, an olive, whose oil almost glows though untouched by fire.\" (An-Nur 24:35)",
            "\"...dari pohon yang berkah, zaitun, yang minyaknya hampir menerangi walau tak disentuh api.\" (QS An-Nur 24:35)",
            "﴿يُوقَدُ مِن شَجَرَةٍ مُّبَارَكَةٍ زَيْتُونَةٍ... يَكَادُ زَيْتُهَا يُضِيءُ وَلَوْ لَمْ تَمْسَسْهُ نَارٌ﴾ (النور: ٣٥)"),
        "science": T(
            "In the PREDIMED randomised trial, ~4 tbsp/day of extra-virgin olive oil cut major cardiovascular events about 30% (New England Journal of Medicine, 2018 re-analysis).",
            "Dalam uji acak PREDIMED, ~4 sdm/hari minyak zaitun extra virgin menurunkan kejadian kardiovaskular mayor sekitar 30% (NEJM, analisis ulang 2018).",
            "في تجربة PREDIMED العشوائية، خفّض نحو ٤ ملاعق يوميًا من زيت الزيتون البكر أحداث القلب الكبرى نحو ٣٠٪."),
    },
    {
        "key": "n_honey", "pillar": "nutrition", "anchor": "morning",
        "minutes": 3, "level": 1,
        "title": T("Honey in Warm Water", "Madu dalam Air Hangat", "عسل في ماء دافئ"),
        "desc": T(
            "A teaspoon of raw honey in warm — never boiling — water. Warm water preserves the enzymes; boiling destroys them.",
            "Satu sendok teh madu murni dalam air hangat — jangan mendidih. Air hangat menjaga enzimnya; air mendidih merusaknya.",
            "ملعقة صغيرة من العسل الخام في ماء دافئ لا مغليّ. الدفء يحفظ الإنزيمات، والغليان يدمّرها."),
        "quran": T(
            "\"From their bellies comes a drink of varying colours in which there is healing for people.\" (An-Nahl 16:69)",
            "\"Dari perutnya keluar minuman beraneka warna, di dalamnya terdapat obat bagi manusia.\" (QS An-Nahl 16:69)",
            "﴿يَخْرُجُ مِن بُطُونِهَا شَرَابٌ مُّخْتَلِفٌ أَلْوَانُهُ فِيهِ شِفَاءٌ لِّلنَّاسِ﴾ (النحل: ٦٩)"),
        "science": T(
            "Cochrane reviews find honey shortens acute cough duration in children and speeds burn/wound healing; it also acts as a prebiotic for gut bifidobacteria.",
            "Tinjauan Cochrane menemukan madu memperpendek durasi batuk akut pada anak dan mempercepat penyembuhan luka bakar; juga bersifat prebiotik bagi bifidobakteri usus.",
            "مراجعات كوكرين تجد أن العسل يقصّر مدّة الكحّة الحادّة عند الأطفال ويسرّع شفاء الجروح، ويعمل كمادة أوّلية نافعة لبكتيريا الأمعاء."),
    },
    {
        "key": "n_mindful", "pillar": "nutrition", "anchor": "maghrib",
        "minutes": 15, "level": 1,
        "title": T("Eat Without a Screen", "Makan Tanpa Layar", "الأكل بلا شاشة"),
        "desc": T(
            "One meal today: Bismillah, right hand, no phone, no TV. Chew properly. Notice when you are actually full.",
            "Satu waktu makan hari ini: Bismillah, tangan kanan, tanpa ponsel, tanpa TV. Kunyah dengan baik. Sadari kapan benar-benar kenyang.",
            "وجبة واحدة اليوم: بسم الله، بيمينك، بلا هاتف ولا تلفاز. امضغ جيّدًا، ولاحظ متى تشبع فعلًا."),
        "hadith": T(
            "Say Bismillah, eat with your right hand, and eat from what is nearest to you. (Sahih al-Bukhari 5376)",
            "Sebutlah nama Allah, makanlah dengan tangan kanan, dan makanlah dari yang terdekat denganmu. (Sahih Bukhari 5376)",
            "«سمِّ الله، وكُل بيمينك، وكُل مما يليك». (صحيح البخاري ٥٣٧٦)"),
        "science": T(
            "Screen-free, slow eating cuts intake roughly 25% at the same reported satiety and significantly reduces binge episodes (Harvard Health; Appetite, 2020).",
            "Makan lambat tanpa layar menurunkan asupan sekitar 25% pada rasa kenyang yang sama dan menurunkan episode makan berlebih (Appetite, 2020).",
            "الأكل البطيء بلا شاشات يقلّل الكمية نحو ٢٥٪ مع الشبع نفسه ويخفّض نُهام الأكل بشكل ملحوظ."),
    },
    {
        "key": "n_blackseed", "pillar": "nutrition", "anchor": "morning",
        "minutes": 2, "level": 2,
        "title": T("Black Seed (Habbatus Sauda)", "Habbatus Sauda (Jintan Hitam)", "الحبّة السوداء"),
        "desc": T(
            "Half a teaspoon of black seed, or its oil, with honey or on food. Consistency matters more than dose.",
            "Setengah sendok teh jintan hitam, atau minyaknya, bersama madu atau di atas makanan. Konsistensi lebih penting dari dosis.",
            "نصف ملعقة صغيرة من الحبّة السوداء أو زيتها مع العسل أو على الطعام. الاستمرار أهم من الكمّية."),
        "hadith": T(
            "In the black seed there is a cure for every disease except death. (Sahih al-Bukhari 5688)",
            "Pada habbatus sauda ada obat bagi setiap penyakit kecuali kematian. (Sahih Bukhari 5688)",
            "«في الحبّة السوداء شفاء من كل داء إلا السام». (صحيح البخاري ٥٦٨٨)"),
        "science": T(
            "Randomised trials of Nigella sativa thymoquinone show modest but consistent reductions in fasting glucose, LDL and systolic blood pressure (Journal of Ethnopharmacology meta-analyses).",
            "Uji acak Nigella sativa (timokuinon) menunjukkan penurunan moderat namun konsisten pada glukosa puasa, LDL, dan tekanan darah sistolik (meta-analisis Journal of Ethnopharmacology).",
            "تجارب عشوائية على الثيموكينون في حبّة البركة تُظهر انخفاضًا متواضعًا ومتّسقًا في سكر الصيام والكوليسترول الضار وضغط الدم."),
    },
    {
        "key": "n_veg", "pillar": "nutrition", "anchor": "dhuhr",
        "minutes": 5, "level": 1,
        "title": T("One Extra Serving of Vegetables", "Satu Porsi Sayur Tambahan", "حصّة خضار إضافية"),
        "desc": T(
            "Add one more vegetable serving to any meal today. Pick a different colour from what you usually eat.",
            "Tambahkan satu porsi sayur pada waktu makan mana pun hari ini. Pilih warna yang berbeda dari biasanya.",
            "أضف حصّة خضار واحدة إلى أي وجبة اليوم، واختر لونًا مختلفًا عمّا تأكله عادة."),
        "quran": T(
            "\"He causes crops to grow for you, and olives, date palms, grapes and every kind of fruit.\" (An-Nahl 16:11)",
            "\"Dia menumbuhkan untukmu tanaman, zaitun, kurma, anggur, dan segala macam buah.\" (QS An-Nahl 16:11)",
            "﴿يُنبِتُ لَكُم بِهِ الزَّرْعَ وَالزَّيْتُونَ وَالنَّخِيلَ وَالْأَعْنَابَ وَمِن كُلِّ الثَّمَرَاتِ﴾ (النحل: ١١)"),
        "science": T(
            "Each extra daily serving of vegetables lowers cardiovascular risk about 10%, with benefit plateauing near five servings (Lancet, 2017 pooled analysis).",
            "Setiap porsi sayur harian tambahan menurunkan risiko kardiovaskular sekitar 10%, dengan manfaat mendatar di sekitar lima porsi (Lancet, 2017).",
            "كل حصّة خضار يومية إضافية تقلّل خطر أمراض القلب نحو ١٠٪، ويستقرّ النفع قرب خمس حصص."),
    },
    {
        "key": "n_nosugar", "pillar": "nutrition", "anchor": "anytime",
        "minutes": 5, "level": 2,
        "title": T("No Added Sugar Today", "Hari Tanpa Gula Tambahan", "يوم بلا سكر مضاف"),
        "desc": T(
            "No added sugar for 24 hours. Sweeten with dates or fruit instead. Read one label before you buy it.",
            "Tanpa gula tambahan selama 24 jam. Manisi dengan kurma atau buah. Baca satu label sebelum membeli.",
            "لا سكر مضاف لمدة ٢٤ ساعة. حلِّ بالتمر أو الفاكهة، واقرأ ملصق منتج واحد قبل شرائه."),
        "science": T(
            "Keeping added sugar below 25g/day is associated with about 36% lower cardiovascular mortality versus high-intake groups (JAMA Internal Medicine, 2014).",
            "Menjaga gula tambahan di bawah 25g/hari dikaitkan dengan mortalitas kardiovaskular sekitar 36% lebih rendah dibanding asupan tinggi (JAMA Internal Medicine, 2014).",
            "إبقاء السكر المضاف تحت ٢٥غ يوميًا يرتبط بانخفاض وفيات القلب نحو ٣٦٪ مقارنة بالاستهلاك العالي."),
    },
    {
        "key": "n_sunnah_fast", "pillar": "nutrition", "anchor": "fajr",
        "minutes": 6, "level": 3,
        "title": T("Sunnah Fast (Mon / Thu)", "Puasa Sunnah (Senin/Kamis)", "صيام السنّة (الاثنين/الخميس)"),
        "desc": T(
            "Fast today if it is Monday or Thursday and your health allows. Break it with dates and water. Skip if you are ill, pregnant or nursing.",
            "Berpuasa hari ini jika Senin atau Kamis dan kondisi kesehatan mengizinkan. Berbuka dengan kurma dan air. Lewati jika sakit, hamil, atau menyusui.",
            "صم اليوم إن كان اثنينًا أو خميسًا وسمحت صحّتك. أفطر على تمر وماء. اترك الصيام إن كنت مريضًا أو حاملًا أو مرضعًا."),
        "hadith": T(
            "The Prophet ﷺ used to fast Mondays and Thursdays. (Sunan an-Nasa'i 2361)",
            "Nabi ﷺ biasa berpuasa Senin dan Kamis. (Sunan an-Nasa'i 2361)",
            "كان النبي ﷺ يصوم يوم الاثنين والخميس. (سنن النسائي ٢٣٦١)"),
        "science": T(
            "Intermittent fasting upregulates autophagy — the cellular clean-up pathway for which Ohsumi won the 2016 Nobel Prize — and improves insulin sensitivity (New England Journal of Medicine, 2019).",
            "Puasa intermiten meningkatkan autofagi — jalur pembersihan sel yang membuat Ohsumi meraih Nobel 2016 — dan memperbaiki sensitivitas insulin (NEJM, 2019).",
            "الصيام المتقطّع يحفّز «البلعمة الذاتية» التي نال أوسومي عليها نوبل ٢٠١٦، ويحسّن حساسية الإنسولين."),
    },

    # ---------------------------------------------------------------- MENTAL
    {
        "key": "m_gratitude", "pillar": "mental", "anchor": "isha",
        "minutes": 5, "level": 1,
        "title": T("Three Specific Shukr", "Tiga Syukur yang Spesifik", "ثلاث نِعم محدّدة"),
        "desc": T(
            "Write three things you thank Allah for — specific ones. Not \"my family\" but \"my mother called to check on me\".",
            "Tuliskan tiga hal yang Anda syukuri — yang spesifik. Bukan \"keluargaku\" tetapi \"ibuku menelepon menanyakan kabarku\".",
            "اكتب ثلاث نِعم تشكر الله عليها، محدّدة لا عامّة: ليس «أهلي» بل «أمّي اتصلت تسأل عنّي»."),
        "quran": T(
            "\"If you are grateful, I will surely increase you.\" (Ibrahim 14:7)",
            "\"Jika kamu bersyukur, niscaya Aku akan menambah nikmat kepadamu.\" (QS Ibrahim 14:7)",
            "﴿لَئِن شَكَرْتُمْ لَأَزِيدَنَّكُمْ﴾ (إبراهيم: ٧)"),
        "science": T(
            "Specific gratitude journaling raises wellbeing scores ~25% and reduces depressive symptoms in RCTs; specificity matters more than length (Journal of Personality & Social Psychology).",
            "Jurnal syukur yang spesifik meningkatkan skor kesejahteraan ~25% dan menurunkan gejala depresi pada uji acak; kekhususan lebih penting daripada panjangnya.",
            "تدوين الشكر المحدّد يرفع مؤشّرات السعادة نحو ٢٥٪ ويخفّض أعراض الاكتئاب، والتحديد أهم من الطول."),
    },
    {
        "key": "m_niyyah", "pillar": "mental", "anchor": "fajr",
        "minutes": 4, "level": 1,
        "title": T("Set Three Intentions", "Tetapkan Tiga Niat", "اكتب ثلاث نيّات"),
        "desc": T(
            "Before opening your phone, write three intentions for today, each beginning \"For the sake of Allah, I intend to...\"",
            "Sebelum membuka ponsel, tulis tiga niat hari ini, masing-masing dimulai \"Demi Allah, aku berniat untuk...\"",
            "قبل أن تفتح هاتفك، اكتب ثلاث نيّات لليوم، تبدأ كل واحدة بـ«لله تعالى، أنوي أن...»."),
        "hadith": T(
            "Actions are only by intentions, and every person will have what he intended. (Sahih al-Bukhari 1)",
            "Amal itu bergantung pada niat, dan setiap orang mendapat sesuai yang ia niatkan. (Sahih Bukhari 1)",
            "«إنما الأعمال بالنيّات، وإنما لكل امرئٍ ما نوى». (صحيح البخاري ١)"),
        "science": T(
            "Written implementation intentions raise goal completion by roughly 40% compared with unwritten goals (Gollwitzer meta-analysis, Advances in Experimental Social Psychology).",
            "Niat implementasi yang dituliskan meningkatkan penyelesaian tujuan sekitar 40% dibanding tujuan yang tidak dituliskan (meta-analisis Gollwitzer).",
            "النيّات المكتوبة ترفع إنجاز الأهداف نحو ٤٠٪ مقارنة بالأهداف غير المكتوبة."),
    },
    {
        "key": "m_muraqaba", "pillar": "mental", "anchor": "anytime",
        "minutes": 5, "level": 1,
        "title": T("Five Minutes of Muraqaba", "Lima Menit Muraqabah", "خمس دقائق مراقبة"),
        "desc": T(
            "Sit still, eyes closed, attention on the breath. When the mind drifts, return gently — that returning is the practice.",
            "Duduk tenang, mata terpejam, perhatian pada napas. Saat pikiran melayang, kembalilah dengan lembut — kembali itulah latihannya.",
            "اجلس ساكنًا، مغمض العينين، وانتباهك على النفس. وإذا شرد الذهن فعُد برفق؛ فالعودة هي التمرين."),
        "science": T(
            "Eight weeks of brief daily mindfulness lowers anxiety 30–40% and increases hippocampal grey-matter density on MRI (Psychiatry Research: Neuroimaging, Harvard/MGH).",
            "Delapan minggu mindfulness harian singkat menurunkan kecemasan 30–40% dan meningkatkan densitas grey matter hipokampus pada MRI (Psychiatry Research: Neuroimaging).",
            "ثمانية أسابيع من التأمّل اليومي القصير تخفّض القلق ٣٠–٤٠٪ وتزيد كثافة المادة الرمادية في الحُصين."),
    },
    {
        "key": "m_digital", "pillar": "mental", "anchor": "isha",
        "minutes": 30, "level": 2,
        "title": T("Digital Quiet Window", "Jendela Sepi Digital", "نافذة هدوء رقمي"),
        "desc": T(
            "One phone-free hour after Isha. Put the device in another room. Read, talk to family, or sit in silence.",
            "Satu jam tanpa ponsel setelah Isya. Letakkan perangkat di ruangan lain. Membaca, berbicara dengan keluarga, atau duduk dalam sepi.",
            "ساعة بلا هاتف بعد العشاء. اترك الجهاز في غرفة أخرى، واقرأ أو تحدّث مع أهلك أو اجلس في صمت."),
        "science": T(
            "Cutting social-media use by an hour a day reduced depressive symptoms about 35% in a randomised undergraduate trial (Journal of Social & Clinical Psychology, 2018).",
            "Mengurangi media sosial satu jam per hari menurunkan gejala depresi sekitar 35% dalam uji acak mahasiswa (Journal of Social & Clinical Psychology, 2018).",
            "تقليل استخدام مواقع التواصل ساعة يوميًا خفّض أعراض الاكتئاب نحو ٣٥٪ في تجربة عشوائية."),
    },
    {
        "key": "m_tafakkur", "pillar": "mental", "anchor": "asr",
        "minutes": 10, "level": 1,
        "title": T("Tafakkur Outdoors", "Tafakur di Alam Terbuka", "تفكّر في الخارج"),
        "desc": T(
            "Ten minutes outside with no phone. Watch one thing closely — a tree, clouds, birds — and let it point you to the Creator.",
            "Sepuluh menit di luar tanpa ponsel. Perhatikan satu hal dengan saksama — pohon, awan, burung — dan biarkan itu menunjuk kepada Sang Pencipta.",
            "عشر دقائق في الخارج بلا هاتف. تأمّل شيئًا واحدًا عن قرب: شجرة، سحابًا، طائرًا، ودعه يدلّك على الخالق."),
        "quran": T(
            "\"Indeed in the creation of the heavens and the earth are signs for people of understanding.\" (Ali 'Imran 3:190)",
            "\"Sungguh dalam penciptaan langit dan bumi terdapat tanda-tanda bagi orang yang berakal.\" (QS Ali Imran 3:190)",
            "﴿إِنَّ فِي خَلْقِ السَّمَاوَاتِ وَالْأَرْضِ... لَآيَاتٍ لِّأُولِي الْأَلْبَابِ﴾ (آل عمران: ١٩٠)"),
        "science": T(
            "Twenty minutes of nature contact lowers salivary cortisol ~21% per hour and measurably restores directed attention (Frontiers in Psychology, 2019).",
            "Dua puluh menit kontak dengan alam menurunkan kortisol saliva ~21% per jam dan memulihkan atensi terarah (Frontiers in Psychology, 2019).",
            "عشرون دقيقة في الطبيعة تخفّض الكورتيزول نحو ٢١٪ في الساعة وتُجدّد الانتباه الموجّه."),
    },
    {
        "key": "m_forgive", "pillar": "mental", "anchor": "isha",
        "minutes": 8, "level": 2,
        "title": T("Forgive One Person", "Maafkan Satu Orang", "اعفُ عن شخص واحد"),
        "desc": T(
            "Bring one person who wronged you to mind, forgive them in your heart, and make one dua for their good.",
            "Hadirkan satu orang yang pernah menyakiti Anda, maafkan dalam hati, dan doakan satu kebaikan untuknya.",
            "استحضر شخصًا أساء إليك، واعفُ عنه في قلبك، وادعُ له بخير مرّة واحدة."),
        "quran": T(
            "\"Let them pardon and forgive. Do you not wish that Allah should forgive you?\" (An-Nur 24:22)",
            "\"Hendaklah mereka memaafkan dan berlapang dada. Tidakkah kamu ingin Allah mengampunimu?\" (QS An-Nur 24:22)",
            "﴿وَلْيَعْفُوا وَلْيَصْفَحُوا أَلَا تُحِبُّونَ أَن يَغْفِرَ اللَّهُ لَكُمْ﴾ (النور: ٢٢)"),
        "science": T(
            "Forgiveness interventions lower systolic blood pressure by 5–10 mmHg and reduce chronic-pain interference by ~20% (American Psychological Association reviews).",
            "Intervensi pemaafan menurunkan tekanan darah sistolik 5–10 mmHg dan menurunkan gangguan nyeri kronis ~20% (tinjauan American Psychological Association).",
            "برامج التسامح تخفض ضغط الدم الانقباضي ٥–١٠ ملم زئبق وتقلّل تأثير الألم المزمن نحو ٢٠٪."),
    },
    {
        "key": "m_kindness", "pillar": "mental", "anchor": "anytime",
        "minutes": 10, "level": 1,
        "title": T("One Deliberate Kindness", "Satu Kebaikan yang Disengaja", "إحسان مقصود واحد"),
        "desc": T(
            "Do one planned kind act today that costs you something — time, effort, or a little money. Tell no one.",
            "Lakukan satu kebaikan terencana hari ini yang menuntut pengorbanan — waktu, tenaga, atau sedikit uang. Jangan beri tahu siapa pun.",
            "افعل إحسانًا مقصودًا اليوم يكلّفك شيئًا: وقتًا أو جهدًا أو مالًا قليلًا، ولا تُخبر أحدًا."),
        "hadith": T(
            "The most beloved people to Allah are those most beneficial to people. (al-Mu'jam al-Awsat, at-Tabarani)",
            "Manusia yang paling dicintai Allah adalah yang paling bermanfaat bagi manusia. (al-Mu'jam al-Awsat, Thabrani)",
            "«أحبّ الناس إلى الله أنفعهم للناس». (المعجم الأوسط للطبراني)"),
        "science": T(
            "Performing acts of kindness for seven days raises life satisfaction more than receiving them, and reduces social anxiety in RCTs (Journal of Social Psychology, 2019).",
            "Melakukan kebaikan selama tujuh hari meningkatkan kepuasan hidup lebih dari menerimanya, dan menurunkan kecemasan sosial pada uji acak (Journal of Social Psychology, 2019).",
            "أداء أعمال لطف لسبعة أيام يرفع الرضا عن الحياة أكثر من تلقّيها، ويخفّض القلق الاجتماعي."),
    },
    {
        "key": "m_worry", "pillar": "mental", "anchor": "isha",
        "minutes": 9, "level": 2,
        "title": T("Sort Your Worries", "Pilah Kekhawatiran Anda", "فرز الهموم"),
        "desc": T(
            "List today's worries in two columns: in my control, not in my control. Act on column one; hand column two to Allah.",
            "Tuliskan kekhawatiran hari ini dalam dua kolom: dalam kendaliku, di luar kendaliku. Kerjakan kolom satu; serahkan kolom dua kepada Allah.",
            "اكتب هموم اليوم في عمودين: ما يخصّني وما لا أملكه. اعمل بالأول، وسلّم الثاني إلى الله."),
        "quran": T(
            "\"Whoever puts his trust in Allah, He is sufficient for him.\" (At-Talaq 65:3)",
            "\"Barangsiapa bertawakal kepada Allah, Dia akan mencukupinya.\" (QS At-Talaq 65:3)",
            "﴿وَمَن يَتَوَكَّلْ عَلَى اللَّهِ فَهُوَ حَسْبُهُ﴾ (الطلاق: ٣)"),
        "science": T(
            "Sorting worries by controllability is a core CBT technique that cuts rumination ~40% and intrusive thoughts significantly (Journal of Experimental Psychology).",
            "Memilah kekhawatiran berdasarkan kendali adalah teknik inti CBT yang menurunkan ruminasi ~40% dan pikiran mengganggu secara signifikan (Journal of Experimental Psychology).",
            "فرز الهموم بحسب القدرة على التحكّم تقنية أساسية في العلاج المعرفي تقلّل التفكير القهري نحو ٤٠٪."),
    },
    {
        "key": "m_read", "pillar": "mental", "anchor": "night",
        "minutes": 15, "level": 1,
        "title": T("Fifteen Minutes Off-Screen Reading", "Lima Belas Menit Membaca Non-Layar", "خمس عشرة دقيقة قراءة ورقية"),
        "desc": T(
            "Read paper, not a screen, for fifteen minutes. Seerah, tafsir, or any beneficial knowledge.",
            "Membaca buku cetak, bukan layar, selama lima belas menit. Sirah, tafsir, atau ilmu bermanfaat apa pun.",
            "اقرأ من ورق لا من شاشة خمس عشرة دقيقة: سيرة أو تفسيرًا أو أي علم نافع."),
        "quran": T(
            "\"Read! In the name of your Lord who created.\" (Al-'Alaq 96:1)",
            "\"Bacalah dengan nama Tuhanmu yang menciptakan.\" (QS Al-'Alaq 96:1)",
            "﴿اقْرَأْ بِاسْمِ رَبِّكَ الَّذِي خَلَقَ﴾ (العلق: ١)"),
        "science": T(
            "Six minutes of reading lowers stress markers ~68%, more than music or walking; regular reading is linked to slower cognitive decline (University of Sussex; Neurology, 2013).",
            "Enam menit membaca menurunkan penanda stres ~68%, lebih baik daripada musik atau berjalan; membaca rutin dikaitkan dengan penurunan kognitif lebih lambat (Neurology, 2013).",
            "ست دقائق من القراءة تخفّض مؤشّرات التوتر نحو ٦٨٪، أكثر من الموسيقى أو المشي، والقراءة المنتظمة تبطئ التدهور المعرفي."),
    },
    {
        "key": "m_muhasabah", "pillar": "mental", "anchor": "night",
        "minutes": 8, "level": 1,
        "title": T("Evening Muhasabah", "Muhasabah Malam", "محاسبة الليل"),
        "desc": T(
            "Three questions before sleep: what went well, what slipped, what will I do differently tomorrow. Then istighfar and let the day close.",
            "Tiga pertanyaan sebelum tidur: apa yang baik, apa yang terlewat, apa yang akan kulakukan berbeda besok. Lalu istighfar dan tutup hari.",
            "ثلاثة أسئلة قبل النوم: ما أحسنتُ فيه، وما أخطأت، وما سأغيّره غدًا. ثم استغفر وأغلق اليوم."),
        "hadith": T(
            "Take account of yourselves before you are called to account. (Reported from 'Umar ibn al-Khattab)",
            "Hisablah diri kalian sebelum kalian dihisab. (Diriwayatkan dari Umar bin Khattab)",
            "«حاسبوا أنفسكم قبل أن تُحاسبوا». (أثرٌ عن عمر بن الخطاب رضي الله عنه)"),
        "science": T(
            "Fifteen minutes of end-of-day reflective writing improved performance by 23% over ten days versus practice alone (Harvard Business School working paper, 2014).",
            "Lima belas menit tulisan reflektif di akhir hari meningkatkan kinerja 23% dalam sepuluh hari dibanding hanya berlatih (Harvard Business School, 2014).",
            "خمس عشرة دقيقة من الكتابة التأمّلية في نهاية اليوم رفعت الأداء ٢٣٪ خلال عشرة أيام مقارنة بالتدريب وحده."),
    },
]

TEMPLATES += ADVANCED_TEMPLATES
TEMPLATES += LIFESTYLE_TEMPLATES

# Personal-fit metadata for the original pools (lifestyle templates carry their own).
BOOST_PATCH = {
    "n_water_sips": ["bp_focus", "more_energy"], "n_third_rule": ["weight_focus", "glucose_focus"],
    "n_olive": ["lipid_focus", "bp_focus"], "n_blackseed": ["glucose_focus", "lipid_focus", "bp_focus"],
    "n_veg": ["bp_focus", "healthy_eating", "weight_focus"], "n_nosugar": ["weight_focus", "glucose_focus", "low_sugar"],
    "n_honey": ["gut_focus"], "n_mindful": ["weight_focus", "gut_focus"], "n_dates": ["low_sugar", "more_energy"],
    "n_talbina": ["lipid_focus", "gut_focus"], "n_protein": ["build_strength", "gain_focus"],
    "n_cook_home": ["weight_focus", "healthy_eating"], "n_no_processed": ["bp_focus", "weight_focus"],
    "n_labels": ["low_sugar", "glucose_focus"],
    "p_walk_fajr": ["sleep_focus", "weight_focus", "joint_friendly"], "p_stretch": ["joint_friendly", "desk_worker"],
    "p_wudu_mobility": ["desk_worker", "joint_friendly"], "p_walk_mosque": ["weight_focus", "bp_focus", "joint_friendly"],
    "p_bodyweight": ["build_strength"], "p_core": ["joint_friendly", "desk_worker"],
    "p_breath": ["calm_focus", "bp_focus"], "p_balance": ["balance_focus", "joint_friendly"],
    "p_stairs": ["desk_worker", "weight_focus"], "p_steps_target": ["weight_focus", "glucose_focus"],
    "p_mobility_flow": ["joint_friendly"], "p_posture": ["desk_worker"], "p_long_walk": ["weight_focus"],
    "m_gratitude": ["calm_focus"], "m_muraqaba": ["calm_focus", "mental_clarity"],
    "m_digital": ["sleep_focus", "insomnia"], "m_tafakkur": ["calm_focus"], "m_worry": ["calm_focus"],
    "m_read": ["mental_clarity"], "m_muhasabah": ["mental_clarity"], "m_silence": ["calm_focus"],
    "s_sleep_adhkar": ["sleep_focus"], "s_mulk": ["sleep_focus", "insomnia"],
}
CONTRA_PATCH = {
    "p_interval": ["no_hiit"], "p_pushup_ladder": ["joint_friendly"],
    "n_sunnah_fast": ["no_fasting"], "n_ayyam_bid": ["no_fasting"], "n_eating_window": ["no_fasting"],
    "s_tahajjud": ["insomnia", "shift_worker"],
}
for _t in TEMPLATES:
    _t.setdefault("min_phase", 1)
    _t.setdefault("boost", BOOST_PATCH.get(_t["key"], []))
    _t.setdefault("contra", CONTRA_PATCH.get(_t["key"], []))

TEMPLATES_BY_KEY = {t["key"]: t for t in TEMPLATES}
TEMPLATES_BY_PILLAR: dict[str, list[dict]] = {p: [] for p in PILLARS}
for _t in sorted(TEMPLATES, key=lambda x: (x["min_phase"], x["level"])):
    TEMPLATES_BY_PILLAR[_t["pillar"]].append(_t)


# --------------------------------------------------------------------- phases

PHASE_DEFS: dict[str, list[dict]] = {
    "30_days": [
        {"days": 30,
         "name": T("Foundation", "Fondasi", "التأسيس"),
         "desc": T("Two-minute habits until they stop feeling like effort.",
                   "Kebiasaan dua menit sampai tidak lagi terasa berat.",
                   "عادات من دقيقتين حتى تزول عنها المشقّة.")},
    ],
    "100_days": [
        {"days": 25,
         "name": T("Foundation", "Fondasi", "التأسيس"),
         "desc": T("Small and daily. We are building the floor you will stand on.",
                   "Kecil dan harian. Kita sedang membangun lantai tempat Anda berdiri.",
                   "صغير ويومي؛ نبني الأرض التي ستقف عليها.")},
        {"days": 25,
         "name": T("Depth", "Kedalaman", "العمق"),
         "desc": T("The same habits, but now with understanding — meaning before quantity.",
                   "Kebiasaan yang sama, kini dengan pemahaman — makna sebelum jumlah.",
                   "العادات نفسها لكن بفهم؛ المعنى قبل الكم.")},
        {"days": 25,
         "name": T("Strength", "Kekuatan", "القوّة"),
         "desc": T("Load increases: real training, real fasting, real discipline.",
                   "Beban meningkat: latihan sungguhan, puasa sungguhan, disiplin sungguhan.",
                   "يزيد الحمل: تدريب حقيقي وصيام حقيقي وانتظام حقيقي.")},
        {"days": 25,
         "name": T("Istiqamah", "Istiqamah", "الاستقامة"),
         "desc": T("Nothing new. Just proof that it holds without motivation.",
                   "Tidak ada yang baru. Hanya bukti bahwa ia bertahan tanpa motivasi.",
                   "لا جديد؛ فقط إثبات أنها تثبت بلا حماسة.")},
    ],
    "1_year": [
        {"days": 30, "name": T("Foundation", "Fondasi", "التأسيس"),
         "desc": T("Start absurdly small. Show up, that is all.",
                   "Mulai sangat kecil. Cukup hadir, itu saja.",
                   "ابدأ صغيرًا جدًّا؛ يكفي أن تحضر.")},
        {"days": 30, "name": T("Discipline", "Kedisiplinan", "الالتزام"),
         "desc": T("Fixed times, fixed places. Remove every decision.",
                   "Waktu tetap, tempat tetap. Hilangkan setiap keputusan.",
                   "أوقات ثابتة وأماكن ثابتة؛ أزل كل قرار.")},
        {"days": 30, "name": T("Purity", "Kesucian", "الطهارة"),
         "desc": T("Clean your intake — food, screens, speech, company.",
                   "Bersihkan asupan Anda — makanan, layar, ucapan, pergaulan.",
                   "طهّر ما يدخلك: طعامًا وشاشة وكلامًا وصحبة.")},
        {"days": 30, "name": T("Strength", "Kekuatan", "القوّة"),
         "desc": T("Build a body that can carry long qiyam and long walks.",
                   "Bangun tubuh yang mampu menopang qiyam dan perjalanan panjang.",
                   "ابنِ جسدًا يحمل قيامًا طويلًا ومشيًا طويلًا.")},
        {"days": 30, "name": T("Stillness", "Ketenangan", "السكينة"),
         "desc": T("Learn to sit with silence without reaching for the phone.",
                   "Belajar duduk dalam sunyi tanpa meraih ponsel.",
                   "تعلّم الجلوس مع الصمت دون أن تمتدّ يدك للهاتف.")},
        {"days": 30, "name": T("Generosity", "Kedermawanan", "الكرم"),
         "desc": T("Give until giving becomes reflex rather than decision.",
                   "Memberi sampai memberi menjadi refleks, bukan keputusan.",
                   "أعطِ حتى يصير العطاء طبعًا لا قرارًا.")},
        {"days": 30, "name": T("Knowledge", "Ilmu", "العلم"),
         "desc": T("Twenty minutes a day of something beneficial, every day.",
                   "Dua puluh menit sehari untuk sesuatu yang bermanfaat, setiap hari.",
                   "عشرون دقيقة يوميًا في علم نافع، كل يوم.")},
        {"days": 30, "name": T("Patience", "Kesabaran", "الصبر"),
         "desc": T("The hard middle. This phase is deliberately unglamorous.",
                   "Bagian tengah yang berat. Fase ini memang tidak menarik.",
                   "الوسط الشاقّ؛ هذه المرحلة غير برّاقة بقصد.")},
        {"days": 30, "name": T("Gratitude", "Syukur", "الشكر"),
         "desc": T("Count what you were given before you count what is missing.",
                   "Hitung yang telah diberikan sebelum menghitung yang belum ada.",
                   "عُدّ ما أُعطيت قبل أن تعدّ ما فقدت.")},
        {"days": 30, "name": T("Service", "Pengabdian", "الخدمة"),
         "desc": T("Turn your health outward: be useful to people.",
                   "Arahkan kesehatan Anda ke luar: bermanfaat bagi orang lain.",
                   "وجّه صحّتك للخارج: كن نافعًا للناس.")},
        {"days": 30, "name": T("Depth", "Kedalaman", "العمق"),
         "desc": T("Tahajjud, i'tikaf, long fasts. Only if the base is solid.",
                   "Tahajud, i'tikaf, puasa panjang. Hanya jika fondasinya kuat.",
                   "تهجّد واعتكاف وصيام أطول، بشرط ثبات الأساس.")},
        {"days": 35, "name": T("Istiqamah", "Istiqamah", "الاستقامة"),
         "desc": T("A whole year in. Now it is simply who you are.",
                   "Satu tahun penuh. Sekarang ini memang siapa diri Anda.",
                   "سنة كاملة؛ الآن هذه هي هُويّتك.")},
    ],
}


def phase_of(day: int, challenge_type: str) -> tuple[int, dict, int, int]:
    """Return (1-based phase index, phase def, phase start day, phase end day)."""
    defs = PHASE_DEFS.get(challenge_type) or PHASE_DEFS["30_days"]
    cursor = 0
    for i, ph in enumerate(defs):
        start = cursor + 1
        end = cursor + ph["days"]
        if day <= end or i == len(defs) - 1:
            return i + 1, ph, start, end
        cursor = end
    return 1, defs[0], 1, defs[0]["days"]


def phase_summary(day: int, challenge_type: str, lang: str) -> dict:
    lang = lang if lang in ("en", "id") else "en"
    defs = PHASE_DEFS.get(challenge_type) or PHASE_DEFS["30_days"]
    index, ph, start, end = phase_of(day, challenge_type)
    return {
        "index": index,
        "total": len(defs),
        "name": ph["name"].get(lang) or ph["name"]["en"],
        "description": ph["desc"].get(lang) or ph["desc"]["en"],
        "start_day": start,
        "end_day": end,
        "day_in_phase": max(1, day - start + 1),
        "phase_days": end - start + 1,
    }


# --------------------------------------------------------------------- helpers

GOAL_PILLAR_WEIGHT = {
    "weight_loss": ["physical", "nutrition"],
    "build_strength": ["physical"],
    "better_sleep": ["mental", "spiritual"],
    "reduce_stress": ["mental", "spiritual"],
    "healthy_eating": ["nutrition"],
    "spiritual_growth": ["spiritual"],
    "mental_clarity": ["mental"],
    "more_energy": ["physical", "nutrition"],
}


def localize(template: dict, lang: str) -> dict:
    lang = lang if lang in ("en", "id") else "en"

    def pick(field: str):
        val = template.get(field)
        if not val:
            return None
        return val.get(lang) or val.get("en")

    return {
        "template_key": template["key"],
        "pillar": template["pillar"],
        "title": pick("title"),
        "description": pick("desc"),
        "quran_reference": pick("quran"),
        "hadith_reference": pick("hadith"),
        "science_reference": pick("science"),
    }


def pillar_priority(goals: list[str]) -> list[str]:
    score = {p: 0 for p in PILLARS}
    for g in goals:
        for p in GOAL_PILLAR_WEIGHT.get(g, []):
            score[p] += 1
    # spiritual always first-class: it is the reason this app exists
    score["spiritual"] += 1
    return sorted(PILLARS, key=lambda p: (-score[p], PILLARS.index(p)))


def tasks_for_day(day: int) -> int:
    """1% better: start absurdly easy, ramp slowly."""
    if day <= 3:
        return 2
    if day <= 10:
        return 3
    if day <= 40:
        return 4
    return 5


def ramp(day: int, total_days: int) -> float:
    """Duration multiplier — early days are deliberately tiny."""
    pct = day / max(total_days, 1)
    if pct <= 0.10:
        return 0.45
    if pct <= 0.25:
        return 0.65
    if pct <= 0.50:
        return 0.85
    return 1.0


def anchor_time(anchor: str, sleep_habit: str) -> str:
    base = ANCHOR_TIMES.get(anchor, "09:30")
    shift = SLEEP_SHIFT.get(sleep_habit, 0)
    if anchor in ("fajr", "night", "isha") and shift:
        hh, mm = (int(x) for x in base.split(":"))
        total = (hh * 60 + mm + shift) % (24 * 60)
        return f"{total // 60:02d}:{total % 60:02d}"
    return base


def generate_plan(prefs: dict, total_days: int, start: date,
                  challenge_type: str = "30_days", flags: list[str] | None = None,
                  seed: str = "") -> list[dict]:
    """Deterministic, personalised 1%-better plan.

    Templates are *scored* for this person (goals, health flags, level fit,
    dietary focus) and contraindicated ones are excluded. A per-user seed
    breaks ties so two users with similar answers still get different plans.
    """
    goals = prefs.get("health_goals") or []
    order = pillar_priority(goals)
    fit_level = LEVELS.get(prefs.get("fitness_level", "beginner"), 1)
    spi_level = LEVELS.get(prefs.get("spiritual_level", "beginner"), 1)
    sleep_habit = prefs.get("sleep_habit", "moderate")
    dietary = prefs.get("dietary_preferences") or []
    flagset = set(flags or [])
    wanted = flagset | set(goals) | set(dietary)

    def salt(key: str) -> float:
        digest = hashlib.sha256(f"{seed}:{key}".encode()).hexdigest()
        return int(digest[:8], 16) / 0xFFFFFFFF

    def allowed(t: dict) -> bool:
        if set(t["contra"]) & flagset:
            return False
        if t["pillar"] == "spiritual":
            return t["level"] <= spi_level
        if t["pillar"] == "nutrition":
            if t["key"] == "n_nosugar" and "low_sugar" not in dietary and t["level"] > fit_level:
                return False
            return t["level"] <= max(fit_level, 2 if "sunnah_diet" in dietary else 1)
        return t["level"] <= fit_level

    def score(t: dict) -> float:
        s = len(wanted & set(t["boost"])) * 3.0
        if "joint_friendly" in flagset and t["pillar"] == "physical" and "joint_friendly" in t["boost"]:
            s += 2
        s -= abs(t["level"] - (spi_level if t["pillar"] == "spiritual" else fit_level)) * 0.5
        return s + salt(t["key"])

    # Longer tracks are allowed to reach deeper practices as they progress.
    def level_cap(phase: int) -> int:
        return min(3, 1 + phase) if challenge_type != "30_days" else 3

    pool_cache: dict[tuple[str, int], list[dict]] = {}

    def pool_for(pillar: str, phase: int) -> list[dict]:
        key = (pillar, phase)
        if key not in pool_cache:
            cap = level_cap(phase)
            pool = [t for t in TEMPLATES_BY_PILLAR[pillar]
                    if t["min_phase"] <= phase and allowed(t) and t["level"] <= cap]
            pool = pool or [t for t in TEMPLATES_BY_PILLAR[pillar] if t["min_phase"] <= phase][:4]
            # Best-fit first, then the long tail — the whole pool still rotates
            # so no habit repeats until every fitting one has had its turn.
            pool.sort(key=lambda t: -score(t))
            pool_cache[key] = pool
        return pool_cache[key]

    counters = {p: 0 for p in PILLARS}
    out: list[dict] = []
    last_phase = 1

    for day in range(1, total_days + 1):
        phase, _, _, _ = phase_of(day, challenge_type)
        if phase != last_phase:
            # Jump straight to whatever this phase just unlocked, so a new phase
            # genuinely feels new instead of replaying the same rotation.
            for p in PILLARS:
                fresh = [i for i, t in enumerate(pool_for(p, phase)) if t["min_phase"] == phase]
                counters[p] = fresh[0] if fresh else 0
            last_phase = phase

        n = tasks_for_day(day)
        day_pillars = [order[i % len(order)] for i in range(n)]
        scheduled = (start + timedelta(days=day - 1)).isoformat()
        difficulty = max(1, min(10, round(day / total_days * 10)))
        base_points = 8 + round(day / total_days * 14)
        mult = ramp(day, total_days)

        used_today: set[str] = set()
        for pillar in day_pillars:
            pool = pool_for(pillar, phase)
            tpl = pool[counters[pillar] % len(pool)]
            counters[pillar] += 1
            if tpl["key"] in used_today and len(pool) > 1:
                tpl = pool[counters[pillar] % len(pool)]
                counters[pillar] += 1
            used_today.add(tpl["key"])
            minutes = max(2, round(tpl["minutes"] * mult))
            out.append({
                "template_key": tpl["key"],
                "pillar": pillar,
                "day_number": day,
                "scheduled_date": scheduled,
                "scheduled_time": anchor_time(tpl["anchor"], sleep_habit),
                "anchor": tpl["anchor"],
                "duration_minutes": minutes,
                "difficulty": difficulty,
                "points_reward": base_points + tpl["level"] * 2,
            })

    return out
