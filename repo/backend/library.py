"""Lifestyle library: recipes, halal supplement guide, exercise routines and
time-specific mind windows. EN + ID. Every entry carries an Islamic grounding
and a clinical/journal note, plus tags for personal ranking.
"""
from templates_lifestyle import T


def L(*pairs: tuple[str, str]) -> dict:
    """List of bilingual lines -> {"en": [...], "id": [...]}."""
    return {"en": [p[0] for p in pairs], "id": [p[1] for p in pairs]}


RECIPES: list[dict] = [
    {
        "id": "r_talbina", "meal": "breakfast", "minutes": 10, "region": "sunnah",
        "kcal": 220, "protein_g": 8, "carbs_g": 34, "fat_g": 5, "fiber_g": 6,
        "tags": ["lipid_focus", "gut_focus", "weight_focus", "sunnah_diet", "healthy_eating"],
        "name": T("Talbina (Barley Porridge)", "Talbina (Bubur Jelai)"),
        "ingredients": L(
            ("2 tbsp barley flour (or 3 tbsp rolled barley)", "2 sdm tepung jelai/barley (atau 3 sdm barley pipih)"),
            ("250 ml low-fat milk or water", "250 ml susu rendah lemak atau air"),
            ("1 tsp honey", "1 sdt madu"),
            ("Pinch of cinnamon, 3 chopped dates (optional)", "Sejumput kayu manis, 3 kurma cincang (opsional)")),
        "steps": L(
            ("Whisk barley flour into cold milk so it does not clump.", "Aduk tepung jelai ke dalam susu dingin agar tidak menggumpal."),
            ("Simmer 5 minutes, stirring, until thick and smooth.", "Masak dengan api kecil 5 menit sambil diaduk hingga kental dan halus."),
            ("Cool slightly, then stir in honey and dates.", "Dinginkan sedikit, lalu tambahkan madu dan kurma.")),
        "islamic": T("The Prophet ﷺ recommended talbina for the sick and the grieving. (Sahih al-Bukhari 5689)",
                     "Nabi ﷺ menganjurkan talbina untuk orang sakit dan yang berduka. (Sahih Bukhari 5689)"),
        "science": T("Barley beta-glucan lowers LDL 5–10% and slows gastric emptying, keeping you full until midday (British Journal of Nutrition; EFSA claim).",
                     "Beta-glukan jelai menurunkan LDL 5–10% dan memperlambat pengosongan lambung sehingga kenyang sampai siang (British Journal of Nutrition; klaim EFSA)."),
    },
    {
        "id": "r_adas_soup", "meal": "dinner", "minutes": 30, "region": "sunnah",
        "kcal": 310, "protein_g": 18, "carbs_g": 42, "fat_g": 7, "fiber_g": 12,
        "tags": ["weight_focus", "lipid_focus", "glucose_focus", "plant_forward", "gut_focus"],
        "name": T("Shorbat Adas (Red Lentil Soup)", "Sup Lentil Merah (Shorbat Adas)"),
        "ingredients": L(
            ("200 g red lentils, rinsed", "200 g lentil merah, dicuci"),
            ("1 onion, 2 garlic cloves, 1 carrot, diced", "1 bawang bombai, 2 siung bawang putih, 1 wortel, potong dadu"),
            ("1 tsp cumin, ½ tsp turmeric, black pepper", "1 sdt jintan, ½ sdt kunyit, merica"),
            ("1 tbsp olive oil, 1 litre water, juice of 1 lemon", "1 sdm minyak zaitun, 1 liter air, air perasan 1 lemon")),
        "steps": L(
            ("Soften onion, garlic and carrot in olive oil 5 minutes.", "Tumis bawang bombai, bawang putih dan wortel dengan minyak zaitun 5 menit."),
            ("Add spices, lentils and water. Simmer 20 minutes.", "Masukkan rempah, lentil dan air. Masak 20 menit."),
            ("Blend roughly, finish with lemon. Serve with a drizzle of olive oil.", "Blender kasar, tambahkan lemon. Sajikan dengan sedikit minyak zaitun.")),
        "islamic": T("Lentils are among the foods of the Prophet's household; the Quran names lentils (adas) as a food the Israelites asked for. (Al-Baqarah 2:61)",
                     "Lentil (adas) disebut dalam Al-Quran sebagai makanan yang diminta Bani Israil. (QS Al-Baqarah 2:61)"),
        "science": T("A daily serving of pulses lowers LDL ~5% and improves glycaemic control; lentils have a GI of ~30 (Canadian Medical Association Journal 2014).",
                     "Seporsi kacang-kacangan polong per hari menurunkan LDL ~5% dan memperbaiki kontrol glikemik; IG lentil ~30 (Canadian Medical Association Journal 2014)."),
    },
    {
        "id": "r_sayur_bening", "meal": "lunch", "minutes": 20, "region": "indonesia",
        "kcal": 120, "protein_g": 5, "carbs_g": 18, "fat_g": 2, "fiber_g": 6,
        "tags": ["bp_focus", "weight_focus", "plant_forward", "low_sodium", "healthy_eating"],
        "name": T("Sayur Bening Bayam & Jagung", "Sayur Bening Bayam & Jagung"),
        "ingredients": L(
            ("2 bunches spinach, 1 sweet corn cut into rounds", "2 ikat bayam, 1 jagung manis potong bulat"),
            ("2 shallots sliced, 1 slice temu kunci (fingerroot) or ginger", "2 bawang merah iris, 1 ruas temu kunci atau jahe"),
            ("1 litre water, pinch of salt, 1 tsp palm sugar (optional)", "1 liter air, sejumput garam, 1 sdt gula aren (opsional)")),
        "steps": L(
            ("Boil water with shallots and temu kunci 5 minutes.", "Rebus air dengan bawang merah dan temu kunci 5 menit."),
            ("Add corn, cook 8 minutes. Add spinach for the last 2 minutes only.", "Masukkan jagung, masak 8 menit. Bayam masuk 2 menit terakhir saja."),
            ("Season lightly. Serve with grilled fish or tempe.", "Bumbui secukupnya. Sajikan dengan ikan bakar atau tempe.")),
        "islamic": T("\"He causes crops to grow for you, and olives, date palms, grapes and every kind of fruit.\" (An-Nahl 16:11)",
                     "\"Dia menumbuhkan untukmu tanaman, zaitun, kurma, anggur dan segala macam buah.\" (QS An-Nahl 16:11)"),
        "science": T("Leafy greens rich in nitrate and potassium lower blood pressure 3–5 mmHg; two servings a day slow cognitive ageing by ~11 years (Neurology 2018).",
                     "Sayuran hijau kaya nitrat dan kalium menurunkan tekanan darah 3–5 mmHg; dua porsi sehari memperlambat penuaan kognitif ~11 tahun (Neurology 2018)."),
    },
    {
        "id": "r_pepes_ikan", "meal": "dinner", "minutes": 40, "region": "indonesia",
        "kcal": 260, "protein_g": 30, "carbs_g": 6, "fat_g": 12, "fiber_g": 2,
        "tags": ["lipid_focus", "bp_focus", "build_strength", "high_protein", "glucose_focus"],
        "name": T("Pepes Ikan Kembung (Steamed Spiced Mackerel)", "Pepes Ikan Kembung"),
        "ingredients": L(
            ("2 whole mackerel (kembung), cleaned", "2 ekor ikan kembung, bersihkan"),
            ("Paste: 4 shallots, 3 garlic, 2 candlenuts, 1 cm turmeric, 1 cm ginger, 2 red chilies", "Bumbu halus: 4 bawang merah, 3 bawang putih, 2 kemiri, 1 cm kunyit, 1 cm jahe, 2 cabai merah"),
            ("Lemon basil, bay leaf, lemongrass, banana leaves, lime", "Kemangi, daun salam, serai, daun pisang, jeruk nipis")),
        "steps": L(
            ("Rub fish with lime and the spice paste.", "Lumuri ikan dengan jeruk nipis dan bumbu halus."),
            ("Wrap in banana leaf with basil, bay leaf and lemongrass.", "Bungkus dengan daun pisang bersama kemangi, daun salam dan serai."),
            ("Steam 25 minutes, then grill 5 minutes for aroma. No frying needed.", "Kukus 25 menit, lalu bakar 5 menit untuk aroma. Tanpa digoreng.")),
        "islamic": T("\"Lawful to you is game from the sea and its food.\" (Al-Ma'idah 5:96)",
                     "\"Dihalalkan bagimu hewan buruan laut dan makanan dari laut.\" (QS Al-Ma'idah 5:96)"),
        "science": T("Steaming preserves omega-3; kembung delivers ~1.5 g EPA+DHA per serving — more than salmon per rupiah. Turmeric adds anti-inflammatory curcumin (AHA 2018).",
                     "Mengukus menjaga omega-3; kembung menyediakan ~1,5 g EPA+DHA per porsi — lebih dari salmon per rupiah. Kunyit menambah kurkumin anti-inflamasi (AHA 2018)."),
    },
    {
        "id": "r_tempe_bacem", "meal": "lunch", "minutes": 35, "region": "indonesia",
        "kcal": 210, "protein_g": 17, "carbs_g": 14, "fat_g": 10, "fiber_g": 5,
        "tags": ["gut_focus", "plant_forward", "build_strength", "low_sugar", "weight_focus"],
        "name": T("Low-Sugar Tempe Bacem", "Tempe Bacem Rendah Gula"),
        "ingredients": L(
            ("300 g tempe, cut into thick slices", "300 g tempe, potong tebal"),
            ("2 shallots, 2 garlic, 1 tsp coriander, 1 bay leaf, 1 cm galangal", "2 bawang merah, 2 bawang putih, 1 sdt ketumbar, 1 lembar daun salam, 1 cm lengkuas"),
            ("1 tbsp palm sugar (instead of 4), 1 tbsp tamarind water, 300 ml water", "1 sdm gula aren (bukan 4), 1 sdm air asam jawa, 300 ml air")),
        "steps": L(
            ("Simmer tempe with all seasonings until the liquid is almost gone (25 min).", "Rebus tempe dengan semua bumbu sampai air hampir habis (25 menit)."),
            ("Grill or pan-sear briefly with 1 tsp oil instead of deep frying.", "Bakar atau panggang sebentar dengan 1 sdt minyak, bukan digoreng dalam minyak banyak.")),
        "islamic": T("\"Eat of the good things We have provided for you.\" (Al-Baqarah 2:172)",
                     "\"Makanlah dari rezeki yang baik yang telah Kami berikan kepadamu.\" (QS Al-Baqarah 2:172)"),
        "science": T("Tempe fermentation adds live cultures and vitamin B12 precursors; soy protein lowers LDL ~4% and tempe's fibre supports gut diversity (Journal of Nutrition 2019).",
                     "Fermentasi tempe menambah kultur hidup dan prekursor B12; protein kedelai menurunkan LDL ~4% dan serat tempe mendukung keragaman usus (Journal of Nutrition 2019)."),
    },
    {
        "id": "r_date_oat_bites", "meal": "snack", "minutes": 15, "region": "sunnah",
        "kcal": 95, "protein_g": 2, "carbs_g": 14, "fat_g": 4, "fiber_g": 2,
        "tags": ["more_energy", "low_sugar", "sunnah_diet", "build_strength"],
        "name": T("Date & Walnut Energy Bites", "Bola Energi Kurma & Kenari"),
        "ingredients": L(
            ("10 medjool dates, pitted", "10 kurma medjool, buang biji"),
            ("60 g walnuts, 60 g rolled oats", "60 g kenari, 60 g oat pipih"),
            ("1 tbsp black seed, 1 tbsp sesame, pinch of sea salt", "1 sdm habbatussauda, 1 sdm wijen, sejumput garam laut")),
        "steps": L(
            ("Blend everything into a sticky dough.", "Blender semua bahan hingga menjadi adonan lengket."),
            ("Roll into 12 balls, chill 30 minutes. One before a walk or workout.", "Bulatkan 12 bola, dinginkan 30 menit. Satu butir sebelum jalan atau olahraga.")),
        "islamic": T("\"When one of you breaks his fast, let him break it with dates.\" (Sunan Abi Dawud 2355)",
                     "\"Jika salah seorang kalian berbuka, berbukalah dengan kurma.\" (Sunan Abu Dawud 2355)"),
        "science": T("Dates plus walnuts give a moderate-GI carbohydrate with polyphenols and omega-3 ALA — an evidence-based pre-exercise snack (Nutrition Journal 2011; Nutrients 2020).",
                     "Kurma dengan kenari memberi karbohidrat IG sedang dengan polifenol dan omega-3 ALA — camilan pra-olahraga berbasis bukti (Nutrition Journal 2011; Nutrients 2020)."),
    },
    {
        "id": "r_zaatar_salad", "meal": "lunch", "minutes": 10, "region": "sunnah",
        "kcal": 180, "protein_g": 4, "carbs_g": 12, "fat_g": 14, "fiber_g": 4,
        "tags": ["lipid_focus", "bp_focus", "weight_focus", "plant_forward", "sunnah_diet"],
        "name": T("Olive-Oil Za'atar Salad", "Salad Zaitun Za'atar"),
        "ingredients": L(
            ("2 tomatoes, 1 cucumber, ½ red onion, parsley", "2 tomat, 1 timun, ½ bawang bombai merah, peterseli"),
            ("2 tbsp extra-virgin olive oil, juice of ½ lemon", "2 sdm minyak zaitun extra virgin, air ½ lemon"),
            ("1 tbsp za'atar, 6 olives", "1 sdm za'atar, 6 buah zaitun")),
        "steps": L(
            ("Dice vegetables, toss with oil, lemon and za'atar.", "Potong dadu sayuran, aduk dengan minyak, lemon dan za'atar."),
            ("Eat before your main dish — vegetables first.", "Makan sebelum hidangan utama — sayur dulu.")),
        "islamic": T("\"...lit from a blessed tree, an olive, whose oil almost glows though untouched by fire.\" (An-Nur 24:35)",
                     "\"...dari pohon yang diberkahi, zaitun, yang minyaknya hampir menerangi walau tak disentuh api.\" (QS An-Nur 24:35)"),
        "science": T("Extra-virgin olive oil at ~4 tbsp/day cut major cardiovascular events ~30% in the PREDIMED trial (New England Journal of Medicine 2018).",
                     "Minyak zaitun extra virgin ~4 sdm/hari menurunkan kejadian kardiovaskular mayor ~30% dalam uji PREDIMED (New England Journal of Medicine 2018)."),
    },
    {
        "id": "r_ginger_lemon_honey", "meal": "drink", "minutes": 8, "region": "universal",
        "kcal": 30, "protein_g": 0, "carbs_g": 8, "fat_g": 0, "fiber_g": 0,
        "tags": ["gut_focus", "glucose_focus", "calm_focus", "low_sugar"],
        "name": T("Warm Ginger, Lemon & Honey", "Wedang Jahe Lemon Madu"),
        "ingredients": L(
            ("3 cm fresh ginger, sliced thin", "3 cm jahe segar, iris tipis"),
            ("300 ml hot water, juice of ½ lemon", "300 ml air panas, air ½ lemon"),
            ("1 tsp raw honey (add when warm, not boiling)", "1 sdt madu murni (tambahkan saat hangat, bukan mendidih)")),
        "steps": L(
            ("Steep ginger in hot water 5 minutes.", "Seduh jahe dalam air panas 5 menit."),
            ("Add lemon, then honey once drinkable-warm.", "Tambahkan lemon, lalu madu saat sudah hangat untuk diminum.")),
        "islamic": T("\"From their bellies comes a drink of varying colours in which there is healing for people.\" (An-Nahl 16:69)",
                     "\"Dari perutnya keluar minuman beraneka warna, di dalamnya terdapat obat bagi manusia.\" (QS An-Nahl 16:69)"),
        "science": T("Ginger (1–2 g) reduces nausea and fasting glucose; honey outperformed dextromethorphan for children's cough in Cochrane reviews. Heat above 40 °C degrades honey enzymes.",
                     "Jahe (1–2 g) mengurangi mual dan glukosa puasa; madu mengalahkan dekstrometorfan untuk batuk anak dalam tinjauan Cochrane. Panas di atas 40 °C merusak enzim madu."),
    },
    {
        "id": "r_oat_dates_bowl", "meal": "breakfast", "minutes": 8, "region": "universal",
        "kcal": 320, "protein_g": 14, "carbs_g": 45, "fat_g": 9, "fiber_g": 8,
        "tags": ["glucose_focus", "weight_focus", "more_energy", "healthy_eating"],
        "name": T("Overnight Oats, Dates & Chia", "Oat Rendam Semalam, Kurma & Chia"),
        "ingredients": L(
            ("50 g rolled oats, 1 tbsp chia seeds", "50 g oat pipih, 1 sdm biji chia"),
            ("150 ml milk or kefir, 100 g plain yoghurt", "150 ml susu atau kefir, 100 g yoghurt tawar"),
            ("2 dates chopped, cinnamon, 5 almonds", "2 kurma cincang, kayu manis, 5 almond")),
        "steps": L(
            ("Mix everything in a jar the night before. Refrigerate.", "Campur semua dalam wadah malam sebelumnya. Simpan di kulkas."),
            ("Eat after Fajr. No cooking, no decisions.", "Makan setelah Subuh. Tanpa memasak, tanpa memutuskan apa pun.")),
        "islamic": T("\"O Allah, bless my Ummah in their early mornings.\" (Sunan Abi Dawud 2606)",
                     "\"Ya Allah, berkahilah umatku pada waktu pagi mereka.\" (Sunan Abu Dawud 2606)"),
        "science": T("Oat beta-glucan and chia's soluble fibre flatten the breakfast glucose curve and extend satiety ~3 hours; regular breakfast eaters have lower BMI (American Journal of Clinical Nutrition).",
                     "Beta-glukan oat dan serat larut chia meratakan kurva glukosa sarapan dan memperpanjang kenyang ~3 jam; sarapan rutin dikaitkan BMI lebih rendah (American Journal of Clinical Nutrition)."),
    },
    {
        "id": "r_gado_gado_light", "meal": "lunch", "minutes": 25, "region": "indonesia",
        "kcal": 380, "protein_g": 20, "carbs_g": 36, "fat_g": 16, "fiber_g": 10,
        "tags": ["plant_forward", "build_strength", "gut_focus", "healthy_eating"],
        "name": T("Light Gado-Gado (Half Peanut, Half Tempe)", "Gado-Gado Ringan (Setengah Kacang, Setengah Tempe)"),
        "ingredients": L(
            ("Steamed: long beans, cabbage, bean sprouts, potato, spinach", "Kukus: kacang panjang, kol, tauge, kentang, bayam"),
            ("2 boiled eggs, 100 g steamed tempe, cucumber", "2 telur rebus, 100 g tempe kukus, timun"),
            ("Sauce: 3 tbsp roasted peanuts, 1 garlic, 1 chili, 1 tsp palm sugar, tamarind, water", "Saus: 3 sdm kacang sangrai, 1 bawang putih, 1 cabai, 1 sdt gula aren, asam jawa, air")),
        "steps": L(
            ("Blend sauce ingredients with water to a pourable consistency — half the usual peanuts.", "Blender bahan saus dengan air hingga encer — setengah takaran kacang biasa."),
            ("Plate vegetables first, then protein, then sauce. Skip the fried crackers.", "Tata sayur dulu, lalu protein, lalu saus. Lewati kerupuk goreng.")),
        "islamic": T("\"Say Bismillah, eat with your right hand, and eat from what is nearest to you.\" (Sahih al-Bukhari 5376)",
                     "\"Sebutlah nama Allah, makan dengan tangan kanan, dan makanlah dari yang terdekat.\" (Sahih Bukhari 5376)"),
        "science": T("Mixed vegetables with legume protein deliver the 25–30 g protein and 10 g fibre per meal that best control appetite (Journal of the Academy of Nutrition and Dietetics).",
                     "Sayuran campur dengan protein kacang-kacangan memberi 25–30 g protein dan 10 g serat per makan yang paling baik mengendalikan nafsu makan (Journal of the Academy of Nutrition and Dietetics)."),
    },
    {
        "id": "r_black_seed_honey_mix", "meal": "snack", "minutes": 3, "region": "sunnah",
        "kcal": 45, "protein_g": 1, "carbs_g": 7, "fat_g": 2, "fiber_g": 1,
        "tags": ["glucose_focus", "lipid_focus", "bp_focus", "sunnah_diet"],
        "name": T("Black Seed & Honey Spoon", "Habbatussauda & Madu"),
        "ingredients": L(
            ("½ tsp ground black seed (Nigella sativa)", "½ sdt habbatussauda bubuk (Nigella sativa)"),
            ("1 tsp raw honey", "1 sdt madu murni")),
        "steps": L(
            ("Mix and take after breakfast, daily. Consistency matters more than dose.", "Campur dan konsumsi setelah sarapan, setiap hari. Konsistensi lebih penting daripada dosis.")),
        "islamic": T("\"In the black seed there is a cure for every disease except death.\" (Sahih al-Bukhari 5688)",
                     "\"Pada habbatussauda ada obat bagi setiap penyakit kecuali kematian.\" (Sahih Bukhari 5688)"),
        "science": T("A 2025 GRADE meta-analysis of 82 RCTs (5,026 people) found Nigella sativa modestly lowers blood pressure, fasting glucose, HbA1c, LDL and waist circumference (Complementary Therapies in Medicine 2025).",
                     "Meta-analisis GRADE 2025 atas 82 uji acak (5.026 orang) menemukan Nigella sativa menurunkan secara moderat tekanan darah, glukosa puasa, HbA1c, LDL dan lingkar pinggang (Complementary Therapies in Medicine 2025)."),
    },
    {
        "id": "r_soto_ayam_bening", "meal": "dinner", "minutes": 45, "region": "indonesia",
        "kcal": 290, "protein_g": 28, "carbs_g": 22, "fat_g": 8, "fiber_g": 3,
        "tags": ["build_strength", "bp_focus", "low_sodium", "weight_focus"],
        "name": T("Clear Soto Ayam (No Coconut Milk)", "Soto Ayam Bening (Tanpa Santan)"),
        "ingredients": L(
            ("300 g skinless chicken breast, 1.5 l water", "300 g dada ayam tanpa kulit, 1,5 l air"),
            ("Paste: 3 shallots, 3 garlic, 2 cm turmeric, 2 cm ginger, 2 candlenuts", "Bumbu halus: 3 bawang merah, 3 bawang putih, 2 cm kunyit, 2 cm jahe, 2 kemiri"),
            ("Lemongrass, bay leaf, lime leaf; bean sprouts, celery, lime, boiled egg", "Serai, daun salam, daun jeruk; tauge, seledri, jeruk nipis, telur rebus")),
        "steps": L(
            ("Poach chicken 20 minutes, shred. Keep the broth.", "Rebus ayam 20 menit, suwir. Simpan kaldunya."),
            ("Sauté paste with aromatics, add to broth, simmer 15 minutes. Salt lightly, lime generously.", "Tumis bumbu dengan rempah daun, masukkan ke kaldu, masak 15 menit. Garam sedikit, jeruk nipis banyak."),
            ("Serve over bean sprouts and half the usual rice.", "Sajikan di atas tauge dengan setengah porsi nasi biasa.")),
        "islamic": T("\"When one of you eats, let him mention the name of Allah.\" (Jami' at-Tirmidhi 1858)",
                     "\"Jika salah seorang kalian makan, sebutlah nama Allah.\" (Tirmidzi 1858)"),
        "science": T("Replacing coconut-milk broth with a clear one saves ~200 kcal and 15 g saturated fat per bowl; lean poultry protein supports muscle retention during weight loss (AJCN 2015).",
                     "Mengganti kuah santan dengan kuah bening menghemat ~200 kkal dan 15 g lemak jenuh per mangkuk; protein unggas tanpa lemak menjaga otot saat menurunkan berat badan (AJCN 2015)."),
    },
    {
        "id": "r_fig_walnut_yoghurt", "meal": "snack", "minutes": 4, "region": "sunnah",
        "kcal": 190, "protein_g": 11, "carbs_g": 22, "fat_g": 7, "fiber_g": 4,
        "tags": ["gut_focus", "build_strength", "sunnah_diet", "sleep_focus"],
        "name": T("Fig, Walnut & Yoghurt Bowl", "Mangkuk Tin, Kenari & Yoghurt"),
        "ingredients": L(
            ("150 g plain Greek yoghurt", "150 g yoghurt Yunani tawar"),
            ("2 fresh or dried figs, sliced", "2 buah tin segar atau kering, iris"),
            ("6 walnut halves, cinnamon", "6 belahan kenari, kayu manis")),
        "steps": L(
            ("Layer and eat slowly as an evening snack, two hours before sleep.", "Susun dan makan perlahan sebagai camilan malam, dua jam sebelum tidur.")),
        "islamic": T("\"By the fig and the olive.\" (At-Tin 95:1)", "\"Demi buah tin dan zaitun.\" (QS At-Tin 95:1)"),
        "science": T("Figs supply prebiotic fibre and potassium; walnuts are the richest nut source of ALA and improved sleep-related melatonin in trials (Nutrition 2005; Nutrients 2019).",
                     "Buah tin menyediakan serat prebiotik dan kalium; kenari adalah kacang terkaya ALA dan meningkatkan melatonin terkait tidur dalam uji klinis (Nutrition 2005; Nutrients 2019)."),
    },
    {
        "id": "r_kunyit_asam", "meal": "drink", "minutes": 10, "region": "indonesia",
        "kcal": 35, "protein_g": 0, "carbs_g": 9, "fat_g": 0, "fiber_g": 0,
        "tags": ["gut_focus", "calm_focus", "female", "low_sugar"],
        "name": T("Kunyit Asam (Turmeric-Tamarind Tonic)", "Kunyit Asam Rendah Gula"),
        "ingredients": L(
            ("3 cm fresh turmeric, grated", "3 cm kunyit segar, parut"),
            ("1 tbsp tamarind pulp, 500 ml water", "1 sdm asam jawa, 500 ml air"),
            ("1 tsp palm sugar or honey, pinch of black pepper", "1 sdt gula aren atau madu, sejumput merica")),
        "steps": L(
            ("Simmer turmeric and tamarind 8 minutes. Strain.", "Rebus kunyit dan asam jawa 8 menit. Saring."),
            ("Add pepper (boosts curcumin absorption) and a little sweetener. Drink warm or chilled.", "Tambahkan merica (meningkatkan penyerapan kurkumin) dan sedikit pemanis. Minum hangat atau dingin.")),
        "islamic": T("\"And He it is Who has made the earth manageable for you, so traverse its paths and eat of His provision.\" (Al-Mulk 67:15)",
                     "\"Dialah yang menjadikan bumi mudah bagimu, maka berjalanlah di penjurunya dan makanlah dari rezeki-Nya.\" (QS Al-Mulk 67:15)"),
        "science": T("Curcumin with piperine reduces menstrual pain and inflammatory markers comparably to NSAIDs in small RCTs; keep sugar minimal (Journal of Pain Research 2019).",
                     "Kurkumin dengan piperin mengurangi nyeri haid dan penanda inflamasi sebanding NSAID pada uji acak kecil; gula tetap minimal (Journal of Pain Research 2019)."),
    },
]

