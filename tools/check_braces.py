import sys

def check_file_braces(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return False
        
    stack = []
    lines = content.split("\n")
    for line_num, line in enumerate(lines, 1):
        for char_idx, char in enumerate(line, 1):
            if char in "{[(":
                stack.append((char, line_num, char_idx))
            elif char in "}])":
                if not stack:
                    print(f"[{filename}] Extra closing character '{char}' at line {line_num}, col {char_idx}")
                    return False
                top_char, top_line, top_col = stack.pop()
                if (char == "}" and top_char != "{") or \
                   (char == "]" and top_char != "[") or \
                   (char == ")" and top_char != "("):
                    print(f"[{filename}] Mismatched closing character '{char}' at line {line_num}, col {char_idx} matches '{top_char}' at line {top_line}, col {top_col}")
                    return False
                    
    if stack:
        print(f"[{filename}] Unclosed open characters left at end of file:")
        for item in stack:
            print(f"  '{item[0]}' opened at line {item[1]}, col {item[2]}")
        return False
        
    print(f"[{filename}] Braces, brackets and parentheses are perfectly balanced!")
    return True

def main():
    files_to_check = ["app.js", "style.css"]
    all_ok = True
    for f in files_to_check:
        if not check_file_braces(f):
            all_ok = False
            
    if not all_ok:
        sys.exit(1)

if __name__ == "__main__":
    main()
