from ArquivoDFA import ArquivoDFA  # Importa a classe responsável por gerar o AFD original a partir de um arquivo

class InversoDFA:  # Define a classe que cria o AFD invertido (inverso das transições)
    def __init__(self, endereco_arquivo):  # Construtor que recebe o caminho do arquivo com o AFD original
        arquivo_dfa = ArquivoDFA(endereco_arquivo)  # Cria o AFD original
        self.estados = arquivo_dfa.estados  # Guarda os estados do AFD
        self.letras = arquivo_dfa.letras  # Guarda o alfabeto do AFD
        self.estado_inicial = arquivo_dfa.estado_inicial  # Guarda o estado inicial original
        self.estados_invertidos = self.gerarEstadosInvertidos()  # Cria estrutura vazia para as transições invertidas
        self.inverterFuncoes()  # Realiza a inversão das transições
        self.colocarNovasFuncoes()  # Substitui as transições atuais pelas invertidas
        self.linhas = self.ajustarArquivo()  # Prepara a estrutura do arquivo de saída
        self.trocarFinalInicial()  # Troca os estados finais por iniciais e vice-versa
        self.colocarFuncoes()  # Adiciona as transições e estados finais/iniciais no arquivo

        with open("AFD Invertido.txt", "w", encoding="utf-8") as arquivo:  # Escreve o AFD invertido no arquivo
            for linha in self.linhas:
                arquivo.write(linha + "\n")

    def gerarEstadosInvertidos(self):  # Cria uma lista de dicionários vazios, um para cada estado, para armazenar as transições invertidas
        estados = []

        for _ in self.estados:
            estados.append({})

        for estado in estados:
            for letra in self.letras:
                estado[letra] = ""

        return estados

    def inverterFuncoes(self):  # Inverte as transições do AFD original
        for u in self.estados:  # Para cada estado u
            for i in range(len(self.estados)):  # Compara com todos os outros estados
                for letra in self.letras:
                    if u.regras[letra] == self.estados[i].simbolo:  # Se a transição leva para o estado atual
                        self.estados_invertidos[i][letra] += u.simbolo + " "  # Adiciona u como origem invertida

    def colocarNovasFuncoes(self):  # Atualiza os estados com as novas transições invertidas
        for i in range(len(self.estados)):
            for letra in self.letras:
                self.estados[i].regras[letra] = self.estados_invertidos[i][letra]

    def trocarFinalInicial(self):  # Troca os estados finais pelos iniciais e vice-versa
        for estado in self.estados:
            estado.inicial, estado.final = estado.final, estado.inicial

    def ajustarArquivo(self):  # Cria a estrutura base do arquivo de saída
        linhas = []
        linhas.append("# AFD Invertido")
        linhas.append("Q: ")
        linhas.append("Σ: ")
        linhas.append("δ: ")

        linhas[1] = self.colocarVirgula(linhas[1], [e.simbolo for e in self.estados])  # Lista de estados
        linhas[2] = self.colocarVirgula(linhas[2], self.letras)  # Alfabeto

        return linhas

    def colocarFuncoes(self):  # Adiciona as transições e os estados finais/iniciais no arquivo
        for estado in self.estados:
            for letra in estado.regras:
                if estado.regras[letra] != "":
                    lista = estado.regras[letra].split(" ")  # Divide múltiplos destinos (caso de NFA invertido)

                    for i in range(len(lista) - 1):  # Ignora string vazia no final
                        texto = "{}, {} → {}".format(estado.simbolo, letra, lista[i])
                        self.linhas.append(texto)

        self.linhas.append("Inicial(s): ")
        self.linhas.append("Final(s): ")

        self.linhas[-2] = self.colocarVirgula(
            self.linhas[-2],
            [estado.simbolo for estado in self.estados if estado.inicial],
        )
        self.linhas[-1] = self.colocarVirgula(
            self.linhas[-1], [estado.simbolo for estado in self.estados if estado.final]
        )

    def colocarVirgula(self, linha, caracteres):  # Junta os elementos com vírgula e espaço
        colocar_virgula = False

        for caractere in caracteres:
            if colocar_virgula:
                linha += ", " + caractere
            else:
                linha += caractere
                colocar_virgula = True

        return linha
