import os
import shutil
import subprocess
from dotenv import load_dotenv

# # Step 1: Common predefined paths

# Load environment variables
load_dotenv()

# Now access the paths
paths = {
    "1": ("Desktop", os.getenv("DESKTOP")),
    "2": ("Downloads", os.getenv("DOWNLOADS")),
    "3": ("Documents", os.getenv("DOCUMENTS")),
    "4": ("Music", os.getenv("MUSIC")),
    "5": ("Pictures", os.getenv("PICTURES"))
}



# Let user select one
print("📁 Choose a folder to work with:")
for key, (label, _) in paths.items():
    print(f"{key}. {label}")

choice = input("Enter the number of your choice: ")
if choice not in paths:
    print("❌ Invalid choice. Exiting...")
    exit()

folder_label, path = paths[choice]
print(f"\n✅ You selected: {folder_label} ({path})\n")

# --- FILE SEARCH ---
name = input("🔍 Enter file name to search: ")
files = [f for f in os.listdir(path) if f.startswith(name)]

if files:
    print("\n📄 Matching files:")
    for file in files:
        print(file)
else:
    print("❌ No files found.")

# file open 
files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
print("\n📄 Available files:")
for file in files:
    print(file)
file_name = input("\n🔍 Enter file name to open: ")

if file_name in files:
    file_path = os.path.join(path, file_name)
    print(f"📄 Opening file: {file_path}")
    os.startfile(file_path)
else:
    print(f"❌ File '{file_name}' does not exist.")


# --- FOLDER SEARCH ---
folder_serch = input("\n🔍 Enter folder name to search: ")
if folder_serch in os.listdir(path):
    folder_path = os.path.join(path, folder_serch)
    print(f"📂 Folder found: {folder_path}")
else:
    print("❌ Folder not found.")

# --- FOLDER LISTING ---
folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
print("\n📁 Available folders:")
for folder in folders:
    print(folder)

vscode_path = os.getenv("VSCODE_PATH")

# --- OPEN FOLDER ---
folder_name = input("\n📂 Enter the folder name to open: ")
if folder_name in folders:
    folder_path = os.path.join(path, folder_name)
    print(f"📂 Opening folder: {folder_path}")
    
    confirm = input("Do you want to open this folder in the default file Vs code? (yes/no): ")
    if confirm.lower() == 'yes':
        try:
            subprocess.run([vscode_path, folder_path], check=True)
        except FileNotFoundError:
            print("❌ VS Code not found at default path. Trying alternatives...")
            # Try alternative paths
            alternative_paths = [
                r"C:\Program Files\Microsoft VS Code\bin\code.cmd",
                r"C:\Program Files (x86)\Microsoft VS Code\bin\code.cmd",
                r"C:\Users\adhik\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            ]
            
            for code_path in alternative_paths:
                if os.path.exists(code_path):
                    subprocess.run([code_path, folder_path])
                    break
            else:
                print("❌ Could not find VS Code executable. Please open manually.")
    else:
        os.startfile(folder_path)
else:
    print(f"❌ Folder '{folder_name}' does not exist.")

# --- CREATE FOLDER ---
folder_name = input("\n➕ Enter the folder name to create: ")
full_path = os.path.join(path, folder_name)
if not os.path.exists(full_path):
    os.makedirs(full_path)
    print(f"✅ Folder '{folder_name}' created at {full_path}")
else:
    print(f"⚠️ Folder '{folder_name}' already exists.")

# --- DELETE FOLDER ---
folder_to_delete = input("\n🗑️ Enter the folder name to delete: ")
folder_to_delete_path = os.path.join(path, folder_to_delete)
if os.path.exists(folder_to_delete_path) and os.path.isdir(folder_to_delete_path):
    confirm = input(f"❗ Are you sure you want to delete '{folder_to_delete}'? (yes/no): ")
    if confirm.lower() == 'yes':
        shutil.rmtree(folder_to_delete_path)
        print(f"✅ Folder '{folder_to_delete}' deleted successfully.")
    else:
        print("🚫 Deletion cancelled.")
else:
    print(f"❌ Folder '{folder_to_delete}' does not exist.")
