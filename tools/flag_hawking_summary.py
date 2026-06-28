import json

def flag_summary():
    path = "data/books.json"
    with open(path, "r", encoding="utf-8") as f:
        books = json.load(f)
        
    for b in books:
        if b["no"] == 1:
            b["hasSummary"] = True
            print("Flagged book 1 in books.json!")
            break
            
    with open(path, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    flag_summary()
