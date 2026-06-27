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
    about: document.getElementById("nav-about")
  };
  
  const postsGrid = document.getElementById("posts-grid");
  const postDetail = document.getElementById("post-detail");
  const filterBtns = document.querySelectorAll(".filter-btn");
  
  let allPosts = [];
  let currentCategory = "all";

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
    
    const filteredPosts = currentCategory === "all" 
      ? allPosts 
      : allPosts.filter(p => p.category === currentCategory);
      
    if (filteredPosts.length === 0) {
      postsGrid.innerHTML = `<div class="loading-placeholder">Bu kategoride henüz bir yazı bulunmuyor.</div>`;
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
        
      // Clear duplicate title from content if it matches the main title
      let cleanContent = post.content;
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

      postDetail.innerHTML = `
        <button class="post-back-btn" onclick="window.location.hash = '#/'">
          ← Geri Dön
        </button>
        <header class="post-meta">
          <div class="post-detail-category">${post.category || 'Düşünce'}</div>
          <h1 class="post-detail-title">${post.title}</h1>
          <div class="post-detail-date">${formatDate(post.date)}</div>
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

  // Routing
  function handleRoute() {
    const hash = window.location.hash || "#/";
    
    // Reset active nav links
    Object.values(navLinks).forEach(link => link.classList.remove("active"));
    
    // Hide all views
    Object.values(views).forEach(view => view.classList.remove("active"));
    
    if (hash === "#/" || hash === "") {
      views.home.classList.add("active");
      navLinks.home.classList.add("active");
      document.title = "Zihin Gezgini | Yazılar";
      // Refresh list
      if (allPosts.length === 0) {
        loadPostsIndex();
      } else {
        renderPostsGrid();
      }
    } else if (hash === "#/about") {
      views.about.classList.add("active");
      navLinks.about.classList.add("active");
      document.title = "Zihin Gezgini | Zihin Odası";
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
  
  // Read saved theme or default to light
  const savedTheme = localStorage.getItem("zg_theme") || "light";
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
