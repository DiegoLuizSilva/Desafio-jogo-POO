from personagem import Personagem
from utils import registrar_acao, linha_separadora, COR_ERRO, COR_SUCESSO, COR_CURA, COR_HEROI
from.personagem import Personagem

class Heroi(Personagem):
    def __init__(self, nome, idade, vida, ataque, defesa, nivel_heroismo):
        super().__init__(nome, idade, vida, ataque, defesa)
        self.nivel_heroismo = nivel_heroismo
        
        self.inventario['pocao_cura'] = 2
        self.inventario['pocao_regen'] = 1 
        
        self.efeito_regen = 0 

    def dialogar(self, outro_personagem, mensagem):
        registrar_acao(COR_HEROI + f"[{self.nome} para {outro_personagem.nome}]: \"{mensagem}\"")

    def usar_pocao_cura(self):
        if self.inventario.get('pocao_cura', 0) <= 0:
            registrar_acao(COR_ERRO + f"{self.nome} tenta usar poção, mas não tem nenhuma!")
            return False 

        if self.vida_atual > 50:
            registrar_acao(COR_ERRO + f"{self.nome} tenta usar poção, mas sua vida está acima de 50!")
            return False 
            
        self.inventario['pocao_cura'] -= 1
        cura = 50  
        self.vida_atual = min(self.vida_maxima, self.vida_atual + cura)
        registrar_acao(COR_CURA + f"❤️ {self.nome} usa Poção de Cura! Recupera {cura} de vida. (Poções restantes: {self.inventario['pocao_cura']})")
        return True

    def usar_pocao_regen(self):
        if self.inventario.get('pocao_regen', 0) > 0:
            self.inventario['pocao_regen'] -= 1
            self.efeito_regen = 3 
            registrar_acao(COR_CURA + f"🌿 {self.nome} bebe a Poção de Regeneração! Irá curar por 3 turnos.")
            return True
        else:
            registrar_acao(COR_ERRO + f"{self.nome} tenta usar a Poção de Regeneração, mas não tem!")
            return False
            
    def aplicar_efeitos_turno(self):
        if self.efeito_regen > 0:
            cura = round(self.vida_maxima * 0.10) 
            self.vida_atual = min(self.vida_maxima, self.vida_atual + cura)
            self.efeito_regen -= 1
            registrar_acao(COR_CURA + f"🌿 Regeneração ativa! {self.nome} cura {cura} de vida. (Turnos restantes: {self.efeito_regen})")


    def salvar_refem(self, refem):
        linha_separadora('~')
        registrar_acao(COR_SUCESSO + f"{self.nome} derrota o vilão e salva {refem.nome}!")
        self.dialogar(refem, "Você está a salvo agora!")
        refem.dialogar(self, f"Meu herói! Obrigada por me salvar, {self.nome}!")
        linha_separadora('~')