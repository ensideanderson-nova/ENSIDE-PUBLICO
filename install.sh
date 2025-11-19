#!/bin/bash

###############################################################################
# SISTEMA ENSIDE - Script de Instalação
# Versão: 1.0
# Descrição: Instala e configura o Sistema ENSIDE completo
###############################################################################

set -e  # Sair em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

# Banner
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         SISTEMA ENSIDE - Instalação Completa             ║"
echo "║         Organização Inteligente de Documentos            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Verificar se está no macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "Este script é específico para macOS"
    exit 1
fi

# Verificar Python 3
print_status "Verificando Python 3..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 não encontrado. Instale via: brew install python3"
    exit 1
fi
print_success "Python 3 encontrado: $(python3 --version)"

# Verificar pip3
print_status "Verificando pip3..."
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 não encontrado"
    exit 1
fi
print_success "pip3 encontrado"

# Instalar dependências Python
print_status "Instalando dependências Python..."
pip3 install -r requirements.txt --quiet
print_success "Dependências instaladas"

# Criar estrutura principal
print_status "Criando estrutura em /Users/Shared/ENSIDE_ORGANIZADO/..."
if [ ! -d "/Users/Shared/ENSIDE_ORGANIZADO" ]; then
    sudo mkdir -p /Users/Shared/ENSIDE_ORGANIZADO
    sudo chown -R $USER:staff /Users/Shared/ENSIDE_ORGANIZADO
fi

# Executar script de criação
bash scripts/organize_master.sh
print_success "Estrutura principal criada"

# Criar workspace pessoal
print_status "Criando WORKSPACE em ~/WORKSPACE/..."
mkdir -p ~/WORKSPACE/{Scripts,Python,HTML,Projetos,Config,Documentos_PDF}
print_success "Workspace criado"

# Instalar skill do Claude Code
print_status "Instalando skill do Claude Code..."
mkdir -p ~/.claude/skills/organize-pdfs

# Copiar scripts
cp scripts/*.py ~/.claude/skills/organize-pdfs/
cp scripts/*.sh ~/.claude/skills/organize-pdfs/
cp requirements.txt ~/.claude/skills/organize-pdfs/

# Copiar documentação
cp docs/INSTALLATION.md ~/.claude/skills/organize-pdfs/GUIA_COMPLETO.md
cat > ~/.claude/skills/organize-pdfs/SKILL.md << 'EOF'
---
name: organize-pdfs
description: Sistema completo de organização de arquivos e documentos. Use quando o usuário pedir para organizar arquivos, PDFs, documentos, criar estrutura de pastas, aplicar cores/etiquetas, ou gerar mapa HTML do sistema. Funciona com ENSIDE_ORGANIZADO e WORKSPACE. Suporta organização automática, classificação inteligente e visualização com cores.
---

# Sistema ENSIDE - Skill de Organização

Esta skill organiza automaticamente arquivos em 14 categorias com detecção inteligente.

## Quando usar:
- Usuário pede para organizar arquivos
- Classificar documentos
- Importar pasta para o sistema
- Gerar visualização HTML
- Aplicar cores no Finder

## Comandos principais:

### Importar arquivos:
```bash
python3 ~/.claude/skills/organize-pdfs/importador_universal.py [PASTA_OU_ARQUIVO]
```

### Gerar HTML:
```bash
python3 ~/.claude/skills/organize-pdfs/gerar_html_completo.py
```

### Aplicar cores:
```bash
bash ~/.claude/skills/organize-pdfs/aplicar_cores_completo.sh
```

## Estrutura:
- 14 categorias organizadas
- Sistema de cores no Finder
- Detecção inteligente de conteúdo
- HTML interativo com filtros

Veja documentação completa em: ~/.claude/skills/organize-pdfs/GUIA_COMPLETO.md
EOF

# Tornar scripts executáveis
chmod +x ~/.claude/skills/organize-pdfs/*.py
chmod +x ~/.claude/skills/organize-pdfs/*.sh

print_success "Skill instalada"

# Aplicar cores
print_status "Aplicando cores no Finder..."
if command -v tag &> /dev/null; then
    bash ~/.claude/skills/organize-pdfs/aplicar_cores_completo.sh 2>/dev/null || true
    print_success "Cores aplicadas"
else
    print_warning "Comando 'tag' não encontrado. Cores não aplicadas."
    print_warning "Instale com: brew install tag"
fi

# Gerar HTML
print_status "Gerando visualização HTML..."
python3 ~/.claude/skills/organize-pdfs/gerar_html_completo.py
print_success "HTML gerado em ~/Desktop/SISTEMA_ENSIDE_COMPLETO.html"

# Criar atalho de importação
print_status "Criando atalho no Desktop..."
cat > ~/Desktop/IMPORTAR_AQUI.command << 'EOFCMD'
#!/bin/bash
clear
echo "════════════════════════════════════════════════════"
echo "  SISTEMA ENSIDE - Importador Universal"
echo "════════════════════════════════════════════════════"
echo ""
echo "Arraste arquivos/pastas aqui ou digite o caminho:"
echo "(Deixe em branco para cancelar)"
echo ""
read -e PASTA

if [ -z "$PASTA" ]; then
    echo "Cancelado."
    sleep 2
    exit 0
fi

# Remover aspas se houver
PASTA="${PASTA//\"/}"

if [ ! -e "$PASTA" ]; then
    echo ""
    echo "ERRO: Arquivo ou pasta não encontrado: $PASTA"
    sleep 3
    exit 1
fi

echo ""
echo "Organizando..."
python3 ~/.claude/skills/organize-pdfs/importador_universal.py "$PASTA"

echo ""
echo "════════════════════════════════════════════════════"
echo "  Concluído!"
echo "════════════════════════════════════════════════════"
echo ""
echo "Pressione ENTER para fechar..."
read
EOFCMD

chmod +x ~/Desktop/IMPORTAR_AQUI.command
print_success "Atalho criado"

# Resumo final
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              INSTALAÇÃO CONCLUÍDA COM SUCESSO!            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
print_success "Sistema instalado em: /Users/Shared/ENSIDE_ORGANIZADO/"
print_success "Workspace criado em: ~/WORKSPACE/"
print_success "Skill instalada em: ~/.claude/skills/organize-pdfs/"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  PRÓXIMOS PASSOS:"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "1. Teste o importador:"
echo "   python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Downloads"
echo ""
echo "2. Ou use o atalho no Desktop:"
echo "   Clique 2x em IMPORTAR_AQUI.command"
echo ""
echo "3. Visualize o sistema:"
echo "   open ~/Desktop/SISTEMA_ENSIDE_COMPLETO.html"
echo ""
echo "4. Use com Claude Code:"
echo '   "Organiza os arquivos da pasta Downloads"'
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  DOCUMENTAÇÃO:"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "README:     $(pwd)/README.md"
echo "Instalação: $(pwd)/docs/INSTALLATION.md"
echo "Exemplos:   $(pwd)/docs/EXEMPLOS.md"
echo ""
echo "Enjoy! "
echo ""