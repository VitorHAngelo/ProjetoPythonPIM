import os
from datetime import datetime
from time import sleep


# ============= FUNÇÕES GERAIS =============
def limpar_console():
    """Função para limpar o console"""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def get_horario() -> datetime:
    """Retorna a data/horário atual

    **Retorna**:
        _datetime_: data horario"""
    return datetime.now()


def simular_carregamento(mensagem_carregamento, mensagem_completo):
    """Função para efeito estético, simula que o programa está carregando
    **Argumentos:**
        mensagem_carregamento (_str_): Ex: 'Carregando menu'
        mensagem_completo (_str_): Ex: 'Menu carregado!'
    """
    simbolos = ["\\", "|", "/", "-"] * 4
    limpar_console()
    for i in simbolos:
        print(f"{mensagem_carregamento} {i}")
        sleep(0.1)
        limpar_console()
    print(mensagem_completo)
