from utils import registrar_acao, COR_AVISO, COR_ERRO, COR_DESTAQUE, COR_VIDA, COR_ATAQUE, COR_DEFESA, COR_SUCESSO
import random 

class Personagem:
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
        
        self.acertos_consecutivos = 0
        self.chance_acerto = 0.70  
        self.tentando_esquivar = False

    def atacar(self, alvo):
        if not self.esta_vivo:
            registrar_acao(COR_AVISO + f"{self.nome} não pode atacar, pois está derrotado.")
            return

        if not alvo.esta_vivo:
            registrar_acao(COR_AVISO + f"{self.nome} não pode atacar {alvo.nome}, pois ele(a) já está derrotado(a).")
            return

        if random.random() > self.chance_acerto:
            registrar_acao(COR_AVISO + f"⚔️ {self.nome} ataca... mas erra o alvo!")
            self.acertos_consecutivos = 0
            return

        dano_base = self.ataque
        
        if self.acertos_consecutivos == 2:
            dano_base *= 1.5 
            registrar_acao(COR_DESTAQUE + f"💥 ATAQUE ESPECIAL! {self.nome} usa um golpe poderoso!")
            self.acertos_consecutivos = 0
        else:
            self.acertos_consecutivos += 1
            
        dano_total = max(1, dano_base - alvo.defesa)
        
        registrar_acao(f"⚔️ {self.nome} ataca {alvo.nome} causando {dano_total} de dano!")
        alvo.receber_dano(dano_total)

    def receber_dano(self, dano):
        if self.tentando_esquivar and random.random() < 0.50:
            registrar_acao(COR_SUCESSO + f"🛡️ {self.nome} se prepara e consegue esquivar do ataque!")
            self.tentando_esquivar = False
            return
            
        self.tentando_esquivar = False
        
        self.vida_atual -= dano
        if self.vida_atual <= 0:
            self.vida_atual = 0
            self.esta_vivo = False
            registrar_acao(COR_ERRO + f"☠️ {self.nome} foi derrotado(a)! ☠️")
        else:
            registrar_acao(COR_AVISO + f"{self.nome} agora tem {self.vida_atual}/{self.vida_maxima} de vida.")

    def dialogar(self, outro_personagem, mensagem):
        registrar_acao(f"[{self.nome} para {outro_personagem.nome}]: \"{mensagem}\"")

    def mostrar_status(self):
        status_vivo = (COR_SUCESSO + "Vivo") if self.esta_vivo else (COR_ERRO + "Derrotado")
        acerto_perc = f"{self.chance_acerto * 100}%"
        status_line = (
            f"[{COR_DESTAQUE + 'Status: ' + self.nome}] "
            f"{COR_VIDA}Vida: {self.vida_atual}/{self.vida_maxima} | "
            f"{COR_ATAQUE}Atk: {self.ataque} | {COR_DEFESA}Def: {self.defesa} | "
            f"Acerto: {acerto_perc} | Status: {status_vivo}"
        )
        registrar_acao(status_line, logar=False)