from AjustesFuncoes import Variavel as Estado
from GeradorNFA import GeradorNFA


class GeradorDFA:
    def __init__(self, endereco_arquivo):
        gerador_nfa = GeradorNFA(endereco_arquivo)
        self.estado_inicial = gerador_nfa.estado_inicial
        self.nfa_estados = gerador_nfa.estados
        self.estados = []
        self.letras = gerador_nfa.letras
        self.add_estado_novo = True
        self.add_estado_morto = False

        self.criarNovosEstados()
        self.gerarRotas()
        self.organizarEstadosMortos()

    def organizarEstadosMortos(self):
        for estado in self.estados:
            for letra in self.letras:

                if estado.regras[letra] == "":
                    estado.regras[letra] = "Ø"

    def criarNovosEstados(self):
        simbolos = []

        for estado in self.nfa_estados:
            if estado.simbolo not in simbolos:
                simbolos.append(estado.simbolo)

            for prox_estado in estado.regras.values():
                prox_estado = self.ordenarAlfabeticamente(prox_estado)

                if prox_estado not in simbolos:
                    simbolos.append(prox_estado)

        for simbolo in simbolos:
            self.estados.append(Estado(simbolo))

    def ordenarAlfabeticamente(self, estado):
        troca = True

        while troca:
            troca = False

            for i in range(len(estado) - 1):
                if estado[i] > estado[i + 1]:
                    copia = estado[i]
                    estado[i] = estado[i + 1]
                    estado[i + 1] = copia
                    troca = True

        return estado

    def gerarRotas(self):
        while self.add_estado_novo:
            self.add_estado_novo = False
            self.estados_novos = []

            for estado in self.estados:
                estados_eq = self.pegarEstadosEquivalentes(estado)

                for letra in self.letras:
                    estado.regras[letra] = ""

                    for estado_eq in estados_eq:
                        if letra not in estado_eq.regras:
                            estado.regras[letra] += "Ø"
                        else:
                            estado.regras[letra] += estado_eq.regras[letra]

                self.ajustarRegras(estado.regras)

            if self.add_estado_novo:
                self.estados_novos = list(set(self.estados_novos))

                for e in self.estados_novos:
                    self.estados.append(Estado(e))

    def pegarEstadosEquivalentes(self, estado):
        estados_eq = []

        for i in range(len(estado.simbolo)):
            for estado_nfa in self.nfa_estados:
                if (
                    estado.simbolo[i] == estado_nfa.simbolo
                    and estado_nfa not in estados_eq
                ):
                    estados_eq.append(estado_nfa)

        return estados_eq

    def ajustarRegras(self, regras):
        for letra in self.letras:
            if len(regras[letra]) > 1:
                regras[letra] = regras[letra].replace("Ø", "")

            regras[letra] = self.removerCaracteresRepetidos(regras[letra])
            regras[letra] = self.ordenarAlfabeticamente(regras[letra])

            if self.adicionarProximoEstado(regras[letra]):
                self.estados_novos.append(regras[letra])

    def adicionarProximoEstado(self, prox_estado):
        if prox_estado == "":
            return False

        for estado in self.estados:
            if prox_estado == estado.simbolo:
                return False

        self.add_estado_novo = True
        return True

    def removerCaracteresRepetidos(self, str):
        resultado = ""
        vistos = set()

        for char in str:
            if char not in vistos:
                resultado += char
                vistos.add(char)

        return resultado
