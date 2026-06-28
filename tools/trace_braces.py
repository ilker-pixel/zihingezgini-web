def trace_braces():
    with open("app.js", "r", encoding="utf-8") as f:
        content = f.read()
        
    stack = []
    lines = content.split("\n")
    for line_num, line in enumerate(lines, 1):
        for char_idx, char in enumerate(line, 1):
            if char in "{[(":
                stack.append((char, line_num, char_idx))
            elif char in "}])":
                if not stack:
                    print(f"Extra closing character '{char}' at line {line_num}, col {char_idx}")
                    return
                top_char, top_line, top_col = stack[-1]
                # Check if it matches
                is_match = False
                if char == "}" and top_char == "{": is_match = True
                elif char == "]" and top_char == "[": is_match = True
                elif char == ")" and top_char == "(": is_match = True
                
                if is_match:
                    stack.pop()
                else:
                    print(f"Mismatch encountered at line {line_num}, col {char_idx}: close '{char}' does not match stack top '{top_char}' opened at line {top_line}, col {top_col}")
                    print("Current active open brackets in stack (last 10):")
                    for s in stack[-10:]:
                        print(f"  '{s[0]}' opened at line {s[1]}, col {s[2]}")
                    return

    if stack:
        print("Unclosed open characters left:")
        for item in stack:
            print(f"  '{item[0]}' opened at line {item[1]}, col {item[2]}")
    else:
        print("Perfect!")

if __name__ == "__main__":
    trace_braces()
