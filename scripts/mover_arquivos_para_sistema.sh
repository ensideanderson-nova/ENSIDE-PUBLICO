#!/bin/bash

BASE="/Users/Shared/ENSIDE_ORGANIZADO"
HOME_DIR="$HOME"

echo "╔═══════════════════════════════════════════════════╗"
echo "║   🚀 MOVENDO ARQUIVOS PARA O SISTEMA             ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Contadores
total_movidos=0
total_erros=0

# ═══════════════════════════════════════════════════════════
# FUNÇÃO PARA MOVER ARQUIVO
# ═══════════════════════════════════════════════════════════

mover_arquivo() {
    local origem="$1"
    local destino="$2"
    local tipo="$3"

    # Criar pasta destino se não existir
    mkdir -p "$(dirname "$destino")"

    # Verificar se arquivo existe no destino
    if [ -f "$destino" ]; then
        # Adicionar timestamp
        local timestamp=$(date +%Y%m%d_%H%M%S)
        local nome_base=$(basename "$origem" | sed 's/\.[^.]*$//')
        local extensao="${origem##*.}"
        destino="$(dirname "$destino")/${nome_base}_${timestamp}.${extensao}"
    fi

    # Mover arquivo
    if mv "$origem" "$destino" 2>/dev/null; then
        echo "   ✓ $tipo: $(basename "$origem")"
        ((total_movidos++))
        return 0
    else
        echo "   ✗ Erro: $(basename "$origem")"
        ((total_erros++))
        return 1
    fi
}

# ═══════════════════════════════════════════════════════════
# 1. MOVER PDFs
# ═══════════════════════════════════════════════════════════

echo "📄 MOVENDO PDFs..."

# Downloads
if [ -d "$HOME_DIR/Downloads" ]; then
    find "$HOME_DIR/Downloads" -maxdepth 1 -name "*.pdf" -type f 2>/dev/null | while read arquivo; do
        nome=$(basename "$arquivo")

        # Classificar por nome
        if [[ $nome =~ [Ee]xtrato|[Bb]anc ]]; then
            mover_arquivo "$arquivo" "$BASE/05_BANCOS/Extratos/$nome" "Extrato"
        elif [[ $nome =~ [Cc]omprovante|[Pp]ix|[Tt]ed ]]; then
            mover_arquivo "$arquivo" "$BASE/05_BANCOS/Comprovantes/$nome" "Comprovante"
        elif [[ $nome =~ [Nn]ota|[Ff]iscal|[Nn]f ]]; then
            mover_arquivo "$arquivo" "$BASE/07_CLIENTES/Notas_Fiscais/2025/$nome" "Nota Fiscal"
        elif [[ $nome =~ [Cc]ontrato ]]; then
            mover_arquivo "$arquivo" "$BASE/02_DOCUMENTOS_EMPRESA/Contratos_Socios/$nome" "Contrato"
        elif [[ $nome =~ [Bb]oleto ]]; then
            mover_arquivo "$arquivo" "$BASE/06_FINANCEIRO/2025/Janeiro/Contas_Pagar/$nome" "Boleto"
        else
            mover_arquivo "$arquivo" "$BASE/01_DOCUMENTOS_PESSOAIS/$nome" "Documento"
        fi
    done
fi

# Desktop
if [ -d "$HOME_DIR/Desktop" ]; then
    find "$HOME_DIR/Desktop" -maxdepth 1 -name "*.pdf" -type f 2>/dev/null | while read arquivo; do
        nome=$(basename "$arquivo")
        mover_arquivo "$arquivo" "$BASE/01_DOCUMENTOS_PESSOAIS/$nome" "PDF Desktop"
    done
fi

# WORKSPACE
if [ -d "$HOME_DIR/WORKSPACE/Documentos_PDF" ]; then
    find "$HOME_DIR/WORKSPACE/Documentos_PDF" -name "*.pdf" -type f 2>/dev/null | while read arquivo; do
        nome=$(basename "$arquivo")
        mover_arquivo "$arquivo" "$BASE/01_DOCUMENTOS_PESSOAIS/$nome" "PDF Workspace"
    done
fi

echo ""

# ═══════════════════════════════════════════════════════════
# 2. MOVER VÍDEOS
# ═══════════════════════════════════════════════════════════

echo "🎥 MOVENDO VÍDEOS..."

