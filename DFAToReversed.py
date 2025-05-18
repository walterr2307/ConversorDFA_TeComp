from Estado import Estado
from GerarArquivo import GerarArquivo


class DFAToReversed:
    def __init__(self, dfa):
        self.alfabeto = dfa.alfabeto
        self.estados = self.copiarEstados(dfa.estados)
        self.novas_transcicoes = self.gerarNovasTransicoes()
        self.trocarTransicoes()
        self.inverterFinais()
        
        GerarArquivo.instanciar().escreverArquivo(
            "Reversed", self.estados, self.alfabeto, "# Reverse of DFA"
        )

    def copiarEstados(self, estados):
        novos_estados = []

        for estado in estados:
            novo_estado = Estado(estado.simbolo, self.alfabeto)
            novo_estado.inicial = estado.inicial
            novo_estado.final = estado.final
            novos_estados.append(novo_estado)

            for letra, transicao in estado.transicoes.items():
                novo_estado.transicoes[letra] = transicao

        return novos_estados

    def gerarNovasTransicoes(self):
        novas_transicoes = []

        for _ in self.estados:
            novas_transicoes.append({})

        for i in range(len(self.estados)):
            for letra in self.alfabeto:
                novas_transicoes[i][letra] = ""

        return novas_transicoes

    def trocarTransicoes(self):
        for estado in self.estados:
            for i in range(len(self.estados)):
                for letra, transicao in estado.transicoes.items():

                    if self.estados[i].simbolo == transicao:
                        self.novas_transcicoes[i][letra] += estado.simbolo + " "

        for i in range(len(self.estados)):
            for letra in self.alfabeto:
                self.estados[i].transicoes[letra] = self.novas_transcicoes[i][letra]

    def inverterFinais(self):
        for estado in self.estados:
            estado.inicial, estado.final = estado.final, estado.inicial
