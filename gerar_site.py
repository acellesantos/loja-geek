import pandas as pd
import numpy as np
import json
import os

print("Lendo a planilha...")
if not os.path.exists('tabela_produtos.xlsx'):
    print("Erro: Arquivo tabela_produtos.xlsx não encontrado!")
    exit()

df = pd.read_excel('tabela_produtos.xlsx')
df['Nome do Produto'] = df['Nome do Produto'].replace(r'^\s*$', np.nan, regex=True)
df_preenchido = df.dropna(subset=['Nome do Produto'])

per_page = 10
total_items = len(df_preenchido)
total_pages = (total_items + per_page - 1) // per_page
if total_pages == 0:
    total_pages = 1

print(f"Encontrados {total_items} produtos. Gerando {total_pages} página(s)...")

for page in range(1, total_pages + 1):
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    df_pagina = df_preenchido.iloc[start_idx:end_idx]

    # Nome do arquivo de saída (página 1 vira index.html, as outras page2.html, page3.html...)
    nome_arquivo = 'index.html' if page == 1 else f'page{page}.html'

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acervo Geek — Catálogo</title>
    <link rel="stylesheet" href="style.css">
    <style>
        dialog.product-dialog {{
            padding: 0;
            border: none;
            border-radius: 20px;
            max-width: 920px;
            width: 90vw;
            background: #fff;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            overflow: hidden;
            margin: auto;
            position: fixed;
            inset: 0;
        }}
        dialog.product-dialog::backdrop {{
            background: rgba(0, 0, 0, 0.6);
        }}
        .modal-container {{
            display: grid;
            grid-template-columns: 1.1fr 1fr;
            min-height: 500px;
            position: relative;
        }}
        @media (max-width: 768px) {{
            .modal-container {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <header class="topbar">
        <a class="brand" href="#inicio"><b>AG</b><span>ACERVO GEEK</span></a>
        <a class="nav-link" href="#catalogo">Ver coleção ↓</a>
    </header>
    <main>
        <section class="hero" id="inicio">
            <div class="hero-copy">
                <span class="eyebrow">PEÇAS DE COLECIONADOR</span>
                <h1>Uma coleção inteira procurando novas prateleiras.</h1>
                <p>Funkos, action figures, estátuas e edições especiais de universos inesquecíveis.</p>
                <a class="button gold" href="#catalogo">Explorar o acervo ↘</a>
            </div>
            <div class="hero-photo" role="img" aria-label="Coleção de itens geek"></div>
        </section>
        
        <section class="catalog" id="catalogo">
            <div class="section-title">
                <div>
                    <span class="eyebrow dark">CATÁLOGO</span>
                    <h2>Encontre sua próxima peça</h2>
                </div>
                <p>{len(df_preenchido)} itens encontrados</p>
            </div>

            <div class="catalog-tools">
                <label class="search-field">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search" aria-hidden="true"><path d="m21 21-4.34-4.34"></path><circle cx="11" cy="11" r="8"></circle></svg>
                    <span class="sr-only">Buscar no catálogo</span>
                    <input placeholder="Buscar personagem, universo ou código…" value="">
                </label>
            </div>
            
            <div class="grid">
"""

for index, row in df_preenchido.iterrows():
    # Coleta segura de múltiplas colunas de fotos (Foto, Foto 1, Foto 2...)
    colunas_foto = ['Foto', 'Foto 1', 'Foto 2', 'Foto 3', 'Foto 4', 'Foto 5', 'Foto 6', 'Foto 7']
    fotos_lista = []
    for col in colunas_foto:
        if col in row and pd.notna(row[col]):
            val = str(row[col]).strip()
            if val and val.lower() != 'nan' and val != '':
                fotos_lista.append(val)
    
    if not fotos_lista:
        fotos_lista = ['default.jpg']
        
    foto_capa = fotos_lista[0]
    nome = str(row['Nome do Produto']).strip()
    preco = str(row['Preço (R$)']).strip()
    categoria = str(row.get('Categoria', 'GEEK')).strip().upper()
    if categoria == 'NAN' or categoria == '': 
        categoria = 'GEEK'
        
    codigo = str(row.get('Código', '')).strip()
    if codigo == 'nan': codigo = ''
    
    estado = str(row.get('Estado', 'Novo')).strip()
    if estado == 'nan': estado = 'Novo'
    
    condicao = str(row.get('Condição da Caixa', 'Caixa em bom estado de conservação.')).strip()
    if condicao == 'nan': condicao = 'Caixa em bom estado de conservação.'

    nome_j = json.dumps(nome)
    preco_j = json.dumps(preco)
    cat_j = json.dumps(categoria)
    fotos_j = json.dumps(fotos_lista)
    codigo_j = json.dumps(codigo)
    estado_j = json.dumps(estado)
    condicao_j = json.dumps(condicao)

    preco_vitrine = preco if preco.startswith('R$') else 'R$ ' + preco

    card = f"""
                <article class="card">
                    <div class="photo" style="cursor: pointer;" onclick='abrirDetalhes({nome_j}, {preco_j}, {cat_j}, {fotos_j}, {codigo_j}, {estado_j}, {condicao_j})'>
                        <img alt="{nome}" src="img/{foto_capa}" style="object-fit: contain; width: 100%; height: 100%;">
                        <i class="status disponível">Disponível</i>
                    </div>
                    <div class="card-body">
                        <div class="meta"><span>{categoria}</span></div>
                        <h3 class="card-title" style="cursor: pointer; font-size: 20px; font-weight: 800; margin: 10px 0 4px;" onclick='abrirDetalhes({nome_j}, {preco_j}, {cat_j}, {fotos_j}, {codigo_j}, {estado_j}, {condicao_j})'>{nome}</h3>
                        <div class="card-foot">
                            <strong>{preco_vitrine}</strong>
                            <button class="details" onclick='abrirDetalhes({nome_j}, {preco_j}, {cat_j}, {fotos_j}, {codigo_j}, {estado_j}, {condicao_j})'>Ver detalhes</button>
                        </div>
                    </div>
                </article>
    """
    html += card

html += """
            </div>
        </section>
    </main>
    
    <!-- MODAL DE DETALHES -->
    <dialog id="modalDetalhes" class="product-dialog">
        <button onclick="fecharDetalhes()" style="position: absolute; top: 16px; right: 16px; z-index: 20; background: #fff; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: none; border-radius: 50%; width: 36px; height: 36px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 16px; color: #111;">✕</button>
        
        <div class="modal-container">
            <!-- Lado Esquerdo -->
            <div style="background: #f7f6f2; padding: 40px; display: flex; flex-direction: column; justify-content: center; align-items: center; box-sizing: border-box;">
                <div id="modalImagemContainer" style="width: 100%; height: 360px; display: flex; align-items: center; justify-content: center; position: relative; overflow: hidden; cursor: zoom-in;">
                    <button id="btnAnterior" onclick="mudarFoto(-1)" style="position: absolute; left: 0; background: rgba(0,0,0,0.15); border: none; border-radius: 50%; width: 36px; height: 36px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: bold; color: #111; z-index: 10;">‹</button>
                    
                    <img id="modalImagemPrincipal" src="" alt="Produto" style="max-width: 90%; max-height: 100%; object-fit: contain; transition: transform 0.1s ease-out;">
                    
                    <button id="btnProximo" onclick="mudarFoto(1)" style="position: absolute; right: 0; background: rgba(0,0,0,0.15); border: none; border-radius: 50%; width: 36px; height: 36px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: bold; color: #111; z-index: 10;">›</button>
                </div>
                
                <div id="modalMiniaturas" style="display: flex; gap: 10px; margin-top: 24px; overflow-x: auto; max-width: 100%; padding-bottom: 8px;"></div>
            </div>

            <!-- Lado Direito -->
            <div style="background: #fff; padding: 50px 40px; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;">
               <div>
                   <div style="display: flex; gap: 8px; margin-bottom: 20px;">
                       <span id="modalBadgeCat" style="background: #fdf8eb; color: #926d24; font-size: 11px; font-weight: 700; padding: 6px 12px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px;">MARVEL</span>
                   </div>
                   
                   <h2 id="modalNome" style="font-size: 32px; font-weight: 500; color: #111; line-height: 1.1; margin: 0 0 12px 0; letter-spacing: -0.5px;">Nome do Produto</h2>
                   <p id="modalCodigo" style="font-size: 13px; color: #888; margin: 0 0 24px 0;"></p>
                   
                   <div id="modalPreco" style="font-size: 28px; font-weight: 700; color: #111; margin-bottom: 32px;">R$ 0,00</div>
                   
                   <div style="border-top: 1px solid #eaeaea; border-bottom: 1px solid #eaeaea; padding: 20px 0; margin-bottom: 24px; display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                       <div>
                           <span style="display: block; font-size: 11px; font-weight: 700; color: #926d24; text-transform: uppercase; margin-bottom: 6px;">Status</span>
                           <span style="font-size: 15px; color: #333;">Disponível</span>
                       </div>
                       <div>
                           <span style="display: block; font-size: 11px; font-weight: 700; color: #926d24; text-transform: uppercase; margin-bottom: 6px;">Estado</span>
                           <span id="modalEstado" style="font-size: 15px; color: #333;">Novo</span>
                       </div>
                   </div>
                   
                   <div style="margin-bottom: 32px;">
                       <span style="display: block; font-size: 11px; font-weight: 700; color: #926d24; text-transform: uppercase; margin-bottom: 6px;">Condição da caixa</span>
                       <p id="modalCondicao" style="font-size: 15px; color: #333; margin: 0; line-height: 1.5;"></p>
                   </div>
               </div>
               
               <div style="margin-top: auto;">
                   <button id="btnTenhoInteresse" style="background: #111; color: #fff; border: none; border-radius: 8px; width: 100%; height: 54px; font-size: 15px; font-weight: 600; cursor: pointer;">Tenho Interesse</button>
               </div>
            </div>
        </div>
    </dialog>

    <footer>
        <div class="brand"><b>AG</b><span>ACERVO GEEK</span></div>
        <p>Catálogo de colecionáveis • 2026</p>
    </footer>

    <script>
        // Define o caminho das imagens para o site estático
        window.caminhoImagens = 'img/';
    </script>
    <script src="script.js"></script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Sucesso! O index.html estático foi gerado integrando o script.js externo e o modal idêntico com zoom.")