from ComplementoDFA import ComplementoDFA  # Importa a classe para gerar o complemento do AFD
from InversoDFA import InversoDFA  # Importa a classe para gerar o inverso do AFD
from ArquivoDFA import ArquivoDFA  # Importa a classe para manipular o AFD original

class Main:
    def __init__(self, endereco_arquivo):
        arq_dfa = ArquivoDFA(endereco_arquivo)
        ComplementoDFA(arq_dfa)  # Gera o AFD complementado a partir do arquivo
        InversoDFA(arq_dfa)  # Gera o AFD invertido a partir do arquivo

        self.estados = arq_dfa.estados  # Obtém os estados do AFD original
        palavra = input("Digite a palavra: ")  # Solicita ao usuário uma palavra para teste
        palavra_aceita = self.verificarPalavraAceita(palavra)  # Verifica se a palavra é aceita pelo AFD

        # Monta uma string com o resultado da verificação e arquivos gerados
        str = "\nCadeia: " + palavra
        str += "\nAceita: {}".format(palavra_aceita)
        str += "\nArquivos gerados: AFN Original"
        str += ", AFD Original, AFD Complementado, AFD Invertido" + "\n"

        print(str)  # Exibe o resultado para o usuário

    def verificarPalavraAceita(self, palavra):
        estado_atual = None

        # Encontra o estado inicial para começar a verificação
        for estado in self.estados:
            if estado.inicial:
                estado_atual = estado
                break

        # Para cada letra da palavra, verifica se há transição válida
        for letra in palavra:
            if letra in estado_atual.regras:
                estado_atual = self.procurarEstado(estado_atual.regras[letra])
            else:
                return False  # Se não houver transição, palavra não é aceita

        return estado_atual.final  # Retorna True se estado final, False caso contrário

    def procurarEstado(self, simbolo):
        # Procura e retorna o estado com o símbolo correspondente
        for estado in self.estados:
            if estado.simbolo == simbolo:
                return estado

# Instancia a classe Main passando o nome do arquivo com a gramática/AFD
Main("Gramática 1.txt")
