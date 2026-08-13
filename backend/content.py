"""Static content: knowledge library + rewards store catalogue."""
from curriculum import T

KNOWLEDGE_CARDS = [
    {
        "id": "k_tibb_nabawi",
        "pillar": "spiritual",
        "category": T("Foundations", "Fondasi", "أصول"),
        "title": T("Health Is an Amanah", "Kesehatan Adalah Amanah", "الصحّة أمانة"),
        "content": T(
            "Your body is not yours to neglect — it is a trust you will be asked about. In Islam, caring for your health is not vanity; it is stewardship. This reframing is what makes the habits in Ihyaa sustainable: you are not chasing a body, you are honouring a trust.",
            "Tubuh Anda bukan milik Anda untuk diabaikan — ia adalah amanah yang akan ditanyakan. Dalam Islam, merawat kesehatan bukan kesombongan, melainkan tanggung jawab. Kerangka inilah yang membuat kebiasaan di Ihyaa bertahan: Anda bukan mengejar bentuk tubuh, Anda menjaga amanah.",
            "جسدك ليس ملكًا لك لتُهمله، بل أمانة ستُسأل عنها. والعناية بالصحّة في الإسلام ليست غرورًا بل رعاية أمانة. وهذا التأطير هو ما يجعل عادات «إحياء» مستدامة: أنت لا تطارد جسدًا، بل تصون أمانة."),
        "quran": T(
            "\"And do not kill yourselves. Indeed, Allah is Merciful to you.\" (An-Nisa 4:29)",
            "\"Dan janganlah kamu membunuh dirimu. Sungguh Allah Maha Penyayang kepadamu.\" (QS An-Nisa 4:29)",
            "﴿وَلَا تَقْتُلُوا أَنفُسَكُمْ إِنَّ اللَّهَ كَانَ بِكُمْ رَحِيمًا﴾ (النساء: ٢٩)"),
        "hadith": T(
            "There are two blessings many people squander: health and free time. (Sahih al-Bukhari 6412)",
            "Dua nikmat yang banyak dilalaikan manusia: kesehatan dan waktu luang. (Sahih Bukhari 6412)",
            "«نعمتان مغبونٌ فيهما كثيرٌ من الناس: الصحّة والفراغ». (صحيح البخاري ٦٤١٢)"),
        "science": T(
            "Health behaviours framed around identity and values persist far longer than those framed around appearance — a core finding of Self-Determination Theory (Ryan & Deci).",
            "Perilaku sehat yang dibingkai identitas dan nilai jauh lebih lestari daripada yang dibingkai penampilan — temuan inti Self-Determination Theory (Ryan & Deci).",
            "السلوكيات الصحّية المبنيّة على الهُويّة والقيم تدوم أطول بكثير من تلك المبنيّة على المظهر (نظرية التقرير الذاتي)."),
    },
    {
        "id": "k_one_percent",
        "pillar": "mental",
        "category": T("Method", "Metode", "منهج"),
        "title": T("Why Ihyaa Starts So Small", "Mengapa Ihyaa Dimulai Sangat Kecil", "لماذا يبدأ «إحياء» صغيرًا جدًّا"),
        "content": T(
            "Days 1–3 give you only two tiny tasks. That is intentional. A habit forms from repetition, not intensity — and intensity is exactly what makes people quit in week two. Ihyaa grows your load by roughly 1% a day so that by day 30 you are doing four real habits that feel effortless.",
            "Hari 1–3 hanya memberi dua tugas kecil. Itu disengaja. Kebiasaan terbentuk dari pengulangan, bukan intensitas — dan intensitas justru yang membuat orang berhenti di pekan kedua. Ihyaa menaikkan beban sekitar 1% per hari sehingga pada hari ke-30 Anda menjalankan empat kebiasaan nyata yang terasa ringan.",
            "الأيام ١–٣ فيها مهمّتان صغيرتان فقط، وهذا مقصود. العادة تُبنى بالتكرار لا بالشدّة، والشدّة هي بالضبط ما يجعل الناس ينقطعون في الأسبوع الثاني. «إحياء» يزيد الحمل نحو ١٪ يوميًا حتى تصل في اليوم الثلاثين إلى أربع عادات حقيقية بلا مشقّة."),
        "hadith": T(
            "The most beloved deeds to Allah are those done consistently, even if small. (Sahih al-Bukhari 6464)",
            "Amal yang paling dicintai Allah adalah yang dikerjakan terus-menerus meski sedikit. (Sahih Bukhari 6464)",
            "«أحبّ الأعمال إلى الله أدومها وإن قلّ». (صحيح البخاري ٦٤٦٤)"),
        "science": T(
            "Habit automaticity plateaus after a median of 66 days of repetition; missing one day does not reset progress, but reducing the behaviour's difficulty raises adherence sharply (Lally et al., European Journal of Social Psychology).",
            "Otomatisasi kebiasaan mendatar setelah median 66 hari pengulangan; melewatkan satu hari tidak mereset kemajuan, tetapi menurunkan tingkat kesulitan meningkatkan kepatuhan secara tajam (Lally et al.).",
            "تلقائية العادة تستقرّ بعد وسيط ٦٦ يومًا من التكرار، وتفويت يوم لا يُلغي التقدّم، لكن تقليل صعوبة السلوك يرفع الالتزام بحدّة."),
    },
    {
        "id": "k_sunnah_food",
        "pillar": "nutrition",
        "category": T("Sunnah Nutrition", "Nutrisi Sunnah", "غذاء نبوي"),
        "title": T("The Prophetic Pantry", "Dapur Nabawi", "مطبخ النبوّة"),
        "content": T(
            "Dates, honey, olive oil, barley (talbina), black seed, figs, milk, water. What is striking is not that these are 'superfoods' — it is that every one of them is whole, minimally processed, and low in added sugar. The Sunnah pantry is a whole-food diet centuries before the term existed.",
            "Kurma, madu, minyak zaitun, jelai (talbina), habbatus sauda, tin, susu, air. Yang mencolok bukan karena semuanya 'superfood' — melainkan karena semuanya utuh, minim olahan, dan rendah gula tambahan. Dapur Sunnah adalah pola makan whole-food berabad-abad sebelum istilah itu ada.",
            "التمر والعسل وزيت الزيتون والشعير (التلبينة) والحبّة السوداء والتين واللبن والماء. والمُلفت ليس أنها «أغذية خارقة»، بل أنها كلّها كاملة قليلة التصنيع ومنخفضة السكر المضاف. مطبخ السنّة نظام غذائي كامل قبل أن يُخترع المصطلح."),
        "hadith": T(
            "Talbina soothes the heart of the grieving and removes some of the sorrow. (Sahih al-Bukhari 5417)",
            "Talbina menenangkan hati orang yang berduka dan menghilangkan sebagian kesedihan. (Sahih Bukhari 5417)",
            "«التلبينة تُجِمّ فؤاد المريض وتُذهب بعض الحَزَن». (صحيح البخاري ٥٤١٧)"),
        "science": T(
            "Ultra-processed food intake tracks with a 26% higher all-cause mortality risk; replacing 10% of it with whole foods lowers cancer risk about 12% (BMJ, 2019).",
            "Asupan makanan ultra-olahan berkorelasi dengan risiko mortalitas 26% lebih tinggi; mengganti 10% dengan makanan utuh menurunkan risiko kanker sekitar 12% (BMJ, 2019).",
            "الأطعمة فائقة التصنيع ترتبط بارتفاع الوفيات نحو ٢٦٪، واستبدال ١٠٪ منها بأطعمة كاملة يخفّض خطر السرطان نحو ١٢٪."),
    },
    {
        "id": "k_salah_movement",
        "pillar": "physical",
        "category": T("Movement", "Gerak", "حركة"),
        "title": T("Salah Is Already Exercise", "Shalat Sudah Merupakan Olahraga", "الصلاة رياضة بالفعل"),
        "content": T(
            "Five prayers a day is roughly 100 postural transitions: standing, forward flexion, deep knee flexion, spinal extension. If you pray on time, you already have a movement baseline most sedentary adults lack. Ihyaa builds on that baseline instead of replacing it.",
            "Lima shalat sehari berarti sekitar 100 transisi postur: berdiri, membungkuk, menekuk lutut penuh, ekstensi tulang belakang. Jika Anda shalat tepat waktu, Anda sudah memiliki basis gerak yang tidak dimiliki banyak orang yang jarang bergerak. Ihyaa membangun di atas basis itu, bukan menggantinya.",
            "خمس صلوات في اليوم تعني نحو مئة انتقال حركي: قيام، وانثناء، وثني كامل للركبتين، وبسط للعمود الفقري. فإن صلّيت في وقتها فلديك أساس حركي يفقده كثير من القاعدين. و«إحياء» يبني على هذا الأساس لا يستبدله."),
        "science": T(
            "Measured joint kinematics during salah fall within therapeutic ranges for lumbar and knee mobility; regular practitioners show better lumbar flexibility than matched non-praying controls (Journal of Physical Therapy Science, 2017).",
            "Kinematika sendi terukur selama shalat berada dalam rentang terapeutik untuk mobilitas lumbal dan lutut; praktisi rutin menunjukkan fleksibilitas lumbal lebih baik daripada kontrol sepadan (Journal of Physical Therapy Science, 2017).",
            "قياسات حركة المفاصل في الصلاة تقع في المدى العلاجي لمرونة أسفل الظهر والركبة، والمصلّون المنتظمون أفضل مرونة من غيرهم."),
    },
    {
        "id": "k_sleep",
        "pillar": "mental",
        "category": T("Sleep", "Tidur", "نوم"),
        "title": T("Fajr Is a Sleep Strategy", "Subuh Adalah Strategi Tidur", "الفجر استراتيجية نوم"),
        "content": T(
            "Waking for Fajr is not a sacrifice of sleep — it is an anchor for it. A fixed wake time is the single most powerful lever on sleep quality, more than bedtime. Pair Fajr with an earlier Isha wind-down and your whole circadian rhythm reorganises within about ten days.",
            "Bangun Subuh bukan mengorbankan tidur — ia justru penambatnya. Waktu bangun yang tetap adalah tuas terkuat kualitas tidur, lebih dari waktu tidur. Padukan Subuh dengan menenangkan diri lebih awal setelah Isya, dan seluruh ritme sirkadian Anda tertata dalam sekitar sepuluh hari.",
            "الاستيقاظ للفجر ليس تفريطًا في النوم بل تثبيتًا له. فوقت الاستيقاظ الثابت أقوى مؤثّر في جودة النوم، أقوى من وقت النوم. واجمع بين الفجر وهدوء مبكّر بعد العشاء فيعيد إيقاعك الحيوي تنظيم نفسه في نحو عشرة أيام."),
        "science": T(
            "Wake-time regularity predicts sleep efficiency and mood better than total sleep duration; irregular wake times raise cardiometabolic risk independently of sleep length (Sleep, 2018; Scientific Reports, 2018).",
            "Keteraturan waktu bangun memprediksi efisiensi tidur dan mood lebih baik daripada total durasi tidur; waktu bangun tak teratur meningkatkan risiko kardiometabolik terlepas dari lama tidur (Sleep, 2018).",
            "انتظام وقت الاستيقاظ يتنبّأ بكفاءة النوم والمزاج أفضل من مدّة النوم، وعدم انتظامه يرفع الخطر القلبي الأيضي مستقلًّا عن المدّة."),
    },
    {
        "id": "k_halal_only",
        "pillar": "nutrition",
        "category": T("Halal Guarantee", "Jaminan Halal", "ضمان الحلال"),
        "title": T("Why Nothing Here Needs a Fatwa", "Mengapa Tidak Ada yang Perlu Fatwa Di Sini", "لماذا لا يحتاج شيء هنا إلى فتوى"),
        "content": T(
            "Ihyaa deliberately avoids anything contested: no yoga chants, no music-dependent workouts, no supplements of doubtful origin, no fasting protocols that clash with fiqh, no mixed-gender requirements. Every practice here is either explicitly Sunnah or religiously neutral movement and nutrition.",
            "Ihyaa sengaja menghindari hal yang diperdebatkan: tanpa mantra yoga, tanpa latihan yang bergantung musik, tanpa suplemen yang asalnya diragukan, tanpa protokol puasa yang berbenturan dengan fikih, tanpa keharusan campur laki-perempuan. Setiap praktik di sini adalah Sunnah yang jelas atau gerak dan nutrisi yang netral secara agama.",
            "يتجنّب «إحياء» قصدًا كل ما فيه خلاف: لا أذكار يوغا، ولا تمارين تعتمد على الموسيقى، ولا مكمّلات مشكوك في أصلها، ولا أنظمة صيام تصادم الفقه، ولا اختلاط مفروض. فكل ممارسة هنا إما سنّة صريحة أو حركة وغذاء محيّدان شرعًا."),
        "hadith": T(
            "Whoever avoids doubtful matters has protected his religion and his honour. (Sahih al-Bukhari 2051)",
            "Barangsiapa menjauhi hal-hal yang samar, ia telah menyelamatkan agama dan kehormatannya. (Sahih Bukhari 2051)",
            "«فمن اتّقى الشبهات استبرأ لدينه وعرضه». (صحيح البخاري ٢٠٥١)"),
        "science": T(
            "Adherence to health programmes rises when the programme is congruent with a participant's religious identity; cultural-religious tailoring improves 6-month retention substantially (Health Education & Behavior).",
            "Kepatuhan pada program kesehatan meningkat bila program tersebut selaras dengan identitas religius peserta; penyesuaian kultural-religius meningkatkan retensi 6 bulan secara substansial (Health Education & Behavior).",
            "الالتزام بالبرامج الصحّية يرتفع عندما تتوافق مع الهُويّة الدينية للمشارك، والتكييف الثقافي الديني يحسّن الاستمرار بعد ستة أشهر بدرجة كبيرة."),
    },
    {
        "id": "k_streak_mercy",
        "pillar": "spiritual",
        "category": T("Consistency", "Konsistensi", "مداومة"),
        "title": T("Breaking a Streak Is Not Failing", "Streak Putus Bukan Berarti Gagal", "انقطاع السلسلة ليس فشلًا"),
        "content": T(
            "If you miss a day, you have not lost 30 days of work. Research on habit formation shows a single lapse has almost no effect on eventual automaticity — but the guilt spiral does. Make istighfar, open the app, do one two-minute task. That is the whole recovery protocol.",
            "Jika Anda melewatkan satu hari, Anda tidak kehilangan 30 hari kerja. Riset pembentukan kebiasaan menunjukkan satu kelalaian nyaris tak berpengaruh pada otomatisasi akhir — tetapi spiral rasa bersalah berpengaruh. Beristighfar, buka aplikasi, kerjakan satu tugas dua menit. Itulah seluruh protokol pemulihannya.",
            "إن فوّتت يومًا فلم تخسر ثلاثين يومًا من العمل. تُظهر بحوث بناء العادة أن الزلّة الواحدة لا تكاد تؤثّر في التلقائية النهائية، لكن دوّامة الشعور بالذنب تؤثّر. استغفر، وافتح التطبيق، وأدِّ مهمّة واحدة من دقيقتين؛ هذا هو بروتوكول العودة كلّه."),
        "quran": T(
            "\"Allah does not burden a soul beyond what it can bear.\" (Al-Baqarah 2:286)",
            "\"Allah tidak membebani seseorang melainkan sesuai kesanggupannya.\" (QS Al-Baqarah 2:286)",
            "﴿لَا يُكَلِّفُ اللَّهُ نَفْسًا إِلَّا وُسْعَهَا﴾ (البقرة: ٢٨٦)"),
        "science": T(
            "Missing a single opportunity to perform a habit did not measurably affect the formation curve in Lally's 84-day tracking study; self-compassion after a lapse predicts faster return to behaviour.",
            "Melewatkan satu kesempatan menjalankan kebiasaan tidak berpengaruh terukur pada kurva pembentukan dalam studi 84 hari Lally; welas diri setelah kelalaian memprediksi kembalinya perilaku lebih cepat.",
            "تفويت فرصة واحدة لأداء العادة لم يؤثّر بشكل ملموس في منحنى التكوين في دراسة لالي (٨٤ يومًا)، والرحمة بالنفس بعد الزلّة تُسرّع العودة."),
    },
    {
        "id": "k_water_adab",
        "pillar": "physical",
        "category": T("Adab", "Adab", "أدب"),
        "title": T("The Adab of Drinking", "Adab Minum", "أدب الشرب"),
        "content": T(
            "Sit. Say Bismillah. Three breaths, not one. Do not breathe into the vessel. Say Alhamdulillah. Four small rules that slow you down enough for your body to register the water — and for your heart to register the giver.",
            "Duduk. Ucapkan Bismillah. Tiga tarikan napas, bukan satu. Jangan bernapas ke dalam wadah. Ucapkan Alhamdulillah. Empat aturan kecil yang memperlambat Anda cukup lama agar tubuh menyadari airnya — dan hati menyadari Pemberinya.",
            "اجلس. قل بسم الله. ثلاث دفعات لا واحدة. ولا تتنفّس في الإناء. وقل الحمد لله. أربع قواعد صغيرة تُبطئك بما يكفي ليسجّل جسدك الماء، ويسجّل قلبك المُنعم."),
        "hadith": T(
            "The Prophet ﷺ forbade breathing into the vessel while drinking. (Sahih al-Bukhari 5630)",
            "Nabi ﷺ melarang bernapas ke dalam wadah saat minum. (Sahih Bukhari 5630)",
            "نهى النبي ﷺ عن التنفّس في الإناء. (صحيح البخاري ٥٦٣٠)"),
        "science": T(
            "Even 2% dehydration reduces cognitive performance ~20% and endurance ~25%; drinking in paced sips improves fluid retention over rapid bolus intake (British Journal of Nutrition).",
            "Dehidrasi 2% saja menurunkan performa kognitif ~20% dan daya tahan ~25%; minum bertahap meningkatkan retensi cairan dibanding menenggak cepat (British Journal of Nutrition).",
            "نقص الماء بنسبة ٢٪ فقط يخفّض الأداء الذهني نحو ٢٠٪ والتحمّل نحو ٢٥٪، والشرب على دفعات يحسّن احتباس السوائل أكثر من الشرب السريع."),
    },
]

