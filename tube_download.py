from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

# Obter o caminho do diretório atual onde o script está sendo executado
current_directory = os.path.dirname(os.path.realpath(__file__))

# Criar a subpasta "downloads" se ela não existir
downloads_folder = os.path.join(current_directory, 'downloads')
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)

# Lendo os links do arquivo
with open('arquivo.txt', 'r') as file:
    links = file.readlines()

# Iterando sobre cada link no arquivo
for link in links:
    link = link.strip()  # Removendo espaços em branco e quebras de linha
    try:
        # Criando um objeto YouTube usando o link
        yt = YouTube(link)

        # Selecionando o stream de áudio de maior qualidade
        stream = yt.streams.filter(only_audio=True).first()

        # Verificando se um stream válido foi encontrado
        if stream is not None:
            # Baixando o áudio na subpasta "downloads"
            print(f'Baixando {yt.title}...')
            download_path = stream.download(output_path=downloads_folder)
            print(f'{yt.title} baixado com sucesso!')

            # Verificando se o arquivo baixado é mp3
            if not download_path.endswith('.mp3'):
                # Convertendo para mp3
                print(f'Convertendo {yt.title} para mp3...')
                audio_clip = AudioFileClip(download_path)
                mp3_path = download_path.rsplit('.', 1)[0] + '.mp3'  # Mudar a extensão para mp3
                audio_clip.write_audiofile(mp3_path)
                audio_clip.close()
                os.remove(download_path)
                print(f'{yt.title} convertido com sucesso!')
        else:
            print(f'Não foi possível encontrar um stream de áudio para {link}.')

    except Exception as e:
        print(f'Erro ao baixar {link}: {e}')
