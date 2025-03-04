# main.py
from backend.analyzer import StructureAnalyzer
from backend.generator import CodeGenerator
from backend.validator import InputValidator

def main():
    # Exemplo de entrada do usuário
    input_text = """
    /meu-projeto/
    │── /public/               # Arquivos estáticos (imagens, fontes, ícones)
    │   ├── /img/              # Imagens do projeto
    │   ├── /fonts/            # Fontes personalizadas
    │   ├── /icons/            # Ícones SVG ou PNG
    │── /src/                  # Código-fonte principal
    │   ├── /css/              # Arquivos CSS
    │   │   ├── styles.css     # Estilos gerais
    │   │   ├── reset.css      # Reset básico para estilos padrão
    │   │   ├── components.css # Estilos para componentes específicos
    │   ├── /js/               # Arquivos JavaScript
    │   │   ├── script.js      # Lógica principal
    │   │   ├── utils.js       # Funções auxiliares
    │   │   ├── api.js         # Comunicação com APIs
    │   ├── /components/       # Componentes reutilizáveis (HTML ou JS)
    │   │   ├── navbar.html    # Menu de navegação
    │   │   ├── footer.html    # Rodapé
    │   │   ├── modal.html     # Componente modal
    │   ├── index.html         # Página principal
    │   ├── about.html         # Página "Sobre"
    │   ├── contact.html       # Página "Contato"
    │── /dist/                 # Arquivos otimizados para produção (gerado pelo build)
    │── /node_modules/         # Dependências instaladas pelo npm (se usar um bundler)
    │── .gitignore             # Arquivos a serem ignorados pelo Git
    │── package.json           # Dependências e scripts do projeto (caso use npm)
    │── README.md              # Documentação do projeto
    """

    # Valida a entrada
    errors = InputValidator.validate(input_text)
    if errors:
        print("Erros encontrados:")
        for error in errors:
            print(f"- {error}")
        return

    # Analisa a estrutura
    analyzer = StructureAnalyzer(input_text)
    structure = analyzer.get_structure()

    # Gera o código Python
    generator = CodeGenerator(structure)
    python_code = generator.generate_code()

    # Exibe o código gerado
    print("Código Python gerado:")
    print(python_code)

if __name__ == "__main__":
    main()