/* ──────────────────────────────────────────────────────────────
   Model Maker Website — Hardware Checker
   Recommends the best model tier based on device specs
   ────────────────────────────────────────────────────────────── */

// Device presets from registry
const DEVICE_PRESETS = {
  computers: [
    { name: "MacBook Air M1/M2 (8GB)", ram_gb: 8, tier: "standard" },
    { name: "MacBook Air M2/M3 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "MacBook Pro M1/M2/M3 (16GB)", ram_gb: 16, tier: "premium" },
    { name: "MacBook Pro M2/M3 (32GB+)", ram_gb: 32, tier: "premium" },
    { name: "Windows Laptop (4GB RAM)", ram_gb: 4, tier: "lite" },
    { name: "Windows Laptop (8GB RAM)", ram_gb: 8, tier: "standard" },
    { name: "Windows Laptop (16GB RAM)", ram_gb: 16, tier: "premium" },
    { name: "Windows Desktop (8GB RAM)", ram_gb: 8, tier: "standard" },
    { name: "Windows Desktop (16GB+ RAM)", ram_gb: 16, tier: "premium" },
    { name: "Linux Desktop/Laptop", ram_gb: 8, tier: "standard" },
    { name: "Chromebook (4GB)", ram_gb: 4, tier: "lite" },
  ],
  phones: [
    { name: "iPhone 15 Pro / Pro Max", ram_gb: 8, tier: "standard" },
    { name: "iPhone 15 / 14 Pro", ram_gb: 6, tier: "lite" },
    { name: "iPhone 14 / 13", ram_gb: 6, tier: "lite" },
    { name: "Samsung Galaxy S24 Ultra", ram_gb: 12, tier: "standard" },
    { name: "Samsung Galaxy S24 / S23", ram_gb: 8, tier: "standard" },
    { name: "Samsung Galaxy A54 / A34", ram_gb: 6, tier: "lite" },
    { name: "Google Pixel 8 Pro", ram_gb: 12, tier: "standard" },
    { name: "Google Pixel 8 / 7", ram_gb: 8, tier: "standard" },
    { name: "Huawei Mate 60 Pro", ram_gb: 12, tier: "standard" },
    { name: "Huawei P60 Pro", ram_gb: 8, tier: "standard" },
    { name: "Huawei Nova 12 / 11", ram_gb: 8, tier: "standard" },
    { name: "Xiaomi 14 / 13", ram_gb: 12, tier: "standard" },
    { name: "OnePlus 12", ram_gb: 16, tier: "premium" },
    { name: "iPad Pro M2/M4", ram_gb: 16, tier: "premium" },
    { name: "iPad Air M2", ram_gb: 8, tier: "standard" },
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
