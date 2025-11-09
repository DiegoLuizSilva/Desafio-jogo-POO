import sys
from personagem import Personagem
from heroi import Heroi
from vilao import Vilao
from utils import registrar_acao, mostrar_log, linha_separadora, intro_texto

def batalha(heroi, vilao):
    """
    Gerencia uma batalha em turnos, agora com menu de ações dinâmico
    e aplicação de efeitos de turno.
    """
    intro_texto(f"A BATALHA COMEÇA: {heroi.nome} vs. {vilao.nome}")
    
    turno = 1
    # Loop de batalha
    while heroi.esta_vivo and vilao.esta_vivo:
        linha_separadora()
        registrar_acao(f"--- TURNO {turno} ---", logar=False)
        
        # Aplicar efeitos de início de turno (ex: regeneração)
        heroi.aplicar_efeitos_turno()
        if not heroi.esta_vivo: # Checa se a regen não salvou (embora não deva matar)
            break
            
        # Turno do Herói
        heroi.mostrar_status()
        vilao.mostrar_status()
        
        # --- Construir menu de ações dinâmico ---
        opcoes = {"1": "Atacar", "2": "Tentar Esquivar"}
        mapa_acoes = {'1': 'atacar', '2': 'esquivar'}
        idx_atual = 3 # Próximo índice numérico

        # Opção de Poção de Cura
        poc_cura_rest = heroi.inventario.get('pocao_cura', 0)
        if poc_cura_rest > 0:
            if heroi.vida_atual <= 50:
                opcoes[str(idx_atual)] = f"Usar Poção de Cura (Restantes: {poc_cura_rest})"
            else:
                opcoes[str(idx_atual)] = f"Usar Poção de Cura (Vida > 50!)"
            mapa_acoes[str(idx_atual)] = 'pocao_cura'
            idx_atual += 1

        # Opção de Poção de Força
        poc_forc_rest = heroi.inventario.get('pocao_forca', 0)
        if poc_forc_rest > 0:
            opcoes[str(idx_atual)] = f"Usar Poção de Força (Restantes: {poc_forc_rest})"
            mapa_acoes[str(idx_atual)] = 'pocao_forca'
            idx_atual += 1

        # Opção de Poção de Regeneração
        poc_regen_rest = heroi.inventario.get('pocao_regen', 0)
        if poc_regen_rest > 0:
            opcoes[str(idx_atual)] = f"Usar Poção de Regeneração (Restantes: {poc_regen_rest})"
            mapa_acoes[str(idx_atual)] = 'pocao_regen'
            idx_atual += 1

        # Gerar texto do menu
        menu_texto = "\nEscolha sua ação:\n"
        for key, desc in opcoes.items():
            menu_texto += f"  {key}: {desc}\n"
        menu_texto += "> "

        escolha = input(menu_texto).lower()
        acao_escolhida = mapa_acoes.get(escolha)
        
        # --- Processar escolha ---
        acao_sucedida = True
        if acao_escolhida == 'atacar':
            heroi.atacar(vilao)
        elif acao_escolhida == 'esquivar':
            heroi.tentando_esquivar = True
            registrar_acao(f"💨 {heroi.nome} se prepara para esquivar do próximo ataque!")
        elif acao_escolhida == 'pocao_cura':
            acao_sucedida = heroi.usar_pocao_cura() # Retorna True/False
        elif acao_escolhida == 'pocao_forca':
            acao_sucedida = heroi.usar_pocao_forca()
        elif acao_escolhida == 'pocao_regen':
            acao_sucedida = heroi.usar_pocao_regen()
        else:
            registrar_acao(f"Ação inválida! {heroi.nome} hesita e perde o turno.")
            acao_sucedida = False
        
        # Se a ação foi inválida (ex: poção sem ter, ou cura > 50)
        if not acao_sucedida:
             registrar_acao(f"{heroi.nome} perde o turno devido à ação falha.")

        # Verifica se o vilão foi derrotado após a ação do herói
        if not vilao.esta_vivo:
            break
            
        linha_separadora('.')
        
        # Turno do Vilão
        registrar_acao(f"Turno de {vilao.nome}.", logar=False)
        vilao.atacar(heroi)
        
        turno += 1

    # Fim da batalha
    linha_separadora()
    if heroi.esta_vivo:
        registrar_acao(f"🏆 {heroi.nome} venceu a batalha! 🏆")
        return True
    else:
        registrar_acao(f"☠️ {vilao.nome} venceu a batalha... ☠️")
        return False

# --- FUNÇÕES DE HISTÓRIA ---

