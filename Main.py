from DFAToComplement import (
    DFAToComplement,
)  # Importa a classe que gera o complemento de um DFA
from DFAToReversed import DFAToReversed  # Importa a classe que gera o reverso de um DFA
from NFAToDFA import NFAToDFA  # Importa a classe que converte NFA em DFA


class Main:
    def __init__(self, endereco_arquivo):
        dfa = NFAToDFA(endereco_arquivo)  # Constrói o DFA a partir de uma gramática
        DFAToComplement(dfa)  # Gera o complemento do DFA
        DFAToReversed(dfa)  # Gera o reverso do DFA

        self.estados = dfa.estados  # Armazena os estados do DFA
        self.alfabeto = dfa.alfabeto  # Armazena o alfabeto do DFA
        self.palavra = input("Digite a palavra: ")  # Recebe a palavra do usuário
        self.palavra_valida = (
            self.verificarPalavraValida()
        )  # Verifica se a palavra é aceita pelo DFA

        print(self.imprimirInformacoes())  # Exibe as informações no terminal

    def verificarPalavraValida(self):
        estado_atual = None

        for estado in self.estados:
            if estado.inicial:  # Encontra o estado inicial
                estado_atual = estado
                break

        for letra in self.palavra:
            if letra in self.alfabeto:  # Verifica se a letra pertence ao alfabeto
                estado_atual = self.procurarEstado(
                    estado_atual.transicoes[letra]
                )  # Caminha para o próximo estado
            else:
                return False  # Letra inválida no alfabeto

        return estado_atual.final  # Verifica se o último estado é final

    def procurarEstado(self, simbolo):
        for estado in self.estados:
            if estado.simbolo == simbolo:  # Busca o estado pelo seu símbolo
                return estado

        return None

    def imprimirInformacoes(self):
        str = "Palavra: {}\n".format(self.palavra)
        str += "Aceita: {}\n".format(self.palavra_valida)
        str += "Arquivos gerados: NFA Original, DFA Original"
        str += ", Complement of DFA, Reverse of DFA\n"

        return str


Main("Gramáticas/Gramática 5.txt")  # Executa o programa com a gramática especificada
