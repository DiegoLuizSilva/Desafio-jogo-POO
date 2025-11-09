from personagem import Personagem
from utils import registrar_acao, linha_separadora

class Heroi(Personagem):
    """
    A classe Heroi representa o protagonista.
    Contém inventário expandido e efeitos de status.
    """
    def __init__(self, nome, idade, vida, ataque, defesa, nivel_heroismo):
        super().__init__(nome, idade, vida, ataque, defesa)
        self.nivel_heroismo = nivel_heroismo
        
        # Inventário inicial
        self.inventario['pocao_cura'] = 2
        
        # Efeitos de status
        self.efeito_regen = 0 # Contador de turnos para regeneração

    def usar_pocao_cura(self):
        """
        Usa uma poção do inventário para curar vida.
        SÓ PODE SER USADA COM VIDA <= 50.
        """
        if self.inventario.get('pocao_cura', 0) <= 0:
            registrar_acao(f"{self.nome} tenta usar poção, mas não tem nenhuma!")
            return False # Falhou

        if self.vida_atual > 50:
            registrar_acao(f"{self.nome} tenta usar poção, mas sua vida está acima de 50!")
            return False # Falhou
            
        self.inventario['pocao_cura'] -= 1
        cura = 50  # Quantidade de vida que a poção cura
        self.vida_atual = min(self.vida_maxima, self.vida_atual + cura)
        
        registrar_acao(f"❤️ {self.nome} usa uma poção e cura {cura} de vida! ❤️")
        self.mostrar_status()
        return True # Sucesso

    def usar_pocao_forca(self):
        """ Usa a poção de força do Mestre Zonai. """
        if self.inventario.get('pocao_forca', 0) > 0:
            self.inventario['pocao_forca'] -= 1
            aumento = round(self.ataque * 0.30)
            self.ataque += aumento
            registrar_acao(f"💪 {self.nome} bebe a Poção de Força! Ataque aumentado em {aumento} (Total: {self.ataque})")
            return True
        else:
            registrar_acao(f"{self.nome} tenta usar a Poção de Força, mas não tem!")
            return False

    def usar_pocao_regen(self):
        """ Usa a poção de regeneração do Mestre Zonai. """
        if self.inventario.get('pocao_regen', 0) > 0:
            self.inventario['pocao_regen'] -= 1
            self.efeito_regen = 3 # Define 3 turnos de regeneração
            registrar_acao(f"🌿 {self.nome} bebe a Poção de Regeneração! Irá curar por 3 turnos.")
            return True
        else:
            registrar_acao(f"{self.nome} tenta usar a Poção de Regeneração, mas não tem!")
            return False
            
    def aplicar_efeitos_turno(self):
        """ Aplica efeitos passivos no início do turno (ex: regeneração). """
        if self.efeito_regen > 0:
            cura = round(self.vida_maxima * 0.10) # Cura 10% da vida máxima
            self.vida_atual = min(self.vida_maxima, self.vida_atual + cura)
            self.efeito_regen -= 1
            registrar_acao(f"🌿 Regeneração ativa! {self.nome} cura {cura} de vida. (Turnos restantes: {self.efeito_regen})")


    def salvar_refem(self, refem):
        """ Método de interação para um evento do jogo. """
        linha_separadora('~')
        registrar_acao(f"{self.nome} derrota o vilão e salva {refem.nome}!")
        self.dialogar(refem, "Você está a salvo agora!")
        refem.dialogar(self, f"Meu herói! Obrigada por me salvar, {self.nome}!")
        linha_separadora('~')

    def dialogar(self, outro_personagem, mensagem):
        """ Diálogo heroico. """
        registrar_acao(f"[{self.nome} diz heroicamente para {outro_personagem.nome}]: \"{mensagem}\"")

    def __str__(self):
        return f'Herói: {super().__str__()}, Heroísmo: {self.nivel_heroismo}'