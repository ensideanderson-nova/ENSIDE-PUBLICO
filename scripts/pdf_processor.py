#!/usr/bin/env python3
"""
PDF Processor - Extrai texto e informações de PDFs
Parte da skill organize-pdfs do Claude Code
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

try:
    import PyPDF2
except ImportError:
    print("ERRO: PyPDF2 não instalado. Execute: pip install PyPDF2", file=sys.stderr)
    sys.exit(1)


class PDFProcessor:
    """Processa PDFs e extrai informações relevantes"""

    # Bancos brasileiros conhecidos
    BANCOS = {
        'itau': ['itau', 'itaú', 'banco itau', 'banco itaú'],
        'bradesco': ['bradesco', 'banco bradesco'],
        'santander': ['santander', 'banco santander'],
        'bb': ['banco do brasil', 'bb', 'banco brasil'],
        'caixa': ['caixa', 'caixa econômica', 'caixa economica', 'cef'],
        'nubank': ['nubank', 'nu pagamentos'],
        'inter': ['inter', 'banco inter'],
        'sicoob': ['sicoob'],
        'sicredi': ['sicredi'],
        'safra': ['safra', 'banco safra']
    }

    # Tipos de documento
    TIPOS_DOCUMENTO = {
        'extrato': ['extrato', 'saldo', 'lançamentos', 'lancamentos', 'movimentação', 'movimentacao'],
        'comprovante': ['comprovante', 'transferência', 'transferencia', 'pix', 'ted', 'doc'],
        'cartao': ['cartão', 'cartao', 'fatura', 'crédito', 'credito', 'débito', 'debito'],
        'contrato': ['contrato', 'partes', 'cláusula', 'clausula', 'contratante', 'contratado'],
        'nota_fiscal': ['nota fiscal', 'nf-e', 'nfe', 'danfe', 'invoice'],
        'romaneio': ['romaneio', 'madeira', 'm³', 'm3', 'tora', 'cubagem'],
        'frete': ['frete', 'transporte', 'carga', 'ctrc', 'conhecimento'],
        'boleto': ['boleto', 'código de barras', 'codigo de barras', 'linha digitável', 'linha digitavel'],
        'recibo': ['recibo', 'recebi', 'pagamento']
    }

    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")

        self.text = ""
        self.info = {
            'arquivo': str(self.pdf_path),
            'nome_arquivo': self.pdf_path.name,
            'tamanho_kb': self.pdf_path.stat().st_size / 1024,
            'data_arquivo': datetime.fromtimestamp(self.pdf_path.stat().st_mtime).strftime('%Y-%m-%d'),
            'cpfs': [],
            'cnpjs': [],
            'banco': None,
            'tipo_documento': None,
            'datas': [],
            'valores': [],
            'palavras_chave': []
        }

    def extrair_texto(self) -> str:
        """Extrai todo o texto do PDF"""
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)

                # Verificar se está protegido
                if reader.is_encrypted:
                    print(f"AVISO: PDF protegido por senha", file=sys.stderr)
                    return ""

                # Extrair texto de todas as páginas
                text_parts = []
                for page_num, page in enumerate(reader.pages):
                    try:
                        text_parts.append(page.extract_text())
                    except Exception as e:
                        print(f"Erro ao extrair página {page_num + 1}: {e}", file=sys.stderr)

                self.text = "\n".join(text_parts)
                return self.text

        except Exception as e:
            print(f"ERRO ao processar PDF: {e}", file=sys.stderr)
            return ""

    def validar_cpf(self, cpf: str) -> bool:
        """Valida CPF com dígito verificador"""
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False

        # Cálculo do primeiro dígito
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10 % 11) % 10

        # Cálculo do segundo dígito
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10 % 11) % 10

        return cpf[-2:] == f"{digito1}{digito2}"

    def validar_cnpj(self, cnpj: str) -> bool:
        """Valida CNPJ com dígito verificador"""
        cnpj = re.sub(r'\D', '', cnpj)
        if len(cnpj) != 14:
            return False

        # Cálculo do primeiro dígito
        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
        digito1 = (soma % 11)
        digito1 = 0 if digito1 < 2 else 11 - digito1

        # Cálculo do segundo dígito
        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
        digito2 = (soma % 11)
        digito2 = 0 if digito2 < 2 else 11 - digito2

        return cnpj[-2:] == f"{digito1}{digito2}"

    def identificar_cpfs(self) -> List[str]:
        """Encontra e valida CPFs no texto"""
        # Padrões: 123.456.789-00 ou 12345678900
        patterns = [
            r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'
        ]

        cpfs_encontrados = set()
        for pattern in patterns:
            matches = re.finditer(pattern, self.text)
            for match in matches:
                cpf = match.group()
                if self.validar_cpf(cpf):
                    cpf_limpo = re.sub(r'\D', '', cpf)
                    cpf_formatado = f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
                    cpfs_encontrados.add(cpf_formatado)

        self.info['cpfs'] = sorted(list(cpfs_encontrados))
        return self.info['cpfs']

    def identificar_cnpjs(self) -> List[str]:
        """Encontra e valida CNPJs no texto"""
        # Padrões: 12.345.678/0001-00 ou 12345678000100
        patterns = [
            r'\b\d{2}\.?\d{3}\.?\d{3}/?0001-?\d{2}\b',
            r'\b\d{14}\b'
        ]

        cnpjs_encontrados = set()
        for pattern in patterns:
            matches = re.finditer(pattern, self.text)
            for match in matches:
                cnpj = match.group()
                if self.validar_cnpj(cnpj):
                    cnpj_limpo = re.sub(r'\D', '', cnpj)
                    cnpj_formatado = f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
                    cnpjs_encontrados.add(cnpj_formatado)

        self.info['cnpjs'] = sorted(list(cnpjs_encontrados))
        return self.info['cnpjs']

    def identificar_banco(self) -> Optional[str]:
        """Identifica qual banco baseado em palavras-chave"""
        text_lower = self.text.lower()

        for banco, keywords in self.BANCOS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    self.info['banco'] = banco
                    return banco

        return None

    def identificar_tipo_documento(self) -> Optional[str]:
        """Identifica tipo de documento baseado em palavras-chave"""
        text_lower = self.text.lower()

        # Contar ocorrências de cada tipo
        scores = {}
        for tipo, keywords in self.TIPOS_DOCUMENTO.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                scores[tipo] = count

        if scores:
            # Retornar tipo com mais ocorrências
            tipo_mais_provavel = max(scores, key=scores.get)
            self.info['tipo_documento'] = tipo_mais_provavel
            self.info['palavras_chave'] = list(self.TIPOS_DOCUMENTO[tipo_mais_provavel])
            return tipo_mais_provavel

        return None

    def identificar_datas(self) -> List[str]:
        """Encontra datas no texto"""
        # Padrões: DD/MM/YYYY, DD-MM-YYYY, YYYY-MM-DD
        patterns = [
            r'\b\d{2}/\d{2}/\d{4}\b',
            r'\b\d{2}-\d{2}-\d{4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b'
        ]

        datas_encontradas = set()
        for pattern in patterns:
            matches = re.finditer(pattern, self.text)
            for match in matches:
                data = match.group()
                datas_encontradas.add(data)

        self.info['datas'] = sorted(list(datas_encontradas))
        return self.info['datas']

    def identificar_valores(self) -> List[str]:
        """Encontra valores monetários no texto"""
        # Padrões: R$ 1.234,56 ou 1234.56
        patterns = [
            r'R\$\s*\d{1,3}(?:\.\d{3})*,\d{2}',
            r'\d{1,3}(?:\.\d{3})*,\d{2}'
        ]

        valores_encontrados = []
        for pattern in patterns:
            matches = re.finditer(pattern, self.text)
            for match in matches:
                valor = match.group()
                # Converter para float
                valor_limpo = re.sub(r'[R$\s]', '', valor)
                valor_limpo = valor_limpo.replace('.', '').replace(',', '.')
                try:
                    valor_float = float(valor_limpo)
                    if valor_float > 0:  # Ignorar valores zero
                        valores_encontrados.append({
                            'texto': valor,
                            'valor': valor_float
                        })
                except ValueError:
                    pass

        # Ordenar por valor
        valores_encontrados = sorted(valores_encontrados, key=lambda x: x['valor'], reverse=True)
        # Pegar apenas os 10 maiores
        self.info['valores'] = valores_encontrados[:10]
        return self.info['valores']

    def processar(self) -> Dict:
        """Processa o PDF completo e retorna informações"""
        print(f"Processando: {self.pdf_path.name}", file=sys.stderr)

        # Extrair texto
        self.extrair_texto()

        if not self.text:
            print("AVISO: Nenhum texto extraído (PDF pode ser imagem)", file=sys.stderr)
            self.info['erro'] = 'Sem texto extraído'
            return self.info

        # Identificar informações
        self.identificar_cpfs()
        self.identificar_cnpjs()
        self.identificar_banco()
        self.identificar_tipo_documento()
        self.identificar_datas()
        self.identificar_valores()

        # Adicionar preview do texto (primeiras 500 caracteres)
        self.info['texto_preview'] = self.text[:500].replace('\n', ' ')

        return self.info


def main():
    """Função principal"""
    if len(sys.argv) != 2:
        print("Uso: python3 pdf_processor.py <caminho_do_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    try:
        processor = PDFProcessor(pdf_path)
        info = processor.processar()

        # Imprimir resultado como JSON
        print(json.dumps(info, indent=2, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({
            'erro': str(e),
            'arquivo': pdf_path
        }, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
