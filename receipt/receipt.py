import datetime
import os
from tkinter import Tk, messagebox, filedialog

def gerar_preview(dados, salvar_arquivo=False):
    # Configurações para Epson LX-350 (80 colunas)
    largura_max = 80  # Aproveitando toda a largura do papel
    recibo_lines = []
    
    # Funções auxiliares
    def centralizar(texto, largura=largura_max):
        espacos = (largura - len(texto)) // 2
        return " " * espacos + texto
    
    def linha_separacao(caractere="=", largura=largura_max):
        return caractere * largura
    
    def linha_dupla_separacao():
        return "=" * largura_max + "\n" + "=" * largura_max
    
    # Construir o recibo linha por linha
    recibo_lines.append(linha_dupla_separacao())
    recibo_lines.append(centralizar("LAR EBENEZER - HILDA MARIA CORREA - ADAS"))
    recibo_lines.append(centralizar("RUA 20 DE BEZENRO, Nº 3170, JARDIM RASSLEN, CEP 79.813-280"))
    recibo_lines.append(centralizar("CNPJ: 12.345.678/0001-90 - Tel: (11) 98765-4321"))
    recibo_lines.append(linha_separacao("-"))
    recibo_lines.append(centralizar("RECIBO DE DOAÇÃO"))
    recibo_lines.append(linha_separacao("-"))
    recibo_lines.append("")
    
    # Dados da venda
    recibo_lines.append(f"{'Data:':<15}{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'):<65}")
    recibo_lines.append(f"{'Cliente:':<15}{dados['cliente']:<65}")
    recibo_lines.append(f"{'CPF/CNPJ:':<15}{dados['documento']:<65}")
    recibo_lines.append(f"{'Endereço:':<15}{dados['endereco']:<65}")
    recibo_lines.append(linha_separacao("-"))
    
    # Cabeçalho dos itens (ajustado para 80 colunas)
    recibo_lines.append("ITEM".ljust(5) + "DESCRIÇÃO".ljust(45) + "QTD".center(10) + "V.UNIT".rjust(10) + "TOTAL".rjust(10))
    recibo_lines.append(linha_separacao("-"))
    
    # Itens (com numeração)
    for idx, item in enumerate(dados['itens'], 1):
        descricao = (item['descricao'][:42] + "...") if len(item['descricao']) > 45 else item['descricao']
        linha = (
            str(idx).ljust(5) + 
            descricao.ljust(45) + 
            str(item['quantidade']).center(10) + 
            f"R$ {item['valor']:>7.2f}" + 
            f"R$ {item['valor'] * item['quantidade']:>7.2f}"
        )
        recibo_lines.append(linha)
    
    # Total
    total = sum(item['valor'] * item['quantidade'] for item in dados['itens'])
    recibo_lines.append(linha_separacao("="))
    recibo_lines.append("TOTAL A PAGAR:".rjust(65) + f"R$ {total:>10.2f}")
    recibo_lines.append(linha_separacao("="))
    recibo_lines.append("")
    
    # Formas de pagamento (se existir no dicionário)
    if 'pagamento' in dados:
        recibo_lines.append(f"{'Forma de Pagamento:':<20}{dados['pagamento']:<60}")
        recibo_lines.append(linha_separacao("-"))
    
    # Rodapé
    recibo_lines.append("")

    recibo_lines.append(centralizar("QUE JESUS RETRIBUA EM BÊNÇÃOS DE VIDA E SAÚDE"))
    recibo_lines.append(centralizar("O LAR EBENEZER AGRADECE SUA DOAÇÃO"))
    recibo_lines.append("")
    #recibo_lines.append(centralizar("Sistema de Vendas v1.0 - (11) 98765-4321"))
    recibo_lines.append("\n")  # Espaço antes da assinatura
    
    # Assinatura centralizada com linha tracejada
    recibo_lines.append(centralizar("_" * 30))  # Linha para assinatura
    recibo_lines.append(centralizar("Assinatura do Responsável"))
    recibo_lines.append("\n" * 5)  # Espaço para corte do papel
    
    # Mostrar no console
    print("\n".join(recibo_lines))
    
    # Salvar em arquivo se solicitado
    if salvar_arquivo:
        root = Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt")],
            title="Salvar pré-visualização do recibo"
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(recibo_lines))
            messagebox.showinfo("Sucesso", f"Pré-visualização salva em:\n{file_path}")
        root.destroy()
    
    return recibo_lines

def imprimir_recibo(dados):
    # Primeiro geramos a pré-visualização
    preview = gerar_preview(dados)
    
    # Perguntar se deseja imprimir
    root = Tk()
    root.withdraw()
    resposta = messagebox.askyesno("Confirmação", "Deseja imprimir o recibo?")
    root.destroy()
    
    if not resposta:
        return

# Exemplo de uso completo
dados_recibo = {
    'cliente': 'Maria da Silva',
    'documento': '123.456.789-00',
    'endereco': 'Av. Paulista, 1000 - São Paulo/SP',
    'pagamento': 'Cartão de Crédito (3x R$ 43,23)',
    'itens': [
        {'descricao': 'Doação Referente ao Mês de Outubro', 'quantidade': 1, 'valor': 29.90}
    ]
}

# Para testar a pré-visualização
gerar_preview(dados_recibo, salvar_arquivo=True)

# Para imprimir diretamente (com confirmação)
# imprimir_recibo(dados_recibo)