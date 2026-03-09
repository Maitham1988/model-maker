/* ═══════════════════════════════════════════════════════════════
   AI Chat — Client Application
   Handles: chat, conversations, streaming, settings, i18n
   ═══════════════════════════════════════════════════════════════ */

const API = "/api";

// ─── State ───────────────────────────────────────────────────────
let currentConversationId = null;
let isStreaming = false;
let currentUILang = "en";

// ─── DOM Elements ────────────────────────────────────────────────
const $ = (sel) => document.querySelector(sel);
const messagesEl = $("#messages");
const emptyStateEl = $("#emptyState");
const inputEl = $("#messageInput");
const sendBtn = $("#sendBtn");
const convListEl = $("#conversationList");

// ─── i18n (Internationalization) ─────────────────────────────────
function t(key, params = {}) {
  const lang = TRANSLATIONS[currentUILang] || TRANSLATIONS.en;
  let str = lang[key] || TRANSLATIONS.en[key] || key;
  for (const [k, v] of Object.entries(params)) {
    str = str.replace(`{${k}}`, v);
  }
  return str;
}

function applyLanguage(langCode) {
  if (!TRANSLATIONS[langCode]) langCode = "en";
  currentUILang = langCode;

  const lang = TRANSLATIONS[langCode];
  document.documentElement.lang = langCode;
  document.documentElement.dir = lang.dir;

  // Update all data-i18n elements
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (lang[key]) el.textContent = lang[key];
  });

  // Update placeholders
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (lang[key]) el.placeholder = lang[key];
  });

  // Update page title
  document.title = lang.emptyTitle || "AI Chat";

  localStorage.setItem("ui_language", langCode);
}

function populateLanguageSelector() {
  const select = $("#settingsLanguage");
  select.innerHTML = "";
  for (const [code, lang] of Object.entries(TRANSLATIONS)) {
    const opt = document.createElement("option");
    opt.value = code;
    opt.textContent = lang.name;
    select.appendChild(opt);
  }
}

// ─── Initialize ──────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", async () => {
  // Auto-setup if not done (no wizard needed)
  const config = await fetchJSON(`${API}/config`);
  if (config && !config.setup_completed) {
    await fetchJSON(`${API}/setup`, {
      method: "POST",
      body: JSON.stringify({}),
    });
  }

  // Apply saved UI language
  const savedLang = localStorage.getItem("ui_language") || "en";
  populateLanguageSelector();
  applyLanguage(savedLang);

  await loadConversations();
  inputEl.focus();
});

