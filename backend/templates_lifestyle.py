"""Healthy-lifestyle habit templates: food & drink, movement, supplements-as-
habits and time-specific mindfulness windows. EN + ID only.

`boost`  — health flags / goals that make this habit a better fit.
`contra` — health flags that exclude it for this user.
"""


def T(en: str, idn: str) -> dict:
    return {"en": en, "id": idn}


LIFESTYLE_TEMPLATES: list[dict] = [
    # ------------------------------------------------------------ FOOD & DRINK
    {
        "key": "n_talbina_breakfast", "pillar": "nutrition", "anchor": "morning",
        "minutes": 10, "level": 1, "min_phase": 1,
        "boost": ["lipid_focus", "gut_focus", "weight_focus", "healthy_eating"],
        "title": T("Talbina Barley Breakfast", "Sarapan Talbina (Bubur Barley)"),
        "desc": T(
            "Simmer 2 tbsp barley flour in a cup of milk or water for 5 minutes, sweeten with a little honey. Warm, soft, slow-release energy until Dhuhr.",
            "Rebus 2 sdm tepung barley (jelai) dengan segelas susu atau air selama 5 menit, tambahkan sedikit madu. Hangat, lembut, energi lepas-lambat sampai Dzuhur."),
        "hadith": T(
            "Talbina soothes the heart of the sick and takes away some of the grief. (Sahih al-Bukhari 5689)",
            "Talbina menenangkan hati orang sakit dan menghilangkan sebagian kesedihan. (Sahih Bukhari 5689)"),
        "science": T(
            "3 g/day of barley beta-glucan lowers LDL cholesterol 5–10% within 6 weeks by binding bile acids; it also feeds gut bifidobacteria (British Journal of Nutrition; EFSA health claim).",
            "3 g beta-glukan barley per hari menurunkan kolesterol LDL 5–10% dalam 6 minggu dengan mengikat asam empedu, sekaligus menjadi makanan bifidobakteri usus (British Journal of Nutrition; klaim kesehatan EFSA)."),
    },
    {
        "key": "n_vinegar_water", "pillar": "nutrition", "anchor": "dhuhr",
        "minutes": 2, "level": 1, "min_phase": 1,
        "boost": ["glucose_focus", "weight_focus"], "contra": ["gut_focus"],
        "title": T("Vinegar Water Before Lunch", "Air Cuka Sebelum Makan Siang"),
        "desc": T(
            "One tablespoon of apple-cider or date vinegar in a large glass of water, 10 minutes before your biggest carbohydrate meal. Rinse your mouth after.",
            "Satu sendok makan cuka apel atau cuka kurma dalam segelas besar air, 10 menit sebelum makan berkarbohidrat terbanyak. Bilas mulut setelahnya."),
        "hadith": T(
            "What an excellent condiment vinegar is. (Sahih Muslim 2051)",
            "Sebaik-baik lauk adalah cuka. (Sahih Muslim 2051)"),
        "science": T(
            "Acetic acid before a starchy meal blunts the post-meal glucose rise by ~20% and improves insulin sensitivity in insulin-resistant adults (Diabetes Care 2004; meta-analysis, BMC Complementary Medicine 2021).",
            "Asam asetat sebelum makan berpati menumpulkan lonjakan glukosa pascamakan ~20% dan memperbaiki sensitivitas insulin pada orang dengan resistensi insulin (Diabetes Care 2004; meta-analisis BMC Complementary Medicine 2021)."),
    },
    {
        "key": "n_ginger_honey", "pillar": "nutrition", "anchor": "maghrib",
        "minutes": 5, "level": 1, "min_phase": 1,
        "boost": ["gut_focus", "glucose_focus", "calm_focus"],
        "title": T("Warm Ginger & Honey After Maghrib", "Wedang Jahe Madu Setelah Maghrib"),
        "desc": T(
            "Slice fresh ginger into hot water, steep five minutes, add a teaspoon of honey once it is warm, not boiling. Replace tonight's sweet drink with it.",
            "Iris jahe segar ke dalam air panas, diamkan lima menit, tambahkan satu sendok teh madu saat sudah hangat, bukan mendidih. Ganti minuman manis malam ini dengannya."),
        "quran": T(
            "\"They will be given a cup whose mixture is of ginger.\" (Al-Insan 76:17)",
            "\"Di dalam surga itu mereka diberi minum segelas minuman yang campurannya adalah jahe.\" (QS Al-Insan 76:17)"),
        "science": T(
            "1–2 g of ginger daily lowers fasting glucose, HbA1c and inflammatory markers (CRP, TNF-α) in randomised trials, and is a first-line remedy for nausea (Nutrients 2019 meta-analysis).",
            "1–2 g jahe per hari menurunkan glukosa puasa, HbA1c dan penanda inflamasi (CRP, TNF-α) pada uji acak, serta menjadi pilihan pertama untuk mual (meta-analisis Nutrients 2019)."),
    },
    {
        "key": "n_veg_first", "pillar": "nutrition", "anchor": "dhuhr",
        "minutes": 12, "level": 1, "min_phase": 1,
        "boost": ["glucose_focus", "weight_focus", "healthy_eating"],
        "title": T("Vegetables First, Rice Last", "Sayur Dulu, Nasi Terakhir"),
        "desc": T(
            "At lunch, eat your vegetables and protein first, and only then the rice or bread. Same plate, different order.",
            "Saat makan siang, habiskan sayur dan lauk protein dulu, baru nasi atau roti. Piring yang sama, urutan berbeda."),
        "quran": T(
            "\"And We caused to grow within it grain, and grapes and herbage, and olives and palm trees.\" (Abasa 80:27–29)",
            "\"Lalu Kami tumbuhkan padanya biji-bijian, anggur dan sayur-sayuran, zaitun dan pohon kurma.\" (QS 'Abasa 80:27–29)"),
        "science": T(
            "Eating vegetables and protein before carbohydrates cuts the post-meal glucose peak by ~30–40% and insulin by ~50% in type 2 diabetes (Diabetes Care 2015; Cornell Weill).",
            "Makan sayur dan protein sebelum karbohidrat memangkas puncak glukosa pascamakan ~30–40% dan insulin ~50% pada diabetes tipe 2 (Diabetes Care 2015; Cornell Weill)."),
    },
    {
        "key": "n_protein_breakfast", "pillar": "nutrition", "anchor": "morning",
        "minutes": 10, "level": 1, "min_phase": 1,
        "boost": ["build_strength", "weight_focus", "gain_focus", "more_energy"],
        "title": T("25 g Protein at Breakfast", "25 g Protein Saat Sarapan"),
        "desc": T(
            "Two eggs and a slice of tempe, or fish with rice, or Greek yoghurt with nuts. Aim for a palm-sized portion of protein before anything sweet.",
            "Dua telur dan sepotong tempe, atau ikan dengan nasi, atau yoghurt Yunani dengan kacang. Targetkan protein seukuran telapak tangan sebelum yang manis-manis."),
        "quran": T(
            "\"It is He who subjected the sea for you to eat from it tender meat.\" (An-Nahl 16:14)",
            "\"Dialah yang menundukkan lautan untukmu agar kamu dapat memakan daging yang segar darinya.\" (QS An-Nahl 16:14)"),
        "science": T(
            "25–30 g of protein per meal maximises muscle protein synthesis; a high-protein breakfast reduces evening snacking and cravings by lowering ghrelin (American Journal of Clinical Nutrition 2013).",
            "25–30 g protein per makan memaksimalkan sintesis protein otot; sarapan tinggi protein mengurangi ngemil malam dan rasa ingin makan dengan menurunkan ghrelin (American Journal of Clinical Nutrition 2013)."),
    },
    {
        "key": "n_sodium_swap", "pillar": "nutrition", "anchor": "dhuhr",
        "minutes": 5, "level": 1, "min_phase": 1,
        "boost": ["bp_focus", "low_sodium"],
        "title": T("Salt Swap: Lemon, Herbs, Spices", "Ganti Garam: Jeruk, Rempah, Daun"),
        "desc": T(
            "No added salt at the table today. Season with lime, black pepper, garlic, turmeric, coriander or lemongrass instead. Skip instant seasoning cubes.",
            "Tanpa garam tambahan di meja hari ini. Bumbui dengan jeruk nipis, merica, bawang putih, kunyit, ketumbar, atau serai. Hindari penyedap instan."),
        "quran": T(
            "\"Eat and drink, but be not excessive. Indeed, He likes not those who commit excess.\" (Al-A'raf 7:31)",
            "\"Makan dan minumlah, tetapi jangan berlebihan. Sungguh, Allah tidak menyukai orang yang berlebihan.\" (QS Al-A'raf 7:31)"),
        "science": T(
            "Cutting sodium to under 2 g/day lowers systolic blood pressure by about 5 mmHg in hypertensive adults, comparable to one medication (Cochrane 2020; WHO guideline).",
            "Menurunkan natrium di bawah 2 g/hari menurunkan tekanan sistolik sekitar 5 mmHg pada penderita hipertensi, setara satu obat (Cochrane 2020; pedoman WHO)."),
    },
    {
        "key": "n_fruit_dessert", "pillar": "nutrition", "anchor": "maghrib",
        "minutes": 5, "level": 1, "min_phase": 1,
        "boost": ["weight_focus", "glucose_focus", "low_sugar"],
        "title": T("Whole Fruit Instead of Dessert", "Buah Utuh Pengganti Hidangan Manis"),
        "desc": T(
            "Tonight's dessert is a whole fruit: papaya, guava, an apple, or a handful of berries. Chew it slowly; not juiced, not blended.",
            "Pencuci mulut malam ini adalah buah utuh: pepaya, jambu biji, apel, atau segenggam beri. Kunyah perlahan; bukan dijus, bukan diblender."),
        "quran": T(
            "\"And fruit of what they select.\" (Al-Waqi'ah 56:20)",
            "\"Dan buah-buahan dari apa yang mereka pilih.\" (QS Al-Waqi'ah 56:20)"),
        "science": T(
            "Whole fruit intake is linked to a lower risk of type 2 diabetes, while fruit juice raises it; the fibre matrix slows sugar absorption (BMJ 2013, 187,000 participants).",
            "Konsumsi buah utuh dikaitkan dengan risiko diabetes tipe 2 lebih rendah, sedangkan jus buah meningkatkannya; serat memperlambat penyerapan gula (BMJ 2013, 187.000 peserta)."),
    },
    {
        "key": "n_prayer_hydration", "pillar": "nutrition", "anchor": "anytime",
        "minutes": 2, "level": 1, "min_phase": 1,
        "boost": ["bp_focus", "glucose_focus", "more_energy", "desk_worker"],
        "title": T("One Glass at Every Prayer", "Segelas Air di Setiap Waktu Shalat"),
        "desc": T(
            "Tie water to wudu: one full glass before or after each of the five prayers. Five glasses locked in before you even think about it.",
            "Kaitkan minum dengan wudhu: segelas penuh sebelum atau sesudah setiap shalat lima waktu. Lima gelas tercapai tanpa perlu diingat-ingat."),
        "quran": T(
            "\"And We made from water every living thing.\" (Al-Anbiya 21:30)",
            "\"Dan Kami jadikan segala sesuatu yang hidup berasal dari air.\" (QS Al-Anbiya 21:30)"),
        "science": T(
            "Even 1–2% dehydration measurably worsens mood, headache and concentration; spacing intake through the day keeps plasma osmolality stable better than large boluses (Journal of Nutrition 2012).",
            "Dehidrasi 1–2% saja sudah memburukkan suasana hati, sakit kepala dan konsentrasi; minum tersebar sepanjang hari menjaga osmolalitas plasma lebih stabil daripada sekali banyak (Journal of Nutrition 2012)."),
    },
    {
        "key": "n_fermented", "pillar": "nutrition", "anchor": "dhuhr",
        "minutes": 5, "level": 1, "min_phase": 1,
        "boost": ["gut_focus", "healthy_eating"],
        "title": T("One Fermented Food Today", "Satu Makanan Fermentasi Hari Ini"),
        "desc": T(
            "Add tempe, plain yoghurt, kefir, or homemade pickles to one meal. Halal, live cultures, no added sugar.",
            "Tambahkan tempe, yoghurt tawar, kefir, atau acar buatan sendiri pada satu waktu makan. Halal, berkultur hidup, tanpa gula tambahan."),
        "hadith": T(
            "When the Prophet ﷺ drank milk he would say: O Allah, bless us in it and give us more of it. (Sunan Abi Dawud 3730)",
            "Ketika Nabi ﷺ minum susu beliau berdoa: Ya Allah, berkahilah kami padanya dan tambahkanlah bagi kami. (Sunan Abu Dawud 3730)"),
        "science": T(
            "A 10-week fermented-food diet increased gut microbiome diversity and reduced 19 inflammatory proteins including IL-6 (Stanford, Cell 2021).",
            "Diet makanan fermentasi selama 10 minggu meningkatkan keragaman mikrobioma usus dan menurunkan 19 protein inflamasi termasuk IL-6 (Stanford, Cell 2021)."),
    },
    {
        "key": "n_fish_twice", "pillar": "nutrition", "anchor": "dhuhr",
        "minutes": 15, "level": 1, "min_phase": 1,
        "boost": ["lipid_focus", "bp_focus", "mental_clarity"],
        "title": T("Fish for Lunch (Omega-3)", "Ikan untuk Makan Siang (Omega-3)"),
        "desc": T(
            "Grilled, steamed or pepes — not deep-fried. Mackerel (kembung), tuna, sardines or salmon. Twice a week is the target; today is one.",
            "Dibakar, dikukus, atau dipepes — bukan digoreng. Kembung, tongkol, sarden, atau salmon. Target dua kali seminggu; hari ini salah satunya."),
        "quran": T(
            "\"Lawful to you is game from the sea and its food.\" (Al-Ma'idah 5:96)",
            "\"Dihalalkan bagimu hewan buruan laut dan makanan yang berasal dari laut.\" (QS Al-Ma'idah 5:96)"),
        "science": T(
            "Two servings of oily fish a week (~250 mg EPA+DHA/day) is associated with 36% lower coronary death and lower triglycerides (JAMA 2006; AHA scientific statement 2018).",
            "Dua porsi ikan berlemak per minggu (~250 mg EPA+DHA/hari) dikaitkan dengan kematian koroner 36% lebih rendah dan trigliserida lebih rendah (JAMA 2006; pernyataan ilmiah AHA 2018)."),
    },
    {
        "key": "n_sun_vitd", "pillar": "nutrition", "anchor": "morning",
        "minutes": 12, "level": 1, "min_phase": 1,
        "boost": ["female", "bp_focus", "sleep_focus", "desk_worker"],
        "title": T("Morning Sun for Vitamin D", "Berjemur Pagi untuk Vitamin D"),
        "desc": T(
            "10–15 minutes of direct sun on forearms and face between 8 and 10 am, no glass in between. If you are rarely outside, ask your doctor to check 25-OH vitamin D.",
            "10–15 menit sinar matahari langsung pada lengan dan wajah antara jam 8–10 pagi, tanpa kaca penghalang. Jika jarang di luar, minta dokter memeriksa kadar 25-OH vitamin D."),
        "quran": T(
            "\"And made the sun a burning lamp.\" (Nuh 71:16)",
            "\"Dan menjadikan matahari sebagai pelita.\" (QS Nuh 71:16)"),
        "science": T(
            "Over 50% of adults in Indonesia and the Gulf are vitamin D deficient despite abundant sun, largely from indoor lifestyles; deficiency is linked to fatigue, bone loss and poor immunity (Nutrients 2020; Endocrine Society guideline).",
            "Lebih dari 50% orang dewasa di Indonesia dan Teluk kekurangan vitamin D meski matahari berlimpah, terutama karena gaya hidup di dalam ruangan; kekurangan ini terkait kelelahan, pengeroposan tulang dan imunitas lemah (Nutrients 2020; pedoman Endocrine Society)."),
    },
    {
        "key": "n_magnesium_evening", "pillar": "nutrition", "anchor": "isha",
        "minutes": 4, "level": 2, "min_phase": 1,
        "boost": ["sleep_focus", "calm_focus", "insomnia"],
        "title": T("Magnesium Evening", "Malam Kaya Magnesium"),
        "desc": T(
            "A handful of pumpkin seeds or almonds, or a serving of dark leafy greens with dinner. If your doctor agrees, 200–300 mg magnesium glycinate an hour before bed.",
            "Segenggam biji labu atau almond, atau seporsi sayuran hijau tua saat makan malam. Jika dokter setuju, 200–300 mg magnesium glisinat satu jam sebelum tidur."),
        "quran": T(
            "\"And it is He who sends down rain and brings forth thereby the growth of all things.\" (Al-An'am 6:99)",
            "\"Dan Dialah yang menurunkan air dari langit, lalu Kami tumbuhkan dengan air itu segala macam tumbuhan.\" (QS Al-An'am 6:99)"),
        "science": T(
            "Magnesium supplementation improved sleep onset, duration and insomnia severity scores in older adults, and lower magnesium intake is linked to poorer sleep (Journal of Research in Medical Sciences 2012; Sleep 2022 meta-analysis).",
            "Suplementasi magnesium memperbaiki waktu mulai tidur, durasi dan skor keparahan insomnia pada orang dewasa yang lebih tua; asupan magnesium rendah dikaitkan dengan tidur buruk (Journal of Research in Medical Sciences 2012; meta-analisis Sleep 2022)."),
    },
    {
        "key": "n_kitchen_closed", "pillar": "nutrition", "anchor": "isha",
        "minutes": 3, "level": 2, "min_phase": 1,
        "boost": ["weight_focus", "glucose_focus", "sleep_focus", "gut_focus"],
        "title": T("Kitchen Closed 3 Hours Before Sleep", "Dapur Tutup 3 Jam Sebelum Tidur"),
        "desc": T(
            "Finish your last bite three hours before bed. Water, or herbal tea, is fine. Notice how differently you wake up.",
            "Suapan terakhir tiga jam sebelum tidur. Air atau teh herbal boleh. Rasakan perbedaannya saat bangun."),
        "quran": T(
            "\"Eat and drink, but be not excessive.\" (Al-A'raf 7:31)",
            "\"Makan dan minumlah, tetapi jangan berlebihan.\" (QS Al-A'raf 7:31)"),
        "science": T(
            "A late dinner (22:00 vs 18:00) raises overnight glucose ~18% and cuts fat oxidation by ~10% in healthy adults; late eating also worsens reflux (Journal of Clinical Endocrinology & Metabolism 2020).",
            "Makan malam larut (22.00 vs 18.00) menaikkan glukosa semalam ~18% dan menurunkan pembakaran lemak ~10% pada orang sehat; makan larut juga memperburuk refluks (Journal of Clinical Endocrinology & Metabolism 2020)."),
    },

    # ------------------------------------------------------------ MOVEMENT
    {
        "key": "p_walk_20", "pillar": "physical", "anchor": "asr",
        "minutes": 20, "level": 1, "min_phase": 1,
        "boost": ["weight_focus", "bp_focus", "joint_friendly", "glucose_focus"],
        "title": T("Brisk 20-Minute Walk", "Jalan Cepat 20 Menit"),
        "desc": T(
            "A purposeful walk after Asr: fast enough that talking takes a little effort. Count it toward your daily step target.",
            "Jalan bertujuan setelah Ashar: cukup cepat sampai berbicara terasa sedikit berat. Hitung ke target langkah harian Anda."),
        "hadith": T(
            "When the Prophet ﷺ walked, he walked briskly, as if the earth were folding up beneath him. (Shama'il at-Tirmidhi)",
            "Ketika Nabi ﷺ berjalan, beliau berjalan cepat seakan bumi dilipat untuknya. (Syama'il at-Tirmidzi)"),
        "science": T(
            "Adults averaging 7,000+ steps a day had 50–70% lower all-cause mortality over 11 years than those under 7,000 (JAMA Network Open 2021).",
            "Orang dewasa dengan rata-rata 7.000+ langkah per hari memiliki mortalitas semua sebab 50–70% lebih rendah selama 11 tahun dibanding di bawah 7.000 (JAMA Network Open 2021)."),
    },
    {
        "key": "p_band_strength", "pillar": "physical", "anchor": "asr",
        "minutes": 12, "level": 1, "min_phase": 1,
        "boost": ["build_strength", "joint_friendly", "female"],
        "title": T("Resistance Band Circuit", "Sirkuit Resistance Band"),
        "desc": T(
            "Two rounds at home: 12 band rows, 12 band squats, 12 overhead presses, 12 glute bridges. Slow on the way down. No gym, no mixed space needed.",
            "Dua putaran di rumah: 12 row band, 12 squat band, 12 overhead press, 12 glute bridge. Perlahan saat menurunkan. Tanpa gym, tanpa ruang campur."),
        "hadith": T(
            "The strong believer is better and more beloved to Allah than the weak believer. (Sahih Muslim 2664)",
            "Mukmin yang kuat lebih baik dan lebih dicintai Allah daripada mukmin yang lemah. (Sahih Muslim 2664)"),
        "science": T(
            "Elastic-band training produces strength gains comparable to free weights in untrained and older adults, with lower joint load (SAGE Open Medicine 2019 meta-analysis).",
            "Latihan band elastis menghasilkan peningkatan kekuatan sebanding dengan beban bebas pada orang tak terlatih dan lansia, dengan beban sendi lebih rendah (meta-analisis SAGE Open Medicine 2019)."),
    },
    {
        "key": "p_desk_breaks", "pillar": "physical", "anchor": "anytime",
        "minutes": 6, "level": 1, "min_phase": 1,
        "boost": ["desk_worker", "bp_focus", "glucose_focus"],
        "title": T("Desk Reset Every 45 Minutes", "Reset Meja Setiap 45 Menit"),
        "desc": T(
            "Set a timer. Every 45 minutes: stand, 10 slow squats or calf raises, roll the shoulders, look 20 metres away for 20 seconds. Two minutes, then back.",
            "Pasang timer. Setiap 45 menit: berdiri, 10 squat perlahan atau angkat tumit, putar bahu, lihat objek 20 meter jauhnya selama 20 detik. Dua menit, lalu lanjut."),
        "hadith": T(
            "Your body has a right over you. (Sahih al-Bukhari 1975)",
            "Tubuhmu memiliki hak atas dirimu. (Sahih Bukhari 1975)"),
        "science": T(
            "Sitting more than 8 hours a day raises mortality risk unless offset by 60–75 minutes of daily movement; frequent 2-minute breaks flatten glucose and blood-pressure curves (Lancet 2016; Diabetes Care 2016).",
            "Duduk lebih dari 8 jam sehari menaikkan risiko kematian kecuali diimbangi 60–75 menit gerak harian; jeda 2 menit yang sering meratakan kurva glukosa dan tekanan darah (Lancet 2016; Diabetes Care 2016)."),
    },
    {
        "key": "p_isha_stretch", "pillar": "physical", "anchor": "isha",
        "minutes": 5, "level": 1, "min_phase": 1,
        "boost": ["joint_friendly", "sleep_focus", "desk_worker"],
        "title": T("Hip & Back Stretch on the Mat", "Peregangan Pinggul & Punggung di Sajadah"),
        "desc": T(
            "After Isha, stay on the mat: child's pose 40 s, seated forward fold 40 s, figure-four hip stretch 30 s each side, gentle spinal twist 30 s each side.",
            "Setelah Isya, tetap di sajadah: posisi sujud panjang 40 detik, duduk membungkuk ke depan 40 detik, peregangan pinggul angka-empat 30 detik tiap sisi, putar tulang belakang lembut 30 detik tiap sisi."),
        "hadith": T(
            "The closest a servant is to his Lord is when he is in prostration. (Sahih Muslim 482)",
            "Saat seorang hamba paling dekat dengan Rabbnya adalah ketika ia bersujud. (Sahih Muslim 482)"),
        "science": T(
            "Evening static stretching improved sleep quality and reduced chronic low-back pain intensity in randomised trials, likely via parasympathetic activation (International Journal of Environmental Research and Public Health 2021).",
            "Peregangan statis malam memperbaiki kualitas tidur dan menurunkan intensitas nyeri punggung bawah kronis pada uji acak, kemungkinan melalui aktivasi parasimpatis (International Journal of Environmental Research and Public Health 2021)."),
    },
    {
        "key": "p_sit_to_stand", "pillar": "physical", "anchor": "asr",
        "minutes": 6, "level": 1, "min_phase": 1,
        "boost": ["joint_friendly", "balance_focus", "build_strength"],
        "title": T("Sit-to-Stand ×30", "Duduk-Berdiri ×30"),
        "desc": T(
            "From a chair, stand fully and sit back down slowly, arms crossed. Three sets of ten. This is the exact strength that carries you through long qiyam.",
            "Dari kursi, berdiri penuh lalu duduk kembali perlahan, tangan menyilang di dada. Tiga set sepuluh kali. Inilah kekuatan yang menopang qiyam panjang."),
        "science": T(
            "Sit-to-stand capacity independently predicts survival in adults over 50; STS training improves knee-osteoarthritis function scores by ~25% (European Journal of Preventive Cardiology 2014; Arthritis Care & Research).",
            "Kemampuan duduk-berdiri memprediksi kelangsungan hidup pada orang dewasa di atas 50 tahun; latihan STS memperbaiki skor fungsi osteoartritis lutut ~25% (European Journal of Preventive Cardiology 2014; Arthritis Care & Research)."),
    },
    {
        "key": "p_incline_pushup", "pillar": "physical", "anchor": "morning",
        "minutes": 7, "level": 1, "min_phase": 1,
        "boost": ["build_strength", "female", "joint_friendly"],
        "title": T("Incline Push-Up Ladder", "Tangga Push-Up Miring"),
        "desc": T(
            "Hands on a wall, then a table, then a chair as you get stronger. Three sets of 8–12, elbows at 45°. Progress one level when 12 feels easy.",
            "Tangan di tembok, lalu meja, lalu kursi seiring bertambah kuat. Tiga set 8–12 kali, siku 45°. Naik satu level saat 12 kali terasa ringan."),
        "hadith": T(
            "Take advantage of your health before your sickness. (Reported by al-Hakim, from Ibn Abbas)",
            "Manfaatkan sehatmu sebelum sakitmu. (Diriwayatkan al-Hakim, dari Ibnu Abbas)"),
        "science": T(
            "Upper-body strength (grip and push capacity) predicts cardiovascular mortality better than blood pressure in a 140,000-person cohort; incline progressions allow safe progressive overload (BMJ 2018; Lancet 2015).",
            "Kekuatan tubuh atas (genggaman dan dorongan) memprediksi kematian kardiovaskular lebih baik daripada tekanan darah pada kohort 140.000 orang; progresi miring memungkinkan penambahan beban yang aman (BMJ 2018; Lancet 2015)."),
    },
    {
        "key": "p_maghrib_family_walk", "pillar": "physical", "anchor": "maghrib",
        "minutes": 15, "level": 1, "min_phase": 1,
        "boost": ["glucose_focus", "weight_focus", "calm_focus"],
        "title": T("After-Dinner Walk With Family", "Jalan Sore Bersama Keluarga"),
        "desc": T(
            "Fifteen unhurried minutes after the evening meal, with a spouse, child or parent. Talk. No phones.",
            "Lima belas menit santai setelah makan malam, bersama pasangan, anak, atau orang tua. Berbincang. Tanpa ponsel."),
        "quran": T(
            "\"The servants of the Most Merciful are those who walk upon the earth humbly.\" (Al-Furqan 25:63)",
            "\"Hamba-hamba Tuhan Yang Maha Pengasih adalah orang-orang yang berjalan di bumi dengan rendah hati.\" (QS Al-Furqan 25:63)"),
        "science": T(
            "A 10–15-minute walk right after a meal lowers the glucose spike by about 22% — more than a single 45-minute walk at another time (Diabetologia 2016; Sports Medicine 2022).",
            "Jalan 10–15 menit tepat setelah makan menurunkan lonjakan glukosa sekitar 22% — lebih efektif daripada satu kali jalan 45 menit di waktu lain (Diabetologia 2016; Sports Medicine 2022)."),
    },
    {
        "key": "p_zone2", "pillar": "physical", "anchor": "asr",
        "minutes": 25, "level": 2, "min_phase": 2,
        "boost": ["more_energy", "lipid_focus", "weight_focus"],
        "title": T("Zone-2 Cardio: Talk-Test Pace", "Kardio Zona 2: Masih Bisa Bicara"),
        "desc": T(
            "25 minutes of cycling, swimming (modest swimwear) or fast walking at a pace where you can still speak a full sentence. Steady, not heroic.",
            "25 menit bersepeda, berenang (pakaian renang tertutup), atau jalan cepat pada kecepatan yang masih memungkinkan bicara satu kalimat penuh. Stabil, tidak heroik."),
        "science": T(
            "Zone-2 training increases mitochondrial density and fat oxidation and improves insulin sensitivity more than higher intensities of equal calorie cost (Cell Metabolism 2017; Sports Medicine 2020).",
            "Latihan zona 2 meningkatkan kepadatan mitokondria dan pembakaran lemak serta memperbaiki sensitivitas insulin lebih dari intensitas tinggi dengan kalori setara (Cell Metabolism 2017; Sports Medicine 2020)."),
    },
    {
        "key": "p_stair_snacks", "pillar": "physical", "anchor": "anytime",
        "minutes": 6, "level": 2, "min_phase": 2,
        "boost": ["more_energy", "weight_focus"], "contra": ["no_hiit", "joint_friendly"],
        "title": T("Stair-Climbing Snacks", "Camilan Gerak: Naik Tangga"),
        "desc": T(
            "Three times today, climb 3 flights of stairs briskly (about 60 seconds), spread across the day. That is the whole workout.",
            "Tiga kali hari ini, naiki 3 lantai tangga dengan cepat (sekitar 60 detik), tersebar sepanjang hari. Itu saja latihannya."),
        "science": T(
            "Three 60-second stair-climbing bouts a day improved cardiorespiratory fitness by ~5% in six weeks in sedentary adults (Applied Physiology, Nutrition, and Metabolism 2019).",
            "Tiga kali naik tangga 60 detik per hari meningkatkan kebugaran kardiorespirasi ~5% dalam enam minggu pada orang dewasa yang kurang gerak (Applied Physiology, Nutrition, and Metabolism 2019)."),
    },

    # ------------------------------------------------------------ MIND WINDOWS
    {
        "key": "m_fajr_clear_hour", "pillar": "mental", "anchor": "fajr",
        "minutes": 10, "level": 1, "min_phase": 1,
        "boost": ["desk_worker", "calm_focus", "mental_clarity"],
        "title": T("The Clear Hour After Fajr", "Jam Jernih Setelah Subuh"),
        "desc": T(
            "Before any screen: write tomorrow's top three tasks for today, in order. The first hour after Fajr is the clearest your mind will be all day. Guard it.",
            "Sebelum layar apa pun: tulis tiga tugas terpenting hari ini, berurutan. Satu jam setelah Subuh adalah saat pikiran paling jernih sepanjang hari. Jagalah."),
        "hadith": T(
            "O Allah, bless my Ummah in their early mornings. (Sunan Abi Dawud 2606)",
            "Ya Allah, berkahilah umatku pada waktu pagi mereka. (Sunan Abu Dawud 2606)"),
        "science": T(
            "The cortisol awakening response peaks 30–45 minutes after waking, the window of highest executive function; checking a phone first thing raises perceived stress for the rest of the morning (Psychoneuroendocrinology; Computers in Human Behavior 2020).",
            "Respons kortisol bangun memuncak 30–45 menit setelah bangun, jendela fungsi eksekutif tertinggi; membuka ponsel pertama kali meningkatkan stres yang dirasakan sepanjang pagi (Psychoneuroendocrinology; Computers in Human Behavior 2020)."),
    },
    {
        "key": "m_qailulah", "pillar": "mental", "anchor": "dhuhr",
        "minutes": 20, "level": 1, "min_phase": 1,
        "boost": ["more_energy", "shift_worker", "mental_clarity"], "contra": ["insomnia"],
        "title": T("Qailulah: 20-Minute Nap", "Qailulah: Tidur Siang 20 Menit"),
        "desc": T(
            "After Dhuhr, lie down for 15–20 minutes with an alarm. Not longer — you want to wake before deep sleep begins.",
            "Setelah Dzuhur, berbaring 15–20 menit dengan alarm. Jangan lebih — bangunlah sebelum tidur dalam dimulai."),
        "hadith": T(
            "Take a midday nap, for the devils do not nap. (al-Mu'jam al-Awsat, at-Tabarani — graded hasan by some scholars)",
            "Tidur sianglah (qailulah), karena setan tidak tidur siang. (al-Mu'jam al-Awsat, Thabrani — dinilai hasan oleh sebagian ulama)"),
        "science": T(
            "A 10–20-minute nap improves alertness and memory for up to three hours without sleep inertia; NASA found a 26-minute nap raised pilot alertness 54% (Sleep 2006; NASA Ames).",
            "Tidur siang 10–20 menit meningkatkan kewaspadaan dan memori hingga tiga jam tanpa rasa linglung; NASA menemukan tidur 26 menit menaikkan kewaspadaan pilot 54% (Sleep 2006; NASA Ames)."),
    },
    {
        "key": "m_sunset_tafakkur", "pillar": "mental", "anchor": "maghrib",
        "minutes": 5, "level": 1, "min_phase": 1,
        "boost": ["calm_focus", "reduce_stress"],
        "title": T("Five Minutes of Sunset", "Lima Menit Senja"),
        "desc": T(
            "Before Maghrib, stand where you can see the sky. Watch the light change for five minutes and let it end in dua. Nothing to achieve.",
            "Sebelum Maghrib, berdirilah di tempat yang bisa melihat langit. Amati perubahan cahaya lima menit dan akhiri dengan doa. Tidak ada yang perlu dicapai."),
        "quran": T(
            "\"Have they not looked at the sky above them — how We structured it and adorned it?\" (Qaf 50:6)",
            "\"Tidakkah mereka memperhatikan langit di atas mereka, bagaimana Kami membangunnya dan menghiasinya?\" (QS Qaf 50:6)"),
        "science": T(
            "Experiences of awe lower the inflammatory cytokine IL-6 and increase wellbeing more than other positive emotions (Emotion 2015, UC Berkeley).",
            "Pengalaman takjub (awe) menurunkan sitokin inflamasi IL-6 dan meningkatkan kesejahteraan lebih dari emosi positif lainnya (Emotion 2015, UC Berkeley)."),
    },
    {
        "key": "m_digital_sunset", "pillar": "mental", "anchor": "night",
        "minutes": 5, "level": 1, "min_phase": 1,
        "boost": ["sleep_focus", "insomnia", "calm_focus"],
        "title": T("Digital Sunset", "Matahari Terbenam Digital"),
        "desc": T(
            "Sixty minutes before sleep, every screen goes dark and out of reach. Dim the lights. Read, talk, or recite instead.",
            "Enam puluh menit sebelum tidur, semua layar dimatikan dan dijauhkan. Redupkan lampu. Membaca, berbincang, atau mengaji sebagai gantinya."),
        "hadith": T(
            "The Prophet ﷺ disliked sleeping before Isha and idle talk after it. (Sahih al-Bukhari 568)",
            "Nabi ﷺ tidak menyukai tidur sebelum Isya dan berbincang sia-sia setelahnya. (Sahih Bukhari 568)"),
        "science": T(
            "Evening screen light suppresses melatonin by about 50% and delays the circadian clock by 1.5 hours, cutting REM sleep (PNAS 2015, Harvard).",
            "Cahaya layar malam menekan melatonin sekitar 50% dan menunda jam sirkadian 1,5 jam, mengurangi tidur REM (PNAS 2015, Harvard)."),
    },
    {
        "key": "m_right_side_sleep", "pillar": "mental", "anchor": "night",
        "minutes": 3, "level": 1, "min_phase": 1,
        "boost": ["sleep_focus", "insomnia", "bp_focus"],
        "title": T("Sleep Sunnah: Right Side, Same Time", "Sunnah Tidur: Miring Kanan, Waktu Tetap"),
        "desc": T(
            "Wudu, then lie on your right side with your hand under your cheek, at the same time as last night. Consistency of bedtime is the goal.",
            "Berwudhu, lalu berbaring miring ke kanan dengan tangan di bawah pipi, pada jam yang sama seperti malam sebelumnya. Konsistensi jam tidur adalah tujuannya."),
        "hadith": T(
            "When you go to bed, perform wudu as for prayer, then lie down on your right side. (Sahih al-Bukhari 247)",
            "Jika engkau hendak tidur, berwudhulah seperti wudhu untuk shalat, lalu berbaringlah miring ke kanan. (Sahih Bukhari 247)"),
        "science": T(
            "Right-lateral sleeping lowers sympathetic activity and heart rate versus supine or left-side positions; a regular bedtime predicts sleep quality better than duration (American Journal of Cardiology 2003; Sleep 2018).",
            "Tidur miring ke kanan menurunkan aktivitas simpatis dan denyut jantung dibanding telentang atau miring kiri; jam tidur teratur memprediksi kualitas tidur lebih baik daripada durasi (American Journal of Cardiology 2003; Sleep 2018)."),
    },
    {
        "key": "m_box_breath_asr", "pillar": "mental", "anchor": "asr",
        "minutes": 4, "level": 1, "min_phase": 1,
        "boost": ["calm_focus", "bp_focus", "desk_worker"],
        "title": T("Box Breathing at the Asr Slump", "Napas Kotak Saat Lesu Ashar"),
        "desc": T(
            "After Asr: inhale 4, hold 4, exhale 4, hold 4. Twelve rounds, eyes closed. Then one istighfar and back to work.",
            "Setelah Ashar: tarik 4, tahan 4, buang 4, tahan 4. Dua belas putaran, mata terpejam. Lalu satu istighfar dan kembali bekerja."),
        "quran": T(
            "\"Surely in the remembrance of Allah do hearts find rest.\" (Ar-Ra'd 13:28)",
            "\"Ingatlah, hanya dengan mengingat Allah hati menjadi tenang.\" (QS Ar-Ra'd 13:28)"),
        "science": T(
            "Slow breathing near six breaths per minute raises heart-rate variability and reduces blood pressure and anxiety within minutes (Frontiers in Psychology 2017; Scientific Reports 2023).",
            "Napas lambat sekitar enam kali per menit meningkatkan variabilitas denyut jantung serta menurunkan tekanan darah dan kecemasan dalam hitungan menit (Frontiers in Psychology 2017; Scientific Reports 2023)."),
    },
    {
        "key": "m_single_task", "pillar": "mental", "anchor": "anytime",
        "minutes": 25, "level": 2, "min_phase": 1,
        "boost": ["desk_worker", "mental_clarity"],
        "title": T("One Task, 25 Minutes, Then Dhikr", "Satu Tugas, 25 Menit, Lalu Dzikir"),
        "desc": T(
            "Pick one task. Phone face-down in another room. Work 25 minutes on it alone, then a 3-minute dhikr break. One block is enough today.",
            "Pilih satu tugas. Ponsel dibalik di ruangan lain. Kerjakan 25 menit hanya itu, lalu jeda dzikir 3 menit. Satu blok cukup untuk hari ini."),
        "hadith": T(
            "Allah has prescribed excellence (ihsan) in everything. (Sahih Muslim 1955)",
            "Sesungguhnya Allah mewajibkan ihsan dalam segala sesuatu. (Sahih Muslim 1955)"),
        "science": T(
            "Task switching costs up to 40% of productive time and raises error rates; single-tasking blocks restore sustained attention (Journal of Experimental Psychology 2001; APA).",
            "Berpindah-pindah tugas menghabiskan hingga 40% waktu produktif dan menaikkan tingkat kesalahan; blok satu-tugas memulihkan atensi berkelanjutan (Journal of Experimental Psychology 2001; APA)."),
    },
]
