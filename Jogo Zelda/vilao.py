from personagem import Personagem
from utils import registrar_acao, COR_VILAO

class Vilao(Personagem):
    def __init__(self, nome, idade, vida, ataque, defesa, maldade):
        super().__init__(nome, idade, vida, ataque, defesa)
        
        niveis_validos = ['Baixa', 'Média', 'Alta', 'Extrema']
        if maldade not in niveis_validos:
            raise ValueError(f"Nível de maldade inválido! Escolha entre {niveis_validos}")
        self.maldade = maldade

    def dialogar(self, outro_personagem, mensagem):
        registrar_acao(COR_VILAO + f"[{self.nome} rosna para {outro_personagem.nome}]: \"{mensagem}\"")

    def __str__(self):
        return f'{COR_VILAO}Vilão: {super().__str__()}, Maldade: {self.maldade}'