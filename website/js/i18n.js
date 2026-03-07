/* ──────────────────────────────────────────────────────────────
   Model Maker Website — i18n (Internationalization)
   28 languages, RTL support, dynamic content switching
   ────────────────────────────────────────────────────────────── */

const TRANSLATIONS = {
  en: {
    nav_features: "Features",
    nav_models: "Models",
    nav_download: "Download",
    nav_community: "Community",
    hero_badge: "Emergency Medical AI",
    hero_title_1: "Medical Guidance",
    hero_title_2: "When the Internet Fails",
    hero_subtitle: "Emergency medical and survival help that runs on your own phone or computer. No internet needed. No data leaves your device. Works in 29 languages.",
    hero_cta_download: "Download — $1",
    hero_cta_check: "Will It Work on My Device?",
    hero_stat_languages: "Languages",
    hero_stat_offline: "Offline",
    hero_stat_tracking: "Tracking",
    hero_stat_free_num: "$1",
    hero_stat_free: "One Time",
    why_title: "Why Model Maker?",
    why_subtitle: "When the internet goes down, when there's no signal, when you need help the most — Model Maker is there.",
    why_nonet_title: "No Internet Needed",
    why_nonet_desc: "Works without any internet connection. During wars, natural disasters, or in remote areas — your AI helper is always available.",
    why_privacy_title: "Zero Data Collection",
    why_privacy_desc: "Everything stays on your phone or computer. Nothing is sent anywhere. No tracking, no data collection. Your conversations are 100% private.",
    why_lang_title: "29 Languages",
    why_lang_desc: "Arabic, English, French, Chinese, Hindi, and 24 more. Including right-to-left languages with full support.",
    why_medical_title: "Medical Knowledge",
    why_medical_desc: "Built with verified emergency medical knowledge. Covers first aid, wound care, medications, burn treatment, water safety, and more.",
    why_fast_title: "Fast on Any Device",
    why_fast_desc: "Works on phones with 4 GB of memory all the way up to powerful computers. We'll help you pick the right version for your device.",
    why_free_title: "Open Source",
    why_free_desc: "All source code is publicly available. Anyone can inspect it, improve it, or build on it. Transparent by design.",
    features_title: "What It Can Do",
    feat_chat_title: "Talk to It Like a Doctor",
    feat_chat_desc: "Talk to it like you would to a doctor. Ask about injuries, symptoms, or emergencies and get clear, helpful answers.",
    feat_rag_title: "Built-in Medical Library",
    feat_rag_desc: "Searches a built-in library of verified medical documents to give you accurate, trustworthy answers.",
    feat_memory_title: "Remembers You",
    feat_memory_desc: "Remembers your allergies, medical conditions, and medications so it can give you personalized advice every time.",
    feat_theme_title: "Easy to Read",
    feat_theme_desc: "Easy-to-read dark screen that works well in daylight and at night. Comfortable for long reading.",
    feat_responsive_title: "Works on Any Screen",
    feat_responsive_desc: "Looks great and works perfectly whether you're on a phone, tablet, or computer.",
    feat_stream_title: "Answers Appear Instantly",
    feat_stream_desc: "See answers appear word by word in real time — no waiting for the full reply to load.",
    models_title: "Choose Your Version",
    models_subtitle: "Three sizes to match your device. Small phones get the Lite version, powerful computers get the Premium.",
    model_lite: "Lite",
    model_standard: "Standard",
    model_premium: "Premium",
    model_recommended: "★ Recommended",
    model_ram_4: "Needs 4 GB memory",
    model_ram_8: "Needs 8 GB memory",
    model_ram_16: "Needs 16 GB memory",
    model_storage_4: "Takes 4 GB space",
    model_storage_6: "Takes 6 GB space",
    model_storage_12: "Takes 12 GB space",
    model_quality_good: "Good quality answers",
    model_quality_great: "Great quality answers",
    model_quality_best: "Best quality answers",
    model_speed_fast: "Fast answers",
    model_speed_balanced: "Good speed",
    model_speed_slower: "Detailed, thoughtful answers",
    model_lite_best: "Best for: Older phones & basic laptops",
    model_standard_best: "Best for: Most modern phones & computers",
    model_premium_best: "Best for: Powerful laptops & desktops",
    checker_title: "Will It Work on My Device?",
    checker_subtitle: "Not sure if it will work on your device? Just pick your phone or computer below.",
    checker_device_type: "What type of device?",
    checker_computer: "Computer / Laptop",
    checker_phone: "Phone / Tablet",
    checker_select_device: "Select your device (or closest match):",
    checker_choose: "-- Choose --",
    checker_dont_know: "Don't know your exact model? No problem!",
    checker_how_much_ram: "How much RAM does your device have?",
    checker_select_ram: "-- Select RAM --",
    checker_ram_tip: "💡 Tip: On Mac → Apple menu → About This Mac. On Windows → Settings → System → About.",
    checker_analyze: "Check Compatibility",
    checker_try_again: "Try Again",
    download_title: "Get Model Maker",
    download_subtitle: "Ready in 3 easy steps. No account needed. No sign-up.",
    download_step1_title: "Download the App",
    download_step1_desc: "Click your device type below to download the app.",
    download_step2_title: "Download the AI Brain",
    download_step2_desc: "The app will automatically suggest the right AI brain for your device. Just click download.",
    download_step3_title: "Start Asking Questions",
    download_step3_desc: "Open the app and start asking questions. No account needed, no internet needed.",
    download_source_title: "Or build from source:",
    community_title: "Help Save Lives",
    community_subtitle: "Model Maker is built by people who believe life-saving AI should be available to everyone.",
    community_contribute_title: "Improve the Code",
    community_contribute_desc: "Help fix bugs, add features, or review code. Every improvement helps save lives.",
    community_contribute_btn: "View on GitHub",
    community_knowledge_title: "Add Medical Info",
    community_knowledge_desc: "Are you a doctor, nurse, or paramedic? Help us add more life-saving medical information.",
    community_knowledge_btn: "Knowledge Guide",
    community_translate_title: "Translate",
    community_translate_desc: "Help this app speak your language. Translate the interface and medical knowledge to reach more people.",
    community_translate_btn: "Translation Guide",
    footer_desc: "Offline AI for emergency medical and survival guidance. Apache 2.0 open source.",
    footer_by: "Built by",
    footer_project: "Project",
    footer_source: "Source Code",
    footer_releases: "Releases",
    footer_changelog: "Changelog",
    footer_license: "License",
    footer_docs: "Documentation",
    footer_getting_started: "Getting Started",
    footer_architecture: "Architecture",
    footer_contributing: "Contributing",
    footer_security: "Security",
    footer_community: "Community",
    footer_discussions: "Discussions",
    footer_issues: "Report Issues",
    footer_author: "Author",
    footer_rights: "Apache 2.0 — Source code is open. Pre-built downloads are $1.",
    checker_result_great: "Great Match!",
    checker_result_good: "Works Well",
    checker_result_low: "Limited Compatibility",
    checker_result_great_desc: "Your device can run the Premium model with excellent performance.",
    checker_result_standard_desc: "Your device is perfect for the Standard model. Great balance of quality and speed.",
    checker_result_lite_desc: "Your device can run the Lite model. Fast responses with good quality.",
    checker_result_low_desc: "Your device has limited RAM. The Lite model will work but may be slow.",
    checker_result_recommend: "Recommended Model:",
  },
  ar: {
    nav_features: "المميزات",
    nav_models: "النماذج",
    nav_download: "تحميل",
    nav_community: "المجتمع",
    hero_badge: "ذكاء اصطناعي للطوارئ الطبية",
    hero_title_1: "إرشاد طبي",
    hero_title_2: "عندما ينقطع الإنترنت",
    hero_subtitle: "مساعد طبي وطوارئ يعمل على جوالك أو كمبيوترك بدون أي إنترنت. بياناتك تبقى عندك. يدعم ٢٩ لغة.",
    hero_cta_download: "تحميل — $1",
    hero_cta_check: "هل يعمل على جهازي؟",
    hero_stat_languages: "لغة",
    hero_stat_offline: "بدون إنترنت",
    hero_stat_tracking: "تتبع",
    hero_stat_free_num: "$1",
    hero_stat_free: "مرة واحدة",
    why_title: "لماذا Model Maker؟",
    why_subtitle: "عندما ينقطع الإنترنت، عندما لا توجد شبكة، عندما تحتاج المساعدة أكثر — Model Maker موجود.",
    why_nonet_title: "لا حاجة للإنترنت",
    why_nonet_desc: "يعمل بدون أي اتصال إنترنت. أثناء الحروب والكوارث أو في المناطق النائية — المساعد الذكي دائماً جاهز.",
    why_privacy_title: "صفر جمع بيانات",
    why_privacy_desc: "كل شيء يبقى على جوالك أو كمبيوترك. لا يتم إرسال أي شيء لأي مكان. محادثاتك خاصة ١٠٠٪.",
    why_lang_title: "٢٩ لغة",
    why_lang_desc: "العربية والإنجليزية والفرنسية والصينية والهندية و٢٤ لغة أخرى. مع دعم كامل للغات من اليمين لليسار.",
    why_medical_title: "معرفة طبية",
    why_medical_desc: "مبني على معلومات طبية موثقة. يغطي الإسعافات الأولية، علاج الجروح، الأدوية، الحروق، سلامة المياه، والمزيد.",
    why_fast_title: "سريع على أي جهاز",
    why_fast_desc: "يعمل على جوالات من ٤ جيجا وصولاً لأقوى الكمبيوترات. نساعدك تختار النسخة المناسبة لجهازك.",
    why_free_title: "مفتوح المصدر",
    why_free_desc: "الكود كله موجود للجميع. أي شخص يقدر يشوفه، يحسّنه، أو يبني عليه. شفافية كاملة.",
    features_title: "شنو يقدر يسوي",
    feat_chat_title: "تكلم معه مثل الدكتور",
    feat_chat_desc: "تكلم معه مثل ما تتكلم مع دكتور. اسأل عن أي إصابة أو حالة طوارئ ويعطيك إجابات واضحة.",
    feat_rag_title: "مكتبة طبية مدمجة",
    feat_rag_desc: "يبحث في مكتبة طبية مدمجة عشان يعطيك إجابات دقيقة وموثوقة.",
    feat_memory_title: "يتذكرك",
    feat_memory_desc: "يتذكر حساسياتك وأمراضك وأدويتك عشان يعطيك نصائح مخصصة كل مرة.",
    feat_theme_title: "سهل القراءة",
    feat_theme_desc: "شاشة داكنة مريحة للعين تشتغل بالنهار والليل.",
    feat_responsive_title: "يشتغل على أي شاشة",
    feat_responsive_desc: "يشتغل بشكل ممتاز على الجوال أو التابلت أو الكمبيوتر.",
    feat_stream_title: "الرد يطلع فوراً",
    feat_stream_desc: "شاهد الرد يطلع كلمة كلمة — ما تحتاج تنتظر.",
    models_title: "اختر النسخة",
    models_subtitle: "ثلاث نسخ تناسب جهازك. الجوالات الصغيرة تاخذ النسخة الخفيفة، الكمبيوترات القوية تاخذ المتميزة.",
    model_lite: "خفيف",
    model_standard: "قياسي",
    model_premium: "متميز",
    model_recommended: "★ موصى به",
    model_ram_4: "٤ جيجا رام كحد أدنى",
    model_ram_8: "٨ جيجا رام كحد أدنى",
    model_ram_16: "١٦ جيجا رام كحد أدنى",
    model_storage_4: "٤ جيجا مساحة تخزين",
    model_storage_6: "٦ جيجا مساحة تخزين",
    model_storage_12: "١٢ جيجا مساحة تخزين",
    model_quality_good: "جودة جيدة",
    model_quality_great: "جودة ممتازة",
    model_quality_best: "أفضل جودة",
    model_speed_fast: "ردود سريعة",
    model_speed_balanced: "سرعة متوازنة",
    model_speed_slower: "ردود مدروسة",
    model_lite_best: "الأفضل لـ: الهواتف القديمة والحواسيب البسيطة",
    model_standard_best: "الأفضل لـ: الهواتف الحديثة ومعظم الحواسيب",
    model_premium_best: "الأفضل لـ: الحواسيب والأجهزة القوية",
    checker_title: "هل يشتغل على جهازي؟",
    checker_subtitle: "مو متأكد إذا يشتغل على جهازك؟ اختر جوالك أو كمبيوترك وراح نقولك.",
    checker_device_type: "ما نوع جهازك؟",
    checker_computer: "كمبيوتر / لابتوب",
    checker_phone: "هاتف / تابلت",
    checker_select_device: "اختر جهازك (أو الأقرب):",
    checker_choose: "-- اختر --",
    checker_dont_know: "لا تعرف موديل جهازك بالضبط؟ لا مشكلة!",
    checker_how_much_ram: "كم رام في جهازك؟",
    checker_select_ram: "-- اختر الرام --",
    checker_ram_tip: "💡 نصيحة: في ماك ← قائمة آبل ← حول هذا الماك. في ويندوز ← الإعدادات ← النظام ← حول.",
    checker_analyze: "فحص التوافق",
    checker_try_again: "حاول مرة أخرى",
    download_title: "حمّل Model Maker",
    download_subtitle: "جاهز بـ ٣ خطوات سهلة. بدون حساب. بدون تسجيل.",
    download_step1_title: "حمّل التطبيق",
    download_step1_desc: "اضغط على نوع جهازك وحمّل التطبيق.",
    download_step2_title: "حمّل العقل الذكي",
    download_step2_desc: "التطبيق يقترح لك العقل المناسب لجهازك. بس اضغط تحميل.",
    download_step3_title: "ابدأ اسأل",
    download_step3_desc: "افتح التطبيق وابدأ اسأل. بدون حساب، بدون إنترنت.",
    download_source_title: "أو ابنِ من المصدر:",
    community_title: "ساعد في إنقاذ الأرواح",
    community_subtitle: "Model Maker بناه أشخاص يؤمنون أن الذكاء الاصطناعي المنقذ للحياة لازم يكون متاح للجميع.",
    community_contribute_title: "حسّن الكود",
    community_contribute_desc: "ساعد في إصلاح المشاكل وإضافة ميزات جديدة. كل تحسين يساعد في إنقاذ الأرواح.",
    community_contribute_btn: "على GitHub",
    community_knowledge_title: "أضف معلومات طبية",
    community_knowledge_desc: "هل أنت دكتور أو ممرض أو مسعف؟ ساعدنا نضيف معلومات طبية تنقذ الأرواح.",
    community_knowledge_btn: "دليل المعرفة",
    community_translate_title: "ترجم",
    community_translate_desc: "ساعد التطبيق يتكلم لغتك. ترجم الواجهة والمعلومات الطبية عشان توصل لناس أكثر.",
    community_translate_btn: "دليل الترجمة",
    footer_desc: "ذكاء اصطناعي بدون إنترنت للإرشاد الطبي الطارئ والبقاء. مفتوح المصدر Apache 2.0.",
    footer_by: "بناه",
    footer_project: "المشروع",
    footer_source: "الكود المصدري",
    footer_releases: "الإصدارات",
    footer_changelog: "سجل التغييرات",
    footer_license: "الرخصة",
    footer_docs: "التوثيق",
    footer_getting_started: "البداية",
    footer_architecture: "البنية",
    footer_contributing: "المساهمة",
    footer_security: "الأمان",
    footer_community: "المجتمع",
    footer_discussions: "النقاشات",
    footer_issues: "الإبلاغ عن مشاكل",
    footer_author: "المؤلف",
    footer_rights: "Apache 2.0 — الكود مفتوح. التحميل الجاهز بـ $1.",
    checker_result_great: "تطابق ممتاز!",
    checker_result_good: "يعمل جيداً",
    checker_result_low: "توافق محدود",
    checker_result_great_desc: "جهازك يمكنه تشغيل النموذج المتميز بأداء ممتاز.",
    checker_result_standard_desc: "جهازك مثالي للنموذج القياسي. توازن ممتاز بين الجودة والسرعة.",
    checker_result_lite_desc: "جهازك يمكنه تشغيل النموذج الخفيف. ردود سريعة بجودة جيدة.",
    checker_result_low_desc: "جهازك فيه رام محدود. النموذج الخفيف سيعمل لكن قد يكون بطيئاً.",
    checker_result_recommend: "النموذج الموصى:",
  },
  fr: {
    nav_features: "Fonctionnalités",
    nav_models: "Modèles",
    nav_download: "Télécharger",
    nav_community: "Communauté",
    hero_badge: "IA Médicale d'Urgence",
    hero_title_1: "Assistance Médicale",
    hero_title_2: "Quand Internet Tombe",
    hero_subtitle: "Aide médicale d'urgence et de survie qui fonctionne sur votre téléphone ou ordinateur. Sans internet. Vos données restent chez vous. 29 langues.",
    hero_cta_download: "Télécharger — 1$",
    hero_cta_check: "Vérifier Mon Appareil",
    hero_stat_languages: "Langues",
    hero_stat_offline: "Hors Ligne",
    hero_stat_tracking: "Pistage",
    hero_stat_free_num: "1$",
    hero_stat_free: "Une Fois",
    why_title: "Pourquoi Model Maker ?",
    why_subtitle: "Quand Internet est coupé, quand les serveurs sont inaccessibles, quand vous avez le plus besoin d'aide — Model Maker est là.",
    checker_title: "Vérifiez Votre Appareil",
    checker_subtitle: "Pas sûr quel modèle convient ? Dites-nous votre appareil et nous recommanderons le parfait.",
    download_title: "Télécharger Model Maker",
    community_title: "Rejoignez la Communauté",
  },
  es: {
    nav_features: "Características",
    nav_models: "Modelos",
    nav_download: "Descargar",
    nav_community: "Comunidad",
    hero_badge: "IA Médica de Emergencia",
    hero_title_1: "Asistencia Médica",
    hero_title_2: "Cuando Falla el Internet",
    hero_subtitle: "Orientación médica de emergencia y supervivencia con IA que funciona completamente en tu dispositivo. Sin internet. Sin nube. Sin recopilación de datos. 29 idiomas.",
    hero_cta_download: "Descargar — $1",
    hero_cta_check: "Verificar Mi Dispositivo",
  },
  de: {
    hero_badge: "Medizinische Notfall-KI",
    hero_title_1: "Medizinische Hilfe",
    hero_title_2: "Wenn das Internet Ausfällt",
    hero_cta_download: "Herunterladen — 1$",
  },
  zh: {
    hero_badge: "急救医疗AI",
    hero_title_1: "医疗指导",
    hero_title_2: "当互联网中断时",
    hero_subtitle: "AI驱动的急救医疗和生存指导，完全在您的设备上运行。无需互联网。无云端。不收集数据。29种语言。",
    hero_cta_download: "下载 — $1",
    hero_cta_check: "检查我的设备",
  },
  ja: {
    hero_badge: "緊急医療AI",
    hero_title_1: "医療ガイダンス",
    hero_title_2: "ネットが途絶えた時",
    hero_cta_download: "ダウンロード — $1",
  },
  ko: {
    hero_badge: "응급 의료 AI",
    hero_title_1: "의료 안내",
    hero_title_2: "인터넷이 끊길 때",
    hero_cta_download: "다운로드 — $1",
  },
  hi: {
    hero_badge: "आपातकालीन चिकित्सा AI",
    hero_title_1: "चिकित्सा मार्गदर्शन",
    hero_title_2: "जब इंटरनेट बंद हो",
    hero_cta_download: "डाउनलोड — $1",
  },
  ur: {
    hero_badge: "ہنگامی طبی AI",
    hero_title_1: "طبی رہنمائی",
    hero_title_2: "جب انٹرنیٹ بند ہو",
    hero_cta_download: "ڈاؤن لوڈ — $1",
  },
  fa: {
    hero_badge: "هوش مصنوعی پزشکی اضطراری",
    hero_title_1: "راهنمای پزشکی",
    hero_title_2: "وقتی اینترنت قطع شود",
    hero_cta_download: "دانلود — ۱$",
  },
  tr: {
    hero_badge: "Acil Tıbbi Yapay Zeka",
    hero_title_1: "Tıbbi Rehberlik",
    hero_title_2: "İnternet Kesildiğinde",
    hero_cta_download: "İndir — $1",
  },
  ru: {
    hero_badge: "Экстренный Медицинский ИИ",
    hero_title_1: "Медицинская Помощь",
    hero_title_2: "Когда Интернет Недоступен",
    hero_cta_download: "Скачать — $1",
  },
  pt: {
    hero_badge: "IA Médica de Emergência",
    hero_title_1: "Orientação Médica",
    hero_title_2: "Quando a Internet Falha",
    hero_cta_download: "Baixar — $1",
  },
  it: {
    hero_badge: "IA Medica di Emergenza",
    hero_title_1: "Assistenza Medica",
    hero_title_2: "Quando Internet Non C'è",
    hero_cta_download: "Scarica — $1",
  },
  nl: { hero_cta_download: "Downloaden — $1" },
  pl: { hero_cta_download: "Pobierz — $1" },
  uk: { hero_cta_download: "Завантажити — $1" },
  ms: { hero_cta_download: "Muat Turun — $1" },
  id: { hero_cta_download: "Unduh — $1" },
  th: { hero_cta_download: "ดาวน์โหลด — $1" },
  vi: { hero_cta_download: "Tải về — $1" },
  bn: { hero_cta_download: "ডাউনলোড — $1" },
  ta: { hero_cta_download: "பதிவிறக்கம் — $1" },
  sw: { hero_cta_download: "Pakua — $1" },
  he: { hero_cta_download: "הורד — $1" },
  ku: { hero_cta_download: "Daxistin — $1" },
  ps: { hero_cta_download: "ډاونلوډ — $1" },
};

