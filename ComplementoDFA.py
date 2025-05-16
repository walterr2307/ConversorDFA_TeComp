from ArquivoDFA import ArquivoDFA  # Importa a classe que gera o AFD a partir do NFA


class ComplementoDFA:
    def __init__(self, endereco_arquivo):  # Construtor da classe
        arquivo_dfa = ArquivoDFA(
            endereco_arquivo
        )  # Gera um AFD a partir do arquivo de entrada
        self.estados = arquivo_dfa.estados  # Guarda os estados do AFD
        self.letras = arquivo_dfa.letras  # Guarda o alfabeto
        self.estado_inicial = arquivo_dfa.estado_inicial  # Guarda o estado inicial
        self.linhas = self.ajustarArquivo()  # Prepara o cabeçalho do novo arquivo
        self.trocarFinalInicial()  # Realiza o complemento: inverte finais e não-finais
        self.colocarFuncoes()  # Escreve as funções de transição no arquivo

        # Salva o resultado no arquivo "AFD Complementado.txt"
        with open("AFD Complementado.txt", "w", encoding="utf-8") as arquivo:
            for linha in self.linhas:
                arquivo.write(linha + "\n")

    def trocarFinalInicial(self):  # Inverte os estados finais e não-finais
        for estado in self.estados:
            if estado.final:  # Se era final, deixa de ser
                estado.final = False
            else:  # Se não era final, torna-se final
                estado.final = True

    def ajustarArquivo(self):  # Cria o cabeçalho do arquivo de saída
        linhas = []
        linhas.append("# AFD Complementado")  # Comentário de identificação
        linhas.append("Q: ")  # Estados
        linhas.append("Σ: ")  # Alfabeto
        linhas.append("δ: ")  # Transições

        # Preenche os estados e o alfabeto com vírgulas
        linhas[1] = self.colocarVirgula(linhas[1], [e.simbolo for e in self.estados])
        linhas[2] = self.colocarVirgula(linhas[2], self.letras)

        return linhas

    def colocarFuncoes(self):  # Adiciona as funções de transição ao arquivo
        for estado in self.estados:
            for letra, prox_estado in estado.regras.items():
                texto = "{}, {} → {}".format(estado.simbolo, letra, prox_estado)
                self.linhas.append(texto)

        self.linhas.append("Inicial: " + self.estado_inicial)  # Define o estado inicial
        self.linhas.append("Final(s): ")  # Placeholder para estados finais

        # Preenche os estados finais após complemento
        self.linhas[-1] = self.colocarVirgula(
            self.linhas[-1], [estado.simbolo for estado in self.estados if estado.final]
        )

    def colocarVirgula(
        self, linha, caracteres
    ):  # Função auxiliar para colocar vírgulas entre os itens
        colocar_virgula = False

        for caractere in caracteres:
            if colocar_virgula:
                linha += ", " + caractere
            else:
                linha += caractere
                colocar_virgula = True

        return linha
