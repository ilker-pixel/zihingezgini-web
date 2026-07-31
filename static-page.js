(() => {
  const storage = {
    get(key, fallback) {
      try {
        const value = localStorage.getItem(key);
        return value === null ? fallback : JSON.parse(value);
      } catch (_) {
        return fallback;
      }
    },
    set(key, value) {
      try {
        localStorage.setItem(key, JSON.stringify(value));
      } catch (_) {
        // The page remains usable when storage is disabled.
      }
    }
  };

  function applyTheme(theme) {
    const isDark = theme === "dark";
    document.documentElement.classList.toggle("dark-theme", isDark);
    document.documentElement.classList.toggle("light-theme", !isDark);
    document.body.classList.toggle("dark-theme", isDark);
    document.documentElement.style.colorScheme = isDark ? "dark" : "light";
    document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
      button.textContent = isDark ? "☀" : "◐";
      const label = isDark ? "Gündüz moduna geç" : "Gece moduna geç";
      button.title = label;
      button.setAttribute("aria-label", label);
    });
  }

  const savedTheme = (() => {
    try {
      return localStorage.getItem("zg_theme") || "light";
    } catch (_) {
      return "light";
    }
  })();
  applyTheme(savedTheme);

  document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const next = document.body.classList.contains("dark-theme") ? "light" : "dark";
      try {
        localStorage.setItem("zg_theme", next);
      } catch (_) {
        // Keep the current page theme even if persistence is unavailable.
      }
      applyTheme(next);
    });
  });

  document.querySelectorAll("[data-share]").forEach((button) => {
    button.addEventListener("click", async () => {
      const payload = { title: document.title, url: window.location.href };
      try {
        if (navigator.share) {
          await navigator.share(payload);
          return;
        }
        await navigator.clipboard.writeText(payload.url);
        button.textContent = "Bağlantı kopyalandı";
      } catch (_) {
        button.textContent = "Bağlantı adres çubuğunda";
      }
    });
  });

  const normalizeSearchText = (value) => String(value ?? "")
    .toLocaleLowerCase("tr-TR")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/ı/g, "i")
    .replace(/\s+/g, " ")
    .trim();

  document.querySelectorAll("[data-section-search]").forEach((panel) => {
    const collection = panel.closest("[data-section-search-collection]");
    const form = panel.querySelector(".section-search-form");
    const input = panel.querySelector("[data-section-search-input]");
    const clearButton = panel.querySelector("[data-section-search-clear]");
    const status = panel.querySelector("[data-section-search-status]");
    const empty = panel.querySelector("[data-section-search-empty]");
    if (!collection || !form || !input || !clearButton || !status || !empty) return;

    const items = Array.from(collection.querySelectorAll("[data-section-search-item]"));
    const groups = Array.from(collection.querySelectorAll("[data-section-search-group]"));
    const groupLinks = Array.from(collection.querySelectorAll("[data-section-search-group-link]"));
    const total = Number(panel.dataset.searchTotal) || items.length;

    const updateAddress = (query) => {
      const url = new URL(window.location.href);
      if (query) url.searchParams.set("arama", query);
      else url.searchParams.delete("arama");
      window.history.replaceState({}, "", `${url.pathname}${url.search}${url.hash}`);
    };

    const applySectionSearch = ({ updateUrl = true } = {}) => {
      const rawQuery = input.value.trim();
      const tokens = normalizeSearchText(rawQuery).split(" ").filter(Boolean);
      let visibleCount = 0;

      items.forEach((item) => {
        const haystack = normalizeSearchText(item.dataset.searchText);
        const matches = tokens.length === 0 || tokens.every((token) => haystack.includes(token));
        item.hidden = !matches;
        if (matches) visibleCount += 1;
      });

      groups.forEach((group) => {
        group.hidden = !Array.from(group.querySelectorAll("[data-section-search-item]")).some((item) => !item.hidden);
      });
      groupLinks.forEach((link) => {
        const group = collection.querySelector(`#${link.dataset.sectionSearchGroupLink}`);
        link.hidden = Boolean(group?.hidden);
      });

      const searching = tokens.length > 0;
      collection.classList.toggle("is-searching", searching);
      clearButton.hidden = !rawQuery;
      empty.hidden = !(searching && visibleCount === 0);
      status.textContent = searching
        ? `${visibleCount} sonuç · ${total} kayıt içinde`
        : `${total} kayıt`;
      if (updateUrl) updateAddress(rawQuery);
    };

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      applySectionSearch();
    });
    input.addEventListener("input", () => applySectionSearch());
    clearButton.addEventListener("click", () => {
      input.value = "";
      applySectionSearch();
      input.focus();
    });

    const initialQuery = new URL(window.location.href).searchParams.get("arama") || "";
    if (initialQuery) input.value = initialQuery;
    applySectionSearch({ updateUrl: false });
  });

  const roadmapChecks = Array.from(document.querySelectorAll("[data-roadmap-book]"));
  if (roadmapChecks.length) {
    let readBooks = storage.get("zg_read_books", []);
    if (!Array.isArray(readBooks)) readBooks = [];

    const refreshRoadmap = () => {
      const normalized = [...new Set(readBooks.map(Number).filter(Number.isFinite))];
      readBooks = normalized;
      roadmapChecks.forEach((checkbox) => {
        const number = Number(checkbox.dataset.roadmapBook);
        checkbox.checked = readBooks.includes(number);
        checkbox.closest(".book-item-row")?.classList.toggle("is-read", checkbox.checked);
      });
      const count = readBooks.length;
      const percentage = Math.round((count / 300) * 100);
      const label = document.querySelector("[data-roadmap-count]");
      const fill = document.querySelector("[data-roadmap-fill]");
      if (label) label.textContent = `${percentage}% (${count} / 300)`;
      if (fill) fill.style.width = `${percentage}%`;
    };

    roadmapChecks.forEach((checkbox) => {
      checkbox.addEventListener("change", () => {
        const number = Number(checkbox.dataset.roadmapBook);
        readBooks = checkbox.checked
          ? [...readBooks, number]
          : readBooks.filter((item) => Number(item) !== number);
        storage.set("zg_read_books", [...new Set(readBooks)]);
        refreshRoadmap();
      });
    });
    refreshRoadmap();
  }

  document.querySelectorAll("[data-summary-href]").forEach((row) => {
    const openSummary = (event) => {
      if (event.defaultPrevented || event.target.closest("a, button, input, label, summary, select, textarea")) return;
      const selection = window.getSelection();
      if (selection && !selection.isCollapsed) return;
      const href = row.dataset.summaryHref;
      if (!href) return;
      if (event.metaKey || event.ctrlKey) window.open(href, "_blank", "noopener");
      else window.location.href = href;
    };

    row.addEventListener("click", openSummary);
  });

  const article = document.querySelector('[data-post-slug="derinlik-ve-sabir-auteur-sinemasinin-anlami"]');
  const filmList = article?.querySelector(".post-body ol");
  if (filmList) {
    let watched = storage.get("zg_watched_films", []);
    if (!Array.isArray(watched)) watched = [];
    const items = Array.from(filmList.querySelectorAll(":scope > li"));
    const panel = document.createElement("section");
    panel.className = "static-film-progress";
    panel.innerHTML = '<strong>Auteur sineması yolculuğu</strong><span data-film-progress></span><div><i data-film-fill></i></div>';
    filmList.before(panel);

    const updateFilmProgress = () => {
      const count = items.filter((item) => item.querySelector("input")?.checked).length;
      const percentage = items.length ? Math.round((count / items.length) * 100) : 0;
      panel.querySelector("[data-film-progress]").textContent = `${percentage}% (${count}/${items.length})`;
      panel.querySelector("[data-film-fill]").style.width = `${percentage}%`;
    };

    items.forEach((item, index) => {
      const film = item.textContent.trim();
      const label = document.createElement("label");
      const checkbox = document.createElement("input");
      const text = document.createElement("span");
      checkbox.type = "checkbox";
      checkbox.checked = watched.includes(film);
      checkbox.id = `film-${index}`;
      text.textContent = film;
      label.htmlFor = checkbox.id;
      label.append(checkbox, text);
      item.replaceChildren(label);
      checkbox.addEventListener("change", () => {
        watched = checkbox.checked
          ? [...new Set([...watched, film])]
          : watched.filter((name) => name !== film);
        storage.set("zg_watched_films", watched);
        updateFilmProgress();
      });
    });
    updateFilmProgress();
  }

  const researchArticle = document.querySelector("[data-research-id]");
  if (researchArticle) {
    const loadButton = researchArticle.querySelector("[data-load-research]");
    const status = researchArticle.querySelector("[data-research-status]");
    const target = researchArticle.querySelector("[data-research-content]");
    let loadPromise = null;

    const escapeHtml = (value) => String(value ?? "").replace(/[&<>\"']/g, (char) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;"
    })[char]);

    const renderTable = (table) => {
      if (!table) return "";
      let rows = [];
      let headers = [];
      if (Array.isArray(table) && table.length) {
        if (table.every(Array.isArray)) rows = table;
        else if (table.every((row) => row && typeof row === "object")) {
          headers = Object.keys(table[0]);
          rows = table.map((row) => headers.map((key) => row[key]));
        }
      } else if (typeof table === "object") {
        headers = ["Başlık", "Açıklama"];
        rows = Object.entries(table);
      }
      if (!rows.length) return "";
      const head = headers.length
        ? `<thead><tr>${headers.map((cell) => `<th>${escapeHtml(cell)}</th>`).join("")}</tr></thead>`
        : "";
      const body = rows.map((row) => `<tr>${row.map((cell) => `<td>${escapeHtml(cell)}</td>`).join("")}</tr>`).join("");
      return `<div class="static-table-wrap"><table class="reader-table">${head}<tbody>${body}</tbody></table></div>`;
    };

    const renderChapter = (chapter, index) => {
      const subsections = (chapter.subsections || []).map((section) =>
        `<section><h3>${escapeHtml(section.title)}</h3><div>${section.text || ""}</div></section>`
      ).join("");
      const quote = chapter.quote ? `<blockquote>${chapter.quote}</blockquote>` : "";
      const table = renderTable(chapter.takeaways || chapter.table);
      return `<section class="research-chapter" id="bolum-${index + 1}">
        <p class="research-chapter-no">Bölüm ${String(index + 1).padStart(3, "0")}</p>
        <h2>${escapeHtml(chapter.title || `Bölüm ${index + 1}`)}</h2>${quote}${subsections}${table}
      </section>`;
    };

    const loadResearch = () => {
      if (loadPromise) return loadPromise;
      loadButton.disabled = true;
      status.textContent = "Tam metin yükleniyor…";
      loadPromise = fetch(`/data/books/${encodeURIComponent(researchArticle.dataset.researchId)}.json`)
        .then((response) => {
          if (!response.ok) throw new Error("Research file not found");
          return response.json();
        })
        .then((book) => {
          target.innerHTML = (book.chapters || []).map(renderChapter).join("");
          status.textContent = "Tam metin yüklendi.";
          loadButton.hidden = true;
        })
        .catch(() => {
          status.textContent = "Tam metin yüklenemedi; PDF bağlantısını kullanabilirsin.";
          loadButton.disabled = false;
          loadPromise = null;
          throw new Error("Research content could not be loaded");
        });
      return loadPromise;
    };

    loadButton.addEventListener("click", () => loadResearch().catch(() => {}));
    researchArticle.querySelectorAll("[data-research-chapter]").forEach((link) => {
      link.addEventListener("click", (event) => {
        event.preventDefault();
        const targetId = link.getAttribute("href");
        loadResearch().then(() => document.querySelector(targetId)?.scrollIntoView({ behavior: "smooth" })).catch(() => {});
      });
    });
  }
})();
