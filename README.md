# Sistema ENSIDE - Organização Inteligente de Documentos

Sistema completo de organização automática de arquivos e documentos empresariais com detecção inteligente, categorização por cores e interface HTML interativa.

## Visão Geral

O Sistema ENSIDE organiza automaticamente seus documentos em 14 categorias principais, com detecção inteligente de conteúdo, aplicação de cores no Finder do macOS e visualização HTML interativa.

### Principais Características

- **733 pastas** estruturadas e organizadas
- **14 categorias** principais com códigos de cores
- **Detecção inteligente** de tipos de documento (PDFs, extratos bancários, notas fiscais, etc)
- **6 bancos** organizados (Itaú, Bradesco, Santander, BB, Caixa, Nubank)
- **Sistema de cores** no Finder do macOS
- **HTML interativo** com filtros e busca em tempo real
- **Integração com Claude Code** via skill personalizada

## Estrutura de Categorias

| # | Categoria | Cor | Descrição |
|---|-----------|-----|-----------|
| 00 | TRIAGEM_POR_PESSOA | Roxo | Organização por CPF ou CNPJ |
| 01 | DOCUMENTOS_PESSOAIS | Verde | RG, CPF, CNH, Certidões |
| 02 | DOCUMENTOS_EMPRESA | Azul | CNPJ, Contratos, Alvarás |
| 03 | MADEIRAS | Roxo | Fornecedores, Estoque, Certificados |
| 04 | FRETES | Laranja | Motoristas, CTe, Cotações |
| 05 | BANCOS | Vermelho | 6 Bancos com CPF/CNPJ separados |
| 06 | FINANCEIRO | Amarelo | Contas, Impostos (12 meses) |
| 07 | CLIENTES | Rosa | Cadastros, Contratos, Notas Fiscais |
| 08 | FORNECEDORES | Cinza | Cadastros, Contratos, Pedidos |
| 09 | SISTEMAS | Roxo | Código-fonte, Scripts, Projetos |
| 10 | BACKUP | Cinza | Backups Diários/Semanais/Mensais |
| 11 | VIDEOS | Vermelho | Tutoriais, Segurança, Reuniões |
| 12 | PRINTS_TELA | Azul | Screenshots, Evidências |
| 13 | SEGURANCA_FRAUDES | Vermelho | Fraudes, Cheques Suspeitos |

## Instalação Rápida

```bash
# Clonar o repositório
git clone https://github.com/ensideanderson-nova/ENSIDE-PUBLICO.git

# Executar instalação
cd ENSIDE-PUBLICO
bash install.sh
```

## Como Usar

### Opção 1: Linha de Comando

```bash
# Organizar pasta Downloads
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Downloads

# Organizar arquivo específico
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Desktop/documento.pdf

# Modo simulação (não move arquivos)
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Downloads --dry-run
```

### Opção 2: Claude Code (Recomendado)

Simplesmente peça ao Claude:
- "Organiza os arquivos da pasta Downloads"
- "Importa esta pasta para o sistema"
- "Classifica estes documentos"

### Opção 3: Atalho Desktop

1. Clique 2x em `IMPORTAR_AQUI.command` no Desktop
2. Arraste arquivos ou pastas
3. Sistema organiza automaticamente

## Detecção Inteligente

O sistema reconhece automaticamente:

### Documentos Bancários
- Extratos bancários → `05_BANCOS/[Banco]/Extratos/`
- Comprovantes → `05_BANCOS/[Banco]/Comprovantes/`
- Detecta 6 bancos principais automaticamente

### Documentos Fiscais
- Notas Fiscais → `07_CLIENTES/` ou `08_FORNECEDORES/`
- Boletos → `06_FINANCEIRO/Contas_Pagar/`
- Contratos → `02_DOCUMENTOS_EMPRESA/Contratos/`

### Segurança e Fraudes
Palavras-chave detectadas:
- fraude, fraud, golpe, scam
- phishing, malware, virus
- cheque suspeito, tentativa invasão

Destino: `13_SEGURANCA_FRAUDES/`

### Mídia
- Vídeos (.mp4, .mov, .avi) → `11_VIDEOS/`
- Prints (.png, .jpg com "screen") → `12_PRINTS_TELA/`
- Documentação e evidências separadas

### Código-fonte
- Python (.py) → `WORKSPACE/Python/`
- HTML/CSS/JS → `WORKSPACE/HTML/`
- Scripts (.sh) → `WORKSPACE/Scripts/`

## Visualização HTML

Gere um mapa visual completo do sistema:

```bash
python3 ~/.claude/skills/organize-pdfs/gerar_html_completo.py
```

