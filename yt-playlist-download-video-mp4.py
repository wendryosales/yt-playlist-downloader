import os
from yt_dlp import YoutubeDL
import re
import unicodedata

def normalize_foldername(name):
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.replace('+', 'mais')
    name = name.replace('&', 'e')
    name = re.sub(r'\s+', '_', name.strip())
    if len(name) > 50:
        name = name[:50]
    return name

def download_youtube_videos(url, output_folder, is_playlist=True):
    # Configuração básica para download em 1080p
    options = {
        # Formato: prioriza 1080p MP4, depois qualquer 1080p, depois o melhor disponível
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]/best',
        
        # Saída: organiza por canal
        'outtmpl': os.path.join(output_folder, '%(channel)s', '%(title)s.%(ext)s'),
        
        'restrictfilenames': True,
        'windowsfilenames': True,
        'ignoreerrors': True,
        'noplaylist': not is_playlist,
        'writethumbnail': True,
        'progress_hooks': [lambda d: print_progress(d)],
        'postprocessors': [
            {'key': 'FFmpegMetadata'},
            {'key': 'EmbedThumbnail'},
            {'key': 'EmbedThumbnail'},
            {
                'key': 'MetadataFromTitle',
                'titleformat': '%(title)s',
            },
        ],
        'channelname_hook': lambda name: normalize_foldername(name),
        'postprocessor_args': [
            '-movflags', '+faststart',
        ],
    }
    
    try:
        print("Iniciando download em 1080p com metadados...")
        with YoutubeDL(options) as ydl:
            ydl.download([url])
            
    except Exception as e:
        print(f"Erro durante o download: {e}")

def print_progress(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        filename = os.path.basename(d.get('filename', 'desconhecido'))
        print(f"\rBaixando: {filename} | {percent} concluído | Velocidade: {speed} | ETA: {eta}", end='')
    elif d['status'] == 'finished':
        print(f"\nDownload concluído: {os.path.basename(d['filename'])}")
        print("Processando vídeo e adicionando metadados...")

if __name__ == "__main__":
    download_type = input("Deseja baixar um vídeo único ou uma playlist? (v/p): ").lower()
    
    if download_type == 'v':
        url = input("Digite a URL do vídeo do YouTube: ")
        is_playlist = False
    else:
        url = input("Digite a URL da playlist do YouTube: ")
        is_playlist = True
    
    output_folder = input("Pasta de destino (default: videos): ") or "videos"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    download_youtube_videos(url, output_folder, is_playlist)
