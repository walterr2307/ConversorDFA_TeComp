from Estado import Estado
from GerarArquivo import GerarArquivo


class GramToNFA:
    def __init__(self, endereco_arquivo):
        self.linhas = self.lerArquivo(endereco_arquivo)
        self.simbolos_estados = []
        self.estados = []
        self.alfabeto = []

        self.separarSimbolosAlfabeto()
        self.criarEstados()
        self.criarTransicoes()
        self.procurarEstado(self.linhas[0][-2]).inicial = True
        self.ordenarTranscicoes()

        GerarArquivo.instanciar().escreverArquivo(
            "NFA", self.estados, self.alfabeto, "# NFA Original"
        )

    def procurarEstado(self, simbolo):
        for estado in self.estados:
            if estado.simbolo == simbolo:
                return estado

    def lerArquivo(self, endereco_arquivo):
        with open(endereco_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = [linha.replace(" ", "").strip() for linha in arquivo.readlines()]

        return linhas

    def ordenarTranscicoes(self):
        for estado in self.estados:
            for letra, transicao in estado.transicoes.items():
                transicao = "".join(sorted(set(transicao)))
                estado.transicoes[letra] = transicao

    def criarEstadoFinal(self):
        estado = Estado("Z", self.alfabeto)
        estado.final = True
        return estado

    def separarSimbolosAlfabeto(self):
        for i in range(2, len(self.linhas)):
            lista = self.linhas[i].split("→")
            simbolo = lista[0]
            letra = lista[1][0]

            if simbolo not in self.simbolos_estados:
                self.simbolos_estados.append(simbolo)

            if letra != "ε" and letra not in self.alfabeto:
                self.alfabeto.append(letra)

        self.simbolos_estados = "".join(sorted(self.simbolos_estados))
        self.alfabeto = "".join(sorted(self.alfabeto))

    def criarEstados(self):
        for simbolo in self.simbolos_estados:
            self.estados.append(Estado(simbolo, self.alfabeto))

    def criarTransicoes(self):
        incluir_estado_final = False

        for i in range(2, len(self.linhas)):
            lista = self.linhas[i].split("→")
            transicao = lista[1]
            estado = self.procurarEstado(lista[0])

            if transicao == "ε":
                estado.final = True
            elif len(transicao) == 1:
                estado.transicoes[transicao] += "Z"
                incluir_estado_final = True
            else:
                estado.transicoes[transicao[0]] += transicao[1]

        if incluir_estado_final:
            self.estados.append(self.criarEstadoFinal())