// RTL languages
const RTL_LANGS = new Set(["ar", "ur", "fa", "he", "ps"]);

// Current language
let currentLang = "en";

/**
 * Apply translations to all elements with data-i18n attribute
 */
function applyTranslations(lang) {
  currentLang = lang;
  const trans = TRANSLATIONS[lang] || {};
  const fallback = TRANSLATIONS.en;

  // Set HTML dir and lang
  document.documentElement.lang = lang;
  document.documentElement.dir = RTL_LANGS.has(lang) ? "rtl" : "ltr";

  // Translate all elements
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    const text = trans[key] || fallback[key];
    if (text) {
      el.textContent = text;
    }
  });

  // Store preference
  try {
    localStorage.setItem("mm-lang", lang);
  } catch (e) {
    // localStorage not available
  }
}

/**
 * Get translated string by key
 */
function t(key) {
  const trans = TRANSLATIONS[currentLang] || {};
  return trans[key] || TRANSLATIONS.en[key] || key;
}

/**
 * Initialize i18n — detect language from URL, localStorage, or browser
 */
function initI18n() {
  // Priority: URL param > localStorage > browser language
  const urlParams = new URLSearchParams(window.location.search);
  let lang = urlParams.get("lang");

  if (!lang) {
    try {
      lang = localStorage.getItem("mm-lang");
    } catch (e) {}
  }

  if (!lang) {
    const browserLang = navigator.language?.split("-")[0];
    if (TRANSLATIONS[browserLang]) {
      lang = browserLang;
    }
  }

  lang = lang && TRANSLATIONS[lang] ? lang : "en";

  // Set switcher
  const switcher = document.getElementById("langSwitcher");
  if (switcher) {
    switcher.value = lang;
    switcher.addEventListener("change", (e) => {
      applyTranslations(e.target.value);
    });
  }

  applyTranslations(lang);
}

// Initialize on DOM ready
document.addEventListener("DOMContentLoaded", initI18n);
