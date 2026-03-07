/* ──────────────────────────────────────────────────────────────
   Model Maker Website — Main JavaScript
   Navigation, animations, smooth scroll, interactions
   ────────────────────────────────────────────────────────────── */

document.addEventListener("DOMContentLoaded", () => {
  initNavbar();
  initSmoothScroll();
  initScrollAnimations();
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

// ── Scroll animations (fade in on scroll) ────────────────────

function initScrollAnimations() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("animate-in");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: "0px 0px -50px 0px" }
  );

  // Observe cards and sections
  document.querySelectorAll(
    ".why-card, .feature-card, .model-card, .community-card, .download-step"
  ).forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(30px)";
    el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
    observer.observe(el);
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
      btn.style.borderColor = "var(--accent-primary)";
      btn.style.background = "rgba(108, 92, 231, 0.1)";
    }
  });
}

// ── Animate numbers on scroll ────────────────────────────────

function animateNumber(element, target, suffix = "") {
  const duration = 1500;
  const start = 0;
  const startTime = performance.now();

  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
    const current = Math.round(start + (target - start) * eased);

    element.textContent = current + suffix;

    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }

  requestAnimationFrame(update);
}
