import yt_dlp
import os
import shutil

# Fixed download path (modify this to your desired location)
DEFAULT_DOWNLOAD_PATH = "C:/Users/adhik/Music/"

def get_user_search_query():
    print("\nYouTube Audio Downloader")
    username = input("Enter your name: ").strip()
    print(f"\nHello {username}! Let's download some audio from YouTube.")
    search_query = input("Enter your search query: ").strip()
    return search_query

def search_youtube(query):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'default_search': 'ytsearch5',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(f"ytsearch5:{query}", download=False)
        return result['entries']

def display_results(videos):
    print("\nTop 5 Results:")
    for i, video in enumerate(videos, 1):
        print(f"{i}. {video['title']}")
    print("6. Cancel")

def download_audio(url):
    # Ensure the download directory exists
    os.makedirs(DEFAULT_DOWNLOAD_PATH, exist_ok=True)

    # Download the best available audio (no FFmpeg conversion)
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',  # Prefers .m4a (no conversion)
        'outtmpl': os.path.join(DEFAULT_DOWNLOAD_PATH, '%(title)s.%(ext)s'),
        'quiet': False,
        'postprocessors': [],  # Disable FFmpeg post-processing
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"\nDownloaded successfully to: {filename}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

def main():
    search_query = get_user_search_query()
    videos = search_youtube(search_query)
    
    if not videos:
        print("No results found. Please try a different search.")
        return
    
    display_results(videos)
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-5 to download, 6 to cancel): "))
            if 1 <= choice <= 5:
                selected_video = videos[choice-1]
                print(f"\nDownloading: {selected_video['title']}")
                download_audio(selected_video['url'])
                break
            elif choice == 6:
                print("Download cancelled.")
                break
            else:
                print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()