def interludio_acampamento(heroi, npc):
    """ Evento pós-Agahnim: Escolha de upgrade. """
    linha_separadora('~')
    registrar_acao(f"{heroi.nome} derrota Agahnim e resgata {npc.nome}!")
    heroi.dialogar(npc, "Você está a salvo agora!")
    npc.dialogar(heroi, f"Meu herói! Obrigada por me salvar, {heroi.nome}!")
    linha_separadora('~')
    
    registrar_acao("\nDe volta ao acampamento, Link e Zelda descansam ao redor da fogueira.")
    registrar_acao("Zelda: 'Você foi incrível, Link. Mas a jornada só começou.'")
    registrar_acao("Zelda: 'Descanse. Você pode focar em afiar sua lâmina ou em recuperar suas forças.'")
    
    while True:
        linha_separadora('?', 40)
        print("Escolha sua recompensa de descanso:")
        print("  1: Afiar a Lâmina (Ataque +10%)")
        print("  2: Recuperar Forças (Cura 100% da vida)")
        escolha = input("> ")
        
        if escolha == '1':
            aumento = round(heroi.ataque * 0.10)
            heroi.ataque += aumento
            registrar_acao(f"Link afia sua espada. Ataque aumentado em {aumento} (Total: {heroi.ataque})")
            break
        elif escolha == '2':
            cura_total = heroi.vida_maxima - heroi.vida_atual
            heroi.vida_atual = heroi.vida_maxima
            registrar_acao(f"Link descansa profundamente. {cura_total} de vida recuperada. (Total: {heroi.vida_atual})")
            break
        else:
            print("Escolha inválida. Tente 1 ou 2.")
    
    linha_separadora('~')
    registrar_acao("Após o descanso, Link e Zelda continuam sua jornada pelos campos...")


def interludio_mestre_zonai(heroi, npc):
    """ Evento pós-Ghirahim: Mestre Zonai dá poções. """
    linha_separadora('~')
    registrar_acao("\nDe volta ao acampamento, uma figura encapuzada os aguarda.")
    registrar_acao("A figura revela ser um Mestre Curandeiro da tribo Zonai.")
    registrar_acao(f"Mestre Zonai: 'Vi sua luta contra Ghirahim. A espada que você carrega... é um mau presságio.'")
    registrar_acao(f"Mestre Zonai: 'Ela atrai a escuridão. O verdadeiro mal ainda está por vir.'")
    registrar_acao(f"Mestre Zonai: 'Tome isto, jovem herói. Você precisará de toda ajuda possível.'")
    
    heroi.inventario['pocao_forca'] = 1
    heroi.inventario['pocao_regen'] = 1
    
    registrar_acao("Poção de Força (Ataque +30%) foi adicionada ao inventário!")
    registrar_acao("Poção de Regeneração (Cura por 3 turnos) foi adicionada ao inventário!")
    linha_separadora('~')


def final_bom(heroi, npc):
    """ História de encerramento se o jogador vencer Ganon. """
    intro_texto("VITÓRIA!")
    registrar_acao(f"Com um golpe final, {heroi.nome} destrói Ganon, o Rei do Mal.")
    registrar_acao("A energia sombria se dissipa. A 'Decayed Master Sword' brilha intensamente...")
    registrar_acao("...e se transforma na verdadeira Master Sword, purificada pelo heroísmo de Link.")
    npc.dialogar(heroi, "Conseguimos, Link! Você salvou o mundo!")
    registrar_acao(f"Com a paz restaurada, {heroi.nome} e {npc.nome} retornam para casa, celebrados como os heróis de Hyrule.")
    registrar_acao("\n--- FIM ---")

def final_ruim():
    """ História de encerramento se o jogador perder para Ganon. """
    intro_texto("DERROTA...")
    registrar_acao("Link cai perante o poder avassalador de Ganon.")
    registrar_acao("O Rei do Mal ri, enquanto a 'Decayed Master Sword' se desfaz em poeira.")
    registrar_acao("'Tolo! Achou que poderia me vencer?'")
    registrar_acao("O mundo é mergulhado em trevas eternas. A era do herói terminou.")
    registrar_acao("\n--- FIM DE JOGO ---")

# --- FUNÇÃO PRINCIPAL ---

