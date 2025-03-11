import os
from yt_dlp import YoutubeDL

def download_youtube_playlist_as_mp3(playlist_url, output_folder):
    options = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(options) as ydl:
        ydl.download([playlist_url])

if __name__ == "__main__":
    playlist_url = input("Digite a URL da playlist do YouTube: ")
    output_folder = input("Pasta de destino (default: musicas): ") or "musicas"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    download_youtube_playlist_as_mp3(playlist_url, output_folder)
