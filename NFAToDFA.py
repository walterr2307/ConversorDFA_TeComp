from Estado import Estado
from GramToNFA import GramToNFA
from GerarArquivo import GerarArquivo


class NFAToDFA:
    def __init__(self, endereco_arquivo):
        gram_nfa = GramToNFA(endereco_arquivo)  # Converte a gramática em um NFA
        self.alfabeto = gram_nfa.alfabeto  # Alfabeto usado na gramática
        self.estados = gram_nfa.estados  # Estados gerados a partir da gramática
        self.novos_simbolos = (
            []
        )  # Lista para armazenar novos símbolos compostos (conjuntos de estados)
        self.criarEstadosNovos()  # Cria os novos estados compostos (conversão NFA → DFA)
        self.verificarEspacosVazios()  # Verifica transições vazias e adiciona estado morto se necessário

        GerarArquivo.instanciar().escreverArquivo(
            "DFA", self.estados, self.alfabeto, "# DFA Original"  # Salva o DFA gerado
        )

    def criarEstadoMorto(self):
        estado = Estado("∅", self.alfabeto)  # Cria um estado "morto" (sem saída útil)

        for letra in estado.transicoes:
            estado.transicoes[letra] = (
                "∅"  # Todas as transições do estado morto vão para ele mesmo
            )

        return estado

    def verificarEspacosVazios(self):
        criar_estado_morto = False

        for estado in self.estados:
            for letra, transicao in estado.transicoes.items():
                if transicao == "":
                    estado.transicoes[letra] = (
                        "∅"  # Se a transição está vazia, aponta para o estado morto
                    )
                    criar_estado_morto = True

        self.estados.sort(
            key=lambda estado: (len(estado.simbolo), estado.simbolo)
        )  # Ordena os estados por tamanho do nome e ordem alfabética

        if criar_estado_morto:
            self.estados.append(
                self.criarEstadoMorto()
            )  # Adiciona o estado morto se foi necessário

    def ordenarTranscicoes(self):
        for estado in self.estados:
            for letra, transicao in estado.transicoes.items():
                transicao = "".join(
                    sorted(set(transicao))
                )  # Ordena e remove repetições nas transições
                estado.transicoes[letra] = transicao

    def criarSimbolosNovos(self):
        novos_simbolos = []

        for estado in self.estados:
            for transicao in estado.transicoes.values():
                if len(transicao) > 1 and transicao not in self.novos_simbolos:
                    self.novos_simbolos.append(
                        transicao
                    )  # Armazena símbolo composto não visto antes
                    novos_simbolos.append(transicao)

        return novos_simbolos

    def criarNovasTransicoes(self, novos_simbolos):
        for novo_simbolo in novos_simbolos:
            novo_estado = Estado(
                novo_simbolo, self.alfabeto
            )  # Cria novo estado a partir de símbolo composto
            self.estados.append(novo_estado)

            for estado in self.estados:
                if self.verificarEquivalencia(novo_simbolo, estado.simbolo):
                    for letra in self.alfabeto:
                        novo_estado.transicoes[letra] += estado.transicoes[
                            letra
                        ]  # Concatena transições equivalentes

                    if estado.final:
                        novo_estado.final = True  # Marca como final se algum estado componente for final

        self.ordenarTranscicoes()  # Ordena as transições após criação dos novos estados

    def verificarEquivalencia(self, novo_simbolo, simbolo):
        for i in range(len(novo_simbolo)):
            if novo_simbolo[i] == simbolo:
                return True  # Verifica se um estado está contido no novo símbolo (composição)

        return False

    def criarEstadosNovos(self):
        while True:
            novos_simbolos = (
                self.criarSimbolosNovos()
            )  # Busca por novos estados compostos

            if len(novos_simbolos) == 0:
                break  # Interrompe quando não há mais novos símbolos

            self.criarNovasTransicoes(
                novos_simbolos
            )  # Gera estados e transições para os novos símbolos
