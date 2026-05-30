// home.js — content rendering + interactions
// Pulls publications from data.js, splits into 4 curated categories,
// hooks up theme toggle, scroll fade-ins.

(function () {
  "use strict";

  const D = window.SITE_DATA;

  // ── Group EVERY publication by theme ───────────────────────────────────
  function shortVenue(v) {
    if (!v) return "";
    return v.split("·")[0].split(",")[0].trim();
  }

  const BUCKETS = [
    { key: "vlm",     match: t => t.includes("vlm") },
    { key: "fewshot", match: t => t.includes("few-shot") || t.includes("meta") || t.includes("continual") },
    { key: "adapt",   match: t => t.includes("finetune") || t.includes("ssl") || t.includes("systems") },
    { key: "vision",  match: t => t.includes("dynamical") || t.includes("detection") },
  ];

  function bucketFor(pub) {
    const tags = pub.tags || [];
    for (const b of BUCKETS) {
      if (b.match(tags)) return b.key;
    }
    return "vision";
  }

  const grouped = { vlm: [], fewshot: [], adapt: [], vision: [] };
  (D.publications || [])
    .filter(p => p.type !== "thesis")
    .forEach(p => { grouped[bucketFor(p)].push(p); });

  // ── Render each theme column (all papers, newest first) ─────────────────
  Object.entries(grouped).forEach(([key, list]) => {
    const catEl = document.querySelector(`.pub-cat[data-cat="${key}"]`);
    if (!catEl) return;
    const listEl = catEl.querySelector(".pub-list");
    const countEl = catEl.querySelector("[data-count]");

    list.sort((a, b) => b.y - a.y);
    if (countEl) countEl.textContent = `${list.length} paper${list.length === 1 ? "" : "s"}`;

    list.forEach(p => {
      const row = document.createElement("a");
      const hasUrl = p.url && p.url !== "#";
      row.href = hasUrl ? p.url : "#";
      if (hasUrl) {
        row.target = "_blank";
        row.rel = "noopener";
      }
      row.className = "pub-row";
      row.innerHTML =
        `<span class="year mono">${p.y}</span>` +
        `<span class="title">${p.t}</span>` +
        `<span class="venue">${shortVenue(p.v)}</span>`;
      listEl.appendChild(row);
    });
  });

  // ── Hero proof metrics (counts from single-source data) ────────────────
  (function fillMetrics() {
    const pubEl = document.querySelector('[data-metric="pubs"]');
    const patEl = document.querySelector('[data-metric="patents"]');
    if (pubEl && Array.isArray(D.publications)) {
      const n = D.publications.filter(p => p.type !== "thesis").length;
      const floor5 = Math.floor(n / 5) * 5;
      pubEl.innerHTML = floor5 + '<span class="unit">+</span>';
    }
    if (patEl && Array.isArray(D.patents)) {
      patEl.textContent = D.patents.length;
    }
  })();

  // ── Patents (collapsible list, newest first) ───────────────────────────
  (function fillPatents() {
    if (!Array.isArray(D.patents)) return;
    const countEl = document.querySelector("[data-pat-count]");
    const listEl = document.querySelector("[data-pat-list]");
    if (countEl) countEl.textContent = D.patents.length;
    if (listEl) {
      D.patents.slice().sort((a, b) => b.y - a.y).forEach(p => {
        const row = document.createElement("a");
        const hasUrl = p.url && p.url !== "#";
        row.href = hasUrl ? p.url : "#";
        if (hasUrl) { row.target = "_blank"; row.rel = "noopener"; }
        row.className = "pt-row";
        row.innerHTML =
          `<span class="pt-num mono">${p.num}</span>` +
          `<span class="pt-title">${p.t}</span>` +
          `<span class="pt-yr mono">${p.y}</span>`;
        listEl.appendChild(row);
      });
    }
    const disc = document.querySelector("details.patents");
    if (disc) {
      const tog = disc.querySelector(".pt-toggle");
      disc.addEventListener("toggle", () => {
        if (tog) tog.textContent = disc.open ? "Hide" : "View list";
      });
    }
  })();

  // ── Theme toggle ───────────────────────────────────────────────────────
  const root = document.documentElement;
  const toggle = document.getElementById("theme-toggle");
  const iconEl = document.getElementById("theme-icon");

  const ICONS = {
    dark: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>',
    light: '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>',
  };

  function setTheme(t) {
    root.setAttribute("data-theme", t);
    if (iconEl) iconEl.innerHTML = (t === "dark") ? ICONS.dark : ICONS.light;
    try { localStorage.setItem("home-theme", t); } catch (e) {}
  }

  let saved = null;
  try { saved = localStorage.getItem("home-theme"); } catch (e) {}
  if (saved === "light" || saved === "dark") setTheme(saved);
  else setTheme("dark");

  if (toggle) {
    toggle.addEventListener("click", () => {
      const cur = root.getAttribute("data-theme");
      setTheme(cur === "dark" ? "light" : "dark");
    });
  }

  // ── Scroll fade-ins ────────────────────────────────────────────────────
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add("in");
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -60px 0px" });

  document.querySelectorAll("[data-fade]").forEach(el => io.observe(el));

  // ── Smooth anchor scroll ───────────────────────────────────────────────
  document.addEventListener("click", (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a) return;
    const id = a.getAttribute("href").slice(1);
    if (!id) return;
    const target = document.getElementById(id);
    if (!target) return;
    e.preventDefault();
    const top = target.getBoundingClientRect().top + window.scrollY - 64;
    window.scrollTo({ top, behavior: "smooth" });
    history.replaceState(null, "", "#" + id);
  });
})();
