#!/bin/bash

HOME_DIR="$HOME"
WORKSPACE="$HOME/WORKSPACE"
BASE="/Users/Shared/ENSIDE_ORGANIZADO"

echo "╔═══════════════════════════════════════════════════╗"
echo "║   🚀 ORGANIZANDO HOME COMPLETA                    ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Criar WORKSPACE se não existir
mkdir -p "$WORKSPACE"/{Scripts,Python,HTML,Config,Projetos}

total=0

# ═══════════════════════════════════════════════════════════
# 1. MOVER SCRIPTS .sh
# ═══════════════════════════════════════════════════════════

echo "💻 Movendo scripts .sh..."
find "$HOME_DIR" -maxdepth 1 -name "*.sh" -type f 2>/dev/null | while read arquivo; do
    if mv "$arquivo" "$WORKSPACE/Scripts/" 2>/dev/null; then
        echo "   ✓ $(basename "$arquivo")"
        ((total++))
    fi
done

# ═══════════════════════════════════════════════════════════
# 2. MOVER PYTHON .py
# ═══════════════════════════════════════════════════════════

echo "🐍 Movendo arquivos .py..."
find "$HOME_DIR" -maxdepth 1 -name "*.py" -type f 2>/dev/null | while read arquivo; do
    if mv "$arquivo" "$WORKSPACE/Python/" 2>/dev/null; then
        echo "   ✓ $(basename "$arquivo")"
        ((total++))
    fi
done

# ═══════════════════════════════════════════════════════════
# 3. MOVER HTML
# ═══════════════════════════════════════════════════════════

echo "🌐 Movendo arquivos .html..."
find "$HOME_DIR" -maxdepth 1 -name "*.html" -type f 2>/dev/null | while read arquivo; do
    if mv "$arquivo" "$WORKSPACE/HTML/" 2>/dev/null; then
        echo "   ✓ $(basename "$arquivo")"
        ((total++))
    fi
done

# ═══════════════════════════════════════════════════════════
# 4. MOVER CONFIG
# ═══════════════════════════════════════════════════════════

echo "⚙️  Movendo arquivos de config..."
find "$HOME_DIR" -maxdepth 1 \( -name "*.json" -o -name "*.yml" -o -name "*.yaml" -o -name "*.md" -o -name "*.txt" \) -type f 2>/dev/null | while read arquivo; do
    nome=$(basename "$arquivo")
    # Pular alguns arquivos importantes
    if [[ ! "$nome" =~ ^(\.|README|package\.json)$ ]]; then
        if mv "$arquivo" "$WORKSPACE/Config/" 2>/dev/null; then
            echo "   ✓ $nome"
            ((total++))
        fi
    fi
done

# ═══════════════════════════════════════════════════════════
# 5. MOVER PASTAS DE PROJETOS
# ═══════════════════════════════════════════════════════════

echo "📁 Movendo pastas de projetos..."

# Lista de pastas para mover (projetos conhecidos)
pastas_projetos=(
    "Enside-Dev"
    "sistema-anderson-enside"
    "sistema-CONSOLE-captacao-motoristas"
    "AnalisadorPDF-Claude"
    "anthropic-sdk-csharp"
)

for pasta in "${pastas_projetos[@]}"; do
    if [ -d "$HOME_DIR/$pasta" ]; then
        if mv "$HOME_DIR/$pasta" "$WORKSPACE/Projetos/" 2>/dev/null; then
            echo "   ✓ $pasta/"
            ((total++))
        fi
    fi
done

# ═══════════════════════════════════════════════════════════
# 6. REMOVER BACKUPS ANTIGOS
# ═══════════════════════════════════════════════════════════

echo "🗑️  Removendo backups antigos..."
find "$HOME_DIR" -maxdepth 1 -name "*BACKUP*" -type d 2>/dev/null | while read pasta; do
    echo "   → $(basename "$pasta") para lixeira"
    mv "$pasta" ~/.Trash/ 2>/dev/null || true
done

echo ""
echo "✅ ORGANIZAÇÃO DA HOME COMPLETA!"
echo ""
echo "📊 Arquivos organizados!"
echo ""
echo "📍 Localização:"
echo "   • Scripts: $WORKSPACE/Scripts/"
echo "   • Python: $WORKSPACE/Python/"
echo "   • HTML: $WORKSPACE/HTML/"
echo "   • Config: $WORKSPACE/Config/"
echo "   • Projetos: $WORKSPACE/Projetos/"
echo ""
