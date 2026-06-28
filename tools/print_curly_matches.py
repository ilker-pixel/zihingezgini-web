def print_curly_depths():
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
                    print(f"Extra closing brace at line {line_num}, col {char_idx}")
                    continue
                open_line, open_col = stack.pop()
                if len(stack) == 0:
                    print(f"Depth 0: closed {{ opened at line {open_line}, col {open_col} by }} at line {line_num}, col {char_idx}")
                elif len(stack) == 1:
                    print(f"Depth 1: closed {{ opened at line {open_line}, col {open_col} by }} at line {line_num}, col {char_idx}")

if __name__ == "__main__":
    print_curly_depths()
