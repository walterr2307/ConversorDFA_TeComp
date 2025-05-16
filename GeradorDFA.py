from AjustesFuncoes import (
    Variavel as Estado,
)  # Importa a classe Variavel renomeando para Estado
from GeradorNFA import GeradorNFA  # Importa a classe GeradorNFA


class GeradorDFA:  # Classe responsável por converter um AFN em AFD
    def __init__(self, endereco_arquivo):  # Construtor
        gerador_nfa = GeradorNFA(endereco_arquivo)  # Gera o NFA a partir do arquivo
        self.estado_inicial = gerador_nfa.estado_inicial  # Estado inicial
        self.nfa_estados = gerador_nfa.estados  # Lista de estados do NFA
        self.estados = []  # Estados do DFA
        self.letras = gerador_nfa.letras  # Alfabeto
        self.add_estado_novo = (
            True  # Flag para saber se há novos estados para processar
        )
        self.add_estado_morto = False  # Flag para adicionar estado morto (Ø)

        self.criarNovosEstados()  # Cria os estados compostos do DFA
        self.gerarRotas()  # Gera as transições do DFA
        self.organizarEstadosMortos()  # Insere transições para estado morto quando necessário

    def organizarEstadosMortos(self):  # Preenche regras vazias com transição para Ø
        for estado in self.estados:
            for letra in self.letras:
                if estado.regras[letra] == "":
                    estado.regras[letra] = "Ø"

    def criarNovosEstados(
        self,
    ):  # Cria os estados do DFA a partir da combinação de estados do NFA
        simbolos = []

        for estado in self.nfa_estados:
            if estado.simbolo not in simbolos:
                simbolos.append(estado.simbolo)

            for prox_estado in estado.regras.values():
                prox_estado = self.ordenarAlfabeticamente(prox_estado)
                if prox_estado not in simbolos:
                    simbolos.append(prox_estado)

        for simbolo in simbolos:
            self.estados.append(Estado(simbolo))  # Cria novo estado do DFA

    def ordenarAlfabeticamente(
        self, estado
    ):  # Ordena os caracteres do nome do estado em ordem alfabética
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

    def gerarRotas(self):  # Gera as regras de transição dos estados do DFA
        while self.add_estado_novo:  # Enquanto houver estados novos a serem processados
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

            if self.add_estado_novo:  # Se novos estados foram identificados
                self.estados_novos = list(set(self.estados_novos))  # Remove duplicatas
                for e in self.estados_novos:
                    self.estados.append(Estado(e))  # Adiciona os novos estados

    def pegarEstadosEquivalentes(
        self, estado
    ):  # Retorna os estados do NFA contidos no estado composto
        estados_eq = []

        for i in range(len(estado.simbolo)):
            for estado_nfa in self.nfa_estados:
                if (
                    estado.simbolo[i] == estado_nfa.simbolo
                    and estado_nfa not in estados_eq
                ):
                    estados_eq.append(estado_nfa)

        return estados_eq

    def ajustarRegras(
        self, regras
    ):  # Ajusta as transições do estado: remove repetições, ordena, verifica novos
        for letra in self.letras:
            if len(regras[letra]) > 1:
                regras[letra] = regras[letra].replace("Ø", "")

            regras[letra] = self.removerCaracteresRepetidos(regras[letra])
            regras[letra] = self.ordenarAlfabeticamente(regras[letra])

            if self.adicionarProximoEstado(regras[letra]):
                self.estados_novos.append(regras[letra])

    def adicionarProximoEstado(
        self, prox_estado
    ):  # Verifica se o estado já foi adicionado
        if prox_estado == "":
            return False

        for estado in self.estados:
            if prox_estado == estado.simbolo:
                return False

        self.add_estado_novo = True
        return True

    def removerCaracteresRepetidos(
        self, str
    ):  # Remove caracteres repetidos do nome do estado composto
        resultado = ""
        vistos = set()

        for char in str:
            if char not in vistos:
                resultado += char
                vistos.add(char)

        return resultado
