import os
import re
import shutil
import tkinter as tk
from tkinter import filedialog
from colorama import init, Fore, Style
from itertools import cycle

init(autoreset=True)
tk.Tk().withdraw()

ASCII_LOGO = r'''
 _______   _______    ______   _______   __    __   ______  ________  ______  ________  __      __ 
|       \ |       \  /      \ |       \ |  \  |  \ /      \|        \|      \|        \|  \    /  \
| $$$$$$$\| $$$$$$$\|  $$$$$$\| $$$$$$$\| $$  | $$|  $$$$$$\\$$$$$$$$ \$$$$$$| $$$$$$$$ \$$\  /  $$ 
| $$__/ $$| $$__| $$| $$  | $$| $$  | $$| $$  | $$| $$   \$$  | $$     | $$  | $$__      \$$\/  $$  
| $$    $$| $$    $$| $$  | $$| $$  | $$| $$  | $$| $$        | $$     | $$  | $$  \      \$$  $$   
| $$$$$$$ | $$$$$$$\| $$  | $$| $$  | $$| $$  | $$| $$   __   | $$     | $$  | $$$$$       \$$$$    
| $$      | $$  | $$| $$__/ $$| $$__/ $$| $$__/ $$| $$__/  \  | $$    _| $$_ | $$          | $$     
| $$      | $$  | $$ \$$    $$| $$    $$ \$$    $$ \$$    $$  | $$   |   $$ \| $$          | $$     
 \$$       \$$   \$$  \$$$$$$  \$$$$$$$   \$$$$$$   \$$$$$$    \$$    \$$$$$$ \$$           \$$     
                                                                                                    
'''

def print_rainbow_logo():
    colors = cycle([Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA])
    for line in ASCII_LOGO.splitlines():
        colored_line = ''
        for char in line:
            if char == ' ':
                colored_line += ' '
            else:
                colored_line += next(colors) + char
        print(colored_line)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def compress_html(content):
    return re.sub(r">\s+<", "><", re.sub(r"\s+", " ", content.strip()))

def compress_css(content):
    content = re.sub(r"\s+", " ", content)
    content = re.sub(r":\s*", ":", content)
    content = re.sub(r";\s*", ";", content)
    return content.strip()

def compress_js(content):
    return re.sub(r"\s+", " ", content.strip())

def compress_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    ext = os.path.splitext(filepath)[1]
    if ext == '.html':
        return compress_html(content)
    elif ext == '.css':
        return compress_css(content)
    elif ext == '.js':
        return compress_js(content)
    return None

def should_ignore(path, is_node):
    if not is_node:
        return False
    return any(part in ['node_modules', 'package.json', 'package-lock.json'] for part in path.split(os.sep))

def productify():
    clear()
    print_rainbow_logo()
    print(Fore.YELLOW + "\n[+] Select your project folder:")
    src_folder = filedialog.askdirectory()
    if not src_folder:
        print(Fore.RED + "[-] No folder selected.")
        input(Fore.YELLOW + "\nPress Enter to return to the menu...")
        return

    nodejs = input(Fore.CYAN + "[?] Is this a Node.js project? (y/n): ").strip().lower() == 'y'

    clear()
    print_rainbow_logo()
    print(Fore.YELLOW + "\n[+] Scanning and compressing files...\n")
    compressed_files = []

    for root, dirs, files in os.walk(src_folder):
        if should_ignore(root, nodejs):
            continue
        for file in files:
            filepath = os.path.join(root, file)
            if should_ignore(filepath, nodejs):
                continue
            ext = os.path.splitext(file)[1]
            if ext in ['.html', '.css', '.js']:
                relative_path = os.path.relpath(filepath, src_folder)
                compressed = compress_file(filepath)
                if compressed:
                    compressed_files.append((relative_path, compressed))
                    print(Fore.GREEN + f"[>] {relative_path} compressed...")

    if not compressed_files:
        print(Fore.RED + "[-] No compressible files found.")
        input(Fore.YELLOW + "\nPress Enter to return to the menu...")
        return

    print(Fore.YELLOW + "\n[+] Select where to save the compressed project:")
    dest_folder = filedialog.askdirectory()
    if not dest_folder:
        print(Fore.RED + "[-] No destination folder selected.")
        input(Fore.YELLOW + "\nPress Enter to return to the menu...")
        return

    for rel_path, compressed in compressed_files:
        out_path = os.path.join(dest_folder, rel_path)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(compressed)

    print(Fore.GREEN + "\n[>] All files compressed and saved successfully!")
    os.startfile(dest_folder)
    input(Fore.YELLOW + "\nPress Enter to return to the menu...")

def show_about():
    clear()
    print_rainbow_logo()
    print(Fore.RED + "\n[ABOUT]")
    print("This script compresses HTML, CSS, and JS files in a project folder.")
    print("Compression reduces the size of HTML, CSS, and JavaScript files by removing unnecessary spaces, comments, and formatting.")
    print("This makes websites load faster, improves performance, and saves bandwidth — especially important for users on slow connections. It also helps clean up the code for deployment while keeping all functionality intact.")
    print(Fore.CYAN + "Developed by: A Dev Named DeLL\n")
    input(Fore.YELLOW + "Press Enter to return to the menu...")

def main_menu():
    while True:
        clear()
        print_rainbow_logo()
        print(Fore.MAGENTA + "\n[MENU]")
        print("1. productify")
        print("2. about")
        print(Fore.RED + "3. exit")

        choice = input(Fore.CYAN + "\nEnter your choice: ").strip()
        if choice == '1':
            productify()
        elif choice == '2':
            show_about()
        elif choice == '3':
            clear()
            print(Fore.YELLOW + "Exiting...\n")
            break
        else:
            print(Fore.RED + "Invalid option. Try again.")
            input(Fore.YELLOW + "\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()
