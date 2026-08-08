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

  document.querySelectorAll("[data-mobile-menu-toggle]").forEach((button) => {
    const navigation = document.getElementById(button.getAttribute("aria-controls"));
    const label = button.querySelector("[data-menu-label]");
    if (!navigation) return;
    const closeMenu = () => {
      navigation.classList.remove("is-open");
      button.setAttribute("aria-expanded", "false");
      if (label) label.textContent = "Menü";
    };
    button.addEventListener("click", () => {
      const open = !navigation.classList.contains("is-open");
      navigation.classList.toggle("is-open", open);
      button.setAttribute("aria-expanded", String(open));
      if (label) label.textContent = open ? "Kapat" : "Menü";
    });
    navigation.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && navigation.classList.contains("is-open")) {
        closeMenu();
        button.focus();
      }
    });
    window.matchMedia("(min-width: 761px)").addEventListener?.("change", (event) => {
      if (event.matches) closeMenu();
    });
    document.documentElement.classList.add("menu-ready");
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
        const searchMatches = tokens.length === 0 || tokens.every((token) => haystack.includes(token));
        const filterMatches = item.dataset.filterMatches !== "false";
        item.dataset.searchMatches = String(searchMatches);
        item.hidden = !(searchMatches && filterMatches);
        if (!item.hidden) visibleCount += 1;
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
    panel.addEventListener("zg:refilter", () => applySectionSearch({ updateUrl: false }));
    applySectionSearch({ updateUrl: false });
  });

  const roadmapChecks = Array.from(document.querySelectorAll("[data-roadmap-book]"));
  if (roadmapChecks.length) {
    let readBooks = storage.get("zg_read_books", []);
    if (!Array.isArray(readBooks)) readBooks = [];
    const roadmapItems = Array.from(document.querySelectorAll("[data-book-no]"));
    const roadmapTools = document.querySelector("[data-roadmap-tools]");
    const roadmapSearch = document.querySelector('[data-search-scope="roadmap"]');
    const filterControls = Array.from(roadmapTools?.querySelectorAll("[data-roadmap-filter]") || []);
    const sortControl = roadmapTools?.querySelector("[data-roadmap-sort]");
    const filterStatus = roadmapTools?.querySelector("[data-roadmap-filter-status]");
    const continueLink = document.querySelector("[data-roadmap-continue]");
    const phaseSections = Array.from(document.querySelectorAll(".roadmap-phase"));
    const responsiveDisclosures = Array.from(document.querySelectorAll("[data-responsive-disclosure]"));
    const mobileRoadmap = window.matchMedia("(max-width: 720px)");
    const roadmapSearchInput = roadmapSearch?.querySelector("[data-section-search-input]");

    const openTargetPhase = (target, exclusive = mobileRoadmap.matches) => {
      const phase = target?.closest(".roadmap-phase");
      if (!phase) return;
      if (exclusive) phaseSections.forEach((item) => { item.open = item === phase; });
      else phase.open = true;
    };

    const revealRoadmapItem = (target) => {
      if (!target) return;
      openTargetPhase(target);
      window.requestAnimationFrame(() => {
        target.scrollIntoView({ behavior: "smooth", block: "center" });
        target.classList.add("is-highlighted");
        window.setTimeout(() => target.classList.remove("is-highlighted"), 1800);
      });
    };

    const syncRoadmapPhases = () => {
      if (!mobileRoadmap.matches) {
        phaseSections.forEach((phase) => { phase.open = true; });
        return;
      }
      const hasActiveSearch = Boolean(roadmapSearchInput?.value.trim());
      const hasActiveFilter = filterControls.some((control) => control.value !== "all");
      if (hasActiveSearch || hasActiveFilter) {
        phaseSections.forEach((phase) => {
          phase.open = !phase.hidden && Array.from(phase.querySelectorAll("[data-book-no]")).some((item) => !item.hidden);
        });
        return;
      }
      const hashTarget = window.location.hash.startsWith("#kitap-")
        ? document.getElementById(window.location.hash.slice(1))
        : null;
      const firstUnread = roadmapItems.find((item) => !readBooks.includes(Number(item.dataset.bookNo))) || roadmapItems[0];
      openTargetPhase(hashTarget || firstUnread, true);
    };

    const syncResponsiveDisclosures = () => {
      responsiveDisclosures.forEach((details) => { details.open = !mobileRoadmap.matches; });
      syncRoadmapPhases();
    };

    const refreshFilters = () => {
      const selected = Object.fromEntries(filterControls.map((control) => [control.dataset.roadmapFilter, control.value]));
      roadmapItems.forEach((item) => {
        const number = Number(item.dataset.bookNo);
        const matches = (
          (selected.category === "all" || item.dataset.bookCategory === selected.category)
          && (selected.phase === "all" || item.dataset.bookPhase === selected.phase)
          && (selected.pdf === "all" || item.dataset.bookPdf === selected.pdf)
          && (selected.status === "all"
            || (selected.status === "read" && readBooks.includes(number))
            || (selected.status === "unread" && !readBooks.includes(number)))
        );
        item.dataset.filterMatches = String(matches);
      });

      document.querySelectorAll(".roadmap-books-list").forEach((list) => {
        const sorted = Array.from(list.querySelectorAll("[data-book-no]")).sort((a, b) => {
          if (sortControl?.value === "title") return a.dataset.bookTitle.localeCompare(b.dataset.bookTitle, "tr");
          if (sortControl?.value === "author") return a.dataset.bookAuthor.localeCompare(b.dataset.bookAuthor, "tr");
          return Number(a.dataset.readingOrder) - Number(b.dataset.readingOrder);
        });
        sorted.forEach((item) => list.append(item));
      });

      roadmapSearch?.dispatchEvent(new CustomEvent("zg:refilter"));
      const visible = roadmapItems.filter((item) => !item.hidden).length;
      if (filterStatus) filterStatus.textContent = `${visible} kitap gösteriliyor.`;
      syncRoadmapPhases();
    };

    const resetRoadmapView = () => {
      filterControls.forEach((control) => { control.value = "all"; });
      if (roadmapSearchInput) {
        roadmapSearchInput.value = "";
        roadmapSearchInput.dispatchEvent(new Event("input", { bubbles: true }));
      }
      refreshFilters();
    };

    const refreshRoadmap = () => {
      const normalized = [...new Set(readBooks.map(Number).filter(Number.isFinite))];
      readBooks = normalized;
      roadmapChecks.forEach((checkbox) => {
        const number = Number(checkbox.dataset.roadmapBook);
        checkbox.checked = readBooks.includes(number);
        checkbox.closest(".book-item-row")?.classList.toggle("is-read", checkbox.checked);
      });
      const count = readBooks.length;
      const total = roadmapItems.length;
      const percentage = total ? Math.round((count / total) * 100) : 0;
      const label = document.querySelector("[data-roadmap-count]");
      const fill = document.querySelector("[data-roadmap-fill]");
      if (label) label.textContent = `${percentage}% (${count} / ${total})`;
      if (fill) fill.style.width = `${percentage}%`;

      phaseSections.forEach((phase) => {
        const phaseItems = Array.from(phase.querySelectorAll("[data-book-no]"));
        const phaseRead = phaseItems.filter((item) => readBooks.includes(Number(item.dataset.bookNo))).length;
        const phaseProgress = phase.querySelector("[data-phase-progress]");
        if (phaseProgress) phaseProgress.textContent = `${phaseRead} / ${phaseItems.length}`;
      });

      const nextItem = roadmapItems.find((item) => !readBooks.includes(Number(item.dataset.bookNo)));
      const target = nextItem || roadmapItems[0];
      if (continueLink && target) {
        const completed = !nextItem;
        continueLink.href = target.dataset.summaryHref || `#${target.id}`;
        const continueLabel = continueLink.querySelector("[data-roadmap-continue-label]");
        const continueTitle = continueLink.querySelector("[data-roadmap-continue-title]");
        if (continueLabel) continueLabel.textContent = completed ? "Rota tamamlandı" : (readBooks.length ? "Kaldığın yerden devam et" : "Rotaya başla");
        if (continueTitle) continueTitle.textContent = `${completed ? "Yeniden gözden geçir" : `Durak ${String(target.dataset.readingOrder).padStart(3, "0")}`} · ${target.dataset.bookTitle}`;
      }
      refreshFilters();
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
    filterControls.forEach((control) => control.addEventListener("change", refreshFilters));
    sortControl?.addEventListener("change", refreshFilters);

    roadmapTools?.querySelector("[data-reset-filters]")?.addEventListener("click", () => {
      filterControls.forEach((control) => { control.value = "all"; });
      if (sortControl) sortControl.value = "number";
      refreshFilters();
    });

    roadmapTools?.querySelector("[data-random-book]")?.addEventListener("click", () => {
      const candidates = roadmapItems.filter((item) => !item.hidden);
      const target = candidates[Math.floor(Math.random() * candidates.length)] || roadmapItems[0];
      revealRoadmapItem(target);
    });

    roadmapTools?.querySelector("[data-roadmap-jump]")?.addEventListener("submit", (event) => {
      event.preventDefault();
      const input = event.currentTarget.querySelector("input");
      const number = Number(input?.value);
      const target = roadmapItems.find((item) => Number(item.dataset.readingOrder) === number);
      if (!target) {
        if (filterStatus) filterStatus.textContent = "1 ile 300 arasında bir rota sırası yaz.";
        input?.focus();
        return;
      }
      resetRoadmapView();
      window.history.replaceState({}, "", `${window.location.pathname}#${target.id}`);
      revealRoadmapItem(target);
    });

    roadmapTools?.querySelector("[data-export-progress]")?.addEventListener("click", () => {
      const payload = JSON.stringify({ version: 1, readBooks: [...new Set(readBooks)].sort((a, b) => a - b) }, null, 2);
      const url = URL.createObjectURL(new Blob([payload], { type: "application/json" }));
      const link = document.createElement("a");
      link.href = url;
      link.download = "zihin-gezgini-okuma-ilerlemesi.json";
      link.click();
      URL.revokeObjectURL(url);
      if (filterStatus) filterStatus.textContent = "Okuma ilerlemesi yedeklendi.";
    });

    const importInput = roadmapTools?.querySelector("[data-import-progress-file]");
    roadmapTools?.querySelector("[data-import-progress]")?.addEventListener("click", () => importInput?.click());
    importInput?.addEventListener("change", async () => {
      try {
        const payload = JSON.parse(await importInput.files[0].text());
        if (payload.version !== 1 || !Array.isArray(payload.readBooks)) throw new Error("Invalid progress file");
        readBooks = [...new Set(payload.readBooks.map(Number).filter((number) => Number.isInteger(number) && number >= 1 && number <= 300))];
        storage.set("zg_read_books", readBooks);
        refreshRoadmap();
        if (filterStatus) filterStatus.textContent = `${readBooks.length} kitaplık ilerleme geri yüklendi.`;
      } catch (_) {
        if (filterStatus) filterStatus.textContent = "Bu dosya geçerli bir Zihin Gezgini ilerleme yedeği değil.";
      } finally {
        importInput.value = "";
      }
    });
    document.querySelectorAll("[data-section-search-group-link]").forEach((link) => {
      link.addEventListener("click", () => {
        const phase = document.getElementById(link.dataset.sectionSearchGroupLink);
        if (!phase) return;
        if (mobileRoadmap.matches) phaseSections.forEach((item) => { item.open = item === phase; });
        else phase.open = true;
      });
    });

    roadmapSearchInput?.addEventListener("input", syncRoadmapPhases);

    document.querySelectorAll('.start-route a[href^="#kitap-"]').forEach((link) => {
      link.addEventListener("click", (event) => {
        const target = document.getElementById(link.getAttribute("href").slice(1));
        if (!target) return;
        event.preventDefault();
        resetRoadmapView();
        window.history.replaceState({}, "", `${window.location.pathname}#${target.id}`);
        revealRoadmapItem(target);
      });
    });

    mobileRoadmap.addEventListener?.("change", syncResponsiveDisclosures);
    refreshRoadmap();
    syncResponsiveDisclosures();
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

  const globalSearch = document.querySelector("[data-global-search]");
  if (globalSearch) {
    const form = globalSearch.querySelector(".global-search-form");
    const input = globalSearch.querySelector("#global-search-input");
    const type = globalSearch.querySelector("#global-search-type");
    const typeButtons = Array.from(globalSearch.querySelectorAll("[data-global-search-type]"));
    const status = globalSearch.querySelector("[data-global-search-status]");
    const results = globalSearch.querySelector("[data-global-search-results]");
    let index = [];

    const escapeHtml = (value) => String(value ?? "").replace(/[&<>\"']/g, (char) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;"
    })[char]);

    const search = () => {
      const rawQuery = input.value.trim();
      const tokens = normalizeSearchText(rawQuery).split(" ").filter(Boolean);
      const candidates = index.filter((item) => {
        if (type.value !== "all" && item.type !== type.value) return false;
        const haystack = normalizeSearchText(`${item.title} ${item.subtitle} ${item.description}`);
        return tokens.length === 0 || tokens.every((token) => haystack.includes(token));
      });
      const matches = (!tokens.length && type.value === "all")
        ? ["post", "summary", "research"].flatMap((recordType) => candidates.filter((item) => item.type === recordType).slice(0, 6))
        : candidates.slice(0, tokens.length ? 80 : 18);
      typeButtons.forEach((button) => button.setAttribute("aria-pressed", String(button.dataset.globalSearchType === type.value)));
      results.innerHTML = matches.map((item) => `
        <a class="global-search-result" href="${escapeHtml(item.url)}">
          <span>${escapeHtml(item.label)}</span><h2>${escapeHtml(item.title)}</h2>
          <strong>${escapeHtml(item.subtitle)}</strong><p>${escapeHtml(item.description)}</p>
        </a>`).join("");
      status.textContent = tokens.length
        ? `${matches.length} sonuç gösteriliyor${matches.length === 80 ? " · aramanı daraltabilirsin" : ""}.`
        : (type.value === "all"
          ? `Arşivde ${index.length} kayıt var; üç koleksiyondan ${matches.length} örnek gösteriliyor.`
          : `${candidates.length} kayıttan ${matches.length} tanesi gösteriliyor.`);
      const url = new URL(window.location.href);
      if (rawQuery) url.searchParams.set("q", rawQuery); else url.searchParams.delete("q");
      if (type.value !== "all") url.searchParams.set("tur", type.value); else url.searchParams.delete("tur");
      window.history.replaceState({}, "", `${url.pathname}${url.search}`);
    };

    fetch("/data/search-index.json")
      .then((response) => {
        if (!response.ok) throw new Error("Search index not found");
        return response.json();
      })
      .then((records) => {
        index = records;
        const params = new URL(window.location.href).searchParams;
        input.value = params.get("q") || "";
        if (["post", "summary", "research"].includes(params.get("tur"))) type.value = params.get("tur");
        search();
      })
      .catch(() => { status.textContent = "Arama dizini şu anda yüklenemedi."; });
    form.addEventListener("submit", (event) => { event.preventDefault(); search(); });
    input.addEventListener("input", search);
    type.addEventListener("change", search);
    typeButtons.forEach((button) => button.addEventListener("click", () => {
      type.value = button.dataset.globalSearchType;
      search();
    }));
  }

  const summaryArticle = document.querySelector("[data-summary-book]");
  if (summaryArticle) {
    const bookNumber = summaryArticle.dataset.summaryBook;
    const chapters = Array.from(summaryArticle.querySelectorAll(".reader-chapter-section[id]"));
    const progress = document.querySelector("[data-reading-progress] span");
    const resumeButton = summaryArticle.querySelector("[data-reader-resume]");
    let positions = storage.get("zg_summary_positions", {});
    if (!positions || typeof positions !== "object" || Array.isArray(positions)) positions = {};
    const savedChapter = positions[bookNumber];
    if (savedChapter && document.getElementById(savedChapter)) resumeButton.hidden = false;

    resumeButton?.addEventListener("click", () => document.getElementById(positions[bookNumber])?.scrollIntoView({ behavior: "smooth" }));
    summaryArticle.querySelector("[data-reader-print]")?.addEventListener("click", () => window.print());
    const readerMore = summaryArticle.querySelector(".summary-reader-more");
    const readerMoreMedia = window.matchMedia("(max-width: 760px)");
    const syncReaderMore = () => readerMore?.toggleAttribute("open", !readerMoreMedia.matches);
    syncReaderMore();
    readerMoreMedia.addEventListener?.("change", syncReaderMore);
    summaryArticle.querySelectorAll(".summary-reader-more-menu button").forEach((button) => {
      button.addEventListener("click", () => {
        if (readerMoreMedia.matches) readerMore?.removeAttribute("open");
      });
    });

    const readToggle = summaryArticle.querySelector("[data-summary-read-toggle]");
    let summaryReadBooks = storage.get("zg_read_books", []);
    if (!Array.isArray(summaryReadBooks)) summaryReadBooks = [];
    summaryReadBooks = [...new Set(summaryReadBooks.map(Number).filter(Number.isFinite))];
    const updateReadToggle = () => {
      if (!readToggle) return;
      const isRead = summaryReadBooks.includes(Number(bookNumber));
      readToggle.setAttribute("aria-pressed", String(isRead));
      readToggle.setAttribute("aria-label", isRead ? "Okundu işaretini kaldır" : "Okundu olarak işaretle");
      readToggle.textContent = isRead ? "Okundu ✓" : "Okundu olarak işaretle";
      readToggle.closest(".summary-completion")?.classList.toggle("is-read", isRead);
    };
    readToggle?.addEventListener("click", () => {
      const number = Number(bookNumber);
      summaryReadBooks = summaryReadBooks.includes(number)
        ? summaryReadBooks.filter((item) => item !== number)
        : [...summaryReadBooks, number];
      storage.set("zg_read_books", summaryReadBooks);
      updateReadToggle();
    });
    updateReadToggle();

    let fontScale = Number(storage.get("zg_summary_font_scale", 1));
    if (!Number.isFinite(fontScale)) fontScale = 1;
    const applyFontScale = () => {
      fontScale = Math.min(1.3, Math.max(0.85, fontScale));
      summaryArticle.style.setProperty("--summary-reader-font-size", `${fontScale}rem`);
      storage.set("zg_summary_font_scale", fontScale);
    };
    summaryArticle.querySelectorAll("[data-reader-font]").forEach((button) => {
      button.addEventListener("click", () => {
        fontScale += button.dataset.readerFont === "increase" ? 0.1 : -0.1;
        applyFontScale();
      });
    });
    applyFontScale();

    const widthButton = summaryArticle.querySelector("[data-reader-width]");
    const compactPreference = storage.get("zg_summary_compact_width", null);
    const compact = compactPreference === null ? true : compactPreference === true;
    summaryArticle.classList.toggle("compact-reader", compact);
    widthButton?.setAttribute("aria-pressed", String(compact));
    widthButton?.addEventListener("click", () => {
      const next = !summaryArticle.classList.contains("compact-reader");
      summaryArticle.classList.toggle("compact-reader", next);
      widthButton.setAttribute("aria-pressed", String(next));
      storage.set("zg_summary_compact_width", next);
    });

    const updateReadingProgress = () => {
      const rect = summaryArticle.getBoundingClientRect();
      const distance = Math.max(1, summaryArticle.offsetHeight - window.innerHeight);
      const percentage = Math.min(100, Math.max(0, (-rect.top / distance) * 100));
      if (progress) progress.style.width = `${percentage}%`;
    };
    window.addEventListener("scroll", updateReadingProgress, { passive: true });
    updateReadingProgress();

    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      positions[bookNumber] = visible.target.id;
      storage.set("zg_summary_positions", positions);
      resumeButton.hidden = true;
      const chapterIndex = chapters.indexOf(visible.target);
      const totalMinutes = Number(summaryArticle.dataset.summaryReadingMinutes) || 0;
      const remainingMinutes = Math.max(0, Math.ceil(totalMinutes * ((chapters.length - chapterIndex - 1) / Math.max(1, chapters.length))));
      const tocStatus = summaryArticle.querySelector("[data-summary-toc-status]");
      if (tocStatus && chapterIndex >= 0) {
        tocStatus.textContent = `Bölüm ${chapterIndex + 1}/${chapters.length} · ${remainingMinutes ? `kalan ~${remainingMinutes} dk` : "son bölüm"}`;
      }
      summaryArticle.querySelectorAll(".summary-toc a").forEach((link) => {
        const isCurrent = link.getAttribute("href") === `#${visible.target.id}`;
        link.classList.toggle("is-current", isCurrent);
        if (isCurrent) link.closest(".summary-toc-group")?.setAttribute("open", "");
      });
    }, { rootMargin: "-20% 0px -65%", threshold: [0, 0.25, 0.6] });
    chapters.forEach((chapter) => observer.observe(chapter));
  }

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