SUPPLEMENTS: list[dict] = [
    {
        "id": "sp_vitd", "evidence_level": "strong",
        "tags": ["female", "desk_worker", "bp_focus", "sleep_focus", "joint_friendly"],
        "name": T("Vitamin D3", "Vitamin D3"),
        "dose": T("1,000–2,000 IU daily with a meal containing fat; higher only under a doctor after a 25-OH-D test.",
                  "1.000–2.000 IU per hari bersama makanan berlemak; dosis lebih tinggi hanya atas anjuran dokter setelah tes 25-OH-D."),
        "who": T("Indoor workers, women who cover fully, older adults, anyone with low test results.",
                 "Pekerja dalam ruangan, muslimah berpakaian tertutup, lansia, siapa pun dengan hasil tes rendah."),
        "evidence": T("Deficiency (<20 ng/ml) affects over half of adults in Indonesia and the Gulf; correction improves bone density, muscle strength and lowers respiratory infections (Endocrine Society; BMJ 2017 meta-analysis).",
                      "Kekurangan (<20 ng/ml) dialami lebih dari separuh orang dewasa di Indonesia dan Teluk; koreksi memperbaiki kepadatan tulang, kekuatan otot dan menurunkan infeksi pernapasan (Endocrine Society; meta-analisis BMJ 2017)."),
        "halal": T("Most D3 is from sheep-wool lanolin — accepted as halal by the majority of scholars. Lichen-derived D3 avoids any doubt. Check the capsule: gelatin must be halal-certified or plant (HPMC).",
                   "Sebagian besar D3 berasal dari lanolin bulu domba — dinilai halal oleh mayoritas ulama. D3 dari lichen bebas keraguan. Periksa kapsul: gelatin harus bersertifikat halal atau nabati (HPMC)."),
        "caution": T("Do not exceed 4,000 IU/day without supervision. Interacts with some heart medicines.",
                     "Jangan melebihi 4.000 IU/hari tanpa pengawasan. Berinteraksi dengan beberapa obat jantung."),
    },
    {
        "id": "sp_omega3", "evidence_level": "strong",
        "tags": ["lipid_focus", "bp_focus", "mental_clarity", "joint_friendly"],
        "name": T("Omega-3 (EPA + DHA)", "Omega-3 (EPA + DHA)"),
        "dose": T("1 g EPA+DHA daily if you eat fish less than twice a week.",
                  "1 g EPA+DHA per hari jika makan ikan kurang dari dua kali seminggu."),
        "who": T("High triglycerides, joint stiffness, low fish intake, mood support.",
                 "Trigliserida tinggi, sendi kaku, jarang makan ikan, dukungan suasana hati."),
        "evidence": T("Lowers triglycerides 15–30% and blood pressure modestly; 4 g/day icosapent ethyl cut cardiovascular events 25% in REDUCE-IT (NEJM 2019).",
                      "Menurunkan trigliserida 15–30% dan tekanan darah secara moderat; 4 g/hari ikosapent etil menurunkan kejadian kardiovaskular 25% dalam REDUCE-IT (NEJM 2019)."),
        "halal": T("Fish oil itself is halal — the problem is the softgel: most use porcine gelatin. Choose liquid oil, algal omega-3 in vegetable capsules, or fish/bovine gelatin with MUI, JAKIM or IFANCA certification.",
                   "Minyak ikan sendiri halal — masalahnya pada kapsul: kebanyakan memakai gelatin babi. Pilih minyak cair, omega-3 alga dalam kapsul nabati, atau gelatin ikan/sapi bersertifikat MUI, JAKIM, atau IFANCA."),
        "caution": T("Stop 1 week before surgery; ask your doctor if on blood thinners.",
                     "Hentikan 1 minggu sebelum operasi; konsultasikan jika memakai pengencer darah."),
    },
    {
        "id": "sp_magnesium", "evidence_level": "moderate",
        "tags": ["sleep_focus", "insomnia", "calm_focus", "bp_focus", "glucose_focus"],
        "name": T("Magnesium (glycinate or citrate)", "Magnesium (glisinat atau sitrat)"),
        "dose": T("200–400 mg elemental magnesium in the evening.", "200–400 mg magnesium elemental di malam hari."),
        "who": T("Poor sleep, muscle cramps, stress, high blood pressure, prediabetes.",
                 "Tidur buruk, kram otot, stres, tekanan darah tinggi, pradiabetes."),
        "evidence": T("Improves insomnia severity and sleep onset; lowers systolic BP ~2 mmHg and fasting glucose in deficient people (Journal of Research in Medical Sciences 2012; Hypertension 2016).",
                      "Memperbaiki keparahan insomnia dan waktu mulai tidur; menurunkan tekanan sistolik ~2 mmHg dan glukosa puasa pada orang yang kekurangan (Journal of Research in Medical Sciences 2012; Hypertension 2016)."),
        "halal": T("Mineral salt — halal by nature. Avoid softgels with unknown gelatin; tablets and vegetable capsules are safe.",
                   "Garam mineral — halal secara alami. Hindari softgel dengan gelatin tidak jelas; tablet dan kapsul nabati aman."),
        "caution": T("Citrate can loosen stools. Avoid high doses with kidney disease.",
                     "Sitrat bisa melunakkan tinja. Hindari dosis tinggi pada penyakit ginjal."),
    },
    {
        "id": "sp_black_seed_oil", "evidence_level": "moderate",
        "tags": ["glucose_focus", "lipid_focus", "bp_focus", "weight_focus", "sunnah_diet"],
        "name": T("Black Seed Oil (Nigella sativa)", "Minyak Habbatussauda (Nigella sativa)"),
        "dose": T("1–2 g of seed or 1 tsp (5 ml) of cold-pressed oil daily, for at least 8 weeks.",
                  "1–2 g biji atau 1 sdt (5 ml) minyak cold-pressed per hari, minimal 8 minggu."),
        "who": T("Metabolic syndrome, prediabetes, mild hypertension, high cholesterol.",
                 "Sindrom metabolik, pradiabetes, hipertensi ringan, kolesterol tinggi."),
        "evidence": T("82-trial meta-analysis (2025): modest but consistent reductions in SBP, fasting glucose (−21 mg/dl in T2D), HbA1c (−0.44), LDL and waist circumference. Adjunct, not replacement.",
                      "Meta-analisis 82 uji (2025): penurunan moderat namun konsisten pada tekanan sistolik, glukosa puasa (−21 mg/dl pada DM2), HbA1c (−0,44), LDL dan lingkar pinggang. Pelengkap, bukan pengganti obat."),
        "halal": T("Plant seed — halal. Prefer pure cold-pressed oil without carrier oils; capsules should be HPMC.",
                   "Biji tanaman — halal. Pilih minyak murni cold-pressed tanpa minyak pembawa; kapsul sebaiknya HPMC."),
        "caution": T("May enhance blood-sugar and BP medication effects — monitor with your doctor.",
                     "Dapat memperkuat efek obat gula darah dan tekanan darah — pantau bersama dokter."),
    },
    {
        "id": "sp_creatine", "evidence_level": "strong",
        "tags": ["build_strength", "more_energy", "mental_clarity", "balance_focus"],
        "name": T("Creatine Monohydrate", "Kreatin Monohidrat"),
        "dose": T("3–5 g daily, any time, with water. No loading phase needed.", "3–5 g per hari, kapan saja, dengan air. Tidak perlu fase loading."),
        "who": T("Strength training, adults over 50 preserving muscle, plant-forward eaters, cognitive support.",
                 "Latihan kekuatan, dewasa 50+ menjaga otot, pola makan nabati, dukungan kognitif."),
        "evidence": T("The most studied sports supplement: +8% strength and +1 kg lean mass over 8–12 weeks; improves memory in older adults and vegetarians (ISSN Position Stand 2017; Nutrition Reviews 2023).",
                      "Suplemen olahraga paling banyak diteliti: +8% kekuatan dan +1 kg massa otot dalam 8–12 minggu; memperbaiki memori pada lansia dan vegetarian (ISSN 2017; Nutrition Reviews 2023)."),
        "halal": T("Synthesised chemically from sarcosine and cyanamide — no animal source, so halal. Buy unflavoured powder to avoid doubtful additives.",
                   "Disintesis secara kimia dari sarkosin dan sianamida — tanpa sumber hewani, sehingga halal. Beli bubuk tanpa rasa untuk menghindari bahan tambahan yang meragukan."),
        "caution": T("Drink extra water. Safe for healthy kidneys; check with a doctor if you have kidney disease.",
                     "Minum lebih banyak air. Aman untuk ginjal sehat; konsultasikan jika ada penyakit ginjal."),
    },
    {
        "id": "sp_probiotic", "evidence_level": "moderate",
        "tags": ["gut_focus", "digestive", "calm_focus"],
        "name": T("Probiotics (multi-strain)", "Probiotik (multi-strain)"),
        "dose": T("10–20 billion CFU daily for 4–8 weeks, or daily fermented food instead.",
                  "10–20 miliar CFU per hari selama 4–8 minggu, atau makanan fermentasi harian sebagai gantinya."),
        "who": T("IBS, bloating, after antibiotics, frequent colds.",
                 "IBS, perut kembung, setelah antibiotik, sering flu."),
        "evidence": T("Multi-strain probiotics reduce IBS symptom severity and antibiotic-associated diarrhoea by ~40%; the gut-brain axis links them to lower anxiety scores (Cochrane; Gastroenterology 2018).",
                      "Probiotik multi-strain menurunkan keparahan gejala IBS dan diare akibat antibiotik ~40%; poros usus-otak mengaitkannya dengan skor kecemasan lebih rendah (Cochrane; Gastroenterology 2018)."),
        "halal": T("Check the growth medium and capsule: some strains are cultured on pork-derived media or packed in porcine gelatin. Halal-certified brands or tempe, yoghurt and kefir are the safe path.",
                   "Periksa media kultur dan kapsul: beberapa strain dikultur pada media turunan babi atau dikemas dalam gelatin babi. Merek bersertifikat halal atau tempe, yoghurt dan kefir adalah jalur aman."),
        "caution": T("Avoid if severely immunocompromised without medical advice.",
                     "Hindari jika imunitas sangat lemah tanpa nasihat medis."),
    },
    {
        "id": "sp_zinc", "evidence_level": "moderate",
        "tags": ["plant_forward", "more_energy", "gut_focus"],
        "name": T("Zinc", "Zink (Seng)"),
        "dose": T("10–15 mg daily with food, short courses; 30 mg only during illness.",
                  "10–15 mg per hari bersama makanan, jangka pendek; 30 mg hanya saat sakit."),
        "who": T("Plant-forward eaters, frequent infections, slow wound healing.",
                 "Pola makan nabati, sering infeksi, luka lambat sembuh."),
        "evidence": T("Zinc within 24 hours of cold onset shortens illness by ~2 days; deficiency is common where diets are grain-heavy (Cochrane 2013; American Journal of Clinical Nutrition).",
                      "Zink dalam 24 jam sejak gejala flu memperpendek sakit ~2 hari; kekurangan umum pada pola makan tinggi biji-bijian (Cochrane 2013; American Journal of Clinical Nutrition)."),
        "halal": T("Mineral — halal. Avoid gelatin capsules of unknown origin.",
                   "Mineral — halal. Hindari kapsul gelatin yang tidak jelas asalnya."),
        "caution": T("Long-term high doses deplete copper. Take apart from iron and antibiotics.",
                     "Dosis tinggi jangka panjang mengurangi tembaga. Pisahkan dari zat besi dan antibiotik."),
    },
    {
        "id": "sp_iron", "evidence_level": "strong",
        "tags": ["female", "more_energy", "plant_forward"],
        "name": T("Iron (only if deficient)", "Zat Besi (hanya jika kekurangan)"),
        "dose": T("Test ferritin first. If low: 60 mg elemental iron every other day with vitamin C.",
                  "Tes feritin dulu. Jika rendah: 60 mg besi elemental setiap dua hari bersama vitamin C."),
        "who": T("Menstruating women, pregnancy, plant-forward eaters, unexplained fatigue.",
                 "Wanita usia haid, kehamilan, pola makan nabati, kelelahan tak jelas."),
        "evidence": T("Iron deficiency is the world's most common nutritional disorder, affecting ~30% of women of reproductive age; alternate-day dosing absorbs better with fewer side effects (Lancet Haematology 2017).",
                      "Kekurangan zat besi adalah gangguan gizi paling umum di dunia, dialami ~30% wanita usia reproduktif; dosis selang sehari terserap lebih baik dengan efek samping lebih sedikit (Lancet Haematology 2017)."),
        "halal": T("Mineral salts (ferrous sulfate, bisglycinate) are halal. Check coatings and capsules.",
                   "Garam mineral (fero sulfat, bisglisinat) halal. Periksa lapisan dan kapsul."),
        "caution": T("Never supplement iron without a blood test — excess is harmful. Keep away from children.",
                     "Jangan suplemen zat besi tanpa tes darah — kelebihan berbahaya. Jauhkan dari anak-anak."),
    },
    {
        "id": "sp_b12", "evidence_level": "strong",
        "tags": ["plant_forward", "mental_clarity", "more_energy"],
        "name": T("Vitamin B12", "Vitamin B12"),
        "dose": T("250 µg daily or 1,000 µg twice weekly if you eat little meat, fish or dairy.",
                  "250 µg per hari atau 1.000 µg dua kali seminggu jika jarang makan daging, ikan atau susu."),
        "who": T("Plant-forward eaters, adults over 60, people on metformin or acid blockers.",
                 "Pola makan nabati, dewasa 60+, pengguna metformin atau penghambat asam lambung."),
        "evidence": T("B12 deficiency causes fatigue, numbness and memory problems; metformin lowers B12 in ~20% of users (Journal of Clinical Endocrinology & Metabolism 2016).",
                      "Kekurangan B12 menyebabkan lelah, kebas dan gangguan memori; metformin menurunkan B12 pada ~20% pengguna (Journal of Clinical Endocrinology & Metabolism 2016)."),
        "halal": T("Produced by bacterial fermentation — halal. Prefer tablets or sprays.",
                   "Diproduksi melalui fermentasi bakteri — halal. Pilih tablet atau semprot."),
        "caution": T("Very safe; no upper limit established.", "Sangat aman; tidak ada batas atas yang ditetapkan."),
    },
    {
        "id": "sp_whey", "evidence_level": "strong",
        "tags": ["build_strength", "gain_focus", "weight_focus"],
        "name": T("Whey or Plant Protein Powder", "Bubuk Protein Whey atau Nabati"),
        "dose": T("20–30 g after training or at a low-protein meal, only to reach your daily target.",
                  "20–30 g setelah latihan atau saat makan rendah protein, hanya untuk mencapai target harian."),
        "who": T("Anyone who cannot reach their protein target from food alone.",
                 "Siapa pun yang tidak bisa mencapai target protein dari makanan saja."),
        "evidence": T("Protein supplementation adds ~27% to strength gains from resistance training; total daily intake of 1.6 g/kg is the ceiling of benefit (British Journal of Sports Medicine 2018).",
                      "Suplemen protein menambah ~27% peningkatan kekuatan dari latihan beban; total 1,6 g/kg per hari adalah batas manfaat (British Journal of Sports Medicine 2018)."),
        "halal": T("Whey comes from cheese-making: the rennet may be porcine or microbial. Choose MUI/JAKIM/IFANCA-certified whey, or pea/soy blends. Avoid 'natural flavours' with alcohol carriers.",
                   "Whey berasal dari pembuatan keju: rennet bisa dari babi atau mikroba. Pilih whey bersertifikat MUI/JAKIM/IFANCA, atau campuran kacang polong/kedelai. Hindari 'perisa alami' dengan pelarut alkohol."),
        "caution": T("Food first. Not needed if you already eat enough protein.",
                     "Makanan utama dulu. Tidak perlu jika protein dari makanan sudah cukup."),
    },
]

