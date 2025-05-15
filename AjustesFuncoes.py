from AjusteVariaveis import AjusteVariaveis


class Variavel:
    def __init__(self, simbolo):
        self.simbolo = simbolo
        self.inicial = False
        self.final = False
        self.regras = {}

    def __str__(self):
        str = "{}, inicial: {}, final: {} > ".format(
            self.simbolo, self.inicial, self.final
        )

        for letra, prox_estado in self.regras.items():
            str += "({}, {}) ".format(letra, prox_estado)

        return str


class AjustesFuncoes:
    def __init__(self, endereco_arquivo):
        ajustes_variaveis = AjusteVariaveis(endereco_arquivo)
        self.variaveis = self.definirVariaveis(ajustes_variaveis.variaveis)
        self.funcoes = self.ajustarFuncoes(ajustes_variaveis.funcoes)
        self.var_inicial = ajustes_variaveis.var_inicial
        self.letras = ajustes_variaveis.letras

        self.estado_final = Variavel("Z")
        self.estado_final.final = True

        self.definirVariavelInicial()
        self.definirRegras()

    def definirVariaveis(self, simbolos):
        variaveis = []

        for simbolo in simbolos:
            variaveis.append(Variavel(simbolo))

        return variaveis

    def ajustarFuncoes(self, funcoes):
        matriz = []

        for funcao in funcoes:
            matriz.append(funcao.split("→"))

        return matriz

    def definirVariavelInicial(self):
        for var in self.variaveis:
            if var.simbolo == self.var_inicial:
                var.inicial = True
                break

    def definirRegras(self):
        for var in self.variaveis:
            for funcao in self.funcoes:
                if var.simbolo == funcao[0]:
                    self.ajustarRegra(var, funcao[1])

    def ajustarRegra(self, var, regra):
        if regra == "ε":
            var.final = True
        else:
            if regra[0] not in var.regras:
                if len(regra) == 1:
                    self.verificarNovoEstadoFinal()
                    var.regras[regra] = "Z"
                else:
                    var.regras[regra[0]] = regra[1]
            else:
                if len(regra) == 1:
                    self.verificarNovoEstadoFinal()
                    var.regras[regra] += "Z"
                else:
                    var.regras[regra[0]] += regra[1]

    def verificarNovoEstadoFinal(self):
        if not any(obj is self.estado_final for obj in self.variaveis):
            self.variaveis.append(self.estado_final)
