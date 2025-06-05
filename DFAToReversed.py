from Estado import Estado  # Importa a classe Estado
from GerarArquivo import GerarArquivo  # Importa a classe que escreve o arquivo de saída


class DFAToReversed:
    def __init__(self, dfa):
        self.alfabeto = dfa.alfabeto  # Salva o alfabeto do DFA
        self.estados = self.copiarEstados(
            dfa.estados
        )  # Copia os estados do DFA original
        self.novas_transcicoes = (
            self.gerarNovasTransicoes()
        )  # Cria estrutura para armazenar as transições invertidas
        self.trocarTransicoes()  # Inverte as transições
        self.inverterFinais()  # Troca os estados finais pelos iniciais e vice-versa

        # Escreve o DFA reverso no arquivo
        GerarArquivo.instanciar().escreverArquivo(
            "Reversed", self.estados, self.alfabeto, "# Reverse of DFA"
        )

    def copiarEstados(self, estados):
        novos_estados = []

        for estado in estados:
            novo_estado = Estado(
                estado.simbolo, self.alfabeto
            )  # Cria um novo estado com o mesmo símbolo
            novo_estado.inicial = estado.inicial  # Copia a marcação de inicial
            novo_estado.final = estado.final  # Copia a marcação de final
            novos_estados.append(novo_estado)

            # Copia as transições originais
            for letra, transicao in estado.transicoes.items():
                novo_estado.transicoes[letra] = transicao

        return novos_estados

    def gerarNovasTransicoes(self):
        novas_transicoes = []

        for _ in self.estados:
            novas_transicoes.append({})  # Cria um dicionário para cada estado

        for i in range(len(self.estados)):
            for letra in self.alfabeto:
                novas_transicoes[i][
                    letra
                ] = ""  # Inicializa as transições com strings vazias

        return novas_transicoes

    def trocarTransicoes(self):
        # Inverte as transições: destino vira origem
        for estado in self.estados:
            for i in range(len(self.estados)):
                for letra, transicao in estado.transicoes.items():
                    if self.estados[i].simbolo == transicao:
                        self.novas_transcicoes[i][letra] += (
                            estado.simbolo + " "
                        )  # Adiciona origem à nova transição

        # Atualiza os estados com as novas transições
        for i in range(len(self.estados)):
            for letra in self.alfabeto:
                self.estados[i].transicoes[letra] = self.novas_transcicoes[i][letra]

    def inverterFinais(self):
        # Inverte quais estados são finais e quais são iniciais
        for estado in self.estados:
            estado.inicial, estado.final = estado.final, estado.inicial
