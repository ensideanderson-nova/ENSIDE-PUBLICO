#!/bin/bash

BASE="/Users/Shared/ENSIDE_ORGANIZADO"

echo "🎨 APLICANDO CORES EM TODO O SISTEMA..."

# ===== PASTA PRINCIPAL =====
echo "  📂 Pasta principal..."
tag -a "Purple" "$BASE" 2>/dev/null

# ===== 00 - TRIAGEM =====
echo "  🔍 Triagem..."
tag -a "Purple" "$BASE/00_TRIAGEM_POR_PESSOA" 2>/dev/null
find "$BASE/00_TRIAGEM_POR_PESSOA" -name "CPF_*" -type d -exec tag -a "Green" {} \; 2>/dev/null
find "$BASE/00_TRIAGEM_POR_PESSOA" -name "CNPJ_*" -type d -exec tag -a "Blue" {} \; 2>/dev/null

# ===== 01 - DOCUMENTOS PESSOAIS =====
echo "  👤 Documentos Pessoais..."
tag -a "Green" "$BASE/01_DOCUMENTOS_PESSOAIS" 2>/dev/null
find "$BASE/01_DOCUMENTOS_PESSOAIS" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Green" {} \; 2>/dev/null

# ===== 02 - DOCUMENTOS EMPRESA =====
echo "  🏢 Documentos Empresa..."
tag -a "Blue" "$BASE/02_DOCUMENTOS_EMPRESA" 2>/dev/null
find "$BASE/02_DOCUMENTOS_EMPRESA" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Blue" {} \; 2>/dev/null

# ===== 03 - MADEIRAS =====
echo "  🌲 Madeiras..."
tag -a "Purple" "$BASE/03_MADEIRAS" 2>/dev/null
find "$BASE/03_MADEIRAS" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Purple" {} \; 2>/dev/null
find "$BASE/03_MADEIRAS" -maxdepth 2 -mindepth 2 -type d -exec tag -a "Purple" {} \; 2>/dev/null

# ===== 04 - FRETES =====
echo "  🚛 Fretes..."
tag -a "Orange" "$BASE/04_FRETES" 2>/dev/null
find "$BASE/04_FRETES" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Orange" {} \; 2>/dev/null
find "$BASE/04_FRETES" -maxdepth 2 -mindepth 2 -type d -exec tag -a "Orange" {} \; 2>/dev/null

# ===== 05 - BANCOS =====
echo "  🏦 Bancos..."
tag -a "Red" "$BASE/05_BANCOS" 2>/dev/null

# Cada banco - Vermelho
find "$BASE/05_BANCOS" -maxdepth 1 -mindepth 1 -type d ! -name ".*" -exec tag -a "Red" {} \; 2>/dev/null

# CPF - Verde
find "$BASE/05_BANCOS" -name "CPF" -type d -exec tag -a "Green" {} \; 2>/dev/null
find "$BASE/05_BANCOS/*/CPF" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Green" {} \; 2>/dev/null

# CNPJ - Azul
find "$BASE/05_BANCOS" -name "CNPJ" -type d -exec tag -a "Blue" {} \; 2>/dev/null
find "$BASE/05_BANCOS/*/CNPJ" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Blue" {} \; 2>/dev/null

# Subcategorias específicas
find "$BASE/05_BANCOS" -name "Extratos*" -type d -exec tag -a "Purple" {} \; 2>/dev/null
find "$BASE/05_BANCOS" -name "Cartoes*" -type d -exec tag -a "Orange" {} \; 2>/dev/null
find "$BASE/05_BANCOS" -name "*Cartao*" -type d -exec tag -a "Orange" {} \; 2>/dev/null
find "$BASE/05_BANCOS" -name "Investimentos*" -type d -exec tag -a "Yellow" {} \; 2>/dev/null
find "$BASE/05_BANCOS" -name "Comprovantes*" -type d -exec tag -a "Pink" {} \; 2>/dev/null

# ===== 06 - FINANCEIRO =====
echo "  💰 Financeiro..."
tag -a "Yellow" "$BASE/06_FINANCEIRO" 2>/dev/null
find "$BASE/06_FINANCEIRO" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Yellow" {} \; 2>/dev/null
find "$BASE/06_FINANCEIRO" -maxdepth 2 -mindepth 2 -type d -exec tag -a "Yellow" {} \; 2>/dev/null

# ===== 07 - CLIENTES =====
echo "  👥 Clientes..."
tag -a "Pink" "$BASE/07_CLIENTES" 2>/dev/null
find "$BASE/07_CLIENTES" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Pink" {} \; 2>/dev/null
find "$BASE/07_CLIENTES" -maxdepth 2 -mindepth 2 -type d -exec tag -a "Pink" {} \; 2>/dev/null

# ===== 08 - FORNECEDORES =====
echo "  🏭 Fornecedores..."
tag -a "Gray" "$BASE/08_FORNECEDORES" 2>/dev/null
find "$BASE/08_FORNECEDORES" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Gray" {} \; 2>/dev/null
find "$BASE/08_FORNECEDORES" -maxdepth 2 -mindepth 2 -type d -exec tag -a "Gray" {} \; 2>/dev/null

# ===== 09 - SISTEMAS =====
echo "  💻 Sistemas..."
tag -a "Purple" "$BASE/09_SISTEMAS" 2>/dev/null
find "$BASE/09_SISTEMAS" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Purple" {} \; 2>/dev/null

# ===== 10 - BACKUP =====
echo "  💾 Backup..."
tag -a "Gray" "$BASE/10_BACKUP" 2>/dev/null
find "$BASE/10_BACKUP" -maxdepth 1 -mindepth 1 -type d -exec tag -a "Gray" {} \; 2>/dev/null

echo "✅ CORES APLICADAS EM TODO O SISTEMA!"
