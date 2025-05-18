class GerarArquivo:
    instancia = None

    @staticmethod
    def instanciar():
        if GerarArquivo.instancia == None:
            GerarArquivo.instancia = GerarArquivo()

        return GerarArquivo.instancia

    def escreverArquivo(self, tipo_maquina, estados, alfabeto, nome_arquivo):
        self.tipo_maquina = tipo_maquina
        self.estados = estados
        self.alfabeto = alfabeto

        self.linhas = []
        self.linhas.append(nome_arquivo)
        self.linhas.append(self.colocarEstados())
        self.linhas.append(self.colocarAlfabeto())

        self.colocarFuncoes()
        self.colocarIniciaisFinais()
        self.abrirArquivo("Arquivos/" + nome_arquivo)

    def colocarEstados(self):
        linha = "Q:"

        for estado in self.estados:
            linha += " " + estado.simbolo

        return linha

    def colocarAlfabeto(self):
        linha = "Σ:"

        for letra in self.alfabeto:
            linha += " " + letra

        return linha

    def colocarFuncoes(self):
        self.linhas.append("δ:")

        for estado in self.estados:
            for letra, transicao in estado.transicoes.items():
                if self.tipo_maquina == "NFA":
                    self.colocarFuncaoNFA(estado, letra, transicao)
                elif self.tipo_maquina == "Reversed":
                    self.colocarFuncaoInversa(estado, letra, transicao)
                else:
                    linha = estado.simbolo + ", " + letra + " → " + transicao
                    self.linhas.append(linha)

    def colocarFuncaoNFA(self, estado, letra, transicao):
        for caractere in transicao:
            self.linhas.append(estado.simbolo + ", " + letra + " → " + caractere)

    def colocarFuncaoInversa(self, estado, letra, transicao):
        transicoes = transicao.split(" ")

        for i in range(len(transicoes) - 1):
            self.linhas.append(estado.simbolo + ", " + letra + " → " + transicoes[i])

    def colocarIniciaisFinais(self):
        self.linhas.append("Iniciais:")
        self.linhas.append("Finais:")

        for estado in self.estados:
            if estado.inicial:
                self.linhas[-2] += " " + estado.simbolo
            if estado.final:
                self.linhas[-1] += " " + estado.simbolo

    def abrirArquivo(self, caminho):
        with open(caminho, "w", encoding="utf-8") as arquivo:
            for linha in self.linhas:
                arquivo.write(linha + "\n")