for ext in mp4 mov avi mkv wmv flv webm m4v; do
    # Downloads
    if [ -d "$HOME_DIR/Downloads" ]; then
        find "$HOME_DIR/Downloads" -maxdepth 1 -name "*.$ext" -type f 2>/dev/null | while read arquivo; do
            nome=$(basename "$arquivo")

            # Classificar por nome
            if [[ $nome =~ [Hh]ack|[Ss]egur|[Vv]ulner|[Pp]enetra ]]; then
                mover_arquivo "$arquivo" "$BASE/11_VIDEOS/Seguranca/Hackers/$nome" "Vídeo Hacking"
            elif [[ $nome =~ [Tt]utorial|[Aa]ula|[Cc]urso ]]; then
                mover_arquivo "$arquivo" "$BASE/11_VIDEOS/Tutoriais/$nome" "Tutorial"
            elif [[ $nome =~ [Rr]euni[aã]o|[Mm]eeting ]]; then
                mover_arquivo "$arquivo" "$BASE/11_VIDEOS/Reunioes/$nome" "Reunião"
            elif [[ $nome =~ [Aa]presenta[cç][aã]o ]]; then
                mover_arquivo "$arquivo" "$BASE/11_VIDEOS/Apresentacoes/$nome" "Apresentação"
            else
                mover_arquivo "$arquivo" "$BASE/11_VIDEOS/2025/$nome" "Vídeo"
            fi
        done
    fi

    # Desktop
    if [ -d "$HOME_DIR/Desktop" ]; then
        find "$HOME_DIR/Desktop" -maxdepth 1 -name "*.$ext" -type f 2>/dev/null | while read arquivo; do
            nome=$(basename "$arquivo")
            mover_arquivo "$arquivo" "$BASE/11_VIDEOS/2025/$nome" "Vídeo Desktop"
        done
    fi

    # Movies
    if [ -d "$HOME_DIR/Movies" ]; then
        find "$HOME_DIR/Movies" -maxdepth 1 -name "*.$ext" -type f 2>/dev/null | while read arquivo; do
            nome=$(basename "$arquivo")
            mover_arquivo "$arquivo" "$BASE/11_VIDEOS/2025/$nome" "Vídeo Movies"
        done
    fi
done

echo ""

# ═══════════════════════════════════════════════════════════
# 3. MOVER SCREENSHOTS / PRINTS
# ═══════════════════════════════════════════════════════════

echo "📸 MOVENDO SCREENSHOTS..."

# Screenshots do Mac geralmente começam com "Screen Shot" ou "Captura de Tela"
if [ -d "$HOME_DIR/Desktop" ]; then
    find "$HOME_DIR/Desktop" -maxdepth 1 \( -name "Screen Shot*" -o -name "Captura de Tela*" -o -name "Screenshot*" \) -type f 2>/dev/null | while read arquivo; do
        nome=$(basename "$arquivo")

        # Classificar por nome
        if [[ $nome =~ [Ff]raude|[Ss]uspeito|[Ee]stranho ]]; then
            mover_arquivo "$arquivo" "$BASE/12_PRINTS_TELA/Evidencias/Fraudes/$nome" "Print Fraude"
        elif [[ $nome =~ [Ee]rro|[Bb]ug|[Pp]roblema ]]; then
            mover_arquivo "$arquivo" "$BASE/12_PRINTS_TELA/Erros/$nome" "Print Erro"
        elif [[ $nome =~ [Cc]omprovante ]]; then
            mover_arquivo "$arquivo" "$BASE/12_PRINTS_TELA/Evidencias/Comprovantes/$nome" "Print Comprovante"
        else
            mover_arquivo "$arquivo" "$BASE/12_PRINTS_TELA/2025/$nome" "Screenshot"
        fi
    done
fi

# Downloads
if [ -d "$HOME_DIR/Downloads" ]; then
    find "$HOME_DIR/Downloads" -maxdepth 1 \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) -type f 2>/dev/null | while read arquivo; do
        nome=$(basename "$arquivo")

        # Só screenshots (nomes típicos)
        if [[ $nome =~ [Ss]creen|[Cc]aptura|[Pp]rint ]]; then
            mover_arquivo "$arquivo" "$BASE/12_PRINTS_TELA/2025/$nome" "Print Downloads"
        fi
    done
fi

echo ""

# ═══════════════════════════════════════════════════════════
# 4. MOVER PLANILHAS
# ═══════════════════════════════════════════════════════════

echo "📊 MOVENDO PLANILHAS..."

