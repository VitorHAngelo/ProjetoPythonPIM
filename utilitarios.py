import os
from datetime import datetime


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
