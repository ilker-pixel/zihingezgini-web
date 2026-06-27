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
    
    const filteredPosts = allPosts.filter(post => {
      const matchesCategory = currentCategory === "all" || post.category === currentCategory;
      const matchesSearch = searchQuery === "" || 
        post.title.toLowerCase().includes(searchQuery) ||
        (post.category && post.category.toLowerCase().includes(searchQuery));
      return matchesCategory && matchesSearch;
    });
      
    if (filteredPosts.length === 0) {
      postsGrid.innerHTML = `<div class="loading-placeholder">Aradığınız kriterlere uygun bir yazı bulunamadı.</div>`;
      return;
    }
    
    filteredPosts.forEach(post => {
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
            ${youtubeUrl ? `• <a href="${youtubeUrl}" target="_blank" class="post-listen-btn">🎧 Monologu Dinle ↗</a>` : ""}
          </div>
        </header>
        ${imgHtml}
        <div class="post-body">
          ${cleanContent}
        </div>
        <div class="post-subscribe-section">
          <h3>Zihin Gezgini E-Bülten</h3>
          <p>Her hafta yeni filozof monologlarından ve felsefi karalamalardan haberdar olmak için bültene katılın.</p>
          <a href="https://zihingezgini.substack.com" target="_blank" class="subscribe-btn">Substack'te Abone Ol ↗</a>
        </div>
      `;

      // Setup Font Size Adjuster Event Listeners
      setupFontSizeAdjuster();

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
      renderPostsGrid();
    });
  }
  
  if (searchForm) {
    searchForm.addEventListener("submit", (e) => {
      e.preventDefault(); // Stop page reload!
      if (searchInput) {
        searchQuery = searchInput.value.toLowerCase().trim();
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

  // Listen to hash change
  window.addEventListener("hashchange", handleRoute);
  
  // Initial route execution
  handleRoute();
});
