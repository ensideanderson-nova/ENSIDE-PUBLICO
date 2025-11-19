#!/usr/bin/env python3
"""
IMPORTADOR UNIVERSAL - Importa qualquer pasta/arquivo para ENSIDE_ORGANIZADO
Analisa automaticamente e move para o local correto
"""

import sys
import os
import shutil
from pathlib import Path
from datetime import datetime
import re
import subprocess

BASE = Path("/Users/Shared/ENSIDE_ORGANIZADO")
WORKSPACE = Path.home() / "WORKSPACE"

# Estatísticas
stats = {
    'total': 0,
    'movidos': 0,
    'erros': 0,
    'por_tipo': {},
    'arquivos': []
}

class ImportadorUniversal:
    """Importa e organiza qualquer arquivo/pasta automaticamente"""

    # Mapeamento de extensões
    EXTENSOES = {
        # Documentos
        'pdf': 'pdf',
        'doc': 'documento', 'docx': 'documento', 'odt': 'documento', 'txt': 'texto',

        # Planilhas
        'xls': 'planilha', 'xlsx': 'planilha', 'ods': 'planilha', 'csv': 'planilha',

        # Apresentações
        'ppt': 'apresentacao', 'pptx': 'apresentacao', 'odp': 'apresentacao',

        # Imagens
        'jpg': 'imagem', 'jpeg': 'imagem', 'png': 'imagem', 'gif': 'imagem',
        'bmp': 'imagem', 'svg': 'imagem', 'webp': 'imagem', 'heic': 'imagem',

        # Vídeos
        'mp4': 'video', 'mov': 'video', 'avi': 'video', 'mkv': 'video',
        'wmv': 'video', 'flv': 'video', 'webm': 'video', 'm4v': 'video',

        # Áudio
        'mp3': 'audio', 'wav': 'audio', 'aac': 'audio', 'flac': 'audio',
        'm4a': 'audio', 'ogg': 'audio',

        # Código
        'py': 'codigo', 'js': 'codigo', 'html': 'codigo', 'css': 'codigo',
        'java': 'codigo', 'cpp': 'codigo', 'c': 'codigo', 'sh': 'codigo',
        'rb': 'codigo', 'go': 'codigo', 'php': 'codigo',

        # Compactados
        'zip': 'compactado', 'rar': 'compactado', '7z': 'compactado',
        'tar': 'compactado', 'gz': 'compactado', 'bz2': 'compactado',

        # Dados
        'json': 'dados', 'xml': 'dados', 'yaml': 'dados', 'yml': 'dados',
        'sql': 'dados', 'db': 'dados',

        # Logs
        'log': 'log',
    }

    # Palavras-chave para classificação
    PALAVRAS_CHAVE = {
        # Bancário
        'banco': ['extrato', 'saldo', 'banco', 'itau', 'bradesco', 'santander', 'bb', 'caixa', 'nubank'],
        'comprovante': ['comprovante', 'pix', 'ted', 'doc', 'transferencia'],
        'cartao': ['cartao', 'fatura', 'credito', 'debito'],
        'boleto': ['boleto', 'codigo de barras', 'linha digitavel'],

        # Documentos
        'cpf': ['cpf', 'cadastro de pessoa'],
        'rg': ['rg', 'identidade'],
        'cnh': ['cnh', 'carteira', 'habilitacao'],
        'contrato': ['contrato', 'acordo', 'termo'],
        'nota_fiscal': ['nota fiscal', 'nf-e', 'nfe', 'danfe'],

        # Segurança
        'fraude': ['fraude', 'golpe', 'suspeito', 'fraudulent', 'scam'],
        'hacking': ['hack', 'exploit', 'vulnerability', 'backdoor', 'rootkit', 'malware', 'inject'],
        'log_seguranca': ['attack', 'intrusion', 'failed login', 'unauthorized', 'blocked', 'suspicious ip'],

        # Outros
        'frete': ['frete', 'cte', 'transporte', 'motorista'],
        'madeira': ['madeira', 'romaneio', 'm3', 'tora', 'cubagem'],
        'cliente': ['cliente', 'cadastro cliente'],
        'fornecedor': ['fornecedor', 'supplier'],
    }

    def __init__(self, caminho):
        self.caminho = Path(caminho)

    def analisar_arquivo(self, arquivo):
        """Analisa um arquivo e determina onde deve ir"""
        arquivo = Path(arquivo)

        if not arquivo.exists():
            return None

        extensao = arquivo.suffix.lower().replace('.', '')
        nome_lower = arquivo.name.lower()
        tipo_arquivo = self.EXTENSOES.get(extensao, 'outro')

        # Análise de conteúdo (para certos tipos)
        conteudo = self._ler_conteudo(arquivo, tipo_arquivo)

        # Determinar destino
        destino = self._determinar_destino(arquivo, tipo_arquivo, nome_lower, conteudo)

        return {
            'origem': str(arquivo),
            'destino': str(destino),
            'tipo': tipo_arquivo,
            'tamanho': arquivo.stat().st_size,
            'nome': arquivo.name
        }

    def _ler_conteudo(self, arquivo, tipo):
        """Lê conteúdo do arquivo (primeiros bytes)"""
        try:
            if tipo in ['texto', 'codigo', 'log', 'dados']:
                with open(arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read(5000).lower()  # Primeiros 5KB
            elif tipo == 'pdf':
                # Tentar extrair texto do PDF
                try:
                    import PyPDF2
                    with open(arquivo, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        if len(reader.pages) > 0:
                            return reader.pages[0].extract_text().lower()[:5000]
                except:
                    pass
        except:
            pass
        return ""

    def _determinar_destino(self, arquivo, tipo, nome_lower, conteudo):
        """Determina o destino correto do arquivo"""

        # Pegar extensão
        extensao = arquivo.suffix.lower().replace('.', '')

        # Combinar nome e conteúdo para análise
        texto_completo = nome_lower + " " + conteudo

        # ═══════════════════════════════════════════════════
        # SEGURANÇA E FRAUDES (Prioridade máxima!)
        # ═══════════════════════════════════════════════════

        if any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['fraude']):
            if tipo == 'imagem' or 'screenshot' in nome_lower or 'print' in nome_lower:
                return BASE / "13_SEGURANCA_FRAUDES" / "Evidencias" / "Screenshots" / arquivo.name
            elif tipo == 'video':
                return BASE / "13_SEGURANCA_FRAUDES" / "Evidencias" / "Videos" / arquivo.name
            else:
                return BASE / "13_SEGURANCA_FRAUDES" / "Fraudes" / "Investigacao" / arquivo.name

        if any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['hacking']):
            if tipo == 'codigo':
                return BASE / "13_SEGURANCA_FRAUDES" / "Analise_Seguranca" / "Scripts_Suspeitos" / arquivo.name
            elif tipo == 'video':
                return BASE / "11_VIDEOS" / "Seguranca" / "Hackers" / arquivo.name
            elif tipo == 'log':
                return BASE / "13_SEGURANCA_FRAUDES" / "Analise_Seguranca" / "Logs" / arquivo.name
            else:
                return BASE / "13_SEGURANCA_FRAUDES" / "Hacking" / "Tentativas_Invasao" / arquivo.name

        if any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['log_seguranca']):
            return BASE / "13_SEGURANCA_FRAUDES" / "Hacking" / "Logs_Acesso" / arquivo.name

        # Cheques
        if 'cheque' in texto_completo:
            if 'estranho' in texto_completo or 'suspeito' in texto_completo or 'devolvido' in texto_completo:
                return BASE / "13_SEGURANCA_FRAUDES" / "Cheques" / "Suspeitos" / arquivo.name
            else:
                return BASE / "13_SEGURANCA_FRAUDES" / "Cheques" / "Analise" / arquivo.name

        # ═══════════════════════════════════════════════════
        # SCREENSHOTS / PRINTS
        # ═══════════════════════════════════════════════════

        if tipo == 'imagem' and ('screenshot' in nome_lower or 'screen shot' in nome_lower or
                                 'captura' in nome_lower or 'print' in nome_lower):
            if 'erro' in texto_completo or 'bug' in texto_completo:
                return BASE / "12_PRINTS_TELA" / "Erros" / arquivo.name
            elif 'comprovante' in texto_completo:
                return BASE / "12_PRINTS_TELA" / "Evidencias" / "Comprovantes" / arquivo.name
            else:
                return BASE / "12_PRINTS_TELA" / "2025" / arquivo.name

        # ═══════════════════════════════════════════════════
        # VÍDEOS
        # ═══════════════════════════════════════════════════

        if tipo == 'video':
            if any(palavra in texto_completo for palavra in ['tutorial', 'aula', 'curso']):
                return BASE / "11_VIDEOS" / "Tutoriais" / arquivo.name
            elif any(palavra in texto_completo for palavra in ['reuniao', 'meeting']):
                return BASE / "11_VIDEOS" / "Reunioes" / arquivo.name
            elif 'apresentacao' in texto_completo:
                return BASE / "11_VIDEOS" / "Apresentacoes" / arquivo.name
            else:
                return BASE / "11_VIDEOS" / "2025" / arquivo.name

        # ═══════════════════════════════════════════════════
        # PDFs E DOCUMENTOS
        # ═══════════════════════════════════════════════════

        if tipo == 'pdf' or tipo == 'documento':
            # Bancário
            if any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['banco']):
                if any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['comprovante']):
                    return BASE / "05_BANCOS" / "Comprovantes" / arquivo.name
                elif any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['cartao']):
                    return BASE / "05_BANCOS" / "Cartoes" / arquivo.name
                else:
                    return BASE / "05_BANCOS" / "Extratos" / arquivo.name

            # Boleto
            if any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['boleto']):
                ano = datetime.now().year
                mes = datetime.now().strftime('%B')
                return BASE / "06_FINANCEIRO" / str(ano) / mes / "Contas_Pagar" / arquivo.name

            # Nota Fiscal
            if any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['nota_fiscal']):
                return BASE / "07_CLIENTES" / "Notas_Fiscais" / "2025" / arquivo.name

            # Contrato
            if any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['contrato']):
                return BASE / "02_DOCUMENTOS_EMPRESA" / "Contratos_Socios" / arquivo.name

            # Frete
            if any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['frete']):
                return BASE / "04_FRETES" / "CTEs" / "2025" / arquivo.name

            # Madeira
            if any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['madeira']):
                return BASE / "03_MADEIRAS" / "Fornecedores_PR" / "Notas_Fiscais" / arquivo.name

            # Documentos pessoais
            if any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['cpf']):
                return BASE / "01_DOCUMENTOS_PESSOAIS" / "CPF" / "Copias" / arquivo.name
            elif any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['rg']):
                return BASE / "01_DOCUMENTOS_PESSOAIS" / "RG" / "Copias" / arquivo.name
            elif any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['cnh']):
                return BASE / "01_DOCUMENTOS_PESSOAIS" / "CNH" / "Atual" / arquivo.name

            # Genérico
            return BASE / "01_DOCUMENTOS_PESSOAIS" / arquivo.name

        # ═══════════════════════════════════════════════════
        # PLANILHAS
        # ═══════════════════════════════════════════════════

        if tipo == 'planilha':
            if 'financeiro' in texto_completo or 'fluxo' in texto_completo or 'conta' in texto_completo:
                return BASE / "06_FINANCEIRO" / "Relatorios" / arquivo.name
            elif any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['cliente']):
                return BASE / "07_CLIENTES" / "Cadastros" / arquivo.name
            elif any(palavra in texto_completo for palavra in self.PALAVRAS_CHAVE['fornecedor']):
                return BASE / "08_FORNECEDORES" / "Cadastros" / arquivo.name
            else:
                return BASE / "06_FINANCEIRO" / "Relatorios" / arquivo.name

        # ═══════════════════════════════════════════════════
        # CÓDIGO
        # ═══════════════════════════════════════════════════

        if tipo == 'codigo':
            if extensao == 'py':
                return WORKSPACE / "Python" / arquivo.name
            elif extensao in ['html', 'css', 'js']:
                return WORKSPACE / "HTML" / arquivo.name
            elif extensao == 'sh':
                return WORKSPACE / "Scripts" / arquivo.name
            else:
                return WORKSPACE / "Projetos" / arquivo.name

        # ═══════════════════════════════════════════════════
        # OUTROS
        # ═══════════════════════════════════════════════════

        if tipo == 'imagem':
            return WORKSPACE / "Documentos_PDF" / "Imagens" / arquivo.name
        elif tipo == 'audio':
            return WORKSPACE / "Documentos_PDF" / "Audio" / arquivo.name
        elif tipo == 'compactado':
            return WORKSPACE / "Downloads" / arquivo.name
        elif tipo == 'dados':
            return WORKSPACE / "Config" / arquivo.name
        elif tipo == 'log':
            return BASE / "13_SEGURANCA_FRAUDES" / "Analise_Seguranca" / "Logs" / arquivo.name
        else:
            return WORKSPACE / "Documentos_PDF" / arquivo.name

    def importar_arquivo(self, arquivo, dry_run=False):
        """Importa um arquivo para o sistema"""
        info = self.analisar_arquivo(arquivo)

        if not info:
            stats['erros'] += 1
            return False

        stats['total'] += 1

        # Criar pasta destino
        destino = Path(info['destino'])
        destino.parent.mkdir(parents=True, exist_ok=True)

        # Verificar se já existe
        if destino.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_base = destino.stem
            extensao = destino.suffix
            destino = destino.parent / f"{nome_base}_{timestamp}{extensao}"
            info['destino'] = str(destino)

        try:
            if dry_run:
                print(f"   [DRY RUN] {arquivo.name} → {destino.parent.name}/")
            else:
                shutil.move(str(arquivo), str(destino))
                print(f"   ✓ {info['tipo']}: {arquivo.name} → {destino.parent.name}/")

            stats['movidos'] += 1

            # Contabilizar por tipo
            tipo = info['tipo']
            stats['por_tipo'][tipo] = stats['por_tipo'].get(tipo, 0) + 1
            stats['arquivos'].append(info)

            return True

        except Exception as e:
            print(f"   ✗ Erro: {arquivo.name} - {e}")
            stats['erros'] += 1
            return False

    def importar(self, dry_run=False):
        """Importa arquivo ou pasta"""
        if not self.caminho.exists():
            print(f"❌ Caminho não encontrado: {self.caminho}")
            return False

        if self.caminho.is_file():
            # Importar um arquivo
            print(f"\n📄 Importando arquivo: {self.caminho.name}")
            self.importar_arquivo(self.caminho, dry_run)

        elif self.caminho.is_dir():
            # Importar pasta inteira
            print(f"\n📁 Importando pasta: {self.caminho.name}")
            print(f"   Escaneando arquivos...")

            arquivos = list(self.caminho.rglob('*'))
            arquivos = [a for a in arquivos if a.is_file() and not a.name.startswith('.')]

            print(f"   Encontrados {len(arquivos)} arquivos")
            print()

            for arquivo in arquivos:
                self.importar_arquivo(arquivo, dry_run)

        return True


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='🚀 IMPORTADOR UNIVERSAL - Importa qualquer arquivo/pasta para ENSIDE_ORGANIZADO',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Importar uma pasta
  %(prog)s ~/Downloads

  # Importar um arquivo
  %(prog)s arquivo.pdf

  # Simular (não mover)
  %(prog)s ~/Downloads --dry-run
        """
    )

    parser.add_argument('caminho', help='Arquivo ou pasta para importar')
    parser.add_argument('--dry-run', action='store_true', help='Simular sem mover arquivos')

    args = parser.parse_args()

    print("╔═══════════════════════════════════════════════════╗")
    print("║   🚀 IMPORTADOR UNIVERSAL - ENSIDE                ║")
    print("╚═══════════════════════════════════════════════════╝")

    importador = ImportadorUniversal(args.caminho)
    importador.importar(dry_run=args.dry_run)

    # Resumo
    print("\n╔═══════════════════════════════════════════════════╗")
    print("║          📊 RESUMO DA IMPORTAÇÃO                  ║")
    print("╚═══════════════════════════════════════════════════╝")
    print(f"\n   Total de arquivos: {stats['total']}")
    print(f"   ✅ Movidos: {stats['movidos']}")
    print(f"   ❌ Erros: {stats['erros']}")

    if stats['por_tipo']:
        print(f"\n   📂 Por tipo:")
        for tipo, count in sorted(stats['por_tipo'].items(), key=lambda x: x[1], reverse=True):
            print(f"      • {tipo}: {count}")

    print()

if __name__ == "__main__":
    main()
