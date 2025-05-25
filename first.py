import os

# path = "C:/Users/adhik/Music/"

# song = input("enter song name : ")

# for foldername, subfolders, filenames in os.walk(path):
#     for filename in filenames:
#         if filename.endswith((".mp3" , '.wav' , '.flac')) and song.lower() in filename.lower():
#             song_path = os.path.join(foldername, filename)
#             print("🎵 Playing song: ", song_path)
#             os.startfile(song_path)
#             found = True
#             break

#     if found:
#         break

# if not found:
#     print("Song not found in the specified directory.")


# Aapka target path
path = "C:/Users/adhik/OneDrive/Desktop"

# List of folders only
folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

# Print the folders
print("Folders:")
for folder in folders:
    print(folder)

folder_name = input("Enter the folder name to open: ")
# Check if the folder exists

if folder_name in folders:
    folder_path = os.path.join(path, folder_name)
    print(f"Opening folder: {folder_path}")
    os.startfile(folder_path)
else:
    print(f"Folder '{folder_name}' does not exist in the specified path.")
