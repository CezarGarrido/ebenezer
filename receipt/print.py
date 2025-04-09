import datetime
import os
import platform

# Só importa win32print se for Windows
if platform.system() == "Windows":
    import win32print

# Importa Tkinter para visualização no Linux
import tkinter as tk
from tkinter import scrolledtext

def gerar_recibo_texto():
    hoje = datetime.datetime.now()
    emitido_em = hoje.strftime("%d/%m/%Y")
    def condensado(texto):
        ESC = chr(27)
        SI = chr(15)
        DC2 = chr(18)
        return ESC + SI + texto + ESC + DC2

    linhas = []
    append = linhas.append
    append("LAR EBENEZER - HILDA MARIA CORREA - ADAS".center(120))
    append(condensado("Utilidade Pública Municipal Lei Nº 1527 de 09/11/88    Utilidade Pública Estadual Lei Nº 1493 de 13/05/94"))
    append(condensado("Utilidade Pública Federal Portaria Nº 735 de 13/08/01 DOU 14/08/01  CEBAS: CEBAS 0030 Resolução Nº 05 de 02/02/04 DOU 05/02/04"))
    append(condensado("Atest. de Reg. no Cons. Mun. de Assist. Soc. R n° 0018 Res n° 05 de 02/02/04 DOU 05/02/04"))
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

def listar_impressoras():
    return [p[2] for p in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]

def imprimir_com_win32print(texto, preferida="EPSON LX-350"):
    impressoras = listar_impressoras()
    bytes_texto = texto.encode("latin1", errors="replace")

    if preferida in impressoras:
        nome_impressora = preferida
        print(f"Usando impressora preferida: {nome_impressora}")
    else:
        nome_impressora = win32print.GetDefaultPrinter()
        print(f"A impressora '{preferida}' não foi encontrada. Usando padrão: {nome_impressora}")

    try:
        hPrinter = win32print.OpenPrinter(nome_impressora)
        hJob = win32print.StartDocPrinter(hPrinter, 1, ("Recibo de Doação", None, "RAW"))
        win32print.StartPagePrinter(hPrinter)
        win32print.WritePrinter(hPrinter, bytes_texto)
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
        print(f"Recibo impresso com sucesso na '{nome_impressora}'.")
    except Exception as e:
        print("Erro ao imprimir:", e)
    finally:
        try:
            win32print.ClosePrinter(hPrinter)
        except:
            pass

def salvar_em_arquivo(texto, caminho_arquivo="recibo_doacao.txt"):
    try:
        with open(caminho_arquivo, "w", encoding="latin1") as f:
            f.write(texto)
        print(f"Recibo salvo em: {os.path.abspath(caminho_arquivo)}")
    except Exception as e:
        print("Erro ao salvar recibo:", e)

def mostrar_preview_tk(texto):
    janela = tk.Tk()
    janela.title("Pré-visualização do Recibo")
    
    text_area = scrolledtext.ScrolledText(janela, font=("Courier New", 10), width=120, height=40)
    text_area.pack(fill=tk.BOTH, expand=True)
    text_area.insert(tk.END, texto)
    text_area.config(state=tk.DISABLED)

    janela.mainloop()

if __name__ == "__main__":
    texto = gerar_recibo_texto()

    # Flags de controle
    salvar = True
    imprimir = True

    if salvar:
        salvar_em_arquivo(texto, "recibo_doacao.txt")

    sistema = platform.system()
    if sistema == "Windows" and imprimir:
        imprimir_com_win32print(texto, preferida="EPSON LX-350")
    elif sistema == "Linux":
        mostrar_preview_tk(texto)
    else:
        print("Sistema não suportado para impressão automática. Exibindo preview.")
        mostrar_preview_tk(texto)