def main():
    """
    Função principal que executa a sequência de história e batalhas do jogo.
    """
    
    # --- ATO 1: O INÍCIO E AGAHNIM ---
    
    # Criando personagens
    heroi = Heroi('Link', 30, 100, 20, 10, 'Lendário')
    vilao1 = Vilao('Agahnim', 200, 100, 18, 8, 'Média')
    npc = Personagem('Zelda', 28, 50, 5, 5) # Refém/Companheira

    # Usando listas para armazenar personagens
    lista_herois = [heroi]
    lista_viloes = [vilao1]
    lista_npcs = [npc]

    intro_texto("ATO 1: O FEITICEIRO SOMBRIO")
    registrar_acao(f"Nosso herói: {lista_herois[0]}")
    registrar_acao(f"O primeiro vilão: {lista_viloes[0]}")
    registrar_acao(f"A princesa: {lista_npcs[0]}")

    # Sistema de interação com diálogos
    linha_separadora()
    vilao1.dialogar(heroi, "Você nunca salvará a princesa, verme!")
    heroi.dialogar(vilao1, "Seu reinado de terror acaba aqui, Agahnim!")
    
    # Inicia a primeira batalha
    vitoria_b1 = batalha(heroi, vilao1)
    
    if not vitoria_b1:
        registrar_acao("A jornada de Link termina antes mesmo de começar...")
        mostrar_log()
        sys.exit() # Fim do jogo se perder a primeira batalha

    # --- ATO 2: O ACAMPAMENTO E GHIRAHIM ---
    
    interludio_acampamento(heroi, npc)
    
    registrar_acao("Enquanto caminham pelos campos, uma figura demoníaca surge das sombras.")
    vilao2 = Vilao('Ghirahim', 150, 150, 25, 12, 'Alta')
    lista_viloes.append(vilao2)
    
    intro_texto("ATO 2: O SENHOR DEMONÍACO")
    registrar_acao(f"Um novo desafio: {vilao2}")
    
    vilao2.dialogar(heroi, "Que interessante... Um humano patético tentando brincar de herói.")
    registrar_acao("Zelda se posiciona ao lado de Link: 'Não vamos deixar você passar!'")
    registrar_acao("A presença de Zelda inspira Link! Ataque aumentado em 10% nesta batalha!")
    
    # Boost de Zelda (arredondado)
    boost_zelda = round(heroi.ataque * 0.10)
    heroi.ataque += boost_zelda
    
    vitoria_b2 = batalha(heroi, vilao2)
    
    # Remove o boost após a batalha
    heroi.ataque -= boost_zelda
    
    if not vitoria_b2:
        registrar_acao("Ghirahim derrota Link e captura Zelda... O mundo está perdido.")
        mostrar_log()
        sys.exit()

    # --- ATO 3: A ESPADA E O MESTRE ZONAI ---

    registrar_acao("Ghirahim é derrotado e se dissolve, deixando cair sua espada...")
    registrar_acao("Link pega a 'Decayed Master Sword'!")
    
    # Upgrade da Decayed Master Sword (arredondado)
    aumento_espada = round(heroi.ataque * 0.35)
    heroi.ataque += aumento_espada
    heroi.chance_acerto = 0.60 # Reduz a chance de acerto para 60%
    
    registrar_acao(f"PODER CORROMPIDO: Ataque aumentado em {aumento_espada} (Total: {heroi.ataque})")
    registrar_acao(f"PREÇO DO PODER: Chance de Acerto reduzida para 60%.")
    
    interludio_mestre_zonai(heroi, npc)

    # --- ATO FINAL: O REI DO MAL ---
    
    registrar_acao("\nO Mestre Zonai aponta para o castelo distante, agora envolto em energia sombria.")
    registrar_acao("Mestre Zonai: 'Ganon, o Rei do Mal, foi atraído pelo poder da sua espada.'")
    registrar_acao("Mestre Zonai: 'Ele o espera no topo da torre. Esta é a batalha final.'")
    
    vilao_final = Vilao('Ganon, Rei do Mal', 1000, 250, 35, 20, 'Extrema')
    lista_viloes.append(vilao_final)

    intro_texto("ATO FINAL: O REI DO MAL")
    heroi.dialogar(npc, "Fique aqui, Zelda. É muito perigoso.")
    npc.dialogar(heroi, "Não. Eu vou com você. Até o fim.")
    
    linha_separadora()
    registrar_acao("Link e Zelda invadem o castelo e chegam ao topo da torre.")
    registrar_acao(f"Lá, ele os espera: {vilao_final}")
    
    vilao_final.dialogar(heroi, "Então o pequeno herói chegou. E trouxe minha espada corrompida...")
    vilao_final.dialogar(heroi, "Você apenas nutriu meu poder. Prepare-se para morrer!")
    
    vitoria_final = batalha(heroi, vilao_final)

    # --- ENCERRAMENTO ---
    
    if vitoria_final:
        final_bom(heroi, npc)
    else:
        final_ruim()

    # Exibe o log de ações no final
    mostrar_log()

if __name__ == "__main__":
    main()