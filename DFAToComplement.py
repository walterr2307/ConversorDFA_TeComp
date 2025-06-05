from Estado import Estado  # Importa a classe Estado (estrutura dos estados)
from GerarArquivo import (
    GerarArquivo,
)  # Importa a classe responsável por gerar arquivos de saída


class DFAToComplement:
    def __init__(self, dfa):
        self.alfabeto = dfa.alfabeto  # Copia o alfabeto do DFA original
        self.estados = self.copiarEstados(dfa.estados)  # Cria cópias dos estados
        self.inverterFinais()  # Inverte os estados finais para obter o complemento

        # Gera um arquivo com o DFA complementar
        GerarArquivo.instanciar().escreverArquivo(
            "DFA", self.estados, self.alfabeto, "# Complement of DFA"
        )

    def copiarEstados(self, estados):
        novos_estados = []

        for estado in estados:
            # Cria um novo estado com o mesmo símbolo e alfabeto
            novo_estado = Estado(estado.simbolo, self.alfabeto)
            novo_estado.inicial = estado.inicial  # Copia a marcação de estado inicial
            novo_estado.final = estado.final  # Copia a marcação de estado final
            novos_estados.append(novo_estado)

            # Copia as transições do estado original
            for letra, transicao in estado.transicoes.items():
                novo_estado.transicoes[letra] = transicao

        return novos_estados

    def inverterFinais(self):
        for estado in self.estados:
            estado.final = (
                not estado.final
            )  # Inverte a marcação: final vira não-final e vice-versa
