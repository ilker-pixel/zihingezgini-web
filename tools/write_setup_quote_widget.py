import json

def write_widget():
    app_js_path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/app.js"
    mapped_quotes_path = "/Users/ilker/.gemini/antigravity-ide/scratch/zihingezgini-web/tools/mapped_quotes_100.json"
    
    with open(mapped_quotes_path, "r", encoding="utf-8") as f:
        quotes = json.load(f)
        
    js_quotes_lines = []
    for q in quotes:
        text = q["text"].replace('"', '\\"')
        title = q["title"].replace('"', '\\"')
        slug = q["slug"]
        js_quotes_lines.append(f'      {{ text: "{text}", author: "Zihin Gezgini", title: "{title}", slug: "{slug}" }}')
        
    quotes_array_str = ",\n".join(js_quotes_lines)
    
    # Use normal string template without f-string to prevent brace issues
    new_function_str = """  // Zihin Kırıntıları Quote Shuffler
  function setupQuoteWidget() {
    const widget = document.getElementById("quote-widget");
    const quoteText = widget ? widget.querySelector(".footer-quote-text") : null;
    const quoteAuthor = widget ? widget.querySelector(".footer-quote-author") : null;
    
    if (!widget || !quoteText || !quoteAuthor) return;
    
    const quotes = [
__QUOTES_PLACEHOLDER__
    ];
    
    let currentIndex = Math.floor(Math.random() * quotes.length);
    
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
  }""".replace("__QUOTES_PLACEHOLDER__", quotes_array_str)

    with open(app_js_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    start_marker = "  // Zihin Kırıntıları Quote Shuffler"
    end_marker = "  // Initialize Quote Widget"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print("Error: Could not locate markers in app.js")
        return
        
    new_content = content[:start_idx] + new_function_str + "\n\n" + content[end_idx:]
    
    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("Successfully updated app.js with the new quote widget implementation!")

if __name__ == "__main__":
    write_widget()
