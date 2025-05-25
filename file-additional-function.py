import os
import shutil
import subprocess
from dotenv import load_dotenv

load_dotenv()

def copy_file():
    src = input("📂 Enter source file path: ").strip()
    dest = input("📁 Enter destination folder path: ").strip()
    
    if os.path.isfile(src) and os.path.isdir(dest):
        try:
            shutil.copy(src, dest)
            print("✅ File copied successfully.")
        except Exception as e:
            print(f"❌ Error copying file: {e}")
    else:
        print("❌ Invalid source or destination.")

def move_file():
    src = input("📂 Enter source file path: ").strip()
    dest = input("📁 Enter destination folder path: ").strip()

    if os.path.isfile(src) and os.path.isdir(dest):
        try:
            shutil.move(src, dest)
            print("✅ File moved successfully.")
        except Exception as e:
            print(f"❌ Error moving file: {e}")
    else:
        print("❌ Invalid source or destination.")

def preview_file():
    file_path = input("👁 Enter full file path to preview: ").strip()

    if os.path.exists(file_path):
        try:
            os.startfile(file_path)  # For Windows
            print("👀 Previewing file...")
        except Exception as e:
            print(f"❌ Error previewing file: {e}")
    else:
        print("❌ File does not exist.")

# Menu Interface
while True:
    print("\n🔧 File Manager")
    print("1. Copy a file")
    print("2. Move a file")
    print("3. Preview a file")
    print("4. Exit")

    choice = input("Select an option: ").strip()

    if choice == '1':
        copy_file()
    elif choice == '2':
        move_file()
    elif choice == '3':
        preview_file()
    elif choice == '4':
        print("👋 Bye babu!")
        break
    else:
        print("❌ Invalid choice. Try again.")