### Funcionalidades do HTML
- Mapa visual de toda estrutura
- Cores correspondentes ao Finder
- 11 botões de filtro por categoria
- Busca em tempo real
- Estatísticas do sistema
- Links diretos para pastas

Arquivo gerado: `~/Desktop/SISTEMA_ENSIDE_COMPLETO.html`

## Sistema de Cores

Aplicar cores no Finder do macOS:

```bash
bash ~/.claude/skills/organize-pdfs/aplicar_cores_completo.sh
```

### Paleta de Cores
- Roxo: Triagem, Madeiras, Sistemas
- Verde: Documentos Pessoais (CPF)
- Azul: Documentos Empresa (CNPJ), Prints
- Vermelho: Bancos, Vídeos, Segurança
- Laranja: Fretes
- Amarelo: Financeiro
- Rosa: Clientes
- Cinza: Fornecedores, Backup

## Scripts Disponíveis

### Organização
```bash
# Recriar sistema completo
bash ~/.claude/skills/organize-pdfs/organize_master.sh

# Organizar HOME completa
bash ~/.claude/skills/organize-pdfs/organizar_home_completo.sh

# Criar novas categorias
bash ~/.claude/skills/organize-pdfs/criar_categorias_novas.sh
```

### Importação
```bash
# Importador universal (recomendado)
python3 ~/.claude/skills/organize-pdfs/importador_universal.py [PASTA]

# Organizador geral
python3 ~/.claude/skills/organize-pdfs/general_organizer.py [PASTA]

# Processador específico de PDFs
python3 ~/.claude/skills/organize-pdfs/pdf_processor.py [ARQUIVO]
```

### Visualização
```bash
# HTML completo com cores
python3 ~/.claude/skills/organize-pdfs/gerar_html_completo.py

# HTML simples
python3 ~/.claude/skills/organize-pdfs/gerar_html_cores.py
```

## Estrutura de Arquivos

```
/Users/Shared/ENSIDE_ORGANIZADO/     # Sistema principal
~/WORKSPACE/                          # Arquivos pessoais
~/.claude/skills/organize-pdfs/       # Scripts e skill
~/Desktop/SISTEMA_ENSIDE_COMPLETO.html # Visualização HTML
```

## Exemplo: Estrutura de Bancos

```
05_BANCOS/
├── Itau/
│   ├── CPF/                         # Verde
│   │   ├── Conta_Corrente/
│   │   ├── Extratos/2025/
│   │   ├── Cartoes/
│   │   └── Comprovantes/
│   └── CNPJ/                        # Azul
│       ├── Conta_Corrente/
│       ├── Extratos/2025/
│       └── Comprovantes/
├── Bradesco/
├── Santander/
├── Banco_do_Brasil/
├── Caixa/
└── Nubank/
```

## Requisitos

- macOS 10.15 ou superior
- Python 3.8+
- Claude Code (opcional, mas recomendado)
- Bibliotecas Python: PyPDF2, python-magic-bin

```bash
pip3 install -r requirements.txt
```

## Documentação Completa

- [Guia de Instalação](docs/INSTALLATION.md)
- [Guia Completo de Uso](docs/GUIA_COMPLETO.md)
- [Exemplos e Casos de Uso](docs/EXEMPLOS.md)
- [Desenvolvimento e Customização](docs/DEVELOPMENT.md)
- [FAQ](docs/FAQ.md)

## Estatísticas

- 733 pastas criadas automaticamente
- 14 categorias principais
- 6 bancos com CPF/CNPJ separados
- 12 meses organizados (Financeiro 2025)
- 3 níveis de backup (Diário/Semanal/Mensal)

## Integração com Claude Code

O sistema inclui uma skill personalizada para Claude Code que permite organização automática através de comandos naturais.

### Ativação
A skill é ativada automaticamente quando você pede ao Claude para organizar arquivos.

### Comandos Exemplo
- "Organiza a pasta Downloads"
- "Classifica os documentos do Desktop"
- "Importa estes arquivos para o sistema"

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Suporte

- Issues: https://github.com/ensideanderson-nova/ENSIDE-PUBLICO/issues
- Email: suporte@enside.com.br
- Documentação: https://github.com/ensideanderson-nova/ENSIDE-PUBLICO/wiki

## Roadmap

- [ ] Suporte para Windows e Linux
- [ ] Interface gráfica nativa
- [ ] OCR automático em PDFs
- [ ] Integração com serviços de nuvem
- [ ] App mobile para visualização
- [ ] API REST para integração

## Créditos

Desenvolvido por Anderson Enside
Powered by Claude AI (Anthropic)

---

**Sistema pronto para uso!**

Comece organizando sua pasta Downloads:
```bash
python3 ~/.claude/skills/organize-pdfs/importador_universal.py ~/Downloads
```
