class GerarArquivo:
    instancia = None  # Atributo estático para implementar o padrão Singleton

    @staticmethod
    def instanciar():
        if GerarArquivo.instancia == None:
            GerarArquivo.instancia = (
                GerarArquivo()
            )  # Cria uma nova instância se ainda não existir
        return GerarArquivo.instancia  # Retorna a instância única

    def escreverArquivo(self, tipo_maquina, estados, alfabeto, nome_arquivo):
        self.tipo_maquina = tipo_maquina
        self.estados = estados
        self.alfabeto = alfabeto

        self.linhas = []  # Lista de linhas que serão escritas no arquivo
        self.linhas.append(nome_arquivo)  # Adiciona o título do arquivo
        self.linhas.append(self.colocarEstados())  # Adiciona os estados
        self.linhas.append(self.colocarAlfabeto())  # Adiciona o alfabeto

        self.colocarFuncoes()  # Adiciona as transições
        self.colocarIniciaisFinais()  # Adiciona os estados iniciais e finais
        self.abrirArquivo("Arquivos/" + nome_arquivo)  # Escreve no arquivo

    def colocarEstados(self):
        linha = "Q:"  # Prefixo da linha de estados

        for estado in self.estados:
            linha += " " + estado.simbolo  # Adiciona cada símbolo de estado

        return linha

    def colocarAlfabeto(self):
        linha = "Σ:"  # Prefixo da linha do alfabeto

        for letra in self.alfabeto:
            linha += " " + letra  # Adiciona cada letra do alfabeto

        return linha

    def colocarFuncoes(self):
        self.linhas.append("δ:")  # Prefixo das transições

        for estado in self.estados:
            for letra, transicao in estado.transicoes.items():
                if self.tipo_maquina == "NFA":
                    self.colocarFuncaoNFA(
                        estado, letra, transicao
                    )  # Para NFA, cada caractere pode ter múltiplos destinos
                elif self.tipo_maquina == "Reversed":
                    self.colocarFuncaoInversa(
                        estado, letra, transicao
                    )  # Para reversos, transições vêm como string separada por espaços
                else:
                    linha = estado.simbolo + ", " + letra + " → " + transicao
                    self.linhas.append(linha)  # DFA padrão

    def colocarFuncaoNFA(self, estado, letra, transicao):
        for caractere in transicao:
            self.linhas.append(
                estado.simbolo + ", " + letra + " → " + caractere
            )  # NFA: múltiplos destinos por letra

    def colocarFuncaoInversa(self, estado, letra, transicao):
        transicoes = transicao.split(" ")  # Divide as transições por espaço

        for i in range(
            len(transicoes) - 1
        ):  # Último elemento é string vazia, por isso -1
            self.linhas.append(
                estado.simbolo + ", " + letra + " → " + transicoes[i]
            )  # Adiciona cada transição individualmente

    def colocarIniciaisFinais(self):
        self.linhas.append("Iniciais:")  # Linha para estados iniciais
        self.linhas.append("Finais:")  # Linha para estados finais

        for estado in self.estados:
            if estado.inicial:
                self.linhas[-2] += " " + estado.simbolo  # Adiciona à linha de iniciais
            if estado.final:
                self.linhas[-1] += " " + estado.simbolo  # Adiciona à linha de finais

    def abrirArquivo(self, caminho):
        with open(caminho, "w", encoding="utf-8") as arquivo:
            for linha in self.linhas:
                arquivo.write(linha + "\n")  # Escreve cada linha no arquivo
