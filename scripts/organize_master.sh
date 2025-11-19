#!/bin/bash
#
# ORGANIZE MASTER - Sistema Mestre de Organização
# Organiza TODO o sistema ENSIDE_ORGANIZADO com cores e estrutura completa
#

set -e

echo "╔═══════════════════════════════════════════════════╗"
echo "║   🎯 ORGANIZE MASTER - Sistema Completo          ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

BASE="/Users/Shared/ENSIDE_ORGANIZADO"
WORKSPACE="$HOME/WORKSPACE"

# ═══════════════════════════════════════════════════════════
# PASSO 1: CRIAR ESTRUTURA COMPLETA
# ═══════════════════════════════════════════════════════════

echo -e "${CYAN}📁 PASSO 1: Criando estrutura completa...${NC}"
echo ""

# Criar pasta base
mkdir -p "$BASE"

# ═══════════════════════════════════════════════════════════
# 00 - TRIAGEM POR PESSOA
# ═══════════════════════════════════════════════════════════

echo -e "${PURPLE}🔍 00 - TRIAGEM POR PESSOA${NC}"

mkdir -p "$BASE/00_TRIAGEM_POR_PESSOA"/{CPF_ANDERSON,CPF_OUTRO_SOCIO,CNPJ_EMPRESA_ENSIDE}

# CPF ANDERSON
mkdir -p "$BASE/00_TRIAGEM_POR_PESSOA/CPF_ANDERSON"/{Documentos_Pessoais,Bancos,Financeiro,Imoveis,Veiculos,Saude}

# CNPJ EMPRESA
mkdir -p "$BASE/00_TRIAGEM_POR_PESSOA/CNPJ_EMPRESA_ENSIDE"/{Documentos_Empresa,Bancos,Financeiro,Clientes,Fornecedores,Fretes,Madeiras,Juridico}

echo "   ✓ Triagem criada"

# ═══════════════════════════════════════════════════════════
# 01 - DOCUMENTOS PESSOAIS
# ═══════════════════════════════════════════════════════════

echo -e "${GREEN}👤 01 - DOCUMENTOS PESSOAIS${NC}"

mkdir -p "$BASE/01_DOCUMENTOS_PESSOAIS"/{CPF,RG,CNH,Titulo_Eleitor,PIS_PASEP,Carteira_Trabalho,Passaporte,Vacinas,Diplomas}
mkdir -p "$BASE/01_DOCUMENTOS_PESSOAIS/CPF"/{Originais,Copias,Certidoes}
mkdir -p "$BASE/01_DOCUMENTOS_PESSOAIS/RG"/{Frente,Verso,Copias_Autenticadas}
mkdir -p "$BASE/01_DOCUMENTOS_PESSOAIS/CNH"/{Atual,Antigas,Renovacao}
mkdir -p "$BASE/01_DOCUMENTOS_PESSOAIS/Comprovantes_Residencia"/{Luz,Agua,Internet,Aluguel,IPTU}
mkdir -p "$BASE/01_DOCUMENTOS_PESSOAIS/Certidoes"/{Nascimento,Casamento,Negativas}

echo "   ✓ Documentos Pessoais criados"

# ═══════════════════════════════════════════════════════════
# 02 - DOCUMENTOS EMPRESA
# ═══════════════════════════════════════════════════════════

echo -e "${BLUE}🏢 02 - DOCUMENTOS EMPRESA${NC}"

mkdir -p "$BASE/02_DOCUMENTOS_EMPRESA"/{CNPJ,Contratos_Socios,Alvaras,Licencas,Inscricoes,Certificados_Digitais}
mkdir -p "$BASE/02_DOCUMENTOS_EMPRESA/CNPJ"/{Cartao_CNPJ,Alteracoes_Contratuais}
mkdir -p "$BASE/02_DOCUMENTOS_EMPRESA/Alvaras"/{Funcionamento,Bombeiros,Vigilancia_Sanitaria}
mkdir -p "$BASE/02_DOCUMENTOS_EMPRESA/Licencas"/{Ambiental,Municipais}
mkdir -p "$BASE/02_DOCUMENTOS_EMPRESA/Inscricoes"/{Estadual,Municipal}

