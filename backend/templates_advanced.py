"""Deeper practices unlocked by the 100-Day and 1-Year tracks.

`min_phase` gates a template: it only appears once the challenge reaches that
phase, so a long track keeps opening new ground instead of looping the basics.
"""


def T(en: str, idn: str, ar: str) -> dict:
    return {"en": en, "id": idn, "ar": ar}


ADVANCED_TEMPLATES: list[dict] = [
    # ---------------------------------------------------------------- SPIRITUAL
    {
        "key": "s_witr", "pillar": "spiritual", "anchor": "night",
        "minutes": 8, "level": 2, "min_phase": 2,
        "title": T("Witr Before Sleep", "Witir Sebelum Tidur", "الوتر قبل النوم"),
        "desc": T(
            "Seal your day with one rakat of Witr — or three if you can. Never sleep without it once it becomes your habit.",
            "Tutup hari Anda dengan satu rakaat Witir — atau tiga jika mampu. Jangan tidur tanpanya setelah menjadi kebiasaan.",
            "اختم يومك بركعة وتر، أو ثلاث إن قدرت. ولا تنم بغير وتر بعد أن تصير عادتك."),
        "hadith": T(
            "Make the last of your prayer at night the Witr. (Sahih al-Bukhari 998)",
            "Jadikanlah akhir shalat malam kalian adalah Witir. (Sahih Bukhari 998)",
            "«اجعلوا آخر صلاتكم بالليل وترًا». (صحيح البخاري ٩٩٨)"),
        "science": T(
            "A short, low-arousal ritual immediately before bed shortens sleep latency and is the mechanism behind stimulus-control therapy for insomnia (Sleep Medicine Reviews).",
            "Ritual singkat berintensitas rendah tepat sebelum tidur mempercepat tertidur dan menjadi mekanisme terapi stimulus-control untuk insomnia (Sleep Medicine Reviews).",
            "روتين قصير هادئ قبل النوم مباشرة يسرّع الغفو، وهو أساس العلاج بضبط المحفّزات للأرق."),
    },
    {
        "key": "s_duha", "pillar": "spiritual", "anchor": "morning",
        "minutes": 10, "level": 2, "min_phase": 2,
        "title": T("Salat ad-Duha", "Shalat Dhuha", "صلاة الضحى"),
        "desc": T(
            "Two to four rakat once the sun has fully risen. It is the charity of every joint in your body.",
            "Dua hingga empat rakaat setelah matahari terbit sempurna. Ia adalah sedekah bagi setiap persendian tubuh Anda.",
            "من ركعتين إلى أربع بعد ارتفاع الشمس. وهي صدقة عن كل مفصل في جسدك."),
        "hadith": T(
            "Every joint of you owes a charity each day... two rakat of Duha suffice for all of that. (Sahih Muslim 720)",
            "Setiap persendianmu wajib bersedekah setiap hari... dua rakaat Dhuha mencukupi semua itu. (Sahih Muslim 720)",
            "«يُصبح على كل سُلامى من أحدكم صدقة... ويُجزئ من ذلك ركعتان يركعهما من الضحى». (صحيح مسلم ٧٢٠)"),
        "science": T(
            "Mid-morning light plus light movement raises alertness and mood more than caffeine alone and stabilises the afternoon dip (Sleep Health; Physiology & Behavior).",
            "Cahaya pagi menjelang siang ditambah gerak ringan meningkatkan kewaspadaan dan mood lebih baik daripada kafein saja, serta menstabilkan lesu sore (Sleep Health).",
            "ضوء الضحى مع حركة خفيفة يرفع اليقظة والمزاج أكثر من الكافيين وحده، ويقلّل هبوط ما بعد الظهر."),
    },
    {
        "key": "s_memorise", "pillar": "spiritual", "anchor": "fajr",
        "minutes": 15, "level": 2, "min_phase": 2,
        "title": T("Memorise Three Ayat", "Hafal Tiga Ayat", "احفظ ثلاث آيات"),
        "desc": T(
            "Three ayat only. Read, repeat ten times, recite from memory, then revise yesterday's three.",
            "Tiga ayat saja. Baca, ulangi sepuluh kali, hafalkan tanpa melihat, lalu murajaah tiga ayat kemarin.",
            "ثلاث آيات فقط: اقرأ، وكرّر عشر مرات، ثم اسمعها من حفظك، وراجع آيات الأمس."),
        "hadith": T(
            "The best of you are those who learn the Quran and teach it. (Sahih al-Bukhari 5027)",
            "Sebaik-baik kalian adalah yang mempelajari Al-Quran dan mengajarkannya. (Sahih Bukhari 5027)",
            "«خيركم من تعلّم القرآن وعلّمه». (صحيح البخاري ٥٠٢٧)"),
        "science": T(
            "Spaced retrieval — recite, revise the day before, then the week before — is the single most efficient memory protocol known (Roediger & Karpicke, Psychological Science).",
            "Retrieval terjadwal — hafal, murajaah hari sebelumnya, lalu pekan sebelumnya — adalah protokol memori paling efisien yang diketahui (Psychological Science).",
            "الاسترجاع المتباعد (حفظ، مراجعة الأمس، ثم الأسبوع الماضي) أكفأ بروتوكول معروف للذاكرة."),
    },
    {
        "key": "s_dua_list", "pillar": "spiritual", "anchor": "isha",
        "minutes": 8, "level": 1, "min_phase": 2,
        "title": T("Your Written Du'a List", "Daftar Doa Tertulis", "قائمة دعائك المكتوبة"),
        "desc": T(
            "Keep a written list of what you ask Allah for. Read it after Isha, add one line, and mark what has been answered.",
            "Simpan daftar tertulis hal yang Anda minta kepada Allah. Baca setelah Isya, tambah satu baris, dan tandai yang telah dikabulkan.",
            "احفظ قائمة مكتوبة بما تسأل الله. اقرأها بعد العشاء، وأضف سطرًا، وضع علامة على ما استُجيب."),
        "quran": T(
            "\"Call upon Me and I will respond to you.\" (Ghafir 40:60)",
            "\"Berdoalah kepada-Ku, niscaya Aku kabulkan bagimu.\" (QS Ghafir 40:60)",
            "﴿ادْعُونِي أَسْتَجِبْ لَكُمْ﴾ (غافر: ٦٠)"),
        "science": T(
            "Writing goals and reviewing them raises attainment about 40% versus unwritten goals, and noting what was granted trains the brain's positive-evidence bias (Gollwitzer; Emmons gratitude research).",
            "Menulis tujuan dan meninjaunya meningkatkan pencapaian sekitar 40% dibanding tujuan tak tertulis, dan mencatat yang terkabul melatih bias bukti positif otak (riset Gollwitzer & Emmons).",
            "كتابة الأهداف ومراجعتها ترفع تحقيقها نحو ٤٠٪، وتسجيل ما تحقّق يدرّب الدماغ على ملاحظة النِّعم."),
    },
    {
        "key": "s_kahf_friday", "pillar": "spiritual", "anchor": "morning",
        "minutes": 20, "level": 2, "min_phase": 3,
        "title": T("Surah al-Kahf on Friday", "Surah Al-Kahf di Hari Jumat", "سورة الكهف يوم الجمعة"),
        "desc": T(
            "If today is Friday, read Surah al-Kahf. If not, read twenty minutes of Quran with tafsir instead.",
            "Jika hari ini Jumat, bacalah Surah Al-Kahf. Jika bukan, bacalah Al-Quran dua puluh menit beserta tafsir.",
            "إن كان اليوم جمعة فاقرأ سورة الكهف، وإلا فاقرأ عشرين دقيقة من القرآن مع التفسير."),
        "hadith": T(
            "Whoever reads Surah al-Kahf on Friday, a light shines for him until the next Friday. (al-Bayhaqi, authenticated by al-Albani)",
            "Barangsiapa membaca Surah Al-Kahf pada hari Jumat, cahaya menyinarinya sampai Jumat berikutnya. (al-Baihaqi, disahihkan al-Albani)",
            "«مَن قرأ سورة الكهف يوم الجمعة أضاء له من النور ما بين الجمعتين». (البيهقي، وصحّحه الألباني)"),
        "science": T(
            "Weekly anchored rituals ('temporal landmarks') restart motivation and improve long-term adherence to behaviour change (Dai, Milkman & Riis, Management Science).",
            "Ritual berjangkar mingguan ('penanda waktu') memulai ulang motivasi dan meningkatkan kepatuhan jangka panjang pada perubahan perilaku (Management Science).",
            "الطقوس الأسبوعية الثابتة («العلامات الزمنية») تُعيد إشعال الدافع وتحسّن الاستمرار طويل المدى."),
    },
    {
        "key": "s_hadith_study", "pillar": "spiritual", "anchor": "isha",
        "minutes": 12, "level": 2, "min_phase": 3,
        "title": T("Study One Hadith Properly", "Kaji Satu Hadits dengan Benar", "دراسة حديث واحد بعمق"),
        "desc": T(
            "Take one hadith from Riyad as-Salihin. Read it, read a scholar's explanation, then write one sentence on what you will change.",
            "Ambil satu hadits dari Riyadhus Shalihin. Baca, baca syarahnya dari ulama, lalu tulis satu kalimat tentang apa yang akan Anda ubah.",
            "خذ حديثًا من رياض الصالحين: اقرأه، ثم اقرأ شرح عالم له، واكتب سطرًا واحدًا عمّا ستغيّره."),
        "hadith": T(
            "Whoever treads a path seeking knowledge, Allah makes easy for him a path to Paradise. (Sahih Muslim 2699)",
            "Barangsiapa menempuh jalan mencari ilmu, Allah mudahkan baginya jalan ke surga. (Sahih Muslim 2699)",
            "«مَن سلك طريقًا يبتغي به علمًا سهّل الله له طريقًا إلى الجنة». (صحيح مسلم ٢٦٩٩)"),
        "science": T(
            "Elaborative encoding — explaining an idea in your own words and tying it to an action — roughly doubles long-term retention over rereading (Applied Cognitive Psychology).",
            "Pengodean elaboratif — menjelaskan gagasan dengan kata sendiri dan mengaitkannya ke tindakan — hampir menggandakan retensi jangka panjang dibanding membaca ulang (Applied Cognitive Psychology).",
            "الترميز التفصيلي (شرح الفكرة بكلماتك وربطها بعمل) يضاعف تقريبًا الاحتفاظ طويل المدى مقارنة بإعادة القراءة."),
    },
    {
        "key": "s_itikaf", "pillar": "spiritual", "anchor": "maghrib",
        "minutes": 30, "level": 3, "min_phase": 4,
        "title": T("Half an Hour of I'tikaf", "Setengah Jam I'tikaf", "نصف ساعة اعتكاف"),
        "desc": T(
            "Stay in the masjid after one prayer with the intention of i'tikaf. No phone. Quran, dhikr, du'a — then leave.",
            "Tetap di masjid setelah satu shalat dengan niat i'tikaf. Tanpa ponsel. Al-Quran, dzikir, doa — lalu pulang.",
            "امكث في المسجد بعد صلاة واحدة بنيّة الاعتكاف. بلا هاتف: قرآن وذكر ودعاء، ثم انصرف."),
        "hadith": T(
            "The Prophet ﷺ would remain in his place of prayer after Fajr until the sun rose. (Sahih Muslim 670)",
            "Nabi ﷺ tetap di tempat shalatnya setelah Subuh sampai matahari terbit. (Sahih Muslim 670)",
            "كان النبي ﷺ يبقى في مصلّاه بعد الفجر حتى تطلع الشمس. (صحيح مسلم ٦٧٠)"),
        "science": T(
            "Solitude without stimulation restores directed attention and cuts perceived stress; even 30 minutes measurably lowers cortisol (Frontiers in Psychology; Journal of Environmental Psychology).",
            "Kesendirian tanpa stimulasi memulihkan atensi terarah dan menurunkan stres yang dirasakan; 30 menit saja sudah menurunkan kortisol secara terukur (Frontiers in Psychology).",
            "الخلوة بلا مثيرات تُجدّد الانتباه الموجّه وتخفّض التوتر، وثلاثون دقيقة تكفي لخفض الكورتيزول بشكل ملموس."),
    },

    # ---------------------------------------------------------------- PHYSICAL
    {
        "key": "p_pushup_ladder", "pillar": "physical", "anchor": "asr",
        "minutes": 12, "level": 2, "min_phase": 2,
        "title": T("Push-Up Ladder", "Tangga Push-Up", "سُلّم تمرين الضغط"),
        "desc": T(
            "Do 1 push-up, rest 10s, then 2, then 3... climb until you must stop, then walk it back down.",
            "Lakukan 1 push-up, istirahat 10 detik, lalu 2, lalu 3... naik sampai harus berhenti, lalu turun kembali.",
            "ضغطة واحدة، راحة ١٠ ثوانٍ، ثم اثنتان، ثم ثلاث... اصعد حتى تتوقّف، ثم انزل مثلها."),
        "science": T(
            "Men able to do 40+ push-ups had a 96% lower incidence of cardiovascular events over ten years than those managing under 10 (JAMA Network Open, 2019).",
            "Pria yang mampu 40+ push-up memiliki insiden kejadian kardiovaskular 96% lebih rendah dalam sepuluh tahun dibanding yang di bawah 10 (JAMA Network Open, 2019).",
            "من قدر على ٤٠ ضغطة أو أكثر انخفضت لديه أحداث القلب بنسبة ٩٦٪ خلال عشر سنوات مقارنة بمن أقل من ١٠."),
    },
    {
        "key": "p_squat_strength", "pillar": "physical", "anchor": "asr",
        "minutes": 16, "level": 3, "min_phase": 3,
        "title": T("Strength: Tempo Squats", "Kekuatan: Squat Tempo", "قوّة: قرفصاء بإيقاع"),
        "desc": T(
            "Four sets of 8 squats, lowering for a slow 3 seconds each rep. Add a backpack with books for load.",
            "Empat set 8 squat, turun perlahan 3 detik setiap repetisi. Tambahkan tas berisi buku sebagai beban.",
            "أربع مجموعات من ٨ قرفصاء، بنزول بطيء ٣ ثوانٍ لكل عدة. أضف حقيبة كتب للحمل."),
        "science": T(
            "Leg strength predicts independence in later life and lower-body resistance work is the most effective single intervention against sarcopenia (Journal of Cachexia, Sarcopenia and Muscle).",
            "Kekuatan kaki memprediksi kemandirian di usia lanjut, dan latihan beban tubuh bawah adalah intervensi tunggal paling efektif melawan sarkopenia (Journal of Cachexia, Sarcopenia and Muscle).",
            "قوّة الساقين تتنبّأ بالاستقلال في الكبر، وتدريب مقاومة الجزء السفلي أنجع تدخّل ضد ضمور العضلات."),
    },
    {
        "key": "p_sunnah_sport", "pillar": "physical", "anchor": "asr",
        "minutes": 25, "level": 2, "min_phase": 2,
        "title": T("A Sunnah Sport", "Olahraga Sunnah", "رياضة من السنّة"),
        "desc": T(
            "Swim, ride, run or practise archery today — the three the Prophet ﷺ named, plus running which he raced in.",
            "Berenang, menunggang, berlari, atau memanah hari ini — tiga yang disebut Nabi ﷺ, ditambah berlari yang beliau lombakan.",
            "اسبح أو اركب أو ارمِ أو اعدُ اليوم؛ فهذه التي ذكرها النبي ﷺ، والعدو الذي سابق فيه."),
        "hadith": T(
            "Teach your children swimming, archery and horsemanship. (Reported from 'Umar ibn al-Khattab)",
            "Ajarkan anak-anakmu berenang, memanah, dan menunggang kuda. (Diriwayatkan dari Umar bin Khattab)",
            "«علّموا أولادكم السباحة والرماية ورُكوب الخيل». (أثرٌ عن عمر رضي الله عنه)"),
        "science": T(
            "Swimmers show ~28% lower all-cause mortality than sedentary adults, and skill-based sport improves adherence because it is intrinsically rewarding (International Journal of Aquatic Research).",
            "Perenang menunjukkan mortalitas semua sebab ~28% lebih rendah daripada orang yang jarang bergerak, dan olahraga berbasis keterampilan meningkatkan kepatuhan karena menyenangkan secara intrinsik.",
            "السبّاحون تقلّ وفياتهم نحو ٢٨٪ مقارنة بالقاعدين، والرياضات المهارية ترفع الالتزام لأنها ممتعة بذاتها."),
    },
    {
        "key": "p_steps_target", "pillar": "physical", "anchor": "anytime",
        "minutes": 30, "level": 2, "min_phase": 2,
        "title": T("Hit 8,000 Steps", "Capai 8.000 Langkah", "بلوغ ٨٠٠٠ خطوة"),
        "desc": T(
            "Aim for 8,000 steps today. Walk to the masjid, park further away, take one call standing and walking.",
            "Targetkan 8.000 langkah hari ini. Jalan ke masjid, parkir lebih jauh, terima satu panggilan sambil berdiri dan berjalan.",
            "استهدف ٨٠٠٠ خطوة اليوم: امشِ إلى المسجد، واركن أبعد، وتلقَّ مكالمة وأنت تمشي."),
        "science": T(
            "Mortality benefit rises steeply up to ~8,000 steps/day and plateaus near 10,000; even 4,400 beats 2,700 significantly (JAMA Internal Medicine, 2019).",
            "Manfaat mortalitas meningkat tajam hingga ~8.000 langkah/hari dan mendatar di sekitar 10.000; bahkan 4.400 jauh lebih baik daripada 2.700 (JAMA Internal Medicine, 2019).",
            "تنخفض الوفيات بحدّة حتى نحو ٨٠٠٠ خطوة يوميًا وتستقر قرب ١٠٠٠٠، وحتى ٤٤٠٠ أفضل بكثير من ٢٧٠٠."),
    },
    {
        "key": "p_mobility_flow", "pillar": "physical", "anchor": "morning",
        "minutes": 11, "level": 2, "min_phase": 3,
        "title": T("Full-Body Mobility Flow", "Alur Mobilitas Seluruh Tubuh", "تدفّق مرونة لكامل الجسم"),
        "desc": T(
            "Ten continuous minutes: cat-cow, hip openers, thoracic rotations, deep squat hold, hamstring sweeps. Breathe throughout.",
            "Sepuluh menit tanpa henti: cat-cow, pembuka pinggul, rotasi toraks, tahan squat dalam, sapuan hamstring. Bernapas sepanjang gerakan.",
            "عشر دقائق متّصلة: القط والبقرة، فتح الورك، دوران الصدر، ثبات القرفصاء العميق، مدّ أوتار الركبة، مع تنفّس مستمر."),
        "science": T(
            "Deep-squat mobility predicts fall-free ageing; continuous mobility flows raise range of motion faster than isolated static stretches (Journal of Bodywork and Movement Therapies).",
            "Mobilitas squat dalam memprediksi penuaan tanpa jatuh; alur mobilitas kontinu meningkatkan rentang gerak lebih cepat daripada peregangan statis terpisah (Journal of Bodywork and Movement Therapies).",
            "مرونة القرفصاء العميق مؤشّر على شيخوخة بلا سقوط، والتدفّق الحركي المتّصل يرفع مدى الحركة أسرع من التمدّد المعزول."),
    },
    {
        "key": "p_posture", "pillar": "physical", "anchor": "anytime",
        "minutes": 6, "level": 1, "min_phase": 2,
        "title": T("Posture Reset", "Reset Postur", "تصحيح الجلسة"),
        "desc": T(
            "Raise your screen to eye level, plant both feet, roll shoulders back. Then 10 chin tucks and 10 wall angels.",
            "Naikkan layar sejajar mata, pijakkan kedua kaki, tarik bahu ke belakang. Lalu 10 chin tuck dan 10 wall angel.",
            "ارفع الشاشة إلى مستوى العين، وثبّت القدمين، وأرجع الكتفين. ثم ١٠ سحب ذقن و١٠ «ملائكة الحائط»."),
        "science": T(
            "Every 2.5cm of forward head posture adds roughly 4.5kg of load to the cervical spine; ergonomic correction cuts neck-pain days by about a third (Surgical Technology International; Applied Ergonomics).",
            "Setiap 2,5 cm posisi kepala ke depan menambah sekitar 4,5 kg beban pada tulang leher; koreksi ergonomis menurunkan hari nyeri leher sekitar sepertiga (Applied Ergonomics).",
            "كل ٢٫٥ سم من ميل الرأس للأمام يضيف نحو ٤٫٥ كغ حملًا على فقرات العنق، والتصحيح المكتبي يقلّل أيام الألم نحو الثلث."),
    },
    {
        "key": "p_long_walk", "pillar": "physical", "anchor": "asr",
        "minutes": 45, "level": 3, "min_phase": 4,
        "title": T("The Long Walk", "Jalan Jauh", "المشي الطويل"),
        "desc": T(
            "One long unhurried walk today, 45 minutes or more, outdoors, ideally with someone you love.",
            "Satu kali jalan panjang hari ini, 45 menit atau lebih, di luar ruangan, sebaiknya bersama orang yang Anda cintai.",
            "مشية طويلة واحدة اليوم، ٤٥ دقيقة أو أكثر، في الخارج، ويُستحسن بمعيّة من تحب."),
        "science": T(
            "Long steady-state walking raises fat oxidation and BDNF while lowering rumination; social walking adds a measurable mood effect beyond solitary walking (Neuroscience Letters; Emotion).",
            "Jalan panjang berkecepatan stabil meningkatkan oksidasi lemak dan BDNF sekaligus menurunkan ruminasi; berjalan bersama menambah efek mood terukur di atas berjalan sendiri (Emotion).",
            "المشي الطويل الثابت يزيد أكسدة الدهون وعامل النمو العصبي ويقلّل التفكير القهري، والمشي مع صاحب يزيد الأثر النفسي."),
    },

    # ---------------------------------------------------------------- NUTRITION
    {
        "key": "n_talbina", "pillar": "nutrition", "anchor": "morning",
        "minutes": 12, "level": 2, "min_phase": 2,
        "title": T("Talbina (Barley Porridge)", "Talbina (Bubur Jelai)", "التلبينة"),
        "desc": T(
            "Simmer two tablespoons of barley flour in milk or water, sweeten with honey. The Prophet's ﷺ comfort food.",
            "Masak dua sendok makan tepung jelai dalam susu atau air, manisi dengan madu. Makanan penenang dari Nabi ﷺ.",
            "اطبخ ملعقتين من دقيق الشعير في لبن أو ماء، وحلِّها بالعسل. طعام النبي ﷺ المُسكِّن للنفس."),
        "hadith": T(
            "Talbina soothes the heart of the grieving and removes some of the sorrow. (Sahih al-Bukhari 5417)",
            "Talbina menenangkan hati orang berduka dan menghilangkan sebagian kesedihan. (Sahih Bukhari 5417)",
            "«التلبينة تُجِمّ فؤاد المريض وتُذهب بعض الحَزَن». (صحيح البخاري ٥٤١٧)"),
        "science": T(
            "Barley beta-glucan lowers LDL cholesterol about 7% and blunts post-meal glucose; it also feeds gut bacteria that produce mood-linked short-chain fatty acids (EFSA health claim; Nutrition Reviews).",
            "Beta-glukan jelai menurunkan kolesterol LDL sekitar 7% dan menumpulkan glukosa pascamakan; ia juga memberi makan bakteri usus penghasil asam lemak rantai pendek yang terkait mood (Nutrition Reviews).",
            "بيتا جلوكان الشعير يخفّض الكوليسترول الضار نحو ٧٪ ويهدّئ سكر ما بعد الأكل، ويغذّي بكتيريا الأمعاء المرتبطة بالمزاج."),
    },
    {
        "key": "n_protein", "pillar": "nutrition", "anchor": "dhuhr",
        "minutes": 8, "level": 2, "min_phase": 2,
        "title": T("Hit Your Protein", "Cukupi Protein Anda", "أكمل بروتينك"),
        "desc": T(
            "Put a palm-sized portion of halal protein in every main meal today — eggs, fish, chicken, lentils, yoghurt.",
            "Sertakan protein halal seukuran telapak tangan di setiap makan utama hari ini — telur, ikan, ayam, lentil, yoghurt.",
            "ضع في كل وجبة رئيسية اليوم حصّة بروتين حلال بحجم كفّك: بيض، سمك، دجاج، عدس، لبن."),
        "science": T(
            "1.2–1.6g of protein per kg of bodyweight preserves lean mass during weight loss and increases satiety more than carbohydrate or fat (American Journal of Clinical Nutrition).",
            "1,2–1,6 g protein per kg berat badan mempertahankan massa otot saat menurunkan berat dan memberi rasa kenyang lebih besar daripada karbohidrat atau lemak (American Journal of Clinical Nutrition).",
            "١٫٢–١٫٦ غرام بروتين لكل كيلوغرام من الوزن يحفظ الكتلة العضلية عند إنقاص الوزن ويزيد الشبع أكثر من الكربوهيدرات والدهون."),
    },
    {
        "key": "n_eating_window", "pillar": "nutrition", "anchor": "anytime",
        "minutes": 10, "level": 3, "min_phase": 3,
        "title": T("A Ten-Hour Eating Window", "Jendela Makan Sepuluh Jam", "نافذة أكل عشر ساعات"),
        "desc": T(
            "Eat everything today inside ten hours — for example after Fajr until Maghrib. Water only outside it.",
            "Makan semua hari ini dalam sepuluh jam — misalnya setelah Subuh hingga Maghrib. Di luar itu hanya air.",
            "اجعل كل أكلك اليوم داخل عشر ساعات، مثلًا من بعد الفجر إلى المغرب، وما عداها ماء فقط."),
        "science": T(
            "A 10-hour eating window improved blood pressure, waist circumference and HbA1c in metabolic-syndrome patients without calorie counting (Cell Metabolism, 2020).",
            "Jendela makan 10 jam memperbaiki tekanan darah, lingkar perut, dan HbA1c pada pasien sindrom metabolik tanpa menghitung kalori (Cell Metabolism, 2020).",
            "نافذة أكل من عشر ساعات حسّنت ضغط الدم ومحيط الخصر والسكر التراكمي لدى مرضى متلازمة التمثيل الغذائي دون حساب سعرات."),
    },
    {
        "key": "n_cook_home", "pillar": "nutrition", "anchor": "maghrib",
        "minutes": 30, "level": 2, "min_phase": 2,
        "title": T("Cook One Meal From Scratch", "Masak Satu Hidangan dari Awal", "اطبخ وجبة من الصفر"),
        "desc": T(
            "Cook one meal yourself today from whole ingredients. You control the salt, the oil and the sugar.",
            "Masak sendiri satu hidangan hari ini dari bahan utuh. Anda yang mengendalikan garam, minyak, dan gula.",
            "اطبخ اليوم وجبة واحدة بيدك من مكوّنات كاملة، فأنت من يتحكّم في الملح والزيت والسكر."),
        "science": T(
            "People who cook at home six or more times a week eat significantly fewer calories, less sugar and less fat than those who rarely cook (Public Health Nutrition, 2017).",
            "Orang yang memasak di rumah enam kali atau lebih per pekan mengonsumsi kalori, gula, dan lemak jauh lebih sedikit daripada yang jarang memasak (Public Health Nutrition, 2017).",
            "من يطبخ في بيته ست مرات أسبوعيًا أو أكثر يستهلك سعرات وسكرًا ودهونًا أقل بكثير من غيره."),
    },
    {
        "key": "n_no_processed", "pillar": "nutrition", "anchor": "anytime",
        "minutes": 8, "level": 2, "min_phase": 3,
        "title": T("No Ultra-Processed Food Today", "Hari Tanpa Makanan Ultra-Olahan", "يوم بلا أطعمة فائقة التصنيع"),
        "desc": T(
            "If the ingredient list has more than five items or a word you cannot pronounce, skip it today.",
            "Jika daftar bahan lebih dari lima item atau ada kata yang tak bisa Anda lafalkan, lewati hari ini.",
            "إن كانت المكوّنات أكثر من خمسة أو فيها كلمة لا تستطيع نطقها، فاتركها اليوم."),
        "science": T(
            "In a controlled inpatient trial, an ultra-processed diet led people to eat 500 more calories a day and gain weight versus a matched unprocessed diet (Cell Metabolism, 2019).",
            "Dalam uji terkontrol rawat inap, pola makan ultra-olahan membuat orang makan 500 kalori lebih banyak per hari dan bertambah berat dibanding pola tak olahan yang setara (Cell Metabolism, 2019).",
            "في تجربة داخلية محكومة، دفع النظام فائق التصنيع الناس لتناول ٥٠٠ سعرة إضافية يوميًا وزيادة الوزن مقارنة بنظام غير مصنّع."),
    },
    {
        "key": "n_labels", "pillar": "nutrition", "anchor": "anytime",
        "minutes": 7, "level": 1, "min_phase": 2,
        "title": T("Read Three Labels", "Baca Tiga Label", "اقرأ ثلاثة ملصقات"),
        "desc": T(
            "Before buying, read three labels: check halal status, added sugar per serving, and the first three ingredients.",
            "Sebelum membeli, baca tiga label: cek status halal, gula tambahan per sajian, dan tiga bahan pertama.",
            "قبل الشراء اقرأ ثلاثة ملصقات: تحقّق من الحلال، والسكر المضاف للحصّة، وأول ثلاثة مكوّنات."),
        "quran": T(
            "\"Eat of the good and lawful things We have provided you.\" (Al-Baqarah 2:168)",
            "\"Makanlah dari rezeki yang halal dan baik yang Kami berikan kepadamu.\" (QS Al-Baqarah 2:168)",
            "﴿كُلُوا مِمَّا فِي الْأَرْضِ حَلَالًا طَيِّبًا﴾ (البقرة: ١٦٨)"),
        "science": T(
            "Label-reading is one of the strongest single predictors of lower BMI and better diet quality in population studies (Agricultural Economics; Journal of Consumer Affairs).",
            "Membaca label adalah salah satu prediktor tunggal terkuat untuk IMT lebih rendah dan kualitas diet lebih baik dalam studi populasi (Journal of Consumer Affairs).",
            "قراءة الملصقات من أقوى المؤشّرات المفردة على انخفاض كتلة الجسم وتحسّن جودة الغذاء في الدراسات السكانية."),
    },
    {
        "key": "n_ayyam_bid", "pillar": "nutrition", "anchor": "fajr",
        "minutes": 8, "level": 3, "min_phase": 4,
        "title": T("Fast the White Days", "Puasa Ayyamul Bidh", "صيام الأيام البيض"),
        "desc": T(
            "If today is the 13th, 14th or 15th of the Hijri month, fast. Suhoor with dates and water; break it the same way.",
            "Jika hari ini tanggal 13, 14, atau 15 Hijriah, berpuasalah. Sahur dengan kurma dan air; berbuka dengan cara yang sama.",
            "إن كان اليوم الثالث عشر أو الرابع عشر أو الخامس عشر من الشهر الهجري فصم. تسحّر بتمر وماء، وأفطر بمثله."),
        "hadith": T(
            "The Prophet ﷺ commanded fasting the white days: the 13th, 14th and 15th. (Sunan an-Nasa'i 2422)",
            "Nabi ﷺ memerintahkan puasa hari-hari putih: tanggal 13, 14, dan 15. (Sunan an-Nasa'i 2422)",
            "أمر النبي ﷺ بصيام الأيام البيض: الثالث عشر والرابع عشر والخامس عشر. (سنن النسائي ٢٤٢٢)"),
        "science": T(
            "Three consecutive fasting days monthly is enough to trigger measurable ketogenesis and autophagy markers while remaining sustainable long term (New England Journal of Medicine, 2019).",
            "Tiga hari puasa berurutan setiap bulan cukup memicu ketogenesis dan penanda autofagi yang terukur, dan tetap lestari jangka panjang (NEJM, 2019).",
            "ثلاثة أيام صيام متتالية شهريًا تكفي لتحفيز الكيتوزية ومؤشّرات البلعمة الذاتية مع بقائها قابلة للاستدامة."),
    },

    # ---------------------------------------------------------------- MENTAL
    {
        "key": "m_journal_deep", "pillar": "mental", "anchor": "isha",
        "minutes": 15, "level": 2, "min_phase": 2,
        "title": T("Deep Journalling", "Menulis Jurnal Mendalam", "كتابة تأمّلية عميقة"),
        "desc": T(
            "Fifteen minutes on one prompt: what am I avoiding, and what would tawakkul look like here?",
            "Lima belas menit untuk satu pertanyaan: apa yang saya hindari, dan bagaimana bentuk tawakal di sini?",
            "خمس عشرة دقيقة على سؤال واحد: ما الذي أتجنّبه؟ وكيف يكون التوكّل في هذا الأمر؟"),
        "science": T(
            "Expressive writing for 15 minutes over a few days improves immune markers and lowers depressive symptoms months later (Pennebaker, Journal of Abnormal Psychology).",
            "Menulis ekspresif 15 menit selama beberapa hari memperbaiki penanda imun dan menurunkan gejala depresi berbulan-bulan kemudian (Journal of Abnormal Psychology).",
            "الكتابة التعبيرية ١٥ دقيقة لعدة أيام تحسّن مؤشّرات المناعة وتخفّض أعراض الاكتئاب بعد أشهر."),
    },
    {
        "key": "m_silence", "pillar": "mental", "anchor": "asr",
        "minutes": 30, "level": 2, "min_phase": 3,
        "title": T("Thirty Minutes of Silence", "Tiga Puluh Menit Sunyi", "ثلاثون دقيقة صمت"),
        "desc": T(
            "No speaking, no audio, no screens for thirty minutes. Just sit, walk or work quietly.",
            "Tanpa bicara, tanpa audio, tanpa layar selama tiga puluh menit. Cukup duduk, berjalan, atau bekerja dalam sepi.",
            "بلا كلام ولا صوت ولا شاشة لثلاثين دقيقة: اجلس أو امشِ أو اعمل في هدوء."),
        "hadith": T(
            "Whoever believes in Allah and the Last Day, let him speak good or stay silent. (Sahih al-Bukhari 6018)",
            "Barangsiapa beriman kepada Allah dan hari akhir, hendaklah berkata baik atau diam. (Sahih Bukhari 6018)",
            "«مَن كان يؤمن بالله واليوم الآخر فليقل خيرًا أو ليصمت». (صحيح البخاري ٦٠١٨)"),
        "science": T(
            "Two hours of silence triggered hippocampal neurogenesis in animal models, and quiet periods lower blood pressure more than relaxing music (Brain Structure & Function; Heart).",
            "Dua jam kesunyian memicu neurogenesis hipokampus pada model hewan, dan periode sunyi menurunkan tekanan darah lebih baik daripada musik menenangkan (Heart).",
            "ساعتان من الصمت حفّزت تكوّن خلايا عصبية في الحُصين في نماذج حيوانية، والهدوء يخفّض الضغط أكثر من الموسيقى المهدّئة."),
    },
    {
        "key": "m_learn_skill", "pillar": "mental", "anchor": "anytime",
        "minutes": 20, "level": 2, "min_phase": 2,
        "title": T("Twenty Minutes of Learning", "Dua Puluh Menit Belajar", "عشرون دقيقة تعلّم"),
        "desc": T(
            "Twenty focused minutes on one beneficial skill — Arabic, tajweed, a trade, a language. Same skill every day.",
            "Dua puluh menit fokus pada satu keterampilan bermanfaat — bahasa Arab, tajwid, keahlian kerja, bahasa. Keterampilan yang sama setiap hari.",
            "عشرون دقيقة تركيز على مهارة نافعة واحدة: العربية، التجويد، حرفة، لغة. المهارة نفسها كل يوم."),
        "science": T(
            "Deliberate practice in short daily blocks beats long infrequent sessions; 20 minutes daily reaches conversational competence in a language in under a year (Ericsson; Applied Linguistics).",
            "Latihan sengaja dalam blok harian singkat mengalahkan sesi panjang yang jarang; 20 menit sehari mencapai kemampuan percakapan sebuah bahasa dalam kurang dari setahun (Applied Linguistics).",
            "التدريب المتعمّد في جرعات يومية قصيرة يتفوّق على الجلسات الطويلة المتباعدة، و٢٠ دقيقة يوميًا تكفي للوصول إلى مستوى محادثة في أقل من سنة."),
    },
    {
        "key": "m_silat_rahm", "pillar": "mental", "anchor": "maghrib",
        "minutes": 18, "level": 2, "min_phase": 2,
        "title": T("Mend One Relationship", "Perbaiki Satu Hubungan", "صِل رحمًا واحدة"),
        "desc": T(
            "Call or visit one relative today — especially the one you have drifted from. No agenda, just presence.",
            "Telepon atau kunjungi satu kerabat hari ini — terutama yang sudah jauh. Tanpa agenda, cukup hadir.",
            "اتّصل أو زُر قريبًا واحدًا اليوم، خاصة من انقطعت عنه. بلا غاية، حضورٌ فقط."),
        "hadith": T(
            "Whoever wishes for his provision to be increased and his life extended, let him maintain ties of kinship. (Sahih al-Bukhari 5986)",
            "Barangsiapa ingin rezekinya dilapangkan dan umurnya dipanjangkan, hendaklah menyambung silaturahmi. (Sahih Bukhari 5986)",
            "«مَن أحبّ أن يُبسط له في رزقه ويُنسأ له في أثره فليصل رحمه». (صحيح البخاري ٥٩٨٦)"),
        "science": T(
            "Social connection is a stronger predictor of longevity than smoking, obesity or exercise — a 50% increased survival odds across 148 studies (Holt-Lunstad, PLOS Medicine).",
            "Koneksi sosial adalah prediktor umur panjang yang lebih kuat daripada merokok, obesitas, atau olahraga — peluang bertahan 50% lebih tinggi pada 148 studi (PLOS Medicine).",
            "الترابط الاجتماعي مؤشّر على طول العمر أقوى من التدخين والسمنة والرياضة، برفع فرص البقاء ٥٠٪ في ١٤٨ دراسة."),
    },
    {
        "key": "m_akhirah", "pillar": "mental", "anchor": "night",
        "minutes": 10, "level": 3, "min_phase": 3,
        "title": T("Remember the Hereafter", "Ingat Akhirat", "تذكّر الآخرة"),
        "desc": T(
            "Ten quiet minutes: if this were my last night, what would I regret, and what would I stop worrying about?",
            "Sepuluh menit tenang: jika ini malam terakhirku, apa yang akan kusesali, dan apa yang tak perlu lagi kukhawatirkan?",
            "عشر دقائق هادئة: لو كانت هذه ليلتي الأخيرة، فعلى ماذا أندم؟ وما الذي سيسقط عن همّي؟"),
        "hadith": T(
            "Visit graves, for it reminds one of the Hereafter. (Sahih Muslim 976)",
            "Berziarahlah ke kubur, karena ia mengingatkan akhirat. (Sahih Muslim 976)",
            "«زوروا القبور فإنها تُذكّر الآخرة». (صحيح مسلم ٩٧٦)"),
        "science": T(
            "Structured mortality reflection ('memento mori') reliably shifts values from extrinsic to intrinsic goals and increases prosocial behaviour (Terror Management Theory; Personality and Social Psychology Review).",
            "Refleksi kematian yang terstruktur secara konsisten menggeser nilai dari tujuan ekstrinsik ke intrinsik dan meningkatkan perilaku prososial (Personality and Social Psychology Review).",
            "التأمّل المنظّم في الموت ينقل القيم من الأهداف الخارجية إلى الداخلية ويزيد السلوك النافع للناس."),
    },
    {
        "key": "m_no_complaint", "pillar": "mental", "anchor": "anytime",
        "minutes": 8, "level": 2, "min_phase": 3,
        "title": T("A Day Without Complaining", "Sehari Tanpa Mengeluh", "يوم بلا شكوى"),
        "desc": T(
            "No complaining out loud for one full day. When you catch yourself, say Alhamdulillah instead and start again.",
            "Tidak mengeluh dengan lisan selama satu hari penuh. Saat tersadar, ucapkan Alhamdulillah dan mulai lagi.",
            "لا شكوى بلسانك يومًا كاملًا. وإذا انتبهت لنفسك فقل الحمد لله وابدأ من جديد."),
        "quran": T(
            "\"And be patient — indeed, Allah is with the patient.\" (Al-Anfal 8:46)",
            "\"Dan bersabarlah — sungguh Allah bersama orang-orang yang sabar.\" (QS Al-Anfal 8:46)",
            "﴿وَاصْبِرُوا إِنَّ اللَّهَ مَعَ الصَّابِرِينَ﴾ (الأنفال: ٤٦)"),
        "science": T(
            "Habitual complaining strengthens negative neural pathways and correlates with elevated cortisol; interrupting the verbal habit measurably reduces perceived stress (Psychoneuroendocrinology).",
            "Kebiasaan mengeluh memperkuat jalur saraf negatif dan berkorelasi dengan kortisol tinggi; memutus kebiasaan verbal ini menurunkan stres yang dirasakan secara terukur (Psychoneuroendocrinology).",
            "الشكوى المعتادة تقوّي المسارات العصبية السلبية وترتبط بارتفاع الكورتيزول، وقطع هذه العادة اللفظية يخفّض التوتر بشكل ملموس."),
    },
    {
        "key": "m_teach", "pillar": "mental", "anchor": "anytime",
        "minutes": 15, "level": 3, "min_phase": 4,
        "title": T("Teach What You Learned", "Ajarkan yang Anda Pelajari", "علّم ما تعلّمت"),
        "desc": T(
            "Explain one thing you learned this week to another person — a child, a spouse, a friend. Teaching seals it.",
            "Jelaskan satu hal yang Anda pelajari pekan ini kepada orang lain — anak, pasangan, sahabat. Mengajar mengunci ilmu.",
            "اشرح لشخص آخر شيئًا تعلّمته هذا الأسبوع: لطفل أو زوج أو صاحب. التعليم يثبّت العلم."),
        "hadith": T(
            "Convey from me, even a single verse. (Sahih al-Bukhari 3461)",
            "Sampaikan dariku, walau satu ayat. (Sahih Bukhari 3461)",
            "«بلّغوا عنّي ولو آية». (صحيح البخاري ٣٤٦١)"),
        "science": T(
            "The protégé effect: learning material in order to teach it produces significantly better recall and organisation than learning to be tested (Memory & Cognition, 2014).",
            "Efek protégé: mempelajari materi untuk mengajarkannya menghasilkan daya ingat dan penataan yang jauh lebih baik daripada belajar untuk diuji (Memory & Cognition, 2014).",
            "«أثر التلميذ»: التعلّم بنيّة التعليم ينتج تذكّرًا وتنظيمًا أفضل بكثير من التعلّم بنيّة الاختبار."),
    },
]
