import datetime
import os
import tempfile
import platform
import subprocess

def gerar_recibo_texto():
    hoje = datetime.datetime.now()
    emitido_em = hoje.strftime("%d/%m/%Y")

    linhas = []
    append = linhas.append
    append("LAR EBENEZER - HILDA MARIA CORREA - ADAS".center(120))
    append("Utilidade Pública Municipal Lei Nº 1527 de 09/11/88    Utilidade Pública Estadual Lei Nº 1493 de 13/05/94")
    append("Utilidade Pública Federal Portaria Nº 735 de 13/08/01 DOU 14/08/01  CEBAS: CEBAS 0030 Resolução Nº 05 de 02/02/04 DOU 05/02/04")
    append("Atest. de Reg. no Cons. Mun. de Assist. Soc. R n° 0018 Res n° 05 de 02/02/04 DOU 05/02/04")
    append("RUA 20 DE BEZENRO, Nº 3170, JARDIM RASSLEN, CEP 79.813-280".center(120))
    append("DOURADOS - MS".center(120))
    append("TELEFONE Nº: 67 3425-4118    CNPJ Nº 03.471.216/0001-23".center(120))
    append("CELULARES: 67 9201-6365 / 67 9201-5508 / 67 9201-8151".center(120))
    append("=" * 120)
    append("RECIBO DE DOAÇÕES".center(120))
    append("=" * 120)
    append("")
    append(f"Recibo Nº: 0001241303".ljust(60) + f"Emitido em: {emitido_em}")
    append("")
    append("Recebemos de: IMOBILIARIA ATHENAS (6172)")
    append("Endereço....: CIRQ MELO Nº 2255")
    append("Bairro......: CENTRO")
    append("Contato.....: DEPÓSITO EM CHEQUE C/C 126-4")
    append("Cidade......: DOURADOS - MS")
    append("Valor.......: R$ 150.00")
    append("Por Extenso.: CENTO E CINQUENTA REAIS")
    append("")
    append("Referente a: DOAÇÃO PARA O MES DE OUTUBRO")
    append("")
    append("QUE JESUS RETRIBUA EM BÊNÇÃOS DE VIDA E SAÚDE".center(120))
    append("O LAR EBENEZER AGRADECE SUA DOAÇÃO".center(120))
    append("")
    append("_" * 30)
    append("Assinatura do Responsável".center(120))
    append("\n" * 5)

    return "\n".join(linhas)

def imprimir_recibo(texto, nome_impressora=None):
    sistema = platform.system()
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="latin1", suffix=".txt") as f:
        f.write(texto)
        caminho = f.name

    if sistema == "Windows":
        if nome_impressora:
            # Se quiser definir uma impressora específica
            os.system(f'notepad /p "{caminho}"')  # ou usar win32print se quiser mais controle
        else:
            os.startfile(caminho, "print")
    elif sistema == "Linux":
        if nome_impressora:
            pass
    else:
        print("Sistema operacional não suportado para impressão automática.")
        print(texto)

if __name__ == "__main__":
    recibo_texto = gerar_recibo_texto()
    imprimir_recibo(recibo_texto)
