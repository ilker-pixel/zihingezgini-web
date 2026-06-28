def check_roadmap_braces():
    with open("app.js", "r", encoding="utf-8") as f:
        content = f.read()
        
    start_str = "async function setupRoadmap()"
    start_idx = content.find(start_str)
    if start_idx == -1:
        print("setupRoadmap not found")
        return
        
    # We will trace from start_idx onwards
    stack = []
    i = start_idx
    while i < len(content):
        char = content[i]
        # We also need to know the line and column
        # Let's compute them
        prefix = content[:i]
        line_num = prefix.count("\n") + 1
        char_idx = len(prefix) - prefix.rfind("\n")
        
        if char in "{[(":
            stack.append((char, line_num, char_idx))
        elif char in "}])":
            if not stack:
                print(f"Extra closing character '{char}' at line {line_num}, col {char_idx} (outside setupRoadmap outer brace!)")
                return
            top_char, top_line, top_col = stack.pop()
            if (char == "}" and top_char != "{") or \
               (char == "]" and top_char != "[") or \
               (char == ")" and top_char != "("):
                print(f"Mismatch: '{char}' at line {line_num}, col {char_idx} matches '{top_char}' at line {top_line}, col {top_col}")
                return
            
            # If stack becomes empty, we have closed setupRoadmap function!
            if not stack:
                print(f"setupRoadmap closed successfully at line {line_num}, col {char_idx}")
                # Print next 50 chars to see what follows
                print("Next content:", content[i+1:i+100])
                return
        i += 1

if __name__ == "__main__":
    check_roadmap_braces()
