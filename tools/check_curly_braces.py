def check_curly_braces():
    with open("app.js", "r", encoding="utf-8") as f:
        content = f.read()
        
    stack = []
    lines = content.split("\n")
    for line_num, line in enumerate(lines, 1):
        for char_idx, char in enumerate(line, 1):
            if char == "{":
                stack.append((line_num, char_idx))
            elif char == "}":
                if not stack:
                    print(f"Extra closing brace '}}' at line {line_num}, col {char_idx}")
                    return
                stack.pop()
                
    if stack:
        print("Unclosed curly braces at end of file:")
        for line_num, char_idx in stack:
            print(f"  {{ opened at line {line_num}, col {char_idx}")
    else:
        print("Curly braces are perfectly balanced!")

if __name__ == "__main__":
    check_curly_braces()
