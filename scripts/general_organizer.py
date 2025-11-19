#!/usr/bin/env python3
"""
General File Organizer - Organiza qualquer tipo de arquivo
Parte da skill organize-pdfs do Claude Code
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import mimetypes
import re


class GeneralOrganizer:
    """Organizador geral de arquivos (não só PDFs)"""

    BASE_PATH = Path("/Users/Shared/ENSIDE_ORGANIZADO")
    WORKSPACE = Path.home() / "WORKSPACE"

    # Mapeamento de extensões para categorias
    EXTENSOES = {
        # Documentos
        'documentos': ['.pdf', '.doc', '.docx', '.odt', '.txt', '.rtf'],
        'planilhas': ['.xls', '.xlsx', '.ods', '.csv'],
        'apresentacoes': ['.ppt', '.pptx', '.odp'],

        # Imagens
        'imagens': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.heic'],

        # Videos
        'videos': ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm'],

        # Audio
        'audio': ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.ogg'],

        # Código
        'codigo': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.sh', '.rb', '.go'],

        # Compactados
        'compactados': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],

        # Dados
        'dados': ['.json', '.xml', '.yaml', '.yml', '.sql', '.db'],
    }

    # Palavras-chave para classificação
    PALAVRAS_CHAVE = {
        'contrato': ['contrato', 'acordo', 'termo'],
        'nota_fiscal': ['nota fiscal', 'nf-e', 'nfe', 'danfe'],
        'extrato': ['extrato', 'saldo', 'movimentação'],
        'comprovante': ['comprovante', 'recibo', 'pagamento'],
        'fatura': ['fatura', 'boleto'],
        'relatorio': ['relatório', 'relatorio', 'report'],
    }

    def __init__(self, arquivo_path: str, destino_sugerido: Optional[str] = None):
        """
        Inicializa o organizador

        Args:
            arquivo_path: Caminho do arquivo
            destino_sugerido: Categoria de destino sugerida
        """
        self.arquivo = Path(arquivo_path)
        self.destino_sugerido = destino_sugerido
        self.extensao = self.arquivo.suffix.lower()
        self.nome = self.arquivo.stem
        self.info = self._analisar_arquivo()

    def _analisar_arquivo(self) -> Dict:
        """Analisa o arquivo e extrai informações"""
        return {
            'nome': self.arquivo.name,
            'nome_sem_ext': self.nome,
            'extensao': self.extensao,
            'tamanho_kb': self.arquivo.stat().st_size / 1024 if self.arquivo.exists() else 0,
            'data_modificacao': datetime.fromtimestamp(self.arquivo.stat().st_mtime).strftime('%Y-%m-%d') if self.arquivo.exists() else None,
            'categoria': self._identificar_categoria(),
            'tipo': self._identificar_tipo(),
        }

    def _identificar_categoria(self) -> str:
        """Identifica a categoria do arquivo pela extensão"""
        for categoria, extensoes in self.EXTENSOES.items():
            if self.extensao in extensoes:
                return categoria
        return 'outros'

    def _identificar_tipo(self) -> Optional[str]:
        """Identifica o tipo baseado no nome do arquivo"""
        nome_lower = self.nome.lower()

        for tipo, palavras in self.PALAVRAS_CHAVE.items():
            for palavra in palavras:
                if palavra in nome_lower:
                    return tipo

        return None

    def determinar_destino(self) -> Path:
        """Determina o melhor destino para o arquivo"""

        # Se tem destino sugerido, usa ele
        if self.destino_sugerido:
            return self.BASE_PATH / self.destino_sugerido

        categoria = self.info['categoria']
        tipo = self.info['tipo']

        # PDFs podem ir para vários lugares
        if self.extensao == '.pdf':
            if tipo == 'nota_fiscal':
                return self.BASE_PATH / "07_CLIENTES" / "Notas_Fiscais" / str(datetime.now().year)
            elif tipo == 'extrato':
                return self.BASE_PATH / "05_BANCOS" / "Extratos"
            elif tipo == 'comprovante':
                return self.BASE_PATH / "05_BANCOS" / "Comprovantes"
            elif tipo == 'contrato':
                return self.BASE_PATH / "02_DOCUMENTOS_EMPRESA" / "Contratos"
            else:
                return self.BASE_PATH / "01_DOCUMENTOS_PESSOAIS"

        # Planilhas
        elif categoria == 'planilhas':
            if 'financeiro' in self.nome.lower() or 'fluxo' in self.nome.lower():
                return self.BASE_PATH / "06_FINANCEIRO" / "Relatorios"
            elif 'cliente' in self.nome.lower():
                return self.BASE_PATH / "07_CLIENTES" / "Cadastros"
            elif 'fornecedor' in self.nome.lower():
                return self.BASE_PATH / "08_FORNECEDORES" / "Cadastros"
            else:
                return self.WORKSPACE / "Documentos_PDF"

        # Imagens
        elif categoria == 'imagens':
            if 'logo' in self.nome.lower() or 'banner' in self.nome.lower():
                return self.WORKSPACE / "Projetos" / "Assets"
            else:
                return self.WORKSPACE / "Documentos_PDF" / "Imagens"

        # Código
        elif categoria == 'codigo':
            if self.extensao == '.py':
                return self.WORKSPACE / "Python"
            elif self.extensao in ['.html', '.css', '.js']:
                return self.WORKSPACE / "HTML"
            elif self.extensao == '.sh':
                return self.WORKSPACE / "Scripts"
            else:
                return self.WORKSPACE / "Projetos"

        # Dados/Config
        elif categoria == 'dados':
            if self.extensao in ['.json', '.yaml', '.yml']:
                return self.WORKSPACE / "Config"
            else:
                return self.WORKSPACE / "Projetos"

        # Compactados
        elif categoria == 'compactados':
            return self.WORKSPACE / "Downloads"

        # Outros
        else:
            return self.WORKSPACE / "Documentos_PDF"

    def organizar(self, dry_run: bool = False) -> Dict:
        """
        Organiza o arquivo movendo para o destino correto

        Args:
            dry_run: Se True, apenas simula sem mover

        Returns:
            Dict com resultado da operação
        """
        if not self.arquivo.exists():
            return {
                'sucesso': False,
                'erro': f'Arquivo não encontrado: {self.arquivo}'
            }

        destino_pasta = self.determinar_destino()

        # Criar pasta se não existir
        if not dry_run:
            destino_pasta.mkdir(parents=True, exist_ok=True)

        # Nome do arquivo no destino
        arquivo_destino = destino_pasta / self.arquivo.name

        # Se já existe, adicionar timestamp
        if arquivo_destino.exists():
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            arquivo_destino = destino_pasta / f"{self.nome}_{timestamp}{self.extensao}"

        resultado = {
            'sucesso': False,
            'origem': str(self.arquivo),
            'destino': str(arquivo_destino),
            'categoria': self.info['categoria'],
            'tipo': self.info['tipo'],
            'dry_run': dry_run
        }

        try:
            if dry_run:
                print(f"[DRY RUN] {self.arquivo} → {arquivo_destino}")
                resultado['sucesso'] = True
                resultado['mensagem'] = 'Simulação OK'
            else:
                shutil.move(str(self.arquivo), str(arquivo_destino))
                print(f"✓ Movido: {self.arquivo.name} → {destino_pasta}")
                resultado['sucesso'] = True
                resultado['mensagem'] = 'Arquivo movido com sucesso'

        except Exception as e:
            resultado['erro'] = str(e)
            print(f"✗ Erro: {e}")

        return resultado


def organizar_pasta(pasta: str, dry_run: bool = False) -> Dict:
    """
    Organiza todos os arquivos de uma pasta

    Args:
        pasta: Caminho da pasta
        dry_run: Se True, apenas simula

    Returns:
        Dict com estatísticas
    """
    pasta_path = Path(pasta)

    if not pasta_path.exists() or not pasta_path.is_dir():
        return {
            'erro': f'Pasta não encontrada: {pasta}'
        }

    estatisticas = {
        'total': 0,
        'sucesso': 0,
        'erros': 0,
        'por_categoria': {},
        'arquivos': []
    }

    # Listar todos os arquivos
    for arquivo in pasta_path.iterdir():
        if arquivo.is_file() and not arquivo.name.startswith('.'):
            estatisticas['total'] += 1

            organizer = GeneralOrganizer(str(arquivo))
            resultado = organizer.organizar(dry_run=dry_run)

            if resultado['sucesso']:
                estatisticas['sucesso'] += 1

                categoria = resultado['categoria']
                if categoria not in estatisticas['por_categoria']:
                    estatisticas['por_categoria'][categoria] = 0
                estatisticas['por_categoria'][categoria] += 1
            else:
                estatisticas['erros'] += 1

            estatisticas['arquivos'].append(resultado)

    return estatisticas


def main():
    """Função principal"""
    import json
    import argparse

    parser = argparse.ArgumentParser(description='Organiza arquivos automaticamente')
    parser.add_argument('caminho', help='Arquivo ou pasta para organizar')
    parser.add_argument('--dry-run', action='store_true', help='Apenas simular, não mover arquivos')
    parser.add_argument('--destino', help='Categoria de destino sugerida')

    args = parser.parse_args()

    caminho = Path(args.caminho)

    if caminho.is_file():
        # Organizar um arquivo
        organizer = GeneralOrganizer(str(caminho), args.destino)
        resultado = organizer.organizar(dry_run=args.dry_run)
        print(json.dumps(resultado, indent=2, ensure_ascii=False))

    elif caminho.is_dir():
        # Organizar uma pasta
        print(f"\n📁 Organizando pasta: {caminho}")
        print(f"{'[DRY RUN]' if args.dry_run else ''}\n")

        estatisticas = organizar_pasta(str(caminho), dry_run=args.dry_run)

        print(f"\n📊 Estatísticas:")
        print(f"  Total de arquivos: {estatisticas['total']}")
        print(f"  Sucesso: {estatisticas['sucesso']}")
        print(f"  Erros: {estatisticas['erros']}")
        print(f"\n📂 Por categoria:")
        for cat, count in estatisticas['por_categoria'].items():
            print(f"  {cat}: {count} arquivos")

        print(json.dumps(estatisticas, indent=2, ensure_ascii=False))

    else:
        print(f"Erro: Caminho não encontrado: {caminho}")
        sys.exit(1)


if __name__ == "__main__":
    main()
