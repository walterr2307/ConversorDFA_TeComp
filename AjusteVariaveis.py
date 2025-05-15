class AjusteVariaveis:
    def __init__(self, endereco_arquivo):
        gram = self.definirGramatica(endereco_arquivo)
        lista = self.retornarLista(gram)
        self.variaveis = self.retornarAtributos(lista)
        self.letras = self.retornarAtributos(lista)

    def definirGramatica(self, endereco_arquivo):
        with open(endereco_arquivo, "r", encoding="utf-8") as f:
            gram = [linha.strip().replace(" ", "") for linha in f.readlines()]

        return gram

    def retornarLista(self, gram):
        lista = gram[0].split(",")

        self.var_inicial = lista[-1][0]
        self.funcoes = gram[2:]

        del lista[-2:]
        return lista

    def retornarAtributos(self, lista):
        atributos = []

        if lista[0][-1] == "}":
            atributo = lista[0][-2]
            del lista[0]
            return atributo

        atributos.append(lista[0][-1])
        del lista[0]

        while True:
            atributos.append(lista[0][0])
            parar = lista[0][-1] == "}"
            del [lista[0]]

            if parar:
                break

        return atributos