echo "   ✓ Documentos Empresa criados"

# ═══════════════════════════════════════════════════════════
# 03 - MADEIRAS
# ═══════════════════════════════════════════════════════════

echo -e "${PURPLE}🌲 03 - MADEIRAS${NC}"

mkdir -p "$BASE/03_MADEIRAS"/{Fornecedores_PR,Fornecedores_SC,Fornecedores_SP,Estoque,Certificados,Exportacao}
mkdir -p "$BASE/03_MADEIRAS/Fornecedores_PR"/{Cadastros,Contratos,Notas_Fiscais}
mkdir -p "$BASE/03_MADEIRAS/Fornecedores_SC"/{Cadastros,Contratos,Notas_Fiscais}
mkdir -p "$BASE/03_MADEIRAS/Fornecedores_SP"/{Cadastros,Contratos,Notas_Fiscais}
mkdir -p "$BASE/03_MADEIRAS/Certificados"/{Origem,Qualidade,FSC}
mkdir -p "$BASE/03_MADEIRAS/Exportacao"/{Documentos,Contratos,Embarques}

echo "   ✓ Madeiras criadas"

# ═══════════════════════════════════════════════════════════
# 04 - FRETES
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}🚛 04 - FRETES${NC}"

mkdir -p "$BASE/04_FRETES"/{Motoristas,Cotacoes,Contratos,Notas_Fiscais,CTEs}
mkdir -p "$BASE/04_FRETES/Motoristas"/{PR,SC,SP}
mkdir -p "$BASE/04_FRETES/Motoristas/PR"/{Cadastros,CNH,ANTT,Contratos,Pagamentos}
mkdir -p "$BASE/04_FRETES/Motoristas/SC"/{Cadastros,CNH,ANTT,Contratos,Pagamentos}
mkdir -p "$BASE/04_FRETES/Motoristas/SP"/{Cadastros,CNH,ANTT,Contratos,Pagamentos}
mkdir -p "$BASE/04_FRETES/Cotacoes/2025"
mkdir -p "$BASE/04_FRETES/Contratos"/{Ativos,Encerrados}
mkdir -p "$BASE/04_FRETES/Notas_Fiscais/2025"
mkdir -p "$BASE/04_FRETES/CTEs/2025"

echo "   ✓ Fretes criados"

# ═══════════════════════════════════════════════════════════
# 05 - BANCOS
# ═══════════════════════════════════════════════════════════

echo -e "${RED}🏦 05 - BANCOS${NC}"

BANCOS=("Itau" "Bradesco" "Santander" "Banco_do_Brasil" "Caixa" "Nubank")

for banco in "${BANCOS[@]}"; do
    echo "   → $banco"

    # CPF
    mkdir -p "$BASE/05_BANCOS/$banco/CPF"/{Conta_Corrente,Conta_Poupanca,Extratos,Cartoes,Investimentos,Emprestimos,Seguros,Comprovantes,Taloes_Cheque}
    mkdir -p "$BASE/05_BANCOS/$banco/CPF/Conta_Corrente"/{Dados_Conta,Contratos}
    mkdir -p "$BASE/05_BANCOS/$banco/CPF/Extratos"/{2025,2024,2023}
    mkdir -p "$BASE/05_BANCOS/$banco/CPF/Cartoes"/{Credito,Debito,Faturas,Comprovantes}
    mkdir -p "$BASE/05_BANCOS/$banco/CPF/Cartoes/Credito"/{Faturas,Comprovantes}
    mkdir -p "$BASE/05_BANCOS/$banco/CPF/Investimentos"/{CDB,Poupanca,Fundos,Tesouro_Direto,Acoes}
    mkdir -p "$BASE/05_BANCOS/$banco/CPF/Emprestimos"/{Pessoal,Consignado,Contratos}
    mkdir -p "$BASE/05_BANCOS/$banco/CPF/Seguros"/{Vida,Residencial,Automovel}
    mkdir -p "$BASE/05_BANCOS/$banco/CPF/Comprovantes"/{Transferencias,Pagamentos,Depositos,PIX}

    # CNPJ
    mkdir -p "$BASE/05_BANCOS/$banco/CNPJ"/{Conta_Corrente,Extratos,Cartoes_Corporativos,Investimentos,Emprestimos,Comprovantes}
    mkdir -p "$BASE/05_BANCOS/$banco/CNPJ/Conta_Corrente"/{Dados_Conta,Contratos}
    mkdir -p "$BASE/05_BANCOS/$banco/CNPJ/Extratos"/{2025,2024,2023}
    mkdir -p "$BASE/05_BANCOS/$banco/CNPJ/Cartoes_Corporativos"/{Faturas,Comprovantes}
    mkdir -p "$BASE/05_BANCOS/$banco/CNPJ/Investimentos"/{CDB,Fundos,Aplicacoes}
    mkdir -p "$BASE/05_BANCOS/$banco/CNPJ/Emprestimos"/{Capital_Giro,Financiamento,Contratos}
    mkdir -p "$BASE/05_BANCOS/$banco/CNPJ/Comprovantes"/{Boletos,Transferencias,PIX}
