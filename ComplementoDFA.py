from AjustesFuncoes import (
    Variavel as Estado,
)  # Importa a classe Variavel renomeando para Estado


class ComplementoDFA:
    def __init__(self, arquivo_dfa):  # Construtor da classe
        self.letras = arquivo_dfa.letras  # Guarda o alfabeto
        self.estados = self.copiarEstados(
            arquivo_dfa.estados
        )  # Guarda os estados do AFD
        self.estado_inicial = arquivo_dfa.estado_inicial  # Guarda o estado inicial
        self.linhas = self.ajustarArquivo()  # Prepara o cabeçalho do novo arquivo
        self.trocarFinalInicial()  # Realiza o complemento: inverte finais e não-finais
        self.colocarFuncoes()  # Escreve as funções de transição no arquivo

        # Salva o resultado no arquivo "AFD Complementado.txt"
        with open("AFD Complementado.txt", "w", encoding="utf-8") as arquivo:
            for linha in self.linhas:
                arquivo.write(linha + "\n")

    def copiarEstados(self, estados):
        # Cria uma lista vazia para armazenar os novos estados copiados
        novos_estados = []

        # Itera sobre cada estado fornecido na lista 'estados'
        for estado in estados:
            # Cria uma nova instância de Estado com o mesmo símbolo do estado original
            novo_estado = Estado(estado.simbolo)
            # Copia os atributos de estado inicial e final
            novo_estado.inicial = estado.inicial
            novo_estado.final = estado.final

            # Copia as regras de transição associadas a cada letra
            for letra in self.letras:
                novo_estado.regras[letra] = estado.regras[letra]

            # Adiciona o novo estado copiado à lista de novos estados
            novos_estados.append(novo_estado)

        # Retorna a lista de estados copiados
        return novos_estados

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
