# 🚀 Gerador de Estrutura de Projetos

## 📌 Sobre o Projeto
O **Gerador de Estrutura de Projetos** é uma ferramenta automatizada que permite aos usuários criar a estrutura inicial de diretórios e arquivos para seus projetos. Com um clique, você pode definir uma hierarquia de pastas e obter um código Python pronto para ser executado.

✅ **Principais Funcionalidades**
- Geração automática de estrutura de diretórios e arquivos.
- Interface intuitiva para entrada de dados.
- **Modo Claro/Escuro** para personalização do visual.
- **Toasts de notificação** no lugar de `alert()`, melhorando a experiência do usuário.
- Opção para **copiar ou baixar** o código gerado.

---

## **🛠 Tecnologias Utilizadas**
### **📌 Backend**
- [Python 3.x](https://www.python.org/) 
- [Flask](https://flask.palletsprojects.com/) - Framework para API.
- [Flask-CORS](https://flask-cors.readthedocs.io/) - Suporte para requisições entre domínios.

### **📌 Frontend**
- **HTML5, CSS3, JavaScript**
- [Bootstrap](https://getbootstrap.com/) - Estilização e responsividade.

### **📌 Bibliotecas Necessárias**
Antes de rodar o projeto, instale as dependências com:

```sh
pip install -r requirements.txt
```

✅ **Lista de bibliotecas Python usadas (`requirements.txt`)**:
```
Flask==3.1.0
Flask-CORS==5.0.0
Werkzeug==3.1.3
Jinja2==3.1.5
itsdangerous==2.2.0
MarkupSafe==3.0.2
click==8.1.8
colorama==0.4.6
blinker==1.9.0
```

---

## **📌 Como Rodar o Projeto?**
### **🔹 Executando Localmente**
1️⃣ **Clone o repositório**:
```sh
git clone https://github.com/Pedroandradeproj/gerador-estrutura-projetos.git
```

2️⃣ **Entre na pasta do projeto**:
```sh
cd gerador-estrutura-projetos
```

3️⃣ **Crie e ative um ambiente virtual (opcional, mas recomendado)**:
```sh
python -m venv venv
# Ativar no Windows
venv\Scripts\activate
# Ativar no macOS/Linux
source venv/bin/activate
```

4️⃣ **Instale as dependências**:
```sh
pip install -r requirements.txt
```

5️⃣ **Execute o servidor Flask**:
```sh
python src/backend/app.py
```

6️⃣ **Acesse o projeto no navegador**:
```
http://127.0.0.1:10000/
```

---

## **📌 Como Usar o Projeto?**
1️⃣ **Digite a estrutura desejada** na caixa de texto.  
2️⃣ **Clique em "Gerar Estrutura"** para visualizar o código.  
3️⃣ **Copie ou baixe o código gerado.**  

✅ **Ative o modo escuro** com o botão "Alternar Tema".  
✅ **Receba notificações visuais ao invés de alertas padrões.**  

---

## **📌 Funcionalidades Adicionadas**
✅ **Modo Claro/Escuro**  
- O usuário pode alternar entre os temas clicando no botão `"Alternar Tema"`.

✅ **Notificações Visuais (Toasts Bootstrap)**  
- Substituímos os `alert()` tradicionais por notificações visuais no canto da tela.

---

## **📌 Como Contribuir?**
Se deseja contribuir para o projeto:

1️⃣ **Faça um Fork** do repositório.  
2️⃣ **Crie uma Branch** para sua funcionalidade:
```sh
git checkout -b minha-nova-funcionalidade
```
3️⃣ **Realize as alterações e faça commit**:
```sh
git add .
git commit -m "Adicionando nova funcionalidade"
```
4️⃣ **Envie as mudanças**:
```sh
git push origin minha-nova-funcionalidade
```
5️⃣ **Crie um Pull Request**.

---

## **🌍 Hospedagem**
O projeto está disponível online:

- **Frontend:** [https://SEU-FRONTEND.onrender.com](https://SEU-FRONTEND.onrender.com)
- **Backend:** [https://SEU-BACKEND.onrender.com](https://SEU-BACKEND.onrender.com)

---

## **📌 Autor**
👤 **Pedro Andrade | Tec4Avalon**  
🔗 **GitHub:** [Pedroandradeproj](https://github.com/Pedroandradeproj)  
🔗 **GitHub:** [Tec4Avalon](https://github.com/Tec4Avalon)

📌 Projeto open-source, fique à vontade para contribuir! 🚀🔥
