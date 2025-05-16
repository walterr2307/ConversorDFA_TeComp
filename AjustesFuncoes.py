from AjusteVariaveis import (
    AjusteVariaveis,
)  # Importa a classe AjusteVariaveis de outro módulo


class Variavel:  # Classe que representa uma variável (ou estado)
    def __init__(self, simbolo):  # Construtor que recebe um símbolo
        self.simbolo = simbolo  # Símbolo da variável
        self.inicial = False  # Define se a variável é o estado inicial
        self.final = False  # Define se a variável é um estado final
        self.regras = {}  # Dicionário para armazenar as regras de transição

    def __str__(self):  # Representação em string da variável
        str = "{}, inicial: {}, final: {} > ".format(
            self.simbolo, self.inicial, self.final
        )

        for letra, prox_estado in self.regras.items():  # Percorre as regras da variável
            str += "({}, {}) ".format(letra, prox_estado)

        str += "\n"
        return str  # Retorna a string formatada


class AjustesFuncoes:  # Classe para montar o autômato com base nas funções/gramática
    def __init__(self, endereco_arquivo):  # Construtor que recebe o caminho do arquivo
        ajustes_variaveis = AjusteVariaveis(
            endereco_arquivo
        )  # Instancia AjusteVariaveis
        self.variaveis = self.definirVariaveis(
            ajustes_variaveis.variaveis
        )  # Cria os objetos Variavel
        self.funcoes = self.ajustarFuncoes(
            ajustes_variaveis.funcoes
        )  # Processa as funções de transição
        self.var_inicial = (
            ajustes_variaveis.var_inicial
        )  # Salva o símbolo da variável inicial
        self.letras = ajustes_variaveis.letras  # Salva os símbolos dos terminais

        self.estado_final = Variavel("Z")  # Cria o estado final especial "Z"
        self.estado_final.final = True  # Marca esse estado como final

        self.definirVariavelInicial()  # Define qual variável é inicial
        self.definirRegras()  # Aplica as regras de transição

    def definirVariaveis(self, simbolos):  # Cria objetos Variavel para cada símbolo
        variaveis = []

        for simbolo in simbolos:
            variaveis.append(Variavel(simbolo))

        return variaveis  # Retorna a lista de variáveis

    def ajustarFuncoes(self, funcoes):  # Separa as funções com base no símbolo "→"
        matriz = []

        for funcao in funcoes:
            matriz.append(funcao.split("→"))  # Divide em duas partes: origem e regra

        return matriz  # Retorna a lista de regras processadas

    def definirVariavelInicial(self):  # Marca a variável inicial
        for var in self.variaveis:
            if var.simbolo == self.var_inicial:  # Compara o símbolo
                var.inicial = True  # Marca como inicial
                break

    def definirRegras(self):  # Associa regras às variáveis
        for var in self.variaveis:
            for funcao in self.funcoes:
                if var.simbolo == funcao[0]:  # Se a variável for a origem da regra
                    self.ajustarRegra(var, funcao[1])  # Aplica a regra

    def ajustarRegra(self, var, regra):  # Aplica a regra à variável
        if regra == "ε":  # Se a regra for uma transição vazia
            var.final = True  # Marca a variável como final
        else:
            if regra[0] not in var.regras:  # Se a letra não está nas regras ainda
                if len(regra) == 1:  # Se só há um símbolo
                    self.verificarNovoEstadoFinal()  # Garante que "Z" está na lista
                    var.regras[regra] = "Z"  # Transição para o estado final
                else:
                    var.regras[regra[0]] = regra[
                        1
                    ]  # Transição comum: letra → próxima variável
            else:
                if len(regra) == 1:
                    self.verificarNovoEstadoFinal()
                    var.regras[regra] += "Z"  # Adiciona mais uma transição para "Z"
                else:
                    var.regras[regra[0]] += regra[
                        1
                    ]  # Acrescenta mais um destino para a letra

    def verificarNovoEstadoFinal(
        self,
    ):  # Verifica se o estado final "Z" já está nas variáveis
        if not any(obj is self.estado_final for obj in self.variaveis):
            self.variaveis.append(
                self.estado_final
            )  # Adiciona "Z" se ainda não estiver presente
