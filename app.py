import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
EXCEL_FILE = 'tabela_produtos.xlsx'

def ler_planilha():
    if not os.path.exists(EXCEL_FILE):
        return pd.DataFrame(columns=['Nome do Produto', 'Preço (R$)', 'Categoria', 'Código', 'Estado', 'Condição da Caixa', 'Foto'])
    df = pd.read_excel(EXCEL_FILE)
    df['Nome do Produto'] = df['Nome do Produto'].fillna('')
    return df

@app.route('/')
def index():
    df = ler_planilha()
    df_preenchido = df[df['Nome do Produto'].str.strip() != '']
    
    # Parâmetro de paginação (padrão é a página 1)
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
        
    per_page = 12
    total_items = len(df_preenchido)
    total_pages = (total_items + per_page - 1) // per_page
    
    # Garante que a página solicitada é válida
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
        
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    df_pagina = df_preenchido.iloc[start_idx:end_idx]
    
    produtos = []
    for _, row in df_pagina.iterrows():
        colunas_foto = ['Foto', 'Foto 1', 'Foto 2', 'Foto 3', 'Foto 4', 'Foto 5', 'Foto 6', 'Foto 7']
        fotos_lista = []
        for col in colunas_foto:
            if col in row and pd.notna(row[col]):
                val = str(row[col]).strip()
                if val and val.lower() != 'nan' and val != '':
                    fotos_lista.append(val)
        
        if not fotos_lista:
            fotos_lista = ['default.jpg']
            
        prod_dict = row.to_dict()
        prod_dict['fotos_lista'] = fotos_lista
        produtos.append(prod_dict)
        
    return render_template('index.html', 
                           produtos=produtos, 
                           page=page, 
                           total_pages=total_pages,
                           total_items=total_items)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    df = ler_planilha()
    
    if request.method == 'POST':
        acao = request.form.get('acao')
        codigo_alvo = request.form.get('codigo_original')
        
        if acao == 'excluir' and codigo_alvo:
            # Remove o produto da planilha com base no código
            df = df[df['Código'].astype(str).str.strip() != str(codigo_alvo).strip()]
        else:
            dados_produto = {
                'Nome do Produto': request.form.get('nome'),
                'Preço (R$)': request.form.get('preco'),
                'Categoria': request.form.get('categoria', '').strip(),
                'Franquia': request.form.get('franquia', '').upper().strip(), # Adicionado aqui
                'Código': request.form.get('codigo', ''),
                'Estado': request.form.get('estado', 'Novo'),
                'Condição da Caixa': request.form.get('condicao', 'Caixa em bom estado de conservação.'),
                'Foto': request.form.get('foto', 'default.jpg')
            }
            
            if acao == 'editar' and codigo_alvo:
                # Atualiza o produto existente
                mask = df['Código'].astype(str).str.strip() == str(codigo_alvo).strip()
                if mask.any():
                    for col, val in dados_produto.items():
                        df.loc[mask, col] = val
                else:
                    df = pd.concat([df, pd.DataFrame([dados_produto])], ignore_index=True)
            else:
                # Adiciona novo produto
                df = pd.concat([df, pd.DataFrame([dados_produto])], ignore_index=True)
            
        df.to_excel(EXCEL_FILE, index=False)
        return redirect(url_for('admin'))
        
    produtos_admin = df[df['Nome do Produto'].str.strip() != ''].to_dict(orient='records')
    return render_template('admin.html', produtos=produtos_admin)

if __name__ == '__main__':
    app.run(debug=True)