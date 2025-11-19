# Exemplos de Uso - Sistema ENSIDE

## Casos de Uso Comuns

### 1. Organizar Pasta Downloads

**Cenário:** Você tem dezenas de PDFs, comprovantes e documentos na pasta Downloads.

```bash
# Importar tudo de uma vez
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Downloads
```

**Resultado:**
- Extratos bancários → `05_BANCOS/[Banco]/Extratos/2025/`
- Comprovantes → `05_BANCOS/[Banco]/Comprovantes/`
- Notas Fiscais → `07_CLIENTES/` ou `08_FORNECEDORES/`
- Boletos → `06_FINANCEIRO/Contas_Pagar/`
- Prints → `12_PRINTS_TELA/`

### 2. Classificar Documento Específico

**Cenário:** Você recebeu um extrato bancário por email e salvou no Desktop.

```bash
# Organizar arquivo específico
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Desktop/extrato_itau.pdf
```

**Detecção Automática:**
1. Sistema lê o PDF
2. Detecta "Itaú" e "extrato"
3. Move para: `05_BANCOS/Itau/Extratos/2025/11/extrato_itau.pdf`
4. Aplica cor vermelha

### 3. Modo Teste (Dry-run)

**Cenário:** Você quer ver onde os arquivos seriam organizados sem movê-los.

```bash
# Simular organização
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Downloads --dry-run
```

**Saída:**
```
MODO SIMULAÇÃO - Nenhum arquivo será movido

Análise de: contrato_cliente_xpto.pdf
→ Detectado: Contrato
→ Destino: /Users/Shared/ENSIDE_ORGANIZADO/07_CLIENTES/Contratos/
→ Cor: Rosa

Análise de: boleto_fornecedor.pdf
→ Detectado: Boleto
→ Destino: /Users/Shared/ENSIDE_ORGANIZADO/06_FINANCEIRO/Contas_Pagar/
→ Cor: Amarelo

Total: 2 arquivos analisados
```

### 4. Organizar via Claude Code

**Cenário:** Você prefere usar linguagem natural.

```
Você: "Organiza os arquivos da pasta Downloads"

Claude: Vou organizar os arquivos da pasta Downloads usando o Sistema ENSIDE.

[Executa: python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Downloads]

Pronto! Organizei 47 arquivos:
- 12 extratos bancários → 05_BANCOS/
- 8 notas fiscais → 07_CLIENTES/
- 15 comprovantes → 05_BANCOS/
- 5 contratos → 02_DOCUMENTOS_EMPRESA/
- 7 prints → 12_PRINTS_TELA/
```

### 5. Importar Pasta de Projeto

**Cenário:** Você tem uma pasta com código-fonte de um projeto Python.

```bash
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Desktop/MeuProjeto
```

**Resultado:**
```
MeuProjeto/
├── *.py → ~/WORKSPACE/Python/MeuProjeto/
├── *.html → ~/WORKSPACE/HTML/MeuProjeto/
├── *.sh → ~/WORKSPACE/Scripts/MeuProjeto/
├── *.json → ~/WORKSPACE/Config/MeuProjeto/
└── *.pdf → ~/WORKSPACE/Documentos_PDF/MeuProjeto/
```

## Detecções Automáticas

### Exemplo 1: Extrato Bancário Itaú

**Arquivo:** `extrato_itau_novembro_2025.pdf`

**Conteúdo do PDF:**
```
BANCO ITAÚ
Extrato de Conta Corrente
Período: 01/11/2025 a 30/11/2025
...
```

**Detecção:**
1. Palavra-chave: "itau" ou "itaú"
2. Palavra-chave: "extrato"
3. Detecta CPF ou CNPJ no conteúdo

**Destino:**
- Com CPF: `05_BANCOS/Itau/CPF/Extratos/2025/11/extrato_itau_novembro_2025.pdf`
- Com CNPJ: `05_BANCOS/Itau/CNPJ/Extratos/2025/11/extrato_itau_novembro_2025.pdf`

**Cor:** Vermelho

### Exemplo 2: Nota Fiscal

**Arquivo:** `nf_12345_cliente_abc.pdf`

**Conteúdo do PDF:**
```
NOTA FISCAL ELETRÔNICA
NF-e: 12345
Cliente: ABC Comércio LTDA
...
```

