// Zihin Gezgini - Core Application Script

document.addEventListener("DOMContentLoaded", () => {
  // Router elements
  const views = {
    home: document.getElementById("view-home"),
    post: document.getElementById("view-post"),
    about: document.getElementById("view-about"),
    roadmap: document.getElementById("view-roadmap"),
    bookSummary: document.getElementById("view-book-summary")
  };
  
  const navLinks = {
    home: document.getElementById("nav-home"),
    about: document.getElementById("nav-about"),
    roadmap: document.getElementById("nav-roadmap"),
    random: document.getElementById("nav-random")
  };
  
  const postsGrid = document.getElementById("posts-grid");
  const postDetail = document.getElementById("post-detail");
  const filterBtns = document.querySelectorAll(".filter-btn");
  
  let allPosts = [];
  let quotes = [];
  let currentIndex = 0;
  let currentCategory = "all";
  let searchQuery = "";
  let currentFontSize = 1.125; // default size in rem
  let postsToShow = 9; // Number of posts to show initially

  // Date formatter (Turkish locale)
  function formatDate(dateStr) {
    if (!dateStr) return "";
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString("tr-TR", {
        year: "numeric",
        month: "long",
        day: "numeric"
      });
    } catch (e) {
      return dateStr;
    }
  }

  // Calculate Reading Time (Turkish)
  function calculateReadingTime(content) {
    if (!content) return "1 dk okuma";
    const wordsPerMinute = 200;
    const cleanText = content.replace(/<[^>]*>/g, '');
    const wordCount = cleanText.split(/\s+/).filter(w => w.length > 0).length;
    const readingTime = Math.ceil(wordCount / wordsPerMinute);
    return `${readingTime} dk okuma`;
  }

  // Dynamic SEO Meta Tag Updater
  function updateMetaTags(title, description, image) {
    document.title = title;
    
    const elements = {
      description: document.querySelector('meta[name="description"]'),
      ogTitle: document.getElementById("og-title"),
      ogDesc: document.getElementById("og-description"),
      ogImage: document.getElementById("og-image"),
      twTitle: document.getElementById("twitter-title"),
      twDesc: document.getElementById("twitter-description"),
      twImage: document.getElementById("twitter-image")
    };
    
    const finalDesc = description || "Hayatın ritminden kaçanlar, anı yaşamak isteyenler ve filozof monologları üzerine felsefi düşünceler.";
    const finalImg = image || "https://zihingezgini.net/images/thinking_man_sketch.png";
    const finalTitle = title;
    
    if (elements.description) elements.description.setAttribute("content", finalDesc.substring(0, 160));
    if (elements.ogTitle) elements.ogTitle.setAttribute("content", finalTitle);
    if (elements.ogDesc) elements.ogDesc.setAttribute("content", finalDesc.substring(0, 160));
    if (elements.ogImage) elements.ogImage.setAttribute("content", finalImg);
    if (elements.twTitle) elements.twTitle.setAttribute("content", finalTitle);
    if (elements.twDesc) elements.twDesc.setAttribute("content", finalDesc.substring(0, 160));
    if (elements.twImage) elements.twImage.setAttribute("content", finalImg);
  }

  // Fetch all posts index
  async function loadPostsIndex() {
    try {
      const response = await fetch(`/data/posts.json?t=${new Date().getTime()}`);
      if (!response.ok) throw new Error("Index file not found");
      allPosts = await response.json();
      renderPostsGrid();
    } catch (error) {
      console.error("Error loading posts index:", error);
      postsGrid.innerHTML = `<div class="loading-placeholder">Yazılar yüklenemedi. Lütfen daha sonra tekrar deneyin.</div>`;
    }
  }

  // Render post list in grid
  function renderPostsGrid() {
    postsGrid.innerHTML = "";
    const loadMoreContainer = document.getElementById("load-more-container");
    if (loadMoreContainer) loadMoreContainer.innerHTML = "";
    
    const filteredPosts = allPosts.filter(post => {
      let matchesCategory = false;
      if (currentCategory === "all") {
        matchesCategory = true;
      } else if (currentCategory === "monologues") {
        matchesCategory = !!post.hasAudio;
      } else {
        matchesCategory = post.category === currentCategory;
      }
      
      const matchesSearch = searchQuery === "" || 
        post.title.toLowerCase().includes(searchQuery) ||
        (post.category && post.category.toLowerCase().includes(searchQuery));
      return matchesCategory && matchesSearch;
    });
      
    if (filteredPosts.length === 0) {
      postsGrid.innerHTML = `<div class="loading-placeholder">Aradığınız kriterlere uygun bir yazı bulunamadı.</div>`;
      return;
    }
    
    // Slice posts to only show the requested number
    const visiblePosts = filteredPosts.slice(0, postsToShow);
    
    visiblePosts.forEach(post => {
      const card = document.createElement("a");
      card.className = "post-card";
      card.href = `#/post/${post.slug}`;
      
      const imgHtml = post.featuredImage 
        ? `<div class="card-img-container"><img src="${post.featuredImage}" class="card-img" alt="${post.title}" loading="lazy"></div>`
        : "";
        
      card.innerHTML = `
        ${imgHtml}
        <div class="card-content">
          <span class="card-category">${post.category || 'Düşünce'}</span>
          <h3 class="card-title">${post.title}</h3>
          <span class="card-date">${formatDate(post.date)}</span>
        </div>
      `;
      postsGrid.appendChild(card);
    });

    // Add "Load More" button if there are more posts remaining
    if (filteredPosts.length > postsToShow && loadMoreContainer) {
      const loadMoreBtn = document.createElement("button");
      loadMoreBtn.className = "load-more-btn";
      loadMoreBtn.innerHTML = "Daha Fazla Yazı Göster";
      loadMoreBtn.addEventListener("click", () => {
        postsToShow += 9;
        renderPostsGrid();
      });
      loadMoreContainer.appendChild(loadMoreBtn);
    }
  }

  // Load single post detail
  async function loadPostDetail(slug) {
    postDetail.innerHTML = `<div class="loading-placeholder">Yazı yükleniyor...</div>`;
    
    try {
      const response = await fetch(`/data/posts/${slug}.json?t=${new Date().getTime()}`);
      if (!response.ok) throw new Error("Post not found");
      const post = await response.json();
      
      const imgHtml = post.featuredImage 
        ? `<img src="${post.featuredImage}" class="post-featured-img" alt="${post.title}">`
        : "";
        
      // Extract YouTube link from content if present
      let cleanContent = post.content;
      let youtubeUrl = null;
      
      const ytRegex = /<a[^>]*href="(https?:\/\/(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)[a-zA-Z0-9_-]+)"[^>]*>.*?<\/a>/i;
      const ytMatch = cleanContent.match(ytRegex);
      if (ytMatch) {
        youtubeUrl = ytMatch[1];
        // Clean the paragraph containing the YouTube video link
        const pRegex = new RegExp(`<p[^>]*>.*?${ytMatch[0].replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')}.*?<\/p>`, 'gi');
        cleanContent = cleanContent.replace(pRegex, '');
      }

      // Clear duplicate title from content if it matches the main title
      const tempDiv = document.createElement("div");
      tempDiv.innerHTML = cleanContent;
      const firstHeading = tempDiv.querySelector("h1, h2, h3");
      if (firstHeading) {
        const normalize = str => str.toLowerCase().replace(/[^a-z0-9]/g, "");
        if (normalize(firstHeading.textContent) === normalize(post.title)) {
          firstHeading.remove();
          cleanContent = tempDiv.innerHTML;
        }
      }

      // Update document title and SEO meta tags
      const plainText = cleanContent.replace(/<[^>]*>/g, '');
      const postDesc = plainText.substring(0, 150).trim() + "...";
      const fullImgUrl = post.featuredImage ? `https://zihingezgini.net${post.featuredImage}` : "https://zihingezgini.net/images/thinking_man_sketch.png";
      updateMetaTags(`Zihin Gezgini | ${post.title}`, postDesc, fullImgUrl);

      postDetail.innerHTML = `
        <div class="post-header-actions">
          <button class="post-back-btn" onclick="window.location.hash = '#/'">
            ← Geri Dön
          </button>
          <div class="font-size-adjuster">
            <button id="font-dec" title="Yazıyı Küçült">A-</button>
            <button id="font-inc" title="Yazıyı Büyüt">A+</button>
          </div>
        </div>
        <header class="post-meta">
          <div class="post-detail-category">${post.category || 'Düşünce'}</div>
          <h1 class="post-detail-title">${post.title}</h1>
          <div class="post-meta-sub">
            <span class="post-detail-date">${formatDate(post.date)}</span>
            <span class="post-read-time">• ${calculateReadingTime(post.content)}</span>
            ${youtubeUrl ? `• <button id="toggle-audio-btn" class="post-listen-btn">🎧 Monoloğu Dinle</button>` : ""}
            • <button id="post-share-btn" class="post-share-btn" title="Yazıyı Paylaş">🔗 Paylaş</button>
          </div>
        </header>
        ${youtubeUrl ? `<div id="post-audio-player-container" class="post-audio-player-container"></div>` : ""}
        ${imgHtml}
        <div class="post-body">
          ${cleanContent}
        </div>
        <div class="post-subscribe-section">
          <h3>Zihin Gezgini Substack</h3>
          <p>Her hafta e-posta kutunuza gelecek yeni filozof monologları ve felsefi karalamalar için bültene katılın.</p>
          <a href="https://zihingezgini.substack.com" target="_blank" class="subscribe-btn">Substack'te Abone Ol ↗</a>
        </div>
      `;

      // Setup Font Size Adjuster Event Listeners
      setupFontSizeAdjuster();
      
      // Setup Share Button Event Listener
      setupShareButton(post);



      // Setup Audio Player Event Listener if YouTube url is present
      setupAudioPlayer(youtubeUrl);

      // Setup Interactive Film List for Auteur Cinema post
      setupInteractiveFilmList(post);

    } catch (error) {
      console.error("Error loading post detail:", error);
      postDetail.innerHTML = `
        <button class="post-back-btn" onclick="window.location.hash = '#/'">
          ← Geri Dön
        </button>
        <div class="loading-placeholder">Yazı yüklenirken bir hata oluştu.</div>
      `;
    }
  }

  // Setup font size controls
  function setupFontSizeAdjuster() {
    const fontDec = document.getElementById("font-dec");
    const fontInc = document.getElementById("font-inc");
    const postBody = document.querySelector(".post-body");
    
    if (fontDec && fontInc && postBody) {
      // Set initial font size
      postBody.style.fontSize = `${currentFontSize}rem`;
      
      fontDec.addEventListener("click", () => {
        if (currentFontSize > 0.95) {
          currentFontSize -= 0.1;
          postBody.style.fontSize = `${currentFontSize}rem`;
        }
      });
      
      fontInc.addEventListener("click", () => {
        if (currentFontSize < 1.45) {
          currentFontSize += 0.1;
          postBody.style.fontSize = `${currentFontSize}rem`;
        }
      });
    }
  }

  // Setup Share Button
  function setupShareButton(post) {
    const shareBtn = document.getElementById("post-share-btn");
    if (shareBtn) {
      shareBtn.addEventListener("click", async () => {
        const shareData = {
          title: `Zihin Gezgini | ${post.title}`,
          text: `${post.title} - Zihin Gezgini Monoloğu`,
          url: window.location.href
        };
        
        if (navigator.share) {
          try {
            await navigator.share(shareData);
          } catch (err) {
            console.log("Error sharing:", err);
          }
        } else {
          try {
            await navigator.clipboard.writeText(window.location.href);
            const originalText = shareBtn.innerHTML;
            shareBtn.innerHTML = "✓ Kopyalandı!";
            shareBtn.style.color = "var(--color-accent)";
            setTimeout(() => {
              shareBtn.innerHTML = originalText;
              shareBtn.style.color = "";
            }, 2000);
          } catch (err) {
            console.error("Failed to copy link:", err);
          }
        }
      });
    }
  }

  // Setup Audio Player Event Listener
  function setupAudioPlayer(youtubeUrl) {
    const toggleBtn = document.getElementById("toggle-audio-btn");
    const container = document.getElementById("post-audio-player-container");
    
    if (!toggleBtn || !container || !youtubeUrl) return;
    
    function getYouTubeId(url) {
      if (!url) return null;
      const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
      const match = url.match(regExp);
      return (match && match[2].length === 11) ? match[2] : null;
    }
    
    const videoId = getYouTubeId(youtubeUrl);
    if (!videoId) return;
    
    toggleBtn.addEventListener("click", () => {
      if (container.classList.contains("active")) {
        // If active, stop and close
        container.innerHTML = "";
        container.classList.remove("active");
        toggleBtn.innerHTML = "🎧 Monoloğu Dinle";
        toggleBtn.classList.remove("playing");
      } else {
        // If not active, play inline
        container.innerHTML = `
          <div class="player-header">
            <span>🎧 Monolog Oynatılıyor</span>
            <button id="close-player-btn" class="close-player-btn">✕ Kapat</button>
          </div>
          <div class="player-wrapper">
            <iframe 
              src="https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0&showinfo=0" 
              frameborder="0" 
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
              allowfullscreen>
            </iframe>
          </div>
        `;
        container.classList.add("active");
        toggleBtn.innerHTML = "⏸ Monoloğu Durdur";
        toggleBtn.classList.add("playing");
        
        // Setup internal close button
        const closeBtn = document.getElementById("close-player-btn");
        if (closeBtn) {
          closeBtn.addEventListener("click", () => {
            container.innerHTML = "";
            container.classList.remove("active");
            toggleBtn.innerHTML = "🎧 Monoloğu Dinle";
            toggleBtn.classList.remove("playing");
          });
        }
      }
    });
  }

  // Setup Interactive Film List for Auteur Cinema post
  function setupInteractiveFilmList(post) {
    if (post.slug !== "derinlik-ve-sabir-auteur-sinemasinin-anlami") return;
    
    const postBody = document.querySelector(".post-body");
    if (!postBody) return;
    
    const list = postBody.querySelector("ol");
    if (!list) return;
    
    list.classList.add("interactive-checklist");
    
    let watchedList = [];
    try {
      watchedList = JSON.parse(localStorage.getItem("zg_watched_films") || "[]");
    } catch(e) {
      watchedList = [];
    }
    
    const items = list.querySelectorAll("li");
    const totalFilms = items.length;
    
    const progressContainer = document.createElement("div");
    progressContainer.id = "film-progress-container";
    progressContainer.className = "film-progress-container";
    progressContainer.innerHTML = `
      <div class="progress-info">
        <span>🎬 Auteur Sineması Yolculuğunuz</span>
        <strong id="progress-percent">0% (0/${totalFilms})</strong>
      </div>
      <div class="progress-bar-bg">
        <div id="progress-bar-fill" class="progress-bar-fill" style="width: 0%"></div>
      </div>
    `;
    
    // Create the top panel
    const checklistPanel = document.createElement("div");
    checklistPanel.className = "checklist-top-panel";
    
    // Move list and progress into the panel
    checklistPanel.appendChild(progressContainer);
    
    // Wrap list inside a scroll container for premium dashboard styling
    const scrollContainer = document.createElement("div");
    scrollContainer.className = "checklist-scroll-container";
    
    // Remove list from original place and append to scroll container
    list.parentNode.removeChild(list);
    scrollContainer.appendChild(list);
    checklistPanel.appendChild(scrollContainer);
    
    // Insert panel at the very top of postBody
    postBody.insertBefore(checklistPanel, postBody.firstChild);
    
    // Move the featured image below the panel
    const featuredImg = document.querySelector(".post-featured-img");
    if (featuredImg) {
      featuredImg.parentNode.removeChild(featuredImg);
      postBody.insertBefore(featuredImg, checklistPanel.nextSibling);
      featuredImg.style.marginTop = "40px";
    }
    
    // Remove the original section header and paragraphs that introduced the list at the bottom
    const listHeading = postBody.querySelector("h2.wp-block-heading");
    if (listHeading && (listHeading.textContent.includes("50") || listHeading.textContent.includes("Listesi"))) {
      const nextP = listHeading.nextElementSibling;
      if (nextP && nextP.tagName === "P") {
        nextP.remove();
      }
      listHeading.remove();
    }
    
    function updateProgress() {
      const checkedCount = list.querySelectorAll('input[type="checkbox"]:checked').length;
      const percent = totalFilms > 0 ? Math.round((checkedCount / totalFilms) * 100) : 0;
      
      const percentText = document.getElementById("progress-percent");
      const barFill = document.getElementById("progress-bar-fill");
      
      if (percentText) percentText.textContent = `${percent}% (${checkedCount}/${totalFilms})`;
      if (barFill) barFill.style.width = `${percent}%`;
    }
    
    items.forEach((item, idx) => {
      const filmName = item.textContent.trim();
      const isWatched = watchedList.includes(filmName);
      
      const checkboxId = `film-check-${idx}`;
      item.innerHTML = `
        <label for="${checkboxId}" class="checklist-label">
          <input type="checkbox" id="${checkboxId}" data-index="${idx}" ${isWatched ? 'checked' : ''}>
          <span class="checkbox-custom"></span>
          <span class="film-text">${item.innerHTML}</span>
        </label>
      `;
      
      const checkbox = item.querySelector('input[type="checkbox"]');
      checkbox.addEventListener("change", (e) => {
        const itemText = filmName;
        if (e.target.checked) {
          if (!watchedList.includes(itemText)) watchedList.push(itemText);
        } else {
          watchedList = watchedList.filter(name => name !== itemText);
        }
        localStorage.setItem("zg_watched_films", JSON.stringify(watchedList));
        updateProgress();
      });
    });
    
    updateProgress();
  }

  // Setup Interactive Reading Roadmap
  const EVRE_TITLES = {
    1: "Evre I: Temeller (Evren, Doğa ve Canlılık)",
    2: "Evre II: Zihin ve Benlik (İnsan Nörobiyolojisi ve Biliş)",
    3: "Evre III: Karakter ve İyi Yaşam (Klasik Felsefe ve Stoacılık)",
    4: "Evre IV: Toplum ve Sözleşme (Devletin Kökenleri ve Siyaset Felsefesi)",
    5: "Evre V: Hakikat ve Yöntem (Epistemoloji ve Bilim Felsefesi)",
    6: "Evre VI: Ekonomi Politik ve Sınıf (Maddi Dünyanın İşleyişi)",
    7: "Evre VII: Dil ve Anlamlandırma (Dilbilim, Semiyotik ve Medya Analizi)",
    8: "Evre VIII: Görsel Kültür, Estetik ve Kimlik (Temsil Politikaları)",
    9: "Evre IX: Geç Modernite ve Yapay Zeka (Teknolojik Gelecek)",
    10: "Evre X: Sentezler ve Bütünsel Felsefe (Zihin Gezgini Manifestosu)"
  };

  async function setupRoadmap() {
    const phasesContainer = document.getElementById("roadmap-phases");
    if (!phasesContainer) return;
    
    try {
      const response = await fetch(`/data/books.json?t=${new Date().getTime()}`);
      if (!response.ok) throw new Error("Books file not found");
      const books = await response.json();
      
      // Render featured summaries at the top
      const featuredSection = document.getElementById("featured-summaries-section");
      if (featuredSection) {
        const featuredBooks = books.filter(b => b.hasSummary);
        if (featuredBooks.length > 0) {
          featuredSection.innerHTML = `
            <div class="featured-summaries-header">
              <h3 class="featured-summaries-title">📖 Hemen Okunabilecek Özet Kitapçıklar</h3>
              <p class="featured-summaries-subtitle">Yalın anlatımlarla özetlenmiş, okumaya hazır eserler.</p>
            </div>
            <div class="featured-summaries-list">
              ${featuredBooks.map(b => {
                return `
                  <div class="featured-summary-row">
                    <div class="featured-row-info">
                      <div class="featured-row-meta">
                        <span class="featured-row-no">#${b.no}</span>
                        <span class="featured-row-category-tag">${b.category}</span>
                        <a href="#/book/${b.no}/summary" class="featured-row-read-btn">📖 Özet Oku</a>
                      </div>
                      <div class="featured-row-title-line">
                        <strong class="featured-row-author">${b.author}</strong> — <span class="featured-row-title">${b.title}</span>
                      </div>
                      <p class="featured-row-desc">${b.description}</p>
                    </div>
                  </div>
                `;
              }).join("")}
            </div>
            <div class="divider" style="margin-top: 30px;"></div>
          `;
        } else {
          featuredSection.innerHTML = "";
        }
      }
      
      let readBooks = [];
      try {
        readBooks = JSON.parse(localStorage.getItem("zg_read_books") || "[]");
      } catch (e) {
        readBooks = [];
      }
      
      // Calculate progress and update stats & quick nav
      function updateRoadmapProgress() {
        const total = 300;
        const count = readBooks.length;
        const percent = Math.round((count / total) * 100);
        
        const percentText = document.getElementById("roadmap-progress-percentage");
        const countText = document.getElementById("roadmap-progress-count");
        const fillBar = document.getElementById("roadmap-progress-fill");
        
        if (percentText) percentText.textContent = `${percent}%`;
        if (countText) countText.textContent = count;
        if (fillBar) fillBar.style.width = `${percent}%`;
        
        // Update quick nav counts
        const quickNavContainer = document.getElementById("roadmap-quick-nav");
        if (quickNavContainer) {
          const EVRE_SHORT_TITLES = {
            1: "Fizik",
            2: "Biyoloji",
            3: "Psikoloji",
            4: "Sosyoloji",
            5: "Tarih",
            6: "Felsefe",
            7: "Dilbilim",
            8: "Sanat",
            9: "Teknoloji",
            10: "Sentez"
          };
          
          let navHtml = "";
          for (let e = 1; e <= 10; e++) {
            const phaseBooks = evreBooks[e] || [];
            const phaseReadCount = phaseBooks.filter(b => readBooks.includes(b.no)).length;
            const isCompleted = phaseReadCount === 30;
            const hasStarted = phaseReadCount > 0;
            
            navHtml += `
              <button class="quick-nav-pill ${isCompleted ? 'is-completed' : ''} ${hasStarted ? 'has-started' : ''}" data-evre="${e}" title="${EVRE_TITLES[e] || ''}">
                <span class="quick-nav-label">${EVRE_SHORT_TITLES[e]}</span>
                <span class="quick-nav-count">${phaseReadCount}/30</span>
              </button>
            `;
          }
          quickNavContainer.innerHTML = navHtml;
          
          // Add click listeners to quick nav buttons
          quickNavContainer.querySelectorAll(".quick-nav-pill").forEach(btn => {
            btn.addEventListener("click", () => {
              const e = parseInt(btn.getAttribute("data-evre"));
              const targetDiv = document.getElementById(`phase-card-${e}`);
              if (targetDiv) {
                // Ensure target is open
                if (!targetDiv.classList.contains("is-open")) {
                  targetDiv.classList.add("is-open");
                  const icon = targetDiv.querySelector(".phase-toggle-icon");
                  if (icon) icon.textContent = "▸";
                }
                
                // Highlight phase card temporarily with a subtle pulse
                targetDiv.classList.add("highlight-pulse");
                setTimeout(() => {
                  targetDiv.classList.remove("highlight-pulse");
                }, 2000);
                
                // Scroll smoothly
                targetDiv.scrollIntoView({ behavior: "smooth", block: "start" });
              }
            });
          });
        }
      }
      
      phasesContainer.innerHTML = "";
      
      // Group books by evre
      const evreBooks = {};
      for (let i = 1; i <= 10; i++) {
        evreBooks[i] = [];
      }
      books.forEach(b => {
        if (evreBooks[b.evre]) evreBooks[b.evre].push(b);
      });
      
      for (let e = 1; e <= 10; e++) {
        const phaseBooks = evreBooks[e];
        const phaseDiv = document.createElement("div");
        phaseDiv.className = "roadmap-phase-card is-open";
        phaseDiv.id = `phase-card-${e}`;
        
        // Count read books in this phase
        const phaseReadCount = phaseBooks.filter(b => readBooks.includes(b.no)).length;
        
        phaseDiv.innerHTML = `
          <div class="phase-header" data-evre="${e}">
            <div class="phase-title-group">
              <span class="phase-toggle-icon">▸</span>
              <h3 class="phase-title">${EVRE_TITLES[e]}</h3>
            </div>
            <span class="phase-badge">${phaseReadCount} / 30 Okundu</span>
          </div>
          <div class="phase-content" id="phase-content-${e}">
            <div class="phase-books-list">
              <!-- Books populated here -->
            </div>
          </div>
        `;
        
        const booksList = phaseDiv.querySelector(".phase-books-list");
        
        phaseBooks.forEach(b => {
          const bookItem = document.createElement("div");
          bookItem.className = `book-item-row ${readBooks.includes(b.no) ? 'is-read' : ''}`;
          
          const titleHtml = b.link 
            ? `<a href="${b.link}" class="book-title-link">${b.title}</a>` 
            : `<span class="book-title-text">${b.title}</span>`;
            
          const summaryBtnHtml = b.hasSummary
            ? `<a href="#/book/${b.no}/summary" class="book-summary-btn">📖 Özet Oku</a>`
            : '';
            
          bookItem.innerHTML = `
            <div class="book-check-col">
              <input type="checkbox" id="book-check-${b.no}" ${readBooks.includes(b.no) ? 'checked' : ''} data-no="${b.no}">
            </div>
            <div class="book-info-col">
              <div class="book-title-row">
                <span class="book-no">#${b.no}</span>
                <strong class="book-author">${b.author}</strong> — ${titleHtml}
                ${summaryBtnHtml}
              </div>
              <div class="book-details-expanded">
                <div class="book-meta-row">
                  <span class="book-category-tag">Kategori: ${b.category}</span>
                  ${b.pubDate ? `<span class="book-pub-date">Yıl: ${b.pubDate}</span>` : ''}
                </div>
                <p class="book-desc">${b.description}</p>
              </div>
            </div>
          `;
          
          // Checkbox event listener
          const checkbox = bookItem.querySelector('input[type="checkbox"]');
          checkbox.addEventListener("change", (event) => {
            const num = b.no;
            if (event.target.checked) {
              if (!readBooks.includes(num)) readBooks.push(num);
              bookItem.classList.add("is-read");
            } else {
              readBooks = readBooks.filter(n => n !== num);
              bookItem.classList.remove("is-read");
            }
            localStorage.setItem("zg_read_books", JSON.stringify(readBooks));
            updateRoadmapProgress();
            
            // Update phase badge count
            const currentPhaseReadCount = phaseBooks.filter(pb => readBooks.includes(pb.no)).length;
            phaseDiv.querySelector(".phase-badge").textContent = `${currentPhaseReadCount} / 30 Okundu`;
          });
          
          // Click handler to toggle description accordion
          const infoCol = bookItem.querySelector(".book-info-col");
          if (infoCol) {
            infoCol.addEventListener("click", (e) => {
              // Ignore clicks on links or buttons (like summary link)
              if (e.target.closest("a") || e.target.closest("button") || e.target.closest("input")) {
                return;
              }
              
              const isCurrentlyExpanded = bookItem.classList.contains("is-expanded");
              
              // Collapse all other book descriptions
              document.querySelectorAll(".book-item-row.is-expanded").forEach(row => {
                row.classList.remove("is-expanded");
              });
              
              // Toggle current row
              if (!isCurrentlyExpanded) {
                bookItem.classList.add("is-expanded");
              }
            });
          }
          
          booksList.appendChild(bookItem);
        });
        
        // Accordion click handler
        const header = phaseDiv.querySelector(".phase-header");
        header.addEventListener("click", () => {
          const isOpen = phaseDiv.classList.contains("is-open");
          if (isOpen) {
            phaseDiv.classList.remove("is-open");
          } else {
            phaseDiv.classList.add("is-open");
          }
        });
        
        phasesContainer.appendChild(phaseDiv);
      }
      
      updateRoadmapProgress();
      
    } catch (error) {
      console.error("Error setting up roadmap:", error);
      phasesContainer.innerHTML = `<div class="loading-placeholder">Yol haritası yüklenemedi.</div>`;
    }
  }

  // Load Book Summary Dynamically
  async function loadBookSummary(bookNo) {
    const readerTitle = document.getElementById("reader-book-title");
    const readerAuthor = document.getElementById("reader-book-author");
    const readerNo = document.getElementById("reader-book-no");
    const readerSubtitle = document.getElementById("reader-book-subtitle");
    const readerOriginal = document.getElementById("reader-meta-original");
    const readerCompiler = document.getElementById("reader-meta-compiler");
    const readerDate = document.getElementById("reader-meta-date");
    const readerIntro = document.getElementById("reader-intro-text");
    const readerChapters = document.getElementById("reader-chapters-list");
    const readerCoverImg = document.getElementById("reader-featured-img");
    
    if (!readerTitle || !readerChapters) return;
    
    readerChapters.innerHTML = `<div class="loading-placeholder">Özet yükleniyor...</div>`;
    
    try {
      const response = await fetch(`/data/summaries/${bookNo}.json?t=${new Date().getTime()}`);
      if (!response.ok) throw new Error("Summary file not found");
      const data = await response.json();
      
      readerTitle.textContent = data.title;
      readerAuthor.textContent = data.author;
      readerNo.textContent = `#${data.bookNo}`;
      readerSubtitle.textContent = data.subtitle || "";
      
      if (readerCoverImg) {
        readerCoverImg.src = data.coverImage || "/images/hawking_space_time_sketch.png";
      }
      
      if (readerOriginal) readerOriginal.textContent = data.meta.originalTitle || "";
      if (readerCompiler) readerCompiler.textContent = data.meta.compiler || "";
      if (readerDate) readerDate.textContent = data.meta.date || "";
      
      if (readerIntro) {
        readerIntro.innerHTML = `<h3>Giriş: Kozmosun Büyüleyici Arayışı</h3><p>${data.intro}</p>`;
      }
      
      readerChapters.innerHTML = "";
      data.chapters.forEach(ch => {
        const chDiv = document.createElement("div");
        chDiv.className = "reader-chapter-section";
        
        let paragraphsHtml = "";
        ch.paragraphs.forEach(p => {
          let text = p.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
          text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
          paragraphsHtml += `<p class="reader-paragraph">${text.replace(/\n/g, '<br>')}</p>`;
        });
        
        const hasMedia = (ch.image || ch.takeaway) ? true : false;
        
        let mediaHtml = '';
        if (hasMedia) {
          mediaHtml += `<div class="reader-chapter-media">`;
          if (ch.image) {
            mediaHtml += `
              <div class="reader-chapter-img-box">
                <img src="${ch.image}" class="reader-chapter-img" alt="${ch.imageCaption || ''}">
                ${ch.imageCaption ? `<span class="reader-chapter-caption">${ch.imageCaption}</span>` : ''}
              </div>
            `;
          }
          if (ch.takeaway) {
            mediaHtml += `
              <div class="reader-takeaway-card">
                <span class="takeaway-badge">Bölümün Özü</span>
                <p class="takeaway-text">“${ch.takeaway}”</p>
              </div>
            `;
          }
          mediaHtml += `</div>`;
        }
        
        chDiv.innerHTML = `
          <h3 class="reader-chapter-title">${ch.title}</h3>
          <div class="reader-chapter-wrapper ${hasMedia ? 'has-media' : ''}">
            <div class="reader-chapter-text">
              ${paragraphsHtml}
            </div>
            ${mediaHtml}
          </div>
        `;
        readerChapters.appendChild(chDiv);
      });
      
      updateMetaTags(
        `Zihin Gezgini | ${data.title} Özeti`,
        `${data.title} eserinin en anlaşılır felsefi ve bilimsel özeti.`,
        "https://zihingezgini.net/images/hawking_space_time_sketch.png"
      );
      
    } catch (error) {
      console.error("Error loading book summary:", error);
      readerChapters.innerHTML = `<div class="loading-placeholder">Özet yüklenemedi.</div>`;
    }
  }

  // Routing
  function handleRoute() {

    const hash = window.location.hash || "#/";
    
    // Reset active nav links
    Object.values(navLinks).forEach(link => {
      if (link) link.classList.remove("active");
    });
    
    // Hide all views
    Object.values(views).forEach(view => {
      if (view) view.classList.remove("active");
    });
    
    if (hash === "#/random") {
      if (allPosts.length > 0) {
        const randomPost = allPosts[Math.floor(Math.random() * allPosts.length)];
        window.location.hash = `#/post/${randomPost.slug}`;
      } else {
        // Fetch index first if empty
        fetch(`/data/posts.json?t=${new Date().getTime()}`)
          .then(res => res.json())
          .then(data => {
            allPosts = data;
            const randomPost = allPosts[Math.floor(Math.random() * allPosts.length)];
            window.location.hash = `#/post/${randomPost.slug}`;
          })
          .catch(() => {
            window.location.hash = "#/";
          });
      }
      return;
    }
    
    if (hash === "#/" || hash === "") {
      views.home.classList.add("active");
      if (navLinks.home) navLinks.home.classList.add("active");
      updateMetaTags(
        "Zihin Gezgini | Yazılar",
        "Hayatın ritminden kaçanlar, anı yaşamak isteyenler ve filozof monologları üzerine felsefi düşünceler.",
        "https://zihingezgini.net/images/thinking_man_sketch.png"
      );
      postsToShow = 9; // Reset pagination!
      // Refresh list
      if (allPosts.length === 0) {
        loadPostsIndex();
      } else {
        renderPostsGrid();
      }
    } else if (hash === "#/about") {
      views.about.classList.add("active");
      if (navLinks.about) navLinks.about.classList.add("active");
      updateMetaTags(
        "Zihin Gezgini | Zihin Odası",
        "Zihin Odası Üzerine: Gürültüden kaçış, kişisel felsefi notlar ve yavaş yaşama denemeleri.",
        "https://zihingezgini.net/images/thinking_man_sketch.png"
      );
    } else if (hash === "#/roadmap") {
      views.roadmap.classList.add("active");
      if (navLinks.roadmap) navLinks.roadmap.classList.add("active");
      updateMetaTags(
        "Zihin Gezgini | Entelektüel Yol Haritası",
        "Zihin Gezgini: 10 Evre ve 300 seçkin eserden oluşan interaktif entelektüel okuma rehberi.",
        "https://zihingezgini.net/images/thinking_man_sketch.png"
      );
      setupRoadmap();
    } else if (hash.startsWith("#/book/") && hash.endsWith("/summary")) {
      const match = hash.match(/#\/book\/(\d+)\/summary/);
      if (match) {
        const bookNo = parseInt(match[1]);
        if (views.bookSummary) {
          views.bookSummary.classList.add("active");
          loadBookSummary(bookNo);
        } else {
          window.location.hash = "#/";
        }
      } else {
        window.location.hash = "#/";
      }
    } else if (hash.startsWith("#/post/")) {
      const slug = hash.replace("#/post/", "");
      views.post.classList.add("active");
      loadPostDetail(slug);
    } else {
      // Fallback to home
      window.location.hash = "#/";
    }
    
    // Scroll to top on page change
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  // Search Form & Input Handlers
  const searchForm = document.getElementById("search-form");
  const searchInput = document.getElementById("search-input");
  
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      searchQuery = e.target.value.toLowerCase().trim();
      postsToShow = 9; // Reset pagination!
      renderPostsGrid();
    });
  }
  
  if (searchForm) {
    searchForm.addEventListener("submit", (e) => {
      e.preventDefault(); // Stop page reload!
      if (searchInput) {
        searchQuery = searchInput.value.toLowerCase().trim();
        postsToShow = 9; // Reset pagination!
        renderPostsGrid();
      }
    });
  }

  // Category Filtering Event Handlers
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentCategory = btn.getAttribute("data-category");
      postsToShow = 9; // Reset pagination!
      renderPostsGrid();
    });
  });

  // Theme Toggle Logic
  const themeToggleBtn = document.getElementById("theme-toggle");
  
  // Read saved theme or default to dark
  const savedTheme = localStorage.getItem("zg_theme") || "dark";
  if (savedTheme === "dark") {
    document.body.classList.add("dark-theme");
    if (themeToggleBtn) themeToggleBtn.textContent = "☀️";
  } else {
    document.body.classList.remove("dark-theme");
    if (themeToggleBtn) themeToggleBtn.textContent = "🌓";
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener("click", () => {
      const isDark = document.body.classList.toggle("dark-theme");
      localStorage.setItem("zg_theme", isDark ? "dark" : "light");
      themeToggleBtn.textContent = isDark ? "☀️" : "🌓";
    });
  }

  // Zihin Kırıntıları Quote Shuffler
  function setupQuoteWidget() {
    const widget = document.getElementById("quote-widget");
    const quoteText = widget ? widget.querySelector(".footer-quote-text") : null;
    const quoteAuthor = widget ? widget.querySelector(".footer-quote-author") : null;
    
    if (!widget || !quoteText || !quoteAuthor) return;
    
    function renderQuote(idx) {
      const q = quotes[idx];
      quoteText.textContent = `“${q.text}”`;
      quoteAuthor.innerHTML = `— ${q.author}, <a href="#/post/${q.slug}" class="quote-post-link">${q.title}</a>`;
    }
    
    // Initial quote render
    renderQuote(currentIndex);
    
    widget.addEventListener("click", (e) => {
      // If user clicked the link, let them navigate and do not shuffle the quote!
      if (e.target.closest("a")) {
        e.stopPropagation();
        return;
      }
      
      widget.classList.add("fade-out");
      
      setTimeout(() => {
        let newIndex = currentIndex;
        while (newIndex === currentIndex) {
          newIndex = Math.floor(Math.random() * quotes.length);
        }
        currentIndex = newIndex;
        
        renderQuote(currentIndex);
        widget.classList.remove("fade-out");
      }, 250);
    });
  }

  // Load Quotes Pool Dynamically
  async function loadQuotes() {
    try {
      const response = await fetch(`/data/quotes.json?t=${new Date().getTime()}`);
      if (!response.ok) throw new Error("Quotes file not found");
      quotes = await response.json();
      if (quotes.length > 0) {
        currentIndex = Math.floor(Math.random() * quotes.length);
        setupQuoteWidget();
      }
    } catch (error) {
      console.error("Error loading quotes:", error);
    }
  }

  // Guide Info Modal Event Listeners
  const guideModal = document.getElementById("guide-info-modal");
  const guideTrigger = document.getElementById("guide-info-trigger");
  const guideClose = document.getElementById("guide-modal-close");
  const guideBackdrop = document.getElementById("guide-modal-backdrop");
  
  if (guideTrigger && guideModal) {
    // Event delegation or direct binding (static element)
    guideTrigger.addEventListener("click", () => {
      guideModal.classList.add("is-active");
      document.body.style.overflow = "hidden"; // Prevent page scroll while reading modal
    });
  }
  
  function closeGuideModal() {
    if (guideModal) {
      guideModal.classList.remove("is-active");
      document.body.style.overflow = ""; // Restore scroll
    }
  }
  
  if (guideClose) guideClose.addEventListener("click", closeGuideModal);
  if (guideBackdrop) guideBackdrop.addEventListener("click", closeGuideModal);
  
  // Close guide modal on Escape key press
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeGuideModal();
    }
  });

  // Initialize App Elements
  loadQuotes();

  // Listen to hash change
  window.addEventListener("hashchange", handleRoute);
  
  // Initial route execution
  handleRoute();
});
