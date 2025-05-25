import os
import shutil

# # Step 1: Common predefined paths
paths = {
    "1": ("Desktop", "C:/Users/adhik/OneDrive/Desktop"),
    "2": ("Downloads", "C:/Users/adhik/Downloads"),
    "3": ("Documents", "C:/Users/adhik/Documents"),
    "4": ("Music", "C:/Users/adhik/Music"),
    "5": ("Pictures", "C:/Users/adhik/Pictures")
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

# --- OPEN FOLDER ---
folder_name = input("\n📂 Enter the folder name to open: ")
if folder_name in folders:
    folder_path = os.path.join(path, folder_name)
    print(f"📂 Opening folder: {folder_path}")
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