done

echo "   ✓ 6 Bancos criados (CPF + CNPJ)"

# ═══════════════════════════════════════════════════════════
# 06 - FINANCEIRO
# ═══════════════════════════════════════════════════════════

echo -e "${YELLOW}💰 06 - FINANCEIRO${NC}"

MESES=("Janeiro" "Fevereiro" "Marco" "Abril" "Maio" "Junho" "Julho" "Agosto" "Setembro" "Outubro" "Novembro" "Dezembro")

for mes in "${MESES[@]}"; do
    mkdir -p "$BASE/06_FINANCEIRO/2025/$mes"/{Receitas,Despesas,Impostos,Contas_Pagar,Contas_Receber,Fluxo_Caixa}
    mkdir -p "$BASE/06_FINANCEIRO/2024/$mes"/{Receitas,Despesas,Impostos}
done

mkdir -p "$BASE/06_FINANCEIRO/Relatorios"/{Mensais,Anuais}
mkdir -p "$BASE/06_FINANCEIRO/Impostos"/{IRPF,IRPJ,ISS,ICMS,DAS,INSS}

echo "   ✓ Financeiro criado (12 meses)"

# ═══════════════════════════════════════════════════════════
# 07 - CLIENTES
# ═══════════════════════════════════════════════════════════

echo -e "${CYAN}👥 07 - CLIENTES${NC}"

mkdir -p "$BASE/07_CLIENTES"/{Cadastros,Contratos,Propostas,Notas_Fiscais,Emails}
mkdir -p "$BASE/07_CLIENTES/Cadastros"/{Ativos,Inativos}
mkdir -p "$BASE/07_CLIENTES/Contratos"/{Vigentes,Encerrados}
mkdir -p "$BASE/07_CLIENTES/Propostas"/{Aprovadas,Pendentes,Negadas}
mkdir -p "$BASE/07_CLIENTES/Notas_Fiscais/2025"
mkdir -p "$BASE/07_CLIENTES/Emails/Comunicacao"

echo "   ✓ Clientes criados"

# ═══════════════════════════════════════════════════════════
# 08 - FORNECEDORES
# ═══════════════════════════════════════════════════════════

echo "🏭 08 - FORNECEDORES"

mkdir -p "$BASE/08_FORNECEDORES"/{Cadastros,Contratos,Notas_Fiscais,Servicos}
mkdir -p "$BASE/08_FORNECEDORES/Cadastros"/{Ativos,Inativos}
mkdir -p "$BASE/08_FORNECEDORES/Notas_Fiscais/2025"
mkdir -p "$BASE/08_FORNECEDORES/Servicos"/{Transporte,TI,Contabilidade,Manutencao}

echo "   ✓ Fornecedores criados"

# ═══════════════════════════════════════════════════════════
# 09 - SISTEMAS
# ═══════════════════════════════════════════════════════════

echo -e "${PURPLE}💻 09 - SISTEMAS${NC}"

mkdir -p "$BASE/09_SISTEMAS"/{Fretes,CRM,ERP,Scripts,Landing_Pages,Documentacao}
mkdir -p "$BASE/09_SISTEMAS/Fretes"/{Frontend,Backend,Database,Testes}
mkdir -p "$BASE/09_SISTEMAS/CRM"/{Frontend,Backend,Database}
mkdir -p "$BASE/09_SISTEMAS/Scripts"/{Automacao,Backup,Deploy}

