#!/bin/bash

BASE="/Users/Shared/ENSIDE_ORGANIZADO"

echo "📁 CRIANDO NOVAS CATEGORIAS..."
echo ""

# ═══════════════════════════════════════════════════════════
# 11 - VIDEOS
# ═══════════════════════════════════════════════════════════

echo "🎥 11 - VIDEOS"

mkdir -p "$BASE/11_VIDEOS"/{Tutoriais,Apresentacoes,Reunioes,Marketing,Pessoal,Treinamento}

# Subcategorias de segurança
mkdir -p "$BASE/11_VIDEOS/Seguranca"/{Hackers,Analise_Sistemas,Vulnerabilidades,Testes_Penetracao}

# Por ano
mkdir -p "$BASE/11_VIDEOS/2025"
mkdir -p "$BASE/11_VIDEOS/2024"

echo "   ✓ Vídeos criados"

# ═══════════════════════════════════════════════════════════
# 12 - PRINTS DE TELA
# ═══════════════════════════════════════════════════════════

echo "📸 12 - PRINTS_TELA"

mkdir -p "$BASE/12_PRINTS_TELA"/{Desktop,Mobile,Web,Sistemas,Erros}

# Por contexto
mkdir -p "$BASE/12_PRINTS_TELA/Evidencias"/{Fraudes,Problemas,Comprovantes}
mkdir -p "$BASE/12_PRINTS_TELA/Documentacao"/{Tutoriais,Manuais,Bugs}

# Por ano
mkdir -p "$BASE/12_PRINTS_TELA/2025"
mkdir -p "$BASE/12_PRINTS_TELA/2024"

echo "   ✓ Prints criados"

# ═══════════════════════════════════════════════════════════
# 13 - SEGURANCA E FRAUDES
# ═══════════════════════════════════════════════════════════

echo "🔐 13 - SEGURANCA_FRAUDES"

# Tipos de fraude
mkdir -p "$BASE/13_SEGURANCA_FRAUDES/Fraudes"/{Tentativas,Investigacao,Relatorios,Boletins_Ocorrencia}

# Cheques
mkdir -p "$BASE/13_SEGURANCA_FRAUDES/Cheques"/{Estranhos,Suspeitos,Devolvidos,Analise}

# Análise de segurança
mkdir -p "$BASE/13_SEGURANCA_FRAUDES/Analise_Seguranca"/{Scripts_Suspeitos,Logs,Vulnerabilidades,Incidentes}

# Hacking e invasões
mkdir -p "$BASE/13_SEGURANCA_FRAUDES/Hacking"/{Tentativas_Invasao,Logs_Acesso,IPs_Suspeitos,Bloqueios}

# Documentação
mkdir -p "$BASE/13_SEGURANCA_FRAUDES/Documentacao"/{Politicas,Procedimentos,Relatorios_Mensais}

# Evidências
mkdir -p "$BASE/13_SEGURANCA_FRAUDES/Evidencias"/{Screenshots,Videos,Logs,Emails}

echo "   ✓ Segurança e Fraudes criados"

# ═══════════════════════════════════════════════════════════
# APLICAR CORES
# ═══════════════════════════════════════════════════════════

echo ""
echo "🎨 APLICANDO CORES..."

# Vídeos - Vermelho escuro
tag -a "Red" "$BASE/11_VIDEOS" 2>/dev/null
find "$BASE/11_VIDEOS" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Red" {} \; 2>/dev/null

# Prints - Azul claro
tag -a "Blue" "$BASE/12_PRINTS_TELA" 2>/dev/null
find "$BASE/12_PRINTS_TELA" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Blue" {} \; 2>/dev/null

# Segurança - Vermelho forte (alerta)
tag -a "Red" "$BASE/13_SEGURANCA_FRAUDES" 2>/dev/null
find "$BASE/13_SEGURANCA_FRAUDES" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Red" {} \; 2>/dev/null
find "$BASE/13_SEGURANCA_FRAUDES/Fraudes" -type d -exec tag -a "Red" {} \; 2>/dev/null

echo "   ✓ Cores aplicadas"

echo ""
echo "✅ NOVAS CATEGORIAS CRIADAS!"
echo ""
echo "📊 RESUMO:"
echo "   • 11_VIDEOS - Tutoriais, Reuniões, Hackers"
echo "   • 12_PRINTS_TELA - Screenshots, Evidências"
echo "   • 13_SEGURANCA_FRAUDES - Fraudes, Cheques, Hacking"