EXERCISES: list[dict] = [
    {
        "id": "ex_walk_progression", "focus": "cardio", "level": 1, "minutes": 20, "joint_friendly": True,
        "tags": ["weight_focus", "bp_focus", "glucose_focus", "joint_friendly"],
        "name": T("4-Week Walking Progression", "Progresi Jalan Kaki 4 Minggu"),
        "equipment": T("Shoes only", "Hanya sepatu"),
        "steps": L(
            ("Week 1: 15 min easy, daily.", "Minggu 1: 15 menit santai, setiap hari."),
            ("Week 2: 20 min, last 5 brisk.", "Minggu 2: 20 menit, 5 menit terakhir cepat."),
            ("Week 3: 25 min, alternate 3 easy / 2 brisk.", "Minggu 3: 25 menit, bergantian 3 santai / 2 cepat."),
            ("Week 4: 30 min brisk, or 7,000+ steps a day.", "Minggu 4: 30 menit cepat, atau 7.000+ langkah sehari.")),
        "islamic": T("Walking to the masjid earns a reward for every step. (Sahih Muslim 654)", "Setiap langkah menuju masjid dicatat sebagai kebaikan. (Sahih Muslim 654)"),
        "science": T("Brisk walking 150 min/week lowers all-cause mortality ~30% and is the most sustainable exercise for beginners (WHO 2020; JAMA Network Open 2021).",
                     "Jalan cepat 150 menit/minggu menurunkan mortalitas ~30% dan menjadi olahraga paling lestari bagi pemula (WHO 2020; JAMA Network Open 2021)."),
    },
    {
        "id": "ex_home_strength", "focus": "strength", "level": 1, "minutes": 15, "joint_friendly": True,
        "tags": ["build_strength", "weight_focus", "female", "joint_friendly"],
        "name": T("Home Strength Basics (no equipment)", "Dasar Kekuatan di Rumah (tanpa alat)"),
        "equipment": T("Chair, wall", "Kursi, tembok"),
        "steps": L(
            ("Sit-to-stand 3×10", "Duduk-berdiri 3×10"),
            ("Incline push-up (wall → table) 3×8–12", "Push-up miring (tembok → meja) 3×8–12"),
            ("Glute bridge 3×12", "Glute bridge 3×12"),
            ("Wall sit 3×30 s; rest 45 s between sets", "Duduk di tembok 3×30 detik; istirahat 45 detik antar set")),
        "islamic": T("The strong believer is better and more beloved to Allah. (Sahih Muslim 2664)", "Mukmin yang kuat lebih baik dan lebih dicintai Allah. (Sahih Muslim 2664)"),
        "science": T("Two short strength sessions a week (30–60 min total) associate with ~20% lower all-cause mortality (British Journal of Sports Medicine 2022).",
                     "Dua sesi kekuatan singkat per minggu (total 30–60 menit) dikaitkan mortalitas ~20% lebih rendah (British Journal of Sports Medicine 2022)."),
    },
    {
        "id": "ex_band_full", "focus": "strength", "level": 2, "minutes": 20, "joint_friendly": True,
        "tags": ["build_strength", "female", "joint_friendly", "desk_worker"],
        "name": T("Resistance Band Full Body", "Resistance Band Seluruh Tubuh"),
        "equipment": T("One loop or tube band", "Satu band loop atau tube"),
        "steps": L(
            ("Band squat 3×12", "Squat band 3×12"),
            ("Standing row 3×12", "Row berdiri 3×12"),
            ("Overhead press 3×10", "Overhead press 3×10"),
            ("Lateral walk 3×10 each side", "Jalan menyamping 3×10 tiap sisi"),
            ("Pallof press 3×10 each side", "Pallof press 3×10 tiap sisi")),
        "islamic": T("Take advantage of your health before your sickness. (al-Hakim)", "Manfaatkan sehatmu sebelum sakitmu. (al-Hakim)"),
        "science": T("Band training matches free-weight strength gains in beginners with lower joint load (SAGE Open Medicine 2019).",
                     "Latihan band menyamai peningkatan kekuatan beban bebas pada pemula dengan beban sendi lebih rendah (SAGE Open Medicine 2019)."),
    },
    {
        "id": "ex_desk_mobility", "focus": "mobility", "level": 1, "minutes": 5, "joint_friendly": True,
        "tags": ["desk_worker", "joint_friendly", "bp_focus"],
        "name": T("Desk Mobility Reset", "Reset Mobilitas Meja Kerja"),
        "equipment": T("None", "Tidak ada"),
        "steps": L(
            ("Neck: 5 slow circles each way", "Leher: 5 putaran perlahan tiap arah"),
            ("Shoulders: 10 rolls back", "Bahu: 10 putaran ke belakang"),
            ("Thoracic twist seated: 8 each side", "Putar dada sambil duduk: 8 tiap sisi"),
            ("Hip flexor stretch standing: 30 s each", "Peregangan hip flexor berdiri: 30 detik tiap sisi"),
            ("Calf raises: 20", "Angkat tumit: 20 kali")),
        "islamic": T("Your body has a right over you. (Sahih al-Bukhari 1975)", "Tubuhmu memiliki hak atas dirimu. (Sahih Bukhari 1975)"),
        "science": T("Micro-breaks every 30–45 min reduce neck/shoulder pain 30% and improve afternoon glucose (Applied Ergonomics; Diabetes Care 2016).",
                     "Jeda mikro setiap 30–45 menit mengurangi nyeri leher/bahu 30% dan memperbaiki glukosa sore (Applied Ergonomics; Diabetes Care 2016)."),
    },
    {
        "id": "ex_balance_55", "focus": "balance", "level": 1, "minutes": 8, "joint_friendly": True,
        "tags": ["balance_focus", "joint_friendly"],
        "name": T("Balance & Fall-Proofing", "Keseimbangan & Cegah Jatuh"),
        "equipment": T("Wall or counter for support", "Tembok atau meja untuk pegangan"),
        "steps": L(
            ("Single-leg stand 3×30 s each side", "Berdiri satu kaki 3×30 detik tiap sisi"),
            ("Heel-to-toe walk 10 steps ×3", "Jalan tumit-jari 10 langkah ×3"),
            ("Tandem stance eyes closed 2×20 s", "Berdiri tandem mata tertutup 2×20 detik"),
            ("Sit-to-stand without hands 2×8", "Duduk-berdiri tanpa tangan 2×8")),
        "islamic": T("Salah's movements themselves are graded balance training. (Journal of Physical Therapy Science 2017)", "Gerakan shalat sendiri adalah latihan keseimbangan bertingkat. (Journal of Physical Therapy Science 2017)"),
        "science": T("Balance training cuts falls ~40% in adults over 55; inability to stand on one leg for 10 s doubles 7-year mortality (British Journal of Sports Medicine 2022).",
                     "Latihan keseimbangan mengurangi jatuh ~40% pada usia 55+; ketidakmampuan berdiri satu kaki 10 detik menggandakan mortalitas 7 tahun (British Journal of Sports Medicine 2022)."),
    },
    {
        "id": "ex_zone2_bike", "focus": "cardio", "level": 2, "minutes": 30, "joint_friendly": True,
        "tags": ["more_energy", "lipid_focus", "weight_focus", "joint_friendly"],
        "name": T("Zone-2 Cycling or Swimming", "Sepeda atau Renang Zona 2"),
        "equipment": T("Bike, static bike, or pool (modest swimwear)", "Sepeda, sepeda statis, atau kolam (pakaian renang tertutup)"),
        "steps": L(
            ("Warm up 5 min easy", "Pemanasan 5 menit santai"),
            ("20 min at talk-test pace (can speak a sentence)", "20 menit pada kecepatan masih bisa bicara satu kalimat"),
            ("Cool down 5 min", "Pendinginan 5 menit")),
        "islamic": T("The Prophet ﷺ encouraged swimming and riding. (Reported in al-Bayhaqi)", "Nabi ﷺ menganjurkan berenang dan berkuda. (Diriwayatkan al-Baihaqi)"),
        "science": T("Zone-2 training improves mitochondrial function and insulin sensitivity; non-impact options spare knees and hips (Cell Metabolism 2017).",
                     "Latihan zona 2 memperbaiki fungsi mitokondria dan sensitivitas insulin; pilihan tanpa benturan menjaga lutut dan pinggul (Cell Metabolism 2017)."),
    },
    {
        "id": "ex_core_back", "focus": "strength", "level": 2, "minutes": 10, "joint_friendly": True,
        "tags": ["joint_friendly", "desk_worker", "build_strength"],
        "name": T("Core for a Pain-Free Back", "Inti Tubuh untuk Punggung Bebas Nyeri"),
        "equipment": T("Mat", "Matras / sajadah"),
        "steps": L(
            ("Dead bug 3×10", "Dead bug 3×10"),
            ("Bird-dog 3×8 each side", "Bird-dog 3×8 tiap sisi"),
            ("Side plank 3×20 s each side", "Plank samping 3×20 detik tiap sisi"),
            ("Glute bridge 3×12", "Glute bridge 3×12")),
        "islamic": T("Your lower back carries you through long qiyam and sujud.", "Punggung bawah Anda menopang qiyam dan sujud yang panjang."),
        "science": T("Core stabilisation reduces chronic low-back pain intensity ~43% (Journal of Physical Therapy Science 2019).",
                     "Stabilisasi inti tubuh menurunkan intensitas nyeri punggung bawah kronis ~43% (Journal of Physical Therapy Science 2019)."),
    },
    {
        "id": "ex_stair_intervals", "focus": "cardio", "level": 3, "minutes": 12, "joint_friendly": False,
        "tags": ["more_energy", "weight_focus"], "avoid": ["no_hiit", "joint_friendly"],
        "name": T("Stair Intervals", "Interval Tangga"),
        "equipment": T("Stairs", "Tangga"),
        "steps": L(
            ("Warm up 3 min walking", "Pemanasan 3 menit jalan"),
            ("Climb 60 s briskly, walk down slowly ×6", "Naik 60 detik cepat, turun perlahan ×6"),
            ("Cool down 3 min", "Pendinginan 3 menit")),
        "islamic": T("Hasten to good deeds. (Al-Baqarah 2:148)", "Berlomba-lombalah dalam kebaikan. (QS Al-Baqarah 2:148)"),
        "science": T("Brief stair-climbing bouts improve VO2peak ~5% in 6 weeks (Applied Physiology, Nutrition, and Metabolism 2019).",
                     "Naik tangga singkat meningkatkan VO2peak ~5% dalam 6 minggu (Applied Physiology, Nutrition, and Metabolism 2019)."),
    },
]

