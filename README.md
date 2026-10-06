# 💛 Acervo Geek — Catálogo de Colecionáveis

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/pt-BR/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/pt-BR/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=000000)](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript)

> 🔗 **Demo online:**  
> 🚧 *Deploy via GitHub Pages em configuração (Em breve)*

Projeto de catálogo virtual focado em itens colecionáveis como **Funko Pops, Action Figures e Estátuas**. Uma interface premium, de estética *dark* e amarela, projetada para destacar os detalhes dos produtos e facilitar o contato direto com o vendedor.

O grande diferencial do projeto é a alimentação de dados dinâmica: o back-end lê as informações diretamente de uma **planilha Excel**, automatizando a geração dos cards do catálogo sem necessidade de um banco de dados complexo.

---

## ✨ Funcionalidades

- 📦 **Catálogo Dinâmico:** Produtos gerados automaticamente a partir de um arquivo Excel (`tabela_produtos.xlsx`).
- 🔍 **Busca em Tempo Real:** Filtro instantâneo no catálogo pelo nome, código ou franquia usando JavaScript puro.
- 🖼️ **Modal de Detalhes Avançado:**
  - Galeria de imagens do produto com miniaturas navegáveis.
  - Efeito de **Zoom In/Out** na imagem principal controlado pelo *scroll* do mouse.
  - Fechamento intuitivo e reset automático do zoom ao trocar de imagem.
- 📱 **Layout Responsivo:** Hero banner de duas colunas em desktop que se adapta perfeitamente para mobile.
- 💬 **CTA Integrado:** Botão de "Tenho interesse" que direciona o usuário para o WhatsApp com uma mensagem pré-formatada (nome e preço do item).

---

## 🛠️ Tecnologias utilizadas

**Back-end & Dados:**
- Python 3
- Flask (Roteamento e renderização web)
- Pandas (Leitura e manipulação da base de dados em Excel)
- Jinja2 (Templating HTML)

**Front-end:**
- HTML5 Semântico
- CSS3 (Flexbox, tipografia e customização de layout sem frameworks externos)
- JavaScript Vanilla (Manipulação do DOM, eventos de teclado/mouse e lógica de busca)
- Git para versionamento de código

---

## 📁 Estrutura do projeto

```text
acervo-geek/
│
├── app.py                   # Arquivo principal (rotas do Flask)
├── gerar_site.py            # Script auxiliar de automação
├── tabela_produtos.xlsx     # Planilha atuando como Banco de Dados
├── static/
│   ├── style.css            # Estilos personalizados (Hero, Grid, Modal)
│   ├── script.js            # Lógica de interatividade (Zoom, Filtros, Galeria)
│   └── img/                 # Imagens dos colecionáveis e assets do layout
├── templates/
│   ├── index.html           # Página principal da loja
│   └── admin.html           # Interface do painel administrativo
└── README.md