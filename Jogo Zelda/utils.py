# Lista global para armazenar o histórico de eventos
import colorama
log_de_acoes = []

def registrar_acao(acao, logar=True):
    """
    Imprime uma ação na tela e, opcionalmente, a adiciona ao log.
    """
    print(acao)
    if logar:
        log_de_acoes.append(acao)

def mostrar_log():
    """
    Exibe o histórico completo de ações do jogo.
    """
    linha_separadora('=')
    print("📜 HISTÓRICO DE AÇÕES DO JOGO 📜")
    linha_separadora('=')
    if not log_de_acoes:
        print("(Nenhuma ação registrada)")
    else:
        for i, acao in enumerate(log_de_acoes):
            print(f"{i+1}. {acao}")
    linha_separadora('=')

def linha_separadora(char='-', tam=60):
    """
    Imprime uma linha separadora para formatar a saída.
    """
    print(char * tam)

def intro_texto(texto):
    """
    Formata um texto de introdução ou título de seção.
    """
    linha_separadora('=')
    registrar_acao(f"⚔️  {texto} ⚔️", logar=False)
    linha_separadora('=')