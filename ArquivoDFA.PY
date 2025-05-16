from GeradorDFA import GeradorDFA  # Importa o gerador de AFD a partir do AFN


class ArquivoDFA:
    def __init__(self, endereco_arquivo):  # Construtor da classe
        gerador_dfa = GeradorDFA(
            endereco_arquivo
        )  # Cria o DFA a partir do arquivo fornecido
        self.estado_inicial = gerador_dfa.estado_inicial  # Salva o estado inicial
        self.estados = sorted(
            gerador_dfa.estados, key=lambda estado: estado.simbolo
        )  # Ordena os estados pelo símbolo
        self.letras = gerador_dfa.letras  # Alfabeto
        self.definirIniciaisFinais(
            gerador_dfa.nfa_estados
        )  # Define os estados iniciais e finais no DFA
        self.linhas = (
            self.ajustarArquivo()
        )  # Monta a estrutura inicial do arquivo de saída
        self.colocarFuncoes()  # Adiciona as funções de transição ao arquivo

        # Salva o conteúdo no arquivo "AFD Original.txt"
        with open("AFD Original.txt", "w", encoding="utf-8") as arquivo:
            for linha in self.linhas:
                arquivo.write(linha + "\n")

    def definirIniciaisFinais(
        self, nfa_estados
    ):  # Define os estados iniciais e finais do DFA com base no NFA
        unitarios = nfa_estados  # Estados individuais do NFA
        n_unitarios = []  # Estados compostos do DFA

        # Identifica os estados compostos (com mais de um símbolo)
        for i in range(len(self.estados) - 1):
            if len(self.estados[i].simbolo) > 1:
                n_unitarios.append(self.estados[i])

        # Define quais estados compostos são finais com base nos estados finais do NFA
        for u in unitarios:
            for n in n_unitarios:
                for i in range(len(n.simbolo)):
                    if n.simbolo[i] == u.simbolo and u.final:
                        n.final = True

            # Define estados iniciais e finais unitários diretamente
            for estado in self.estados:
                if estado.simbolo == u.simbolo and u.inicial:
                    estado.inicial = True
                if estado.simbolo == u.simbolo and u.final:
                    estado.final = True

    def colocarVirgula(
        self, linha, caracteres
    ):  # Adiciona os elementos separados por vírgulas
        colocar_virgula = False

        for caractere in caracteres:
            if colocar_virgula:
                linha += ", " + caractere
            else:
                linha += caractere
                colocar_virgula = True

        return linha

    def ajustarArquivo(self):  # Inicializa a estrutura do arquivo AFD
        linhas = []
        linhas.append("# AFD Original")  # Comentário de cabeçalho
        linhas.append("Q: ")  # Conjunto de estados
        linhas.append("Σ: ")  # Alfabeto
        linhas.append("δ: ")  # Transições

        # Adiciona os estados e letras
        linhas[1] = self.colocarVirgula(linhas[1], [e.simbolo for e in self.estados])
        linhas[2] = self.colocarVirgula(linhas[2], self.letras)

        return linhas

    def colocarFuncoes(self):  # Adiciona todas as transições do AFD
        for estado in self.estados:
            for letra, prox_estado in estado.regras.items():
                texto = "{}, {} → {}".format(estado.simbolo, letra, prox_estado)
                self.linhas.append(texto)

        self.linhas.append("Inicial: " + self.estado_inicial)  # Define o estado inicial
        self.linhas.append("Final(s): ")  # Placeholder para estados finais

        # Preenche a linha de estados finais
        self.linhas[-1] = self.colocarVirgula(
            self.linhas[-1], [estado.simbolo for estado in self.estados if estado.final]
        )
