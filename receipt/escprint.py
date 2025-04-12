from escpbuilder import ESCPBuilder  # suponha que você salvou a lib anterior como escbuilder.py

def gerar_recibo_ebenezer():
    
    center= 66
    def linha_lado_lado(esquerda, direita, largura=center):
        return f"{esquerda}{' ' * (largura - len(esquerda) - len(direita))}{direita}"

    b = ESCPBuilder()
    b.set_charset().font(draft=True)

    # Cabeçalho institucional
    b.bold(True).linefeed()
    b.text("LAR EBENEZER - HILDA MARIA CORREA - ADAS".center(center+40))
    b.bold(False).linefeed()
    b.condensed(True)  # Fonte menor
    a = "Utilidade Pública Municipal Lei Nº 1527 de 09/11/88"
    c = "Utilidade Pública Estadual Lei Nº 1493 de 13/05/94"
    
    b.text(linha_lado_lado(f"{a}", f"{c}", largura=center+40)).linefeed()

    b.text(linha_lado_lado(f"Utilidade Pública Federal Portaria Nº 735 de 13/08/01 DOU 14/08/01 ", 
                           f"CEBAS: CEBAS 0030 Resolução Nº 05 de 02/02/04 DOU 05/02/04", largura=center+40)).linefeed()

    b.text("Atest. de Reg. no Cons. Mun. de Assist. Soc. R n° 0018 Res n° 05 de 02/02/04 DOU 05/02/04\n".center(center+40))
    b.condensed(False)  # Fonte menor
    
    b.text("RUA 20 DE BEZENRO, Nº 3170, JARDIM RASSLEN, CEP 79.813-280".center(center + 40)).linefeed()
    b.text("DOURADOS - MS".center(center + 40)).linefeed()
    b.text("TELEFONE Nº: 67 3425-4118    CNPJ Nº 03.471.216/0001-23").linefeed()
    b.text("CELULARES: 67 9201-6365 / 67 9201-5508 / 67 9201-8151").linefeed(2)

    # Linha de separação
    b.text("=" * (center + 40)).linefeed()
    b.bold(True).text("RECIBO DE DOAÇÕES".center(center + 40)).linefeed()
    b.text("=" * (center + 40)).linefeed()

    # Dados do recibo

    b.text(linha_lado_lado(f"Recibo Nº: 1343434343", f"Emitido em: 15/10/2025", largura=center+40)).linefeed()

    b.text("Recebemos de: IMOBILIARIA ATHENAS (6172)").linefeed()
    b.text("Endereço....: CIRO MELO Nº 2255").linefeed()
    b.text("Bairro......: CENTRO").linefeed()
    b.text("Contato.....: (67) 9 99999-9999").linefeed()
    b.text("Cidade......: DOURADOS - MS").linefeed()
    b.text("Valor.......: R$ 150.00").linefeed()
    b.text("Por Extenso.: CENTO E CINQUENTA REAIS").linefeed()
    b.text("Pago em.....: PIX").linefeed()

    b.text("Referente a: DOAÇÃO PARA O MES DE OUTUBRO").linefeed(2)

    # Mensagem final
    b.text("QUE JESUS RETRIBUA EM BÊNÇÃOS DE VIDA E SAÚDE".center(center + 40)).linefeed()
    b.text("O LAR EBENEZER AGRADECE SUA DOAÇÃO".center(center + 40)).linefeed(2)

    b.text("______________________________".center(center + 40)).linefeed()
    b.text("Assinatura do Responsável".center(center + 40)).linefeed()

    b.form_feed()

    return b.build()


dados = gerar_recibo_ebenezer().decode("latin1")
with open("recibo_saida.esc", "w", encoding="latin1") as f:
        f.write(dados)