import sys

class ESCPrinter:
    def __init__(self, printer, escp24pin):
        """
        Construtor da classe ESCPrinter
        :param printer: string indicando o caminho da impressora na rede
        :param escp24pin: booleano indicando se a impressora é 24 pinos ESC/P2
        """
        
        self.printer = printer
        self.escp24pin = escp24pin
        self.ostream = None
        self.streamOpenSuccess = False
        
        # Constantes
        self.MAX_ADVANCE_9PIN = 216  # Para impressoras 24/48 pinos ESC/P2 deve ser 180
        self.MAX_ADVANCE_24PIN = 180
        self.MAX_UNITS = 127  # Para posicionamento vertical, 127 como máximo parece funcionar melhor
        self.CM_PER_INCH = 2.54
        
        # Comandos ESC/P em ASCII
        self.ESC = chr(27)
        self.AT = chr(64)
        self.LINE_FEED = chr(10)
        self.PARENTHESIS_LEFT = chr(40)
        self.BACKSLASH = chr(92)
        self.CR = chr(13)
        self.TAB = chr(9)
        self.FF = chr(12)
        self.g = chr(103)
        self.p = chr(112)
        self.t = chr(116)
        self.l = chr(108)
        self.x = chr(120)
        self.E = chr(69)
        self.F = chr(70)
        self.J = chr(74)
        self.P = chr(80)
        self.Q = chr(81)
        self.dollar = chr(36)  # $ é palavra reservada em Python
        
        # Argumentos
        self.ARGUMENT_0 = chr(0)
        self.ARGUMENT_1 = chr(1)
        self.ARGUMENT_2 = chr(2)
        self.ARGUMENT_3 = chr(3)
        self.ARGUMENT_4 = chr(4)
        self.ARGUMENT_5 = chr(5)
        self.ARGUMENT_6 = chr(6)
        self.ARGUMENT_7 = chr(7)
        self.ARGUMENT_25 = chr(25)
        
        # Conjuntos de caracteres
        self.USA = self.ARGUMENT_1
        self.BRAZIL = self.ARGUMENT_25
    
    def close(self):
        """Fecha o stream, usado quando o trabalho de impressão termina"""
        if self.ostream:
            try:
                self.ostream.close()
            except IOError as e:
                print(f"Erro ao fechar o stream: {e}", file=sys.stderr)
    
    def initialize(self):
        """Inicializa a impressora e retorna True se bem-sucedido"""
        self.streamOpenSuccess = False
        
        try:
            self.ostream = open(self.printer, 'wb')
            
            # Reset configurações padrão
            self._write(self.ESC + self.AT)
            
            # Seleciona pitch de 10 caracteres por polegada
            self.select10CPI()
            
            # Seleciona qualidade de rascunho
            self.selectDraftPrinting()
            
            # Define conjunto de caracteres
            self.setCharacterSet(self.BRAZIL)
            
            self.streamOpenSuccess = True
        except IOError as e:
            print(f"Erro ao inicializar impressora: {e}", file=sys.stderr)
        
        return self.streamOpenSuccess
    
    def _write(self, data):
        """Método auxiliar para escrever dados na impressora"""
        if self.ostream:
            try:
                if isinstance(data, str):
                    self.ostream.write(data.encode('latin-1'))
                else:
                    self.ostream.write(data)
                self.ostream.flush()
            except IOError as e:
                print(f"Erro ao escrever na impressora: {e}", file=sys.stderr)
    
    def select10CPI(self):
        """10 caracteres por polegada (condensado disponível)"""
        self._write(self.ESC + self.P)
    
    def select15CPI(self):
        """15 caracteres por polegada (condensado não disponível)"""
        self._write(self.ESC + self.g)
    
    def selectDraftPrinting(self):
        """Define qualidade de impressão como rascunho"""
        self._write(self.ESC + self.x + chr(48))
    
    def selectLQPrinting(self):
        """Define qualidade de impressão como letter quality"""
        self._write(self.ESC + self.x + chr(49))
    
    def setCharacterSet(self, charset):
        """Define o conjunto de caracteres"""
        # Atribui tabela de caracteres
        self._write(self.ESC + self.PARENTHESIS_LEFT + self.t + 
                   self.ARGUMENT_3 + self.ARGUMENT_0 + 
                   self.ARGUMENT_1 + charset + self.ARGUMENT_0)
        
        # Seleciona tabela de caracteres
        self._write(self.ESC + self.t + self.ARGUMENT_1)
    
    def lineFeed(self):
        """Executa nova linha"""
        self._write(self.CR + self.LINE_FEED)
    
    def formFeed(self):
        """Ejeita uma única folha"""
        self._write(self.CR + self.FF)
    
    def bold(self, bold):
        """Ativa/desativa negrito"""
        self._write(self.ESC + (self.E if bold else self.F))
    
    def proportionalMode(self, proportional):
        """Ativa/desativa modo proporcional"""
        self._write(self.ESC + self.p + (chr(49) if proportional else chr(48)))
    
    def advanceVertical(self, centimeters):
        """Avança a posição vertical de impressão aproximadamente em centímetros"""
        inches = centimeters / self.CM_PER_INCH
        units = int(inches * (self.MAX_ADVANCE_24PIN if self.escp24pin else self.MAX_ADVANCE_9PIN))
        
        while units > 0:
            n = chr(self.MAX_UNITS) if units > self.MAX_UNITS else chr(units)
            self._write(self.ESC + self.J + n)
            units -= self.MAX_UNITS
    
    def advanceHorizontal(self, centimeters):
        """Avança a posição horizontal de impressão aproximadamente em centímetros"""
        inches = centimeters / self.CM_PER_INCH
        units = int(inches * 120)
        units_low = units % 256
        units_high = units // 256
        
        self._write(self.ESC + self.BACKSLASH + chr(units_low) + chr(units_high))
    
    def setAbsoluteHorizontalPosition(self, centimeters):
        """Define a posição horizontal absoluta em centímetros da margem esquerda"""
        inches = centimeters / self.CM_PER_INCH
        units = int(inches * 60)
        units_low = units % 256
        units_high = units // 256
        
        self._write(self.ESC + self.dollar + chr(units_low) + chr(units_high))
    
    def horizontalTab(self, tabs):
        """Executa tabulação horizontal o número especificado de vezes"""
        self._write(self.TAB * tabs)
    
    def setMargins(self, columnsLeft, columnsRight):
        """Define margens esquerda e direita em colunas"""
        # Margem esquerda
        self._write(self.ESC + self.l + chr(columnsLeft))
        
        # Margem direita
        self._write(self.ESC + self.Q + chr(columnsRight))
    
    def print(self, text):
        """Imprime texto"""
        self._write(text)
    
    def isInitialized(self):
        """Retorna True se a impressora foi inicializada com sucesso"""
        return self.streamOpenSuccess
    
    def getShare(self):
        """Retorna o nome do compartilhamento da impressora (rede Windows)"""
        return self.printer
    
    def __str__(self):
        """Retorna representação em string do ESCPrinter"""
        
        return f"<ESCPrinter[share={self.printer}, 24pin={self.escp24pin}]>"
        