// ─── API Helpers ─────────────────────────────────────────────────
async function fetchJSON(url, options = {}) {
  try {
    const res = await fetch(url, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (e) {
    console.error("API Error:", e);
    return null;
  }
}

// ─── Conversations ───────────────────────────────────────────────
async function loadConversations() {
  const convs = await fetchJSON(`${API}/conversations`);
  if (!convs) return;

  convListEl.innerHTML = "";
  convs.forEach((conv) => {
    const el = document.createElement("div");
    el.className = `conv-item${conv.id === currentConversationId ? " active" : ""}`;
    el.innerHTML = `
            <span class="conv-title">${escapeHtml(conv.title)}</span>
            <span class="conv-actions">
                <button onclick="event.stopPropagation(); renameConversation('${conv.id}')" title="Rename">✎</button>
                <button onclick="event.stopPropagation(); deleteConversation('${conv.id}')" title="Delete">🗑</button>
            </span>
        `;
    el.addEventListener("click", () => openConversation(conv.id));
    convListEl.appendChild(el);
  });
}

async function newChat() {
  const conv = await fetchJSON(`${API}/conversations`, {
    method: "POST",
    body: JSON.stringify({ title: t("newChat") }),
  });
  if (!conv) return;
  currentConversationId = conv.id;
  showChatView([]);
  await loadConversations();
  inputEl.focus();
  closeSidebar();
}

async function openConversation(convId) {
  currentConversationId = convId;
  const messages = await fetchJSON(`${API}/conversations/${convId}/messages`);
  showChatView(messages || []);
  await loadConversations();
  closeSidebar();
}

async function renameConversation(convId) {
  const newTitle = prompt(t("renamePrompt"));
  if (!newTitle || !newTitle.trim()) return;
  await fetchJSON(`${API}/conversations/${convId}`, {
    method: "PUT",
    body: JSON.stringify({ title: newTitle.trim() }),
  });
  await loadConversations();
}

async function deleteConversation(convId) {
  if (!confirm(t("confirmDelete"))) return;
  await fetchJSON(`${API}/conversations/${convId}`, { method: "DELETE" });
  if (currentConversationId === convId) {
    currentConversationId = null;
    showEmptyState();
  }
  await loadConversations();
}

// ─── Chat View ───────────────────────────────────────────────────
function showChatView(messages) {
  emptyStateEl.style.display = "none";
  messagesEl.classList.add("active");
  messagesEl.innerHTML = "";

  messages.forEach((msg) => {
    if (msg.role === "system") return;
    appendMessage(msg.role, msg.content);
  });

  scrollToBottom();
}

function showEmptyState() {
  emptyStateEl.style.display = "flex";
  messagesEl.classList.remove("active");
  messagesEl.innerHTML = "";
}

function appendMessage(role, content) {
  const msgEl = document.createElement("div");
  msgEl.className = `message ${role}`;

  const avatarLabel = role === "user" ? "Y" : "✦";
  const dir = detectDirection(content);

  const shareBtn = role === "assistant" ? `
        <div class="message-actions">
            <button class="msg-action-btn" onclick="copyMessage(this)" title="${t('copyMessage')}">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>
            </button>
            <button class="msg-action-btn" onclick="shareMessage(this)" title="${t('shareMessage')}">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
            </button>
        </div>` : "";

  msgEl.innerHTML = `
        <div class="message-avatar">${avatarLabel}</div>
        <div class="message-content" dir="${dir}">${formatContent(content)}</div>
        ${shareBtn}
    `;
  messagesEl.appendChild(msgEl);
  return msgEl;
}

function appendStreamingMessage() {
  const msgEl = document.createElement("div");
  msgEl.className = "message assistant";
  msgEl.id = "streaming-message";
  msgEl.innerHTML = `
        <div class="message-avatar">✦</div>
        <div class="message-content">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
    `;
  messagesEl.appendChild(msgEl);
  scrollToBottom();
  return msgEl;
}

function updateStreamingMessage(msgEl, content) {
  const contentEl = msgEl.querySelector(".message-content");
  const dir = detectDirection(content);
  contentEl.setAttribute("dir", dir);
  contentEl.innerHTML = formatContent(content);
  scrollToBottom();
}

function scrollToBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

// ─── Send Message ────────────────────────────────────────────────
async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text || isStreaming) return;

  // Create conversation if needed
  if (!currentConversationId) {
    const conv = await fetchJSON(`${API}/conversations`, {
      method: "POST",
      body: JSON.stringify({ title: t("newChat") }),
    });
    if (!conv) return;
    currentConversationId = conv.id;
    emptyStateEl.style.display = "none";
    messagesEl.classList.add("active");
  }

  // Clear input
  inputEl.value = "";
  inputEl.style.height = "auto";

  // Show user message
  appendMessage("user", text);
  scrollToBottom();

  // Start streaming
  isStreaming = true;
  sendBtn.disabled = true;
  const streamEl = appendStreamingMessage();

  let fullResponse = "";

  try {
    const res = await fetch(`${API}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        conversation_id: currentConversationId,
        message: text,
      }),
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // Process SSE lines
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const data = line.slice(6).trim();
        if (!data) continue;

        try {
          const parsed = JSON.parse(data);
          if (parsed.token) {
            fullResponse += parsed.token;
            updateStreamingMessage(streamEl, fullResponse);
          }
          if (parsed.done) {
            await loadConversations();
          }
        } catch (e) {
          // Skip malformed JSON
        }
      }
    }
  } catch (e) {
    fullResponse = "Error: Could not get response. Is the model loaded?";
    updateStreamingMessage(streamEl, fullResponse);
  }

  streamEl.removeAttribute("id");
  isStreaming = false;
  sendBtn.disabled = false;
  inputEl.focus();
}

// ─── Input Handling ──────────────────────────────────────────────
function handleKeyDown(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function autoResize(el) {
  el.style.height = "auto";
  el.style.height = Math.min(el.scrollHeight, 200) + "px";
}

// ─── Settings ────────────────────────────────────────────────────
async function openSettings() {
  // Set language selector to current
  $("#settingsLanguage").value = currentUILang;

  // Load memory count
  const memories = await fetchJSON(`${API}/memory`);
  updateMemoryCount(memories ? memories.length : 0);

  $("#settingsModal").classList.remove("hidden");
}

function closeSettings() {
  $("#settingsModal").classList.add("hidden");
}

function saveSettings() {
  const lang = $("#settingsLanguage").value;
  applyLanguage(lang);
  closeSettings();
}

function updateMemoryCount(count) {
  const el = $("#memoryCount");
  const clearBtn = $("#clearMemoryBtn");
  if (count === 0) {
    el.textContent = t("noMemories");
    if (clearBtn) clearBtn.style.display = "none";
  } else {
    el.textContent = t("memoriesStored", { n: count });
    if (clearBtn) clearBtn.style.display = "inline-flex";
  }
}

async function clearAllMemory() {
  if (!confirm(t("confirmClearMemory"))) return;
  const memories = await fetchJSON(`${API}/memory`);
  if (memories) {
    for (const m of memories) {
      await fetchJSON(`${API}/memory/${m.id}`, { method: "DELETE" });
    }
  }
  const updated = await fetchJSON(`${API}/memory`);
  updateMemoryCount(updated ? updated.length : 0);
}

// ─── Sidebar Toggle (Mobile) ────────────────────────────────────
function toggleSidebar() {
  $("#sidebar").classList.toggle("open");
}

function closeSidebar() {
  $("#sidebar").classList.remove("open");
}

// ─── Utilities ───────────────────────────────────────────────────
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function detectDirection(text) {
  const rtlRegex =
    /[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\u0590-\u05FF]/;
  const first100 = text.substring(0, 100);
  const rtlChars = (first100.match(rtlRegex) || []).length;
  const totalAlpha = (first100.match(/[a-zA-Z\u0600-\u06FF]/g) || []).length;
  return totalAlpha > 0 && rtlChars / totalAlpha > 0.3 ? "rtl" : "ltr";
}

function formatContent(text) {
  let html = escapeHtml(text);
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, "<pre><code>$2</code></pre>");
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  html = html.replace(/\n\n/g, "</p><p>");
  html = html.replace(/\n/g, "<br>");
  html = `<p>${html}</p>`;
  return html;
}

// ─── Share & Copy Features ───────────────────────────────────────

function copyMessage(btn) {
  const msgEl = btn.closest(".message");
  const content = msgEl.querySelector(".message-content").innerText;
  navigator.clipboard.writeText(content).then(() => {
    showToast(t("copied"));
    btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00b894" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>`;
    setTimeout(() => {
      btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>`;
    }, 2000);
  });
}

function shareMessage(btn) {
  const msgEl = btn.closest(".message");
  const content = msgEl.querySelector(".message-content").innerText;

  // Try native share API first (mobile & some desktops)
  if (navigator.share) {
    navigator.share({
      title: "Model Maker — AI Knowledge",
      text: content,
      url: "https://github.com/Maitham1988/model-maker",
    }).catch(() => {});
    return;
  }

  // Fallback: copy with context
  const shareText = `💡 AI Knowledge from Model Maker:\n\n${content}\n\n—\n🏥 Model Maker — Free Offline AI\nhttps://github.com/Maitham1988/model-maker`;
  navigator.clipboard.writeText(shareText).then(() => {
    showToast(t("copiedForSharing"));
  });
}

async function shareConversation() {
  if (!currentConversationId) return;

  const messages = await fetchJSON(`${API}/conversations/${currentConversationId}/messages`);
  if (!messages || messages.length === 0) {
    showToast(t("noMessagesToShare"));
    return;
  }

  let text = `🏥 Model Maker — Conversation Export\n${"─".repeat(40)}\n\n`;

  for (const msg of messages) {
    const role = msg.role === "user" ? "👤 You" : "🤖 AI";
    text += `${role}:\n${msg.content}\n\n`;
  }

  text += `${"─".repeat(40)}\n🏥 Model Maker — Free Offline AI for Everyone\nhttps://github.com/Maitham1988/model-maker\n`;

  if (navigator.share) {
    navigator.share({ title: "Model Maker Conversation", text }).catch(() => {});
    return;
  }

  // Fallback: download as text file
  const blob = new Blob([text], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `model-maker-chat-${new Date().toISOString().slice(0, 10)}.txt`;
  a.click();
  URL.revokeObjectURL(url);
  showToast(t("conversationExported"));
}

function showToast(message) {
  // Remove existing toast
  const existing = document.querySelector(".toast");
  if (existing) existing.remove();

  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  document.body.appendChild(toast);

  // Animate in
  requestAnimationFrame(() => {
    toast.classList.add("show");
    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 300);
    }, 2500);
  });
}

// ─── Voice Chat ─────────────────────────────────────────────────────

let voiceAvailable = false;
let isRecording = false;
let isProcessingVoice = false;
let mediaRecorder = null;
let audioChunks = [];
let recordingStartTime = null;
let voiceTimerInterval = null;

// Check if voice is available on page load
async function checkVoiceStatus() {
  try {
    const res = await fetch("/api/voice/status");
    const data = await res.json();
    voiceAvailable = data.available;
    const btn = document.getElementById("voiceBtn");
    if (btn) {
      btn.classList.toggle("hidden", !voiceAvailable);
    }
  } catch (e) {
    voiceAvailable = false;
  }
}

function toggleVoice() {
  if (isProcessingVoice) return;
  if (isRecording) {
    stopRecording();
  } else {
    startRecording();
  }
}

async function startRecording() {
  if (isRecording || isProcessingVoice) return;

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: {
        channelCount: 1,
        sampleRate: 16000,
        echoCancellation: true,
        noiseSuppression: true,
      },
    });

    audioChunks = [];
    mediaRecorder = new MediaRecorder(stream, {
      mimeType: MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
        ? "audio/webm;codecs=opus"
        : "audio/webm",
    });

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) audioChunks.push(e.data);
    };

    mediaRecorder.onstop = () => {
      // Stop all tracks
      stream.getTracks().forEach((t) => t.stop());
      // Process the recorded audio
      processVoiceChat();
    };

    mediaRecorder.start(100); // Collect data every 100ms
    isRecording = true;
    recordingStartTime = Date.now();

    // Update UI
    const btn = document.getElementById("voiceBtn");
    btn.classList.add("recording");
    const status = document.getElementById("voiceStatus");
    status.classList.add("active");
    status.classList.remove("processing");
    document.getElementById("voiceLabel").textContent = "Listening...";
    document.getElementById("voiceTimer").textContent = "0:00";

    // Start timer
    voiceTimerInterval = setInterval(updateVoiceTimer, 1000);
  } catch (err) {
    console.error("Microphone access denied:", err);
    showToast("Microphone access denied. Please allow microphone in browser settings.");
  }
}

