import yt_dlp
from colorama import Fore, Style

def list_resolutions(url):
    """Lista as resoluções disponíveis para o vídeo"""
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])

            print(Fore.YELLOW + "Resoluções disponíveis:" + Style.RESET_ALL)
            resolutions = []
            for f in formats:
                if f.get('vcodec') != 'none':  # Filtrar apenas streams com vídeo
                    resolutions.append(f)
                    index = len(resolutions)  # Garante que o índice mostrado corresponda ao real
                    resolution = f.get('format_note', 'Desconhecida')
                    size = f.get('filesize', 0) // 1024 ** 2 if f.get('filesize') else 'Tamanho desconhecido'
                    audio_status = "Com áudio" if f.get('acodec') != 'none' else "Sem áudio"
                    print(Fore.CYAN + f"{index}. {resolution} - {f['ext']} - {size} MB - {audio_status}" + Style.RESET_ALL)
            return resolutions
    except Exception as e:
        print(Fore.RED + f"Erro ao listar resoluções: {e}" + Style.RESET_ALL)
        return []

def download_youtube_video(url, download_path, format_type):
    try:
        if format_type == "mp4":
            resolutions = list_resolutions(url)
            if not resolutions:
                print(Fore.RED + "Nenhuma resolução disponível para download." + Style.RESET_ALL)
                return

            choice = int(input(Fore.YELLOW + "Escolha o número da resolução desejada: " + Style.RESET_ALL)) - 1
            if choice < 0 or choice >= len(resolutions):
                print(Fore.RED + "Escolha inválida. Certifique-se de escolher um dos números listados." + Style.RESET_ALL)
                return

            format_id = resolutions[choice]['format_id']

            # Verificar se o formato escolhido tem áudio
            selected_format = resolutions[choice]
            if selected_format.get('acodec') == 'none':
                print(Fore.YELLOW + "A resolução escolhida não possui áudio. O áudio será combinado automaticamente." + Style.RESET_ALL)
                ydl_opts = {
                    'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                    'format': f"{format_id}+bestaudio/best",
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4'
                    }],
                }
            else:
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
            print(Fore.RED + "Formato inválido. Escolha 'mp4' ou 'mp3'." + Style.RESET_ALL)
            return

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(Fore.GREEN + f"Download concluído! Salvo em: {download_path}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Erro ao baixar o vídeo: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    video_url = input(Fore.YELLOW + "Digite a URL do vídeo do YouTube: " + Style.RESET_ALL)
    default_folder = r"C:\Users\etake\Videos\YouTube"  # Caminho padrão
    download_folder = input(Fore.YELLOW + f"Digite o diretório onde deseja salvar o vídeo (pressione Enter para usar o padrão: {default_folder}): " + Style.RESET_ALL)

    if not download_folder.strip():
        download_folder = default_folder

    format_type = input(Fore.YELLOW + "Escolha o formato (mp4/mp3): " + Style.RESET_ALL).strip().lower()

    download_youtube_video(video_url, download_folder, format_type)