MIND_WINDOWS: list[dict] = [
    {
        "id": "mw_fajr", "window": "fajr", "minutes": 10, "tags": ["desk_worker", "mental_clarity", "calm_focus"],
        "name": T("After Fajr — The Clear Hour", "Setelah Subuh — Jam Jernih"),
        "how": T("No screen for 60 minutes. Quran, then write today's top 3 in order. Sunlight on your face if you can.",
                 "Tanpa layar 60 menit. Al-Quran, lalu tulis 3 prioritas hari ini berurutan. Terkena cahaya matahari jika bisa."),
        "islamic": T("\"O Allah, bless my Ummah in their early mornings.\" (Sunan Abi Dawud 2606)", "\"Ya Allah, berkahilah umatku di waktu pagi.\" (Sunan Abu Dawud 2606)"),
        "science": T("Cortisol and alertness peak 30–45 min after waking — the best window for planning and hard thinking (Psychoneuroendocrinology).",
                     "Kortisol dan kewaspadaan memuncak 30–45 menit setelah bangun — jendela terbaik untuk perencanaan dan berpikir berat (Psychoneuroendocrinology)."),
    },
    {
        "id": "mw_duha", "window": "morning", "minutes": 8, "tags": ["more_energy", "calm_focus"],
        "name": T("Mid-Morning — Duha Reset", "Pertengahan Pagi — Reset Dhuha"),
        "how": T("Two rakat Duha, then a glass of water and 2 minutes of standing stretch. Break the sitting.",
                 "Dua rakaat Dhuha, lalu segelas air dan 2 menit peregangan berdiri. Putus waktu duduk."),
        "islamic": T("\"In the morning, charity is due on every joint of you... and two rakat of Duha suffice for all of that.\" (Sahih Muslim 720)", "\"Setiap pagi ada sedekah pada setiap persendian kalian... dan dua rakaat Dhuha mencukupi semuanya.\" (Sahih Muslim 720)"),
        "science": T("Attention decays after ~90 minutes of focus; a movement break restores it (ultradian rhythm research, Kleitman).",
                     "Atensi menurun setelah ~90 menit fokus; jeda gerak memulihkannya (riset ritme ultradian, Kleitman)."),
    },
    {
        "id": "mw_dhuhr", "window": "dhuhr", "minutes": 20, "tags": ["more_energy", "shift_worker"],
        "name": T("After Dhuhr — Qailulah", "Setelah Dzuhur — Qailulah"),
        "how": T("Lunch (vegetables first), then a 15–20 min nap with an alarm, or 10 minutes of eyes-closed rest.",
                 "Makan siang (sayur dulu), lalu tidur 15–20 menit dengan alarm, atau 10 menit istirahat mata tertutup."),
        "islamic": T("The companions practised qailulah before Dhuhr or after it. (Sahih al-Bukhari 939 mentions napping after Jumu'ah)", "Para sahabat biasa qailulah sebelum atau sesudah Dzuhur. (Sahih Bukhari 939 menyebut tidur siang setelah Jumat)"),
        "science": T("10–20-minute naps improve alertness 3 hours without sleep inertia (Sleep 2006).", "Tidur 10–20 menit meningkatkan kewaspadaan 3 jam tanpa linglung (Sleep 2006)."),
    },
    {
        "id": "mw_asr", "window": "asr", "minutes": 5, "tags": ["calm_focus", "bp_focus", "desk_worker"],
        "name": T("After Asr — Breath & Reset", "Setelah Ashar — Napas & Reset"),
        "how": T("Box breathing 12 rounds on the mat. Then the evening adhkar. Close the work day mentally.",
                 "Napas kotak 12 putaran di sajadah. Lalu dzikir petang. Tutup hari kerja secara mental."),
        "islamic": T("\"Glorify Him before the rising of the sun and before its setting.\" (Ta-Ha 20:130)", "\"Bertasbihlah sebelum terbit matahari dan sebelum terbenamnya.\" (QS Ta-Ha 20:130)"),
        "science": T("Slow breathing raises HRV and lowers BP within minutes (Frontiers in Psychology 2017).", "Napas lambat menaikkan HRV dan menurunkan tekanan darah dalam hitungan menit (Frontiers in Psychology 2017)."),
    },
    {
        "id": "mw_maghrib", "window": "maghrib", "minutes": 15, "tags": ["glucose_focus", "calm_focus"],
        "name": T("After Maghrib — Walk & Sunset", "Setelah Maghrib — Jalan & Senja"),
        "how": T("Eat, then a 10–15 min family walk. Look at the sky. Screens stay home.",
                 "Makan, lalu jalan keluarga 10–15 menit. Lihat langit. Layar ditinggal di rumah."),
        "islamic": T("\"Indeed in the creation of the heavens and the earth are signs for people of understanding.\" (Ali 'Imran 3:190)", "\"Sungguh dalam penciptaan langit dan bumi ada tanda-tanda bagi orang berakal.\" (QS Ali Imran 3:190)"),
        "science": T("Post-meal walking lowers glucose spikes ~22%; awe reduces IL-6 (Diabetologia 2016; Emotion 2015).", "Jalan setelah makan menurunkan lonjakan glukosa ~22%; rasa takjub menurunkan IL-6 (Diabetologia 2016; Emotion 2015)."),
    },
    {
        "id": "mw_night", "window": "night", "minutes": 20, "tags": ["sleep_focus", "insomnia", "calm_focus"],
        "name": T("Before Sleep — Digital Sunset & Muhasabah", "Sebelum Tidur — Layar Padam & Muhasabah"),
        "how": T("Screens off 60 min before bed. Dim lights, wudu, three-question muhasabah, sleep adhkar, right side.",
                 "Layar padam 60 menit sebelum tidur. Lampu redup, wudhu, muhasabah tiga pertanyaan, dzikir tidur, miring kanan."),
        "islamic": T("\"When you go to bed, perform wudu... then lie on your right side.\" (Sahih al-Bukhari 247)", "\"Jika hendak tidur, berwudhulah... lalu berbaring miring ke kanan.\" (Sahih Bukhari 247)"),
        "science": T("A fixed pre-sleep ritual and screen-free hour give ~30% faster sleep onset and more deep sleep (Sleep Medicine Reviews 2015; PNAS 2015).",
                     "Ritual tidur tetap dan satu jam bebas layar memberi tidur ~30% lebih cepat dan tidur dalam lebih banyak (Sleep Medicine Reviews 2015; PNAS 2015)."),
    },
]


def _pick(val, lang: str):
    if isinstance(val, dict):
        return val.get(lang) or val.get("en")
    return val


def localize_entry(entry: dict, lang: str) -> dict:
    lang = lang if lang in ("en", "id") else "en"
    return {k: _pick(v, lang) for k, v in entry.items()}


def rank(entries: list[dict], flags: list[str], goals: list[str], diets: list[str], level: int = 1) -> list[dict]:
    """Score entries for this user; excluded ones are dropped, rest sorted by fit."""
    wanted = set(flags) | set(goals) | set(diets)
    out = []
    for e in entries:
        if set(e.get("avoid", [])) & set(flags):
            continue
        score = len(wanted & set(e.get("tags", []))) * 3
        if "level" in e:
            score -= abs(e["level"] - level) * 2
        out.append((score, e))
    out.sort(key=lambda p: -p[0])
    return [dict(e, fit_score=s) for s, e in out]
