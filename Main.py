from DFAToComplement import DFAToComplement as Complement
from DFAToReversed import DFAToReversed as Reversed
from NFAToDFA import NFAToDFA as DFA


class Main:
    def __init__(self, endereco_arquivo):
        dfa = DFA(endereco_arquivo)
        Complement(dfa)
        Reversed(dfa)

        self.estados = dfa.estados
        self.alfabeto = dfa.alfabeto
        self.palavra = input("Digite a palavra: ")
        self.palavra_valida = self.verificarPalavraValida()

        print(self.imprimirInformacoes())

    def verificarPalavraValida(self):
        estado_atual = None

        for estado in self.estados:
            if estado.inicial:
                estado_atual = estado
                break

        for letra in self.palavra:
            if letra in self.alfabeto:
                estado_atual = self.procurarEstado(estado_atual.transicoes[letra])
            else:
                return False

        return estado_atual.final

    def procurarEstado(self, simbolo):
        for estado in self.estados:
            if estado.simbolo == simbolo:
                return estado

        return None

    def imprimirInformacoes(self):
        str = "Palavra: {}\n".format(self.palavra)
        str += "Aceita: {}\n".format(self.palavra_valida)
        str += "Arquivos gerados: NFA Original, DFA Original"
        str += ", Complement of DFA, Reverse of DFA\n"

        return str


Main("Gramáticas/Gramática 5.txt")