**Detecção:**
1. Palavra-chave: "nota fiscal" ou "nfe"
2. Detecta se é emitida (fornecedor) ou recebida (cliente)

**Destino:**
- Emitida: `07_CLIENTES/ABC_Comercio/Notas_Fiscais/2025/nf_12345_cliente_abc.pdf`
- Recebida: `08_FORNECEDORES/ABC_Comercio/Notas_Fiscais/2025/nf_12345_cliente_abc.pdf`

**Cor:** Rosa (cliente) ou Cinza (fornecedor)

### Exemplo 3: Documento de Segurança

**Arquivo:** `tentativa_fraude_analise.pdf`

**Conteúdo:**
```
Análise de tentativa de fraude
Cheque suspeito identificado
...
```

**Detecção:**
1. Palavra-chave: "fraude"
2. Palavra-chave: "cheque suspeito"
3. Categoria: Segurança

**Destino:**
`13_SEGURANCA_FRAUDES/Analises/2025/tentativa_fraude_analise.pdf`

**Cor:** Vermelho

### Exemplo 4: Vídeo de Tutorial

**Arquivo:** `tutorial_python_basico.mp4`

**Detecção:**
1. Extensão: `.mp4`
2. Palavra-chave: "tutorial"

**Destino:**
`11_VIDEOS/Tutoriais/tutorial_python_basico.mp4`

**Cor:** Vermelho

### Exemplo 5: Print de Tela

**Arquivo:** `screenshot_erro_sistema.png`

**Detecção:**
1. Extensão: `.png`
2. Palavra-chave: "screenshot" ou "screen"
3. Palavra-chave: "erro"

**Destino:**
`12_PRINTS_TELA/Evidencias/screenshot_erro_sistema.png`

**Cor:** Azul

## Fluxos de Trabalho

### Fluxo 1: Organização Diária

**Rotina diária de um contador:**

```bash
# Manhã: Organizar emails da noite
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Downloads

# Tarde: Verificar documentos do Desktop
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Desktop

# Fim do dia: Gerar relatório HTML
python3 ~/.claude/skills/organize-pdfs/gerar_html_completo.py
open ~/Desktop/SISTEMA_ENSIDE_COMPLETO.html
```

### Fluxo 2: Fechamento Mensal

**Preparação para fechamento contábil:**

```bash
# 1. Organizar todos os documentos do mês
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Downloads
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Desktop

# 2. Verificar estrutura no HTML
python3 ~/.claude/skills/organize-pdfs/gerar_html_completo.py
open ~/Desktop/SISTEMA_ENSIDE_COMPLETO.html

# 3. Fazer backup do mês
cp -r /Users/Shared/ENSIDE_ORGANIZADO/06_FINANCEIRO/2025/11_Novembro \
   /Users/Shared/ENSIDE_ORGANIZADO/10_BACKUP/Mensal/2025/11_Novembro_$(date +%Y%m%d)
```

### Fluxo 3: Auditoria de Documentos

**Preparar documentos para auditoria:**

```bash
# 1. Gerar HTML com todos os documentos
python3 ~/.claude/skills/organize-pdfs/gerar_html_completo.py

# 2. Filtrar categoria específica (ex: Bancos)
# Abrir HTML e usar filtro "Bancos"

# 3. Exportar lista de arquivos
find /Users/Shared/ENSIDE_ORGANIZADO/05_BANCOS -type f -name "*.pdf" > lista_documentos_bancarios.txt
```

## Integração com Outros Sistemas

### Exemplo 1: Automator do macOS

Criar ação de "Serviço Rápido":

```applescript
on run {input, parameters}
    set thePath to POSIX path of input
    do shell script "python3 ~/.claude/skills/organize-pdfs/importador_universal.py " & quoted form of thePath
    return input
end run
```

**Uso:** Clique direito em arquivo/pasta → Serviços → Organizar no ENSIDE

### Exemplo 2: Script de Backup Automático

