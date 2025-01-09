import yt_dlp

def list_resolutions(url):
    """Lista as resoluções disponíveis para o vídeo"""
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

            print("Resoluções disponíveis:")
            resolutions = []
            for f in formats:
                if f.get('vcodec') != 'none':  # Apenas vídeos
                    resolutions.append(f)
                    index = len(resolutions)  # Garante que o índice mostrado corresponda ao real
                    resolution = f.get('format_note', 'Desconhecida')
                    size = f.get('filesize', 0) // 1024 ** 2 if f.get('filesize') else 'Tamanho desconhecido'
                    print(f"{index}. {resolution} - {f['ext']} - {size} MB")
            return resolutions
    except Exception as e:
        print(f"Erro ao listar resoluções: {e}")
        return []

def download_youtube_video(url, download_path, format_type):
    try:
        if format_type == "mp4":
            resolutions = list_resolutions(url)
            if not resolutions:
                print("Nenhuma resolução disponível para download.")
                return

            choice = int(input("Escolha o número da resolução desejada: ")) - 1
            if choice < 0 or choice >= len(resolutions):
                print("Escolha inválida. Certifique-se de escolher um dos números listados.")
                return

            format_id = resolutions[choice]['format_id']

            ydl_opts = {
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',  # Nome do arquivo
                'format': format_id,  # Formato escolhido
            }
        elif format_type == "mp3":
            ydl_opts = {
                'outtmpl': f'{download_path}/%(title)s.%(ext)s',  # Nome do arquivo
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            print("Formato inválido. Escolha 'mp4' ou 'mp3'.")
            return

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Download concluído! Salvo em: {download_path}")
    except Exception as e:
        print(f"Erro ao baixar o vídeo: {e}")

if __name__ == "__main__":
    video_url = input("Digite a URL do vídeo do YouTube: ")
    default_folder = r"C:\Users\etake\Videos\YouTube"  # Caminho padrão
    download_folder = input(f"Digite o diretório onde deseja salvar o vídeo (pressione Enter para usar o padrão: {default_folder}): ")

    if not download_folder.strip():
        download_folder = default_folder

    format_type = input("Escolha o formato (mp4/mp3): ").strip().lower()

    download_youtube_video(video_url, download_folder, format_type)
