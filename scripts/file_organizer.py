#!/usr/bin/env python3
"""
File Organizer - Move arquivos PDFs para a estrutura ENSIDE_ORGANIZADO
Parte da skill organize-pdfs do Claude Code
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import re


class FileOrganizer:
    """Organiza arquivos PDF na estrutura ENSIDE_ORGANIZADO"""

    # Caminho base do sistema
    BASE_PATH = Path("/Users/Shared/ENSIDE_ORGANIZADO")

    # Mapeamento de bancos
    BANCOS_MAP = {
        'itau': 'Itau',
        'bradesco': 'Bradesco',
        'santander': 'Santander',
        'bb': 'Banco_do_Brasil',
        'caixa': 'Caixa',
        'nubank': 'Nubank',
        'inter': 'Inter',
        'sicoob': 'Sicoob',
        'sicredi': 'Sicredi',
        'safra': 'Safra'
    }

    def __init__(self, pdf_info: Dict, dry_run: bool = False):
        """
        Inicializa o organizador

        Args:
            pdf_info: Informações extraídas do PDF
            dry_run: Se True, apenas simula sem mover arquivos
        """
        self.pdf_info = pdf_info
        self.dry_run = dry_run
        self.arquivo_origem = Path(pdf_info['arquivo'])
        self.destinos = []
        self.log = []

    def determinar_destinos(self) -> list:
        """Determina para quais pastas o arquivo deve ir"""
        destinos = []

        # 1. TRIAGEM POR PESSOA (00_TRIAGEM_POR_PESSOA)
        if self.pdf_info.get('cpfs'):
            for cpf in self.pdf_info['cpfs']:
                destino_cpf = self._destino_triagem_cpf(cpf)
                if destino_cpf:
                    destinos.append(destino_cpf)

        if self.pdf_info.get('cnpjs'):
            for cnpj in self.pdf_info['cnpjs']:
                destino_cnpj = self._destino_triagem_cnpj(cnpj)
                if destino_cnpj:
                    destinos.append(destino_cnpj)

        # 2. BANCOS (05_BANCOS)
        if self.pdf_info.get('banco'):
            destino_banco = self._destino_banco()
            if destino_banco:
                destinos.append(destino_banco)

        # 3. FINANCEIRO (06_FINANCEIRO)
        if self._e_documento_financeiro():
            destino_financeiro = self._destino_financeiro()
            if destino_financeiro:
                destinos.append(destino_financeiro)

        # 4. FRETES (04_FRETES)
        if self.pdf_info.get('tipo_documento') == 'frete':
            destinos.append(self.BASE_PATH / "04_FRETES" / "Documentos")

        # 5. MADEIRAS (03_MADEIRAS)
        if self.pdf_info.get('tipo_documento') == 'romaneio':
            destinos.append(self.BASE_PATH / "03_MADEIRAS" / "Romaneios")

        # 6. CLIENTES (07_CLIENTES)
        if self.pdf_info.get('tipo_documento') == 'nota_fiscal' and self._e_cnpj():
            destinos.append(self.BASE_PATH / "07_CLIENTES" / "Notas_Fiscais")

        # 7. FORNECEDORES (08_FORNECEDORES)
        if self.pdf_info.get('tipo_documento') == 'nota_fiscal' and self._e_entrada():
            destinos.append(self.BASE_PATH / "08_FORNECEDORES" / "Notas_Fiscais")

        self.destinos = list(set(str(d) for d in destinos))  # Remove duplicatas
        return self.destinos

    def _destino_triagem_cpf(self, cpf: str) -> Optional[Path]:
        """Determina destino na triagem por CPF"""
        # Aqui você pode mapear CPFs conhecidos
        # Por enquanto, vou para CPF_ANDERSON como padrão
        base = self.BASE_PATH / "00_TRIAGEM_POR_PESSOA" / "CPF_ANDERSON"

        tipo = self.pdf_info.get('tipo_documento')

        if tipo == 'extrato' or tipo == 'comprovante' or tipo == 'cartao':
            return base / "Bancos"
        elif tipo == 'contrato':
            return base / "Documentos_Pessoais"
        elif tipo == 'boleto':
            return base / "Financeiro" / "Contas_Pagar"
        elif tipo == 'nota_fiscal':
            return base / "Financeiro" / "Receitas"
        else:
            return base / "Documentos_Pessoais"

    def _destino_triagem_cnpj(self, cnpj: str) -> Optional[Path]:
        """Determina destino na triagem por CNPJ"""
        base = self.BASE_PATH / "00_TRIAGEM_POR_PESSOA" / "CNPJ_EMPRESA_ENSIDE"

        tipo = self.pdf_info.get('tipo_documento')

        if tipo == 'extrato' or tipo == 'comprovante':
            return base / "Bancos"
        elif tipo == 'nota_fiscal':
            return base / "Clientes"
        elif tipo == 'frete':
            return base / "Fretes"
        elif tipo == 'romaneio':
            return base / "Madeiras"
        else:
            return base / "Documentos_Empresa"

    def _destino_banco(self) -> Optional[Path]:
        """Determina destino na pasta de bancos"""
        banco = self.pdf_info.get('banco')
        if not banco:
            return None

        banco_nome = self.BANCOS_MAP.get(banco.lower(), banco.title())
        base = self.BASE_PATH / "05_BANCOS" / banco_nome

        # Determinar se é CPF ou CNPJ
        tipo_pessoa = "CNPJ" if self.pdf_info.get('cnpjs') else "CPF"
        base = base / tipo_pessoa

        # Determinar subpasta baseado no tipo
        tipo = self.pdf_info.get('tipo_documento')

        if tipo == 'extrato':
            # Pegar ano da data
            ano = self._extrair_ano()
            return base / "Extratos" / ano
        elif tipo == 'comprovante':
            return base / "Comprovantes" / "Transferencias"
        elif tipo == 'cartao':
            return base / "Cartoes" / "Faturas"
        elif tipo == 'boleto':
            return base / "Comprovantes" / "Boletos"
        else:
            return base / "Conta_Corrente"

    def _destino_financeiro(self) -> Optional[Path]:
        """Determina destino na pasta financeiro"""
        base = self.BASE_PATH / "06_FINANCEIRO"

        tipo = self.pdf_info.get('tipo_documento')
        ano = self._extrair_ano()
        mes = self._extrair_mes()

        if tipo == 'boleto':
            return base / ano / mes / "Contas_Pagar"
        elif tipo == 'nota_fiscal':
            return base / ano / mes / "Receitas"
        else:
            return base / ano / mes / "Despesas"

    def _e_documento_financeiro(self) -> bool:
        """Verifica se é documento financeiro"""
        tipo = self.pdf_info.get('tipo_documento')
        return tipo in ['boleto', 'recibo', 'nota_fiscal']

    def _e_cnpj(self) -> bool:
        """Verifica se tem CNPJ"""
        return bool(self.pdf_info.get('cnpjs'))

    def _e_entrada(self) -> bool:
        """Verifica se é nota de entrada (heurística)"""
        # Aqui você pode adicionar lógica mais sofisticada
        text_lower = self.pdf_info.get('texto_preview', '').lower()
        return 'entrada' in text_lower or 'compra' in text_lower

    def _extrair_ano(self) -> str:
        """Extrai ano do documento"""
        if self.pdf_info.get('datas'):
            primeira_data = self.pdf_info['datas'][0]
            if '/' in primeira_data:
                return primeira_data.split('/')[-1]
            elif '-' in primeira_data:
                return primeira_data.split('-')[0]

        # Fallback para data do arquivo
        return datetime.now().strftime('%Y')

    def _extrair_mes(self) -> str:
        """Extrai mês do documento"""
        if self.pdf_info.get('datas'):
            primeira_data = self.pdf_info['datas'][0]
            if '/' in primeira_data:
                mes_num = primeira_data.split('/')[1]
            elif '-' in primeira_data:
                mes_num = primeira_data.split('-')[1]
            else:
                mes_num = datetime.now().strftime('%m')

            meses = {
                '01': 'Janeiro', '02': 'Fevereiro', '03': 'Março',
                '04': 'Abril', '05': 'Maio', '06': 'Junho',
                '07': 'Julho', '08': 'Agosto', '09': 'Setembro',
                '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'
            }
            return meses.get(mes_num, 'Outros')

        return datetime.now().strftime('%B')

    def gerar_nome_arquivo(self) -> str:
        """Gera nome padronizado para o arquivo"""
        partes = []

        # Data
        ano = self._extrair_ano()
        mes_num = datetime.now().strftime('%m')
        dia = datetime.now().strftime('%d')
        partes.append(f"{ano}-{mes_num}-{dia}")

        # Tipo
        tipo = self.pdf_info.get('tipo_documento', 'documento')
        partes.append(tipo.title())

        # Banco
        if self.pdf_info.get('banco'):
            partes.append(self.pdf_info['banco'].title())

        # Valor (se tiver)
        if self.pdf_info.get('valores'):
            maior_valor = self.pdf_info['valores'][0]['valor']
            partes.append(f"R${maior_valor:.2f}".replace('.', ','))

        # Extensão
        nome = "_".join(partes) + ".pdf"

        # Limpar caracteres inválidos
        nome = re.sub(r'[<>:"/\\|?*]', '_', nome)

        return nome

    def mover_arquivo(self) -> Dict:
        """Move o arquivo para os destinos determinados"""
        if not self.destinos:
            self.determinar_destinos()

        resultado = {
            'sucesso': [],
            'erros': [],
            'destinos': self.destinos
        }

        novo_nome = self.gerar_nome_arquivo()

        for destino_str in self.destinos:
            destino = Path(destino_str)

            try:
                # Criar pasta se não existir
                if not self.dry_run:
                    destino.mkdir(parents=True, exist_ok=True)

                # Caminho completo do destino
                arquivo_destino = destino / novo_nome

                # Verificar se já existe
                if arquivo_destino.exists():
                    # Adicionar timestamp
                    timestamp = datetime.now().strftime('%H%M%S')
                    nome_sem_ext = arquivo_destino.stem
                    arquivo_destino = destino / f"{nome_sem_ext}_{timestamp}.pdf"

                # Mover arquivo
                if self.dry_run:
                    msg = f"[DRY RUN] {self.arquivo_origem} -> {arquivo_destino}"
                    print(msg, file=sys.stderr)
                    self.log.append(msg)
                    resultado['sucesso'].append(str(arquivo_destino))
                else:
                    shutil.copy2(self.arquivo_origem, arquivo_destino)
                    msg = f"✓ Movido para: {arquivo_destino}"
                    print(msg, file=sys.stderr)
                    self.log.append(msg)
                    resultado['sucesso'].append(str(arquivo_destino))

            except Exception as e:
                msg = f"✗ Erro ao mover para {destino}: {e}"
                print(msg, file=sys.stderr)
                self.log.append(msg)
                resultado['erros'].append({'destino': str(destino), 'erro': str(e)})

        return resultado


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python3 file_organizer.py <json_info_pdf> [--dry-run]")
        print("\nExemplo:")
        print('  python3 file_organizer.py \'{"arquivo": "doc.pdf", "banco": "itau", "tipo_documento": "extrato"}\'')
        sys.exit(1)

    json_info = sys.argv[1]
    dry_run = '--dry-run' in sys.argv

    try:
        pdf_info = json.loads(json_info)

        organizer = FileOrganizer(pdf_info, dry_run=dry_run)
        organizer.determinar_destinos()

        print(f"\n📄 Arquivo: {pdf_info.get('nome_arquivo')}", file=sys.stderr)
        print(f"📍 Destinos determinados: {len(organizer.destinos)}", file=sys.stderr)

        for i, dest in enumerate(organizer.destinos, 1):
            print(f"   {i}. {dest}", file=sys.stderr)

        print("\n🔄 Movendo arquivo...", file=sys.stderr)
        resultado = organizer.mover_arquivo()

        # Imprimir resultado como JSON
        print(json.dumps(resultado, indent=2, ensure_ascii=False))

    except json.JSONDecodeError as e:
        print(f"Erro ao parsear JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
