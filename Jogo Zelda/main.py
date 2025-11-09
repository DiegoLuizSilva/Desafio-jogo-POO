import sys
from personagem import Personagem
from heroi import Heroi
from vilao import Vilao
from utils import registrar_acao, mostrar_log, linha_separadora, intro_texto, limpar_tela, COR_TITULO, COR_DESTAQUE, COR_ERRO, COR_SUCESSO, COR_AVISO, COR_INFO, COR_NPC

def batalha(heroi, vilao):
    intro_texto(f"A BATALHA COMEÇA: {heroi.nome} vs. {vilao.nome}")
    
    turno = 1
    while heroi.esta_vivo and vilao.esta_vivo:
        limpar_tela()
        linha_separadora()
        registrar_acao(COR_TITULO + f"--- TURNO {turno} ---", logar=False)
        
        heroi.aplicar_efeitos_turno()
        if not heroi.esta_vivo: 
            break
            
        heroi.mostrar_status()
        vilao.mostrar_status()
        
        opcoes = {"1": "Atacar", "2": "Tentar Esquivar"}
        mapa_acoes = {'1': 'atacar', '2': 'esquivar'}
        idx_atual = 3 

        if heroi.inventario.get('pocao_cura', 0) > 0 and heroi.vida_atual <= 50:
            opcoes[str(idx_atual)] = f"Usar Poção de Cura ({heroi.inventario['pocao_cura']})"
            mapa_acoes[str(idx_atual)] = 'pocao_cura'
            idx_atual += 1

        if heroi.inventario.get('pocao_regen', 0) > 0 and heroi.efeito_regen == 0:
            opcoes[str(idx_atual)] = f"Usar Poção de Regeneração ({heroi.inventario['pocao_regen']})"
            mapa_acoes[str(idx_atual)] = 'pocao_regen'
            idx_atual += 1
        
        opcoes_str = " | ".join([f"[{k}] {v}" for k, v in opcoes.items()])
        registrar_acao(COR_DESTAQUE + f"\nAções de {heroi.nome}: {opcoes_str}", logar=False)
        
        escolha = input(COR_INFO + "Escolha sua ação: ")
        
        acao_escolhida = mapa_acoes.get(escolha)
        acao_sucesso = True 

        if acao_escolhida == 'atacar':
            heroi.atacar(vilao)
        elif acao_escolhida == 'esquivar':
            heroi.tentando_esquivar = True
            registrar_acao(f"🛡️ {heroi.nome} se prepara para esquivar do próximo ataque!")
        elif acao_escolhida == 'pocao_cura':
            acao_sucesso = heroi.usar_pocao_cura()
        elif acao_escolhida == 'pocao_regen':
            acao_sucesso = heroi.usar_pocao_regen()
        else:
            registrar_acao(COR_ERRO + "Opção inválida. Herói perde o turno!")
            acao_sucesso = True 

        if not acao_sucesso:
            registrar_acao(COR_ERRO + "Ação falhou! Tente novamente no próximo turno.", logar=False)
            continue 

        if vilao.esta_vivo:
            vilao.atacar(heroi)
            
        turno += 1

    linha_separadora()
    if heroi.esta_vivo:
        registrar_acao(COR_SUCESSO + f"🎉 VITÓRIA! {heroi.nome} derrotou {vilao.nome}! 🎉")
    else:
        registrar_acao(COR_ERRO + f"DEFEAT! {heroi.nome} foi derrotado por {vilao.nome}...")
    linha_separadora()
    input(COR_INFO + "Pressione Enter para continuar...")
    return heroi.esta_vivo

def interludio_mestre_zonai(heroi, npc):
    limpar_tela()
    intro_texto("INTERLÚDIO: A ESPADA CORROMPIDA")
    heroi.dialogar(npc, "Mestre Zonai, o que aconteceu com minha espada? Ela... ela está sombria.")
    
    registrar_acao(COR_NPC + "\n[Mestre Zonai olha para a espada com pesar]:")
    registrar_acao(COR_NPC + f"\"A 'Espada Mestra' que você empunha, {heroi.nome}, não é o que parece.\"")
    registrar_acao(COR_NPC + "\"Ela é a 'Espada Corrompida', uma arma que drena a escuridão... para si mesma.\"")
    registrar_acao(COR_NPC + "\"Ela amplifica o poder do usuário, mas a um custo terrível: ela atrai o mal.\"")
    
    heroi.dialogar(npc, "Então... eu atraí o Rei do Mal até aqui? Eu sou o culpado?")
    registrar_acao(COR_NPC + "\"Culpado ou não, é o seu destino empunhá-la. O poder dela agora é seu.\"")
    
    input(COR_INFO + "\nPressione Enter para aceitar o poder...")

