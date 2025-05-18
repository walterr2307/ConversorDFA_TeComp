from Estado import Estado
from GramToNFA import GramToNFA
from GerarArquivo import GerarArquivo


class NFAToDFA:
    def __init__(self, endereco_arquivo):
        gram_nfa = GramToNFA(endereco_arquivo)
        self.alfabeto = gram_nfa.alfabeto
        self.estados = gram_nfa.estados
        self.novos_simbolos = []
        self.criarEstadosNovos()
        self.verificarEspacosVazios()
        
        GerarArquivo.instanciar().escreverArquivo(
            "DFA", self.estados, self.alfabeto, "# DFA Original"
        )

    def criarEstadoMorto(self):
        estado = Estado("∅", self.alfabeto)

        for letra in estado.transicoes:
            estado.transicoes[letra] = "∅"

        return estado

    def verificarEspacosVazios(self):
        criar_estado_morto = False

        for estado in self.estados:
            for letra, transicao in estado.transicoes.items():
                if transicao == "":
                    estado.transicoes[letra] = "∅"
                    criar_estado_morto = True

        self.estados.sort(key=lambda estado: (len(estado.simbolo), estado.simbolo))

        if criar_estado_morto:
            self.estados.append(self.criarEstadoMorto())

    def ordenarTranscicoes(self):
        for estado in self.estados:
            for letra, transicao in estado.transicoes.items():
                transicao = "".join(sorted(set(transicao)))
                estado.transicoes[letra] = transicao

    def criarSimbolosNovos(self):
        novos_simbolos = []

        for estado in self.estados:
            for transicao in estado.transicoes.values():
                if len(transicao) > 1 and transicao not in self.novos_simbolos:
                    self.novos_simbolos.append(transicao)
                    novos_simbolos.append(transicao)

        return novos_simbolos

    def criarNovasTransicoes(self, novos_simbolos):
        for novo_simbolo in novos_simbolos:
            novo_estado = Estado(novo_simbolo, self.alfabeto)
            self.estados.append(novo_estado)

            for estado in self.estados:
                if self.verificarEquivalencia(novo_simbolo, estado.simbolo):
                    for letra in self.alfabeto:
                        novo_estado.transicoes[letra] += estado.transicoes[letra]

                    if estado.final:
                        novo_estado.final = True

        self.ordenarTranscicoes()

    def verificarEquivalencia(self, novo_simbolo, simbolo):
        for i in range(len(novo_simbolo)):
            if novo_simbolo[i] == simbolo:
                return True

        return False

    def criarEstadosNovos(self):
        while True:
            novos_simbolos = self.criarSimbolosNovos()

            if len(novos_simbolos) == 0:
                break

            self.criarNovasTransicoes(novos_simbolos)
