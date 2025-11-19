#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera HTML COMPLETO com CORES VIBRANTES e ORGANIZAÇÃO VISUAL
"""

import os
import json
from pathlib import Path

BASE = "/Users/Shared/ENSIDE_ORGANIZADO"

# Cores VIBRANTES e claras
CORES = {
    '00_TRIAGEM_POR_PESSOA': {
        'cor': '#9C27B0',
        'cor_clara': '#E1BEE7',
        'nome': 'ROXO',
        'emoji': '🔍',
        'titulo': 'TRIAGEM POR PESSOA'
    },
    '01_DOCUMENTOS_PESSOAIS': {
        'cor': '#4CAF50',
        'cor_clara': '#C8E6C9',
        'nome': 'VERDE',
        'emoji': '👤',
        'titulo': 'DOCUMENTOS PESSOAIS'
    },
    '02_DOCUMENTOS_EMPRESA': {
        'cor': '#2196F3',
        'cor_clara': '#BBDEFB',
        'nome': 'AZUL',
        'emoji': '🏢',
        'titulo': 'DOCUMENTOS EMPRESA'
    },
    '03_MADEIRAS': {
        'cor': '#673AB7',
        'cor_clara': '#D1C4E9',
        'nome': 'ROXO ESCURO',
        'emoji': '🌲',
        'titulo': 'MADEIRAS'
    },
    '04_FRETES': {
        'cor': '#FF9800',
        'cor_clara': '#FFE0B2',
        'nome': 'LARANJA',
        'emoji': '🚛',
        'titulo': 'FRETES'
    },
    '05_BANCOS': {
        'cor': '#F44336',
        'cor_clara': '#FFCDD2',
        'nome': 'VERMELHO',
        'emoji': '🏦',
        'titulo': 'BANCOS'
    },
    '06_FINANCEIRO': {
        'cor': '#FFC107',
        'cor_clara': '#FFECB3',
        'nome': 'AMARELO',
        'emoji': '💰',
        'titulo': 'FINANCEIRO'
    },
    '07_CLIENTES': {
        'cor': '#E91E63',
        'cor_clara': '#F8BBD0',
        'nome': 'ROSA',
        'emoji': '👥',
        'titulo': 'CLIENTES'
    },
    '08_FORNECEDORES': {
        'cor': '#9E9E9E',
        'cor_clara': '#E0E0E0',
        'nome': 'CINZA',
        'emoji': '🏭',
        'titulo': 'FORNECEDORES'
    },
    '09_SISTEMAS': {
        'cor': '#3F51B5',
        'cor_clara': '#C5CAE9',
        'nome': 'INDIGO',
        'emoji': '💻',
        'titulo': 'SISTEMAS'
    },
    '10_BACKUP': {
        'cor': '#607D8B',
        'cor_clara': '#CFD8DC',
        'nome': 'AZUL CINZA',
        'emoji': '💾',
        'titulo': 'BACKUP'
    },
}

def escanear_sistema():
    """Escaneia o sistema e retorna estrutura completa"""
    estrutura = {}

    if not os.path.exists(BASE):
        print(f"⚠️  Sistema não encontrado: {BASE}")
        return estrutura

    for categoria in sorted(os.listdir(BASE)):
        caminho_cat = os.path.join(BASE, categoria)

        if not os.path.isdir(caminho_cat) or categoria.startswith('.'):
            continue

        info_cor = CORES.get(categoria, {
            'cor': '#757575',
            'cor_clara': '#E0E0E0',
            'nome': 'CINZA',
            'emoji': '📁',
            'titulo': categoria
        })

        estrutura[categoria] = {
            'info': info_cor,
            'pastas': []
        }

        # Listar todas as subpastas
        try:
            for item in sorted(os.listdir(caminho_cat)):
                caminho_item = os.path.join(caminho_cat, item)
                if os.path.isdir(caminho_item) and not item.startswith('.'):

                    # Contar subpastas
                    num_subpastas = 0
                    try:
                        subpastas = [s for s in os.listdir(caminho_item)
                                   if os.path.isdir(os.path.join(caminho_item, s))
                                   and not s.startswith('.')]
                        num_subpastas = len(subpastas)
                    except:
                        pass

                    estrutura[categoria]['pastas'].append({
                        'nome': item,
                        'caminho': caminho_item,
                        'subpastas': num_subpastas
                    })
        except Exception as e:
            print(f"Erro ao ler {categoria}: {e}")

    return estrutura

def gerar_html(estrutura):
    """Gera HTML completo com cores e organização"""

    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🗂️ Sistema ENSIDE - Organizado com Cores</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            text-align: center;
        }

        h1 {
            font-size: 2.5em;
            color: #333;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #666;
            font-size: 1.1em;
            margin-bottom: 20px;
        }

        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin-top: 20px;
        }

        .stat {
            text-align: center;
        }

        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }

        .stat-label {
            color: #666;
            font-size: 0.9em;
        }

        .controls {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }

        .filters {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }

        .filter-btn {
            padding: 10px 20px;
            border: 2px solid #ddd;
            background: white;
            border-radius: 25px;
            cursor: pointer;
            font-size: 0.95em;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        .filter-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .filter-btn.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }

        .search-box {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 1em;
            transition: border-color 0.3s;
        }

        .search-box:focus {
            outline: none;
            border-color: #667eea;
        }

        .categorias {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }

        .categoria {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }

        .categoria:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .categoria-header {
            padding: 20px;
            color: white;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .categoria-titulo {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.1em;
        }

        .categoria-count {
            background: rgba(255,255,255,0.3);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }

        .categoria-body {
            padding: 15px;
            max-height: 400px;
            overflow-y: auto;
        }

        .pasta-item {
            padding: 12px 15px;
            margin-bottom: 8px;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s;
            cursor: pointer;
            border: 2px solid transparent;
        }

        .pasta-item:hover {
            transform: translateX(5px);
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }

        .pasta-nome {
            font-weight: 500;
            color: #333;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .pasta-badge {
            background: #f0f0f0;
            color: #666;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8em;
        }

        .legenda {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }

        .legenda h3 {
            margin-bottom: 15px;
            color: #333;
        }

        .legenda-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }

        .legenda-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .legenda-cor {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2em;
        }

        .legenda-info {
            flex: 1;
        }

        .legenda-nome {
            font-weight: bold;
            color: #333;
            font-size: 0.9em;
        }

        .legenda-desc {
            color: #666;
            font-size: 0.8em;
        }

        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }

        .empty-state-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }

        /* Scrollbar personalizada */
        .categoria-body::-webkit-scrollbar {
            width: 8px;
        }

        .categoria-body::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }

        .categoria-body::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 10px;
        }

        .categoria-body::-webkit-scrollbar-thumb:hover {
            background: #555;
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 1.8em;
            }

            .categorias {
                grid-template-columns: 1fr;
            }

            .filters {
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🗂️ Sistema ENSIDE Organizado</h1>
            <p class="subtitle">Organização Completa com Cores e Categorias</p>

            <div class="stats">
                <div class="stat">
                    <div class="stat-number" id="total-categorias">0</div>
                    <div class="stat-label">Categorias</div>
                </div>
                <div class="stat">
                    <div class="stat-number" id="total-pastas">0</div>
                    <div class="stat-label">Pastas</div>
                </div>
                <div class="stat">
                    <div class="stat-number">673+</div>
                    <div class="stat-label">Subpastas</div>
                </div>
            </div>
        </header>

        <div class="controls">
            <div class="filters">
                <button class="filter-btn active" onclick="filtrarCategoria('todas')">
                    🌟 TODAS AS CATEGORIAS
                </button>
"""

    # Adicionar botões de filtro com nomes descritivos
    for cat_id, cat_data in estrutura.items():
        info = cat_data['info']
        html += f"""
                <button class="filter-btn" onclick="filtrarCategoria('{cat_id}')">
                    {info['emoji']} {info['titulo']}
                </button>
"""

    html += """
            </div>
            <input type="text" class="search-box" id="search" placeholder="🔍 Buscar pasta..." onkeyup="buscar()">
        </div>

        <div class="categorias" id="categorias">
"""

    # Adicionar categorias
    total_pastas = 0
    for cat_id, cat_data in estrutura.items():
        info = cat_data['info']
        pastas = cat_data['pastas']
        total_pastas += len(pastas)

        html += f"""
            <div class="categoria" data-categoria="{cat_id}">
                <div class="categoria-header" style="background: linear-gradient(135deg, {info['cor']} 0%, {info['cor']}dd 100%);">
                    <div class="categoria-titulo">
                        <span>{info['emoji']}</span>
                        <span>{info['titulo']}</span>
                    </div>
                    <div class="categoria-count">{len(pastas)} pastas</div>
                </div>
                <div class="categoria-body">
"""

        if pastas:
            for pasta in pastas:
                sub_info = f"📁 {pasta['subpastas']}" if pasta['subpastas'] > 0 else "📄"
                html += f"""
                    <div class="pasta-item" style="background-color: {info['cor_clara']}; border-color: {info['cor']}20;"
                         onclick="abrirPasta('{pasta['caminho']}')">
                        <div class="pasta-nome">
                            <span>{sub_info}</span>
                            <span>{pasta['nome']}</span>
                        </div>
                        {f'<span class="pasta-badge">{pasta["subpastas"]} subpastas</span>' if pasta['subpastas'] > 0 else ''}
                    </div>
"""
        else:
            html += """
                    <div class="empty-state">
                        <div class="empty-state-icon">📂</div>
                        <div>Nenhuma pasta encontrada</div>
                    </div>
"""

        html += """
                </div>
            </div>
"""

    html += """
        </div>

        <div class="legenda">
            <h3>🎨 Legenda de Cores</h3>
            <div class="legenda-grid">
"""

    # Legenda de cores com NOMES e DESCRIÇÕES
    descricoes = {
        '00_TRIAGEM_POR_PESSOA': 'Organize por CPF (Pessoa Física) ou CNPJ (Empresa)',
        '01_DOCUMENTOS_PESSOAIS': 'RG, CPF, CNH, Certidões, Comprovantes',
        '02_DOCUMENTOS_EMPRESA': 'CNPJ, Contratos Sociais, Alvarás, Licenças',
        '03_MADEIRAS': 'Fornecedores PR/SC/SP, Estoque, Certificados FSC',
        '04_FRETES': 'Motoristas, CTe, Cotações, Notas Fiscais',
        '05_BANCOS': 'Itaú, Bradesco, Santander, BB, Caixa, Nubank',
        '06_FINANCEIRO': 'Contas, Impostos, Fluxo de Caixa (12 meses)',
        '07_CLIENTES': 'Cadastros, Contratos, Propostas, Notas Fiscais',
        '08_FORNECEDORES': 'Cadastros, Contratos, Pedidos, Serviços',
        '09_SISTEMAS': 'Fretes, CRM, ERP, Scripts, Landing Pages',
        '10_BACKUP': 'Backups Diários, Semanais, Mensais, Completos',
    }

    # Tags do macOS correspondentes
    tags_macos = {
        '00_TRIAGEM_POR_PESSOA': 'Purple',
        '01_DOCUMENTOS_PESSOAIS': 'Green',
        '02_DOCUMENTOS_EMPRESA': 'Blue',
        '03_MADEIRAS': 'Purple',
        '04_FRETES': 'Orange',
        '05_BANCOS': 'Red',
        '06_FINANCEIRO': 'Yellow',
        '07_CLIENTES': 'Pink',
        '08_FORNECEDORES': 'Gray',
        '09_SISTEMAS': 'Blue',
        '10_BACKUP': 'Gray',
    }

    for cat_id, cat_data in estrutura.items():
        info = cat_data['info']
        desc = descricoes.get(cat_id, '')
        tag = tags_macos.get(cat_id, 'Gray')

        html += f"""
                <div class="legenda-item">
                    <div class="legenda-cor" style="background-color: {info['cor']}; color: white;">
                        {info['emoji']}
                    </div>
                    <div class="legenda-info">
                        <div class="legenda-nome">{info['titulo']}</div>
                        <div class="legenda-desc">{desc}</div>
                        <div class="legenda-desc" style="font-style: italic; margin-top: 3px;">
                            🏷️ Tag no Finder: {tag}
                        </div>
                    </div>
                </div>
"""

    html += f"""
            </div>
        </div>
    </div>

    <script>
        // Atualizar estatísticas
        document.getElementById('total-categorias').textContent = {len(estrutura)};
        document.getElementById('total-pastas').textContent = {total_pastas};

        // Filtrar por categoria
        function filtrarCategoria(categoria) {{
            const categorias = document.querySelectorAll('.categoria');
            const botoes = document.querySelectorAll('.filter-btn');

            // Atualizar botões
            botoes.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            // Mostrar/ocultar categorias
            categorias.forEach(cat => {{
                if (categoria === 'todas' || cat.dataset.categoria === categoria) {{
                    cat.style.display = 'block';
                }} else {{
                    cat.style.display = 'none';
                }}
            }});
        }}

        // Buscar
        function buscar() {{
            const termo = document.getElementById('search').value.toLowerCase();
            const categorias = document.querySelectorAll('.categoria');

            categorias.forEach(cat => {{
                const pastas = cat.querySelectorAll('.pasta-item');
                let encontrou = false;

                pastas.forEach(pasta => {{
                    const nome = pasta.textContent.toLowerCase();
                    if (nome.includes(termo)) {{
                        pasta.style.display = 'flex';
                        encontrou = true;
                    }} else {{
                        pasta.style.display = 'none';
                    }}
                }});

                // Mostrar categoria se encontrou algo
                if (termo === '' || encontrou) {{
                    cat.style.display = 'block';
                }} else {{
                    cat.style.display = 'none';
                }}
            }});
        }}

        // Abrir pasta no Finder
        function abrirPasta(caminho) {{
            // Criar URL para abrir no Finder
            const url = 'file://' + encodeURI(caminho);

            // Tentar abrir
            window.location.href = url;

            // Feedback visual
            event.currentTarget.style.transform = 'scale(0.95)';
            setTimeout(() => {{
                event.currentTarget.style.transform = '';
            }}, 200);
        }}
    </script>
</body>
</html>
"""

    return html

def main():
    print("🔍 Escaneando sistema completo...")
    estrutura = escanear_sistema()

    if not estrutura:
        print("❌ Sistema não encontrado ou vazio!")
        return

    print(f"✅ Encontradas {len(estrutura)} categorias")

    print("🎨 Gerando HTML com cores...")
    html = gerar_html(estrutura)

    # Salvar HTML
    output_file = os.path.expanduser("~/sistema_enside_completo.html")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ HTML gerado: {output_file}")
    print(f"📊 Total de categorias: {len(estrutura)}")

    total_pastas = sum(len(cat['pastas']) for cat in estrutura.values())
    print(f"📁 Total de pastas: {total_pastas}")

    print("\n🌐 Abra o HTML no navegador:")
    print(f"   open {output_file}")

if __name__ == "__main__":
    main()
