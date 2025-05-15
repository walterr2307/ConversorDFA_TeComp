from ArquivoDFA import ArquivoDFA


class ComplementoDFA:
    def __init__(self, endereco_arquivo):
        arquivo_dfa = ArquivoDFA(endereco_arquivo)
        self.estados = arquivo_dfa.estados
        self.letras = arquivo_dfa.letras
        self.estado_inicial = arquivo_dfa.estado_inicial
        self.linhas = self.ajustarArquivo()
        self.trocarFinalInicial()
        self.colocarFuncoes()
        
        with open("AFD Complementado.txt", "w", encoding="utf-8") as arquivo:
            for linha in self.linhas:
                arquivo.write(linha + "\n")

    def trocarFinalInicial(self):
        for estado in self.estados:
            if estado.final:
                estado.final = False
            else:
                estado.final = True

    def ajustarArquivo(self):
        linhas = []
        linhas.append("# AFD Complementado")
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

    def colocarVirgula(self, linha, caracteres):
        colocar_virgula = False

        for caractere in caracteres:
            if colocar_virgula:
                linha += ", " + caractere
            else:
                linha += caractere
                colocar_virgula = True

        return linha


ComplementoDFA("gramatica1.txt")
