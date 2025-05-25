from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os

path = os.getenv("DEFAULT_MUSIC_PATH")
if not path:
    print("❌ Default music path is not set. Please set the environment variable 'DEFAULT_MUSIC_PATH'.")
    exit()

files = os.listdir(path)


# सभी MP3 फाइल्स की लिस्ट
mp3_files = [f for f in os.listdir(path) if f.endswith('.mp3')]

for file in mp3_files:
    file_path = os.path.join(path, file)
    
    try:
        audio = EasyID3(file_path)
        title = audio.get('title', ['Unknown'])[0]
        artist = audio.get('artist', ['Unknown'])[0]
        album = audio.get('album', ['Unknown'])[0]
        print(f"🎶 Title: {title} | 👤 Artist: {artist} | 💿 Album: {album}")
    except Exception as e:
        print(f"Error reading {file}: {e}")

# search song by artist fun

search_artist = input("Enter artist name to search: ")

for file in os.listdir(path):
    if file.lower().endswith(('.mp3', '.flac' , '.m4a')):
        file_path = os.path.join(path, file)

        try:
            audio = EasyID3(file_path)
            artist = audio.get('artist', ['Unknown'])[0]

            if search_artist.lower() in artist.lower():
                title = audio.get('title', ['Title Not Found'])[0]
                print(f"Found: {title} by {artist} in {file_path}")
        except Exception as e:
            print(f"Error reading {file}: {e}") 



# search song fun
song = input("enter song name : ")

found = False

for foldername, subfolders, filenames in os.walk(path):
    for filename in filenames:
        if filename.endswith((".mp3" , '.wav' , '.flac')) and song.lower() in filename.lower():
            song_path = os.path.join(foldername, filename)
            print("🎵 Playing song: ", song_path)
            os.startfile(song_path)
            found = True
            break

    if found:
        break

if not found:
    print("Song not found in the specified directory.")