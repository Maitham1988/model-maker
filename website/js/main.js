/* ──────────────────────────────────────────────────────────────
   Model Maker Website — Main JavaScript
   Navigation, animations, smooth scroll, interactions
   ────────────────────────────────────────────────────────────── */

document.addEventListener("DOMContentLoaded", () => {
  initNavbar();
  initSmoothScroll();
  initMobileNav();
  detectPlatform();
});

// ── Navbar scroll effect ──────────────────────────────────────

function initNavbar() {
  const navbar = document.getElementById("navbar");
  let lastScroll = 0;

  window.addEventListener("scroll", () => {
    const scrollY = window.scrollY;
    navbar.classList.toggle("scrolled", scrollY > 50);
    lastScroll = scrollY;
  }, { passive: true });
}

// ── Smooth scroll for anchor links ───────────────────────────

function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (e) => {
      const targetId = link.getAttribute("href");
      if (targetId === "#") return;

      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const navHeight = document.getElementById("navbar").offsetHeight;
        const targetPos = target.getBoundingClientRect().top + window.scrollY - navHeight - 20;

        window.scrollTo({
          top: targetPos,
          behavior: "smooth",
        });

        // Close mobile nav if open
        document.getElementById("navLinks")?.classList.remove("active");
      }
    });
  });
}

// ── Mobile navigation toggle ─────────────────────────────────

function initMobileNav() {
  const toggle = document.getElementById("navToggle");
  const links = document.getElementById("navLinks");

  if (toggle && links) {
    toggle.addEventListener("click", () => {
      links.classList.toggle("active");
      // Animate hamburger
      toggle.classList.toggle("active");
    });

    // Close on outside click
    document.addEventListener("click", (e) => {
      if (!toggle.contains(e.target) && !links.contains(e.target)) {
        links.classList.remove("active");
        toggle.classList.remove("active");
      }
    });
  }
}

// ── Auto-detect platform for download section ────────────────

function detectPlatform() {
  const ua = navigator.userAgent.toLowerCase();
  let platform = "linux";

  if (ua.includes("mac") || ua.includes("iphone") || ua.includes("ipad")) {
    platform = "mac";
  } else if (ua.includes("win")) {
    platform = "windows";
  }

  // Highlight user's platform button
  document.querySelectorAll(".platform-btn").forEach((btn) => {
    if (btn.dataset.platform === platform) {
      btn.style.borderColor = "var(--emergency-red)";
      btn.style.background = "rgba(198, 40, 40, 0.06)";
    }
  });
}

// ── Copy install command ─────────────────────────────────────

function copyInstallCmd(el) {
  const code = el.querySelector("code");
  if (!code) return;

  const text = code.textContent.trim();
  navigator.clipboard.writeText(text).then(() => {
    const btn = el.querySelector(".download-copy-btn span");
    if (btn) {
      const orig = btn.textContent;
      btn.textContent = "Copied!";
      el.style.boxShadow = "0 0 0 2px #34c759";
      setTimeout(() => {
        btn.textContent = orig;
        el.style.boxShadow = "";
      }, 2000);
    }
  }).catch(() => {
    // Fallback: select the text
    const range = document.createRange();
    range.selectNodeContents(code);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  });
}


