# Guia de Instalação - Sistema ENSIDE

## Requisitos do Sistema

### Sistema Operacional
- macOS 10.15 (Catalina) ou superior
- Acesso de administrador (sudo)

### Software Necessário
- Python 3.8 ou superior
- pip3 (gerenciador de pacotes Python)
- Git (opcional, para clonar o repositório)

### Espaço em Disco
- Mínimo: 100 MB para o sistema
- Recomendado: 10 GB+ para documentos organizados

## Verificação de Requisitos

```bash
# Verificar versão do Python
python3 --version

# Verificar pip3
pip3 --version

# Verificar Git (opcional)
git --version
```

## Instalação Passo a Passo

### 1. Clonar o Repositório

```bash
# Navegar para a pasta desejada
cd ~/Documents

# Clonar o repositório
git clone https://github.com/ensideanderson-nova/ENSIDE-PUBLICO.git

# Entrar na pasta
cd ENSIDE-PUBLICO
```

### 2. Instalar Dependências Python

```bash
# Instalar bibliotecas necessárias
pip3 install -r requirements.txt
```

Bibliotecas instaladas:
- `PyPDF2`: Leitura e processamento de PDFs
- `python-magic-bin`: Detecção de tipos de arquivo

### 3. Executar Script de Instalação

```bash
# Tornar o script executável
chmod +x install.sh

# Executar instalação
bash install.sh
```

O script irá:
1. Criar a estrutura em `/Users/Shared/ENSIDE_ORGANIZADO/`
2. Instalar a skill do Claude Code em `~/.claude/skills/organize-pdfs/`
3. Criar workspace em `~/WORKSPACE/`
4. Aplicar cores no Finder
5. Gerar HTML de visualização
6. Criar atalho no Desktop

### 4. Verificar Instalação

```bash
# Verificar estrutura principal
ls -la /Users/Shared/ENSIDE_ORGANIZADO/

# Verificar skill
ls -la ~/.claude/skills/organize-pdfs/

# Verificar workspace
ls -la ~/WORKSPACE/

# Verificar atalhos
ls -la ~/Desktop/IMPORTAR_AQUI.command
ls -la ~/Desktop/SISTEMA_ENSIDE_COMPLETO.html
```

## Instalação Manual

Se preferir instalar manualmente:

### 1. Criar Estrutura Principal

```bash
# Criar diretório principal
sudo mkdir -p /Users/Shared/ENSIDE_ORGANIZADO

# Ajustar permissões
sudo chown -R $USER:staff /Users/Shared/ENSIDE_ORGANIZADO

# Executar script de criação
bash scripts/organize_master.sh
```

### 2. Instalar Skill do Claude Code

```bash
# Criar diretório da skill
mkdir -p ~/.claude/skills/organize-pdfs

# Copiar arquivos
cp scripts/*.py ~/.claude/skills/organize-pdfs/
cp scripts/*.sh ~/.claude/skills/organize-pdfs/
cp docs/SKILL.md ~/.claude/skills/organize-pdfs/

# Tornar scripts executáveis
chmod +x ~/.claude/skills/organize-pdfs/*.sh
chmod +x ~/.claude/skills/organize-pdfs/*.py
```

### 3. Criar Workspace

```bash
# Criar estrutura do workspace
mkdir -p ~/WORKSPACE/{Scripts,Python,HTML,Projetos,Config,Documentos_PDF}
```

### 4. Aplicar Cores

```bash
# Executar script de cores
bash ~/.claude/skills/organize-pdfs/aplicar_cores_completo.sh
```

### 5. Gerar HTML

```bash
# Gerar visualização HTML
python3 ~/.claude/skills/organize-pdfs/gerar_html_completo.py
```

### 6. Criar Atalhos

```bash
# Criar atalho de importação no Desktop
cat > ~/Desktop/IMPORTAR_AQUI.command << 'EOF'
#!/bin/bash
echo "Arraste arquivos/pastas aqui ou digite o caminho:"
read -e PASTA
python3 ~/.claude/skills/organize-pdfs/importador_universal.py "$PASTA"
EOF

chmod +x ~/Desktop/IMPORTAR_AQUI.command
```

## Configuração do Claude Code

### 1. Verificar Instalação do Claude Code

```bash
# Verificar se Claude Code está instalado
which claude

# Se não estiver, instalar seguindo:
# https://github.com/anthropics/claude-code
```

### 2. Configurar Skill

A skill é detectada automaticamente pelo Claude Code em:
```
~/.claude/skills/organize-pdfs/SKILL.md
```

### 3. Testar Skill

Abra o Claude Code e teste:
```
Você: "Organiza a pasta Downloads"
```

O Claude deve ativar a skill automaticamente.

## Solução de Problemas

### Erro: Permissão Negada

```bash
# Ajustar permissões
sudo chown -R $USER:staff /Users/Shared/ENSIDE_ORGANIZADO
chmod -R 755 /Users/Shared/ENSIDE_ORGANIZADO
```

### Erro: Python não encontrado

```bash
# Instalar Python via Homebrew
brew install python3

# Ou baixar de: https://www.python.org/downloads/
```

### Erro: pip3 não encontrado

```bash
# Instalar pip3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### Erro: Biblioteca não instalada

```bash
# Reinstalar dependências
pip3 install --upgrade -r requirements.txt
```

### Erro: Cores não aplicadas

```bash
# Reinstalar tag (utilitário de cores)
brew install tag

# Ou baixar de: https://github.com/jdberry/tag
```

### Skill não ativa no Claude Code

```bash
# Verificar localização da skill
ls -la ~/.claude/skills/organize-pdfs/SKILL.md

# Reiniciar Claude Code
# Fechar e reabrir o terminal
```

## Atualização

### Atualizar via Git

```bash
cd ~/Documents/ENSIDE-PUBLICO
git pull origin main
bash install.sh
```

### Atualizar Manualmente

```bash
# Fazer backup da configuração atual
cp -r ~/.claude/skills/organize-pdfs ~/.claude/skills/organize-pdfs.backup

# Copiar novos arquivos
cp scripts/*.py ~/.claude/skills/organize-pdfs/
cp scripts/*.sh ~/.claude/skills/organize-pdfs/

# Tornar executáveis
chmod +x ~/.claude/skills/organize-pdfs/*.{py,sh}
```

## Desinstalação

### Desinstalação Completa

```bash
# Remover estrutura principal (CUIDADO: apaga todos os documentos!)
sudo rm -rf /Users/Shared/ENSIDE_ORGANIZADO

# Remover skill
rm -rf ~/.claude/skills/organize-pdfs

# Remover workspace (CUIDADO: apaga arquivos!)
rm -rf ~/WORKSPACE

# Remover atalhos
rm ~/Desktop/IMPORTAR_AQUI.command
rm ~/Desktop/SISTEMA_ENSIDE_COMPLETO.html
```

### Desinstalação Parcial (manter documentos)

```bash
# Remover apenas skill
rm -rf ~/.claude/skills/organize-pdfs

# Remover apenas atalhos
rm ~/Desktop/IMPORTAR_AQUI.command
rm ~/Desktop/SISTEMA_ENSIDE_COMPLETO.html
```

## Próximos Passos

Após a instalação:

1. [Ler o Guia Completo](GUIA_COMPLETO.md)
2. [Ver Exemplos de Uso](EXEMPLOS.md)
3. [Testar o Importador](../README.md#como-usar)
4. [Visualizar o HTML](../README.md#visualização-html)

## Suporte

Problemas na instalação?
- Issues: https://github.com/ensideanderson-nova/ENSIDE-PUBLICO/issues
- Email: suporte@enside.com.br