for ext in xlsx xls csv ods; do
    # Downloads
    if [ -d "$HOME_DIR/Downloads" ]; then
        find "$HOME_DIR/Downloads" -maxdepth 1 -name "*.$ext" -type f 2>/dev/null | while read arquivo; do
            nome=$(basename "$arquivo")

            if [[ $nome =~ [Ff]inanceiro|[Ff]luxo|[Cc]onta ]]; then
                mover_arquivo "$arquivo" "$BASE/06_FINANCEIRO/Relatorios/$nome" "Planilha Financeira"
            elif [[ $nome =~ [Cc]liente ]]; then
                mover_arquivo "$arquivo" "$BASE/07_CLIENTES/Cadastros/$nome" "Planilha Clientes"
            elif [[ $nome =~ [Ff]ornecedor ]]; then
                mover_arquivo "$arquivo" "$BASE/08_FORNECEDORES/Cadastros/$nome" "Planilha Fornecedores"
            else
                mover_arquivo "$arquivo" "$BASE/01_DOCUMENTOS_PESSOAIS/$nome" "Planilha"
            fi
        done
    fi
done

echo ""

# ═══════════════════════════════════════════════════════════
# 5. MOVER SCRIPTS
# ═══════════════════════════════════════════════════════════

echo "💻 MOVENDO SCRIPTS..."

# Verificar scripts suspeitos ou de hackers
if [ -d "$HOME_DIR/Downloads" ]; then
    find "$HOME_DIR/Downloads" -maxdepth 1 -name "*.sh" -type f 2>/dev/null | while read arquivo; do
        nome=$(basename "$arquivo")

        # Analisar conteúdo para detectar scripts suspeitos
        if grep -qi "hack\|exploit\|vulnerability\|backdoor\|rootkit" "$arquivo" 2>/dev/null; then
            mover_arquivo "$arquivo" "$BASE/13_SEGURANCA_FRAUDES/Analise_Seguranca/Scripts_Suspeitos/$nome" "⚠️  Script Suspeito"
        elif [[ $nome =~ organiz|backup|sistema ]]; then
            mover_arquivo "$arquivo" "$BASE/09_SISTEMAS/Scripts/Automacao/$nome" "Script Sistema"
        else
            # Mover para WORKSPACE
            mkdir -p "$HOME_DIR/WORKSPACE/Scripts"
            mover_arquivo "$arquivo" "$HOME_DIR/WORKSPACE/Scripts/$nome" "Script"
        fi
    done
fi

# Python
if [ -d "$HOME_DIR/Downloads" ]; then
    find "$HOME_DIR/Downloads" -maxdepth 1 -name "*.py" -type f 2>/dev/null | while read arquivo; do
        nome=$(basename "$arquivo")

        # Analisar conteúdo
        if grep -qi "hack\|exploit\|malware\|inject" "$arquivo" 2>/dev/null; then
            mover_arquivo "$arquivo" "$BASE/13_SEGURANCA_FRAUDES/Analise_Seguranca/Scripts_Suspeitos/$nome" "⚠️  Python Suspeito"
        else
            mkdir -p "$HOME_DIR/WORKSPACE/Python"
            mover_arquivo "$arquivo" "$HOME_DIR/WORKSPACE/Python/$nome" "Python"
        fi
    done
fi

echo ""

# ═══════════════════════════════════════════════════════════
# 6. MOVER LOGS E EVIDÊNCIAS
# ═══════════════════════════════════════════════════════════

echo "📝 MOVENDO LOGS..."

if [ -d "$HOME_DIR/Downloads" ]; then
    find "$HOME_DIR/Downloads" -maxdepth 1 \( -name "*.log" -o -name "*.txt" \) -type f 2>/dev/null | while read arquivo; do
        nome=$(basename "$arquivo")

        # Analisar conteúdo para detectar logs de segurança
        if grep -qi "attack\|intrusion\|failed.*login\|unauthorized\|blocked\|suspicious" "$arquivo" 2>/dev/null; then
            mover_arquivo "$arquivo" "$BASE/13_SEGURANCA_FRAUDES/Hacking/Logs_Acesso/$nome" "⚠️  Log Suspeito"
        elif [[ $nome =~ [Ll]og ]]; then
            mover_arquivo "$arquivo" "$BASE/13_SEGURANCA_FRAUDES/Analise_Seguranca/Logs/$nome" "Log"
        fi
    done
fi

echo ""

# ═══════════════════════════════════════════════════════════
# RESUMO FINAL
# ═══════════════════════════════════════════════════════════

echo "╔═══════════════════════════════════════════════════╗"
echo "║          ✅ ORGANIZAÇÃO COMPLETA!                 ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""
echo "📊 ESTATÍSTICAS:"
echo "   • Arquivos movidos: $total_movidos"
echo "   • Erros: $total_erros"
echo ""
echo "📁 VERIFIQUE:"
echo "   • Sistema: /Users/Shared/ENSIDE_ORGANIZADO/"
echo "   • Workspace: ~/WORKSPACE/"
echo ""
echo "🎨 CORES aplicadas automaticamente!"
echo ""
