from utils import registrar_acao
import random # Necessário para chances (falha, esquiva, etc.)

class Personagem:
    """
    Classe base para todos os personagens.
    Inclui novas mecânicas de combate.
    """
    def __init__(self, nome, idade, vida, ataque, defesa):
        self.nome = nome
        self.idade = idade
        self.vida_maxima = vida
        self.vida_atual = vida
        self.ataque = ataque
        self.defesa = defesa
        self.inventario = {}  
        self.habilidades = [] 
        self.esta_vivo = True
        
        # Novas mecânicas de combate
        self.acertos_consecutivos = 0
        self.chance_acerto = 0.70  # Chance base de 70% (30% de falha)
        self.tentando_esquivar = False

    def atacar(self, alvo):
        """
        Calcula e aplica o dano a um alvo.
        Agora inclui chance de falha e ataque especial.
        """
        if not self.esta_vivo:
            registrar_acao(f"{self.nome} não pode atacar, pois está derrotado.")
            return

        if not alvo.esta_vivo:
            registrar_acao(f"{self.nome} não pode atacar {alvo.nome}, pois ele(a) já está derrotado(a).")
            return

        # 1. Verificar chance de falha
        if random.random() > self.chance_acerto:
            registrar_acao(f"ATAQUE FALHOU! {self.nome} errou o alvo {alvo.nome}.")
            self.acertos_consecutivos = 0  # Reseta o contador ao falhar
            return

        # 2. Calcular dano base
        dano_bruto = self.ataque - alvo.defesa
        dano_final = max(1, dano_bruto)  # Garante pelo menos 1 de dano

        # 3. Verificar Ataque Especial (3 acertos seguidos)
        self.acertos_consecutivos += 1
        if self.acertos_consecutivos >= 3:
            dano_bonus = round(dano_final * 0.40) # 40% a mais
            dano_final += dano_bonus
            registrar_acao(f"✨ ATAQUE ESPECIAL! ✨ {self.nome} acerta 3x seguidas!")
            self.acertos_consecutivos = 0 # Reseta após usar
        
        registrar_acao(f"{self.nome} ataca {alvo.nome} causando {dano_final} de dano!")
        alvo.receber_dano(dano_final)

    def receber_dano(self, dano):
        """
        Reduz a vida do personagem, com chance de esquiva.
        """
        # 1. Verificar tentativa de Esquiva (70% de chance)
        if self.tentando_esquivar:
            if random.random() < 0.70:
                registrar_acao(f"💨 ESQUIVA! {self.nome} se esquivou do ataque!")
                self.tentando_esquivar = False # Reseta a tentativa
                return # Não recebe dano
            else:
                registrar_acao(f"A esquiva de {self.nome} falhou!")
        
        # Reseta a tentativa de esquiva (mesmo se falhou ou não tentou)
        self.tentando_esquivar = False
        
        # 2. Receber dano
        self.vida_atual -= dano
        if self.vida_atual <= 0:
            self.vida_atual = 0
            self.esta_vivo = False
            registrar_acao(f"☠️ {self.nome} foi derrotado(a)! ☠️")
        else:
            registrar_acao(f"{self.nome} agora tem {self.vida_atual}/{self.vida_maxima} de vida.")

    def dialogar(self, outro_personagem, mensagem):
        """
        Inicia um diálogo com outro personagem.
        """
        registrar_acao(f"[{self.nome} para {outro_personagem.nome}]: \"{mensagem}\"")

    def mostrar_status(self):
        """
        Exibe o status atual do personagem.
        """
        status_vivo = "Vivo" if self.esta_vivo else "Derrotado"
        acerto_perc = f"{self.chance_acerto * 100}%"
        status_line = (
            f"[Status: {self.nome}] "
            f"Vida: {self.vida_atual}/{self.vida_maxima} | "
            f"Atk: {self.ataque} | Def: {self.defesa} | "
            f"Acerto: {acerto_perc} | Status: {status_vivo}"
        )
        registrar_acao(status_line, logar=False)
        
        if self.acertos_consecutivos > 0:
            registrar_acao(f"  (Acertos consecutivos: {self.acertos_consecutivos})", logar=False)

    def __str__(self):
        return f'{self.nome} (V: {self.vida_atual}/{self.vida_maxima}, A: {self.ataque}, D: {self.defesa})'