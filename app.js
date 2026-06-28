// Zihin Gezgini - Core Application Script

document.addEventListener("DOMContentLoaded", () => {
  // Router elements
  const views = {
    home: document.getElementById("view-home"),
    post: document.getElementById("view-post"),
    about: document.getElementById("view-about")
  };
  
  const navLinks = {
    home: document.getElementById("nav-home"),
    about: document.getElementById("nav-about"),
    random: document.getElementById("nav-random")
  };
  
  const postsGrid = document.getElementById("posts-grid");
  const postDetail = document.getElementById("post-detail");
  const filterBtns = document.querySelectorAll(".filter-btn");
  
  let allPosts = [];
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
          <div class="post-actions-right">
            <button id="toggle-focus-btn" class="post-focus-btn" title="Odaklanma Modu">👁 Odak Modu</button>
            <div class="font-size-adjuster">
              <button id="font-dec" title="Yazıyı Küçült">A-</button>
              <button id="font-inc" title="Yazıyı Büyüt">A+</button>
            </div>
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

      // Setup Focus Mode Event Listener
      setupFocusMode();

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

  // Setup Focus Mode
  function setupFocusMode() {
    const focusBtn = document.getElementById("toggle-focus-btn");
    if (focusBtn) {
      focusBtn.addEventListener("click", () => {
        const isFocus = document.body.classList.toggle("focus-mode");
        focusBtn.classList.toggle("active", isFocus);
        focusBtn.innerHTML = isFocus ? "👁 Odaktan Çık" : "👁 Odak Modu";
      });
    }
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
    
    list.parentNode.insertBefore(progressContainer, list);
    
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

  // Routing
  function handleRoute() {
    // Automatically turn off focus mode on page navigation
    document.body.classList.remove("focus-mode");

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
    
    const quotes = [
      { text: "Uygulamaya koymadıkça, bilgi değersizdir.", author: "Anton Çehov" },
      { text: "İnsanoğlu Yirminci yüzyılda yaşıyor olsa da; çoğu insanın beyni Taş devrinde yaşıyor.", author: "Erich Fromm" },
      { text: "Kuantum fiziği kafanızı karıştırmadıysa, onu tam olarak anlamamışsınız demektir.", author: "Niels Bohr" },
      { text: "Gerçek keşif, yeni topraklar bulmak değil, yeni gözlerle bakmaktır.", author: "Marcel Proust" },
      { text: "Düşünüyorum, öyleyse varım.", author: "René Descartes" },
      { text: "Hayatın bir sanat olduğunu kabul eden bir insan beyni, bir süre sonra kalbinin yerini alır.", author: "Oscar Wilde" },
      { text: "Hayat geriye doğru anlaşılır, ama ileriye doğru yaşanmalıdır.", author: "Søren Kierkegaard" },
      { text: "Mutluluk, arzu edilmeyen şeyleri istememekten geçer.", author: "Arthur Schopenhauer" },
      { text: "İnsan insanın kurdudur.", author: "Thomas Hobbes" },
      { text: "Aklın kurnazlığı, diyalektik süreçte gizlidir.", author: "Friedrich Hegel" }
    ];
    
    let currentIndex = Math.floor(Math.random() * quotes.length);
    quoteText.textContent = `“${quotes[currentIndex].text}”`;
    quoteAuthor.textContent = `— ${quotes[currentIndex].author}`;
    
    widget.addEventListener("click", () => {
      widget.classList.add("fade-out");
      
      setTimeout(() => {
        let newIndex = currentIndex;
        while (newIndex === currentIndex) {
          newIndex = Math.floor(Math.random() * quotes.length);
        }
        currentIndex = newIndex;
        
        quoteText.textContent = `“${quotes[currentIndex].text}”`;
        quoteAuthor.textContent = `— ${quotes[currentIndex].author}`;
        widget.classList.remove("fade-out");
      }, 250);
    });
  }

  // Initialize Quote Widget
  setupQuoteWidget();

  // Listen to hash change
  window.addEventListener("hashchange", handleRoute);
  
  // Initial route execution
  handleRoute();
});
