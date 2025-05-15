from AjustesFuncoes import AjustesFuncoes


class GeradorNFA:
    def __init__(self, endereco_arquivo):
        ajustes_funcoes = AjustesFuncoes(endereco_arquivo)
        self.estados = ajustes_funcoes.variaveis
        self.estado_inicial = ajustes_funcoes.var_inicial
        self.letras = ajustes_funcoes.letras
        self.linhas = self.ajustarArquivo()
        self.colocarFuncoes()

        with open("AFN Original.txt", "w", encoding="utf-8") as arquivo:
            for linha in self.linhas:
                arquivo.write(linha + "\n")

    def ajustarArquivo(self):
        linhas = []
        linhas.append("# AFN Original")
        linhas.append("Q: ")
        linhas.append("Σ: ")
        linhas.append("δ: ")

        linhas[1] = self.colocarVirgula(linhas[1], [e.simbolo for e in self.estados])
        linhas[2] = self.colocarVirgula(linhas[2], self.letras)

        return linhas

    def colocarVirgula(self, linha, caracteres):
        colocar_virgula = False

        for caractere in caracteres:
            if colocar_virgula:
                linha += ", " + caractere
            else:
                linha += caractere
                colocar_virgula = True

        return linha

    def colocarFuncoes(self):
        for estado in self.estados:
            for letra, prox_estado in estado.regras.items():
                for i in range(len(prox_estado)):
                    texto = "{}, {} → {}".format(estado.simbolo, letra, prox_estado[i])
                    self.linhas.append(texto)

        self.linhas.append("Inicial: " + self.estado_inicial)
        self.linhas.append("Final(s): ")

        self.linhas[-1] = self.colocarVirgula(
            self.linhas[-1], [estado.simbolo for estado in self.estados if estado.final]
        )
