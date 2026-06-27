// Zihin Gezgini - Admin Portal Script

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const configOverlay = document.getElementById("config-overlay");
  const configTriggerBtn = document.getElementById("config-trigger-btn");
  const configSaveBtn = document.getElementById("config-save-btn");
  const syncStatus = document.getElementById("sync-status");
  
  const ownerInput = document.getElementById("config-owner");
  const repoInput = document.getElementById("config-repo");
  const tokenInput = document.getElementById("config-token");
  
  const postTitle = document.getElementById("post-title");
  const postContent = document.getElementById("post-content");
  const postCategory = document.getElementById("post-category");
  const postDate = document.getElementById("post-date");
  
  const selectImgBtn = document.getElementById("select-img-btn");
  const featuredImgFile = document.getElementById("post-featured-image-file");
  const previewContainer = document.getElementById("preview-container");
  const featuredImgPreview = document.getElementById("featured-image-preview");
  
  const editorImgBtn = document.getElementById("editor-img-btn");
  const inlineImgFile = document.getElementById("editor-inline-image-file");
  
  const publishBtn = document.getElementById("publish-btn");
  const toast = document.getElementById("toast");
  
  // State
  let config = { owner: "", repo: "", token: "" };
  let featuredImageBase64 = null;
  let featuredImageName = null;

  // Initialize
  loadConfig();
  setDefaultDate();
  setupToolbarButtons();

  // Configuration management
  function loadConfig() {
    const saved = localStorage.getItem("zg_git_config");
    if (saved) {
      try {
        config = JSON.parse(saved);
        ownerInput.value = config.owner || "";
        repoInput.value = config.repo || "";
        tokenInput.value = config.token || "";
        
        if (config.owner && config.repo && config.token) {
          syncStatus.textContent = "BAĞLANDI";
          syncStatus.style.color = "#10b981"; // green
        } else {
          showConfigModal();
        }
      } catch (e) {
        showConfigModal();
      }
    } else {
      showConfigModal();
    }
  }

  function showConfigModal() {
    configOverlay.classList.remove("hidden");
  }

  function hideConfigModal() {
    configOverlay.classList.add("hidden");
  }

  configTriggerBtn.addEventListener("click", showConfigModal);

  configSaveBtn.addEventListener("click", () => {
    const owner = ownerInput.value.trim();
    const repo = repoInput.value.trim();
    const token = tokenInput.value.trim();
    
    if (!owner || !repo || !token) {
      showToast("Lütfen tüm alanları doldurun.");
      return;
    }
    
    config = { owner, repo, token };
    localStorage.setItem("zg_git_config", JSON.stringify(config));
    
    syncStatus.textContent = "BAĞLANDI";
    syncStatus.style.color = "#10b981";
    
    hideConfigModal();
    showToast("Bağlantı ayarları kaydedildi!");
  });

  // Default publication date set to current local time
  function setDefaultDate() {
    const now = new Date();
    // Offset local timezone
    const tzOffset = now.getTimezoneOffset() * 60000;
    const localISOTime = (new Date(now - tzOffset)).toISOString().slice(0, 16);
    postDate.value = localISOTime;
  }

  // Toast
  function showToast(message) {
    toast.textContent = message;
    toast.classList.add("show");
    setTimeout(() => {
      toast.classList.remove("show");
    }, 3000);
  }

  // Toolbar Formatting
  function setupToolbarButtons() {
    document.querySelectorAll(".toolbar-btn[data-tag]").forEach(btn => {
      btn.addEventListener("click", () => {
        const tag = btn.getAttribute("data-tag");
        insertTag(tag);
      });
    });
  }

  function insertTag(type) {
    const start = postContent.selectionStart;
    const end = postContent.selectionEnd;
    const text = postContent.value;
    const selected = text.substring(start, end);
    let replacement = "";
    
    switch(type) {
      case "b":
        replacement = `**${selected || 'kalın yaz'}**`;
        break;
      case "i":
        replacement = `*${selected || 'italik yaz'}*`;
        break;
      case "quote":
        replacement = `\n> ${selected || 'alıntı metni'}\n`;
        break;
      case "h2":
        replacement = `\n## ${selected || 'Başlık 2'}\n`;
        break;
      case "h3":
        replacement = `\n### ${selected || 'Başlık 3'}\n`;
        break;
    }
    
    postContent.value = text.substring(0, start) + replacement + text.substring(end);
    postContent.focus();
    postContent.setSelectionRange(start + replacement.length, start + replacement.length);
  }

  // Image Helper (Base64 file reader)
  function getBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        // Strip data:image/*;base64, header
        const base64Data = reader.result.split(',')[1];
        resolve(base64Data);
      };
      reader.onerror = error => reject(error);
    });
  }

  // Cover Image selection
  selectImgBtn.addEventListener("click", () => featuredImgFile.click());
  
  featuredImgFile.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (file) {
      try {
        featuredImageBase64 = await getBase64(file);
        featuredImageName = sanitizeFilename(file.name);
        
        // Show preview
        featuredImgPreview.src = URL.createObjectURL(file);
        featuredImgPreview.style.display = "block";
        document.querySelector(".preview-placeholder").style.display = "none";
        showToast("Kapak görseli seçildi.");
      } catch (err) {
        console.error(err);
        showToast("Görsel yüklenirken hata oluştu.");
      }
    }
  });

  // Inline Image selection
  editorImgBtn.addEventListener("click", () => inlineImgFile.click());

  inlineImgFile.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (file) {
      if (!config.token || !config.owner || !config.repo) {
        showToast("Lütfen önce GitHub bağlantı ayarlarını yapın.");
        return;
      }
      
      showToast("Görsel GitHub'a yükleniyor...");
      try {
        const base64 = await getBase64(file);
        const name = sanitizeFilename(file.name);
        const filename = `${Date.now()}-${name}`;
        
        const path = `images/${filename}`;
        await uploadToGithub(path, base64, `Upload inline image: ${filename}`);
        
        // Insert markdown tag into content
        const markdownTag = `\n![${name}](/images/${filename})\n`;
        const start = postContent.selectionStart;
        const end = postContent.selectionEnd;
        const text = postContent.value;
        
        postContent.value = text.substring(0, start) + markdownTag + text.substring(end);
        showToast("Görsel başarıyla eklendi!");
      } catch (err) {
        console.error(err);
        showToast("Görsel yüklenirken bir hata oluştu.");
      }
    }
  });

  function sanitizeFilename(name) {
    tr_map = {"ç":"c","ğ":"g","ı":"i","ö":"o","ş":"s","ü":"u","Ç":"C","Ğ":"G","İ":"I","Ö":"O","Ş":"S","Ü":"U"};
    let clean = name.replace(/[çğıöşüÇĞİÖŞÜ]/g, m => tr_map[m] || m);
    return clean.replace(/[^a-zA-Z0-9\.\-_]/g, '_').toLowerCase();
  }

  // GitHub API Wrapper
  async function uploadToGithub(path, contentBase64, commitMessage, sha = null) {
    const url = `https://api.github.com/repos/${config.owner}/${config.repo}/contents/${path}`;
    
    const body = {
      message: commitMessage,
      content: contentBase64
    };
    if (sha) {
      body.sha = sha;
    }
    
    const response = await fetch(url, {
      method: "PUT",
      headers: {
        "Authorization": `token ${config.token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    });
    
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.message || "GitHub API update failed");
    }
    return await response.json();
  }

  async function fetchFromGithub(path) {
    const url = `https://api.github.com/repos/${config.owner}/${config.repo}/contents/${path}`;
    const response = await fetch(url, {
      headers: {
        "Authorization": `token ${config.token}`
      }
    });
    
    if (response.status === 404) {
      return null;
    }
    
    if (!response.ok) {
      throw new Error("GitHub file fetch failed");
    }
    
    const data = await response.json();
    return data;
  }

  // Markdown parser to output clean HTML
  function markdownToHtml(md) {
    let html = md;
    // Headers
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h2>$1</h2>');
    
    // Images
    html = html.replace(/!\[(.*?)\]\((.*?)\)/gim, "<img src='$2' alt='$1' class='inline-image' />");
    
    // Bold & Italic
    html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');
    html = html.replace(/\*(.*?)\*/gim, '<em>$1</em>');
    
    // Blockquotes
    html = html.replace(/^\> (.*$)/gim, '<blockquote><p>$1</p></blockquote>');
    
    // Split to paragraphs, skipping block elements
    const lines = html.split('\n\n');
    const processedLines = lines.map(line => {
      line = line.trim();
      if (!line) return '';
      if (line.startsWith('<h') || line.startsWith('<blockquote') || line.startsWith('<img')) {
        return line;
      }
      return `<p>${line.replace(/\n/g, '<br>')}</p>`;
    });
    
    return processedLines.filter(l => l !== '').join('\n');
  }

  // Publish Post action
  publishBtn.addEventListener("click", async () => {
    const title = postTitle.value.trim();
    const contentMarkdown = postContent.value.trim();
    const category = postCategory.value;
    const dateStr = new Date(postDate.value).toISOString();
    
    if (!title || !contentMarkdown) {
      showToast("Lütfen Başlık ve İçerik alanlarını doldurun.");
      return;
    }
    
    if (!config.token || !config.owner || !config.repo) {
      showToast("Lütfen önce GitHub bağlantı ayarlarını yapın.");
      showConfigModal();
      return;
    }
    
    publishBtn.disabled = true;
    publishBtn.textContent = "Yükleniyor...";
    
    try {
      // 1. Generate Slug
      const tr_map = {"ç":"c","ğ":"g","ı":"i","ö":"o","ş":"s","ü":"u","Ç":"C","Ğ":"G","İ":"I","Ö":"O","Ş":"S","Ü":"U"};
      let slug = title.replace(/[çğıöşüÇĞİÖŞÜ]/g, m => tr_map[m] || m).toLowerCase();
      slug = slug.replace(/[^a-z0-9\s-]/g, '').trim().replace(/[\s-]+/g, '-');
      
      // 2. Upload cover image if exists
      let localFeaturedImage = null;
      if (featuredImageBase64) {
        const coverFilename = `${Date.now()}-${featuredImageName}`;
        showToast("Kapak görseli yükleniyor...");
        await uploadToGithub(`images/${coverFilename}`, featuredImageBase64, `Upload cover image: ${coverFilename}`);
        localFeaturedImage = `/images/${coverFilename}`;
      }
      
      // 3. Compile post HTML and JSON data
      const contentHtml = markdownToHtml(contentMarkdown);
      const postPayload = {
        title: title,
        date: dateStr,
        slug: slug,
        featuredImage: localFeaturedImage,
        content: contentHtml,
        category: category
      };
      
      const payloadBase64 = btoa(unescape(encodeURIComponent(JSON.stringify(postPayload, null, 4))));
      
      showToast("Yazı kaydediliyor...");
      // Check if post already exists to overwrite or create
      const postPath = `data/posts/${slug}.json`;
      const existingPostFile = await fetchFromGithub(postPath);
      const postSha = existingPostFile ? existingPostFile.sha : null;
      
      await uploadToGithub(postPath, payloadBase64, `Publish post: ${title}`, postSha);
      
      // 4. Update posts.json index
      showToast("Dizin güncelleniyor...");
      const indexPath = "data/posts.json";
      const indexFile = await fetchFromGithub(indexPath);
      
      let postsIndex = [];
      let indexSha = null;
      
      if (indexFile) {
        indexSha = indexFile.sha;
        // Decode base64
        const decodedIndex = decodeURIComponent(escape(atob(indexFile.content.replace(/\s/g, ''))));
        postsIndex = JSON.parse(decodedIndex);
      }
      
      // Remove previous entry with same slug if editing
      postsIndex = postsIndex.filter(p => p.slug !== slug);
      
      // Add new entry
      postsIndex.unshift({
        title: title,
        date: dateStr,
        slug: slug,
        featuredImage: localFeaturedImage,
        category: category
      });
      
      // Sort by date descending
      postsIndex.sort((a, b) => new Date(b.date) - new Date(a.date));
      
      const updatedIndexBase64 = btoa(unescape(encodeURIComponent(JSON.stringify(postsIndex, null, 4))));
      await uploadToGithub(indexPath, updatedIndexBase64, `Update posts index for: ${title}`, indexSha);
      
      showToast("Tebrikler! Yazınız başarıyla yayınlandı! 🚀");
      
      // Reset form
      postTitle.value = "";
      postContent.value = "";
      featuredImageBase64 = null;
      featuredImgPreview.style.display = "none";
      document.querySelector(".preview-placeholder").style.display = "block";
      setDefaultDate();
      
    } catch (err) {
      console.error(err);
      showToast(`Hata: ${err.message}`);
    } finally {
      publishBtn.disabled = false;
      publishBtn.textContent = "Yayına Al 🚀";
    }
  });
});
