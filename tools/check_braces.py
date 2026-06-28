def check_braces():
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
                    return False
                top_char, top_line, top_col = stack.pop()
                if (char == "}" and top_char != "{") or \
                   (char == "]" and top_char != "[") or \
                   (char == ")" and top_char != "("):
                    print(f"Mismatched closing character '{char}' at line {line_num}, col {char_idx} matches '{top_char}' at line {top_line}, col {top_col}")
                    return False
                    
    if stack:
        print("Unclosed open characters left at end of file:")
        for item in stack:
            print(f"  '{item[0]}' opened at line {item[1]}, col {item[2]}")
        return False
        
    print("Braces, brackets and parentheses are perfectly balanced!")
    return True

if __name__ == "__main__":
    check_braces()
