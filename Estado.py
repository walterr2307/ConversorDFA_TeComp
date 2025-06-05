class Estado:
    def __init__(self, simbolo, alfabeto):
        self.simbolo = simbolo  # Símbolo que representa o estado (ex: 'A', 'B', etc.)
        self.inicial = False  # Indica se o estado é o estado inicial
        self.final = False  # Indica se o estado é um estado final (de aceitação)
        self.transicoes = {}  # Dicionário que armazena as transições do estado

        for letra in alfabeto:
            self.transicoes[letra] = (
                ""  # Inicializa as transições com cadeia vazia para cada letra do alfabeto
            )
