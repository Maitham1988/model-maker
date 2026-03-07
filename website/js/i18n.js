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
    hero_badge: "100% Free & Open Source",
    hero_title_1: "Offline AI",
    hero_title_2: "That Saves Lives",
    hero_subtitle: "Medical guidance, survival knowledge, and emergency help — powered by AI that runs entirely on your device. No internet. No cloud. No tracking. Free forever.",
    hero_cta_download: "Download Free",
    hero_cta_check: "Check My Device",
    hero_stat_languages: "Languages",
    hero_stat_offline: "Offline",
    hero_stat_tracking: "Tracking",
    hero_stat_free_num: "Free",
    hero_stat_free: "Forever",
    why_title: "Why Model Maker?",
    why_subtitle: "When the internet goes down, when servers are unreachable, when you need help the most — Model Maker is there.",
    why_nonet_title: "No Internet Needed",
    why_nonet_desc: "Works completely offline. During wars, disasters, or in remote areas — your AI assistant never goes down.",
    why_privacy_title: "Zero Data Collection",
    why_privacy_desc: "Everything stays on your device. No telemetry, no analytics, no cloud sync. Your conversations are yours alone.",
    why_lang_title: "29 Languages",
    why_lang_desc: "Arabic, English, French, Chinese, Hindi, and 24 more. Including right-to-left languages with full support.",
    why_medical_title: "Medical Knowledge",
    why_medical_desc: "Trained on verified emergency medical and survival knowledge. First aid, wound care, medication, water purification.",
    why_fast_title: "Fast on Any Device",
    why_fast_desc: "From 4GB phones to powerful desktops. Choose the model that fits your device. GPU acceleration on Mac and NVIDIA.",
    why_free_title: "Free & Open Source",
    why_free_desc: "Apache 2.0 license. Free to use, modify, and distribute. Built by the community, for humanity.",
    features_title: "Powerful Features",
    feat_chat_title: "Smart Chat",
    feat_chat_desc: "ChatGPT-like conversation with streaming responses. Ask anything about medical emergencies, survival, or daily life.",
    feat_rag_title: "Knowledge System",
    feat_rag_desc: "Built-in RAG searches verified medical documents to give accurate answers.",
    feat_memory_title: "Persistent Memory",
    feat_memory_desc: "Remembers important facts about you — allergies, conditions, medications — for personalized guidance.",
    feat_theme_title: "Beautiful Dark UI",
    feat_theme_desc: "Professional dark theme designed for readability in any lighting condition.",
    feat_responsive_title: "Any Screen Size",
    feat_responsive_desc: "Works perfectly on phones, tablets, and desktops.",
    feat_stream_title: "Real-Time Streaming",
    feat_stream_desc: "See AI responses appear word by word. Powered by Server-Sent Events.",
    models_title: "Choose Your Model",
    models_subtitle: "Three tiers to match any device. Powered by Qwen2.5 — one of the world's best multilingual AI models.",
    model_lite: "Lite",
    model_standard: "Standard",
    model_premium: "Premium",
    model_recommended: "★ Recommended",
    model_ram_4: "4 GB RAM minimum",
    model_ram_8: "8 GB RAM minimum",
    model_ram_16: "16 GB RAM minimum",
    model_storage_4: "4 GB storage",
    model_storage_6: "6 GB storage",
    model_storage_12: "12 GB storage",
    model_quality_good: "Good quality",
    model_quality_great: "Great quality",
    model_quality_best: "Best quality",
    model_speed_fast: "Fast responses",
    model_speed_balanced: "Balanced speed",
    model_speed_slower: "Thoughtful responses",
    model_lite_best: "Best for: Older phones & basic laptops",
    model_standard_best: "Best for: Modern phones & most computers",
    model_premium_best: "Best for: Powerful laptops & desktops",
    checker_title: "Check Your Device",
    checker_subtitle: "Not sure which model fits? Tell us about your device and we'll recommend the perfect one.",
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
    download_title: "Download Model Maker",
    download_subtitle: "Get started in 3 simple steps. No account needed.",
    download_step1_title: "Download the App",
    download_step1_desc: "Choose your platform and download Model Maker.",
    download_step2_title: "Download a Model",
    download_step2_desc: "Run the built-in downloader to get the AI model that fits your device.",
    download_step3_title: "Start Using",
    download_step3_desc: "Launch the app and start chatting. No account, no setup, no internet.",
    download_source_title: "Or build from source:",
    community_title: "Join the Community",
    community_subtitle: "Model Maker is built by people who believe AI should be accessible to everyone.",
    community_contribute_title: "Contribute",
    community_contribute_desc: "Add medical knowledge, translate to your language, improve the code. Every contribution saves lives.",
    community_contribute_btn: "View on GitHub",
    community_knowledge_title: "Add Knowledge",
    community_knowledge_desc: "Are you a doctor, nurse, or paramedic? Help us build the most comprehensive offline medical guide.",
    community_knowledge_btn: "Knowledge Guide",
    community_translate_title: "Translate",
    community_translate_desc: "Help us reach more people. Translate the interface and knowledge base into your native language.",
    community_translate_btn: "Translation Guide",
    footer_desc: "Offline AI for emergency, medical, and survival situations. Free forever.",
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
    footer_rights: "Apache 2.0 — Free for everyone.",
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
    hero_badge: "مجاني ومفتوح المصدر ١٠٠٪",
    hero_title_1: "ذكاء اصطناعي بدون إنترنت",
    hero_title_2: "ينقذ الأرواح",
    hero_subtitle: "إرشادات طبية ومعرفة بالنجاة ومساعدة طارئة — مدعوم بذكاء اصطناعي يعمل بالكامل على جهازك. بدون إنترنت. بدون سحابة. بدون تتبع. مجاني للأبد.",
    hero_cta_download: "تحميل مجاني",
    hero_cta_check: "فحص جهازي",
    hero_stat_languages: "لغة",
    hero_stat_offline: "بدون إنترنت",
    hero_stat_tracking: "تتبع",
    hero_stat_free_num: "مجاني",
    hero_stat_free: "للأبد",
    why_title: "لماذا Model Maker؟",
    why_subtitle: "عندما ينقطع الإنترنت، عندما لا يمكن الوصول للخوادم، عندما تحتاج المساعدة أكثر — Model Maker موجود.",
    why_nonet_title: "لا حاجة للإنترنت",
    why_nonet_desc: "يعمل بالكامل بدون اتصال. أثناء الحروب والكوارث أو في المناطق النائية — مساعدك الذكي لا يتوقف أبداً.",
    why_privacy_title: "صفر جمع بيانات",
    why_privacy_desc: "كل شيء يبقى على جهازك. لا تتبع، لا تحليلات، لا مزامنة سحابية. محادثاتك ملكك وحدك.",
    why_lang_title: "٢٩ لغة",
    why_lang_desc: "العربية والإنجليزية والفرنسية والصينية والهندية و٢٤ لغة أخرى. مع دعم كامل للغات من اليمين لليسار.",
    why_medical_title: "معرفة طبية",
    why_medical_desc: "مدرّب على معرفة طبية وبقاء طارئة موثقة. إسعافات أولية، عناية بالجروح، أدوية، تنقية المياه.",
    why_fast_title: "سريع على أي جهاز",
    why_fast_desc: "من هواتف ٤ جيجا إلى أجهزة كمبيوتر قوية. اختر النموذج المناسب لجهازك.",
    why_free_title: "مجاني ومفتوح المصدر",
    why_free_desc: "رخصة Apache 2.0. مجاني للاستخدام والتعديل والتوزيع. بناه المجتمع، للبشرية.",
    features_title: "مميزات قوية",
    feat_chat_title: "محادثة ذكية",
    feat_chat_desc: "محادثة مثل ChatGPT مع ردود متدفقة. اسأل عن أي شيء يخص الطوارئ الطبية أو النجاة.",
    feat_rag_title: "نظام معرفي",
    feat_rag_desc: "يبحث في وثائق طبية موثقة لإعطاء إجابات دقيقة.",
    feat_memory_title: "ذاكرة دائمة",
    feat_memory_desc: "يتذكر معلومات مهمة عنك — الحساسية، الحالات، الأدوية — لإرشاد مخصص.",
    feat_theme_title: "واجهة داكنة جميلة",
    feat_theme_desc: "سمة داكنة احترافية مصممة للقراءة في أي ظروف إضاءة.",
    feat_responsive_title: "أي حجم شاشة",
    feat_responsive_desc: "يعمل بشكل مثالي على الهواتف والأجهزة اللوحية وأجهزة الكمبيوتر.",
    feat_stream_title: "بث مباشر",
    feat_stream_desc: "شاهد ردود الذكاء الاصطناعي تظهر كلمة بكلمة.",
    models_title: "اختر نموذجك",
    models_subtitle: "ثلاث مستويات لتناسب أي جهاز. مدعوم بـ Qwen2.5 — أحد أفضل نماذج الذكاء الاصطناعي متعددة اللغات.",
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
    checker_title: "افحص جهازك",
    checker_subtitle: "غير متأكد أي نموذج يناسبك؟ أخبرنا عن جهازك وسنوصي بالنموذج المثالي.",
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
    download_title: "تحميل Model Maker",
    download_subtitle: "ابدأ في ٣ خطوات بسيطة. لا حاجة لحساب.",
    download_step1_title: "حمّل التطبيق",
    download_step1_desc: "اختر منصتك وحمّل Model Maker.",
    download_step2_title: "حمّل النموذج",
    download_step2_desc: "شغّل المحمّل المدمج للحصول على نموذج الذكاء الاصطناعي المناسب لجهازك.",
    download_step3_title: "ابدأ الاستخدام",
    download_step3_desc: "شغّل التطبيق وابدأ المحادثة. بدون حساب، بدون إعداد، بدون إنترنت.",
    download_source_title: "أو ابنِ من المصدر:",
    community_title: "انضم للمجتمع",
    community_subtitle: "Model Maker بناه أشخاص يؤمنون أن الذكاء الاصطناعي يجب أن يكون متاحاً للجميع.",
    community_contribute_title: "ساهم",
    community_contribute_desc: "أضف معرفة طبية، ترجم للغتك، حسّن الكود. كل مساهمة تنقذ أرواحاً.",
    community_contribute_btn: "على GitHub",
    community_knowledge_title: "أضف معرفة",
    community_knowledge_desc: "هل أنت طبيب أو ممرض أو مسعف؟ ساعدنا في بناء أشمل دليل طبي بدون إنترنت.",
    community_knowledge_btn: "دليل المعرفة",
    community_translate_title: "ترجم",
    community_translate_desc: "ساعدنا في الوصول لمزيد من الناس. ترجم الواجهة وقاعدة المعرفة إلى لغتك.",
    community_translate_btn: "دليل الترجمة",
    footer_desc: "ذكاء اصطناعي بدون إنترنت لحالات الطوارئ والبقاء. مجاني للأبد.",
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
    footer_rights: "Apache 2.0 — مجاني للجميع.",
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
    hero_badge: "100% Gratuit & Open Source",
    hero_title_1: "IA Hors Ligne",
    hero_title_2: "Qui Sauve des Vies",
    hero_subtitle: "Conseils médicaux, connaissances de survie et aide d'urgence — alimentés par une IA qui fonctionne entièrement sur votre appareil. Sans internet. Sans cloud. Sans pistage. Gratuit pour toujours.",
    hero_cta_download: "Télécharger Gratuit",
    hero_cta_check: "Vérifier Mon Appareil",
    hero_stat_languages: "Langues",
    hero_stat_offline: "Hors Ligne",
    hero_stat_tracking: "Pistage",
    hero_stat_free_num: "Gratuit",
    hero_stat_free: "Pour Toujours",
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
    hero_badge: "100% Gratis y Código Abierto",
    hero_title_1: "IA Sin Internet",
    hero_title_2: "Que Salva Vidas",
    hero_subtitle: "Orientación médica, conocimientos de supervivencia y ayuda de emergencia — con IA que funciona completamente en tu dispositivo. Sin internet. Sin nube. Sin rastreo. Gratis para siempre.",
    hero_cta_download: "Descargar Gratis",
    hero_cta_check: "Verificar Mi Dispositivo",
  },
  de: {
    hero_badge: "100% Kostenlos & Open Source",
    hero_title_1: "Offline-KI",
    hero_title_2: "Die Leben Rettet",
    hero_cta_download: "Kostenlos Herunterladen",
  },
  zh: {
    hero_badge: "100% 免费开源",
    hero_title_1: "离线人工智能",
    hero_title_2: "拯救生命",
    hero_subtitle: "医疗指导、生存知识和紧急帮助——由完全在您设备上运行的AI提供支持。无需互联网。无云。无追踪。永久免费。",
    hero_cta_download: "免费下载",
    hero_cta_check: "检查我的设备",
  },
  ja: {
    hero_badge: "100% 無料・オープンソース",
    hero_title_1: "オフラインAI",
    hero_title_2: "命を救う",
    hero_cta_download: "無料ダウンロード",
  },
  ko: {
    hero_badge: "100% 무료 & 오픈소스",
    hero_title_1: "오프라인 AI",
    hero_title_2: "생명을 구하는",
    hero_cta_download: "무료 다운로드",
  },
  hi: {
    hero_badge: "100% मुफ्त और ओपन सोर्स",
    hero_title_1: "ऑफलाइन AI",
    hero_title_2: "जो जान बचाए",
    hero_cta_download: "मुफ्त डाउनलोड",
  },
  ur: {
    hero_badge: "100% مفت اور اوپن سورس",
    hero_title_1: "آف لائن AI",
    hero_title_2: "جو زندگیاں بچائے",
    hero_cta_download: "مفت ڈاؤن لوڈ",
  },
  fa: {
    hero_badge: "100% رایگان و متن‌باز",
    hero_title_1: "هوش مصنوعی آفلاین",
    hero_title_2: "که جان نجات می‌دهد",
    hero_cta_download: "دانلود رایگان",
  },
  tr: {
    hero_badge: "100% Ücretsiz & Açık Kaynak",
    hero_title_1: "Çevrimdışı Yapay Zeka",
    hero_title_2: "Hayat Kurtaran",
    hero_cta_download: "Ücretsiz İndir",
  },
  ru: {
    hero_badge: "100% Бесплатно и с открытым кодом",
    hero_title_1: "Офлайн ИИ",
    hero_title_2: "Который Спасает Жизни",
    hero_cta_download: "Скачать Бесплатно",
  },
  pt: {
    hero_badge: "100% Grátis & Código Aberto",
    hero_title_1: "IA Offline",
    hero_title_2: "Que Salva Vidas",
    hero_cta_download: "Baixar Grátis",
  },
  it: {
    hero_badge: "100% Gratuito & Open Source",
    hero_title_1: "IA Offline",
    hero_title_2: "Che Salva Vite",
    hero_cta_download: "Scarica Gratis",
  },
  nl: { hero_cta_download: "Gratis Downloaden" },
  pl: { hero_cta_download: "Pobierz za Darmo" },
  uk: { hero_cta_download: "Завантажити Безкоштовно" },
  ms: { hero_cta_download: "Muat Turun Percuma" },
  id: { hero_cta_download: "Unduh Gratis" },
  th: { hero_cta_download: "ดาวน์โหลดฟรี" },
  vi: { hero_cta_download: "Tải Miễn Phí" },
  bn: { hero_cta_download: "বিনামূল্যে ডাউনলোড" },
  ta: { hero_cta_download: "இலவசமாக பதிவிறக்கம்" },
  sw: { hero_cta_download: "Pakua Bure" },
  he: { hero_cta_download: "הורד בחינם" },
  ku: { hero_cta_download: "Belaş Daxistin" },
  ps: { hero_cta_download: "وړيا ډاونلوډ" },
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
