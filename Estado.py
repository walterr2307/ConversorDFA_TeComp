class Estado:
    def __init__(self, simbolo, alfabeto):
        self.simbolo = simbolo
        self.inicial = False
        self.final = False
        self.transicoes = {}

        for letra in alfabeto:
            self.transicoes[letra] = ""

    def __str__(self):
        str = "{}, Inicial: {}".format(self.simbolo, self.inicial)
        str += ", Final: {} → ".format(self.final)
        
        for letra, transicao in self.transicoes.items():
            str += "({}, {}) ".format(letra, transicao)

        return str + "\n"
