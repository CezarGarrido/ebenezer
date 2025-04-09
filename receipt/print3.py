import datetime
from tkinter import Tk, messagebox

def imprimir_recibo_imobiliaria(dados):
    # Configurações para Epson LX-350
    largura_max = 80  # 80 colunas
    recibo_lines = []
    
    # Funções auxiliares
    def centralizar(texto, largura=largura_max):
        espacos = (largura - len(texto)) // 2
        return " " * espacos + texto
    
    def linha_separacao(caractere="=", largura=largura_max):
        return caractere * largura
    
    # Cabeçalho da instituição
    recibo_lines.append(centralizar("LAR EBENEZER - HILDA MARIA CORREA - ADAS"))
    recibo_lines.append(centralizar("Utilidade Pública Municipal Lei Nº 1527 de 09/11/88"))
    recibo_lines.append(centralizar("Utilidade Pública Estadual Lei Nº 1493 de 13/05/94"))
    recibo_lines.append(centralizar("Utilidade Pública Federal Portaria Nº 735 de 13/08/01 DOU 14/08/01"))
    recibo_lines.append(centralizar("CEBAS: CEBAS 0030 Resolução Nº 05 de 02/02/04 DOU 05/02/04"))
    recibo_lines.append(centralizar("Atest. de Reg. no Cons. Mun. de Assist. Soc. R n° 0018 Res n° 05 de 02/02/04 DOU 05/02/04"))
    recibo_lines.append(centralizar("RUA 20 DE BEZENRO, Nº 3170, JARDIM RASSLEN, CEP 79.813-280"))
    recibo_lines.append(centralizar("DOURADOS - MS"))
    recibo_lines.append(centralizar("TELEFONE Nº: 67 3425-4118    CNPJ Nº 03.471.216/0001-23"))
    recibo_lines.append(centralizar("CELULARES: 67 9201-6365 / 67 9201-5508 / 67 9201-8151"))
    recibo_lines.append(linha_separacao())
    recibo_lines.append(centralizar("RECIBO DE DOAÇÕES"))
    recibo_lines.append(linha_separacao())
    recibo_lines.append("")
    
    # Dados do recibo
    recibo_lines.append(f"Recibo Nº: {dados['numero_recibo']}".ljust(40) + f"Emitido em: {dados['data_emissao']}")
    recibo_lines.append("")
    recibo_lines.append(f"Recebemos de: {dados['doador']} ({dados['codigo_doador']})")
    recibo_lines.append(f"Endereço....: {dados['endereco_doador']}")
    recibo_lines.append(f"Bairro......: {dados['bairro_doador']}")
    recibo_lines.append(f"Contato.....: {dados['contato_doador']}")
    recibo_lines.append(f"Cidade......: {dados['cidade_doador']} - {dados['uf_doador']}")
    recibo_lines.append(f"Valor.......: R$ {dados['valor']:.2f}")
    recibo_lines.append(f"Por Extenso.: {dados['valor_extenso']}")
    recibo_lines.append("")
    recibo_lines.append(f"Referente a: {dados['referente_a']}")
    recibo_lines.append("")
    recibo_lines.append(centralizar("QUE JESUS RETRIBUA EM BÊNÇÃOS DE VIDA E SAÚDE"))
    recibo_lines.append(centralizar("O LAR EBENEZER AGRADECE SUA DOAÇÃO"))
    recibo_lines.append("")
    recibo_lines.append("")
    
    # Assinatura
    recibo_lines.append(centralizar("_" * 30))
    recibo_lines.append(centralizar("Assinatura do Responsável"))
    recibo_lines.append("\n" * 5)  # Espaço para corte
    
    # Imprimir na Epson LX-350
    print("\n".join(recibo_lines))

# Exemplo de uso
dados_recibo = {
    'numero_recibo': '0001241303',
    'data_emissao': '15/10/2024',
    'doador': 'IMOBILIARIA ATHENAS',
    'codigo_doador': '6172',
    'endereco_doador': 'CIRQ MELO Nº 2255',
    'bairro_doador': 'CENTRO',
    'contato_doador': 'DEPÓSITO EM CHEQUE C/C 126-4',
    'cidade_doador': 'DOURADOS',
    'uf_doador': 'MS',
    'valor': 150.00,
    'valor_extenso': 'CENTO E CINQUENTA REAIS',
    'referente_a': 'DOAÇÃO PARA O MES DE OUTUBRO'
}

# Para imprimir o recibo
imprimir_recibo_imobiliaria(dados_recibo)