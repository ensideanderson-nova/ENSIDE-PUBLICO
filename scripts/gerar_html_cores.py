#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera HTML com CORES e botões que ABREM no Finder
"""

import os
import json

# Sistema criado
BASE = "/Users/Shared/ENSIDE_ORGANIZADO"

# Cores das categorias
CORES = {
    '01_DOCUMENTOS_PESSOAIS': {'cor': '#4CAF50', 'nome': 'VERDE', 'emoji': '👤'},
    '02_DOCUMENTOS_EMPRESA': {'cor': '#2196F3', 'nome': 'AZUL', 'emoji': '🏢'},
    '03_MADEIRAS': {'cor': '#9C27B0', 'nome': 'ROXO', 'emoji': '🌲'},
    '04_FRETES': {'cor': '#FF9800', 'nome': 'LARANJA', 'emoji': '🚛'},
    '05_BANCOS': {'cor': '#F44336', 'nome': 'VERMELHO', 'emoji': '🏦'},
    '06_FINANCEIRO': {'cor': '#FFEB3B', 'nome': 'AMARELO', 'emoji': '💰'},
    '07_CLIENTES': {'cor': '#E91E63', 'nome': 'ROSA', 'emoji': '👥'},
    '08_FORNECEDORES': {'cor': '#9E9E9E', 'nome': 'CINZA', 'emoji': '🏭'},
    '09_SISTEMAS': {'cor': '#673AB7', 'nome': 'ROXO', 'emoji': '💻'},
    '10_BACKUP': {'cor': '#607D8B', 'nome': 'CINZA', 'emoji': '💾'},
}

def escanear_pastas():
    """Escaneia o sistema criado"""
    estrutura = {}

    for categoria in sorted(os.listdir(BASE)):
        caminho_cat = os.path.join(BASE, categoria)

        if not os.path.isdir(caminho_cat) or categoria.startswith('.'):
            continue

        estrutura[categoria] = []

        # Listar subpastas
        try:
            for item in os.listdir(caminho_cat):
                caminho_item = os.path.join(caminho_cat, item)
                if os.path.isdir(caminho_item) and not item.startswith('.'):
                    estrutura[categoria].append({
                        'nome': item,
                        'caminho': caminho_item
                    })
        except:
            pass

    return estrutura

def gerar_html(estrutura):
    """Gera HTML colorido"""

    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>🗂️ Sistema Enside - Com Cores</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 30px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .categoria {
            margin: 30px 0;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        .categoria-header {
            font-size: 1.8em;
            font-weight: bold;
            margin-bottom: 20px;
            padding: 15px;
            background: white;
            border-radius: 10px;
            cursor: pointer;
            border-left: 8px solid;
        }
        .categoria-header:hover {
            transform: translateX(5px);
        }
        .pastas {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .pasta {
            background: white;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #ddd;
        }
        .pasta-nome {
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        .btn-abrir {
            background: linear-gradient(135deg, #4CAF50, #66BB6A);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            width: 100%;
            transition: all 0.3s;
        }
        .btn-abrir:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(76,175,80,0.4);
        }
        .caminho {
            font-size: 0.85em;
            color: #666;
            margin: 8px 0;
            font-family: monospace;
            word-break: break-all;
        }
        .aviso {
            background: #fff3cd;
            border: 2px solid #ffc107;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗂️ SISTEMA ENSIDE - ORGANIZADO COM CORES</h1>

        <div class="aviso">
            ⚠️ Para abrir pastas no Finder, use o servidor local!
            <br>Execute: <code>python3 servidor_organizacao.py</code>
        </div>

        <div id="categorias">
"""

    # Adicionar cada categoria
    for categoria, pastas in estrutura.items():
        info_cor = CORES.get(categoria, {'cor': '#999', 'nome': 'CINZA', 'emoji': '📁'})

        html += f"""
        <div class="categoria" style="background: {info_cor['cor']}22;">
            <div class="categoria-header" style="border-left-color: {info_cor['cor']};">
                {info_cor['emoji']} {categoria}
                <span style="font-size: 0.5em; color: #666; margin-left: 15px;">
                    ({len(pastas)} pastas)
                </span>
            </div>
            <div class="pastas">
"""

        for pasta in pastas:
            caminho_escapado = pasta['caminho'].replace("'", "\\'")

            html += f"""
                <div class="pasta">
                    <div class="pasta-nome">📁 {pasta['nome']}</div>
                    <div class="caminho">{pasta['caminho']}</div>
                    <button class="btn-abrir" onclick="abrirPasta('{caminho_escapado}')">
                        🔗 Abrir no Finder
                    </button>
                </div>
"""

        html += """
            </div>
        </div>
"""

    html += """
        </div>
    </div>

    <script>
        function abrirPasta(caminho) {
            // Verificar se está usando servidor local
            if (window.location.protocol === 'http:' && window.location.hostname === 'localhost') {
                // Chamar servidor para abrir pasta
                fetch('/abrir-finder?pasta=' + encodeURIComponent(caminho))
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'ok') {
                            console.log('✅ Pasta aberta:', caminho);
                        } else {
                            alert('❌ Erro: ' + data.mensagem);
                        }
                    })
                    .catch(err => {
                        alert('❌ Erro ao abrir pasta!\\n\\nCertifique-se que o servidor está rodando.');
                    });
            } else {
                alert('⚠️ Para abrir pastas automaticamente:\\n\\n' +
                      '1. Abra o Terminal\\n' +
                      '2. Execute: python3 servidor_organizacao.py\\n' +
                      '3. O HTML abrirá em http://localhost:8889\\n\\n' +
                      'Caminho: ' + caminho);
            }
        }
    </script>
</body>
</html>
"""

    return html

def main():
    print("🔍 Escaneando sistema...")
    estrutura = escanear_pastas()

    print("🎨 Gerando HTML com cores...")
    html = gerar_html(estrutura)

    arquivo = os.path.expanduser('~/mapa_com_cores.html')
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ HTML gerado: {arquivo}")
    print(f"📊 Total de categorias: {len(estrutura)}")

    total_pastas = sum(len(p) for p in estrutura.values())
    print(f"📁 Total de pastas: {total_pastas}")

if __name__ == '__main__':
    main()
