from html import escape
import re

class ESCPrinter:
    def __init__(self, escp24pin=False):
        """
        Construtor da classe ESCPrinter
        :param printer: string indicando o caminho da impressora (não usado agora)
        :param escp24pin: booleano indicando se a impressora é 24 pinos ESC/P2
        """
        self.escp24pin = escp24pin
        self.commands = bytearray()
        self.streamOpenSuccess = False
        
        # Constantes
        self.MAX_ADVANCE_9PIN = 216
        self.MAX_ADVANCE_24PIN = 180
        self.MAX_UNITS = 127
        self.CM_PER_INCH = 2.54
        
        # ESC/P comandos
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
        self.dollar = chr(36)
        
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
        
        self.USA = self.ARGUMENT_1
        self.BRAZIL = self.ARGUMENT_25
    
        self.columnsRight = -1
        self.columnsLeft = -1
        
        self.LINES_PER_PAGE = 66
        self.LINES_PER_HALF_PAGE = self.LINES_PER_PAGE // 2
        self.printed_lines = 0
        
    def close(self):
        """Simula o fechamento do stream"""
        pass  # Nada a fechar porque está tudo na memória
    
    def initialize(self):
        """Inicializa o buffer de comandos"""
        self.commands.clear()
        self.streamOpenSuccess = True
        
        self._write(self.ESC + self.AT)
        self.select10CPI()
        self.selectDraftPrinting()
        self.setCharacterSet(self.BRAZIL)
        
        return self.streamOpenSuccess
    
    def _write(self, data):
        """Acumula dados em memória"""
        if isinstance(data, str):
            self.commands += data.encode('latin-1')
        else:
            self.commands += data

    def select10CPI(self):
        self._write(self.ESC + self.P)
    
    def select15CPI(self):
        self._write(self.ESC + self.g)
    
    def selectDraftPrinting(self):
        self._write(self.ESC + self.x + chr(48))
    
    def selectLQPrinting(self):
        self._write(self.ESC + self.x + chr(49))
    
    def setCharacterSet(self, charset):
        self._write(self.ESC + self.PARENTHESIS_LEFT + self.t + 
                    self.ARGUMENT_3 + self.ARGUMENT_0 + 
                    self.ARGUMENT_1 + charset + self.ARGUMENT_0)
        self._write(self.ESC + self.t + self.ARGUMENT_1)
    
    def lineFeed(self, lines=1):
        for _ in range(lines):
            self._write(self.CR + self.LINE_FEED)
        self.printed_lines += lines
        return self
    
    def fill_to_end_of_current_page(self):
        linhas_restantes = self.LINES_PER_PAGE - (self.printed_lines % self.LINES_PER_PAGE)
        if linhas_restantes > 0 and linhas_restantes < self.LINES_PER_PAGE:
            self.lineFeed(linhas_restantes)

    def fill_to_end_of_half_page(self):
        linhas_restantes = self.LINES_PER_HALF_PAGE - (self.printed_lines % self.LINES_PER_HALF_PAGE) - 1
        if linhas_restantes > 0 and linhas_restantes < self.LINES_PER_HALF_PAGE:
            self.lineFeed(linhas_restantes)    

    def formFeed(self):
        self._write(self.CR + self.FF)
    
    def bold(self, bold):
        self._write(self.ESC + (self.E if bold else self.F))
        return self
        
    def condensed(self, enable=True):
        """Ativa ou desativa modo condensado"""
        if enable:
            self._write(self.ESC + chr(15))  # Condensed ON
            self._write(self.CR)
        else:
            # Reset completo
            self.reset()
            self.select10CPI()
            self.selectDraftPrinting()
            self.setCharacterSet(self.BRAZIL)
            
            if self.columnsLeft > 0 and self.columnsRight > 0:
                self.setMargins(self.columnsLeft, self.columnsRight)

        return self

    def reset(self):
        self._write(self.ESC + self.AT)  # ESC @

    def proportionalMode(self, proportional):
        self._write(self.ESC + self.p + (chr(49) if proportional else chr(48)))
    
    def advanceVertical(self, centimeters):
        inches = centimeters / self.CM_PER_INCH
        units = int(inches * (self.MAX_ADVANCE_24PIN if self.escp24pin else self.MAX_ADVANCE_9PIN))
        
        while units > 0:
            n = chr(self.MAX_UNITS) if units > self.MAX_UNITS else chr(units)
            self._write(self.ESC + self.J + n)
            units -= self.MAX_UNITS
    
    def advanceHorizontal(self, centimeters):
        inches = centimeters / self.CM_PER_INCH
        units = int(inches * 120)
        units_low = units % 256
        units_high = units // 256
        
        self._write(self.ESC + self.BACKSLASH + chr(units_low) + chr(units_high))
    
    def setAbsoluteHorizontalPosition(self, centimeters):
        inches = centimeters / self.CM_PER_INCH
        units = int(inches * 60)
        units_low = units % 256
        units_high = units // 256
        
        self._write(self.ESC + self.dollar + chr(units_low) + chr(units_high))
    
    def horizontalTab(self, tabs):
        self._write(self.TAB * tabs)
    
    def setMargins(self, columnsLeft, columnsRight):
        self.columnsLeft = columnsLeft
        self.columnsRight = columnsRight
        self._write(self.ESC + self.l + chr(columnsLeft))
        self._write(self.ESC + self.Q + chr(columnsRight))
        return self
    
    def print(self, text):
        self._write(text)
        return self
    
    def isInitialized(self):
        return self.streamOpenSuccess
    
    def build(self):
        """Retorna os comandos acumulados como bytes"""
        return bytes(self.commands)
    
    def __str__(self):
        return f"<ESCPrinter[24pin={self.escp24pin}]>"

    def to_html(self, data: bytes) -> str:
        # Converte os bytes para string usando latin1 (compatível com ESC/P)
        texto = data.decode('latin1')

        # Substituições de controle
        texto = (
            texto
            .replace('\x1BE', '<b>')   # ESC E → Negrito ON
            .replace('\x1BF', '</b>')  # ESC F → Negrito OFF
            .replace('\x0D', '')       # CR (carriage return)
            .replace('\x0C', '\f')     # FF → marca página (vamos dividir depois)
        )

        # Remove outros comandos ESC/P (menos os que mapeamos acima)
        texto = re.sub(r'\x1B[@-Z\\^_]', '', texto)            # ESC comandos simples
        texto = re.sub(r'\x1B\([^\x1B]{0,6}', '', texto)       # ESC (x comandos
        texto = re.sub(r'\x1B\(t[\s\S]{0,6}', '', texto)       # ESC (t com charset
        texto = re.sub(r'\x1Bt.', '', texto)                   # ESC tX
        texto = re.sub(r'\x1Bx.', '', texto)                   # ESC xX
        
        # Processa texto condensado (alternando entre normal e condensado)
        partes = []
        condensado = False
        for char in texto:
            if char == '\x0F':  # Condensed ON
                condensado = True
                partes.append('<span style="font-size: 8px;font-stretch:condensed;">')
            elif char == '\x12':  # Condensed OFF
                condensado = False
                partes.append('</span>')
            elif char == '\x1B':  # ESC perdido
                continue
            else:
                partes.append(char)
        
        texto_processado = ''.join(partes)
        
        # Fecha qualquer tag de condensed não fechada
        if condensado:
            texto_processado += '</span>'

        # Divide por páginas (form feed)
        blocos = texto_processado.split('\f')
        html_blocos = []

        for bloco in blocos:
            if bloco.strip():
                # Protege conteúdo não interpretado (evita quebras por acentos)
                bloco_escapado = escape(bloco)
                # Mantém as tags HTML (negrito e condensed) interpretáveis
                bloco_final = (
                    bloco_escapado
                    .replace('&lt;b&gt;', '<b>')
                    .replace('&lt;/b&gt;', '</b>')
                    .replace('&lt;span style=&quot;font-size: 8px;font-stretch:condensed;&quot;&gt;', 
                            '<span style="font-size: 8px;font-stretch:condensed;">')
                    .replace('&lt;/span&gt;', '</span>')
                )
                html_blocos.append(f"<pre>{bloco_final}</pre>")

        return '\n'.join(html_blocos)
    

        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm

        PAGE_WIDTH, PAGE_HEIGHT = A4
        MARGIN_LEFT = 15 * mm
        MARGIN_TOP = 20 * mm
        LINE_HEIGHT = 5 * mm
        FONT_NAME = "Courier"
        FONT_SIZE = 9
        FONT_SIZE_CONDENSED = 6.5
        CHAR_WIDTH = 3 * mm
        CHAR_WIDTH_CONDENSED = 2 * mm

        c = canvas.Canvas(pdf_path, pagesize=A4)
        x = MARGIN_LEFT
        y = PAGE_HEIGHT - MARGIN_TOP
        condensed = False
        bold = False

        current_font = FONT_NAME
        current_font_size = FONT_SIZE
        current_char_width = CHAR_WIDTH
        c.setFont(current_font, current_font_size)

        text_buffer = ""
        
        def flush_buffer():
            nonlocal x, y
            if text_buffer:
                if bold:
                    c.setFont(f"{current_font}-Bold", current_font_size)
                else:
                    c.setFont(current_font, current_font_size)
                c.drawString(x, y, text_buffer)
                return len(text_buffer) * current_char_width
            return 0

        for char in data.decode('latin-1', errors='ignore'):
            if char == '\f':  # Form feed - nova página
                flush_buffer()
                c.showPage()
                y = PAGE_HEIGHT - MARGIN_TOP
                x = MARGIN_LEFT
                text_buffer = ""
                continue
            elif char == '\n':  # Nova linha
                x += flush_buffer()
                y -= LINE_HEIGHT
                x = MARGIN_LEFT
                text_buffer = ""
                
                # Verifica se precisa de nova página
                if y < MARGIN_TOP:
                    c.showPage()
                    y = PAGE_HEIGHT - MARGIN_TOP
                    x = MARGIN_LEFT
                continue
            elif char == '\r':  # Carriage return - volta ao início da linha
                x += flush_buffer()
                x = MARGIN_LEFT
                text_buffer = ""
                continue
            elif char == '\x0F':  # Condensed ON
                x += flush_buffer()
                condensed = True
                current_font_size = FONT_SIZE_CONDENSED
                current_char_width = CHAR_WIDTH_CONDENSED
                text_buffer = ""
                continue
            elif char == '\x12':  # Condensed OFF
                x += flush_buffer()
                condensed = False
                current_font_size = FONT_SIZE
                current_char_width = CHAR_WIDTH
                text_buffer = ""
                continue
            elif char == '\x1B':  # ESC - início de comando (vamos ignorar)
                continue
            elif char == '\x1BE':  # Bold ON
                x += flush_buffer()
                bold = True
                text_buffer = ""
                continue
            elif char == '\x1BF':  # Bold OFF
                x += flush_buffer()
                bold = False
                text_buffer = ""
                continue
            elif ord(char) < 32:  # Ignora outros caracteres de controle
                continue
            else:
                text_buffer += char
                # Se o próximo caractere ultrapassar a margem direita, faz flush
                if x + (len(text_buffer) * current_char_width) > PAGE_WIDTH - MARGIN_LEFT:
                    x += flush_buffer()
                    y -= LINE_HEIGHT
                    x = MARGIN_LEFT
                    text_buffer = ""
                    
                    # Verifica se precisa de nova página
                    if y < MARGIN_TOP:
                        c.showPage()
                        y = PAGE_HEIGHT - MARGIN_TOP
                        x = MARGIN_LEFT

        # Flush do buffer final
        flush_buffer()
        c.save()