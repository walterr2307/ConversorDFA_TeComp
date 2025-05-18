from Estado import Estado
from GerarArquivo import GerarArquivo


class DFAToComplement:
    def __init__(self, dfa):
        self.alfabeto = dfa.alfabeto
        self.estados = self.copiarEstados(dfa.estados)
        self.inverterFinais()

        GerarArquivo.instanciar().escreverArquivo(
            "DFA", self.estados, self.alfabeto, "# Complement of DFA"
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

    def inverterFinais(self):
        for estado in self.estados:
            estado.final = not estado.final
