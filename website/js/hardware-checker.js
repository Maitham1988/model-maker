/* ──────────────────────────────────────────────────────────────
   Model Maker Website — Hardware Checker
   Recommends the best model tier based on device specs
   ────────────────────────────────────────────────────────────── */

// Device presets from registry
const DEVICE_PRESETS = {
  computers: [
    // ── Apple Mac ──────────────────────────────────
    { name: "MacBook Air M1 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "MacBook Air M2 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "MacBook Air M2 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "MacBook Air M3 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "MacBook Air M3 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "MacBook Air M4 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "MacBook Pro M1 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "MacBook Pro M1 Pro (16GB)", ram_gb: 16, tier: "premium" },
    { name: "MacBook Pro M1 Pro (32GB)", ram_gb: 32, tier: "premium" },
    { name: "MacBook Pro M1 Max (32GB)", ram_gb: 32, tier: "premium" },
    { name: "MacBook Pro M1 Max (64GB)", ram_gb: 64, tier: "premium" },
    { name: "MacBook Pro M2 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "MacBook Pro M2 Pro (16GB)", ram_gb: 16, tier: "premium" },
    { name: "MacBook Pro M2 Pro (32GB)", ram_gb: 32, tier: "premium" },
    { name: "MacBook Pro M2 Max (32GB)", ram_gb: 32, tier: "premium" },
    { name: "MacBook Pro M2 Max (64GB+)", ram_gb: 64, tier: "premium" },
    { name: "MacBook Pro M3 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "MacBook Pro M3 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "MacBook Pro M3 Pro (18GB)", ram_gb: 18, tier: "premium" },
    { name: "MacBook Pro M3 Pro (36GB)", ram_gb: 36, tier: "premium" },
    { name: "MacBook Pro M3 Max (36GB)", ram_gb: 36, tier: "premium" },
    { name: "MacBook Pro M3 Max (48GB)", ram_gb: 48, tier: "premium" },
    { name: "MacBook Pro M3 Max (64GB+)", ram_gb: 64, tier: "premium" },
    { name: "MacBook Pro M4 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "MacBook Pro M4 (24GB)", ram_gb: 24, tier: "premium" },
    { name: "MacBook Pro M4 Pro (24GB)", ram_gb: 24, tier: "premium" },
    { name: "MacBook Pro M4 Pro (48GB)", ram_gb: 48, tier: "premium" },
    { name: "MacBook Pro M4 Max (36GB)", ram_gb: 36, tier: "premium" },
    { name: "MacBook Pro M4 Max (48GB)", ram_gb: 48, tier: "premium" },
    { name: "MacBook Pro M4 Max (64GB+)", ram_gb: 64, tier: "premium" },
    { name: "iMac M1 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "iMac M1 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "iMac M3 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "iMac M3 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "iMac M3 (24GB)", ram_gb: 24, tier: "premium" },
    { name: "iMac M4 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "iMac M4 (24GB+)", ram_gb: 24, tier: "premium" },
    { name: "Mac Mini M1 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "Mac Mini M1 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "Mac Mini M2 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "Mac Mini M2 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "Mac Mini M2 Pro (16GB)", ram_gb: 16, tier: "premium" },
    { name: "Mac Mini M2 Pro (32GB)", ram_gb: 32, tier: "premium" },
    { name: "Mac Mini M4 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "Mac Mini M4 Pro (24GB)", ram_gb: 24, tier: "premium" },
    { name: "Mac Mini M4 Pro (48GB)", ram_gb: 48, tier: "premium" },
    { name: "Mac Studio M1 Max (32GB)", ram_gb: 32, tier: "premium" },
    { name: "Mac Studio M1 Ultra (64GB+)", ram_gb: 64, tier: "premium" },
    { name: "Mac Studio M2 Max (32GB)", ram_gb: 32, tier: "premium" },
    { name: "Mac Studio M2 Ultra (64GB+)", ram_gb: 64, tier: "premium" },
    { name: "Mac Studio M4 Max (36GB+)", ram_gb: 36, tier: "premium" },
    { name: "Mac Pro M2 Ultra (64GB+)", ram_gb: 64, tier: "premium" },
    { name: "Mac Pro (Intel, 32GB+)", ram_gb: 32, tier: "premium" },
    // ── Windows ───────────────────────────────────
    { name: "Windows Laptop (4GB RAM)", ram_gb: 4, tier: "lite" },
    { name: "Windows Laptop (8GB RAM)", ram_gb: 8, tier: "standard" },
    { name: "Windows Laptop (16GB RAM)", ram_gb: 16, tier: "premium" },
    { name: "Windows Laptop (32GB+ RAM)", ram_gb: 32, tier: "premium" },
    { name: "Windows Desktop (4GB RAM)", ram_gb: 4, tier: "lite" },
    { name: "Windows Desktop (8GB RAM)", ram_gb: 8, tier: "standard" },
    { name: "Windows Desktop (16GB RAM)", ram_gb: 16, tier: "premium" },
    { name: "Windows Desktop (32GB+ RAM)", ram_gb: 32, tier: "premium" },
    { name: "Dell XPS 13 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "Dell XPS 13 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "Dell XPS 15 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "Dell XPS 15 (32GB)", ram_gb: 32, tier: "premium" },
    { name: "HP Spectre x360 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "HP Spectre x360 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "HP Pavilion (8GB)", ram_gb: 8, tier: "standard" },
    { name: "Lenovo ThinkPad X1 Carbon (8GB)", ram_gb: 8, tier: "standard" },
    { name: "Lenovo ThinkPad X1 Carbon (16GB)", ram_gb: 16, tier: "premium" },
    { name: "Lenovo ThinkPad T14 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "Lenovo ThinkPad T14 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "Lenovo IdeaPad (4GB)", ram_gb: 4, tier: "lite" },
    { name: "Lenovo IdeaPad (8GB)", ram_gb: 8, tier: "standard" },
    { name: "ASUS ZenBook (8GB)", ram_gb: 8, tier: "standard" },
    { name: "ASUS ZenBook (16GB)", ram_gb: 16, tier: "premium" },
    { name: "ASUS ROG Gaming (16GB)", ram_gb: 16, tier: "premium" },
    { name: "ASUS ROG Gaming (32GB+)", ram_gb: 32, tier: "premium" },
    { name: "Microsoft Surface Pro (8GB)", ram_gb: 8, tier: "standard" },
    { name: "Microsoft Surface Pro (16GB)", ram_gb: 16, tier: "premium" },
    { name: "Microsoft Surface Laptop (8GB)", ram_gb: 8, tier: "standard" },
    { name: "Microsoft Surface Laptop (16GB)", ram_gb: 16, tier: "premium" },
    { name: "Acer Swift (8GB)", ram_gb: 8, tier: "standard" },
    { name: "Acer Nitro Gaming (16GB)", ram_gb: 16, tier: "premium" },
    { name: "MSI Gaming Laptop (16GB)", ram_gb: 16, tier: "premium" },
    { name: "MSI Gaming Laptop (32GB+)", ram_gb: 32, tier: "premium" },
    { name: "Razer Blade (16GB)", ram_gb: 16, tier: "premium" },
    { name: "Razer Blade (32GB+)", ram_gb: 32, tier: "premium" },
    // ── Huawei ────────────────────────────────────
    { name: "Huawei MateBook X Pro (8GB)", ram_gb: 8, tier: "standard" },
    { name: "Huawei MateBook X Pro (16GB)", ram_gb: 16, tier: "premium" },
    { name: "Huawei MateBook 14 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "Huawei MateBook D 15 (8GB)", ram_gb: 8, tier: "standard" },
    // ── Linux ─────────────────────────────────────
    { name: "Linux Desktop / Laptop (4GB)", ram_gb: 4, tier: "lite" },
    { name: "Linux Desktop / Laptop (8GB)", ram_gb: 8, tier: "standard" },
    { name: "Linux Desktop / Laptop (16GB)", ram_gb: 16, tier: "premium" },
    { name: "Linux Desktop / Laptop (32GB+)", ram_gb: 32, tier: "premium" },
    { name: "System76 Laptop (16GB)", ram_gb: 16, tier: "premium" },
    // ── Other ─────────────────────────────────────
    { name: "Chromebook (4GB)", ram_gb: 4, tier: "lite" },
    { name: "Chromebook (8GB)", ram_gb: 8, tier: "standard" },
  ],
  phones: [
    // ── Apple iPhone ──────────────────────────────
    { name: "iPhone 16 Pro Max", ram_gb: 8, tier: "standard" },
    { name: "iPhone 16 Pro", ram_gb: 8, tier: "standard" },
    { name: "iPhone 16 / 16 Plus", ram_gb: 8, tier: "standard" },
    { name: "iPhone 15 Pro Max", ram_gb: 8, tier: "standard" },
    { name: "iPhone 15 Pro", ram_gb: 8, tier: "standard" },
    { name: "iPhone 15 / 15 Plus", ram_gb: 6, tier: "lite" },
    { name: "iPhone 14 Pro / Pro Max", ram_gb: 6, tier: "lite" },
    { name: "iPhone 14 / 14 Plus", ram_gb: 6, tier: "lite" },
    { name: "iPhone 13 / 13 Mini", ram_gb: 4, tier: "lite" },
    { name: "iPhone SE (3rd gen)", ram_gb: 4, tier: "lite" },
    // ── Apple iPad ────────────────────────────────
    { name: "iPad Pro M4 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "iPad Pro M2 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "iPad Pro M2 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "iPad Air M2 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "iPad Air M3 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "iPad (10th gen, 4GB)", ram_gb: 4, tier: "lite" },
    { name: "iPad Mini (6th gen, 4GB)", ram_gb: 4, tier: "lite" },
    // ── Samsung ───────────────────────────────────
    { name: "Samsung Galaxy S25 Ultra", ram_gb: 12, tier: "standard" },
    { name: "Samsung Galaxy S25 / S25+", ram_gb: 12, tier: "standard" },
    { name: "Samsung Galaxy S24 Ultra", ram_gb: 12, tier: "standard" },
    { name: "Samsung Galaxy S24 / S24+", ram_gb: 8, tier: "standard" },
    { name: "Samsung Galaxy S23 Ultra", ram_gb: 12, tier: "standard" },
    { name: "Samsung Galaxy S23 / S23+", ram_gb: 8, tier: "standard" },
    { name: "Samsung Galaxy Z Fold 5", ram_gb: 12, tier: "standard" },
    { name: "Samsung Galaxy Z Fold 6", ram_gb: 12, tier: "standard" },
    { name: "Samsung Galaxy Z Flip 5 / 6", ram_gb: 8, tier: "standard" },
    { name: "Samsung Galaxy A55 / A54", ram_gb: 8, tier: "standard" },
    { name: "Samsung Galaxy A35 / A34", ram_gb: 6, tier: "lite" },
    { name: "Samsung Galaxy A15", ram_gb: 4, tier: "lite" },
    { name: "Samsung Galaxy Tab S9 Ultra", ram_gb: 16, tier: "premium" },
    { name: "Samsung Galaxy Tab S9 / S9+", ram_gb: 12, tier: "standard" },
    { name: "Samsung Galaxy Tab A9", ram_gb: 4, tier: "lite" },
    // ── Google ────────────────────────────────────
    { name: "Google Pixel 9 Pro / Pro XL", ram_gb: 16, tier: "premium" },
    { name: "Google Pixel 9", ram_gb: 12, tier: "standard" },
    { name: "Google Pixel 8 Pro", ram_gb: 12, tier: "standard" },
    { name: "Google Pixel 8 / 8a", ram_gb: 8, tier: "standard" },
    { name: "Google Pixel 7 Pro", ram_gb: 12, tier: "standard" },
    { name: "Google Pixel 7 / 7a", ram_gb: 8, tier: "standard" },
    // ── Huawei ────────────────────────────────────
    { name: "Huawei Mate 60 Pro+", ram_gb: 16, tier: "premium" },
    { name: "Huawei Mate 60 Pro", ram_gb: 12, tier: "standard" },
    { name: "Huawei Mate 60", ram_gb: 12, tier: "standard" },
    { name: "Huawei P60 Pro", ram_gb: 8, tier: "standard" },
    { name: "Huawei P60", ram_gb: 8, tier: "standard" },
    { name: "Huawei Nova 12 / 11", ram_gb: 8, tier: "standard" },
    { name: "Huawei MatePad Pro 13.2", ram_gb: 16, tier: "premium" },
    { name: "Huawei MatePad 11.5", ram_gb: 8, tier: "standard" },
    // ── Xiaomi ────────────────────────────────────
    { name: "Xiaomi 15 Pro", ram_gb: 16, tier: "premium" },
    { name: "Xiaomi 15", ram_gb: 12, tier: "standard" },
    { name: "Xiaomi 14 Ultra", ram_gb: 16, tier: "premium" },
    { name: "Xiaomi 14 / 14 Pro", ram_gb: 12, tier: "standard" },
    { name: "Xiaomi 13 / 13 Pro", ram_gb: 12, tier: "standard" },
    { name: "Redmi Note 13 Pro", ram_gb: 8, tier: "standard" },
    { name: "Redmi Note 13", ram_gb: 6, tier: "lite" },
    { name: "Redmi 13", ram_gb: 4, tier: "lite" },
    // ── OnePlus ───────────────────────────────────
    { name: "OnePlus 13", ram_gb: 16, tier: "premium" },
    { name: "OnePlus 12", ram_gb: 16, tier: "premium" },
    { name: "OnePlus 11", ram_gb: 16, tier: "premium" },
    { name: "OnePlus Nord 4 / CE 4", ram_gb: 8, tier: "standard" },
    // ── Other ─────────────────────────────────────
    { name: "Sony Xperia 1 VI", ram_gb: 12, tier: "standard" },
    { name: "Motorola Edge 50 Pro", ram_gb: 12, tier: "standard" },
    { name: "Nothing Phone (2)", ram_gb: 12, tier: "standard" },
    { name: "OPPO Find X7 Ultra", ram_gb: 16, tier: "premium" },
    { name: "OPPO Reno 12", ram_gb: 8, tier: "standard" },
    { name: "vivo X100 Pro", ram_gb: 16, tier: "premium" },
    { name: "Realme GT 5 Pro", ram_gb: 16, tier: "premium" },
  ],
};

const MODEL_INFO = {
  lite: { name: "Lite (Qwen2.5-3B)", size: "2.0 GB", ram: "4GB", color: "#757575" },
  standard: { name: "Standard (Qwen2.5-7B)", size: "4.4 GB", ram: "8GB", color: "#c62828" },
  premium: { name: "Premium (Qwen2.5-14B)", size: "8.5 GB", ram: "16GB", color: "#1565c0" },
};

let selectedDeviceType = null;

/**
 * User selects device type (computer or phone)
 */
function checkerSelectType(type) {
  selectedDeviceType = type;

  // Highlight selected button
  document.querySelectorAll(".checker-option").forEach((btn) => {
    btn.classList.toggle("selected", btn.dataset.type === type);
  });

  // Populate device dropdown
  const selectEl = document.getElementById("checkerDevice");
  selectEl.innerHTML = `<option value="">${t("checker_choose")}</option>`;

  const presets = DEVICE_PRESETS[type === "computer" ? "computers" : "phones"];
  presets.forEach((device, i) => {
    const opt = document.createElement("option");
    opt.value = i;
    opt.textContent = device.name;
    selectEl.appendChild(opt);
  });

  // Show step 2
  document.getElementById("checkerStep2").classList.remove("hidden");
}

/**
 * Analyze device and show recommendation
 */
function checkerAnalyze() {
  let ram = 0;
  let tier = "lite";

  // Check if a device was selected from dropdown
  const deviceSelect = document.getElementById("checkerDevice");
  const ramSelect = document.getElementById("checkerRam");

  if (deviceSelect.value) {
    const presets = DEVICE_PRESETS[selectedDeviceType === "computer" ? "computers" : "phones"];
    const device = presets[parseInt(deviceSelect.value)];
    if (device) {
      ram = device.ram_gb;
      tier = device.tier;
    }
  } else if (ramSelect.value) {
    ram = parseInt(ramSelect.value);
    if (ram >= 16) tier = "premium";
    else if (ram >= 8) tier = "standard";
    else tier = "lite";
  } else {
    // Nothing selected — show a hint
    deviceSelect.style.borderColor = "#e17055";
    setTimeout(() => { deviceSelect.style.borderColor = ""; }, 2000);
    return;
  }

  // Determine result type and styling
  let resultClass, icon, title, desc;

  if (ram >= 16) {
    resultClass = "compatible";
    icon = "🎉";
    title = t("checker_result_great");
    desc = t("checker_result_great_desc");
  } else if (ram >= 8) {
    resultClass = "compatible";
    icon = "✅";
    title = t("checker_result_good");
    desc = t("checker_result_standard_desc");
  } else if (ram >= 4) {
    resultClass = "limited";
    icon = "⚠️";
    title = t("checker_result_good");
    desc = t("checker_result_lite_desc");
  } else {
    resultClass = "incompatible";
    icon = "❌";
    title = t("checker_result_low");
    desc = t("checker_result_low_desc");
  }

  const modelInfo = MODEL_INFO[tier];

  // Show result
  const resultCard = document.getElementById("checkerResultCard");
  resultCard.className = `checker-result-card ${resultClass}`;
  resultCard.innerHTML = `
    <div class="checker-result-icon">${icon}</div>
    <div class="checker-result-title">${title}</div>
    <div class="checker-result-desc">${desc}</div>
    <p style="margin-bottom: 8px; color: var(--text-muted); font-size: 0.9rem;">
      ${t("checker_result_recommend")}
    </p>
    <div class="checker-result-model" style="border-left: 3px solid ${modelInfo.color}; padding-left: 16px;">
      ${modelInfo.name} — ${modelInfo.size}
    </div>
  `;

  document.getElementById("checkerStep1").classList.add("hidden");
  document.getElementById("checkerStep2").classList.add("hidden");
  document.getElementById("checkerResult").classList.remove("hidden");
}

/**
 * Reset the checker to start over
 */
function checkerReset() {
  selectedDeviceType = null;
  document.getElementById("checkerStep1").classList.remove("hidden");
  document.getElementById("checkerStep2").classList.add("hidden");
  document.getElementById("checkerResult").classList.add("hidden");
  document.getElementById("checkerDevice").value = "";
  document.getElementById("checkerRam").value = "";
  document.querySelectorAll(".checker-option").forEach((btn) => {
    btn.classList.remove("selected");
  });
}
