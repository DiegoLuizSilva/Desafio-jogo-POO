import os
from colorama import Fore, Style, init

init(autoreset=True)

COR_ERRO = Fore.RED
COR_SUCESSO = Fore.GREEN
COR_AVISO = Fore.YELLOW
COR_TITULO = Fore.CYAN
COR_DESTAQUE = Fore.MAGENTA
COR_INFO = Fore.WHITE
COR_CURA = Fore.GREEN
COR_VILAO = Fore.RED
COR_HEROI = Fore.BLUE
COR_NPC = Fore.YELLOW
COR_VIDA = Fore.GREEN
COR_ATAQUE = Fore.RED
COR_DEFESA = Fore.BLUE

log_de_acoes = []

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def registrar_acao(acao, logar=True):
    print(acao)
    if logar:
        log_de_acoes.append(acao)

def mostrar_log():
    limpar_tela()
    linha_separadora('=')
    print(COR_TITULO + "📜 HISTÓRICO DE AÇÕES DO JOGO 📜")
    linha_separadora('=')
    if not log_de_acoes:
        print(COR_AVISO + "(Nenhuma ação registrada)")
    else:
        for i, acao in enumerate(log_de_acoes):
            print(f"{i+1}. {acao}")
    linha_separadora('=')

def linha_separadora(char='-', tam=60):
    print(char * tam)

def intro_texto(texto):
    limpar_tela()
    linha_separadora('=')
    registrar_acao(COR_TITULO + f"⚔️  {texto.upper()}  ⚔️")
    linha_separadora('=')