function stopRecording() {
  if (!isRecording || !mediaRecorder) return;
  isRecording = false;
  clearInterval(voiceTimerInterval);
  mediaRecorder.stop();

  // Update button
  const btn = document.getElementById("voiceBtn");
  btn.classList.remove("recording");
  btn.classList.add("processing");

  // Update status
  const status = document.getElementById("voiceStatus");
  status.classList.add("processing");
  document.getElementById("voiceLabel").textContent = "Processing...";
}

function cancelVoice() {
  if (mediaRecorder && isRecording) {
    isRecording = false;
    clearInterval(voiceTimerInterval);
    mediaRecorder.stream.getTracks().forEach((t) => t.stop());
    mediaRecorder = null;
    audioChunks = [];
  }
  isProcessingVoice = false;

  // Reset UI
  const btn = document.getElementById("voiceBtn");
  btn.classList.remove("recording", "processing");
  const status = document.getElementById("voiceStatus");
  status.classList.remove("active", "processing");
}

function updateVoiceTimer() {
  if (!recordingStartTime) return;
  const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
  const min = Math.floor(elapsed / 60);
  const sec = elapsed % 60;
  document.getElementById("voiceTimer").textContent =
    `${min}:${sec.toString().padStart(2, "0")}`;
}

async function processVoiceChat() {
  if (audioChunks.length === 0) {
    cancelVoice();
    return;
  }

  isProcessingVoice = true;
  const status = document.getElementById("voiceStatus");
  document.getElementById("voiceLabel").textContent = "Transcribing...";

  // Create audio blob
  const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
  audioChunks = [];

  // Ensure we have a conversation
  if (!currentConversation) {
    await createNewConversation();
  }

  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.webm");
  formData.append("conversation_id", currentConversation || "");

  try {
    document.getElementById("voiceLabel").textContent = "Thinking...";

    const res = await fetch("/api/voice/chat", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Voice processing failed" }));
      throw new Error(err.detail || "Voice processing failed");
    }

    // Get metadata from headers
    const userText = res.headers.get("X-User-Text") || "";
    const responseText = res.headers.get("X-Response-Text") || "";
    const convId = res.headers.get("X-Conversation-Id");
    const sttMs = res.headers.get("X-STT-Ms") || "?";
    const llmMs = res.headers.get("X-LLM-Ms") || "?";
    const ttsMs = res.headers.get("X-TTS-Ms") || "?";
    const totalMs = res.headers.get("X-Total-Ms") || "?";

    if (convId) currentConversation = convId;

    // Show user message in chat
    if (userText) {
      addMessageToChat("user", "🎤 " + userText);
    }

    // Show assistant message in chat
    if (responseText) {
      addMessageToChat("assistant", responseText);
    }

    // Play audio response
    document.getElementById("voiceLabel").textContent = "Speaking...";
    const audioBytes = await res.arrayBuffer();
    await playAudioResponse(audioBytes);

    console.log(`Voice: STT=${sttMs}ms LLM=${llmMs}ms TTS=${ttsMs}ms Total=${totalMs}ms`);

    // Refresh conversation list
    loadConversations();
  } catch (err) {
    console.error("Voice chat error:", err);
    showToast(err.message || "Voice chat failed");
  } finally {
    isProcessingVoice = false;
    // Reset UI
    const btn = document.getElementById("voiceBtn");
    btn.classList.remove("recording", "processing");
    status.classList.remove("active", "processing");
  }
}

function addMessageToChat(role, content) {
  const messagesDiv = document.getElementById("messages");
  const emptyState = document.getElementById("emptyState");
  if (emptyState) emptyState.style.display = "none";

  const msgDiv = document.createElement("div");
  msgDiv.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "message-content";
  bubble.textContent = content;

  msgDiv.appendChild(bubble);
  messagesDiv.appendChild(msgDiv);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function playAudioResponse(arrayBuffer) {
  return new Promise((resolve, reject) => {
    try {
      const blob = new Blob([arrayBuffer], { type: "audio/wav" });
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      audio.onended = () => {
        URL.revokeObjectURL(url);
        resolve();
      };
      audio.onerror = (e) => {
        URL.revokeObjectURL(url);
        reject(e);
      };
      audio.play().catch(reject);
    } catch (e) {
      reject(e);
    }
  });
}

// Check voice on startup
document.addEventListener("DOMContentLoaded", () => {
  checkVoiceStatus();
});