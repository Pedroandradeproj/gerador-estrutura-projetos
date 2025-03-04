import os
import zipfile

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
        
        # Verifica se a pasta contém arquivos ou subpastas
        if not any(os.scandir(source_folder)):
            raise ValueError(f'A pasta {source_folder} está vazia.')

        # Caminho absoluto do arquivo ZIP
        zip_path = os.path.abspath(zip_filename)

        # Garante que o arquivo ZIP não esteja dentro da pasta a ser compactada
        if zip_path.startswith(os.path.abspath(source_folder)):
            raise ValueError("O arquivo ZIP de destino não pode estar dentro da pasta a ser compactada.")

        # Cria o arquivo ZIP
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_folder)
                    zipf.write(file_path, arcname)

        print(f"Arquivo ZIP '{zip_filename}' criado com sucesso!")

    except FileNotFoundError as fnf_error:
        print(f"Erro: {str(fnf_error)}")
    except ValueError as ve_error:
        print(f"Erro: {str(ve_error)}")
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")


def main():
    # Exemplo de uso
    source_folder = './estrutura'  # Pasta a ser compactada
    zip_filename = 'estrutura.zip'  # Nome do arquivo ZIP de saída
    
    # Chama a função para gerar o ZIP
    create_zip_structure(source_folder, zip_filename)


if __name__ == "__main__":
    main()