```bash
#!/bin/bash
# backup_diario.sh

# Organizar Downloads
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Downloads

# Fazer backup
BACKUP_DIR="/Users/Shared/ENSIDE_ORGANIZADO/10_BACKUP/Diario/$(date +%Y%m%d)"
mkdir -p "$BACKUP_DIR"

# Copiar categorias importantes
cp -r /Users/Shared/ENSIDE_ORGANIZADO/06_FINANCEIRO "$BACKUP_DIR/"
cp -r /Users/Shared/ENSIDE_ORGANIZADO/05_BANCOS "$BACKUP_DIR/"

# Gerar HTML
python3 ~/.claude/skills/organize-pdfs/gerar_html_completo.py

echo "Backup concluído: $BACKUP_DIR"
```

**Agendar com cron:**
```bash
# Editar crontab
crontab -e

# Executar todo dia às 18h
0 18 * * * /Users/andersonenside/backup_diario.sh
```

### Exemplo 3: Integração com Hazel

Criar regra no Hazel para pasta Downloads:

**Condições:**
- Se o arquivo termina com `.pdf`
- Se o arquivo foi adicionado

**Ações:**
- Executar script: `python3 ~/.claude/skills/organize-pdfs/importador_universal.py "$1"`

**Resultado:** PDFs são organizados automaticamente ao serem baixados.

## Casos Especiais

### Caso 1: Múltiplos Bancos no Mesmo PDF

**Arquivo:** `comparativo_bancos.pdf`

**Conteúdo:**
```
Comparativo de Taxas
- Itaú: 1.5%
- Bradesco: 1.8%
- Santander: 1.6%
```

**Ação do Sistema:**
- Detecta múltiplos bancos
- Prioriza o primeiro encontrado
- Move para: `05_BANCOS/Itau/Documentos_Gerais/`
- Sugestão: Criar cópia manual para outros bancos se necessário

### Caso 2: Documento Sem Detecção Clara

**Arquivo:** `documento_generico.pdf`

**Ação do Sistema:**
- Não identifica categoria específica
- Move para: `00_TRIAGEM_POR_PESSOA/A_Classificar/`
- Aguarda classificação manual

**Classificação Manual:**
```bash
# Mover para categoria correta
mv "/Users/Shared/ENSIDE_ORGANIZADO/00_TRIAGEM_POR_PESSOA/A_Classificar/documento_generico.pdf" \
   "/Users/Shared/ENSIDE_ORGANIZADO/02_DOCUMENTOS_EMPRESA/Contratos/"
```

### Caso 3: Arquivo Duplicado

**Cenário:** Mesmo arquivo em múltiplas pastas.

**Ação do Sistema:**
- Detecta arquivo com mesmo nome
- Adiciona sufixo: `_2`, `_3`, etc
- Exemplo: `extrato.pdf` → `extrato_2.pdf`

**Verificar Duplicatas:**
```bash
# Encontrar arquivos duplicados
find /Users/Shared/ENSIDE_ORGANIZADO -type f -name "*_2.pdf"
```

## Dicas e Truques

### Dica 1: Organização em Lote

```bash
# Organizar múltiplas pastas de uma vez
for folder in ~/Downloads ~/Desktop ~/Documents/Temporarios; do
    python3 ~/.claude/skills/organize-pdfs/importador_universal.py "$folder"
done
```

### Dica 2: Busca Rápida

```bash
# Encontrar todos os extratos do Itaú
find /Users/Shared/ENSIDE_ORGANIZADO/05_BANCOS/Itau -name "*extrato*"

# Encontrar documentos de novembro de 2025
find /Users/Shared/ENSIDE_ORGANIZADO -path "*/2025/11/*"
```

### Dica 3: Estatísticas

```bash
# Contar arquivos por categoria
for dir in /Users/Shared/ENSIDE_ORGANIZADO/*/; do
    echo "$(basename "$dir"): $(find "$dir" -type f | wc -l) arquivos"
done
```

### Dica 4: Visualização Rápida

```bash
# Abrir HTML automaticamente após organizar
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Downloads && \
python3 ~/.claude/skills/organize-pdfs/gerar_html_completo.py && \
open ~/Desktop/SISTEMA_ENSIDE_COMPLETO.html
```

## Próximos Passos

- [Voltar ao README](../README.md)
- [Ver Guia de Instalação](INSTALLATION.md)
- [Ler Documentação Completa](GUIA_COMPLETO.md)
- [FAQ](FAQ.md)
