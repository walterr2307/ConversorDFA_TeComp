from GeradorDFA import GeradorDFA


class ArquivoDFA:
    def __init__(self, endereco_arquivo):
        gerador_dfa = GeradorDFA(endereco_arquivo)
        self.estado_inicial = gerador_dfa.estado_inicial
        self.estados = sorted(gerador_dfa.estados, key=lambda estado: estado.simbolo)
        self.letras = gerador_dfa.letras
        self.definirIniciaisFinais(gerador_dfa.nfa_estados)
        self.linhas = self.ajustarArquivo()
        self.colocarFuncoes()

        with open("AFD Original.txt", "w", encoding="utf-8") as arquivo:
            for linha in self.linhas:
                arquivo.write(linha + "\n")

    def definirIniciaisFinais(self, nfa_estados):
        unitarios = nfa_estados
        n_unitarios = []

        for i in range(len(self.estados) - 1):
            if len(self.estados[i].simbolo) > 1:
                n_unitarios.append(self.estados[i])

        for u in unitarios:
            for n in n_unitarios:
                for i in range(len(n.simbolo)):
                    if n.simbolo[i] == u.simbolo and u.final:
                        n.final = True

            for estado in self.estados:
                if estado.simbolo == u.simbolo and u.inicial:
                    estado.inicial = True
                if estado.simbolo == u.simbolo and u.final:
                    estado.final = True

    def colocarVirgula(self, linha, caracteres):
        colocar_virgula = False

        for caractere in caracteres:
            if colocar_virgula:
                linha += ", " + caractere
            else:
                linha += caractere
                colocar_virgula = True

        return linha

    def ajustarArquivo(self):
        linhas = []
        linhas.append("# AFD Original")
        linhas.append("Q: ")
        linhas.append("Σ: ")
        linhas.append("δ: ")

        linhas[1] = self.colocarVirgula(linhas[1], [e.simbolo for e in self.estados])
        linhas[2] = self.colocarVirgula(linhas[2], self.letras)

        return linhas

    def colocarFuncoes(self):
        for estado in self.estados:
            for letra, prox_estado in estado.regras.items():
                texto = "{}, {} → {}".format(estado.simbolo, letra, prox_estado)
                self.linhas.append(texto)

        self.linhas.append("Inicial: " + self.estado_inicial)
        self.linhas.append("Final(s): ")

        self.linhas[-1] = self.colocarVirgula(
            self.linhas[-1], [estado.simbolo for estado in self.estados if estado.final]
        )


ArquivoDFA("gramatica1.txt")
