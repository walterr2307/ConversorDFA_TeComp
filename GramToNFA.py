from Estado import Estado  # Importa a classe Estado de outro módulo
from GerarArquivo import GerarArquivo  # Importa a classe GerarArquivo para gerar saídas


class GramToNFA:
    def __init__(self, endereco_arquivo):
        # Lê o conteúdo do arquivo especificado
        self.linhas = self.lerArquivo(endereco_arquivo)
        # Inicializa listas para armazenar os símbolos de estados, objetos Estado e o alfabeto
        self.simbolos_estados = []
        self.estados = []
        self.alfabeto = []

        # Processa os símbolos e o alfabeto a partir das regras
        self.separarSimbolosAlfabeto()
        # Cria os estados com base nos símbolos identificados
        self.criarEstados()
        # Define as transições entre os estados
        self.criarTransicoes()
        # Marca o estado inicial com base na primeira regra
        self.procurarEstado(self.linhas[0][-2]).inicial = True
        # Organiza as transições (remove duplicatas e ordena)
        self.ordenarTranscicoes()

        # Gera o arquivo com a NFA resultante
        GerarArquivo.instanciar().escreverArquivo(
            "NFA", self.estados, self.alfabeto, "# NFA Original"
        )

    def procurarEstado(self, simbolo):
        # Busca um estado pelo símbolo
        for estado in self.estados:
            if estado.simbolo == simbolo:
                return estado

    def lerArquivo(self, endereco_arquivo):
        # Lê o arquivo e remove espaços em branco e quebras de linha
        with open(endereco_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = [linha.replace(" ", "").strip() for linha in arquivo.readlines()]

        return linhas

    def ordenarTranscicoes(self):
        # Ordena as transições de cada estado (sem duplicatas)
        for estado in self.estados:
            for letra, transicao in estado.transicoes.items():
                transicao = "".join(sorted(set(transicao)))
                estado.transicoes[letra] = transicao

    def criarEstadoFinal(self):
        # Cria um estado final adicional chamado 'Z'
        estado = Estado("Z", self.alfabeto)
        estado.final = True
        return estado

    def separarSimbolosAlfabeto(self):
        # Separa os símbolos dos estados e letras do alfabeto a partir das regras
        for i in range(2, len(self.linhas)):
            lista = self.linhas[i].split("→")
            simbolo = lista[0]
            letra = lista[1][0]

            if simbolo not in self.simbolos_estados:
                self.simbolos_estados.append(simbolo)

            if letra != "ε" and letra not in self.alfabeto:
                self.alfabeto.append(letra)

        # Ordena os símbolos e o alfabeto
        self.simbolos_estados = "".join(sorted(self.simbolos_estados))
        self.alfabeto = "".join(sorted(self.alfabeto))

    def criarEstados(self):
        # Cria objetos Estado para cada símbolo identificado
        for simbolo in self.simbolos_estados:
            self.estados.append(Estado(simbolo, self.alfabeto))

    def criarTransicoes(self):
        incluir_estado_final = (
            False  # Flag para saber se o estado final 'Z' deve ser incluído
        )

        for i in range(2, len(self.linhas)):
            lista = self.linhas[i].split("→")
            transicao = lista[1]
            estado = self.procurarEstado(lista[0])

            if transicao == "ε":
                estado.final = (
                    True  # Marca o estado como final se for uma transição vazia
                )
            elif len(transicao) == 1:
                estado.transicoes[
                    transicao
                ] += "Z"  # Adiciona transição para o estado final
                incluir_estado_final = True
            else:
                estado.transicoes[transicao[0]] += transicao[
                    1
                ]  # Transição comum (letra + próximo estado)

        if incluir_estado_final:
            # Adiciona o estado final 'Z' ao conjunto de estados
            self.estados.append(self.criarEstadoFinal())
