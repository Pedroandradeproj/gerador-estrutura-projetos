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
            empty_folders = []  # Lista para rastrear pastas vazias
            for root, dirs, files in os.walk(source_folder):
                # Se não houver arquivos nem subpastas, adicionar à lista de pastas vazias
                if not files and not dirs:
                    empty_folders.append(root)
                
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_folder)

                    # **Evita incluir o próprio arquivo ZIP dentro do ZIP**
                    if zip_filename not in arcname:  # Não inclui o arquivo ZIP no próprio ZIP
                        zipf.write(file_path, arcname)

        # **Verifica se o ZIP contém pastas vazias**
        if empty_folders:
            print("⚠️ O ZIP contém pastas vazias. Removendo...")
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                zip_contents = zipf.namelist()

            # Remove pastas vazias do ZIP recriando-o sem elas
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for item in zip_contents:
                    # Só adiciona os itens que não são pastas vazias
                    if item not in empty_folders:
                        zipf.write(os.path.join(source_folder, item), item)
                print("✔️ Pastas vazias removidas do ZIP.")

        print(f"✅ Arquivo ZIP '{zip_filename}' criado com sucesso!")

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
