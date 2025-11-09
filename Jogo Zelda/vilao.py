from personagem import Personagem
from utils import registrar_acao

class Vilao(Personagem):
    """
    A classe Vilao.
    Herda de Personagem e possui um nível de maldade.
    """
    def __init__(self, nome, idade, vida, ataque, defesa, maldade):
        super().__init__(nome, idade, vida, ataque, defesa)
        # Nível de maldade "Extrema" adicionado
        niveis_validos = ['Baixa', 'Média', 'Alta', 'Extrema']
        if maldade not in niveis_validos:
            raise ValueError(f"Nível de maldade inválido! Escolha entre {niveis_validos}")
        self.maldade = maldade

    def dialogar(self, outro_personagem, mensagem):
        """ Diálogo maligno. """
        registrar_acao(f"[{self.nome} rosna para {outro_personagem.nome}]: \"{mensagem}\"")

    def __str__(self):
        return f'Vilão: {super().__str__()}, Maldade: {self.maldade}'