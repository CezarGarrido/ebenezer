class ESCPBuilder:
    # Caractere de controle ESC (Escape)
    # Usado como prefixo para iniciar comandos ESC/P
    ESC = b'\x1B'  # ASCII 27

    # Line Feed (nova linha / avanço de papel)
    # Move o papel uma linha para baixo (vertical)
    LF = b'\x0A'   # ASCII 10

    # Carriage Return (retorno do carro)
    # Move o cabeçote de impressão para o início da linha (horizontal)
    CR = b'\x0D'   # ASCII 13

    # Form Feed (avanço de formulário)
    # Avança o papel até o topo da próxima página (ejetar folha)
    FF = b'\x0C'   # ASCII 12

    CHARSET_SELECT = b't'
    
    CHARSET_ASSIGN = b'(t'
    
    ARGUMENTS = [bytes([i]) for i in range(256)]
    BRAZIL    = ARGUMENTS[25]
    USA       = ARGUMENTS[1]

    def __init__(self):
        self.commands = bytearray()
        self.reset()

    def reset(self):
        self.commands += self.ESC + b'@'  # Reset impressora
        return self

    def text(self, content):
        if isinstance(content, str):
            content = content.encode('latin1')  # Compatível com ESC/P
        self.commands += content
        return self

    def bold(self, enable=True):
        self.commands += self.ESC + (b'E' if enable else b'F')
        return self

    def italic(self, enable=True):
        self.commands += self.ESC + b'4' if enable else self.ESC + b'5'
        return self

    def underline(self, enable=True):
        self.commands += self.ESC + b'-' + (b'\x01' if enable else b'\x00')
        return self

    def font(self, draft=True):
        self.commands += self.ESC + b'x' + (b'0' if draft else b'1')
        return self

    def linefeed(self, lines=1):
        for _ in range(lines):
            self.commands += self.CR + self.LF
        return self

    def form_feed(self):
        self.commands += self.CR + self.FF
        return self
    
    def set_charset(self, charset=BRAZIL):
        self.commands += self.ESC + self.CHARSET_ASSIGN + b'\x03\x00\x01' + charset + b'\x00'
        self.commands += self.ESC + self.CHARSET_SELECT + b'\x01'
        return self

    def horizontal_tab(self, count=1):
        self.commands += b'\x09' * count
        return self
    
    def condensed(self, enable=True):
        self.commands += self.ESC + (b'\x0F' if enable else b'\x12')
        if enable:
            self.commands += self.CR  # evita perda do primeiro caractere
        return self

    def build(self):
        return bytes(self.commands)
