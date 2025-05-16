from AjustesFuncoes import (
    AjustesFuncoes,
)  # Importa a classe AjustesFuncoes de outro módulo


class GeradorNFA:  # Classe que gera e escreve um autômato finito não determinístico (AFN)
    def __init__(self, endereco_arquivo):  # Construtor que recebe o caminho do arquivo
        ajustes_funcoes = AjustesFuncoes(
            endereco_arquivo
        )  # Instancia AjustesFuncoes para processar os dados
        self.estados = ajustes_funcoes.variaveis  # Lista de estados (Variavel)
        self.estado_inicial = ajustes_funcoes.var_inicial  # Símbolo do estado inicial
        self.letras = ajustes_funcoes.letras  # Letras do alfabeto
        self.linhas = (
            self.ajustarArquivo()
        )  # Cria as primeiras linhas do arquivo do AFN
        self.colocarFuncoes()  # Adiciona as funções de transição

        with open(
            "AFN Original.txt", "w", encoding="utf-8"
        ) as arquivo:  # Abre/cria o arquivo de saída
            for linha in self.linhas:
                arquivo.write(linha + "\n")  # Escreve cada linha no arquivo

    def ajustarArquivo(
        self,
    ):  # Inicializa a estrutura do arquivo com cabeçalhos e listas vazias
        linhas = []
        linhas.append("# AFN Original")  # Comentário inicial
        linhas.append("Q: ")  # Estados
        linhas.append("Σ: ")  # Alfabeto
        linhas.append("δ: ")  # Transições

        linhas[1] = self.colocarVirgula(
            linhas[1], [e.simbolo for e in self.estados]
        )  # Adiciona os estados à linha "Q"
        linhas[2] = self.colocarVirgula(
            linhas[2], self.letras
        )  # Adiciona as letras à linha "Σ"

        return linhas  # Retorna a estrutura inicial do arquivo

    def colocarVirgula(
        self, linha, caracteres
    ):  # Adiciona os caracteres separados por vírgula a uma linha
        colocar_virgula = False  # Flag para saber se já é necessário colocar vírgula

        for caractere in caracteres:
            if colocar_virgula:
                linha += ", " + caractere  # Adiciona vírgula e caractere
            else:
                linha += caractere  # Adiciona só o primeiro caractere
                colocar_virgula = True  # A partir daqui, colocar vírgula

        return linha  # Retorna a linha montada

    def colocarFuncoes(self):  # Monta as regras de transição do AFN
        for estado in self.estados:
            for (
                letra,
                prox_estado,
            ) in estado.regras.items():  # Para cada letra e seus destinos
                for i in range(
                    len(prox_estado)
                ):  # Percorre cada estado de destino (não determinismo)
                    texto = "{}, {} → {}".format(
                        estado.simbolo, letra, prox_estado[i]
                    )  # Formata a transição
                    self.linhas.append(texto)  # Adiciona ao conteúdo do arquivo

        self.linhas.append(
            "Inicial: " + self.estado_inicial
        )  # Adiciona o estado inicial
        self.linhas.append("Final(s): ")  # Adiciona cabeçalho para estados finais

        self.linhas[-1] = self.colocarVirgula(
            self.linhas[-1],
            [
                estado.simbolo for estado in self.estados if estado.final
            ],  # Insere os estados finais
        )