STORE_ITEMS = [
    {
        "id": "pro_1_month",
        "points_cost": 2500,
        "grants_pro_days": 30,
        "name": T("Ihyaa Pro — 1 Month", "Ihyaa Pro — 1 Bulan", "إحياء برو — شهر"),
        "description": T(
            "Unlocks the 100-Day and 1-Year tracks, unlimited AI Coach conversations, calendar export and the full knowledge library for 30 days.",
            "Membuka jalur 100 Hari dan 1 Tahun, percakapan AI Coach tanpa batas, ekspor kalender, dan perpustakaan ilmu lengkap selama 30 hari.",
            "يفتح مسارَي ١٠٠ يوم وسنة كاملة، ومحادثات غير محدودة مع المدرّب الذكي، وتصدير التقويم، ومكتبة المعرفة كاملة لمدّة ٣٠ يومًا."),
    },
    {
        "id": "pro_3_months",
        "points_cost": 6000,
        "grants_pro_days": 90,
        "name": T("Ihyaa Pro — 3 Months", "Ihyaa Pro — 3 Bulan", "إحياء برو — ٣ أشهر"),
        "description": T(
            "Three months of Pro. The sweet spot: long enough to finish a 100-Day track from start to finish.",
            "Tiga bulan Pro. Titik ideal: cukup panjang untuk menyelesaikan satu jalur 100 Hari dari awal hingga akhir.",
            "ثلاثة أشهر من برو. المدّة المثالية لإكمال مسار ١٠٠ يوم من أوّله إلى آخره."),
    },
    {
        "id": "pro_1_year",
        "points_cost": 18000,
        "grants_pro_days": 365,
        "name": T("Ihyaa Pro — 1 Year", "Ihyaa Pro — 1 Tahun", "إحياء برو — سنة"),
        "description": T(
            "A full year of Pro, including the 1-Year Revival track. Earned entirely with points — no payment.",
            "Satu tahun penuh Pro, termasuk jalur Kebangkitan 1 Tahun. Diperoleh sepenuhnya dengan poin — tanpa pembayaran.",
            "سنة كاملة من برو، بما فيها مسار «الإحياء» لسنة. تُنال بالنقاط وحدها بلا دفع."),
    },
]


def localize_card(card: dict, lang: str) -> dict:
    lang = lang if lang in ("en", "id", "ar") else "en"

    def pick(f):
        v = card.get(f)
        return (v.get(lang) or v.get("en")) if v else None

    return {
        "id": card["id"],
        "pillar": card["pillar"],
        "category": pick("category"),
        "title": pick("title"),
        "content": pick("content"),
        "quran_verse": pick("quran"),
        "hadith_text": pick("hadith"),
        "scientific_fact": pick("science"),
    }


def localize_item(item: dict, lang: str) -> dict:
    lang = lang if lang in ("en", "id", "ar") else "en"

    def pick(f):
        v = item.get(f)
        return (v.get(lang) or v.get("en")) if v else None

    return {
        "id": item["id"],
        "points_cost": item["points_cost"],
        "grants_pro_days": item["grants_pro_days"],
        "name": pick("name"),
        "description": pick("description"),
    }