def run_game():
    limpar_tela()
    
    heroi = Heroi('Link', 25, 100, 20, 10, 'Lendário')
    npc = Personagem('Zelda', 26, 50, 5, 5) 
    refem = Personagem('Impa', 80, 30, 5, 2)
    
    lista_viloes = [
        Vilao('Bokoblin', 100, 50, 15, 5, 'Baixa'),
        Vilao('Moblin', 150, 80, 20, 10, 'Média'),
    ]
    
    intro_texto(f"Bem-vindo à Aventura de {heroi.nome}!")
    heroi.dialogar(npc, "Fique segura, Zelda. Eu vou resgatar a Impa.")
    npc.dialogar(heroi, "Tome cuidado, Link! Os viloes são fortes.")
    
    input(COR_INFO + "Pressione Enter para começar a jornada...")
    
    for vilao in lista_viloes:
        vitoria = batalha(heroi, vilao)
        if not vitoria:
            registrar_acao(COR_ERRO + "O Herói foi derrotado. Fim de jogo.")
            sys.exit() 
            
    heroi.salvar_refem(refem)
    
    aumento_espada = 15
    heroi.ataque += aumento_espada
    heroi.chance_acerto = 0.60
    
    registrar_acao(COR_DESTAQUE + f"\\nA 'Espada Mestra' absorve a energia dos viloes derrotados!")
    registrar_acao(COR_DESTAQUE + f"PODER CORROMPIDO: Ataque aumentado em {aumento_espada} (Total: {heroi.ataque})")
    registrar_acao(COR_ERRO + f"PREÇO DO PODER: Chance de Acerto reduzida para 60%.")
    
    interludio_mestre_zonai(heroi, npc)
    
    registrar_acao(COR_NPC + "\nO Mestre Zonai aponta para o castelo distante, agora envolto em energia sombria.")
    registrar_acao(COR_NPC + "Mestre Zonai: 'Ganon, o Rei do Mal, foi atraído pelo poder da sua espada.'")
    registrar_acao(COR_NPC + "Mestre Zonai: 'Ele o espera no topo da torre. Esta é a batalha final.'")
    
    vilao_final = Vilao('Ganon, Rei do Mal', 1000, 250, 35, 20, 'Extrema')
    lista_viloes.append(vilao_final)

    intro_texto("ATO FINAL: O REI DO MAL")
    heroi.dialogar(npc, "Fique aqui, Zelda. É muito perigoso.")
    npc.dialogar(heroi, "Não. Eu vou com você. Até o fim.")
    
    linha_separadora()
    registrar_acao("Link e Zelda invadem o castelo e chegam ao topo da torre.")
    registrar_acao(f"Lá, ele os espera: {vilao_final}")
    
    vitoria_final = batalha(heroi, vilao_final)
    
    if vitoria_final:
        intro_texto("FINAL: A LUZ RESTAURADA")
        registrar_acao(COR_SUCESSO + "Ganon é derrotado! A escuridão se dissipa.")
        heroi.dialogar(npc, "Conseguimos, Zelda. Acabou.")
        npc.dialogar(heroi, "Nós conseguimos, Link. Juntos.")
    else:
        intro_texto("FINAL: A ESCURIDÃO VENCE")
        registrar_acao(COR_ERRO + "Ganon ri enquanto a luz de Hyrule se apaga...")

    linha_separadora('=')
    log_final = input(COR_AVISO + "\nDeseja ver o log completo da aventura? (s/n): ").lower()
    if log_final == 's':
        mostrar_log()
    
    registrar_acao(COR_TITULO + "\n--- FIM DE JOGO ---")

if __name__ == "__main__":
    run_game()