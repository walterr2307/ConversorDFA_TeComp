class AjusteVariaveis:  # Define uma classe chamada AjusteVariaveis
    def __init__(
        self, endereco_arquivo
    ):  # Método construtor, recebe o caminho do arquivo
        gram = self.definirGramatica(
            endereco_arquivo
        )  # Lê e processa o arquivo para obter a gramática
        lista = self.retornarLista(gram)  # Extrai uma lista com base na gramática
        self.variaveis = self.retornarAtributos(
            lista
        )  # Armazena atributos em self.variaveis
        self.letras = self.retornarAtributos(
            lista
        )  # Armazena novamente os atributos em self.letras (possível redundância)

    def definirGramatica(
        self, endereco_arquivo
    ):  # Lê o conteúdo do arquivo e remove espaços em branco e quebras de linha
        with open(endereco_arquivo, "r", encoding="utf-8") as f:
            gram = [linha.strip().replace(" ", "") for linha in f.readlines()]

        return gram  # Retorna a lista de linhas processadas

    def retornarLista(self, gram):  # Extrai e trata a primeira linha da gramática
        lista = gram[0].split(
            ","
        )  # Divide a linha inicial em uma lista, separando por vírgulas

        self.var_inicial = lista[-1][
            0
        ]  # Armazena o primeiro caractere do último item como var_inicial
        self.funcoes = gram[2:]  # Armazena as linhas a partir da terceira como funções

        del lista[-2:]  # Remove os dois últimos elementos da lista
        return lista  # Retorna a lista modificada

    def retornarAtributos(self, lista):  # Extrai atributos de uma lista de strings
        atributos = []  # Inicializa a lista de atributos

        if lista[0][-1] == "}":  # Caso especial: se o primeiro item termina com }
            atributo = lista[0][-2]  # Pega o penúltimo caractere como atributo
            del lista[0]  # Remove o item da lista
            return atributo  # Retorna o atributo único

        atributos.append(lista[0][-1])  # Adiciona o último caractere do primeiro item
        del lista[0]  # Remove o item da lista

        while True:  # Loop para extrair mais atributos
            atributos.append(
                lista[0][0]
            )  # Adiciona o primeiro caractere do próximo item
            parar = lista[0][-1] == "}"  # Verifica se o item termina com }
            del [lista[0]]  # Remove o item da lista

            if parar:  # Se encontrou }, encerra o loop
                break

        return atributos  # Retorna a lista de atributos