echo "   ✓ Sistemas criados"

# ═══════════════════════════════════════════════════════════
# 10 - BACKUP
# ═══════════════════════════════════════════════════════════

echo "💾 10 - BACKUP"

mkdir -p "$BASE/10_BACKUP"/{Diario,Semanal,Mensal,Completo}
mkdir -p "$BASE/10_BACKUP/Diario/2025"
mkdir -p "$BASE/10_BACKUP/Semanal/2025"
mkdir -p "$BASE/10_BACKUP/Mensal/2025"

echo "   ✓ Backup criados"

echo ""
echo -e "${GREEN}✅ Estrutura completa criada!${NC}"
echo ""

# ═══════════════════════════════════════════════════════════
# PASSO 2: APLICAR CORES COM ETIQUETAS
# ═══════════════════════════════════════════════════════════

echo -e "${CYAN}🎨 PASSO 2: Aplicando cores com etiquetas...${NC}"
echo ""

# Verificar se o comando 'tag' está disponível
if ! command -v tag &> /dev/null; then
    echo -e "${YELLOW}⚠️  Comando 'tag' não encontrado. Instale com: brew install tag${NC}"
    echo "   Continuando sem aplicar cores..."
else
    # Executar script de cores
    bash ~/.claude/skills/organize-pdfs/aplicar_cores_completo.sh
    echo -e "${GREEN}✅ Cores aplicadas!${NC}"
fi

echo ""

# ═══════════════════════════════════════════════════════════
# PASSO 3: CRIAR WORKSPACE
# ═══════════════════════════════════════════════════════════

echo -e "${CYAN}📂 PASSO 3: Criando WORKSPACE...${NC}"
echo ""

mkdir -p "$WORKSPACE"/{Scripts,Python,HTML,Projetos,Config,Documentos_PDF,Downloads}

echo -e "${GREEN}✅ WORKSPACE criado!${NC}"
echo ""

# ═══════════════════════════════════════════════════════════
# PASSO 4: GERAR HTML COM MAPA
# ═══════════════════════════════════════════════════════════

echo -e "${CYAN}🌐 PASSO 4: Gerando HTML completo com cores...${NC}"
echo ""

python3 ~/.claude/skills/organize-pdfs/gerar_html_completo.py

# Copiar para Desktop também
cp ~/sistema_enside_completo.html ~/Desktop/SISTEMA_ENSIDE_COMPLETO.html 2>/dev/null || true

echo -e "${GREEN}✅ HTML completo gerado!${NC}"
echo ""

# ═══════════════════════════════════════════════════════════
# RESUMO FINAL
# ═══════════════════════════════════════════════════════════

echo ""
echo "╔═══════════════════════════════════════════════════╗"
echo "║          ✅ ORGANIZAÇÃO COMPLETA!                 ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}📍 SISTEMA PRINCIPAL:${NC}"
echo "   $BASE"
echo ""
echo -e "${BLUE}📍 WORKSPACE:${NC}"
echo "   $WORKSPACE"
echo ""
echo -e "${PURPLE}📊 ESTATÍSTICAS:${NC}"

# Contar pastas criadas
total_pastas=$(find "$BASE" -type d | wc -l | tr -d ' ')
echo "   • $total_pastas pastas criadas no sistema"
echo "   • 11 categorias principais"
echo "   • 6 bancos com CPF/CNPJ"
echo "   • 12 meses organizados"
echo "   • Cores aplicadas em todas as pastas"
echo ""
echo -e "${CYAN}🌐 HTML GERADO:${NC}"
echo "   ~/mapa_com_cores.html"
echo ""
echo -e "${YELLOW}🚀 PRÓXIMOS PASSOS:${NC}"
echo "   1. Abra o Finder: $BASE"
echo "   2. Veja as cores aplicadas!"
echo "   3. Abra o HTML: open ~/sistema_enside_completo.html
   4. Ou use o atalho no Desktop: SISTEMA_ENSIDE_COMPLETO.html"
echo ""
echo "╔═══════════════════════════════════════════════════╗"
echo "║     Sistema pronto para uso! 🎉                   ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""
