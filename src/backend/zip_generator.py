import os
import zipfile
import shutil

def create_zip_structure(source_folder, zip_filename):
    """
    Cria um arquivo ZIP contendo todos os arquivos e pastas da estrutura de origem.
    
    Args:
        source_folder (str): Caminho da pasta a ser compactada.
        zip_filename (str): Nome do arquivo ZIP de destino.
    """
    try:
        # Verifica se a pasta de origem existe
        if not os.path.exists(source_folder):
            raise FileNotFoundError(f'A pasta {source_folder} não foi encontrada.')
        
        # Cria o arquivo ZIP
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Caminha pela pasta de origem e adiciona os arquivos ao ZIP
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    # Adiciona o arquivo ao ZIP com o caminho relativo
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, start=source_folder)
                    zipf.write(file_path, arcname)
        
        print(f"Arquivo ZIP {zip_filename} criado com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar ou compactar a estrutura: {str(e)}")


def main():
    # Exemplo de uso
    source_folder = './estrutura'  # Pasta a ser compactada
    zip_filename = 'estrutura.zip'  # Nome do arquivo ZIP de saída
    
    # Chama a função para gerar o ZIP
    create_zip_structure(source_folder, zip_filename)


if __name__ == "__main__":
    main()
