import textos
import json
import os
from sys import exit
from csv import DictWriter
from hashlib import sha256
from dotenv import get_key
from cryptography.fernet import Fernet
from aprender import *
from utilitarios import limpar_console, get_horario, simular_carregamento
from matplotlib import pyplot as plt
from datetime import datetime
from random import choice

# Variáveis globais
usuario = None
horario_login = None

# Constantes
FILES_PATH = "./files/"
USER_DATA_PATH = FILES_PATH + "user_data.json"
ENV_PATH = FILES_PATH + ".env"
CONTADOR_QUIZ = "contador_quiz.json"
IDADE_MINIMA_USUARIO = 5
QUESTOES_POR_QUIZ = 5


# ============= ARQUIVO JSON =============
def gerar_salt():
    """Função para gerar salt hexadecimal usando urandom(n bytes)
    Converte para hexadecimal, retorna em _str_
    """
    return os.urandom(8).hex()


def criar_fernet():
    """Criar objeto Fernet para criptografar arquivo JSON."""
    fernet_key = get_key(ENV_PATH, "FERNET_KEY")
    fernet = Fernet(fernet_key)
    del fernet_key
    return fernet


def criar_json():
    """Cria arquivo JSON, caso ainda não exista."""
    if not os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, "w") as file:
            json.dump({}, file)
        criptografar_json()


def get_usuario(cod_aluno: str):
    """cod_aluno espera receber em _str_ o RA do aluno.\n
    Se não existir retorna None.\n
    **Retorna:**
        _dict_: dicionário com dados do usuário
    """
    file_data = descriptografar_json()
    if cod_aluno not in file_data:
        return None
    elif cod_aluno in file_data and file_data[cod_aluno]["nome"] == None:
        return None
    return {"RA": cod_aluno, **file_data[cod_aluno]}


def gerar_ra():
    """Abre o JSON para checar o último RA cadastrado e retorna _int_ incrementado.\n
    Ex: Se o último for RA004, ele retorna 5"""
    file_data = descriptografar_json()
    if not file_data:
        return 0
    else:
        ra = list(file_data)[-1]
        return int(ra[2:]) + 1


def gerar_dados_seguros() -> dict:
    """Gera _dict_ com todos usuários e seus dados, removendo os dados sensíveis."""
    if not os.path.exists(USER_DATA_PATH):
        print("Arquivo .JSON inexistente")
        return
    file_data = descriptografar_json()
    dados_seguros = {}
    for user in file_data:
        dados_seguros[user] = file_data[user]
        dados_seguros[user].pop("senha")
        dados_seguros[user].pop("salt")
    del file_data
    return dados_seguros


# ============= ARQUIVO ENV =============


def criar_env():
    """Verifica se o arquivo .env (que guarda variáveis importantes do programa em um
    arquivo oculto para maior segurança, arquivo este que nunca deve ser enviado para
    o repositório, por questões de segurança, ou seja, é sempre gerado um novo na
    primeira execução em um ambiente novo).
    Caso o arquivo não exista, ele cria e gera novas chaves fernet e pepper para o mesmo.
    """
    if not os.path.exists("files/.env"):
        pepper = os.urandom(8).hex()
        fernet_key = Fernet.generate_key().decode()
        with open("files/.env", "w") as file:
            file.write(
                f"PEPPER={pepper}\nFERNET_KEY={fernet_key}\nADMIN_PW=ads2025unip"
            )


# ============= ARQUIVO CSV =============
def gerar_csv():
    """Cria arquivo .csv (comma separated values / valores separados por vírgula).\n
    Arquivo este que contém uma tabela dos cadastros, sem os dados sensíveis."""
    file_data = gerar_dados_seguros()
    if not file_data:
        print("Não existem dados a serem gerados.")
    else:
        primeiro_ra = list(file_data)[0]
        campos = []
        for campo in file_data[primeiro_ra].keys():
            campos.append(campo)
        campos.insert(0, "RA")
        with open(FILES_PATH + "user_data.csv", mode="w", newline="") as file:
            writer = DictWriter(file, fieldnames=campos)
            writer.writeheader()
            for cod_aluno, usuario in file_data.items():
                linha = {"RA": cod_aluno, **usuario}
                writer.writerow(linha)


# ============= CRIPTOGRAFIA =============
def criptografar_json():
    """Criptografa os dados vulneráveis do JSON, não queremos que o JSON fique
    desprotegido NUNCA, portanto, será utilizado somente quando o arquivo for criado
    e só conter um dict vazio. Nas vezes subsequentes, sobrescreveremos já criptografado.
    """
    fernet = criar_fernet()
    with open(USER_DATA_PATH, "r", encoding="utf-8") as file:
        file_data = file.read()
    dados_bytes = file_data.encode()
    dados_criptografados = fernet.encrypt(dados_bytes)
    with open(USER_DATA_PATH, "wb") as file:
        file.write(dados_criptografados)


def descriptografar_json():
    """Função para obter os dados do JSON. (Não deixa o arquivo descriptografado!!! Só
    puxa os dados criptografados, traduz e retorna como _dict_)"""
    with open(USER_DATA_PATH, "rb") as file:
        dados_criptografados = file.read()
    dados_json = criar_fernet().decrypt(dados_criptografados).decode()
    "fernet = criar_fernet()"  # Instanciariamos o fernet e atribuiriamos a variavel fernet
    "dados_descriptografados = fernet.decrypt(dados_criptografados)"
    "dados_json = dados_descriptografados.decode()"
    return json.loads(dados_json).copy()


def update_json(cod_aluno, usuario):
    """Função utilizada para atualizar o JSON, sem que ele fique com os dados desproteg.
    em nenhum momento.\n
    **Argumentos:**
    cod_aluno: RA em _str_\n
    usuario: _dict_ com dados do usuário"""
    file_data = descriptografar_json()
    usuario_sem_ra = dict(list(usuario.items())[1:])
    if cod_aluno in file_data:
        file_data[cod_aluno].update(usuario_sem_ra)
    else:
        file_data[cod_aluno] = dict(usuario_sem_ra)
    dados_bytes = json.dumps(file_data).encode()
    dados_criptografados = criar_fernet().encrypt(dados_bytes)
    with open(USER_DATA_PATH, "wb") as file:
        file.write(dados_criptografados)


def verificar_duplicidade(nome, ano_nascimento):
    """Verifica se usuário com mesmo nome e ano de nascimento já existe no cadastro.

    **Retorno**:
        _boolean_: True caso positivo ou False se chegar ao fim do loop sem match.
    """
    file_data = descriptografar_json()
    for usuario in file_data:
        if (
            file_data[usuario]["nome"] == nome
            and file_data[usuario]["ano_nascimento"] == ano_nascimento
        ):
            return True
    return False


def get_idade(ano_nascimento) -> int:
    """
    Função recebe o ano de nascimento da pessoa e retorna a idade que ela terá após
    aniversário do ano atual.
    **Argumentos**:
        _int_: Ano de nascimento

    **Retorna**
        _int_: Idade
    """
    if ano_nascimento == None:
        return 0
    return datetime.now().year - ano_nascimento


def cadastro():
    """Função destinada a cadastrar um novo usuário e salvar no JSON"""
    usuario = {}
    print("Seja bem-vindo! Faremos seu cadastro a seguir:")
    while True:
        while True:  # Loop Nome
            nome = input("Insira seu nome com sobrenome: ").title()
            if not nome.replace(" ", "").isalpha():
                'nome = nome.replace(" ", "")'
                print("Utilize somente letras e espaços, por favor.")
            elif len(nome) < 3:
                print("Nome muito curto, favor insira um nome válido")
            else:
                break
        while True:  # Loop Idade
            ano_nascimento = input(
                f"Olá {' '.join(nome.split()[:2])}, por favor, insira seu ano de nascimento, com quatro dígitos: "
            )
            if not ano_nascimento.isdecimal() or len(ano_nascimento) != 4:
                print("Por gentileza, utilize quatro dígitos númericos.")
                continue
            ano_nascimento = int(ano_nascimento)
            if (
                get_idade(ano_nascimento) < IDADE_MINIMA_USUARIO
                or get_idade(ano_nascimento) > 120
            ):
                print("Insira um ano válido!")
            else:
                limpar_console()
                break
        while True:  # Loop Confirmação de dados
            confirmacao_dados = input(
                f"Verifique os dados inseridos:\nNome: {nome}\n\
Ano de nascimento: {ano_nascimento}\nDigite 'S' para continuar ou 'N' para começar novamente.\n"
            ).upper()
            if confirmacao_dados in ("S", "N"):
                break
        if confirmacao_dados == "N":
            limpar_console()
            continue
        if verificar_duplicidade(nome, ano_nascimento):
            input(
                "Usuário já cadastrado, faça seu login ou recupere seus dados.\n\
Aperte ENTER para retornar ao Menu.\n"
            )
            return
        while True:  # Loop Senha
            senha = input("Insira sua senha: ")
            limpar_console()
            senha2 = input("Insira sua senha novamente, por favor: ")
            limpar_console()
            if senha == senha2:
                if senha.isascii() and senha.count(" ") == 0 and len(senha) >= 6:
                    break
                else:
                    print(
                        "Senha inválida, favor utilizar ao menos 6 letras, números e caracteres \
especiais, espaços não são válidos."
                    )
                    continue
            else:
                print("Senhas diferentes, insira duas senhas iguais para continuar.")
        salt = gerar_salt()
        senha_hash = hashear_senha(senha, salt)
        cod_aluno = f"RA{gerar_ra():03d}"
        usuario = {
            "RA": cod_aluno,
            "nome": nome,
            "ano_nascimento": ano_nascimento,
            "senha": senha_hash,
            "materias": {
                "ciberseguranca": [],
                "logica": [],
                "python": [],
            },
            "minutos_uso": 0,
            "salt": salt,
        }
        print(
            f"""============================= ATENÇÃO =============================
Seu RA é: {cod_aluno}. ANOTE este código pois será utilizado para realizar seu login!
Aperte ENTER para prosseguir"""
        )
        input("===================================================================\n")
        update_json(cod_aluno, usuario)
        return


def hashear_senha(entrada_senha: str, salt: str):
    """Função para proteger senha do usuário, para que seja armazenado de forma segura
    e para que quando ele faça login, criptografamos a senha e então compararemos com a
    salva no arquivo .JSON (que sempre estará criptografada)
    **Argumentos:**
        entrada_senha (_str_): Senha crua inserida pelo usuário
        salt (_str_): String hexadecimal individual, armazenada no _dict_ de cada usuário
    **Retorna:**
        _str_: String hexadecimal com salt, pepper e criptog. sha256
    """
    senha_salt_pepper = salt + entrada_senha + str(get_key(ENV_PATH, "PEPPER"))
    objeto_hash = sha256(senha_salt_pepper.encode())
    return objeto_hash.hexdigest()


def gerar_grafico():
    # Criando subplots
    fig, ax1 = plt.subplots(nrows=2, ncols=2, figsize=(14, 9))
    fig.set_facecolor("lightgray")
    fig.suptitle("Representação gráfica do seu progresso em nosso programa!")
    # var recebe dict
    dados_seguros = gerar_dados_seguros()

    # GRAFICO MEDIA DA IDADE
    idade_aluno = int(get_idade(usuario["ano_nascimento"]))

    # calculo média
    soma_idades = 0
    soma_minutos = 0
    quantidade_idades_calculadas = 0

    for user in dados_seguros:
        idade_usuario = get_idade(dados_seguros[user]["ano_nascimento"])

        if idade_usuario != 0:  # Se usuário não tiver sido anonimizado
            soma_idades += idade_usuario
            quantidade_idades_calculadas += 1

        minutos_uso = int(dados_seguros[user]["minutos_uso"])
        soma_minutos += minutos_uso

    media_minutos = int(soma_minutos / len(dados_seguros))
    media_idades = soma_idades / quantidade_idades_calculadas

    posicao = [0, 6]
    rotulos = [
        "Sua Idade",
        f"Media das Idades ({quantidade_idades_calculadas} alunos)",
    ]

    ax1[0, 0].bar(
        posicao,
        [idade_aluno, media_idades],
        color="green",
        label="Idade",
        align="center",
        width=3,
    )
    ax1[0, 0].set_facecolor("lightgray")
    ax1[0, 0].set_xticks(posicao, rotulos)
    ax1[0, 0].set_title("Sua idade comparada a idade média dos outros alunos")
    ax1[0, 0].set_ylabel("Idade")

    # GRAFICO HORAS TOTAIS

    minutos_uso_usuario = int(usuario["minutos_uso"])

    posicao_grafico_minutos_totais = [0, 6]
    rotulos_grafico_minutos_totais = [
        "Seu tempo de uso",
        f"Media Geral de tempo de uso ({len(dados_seguros)} alunos)",
    ]

    media_minutos = 48
    ax1[0, 1].bar(
        posicao_grafico_minutos_totais,
        [minutos_uso_usuario, media_minutos],
        align="center",
        width=3,
    )
    # Calcular yticks:
    maior_tempo = max([minutos_uso_usuario, media_minutos])
    maior_tempo += 10 - (maior_tempo % 10)

    ax1[0, 1].set_xticks(posicao_grafico_minutos_totais, rotulos_grafico_minutos_totais)
    ax1[0, 1].set_yticks(range(0, maior_tempo + 1, 5))
    ax1[0, 1].set_facecolor("lightgray")
    ax1[0, 1].set_title("Seu tempo de uso do programa comparado a média dos alunos")
    ax1[0, 1].set_ylabel("Média de uso (minutos)")

    # GRAFICO HISTORICO ACERTOS
    acertos_python = usuario["materias"]["python"]
    acertos_logica = usuario["materias"]["logica"]
    acertos_ciberseguranca = usuario["materias"]["ciberseguranca"]

    total_tentativas = max(
        [len(acertos_python), len(acertos_ciberseguranca), len(acertos_logica)]
    )

    if not total_tentativas:
        total_tentativas = 1

    ax1[1, 0].plot(acertos_ciberseguranca, label="Cibersegurança", marker="o")
    ax1[1, 0].plot(acertos_logica, linestyle="dashed", label="Lógica", marker="o")
    ax1[1, 0].plot(acertos_python, linestyle="dotted", label="Python", marker="o")
    ax1[1, 0].set_facecolor("lightgray")
    ax1[1, 0].set_title("Cronograma de notas dos quizzes")
    ax1[1, 0].set_ylim(0, 5.5)
    ax1[1, 0].set_xticks(ticks=range(0, total_tentativas + 1))
    ax1[1, 0].hlines(
        y=[range(0, 6)], xmin=0, xmax=total_tentativas, color="tab:gray", alpha=0.2
    )

    ax1[1, 0].legend(facecolor="gainsboro")
    ax1[1, 0].set_ylabel("Nota")
    ax1[1, 0].set_xlabel("Tentativas")

    # GRAFICO TAXA DE ACERTO
    all_notas = []
    all_notas.extend(acertos_ciberseguranca)
    all_notas.extend(acertos_logica)
    all_notas.extend(acertos_python)

    #                 NOTAS       TENTATIVAS      NOTA MAXIMA
    pie_labels = ["Taxa de acertos", "Taxa de erros"]
    taxa_acerto = sum(all_notas) / (len(all_notas) * 5)
    ax1[1, 1].pie(
        [taxa_acerto, 1 - taxa_acerto],
        autopct="%1.1f%%",
        labels=pie_labels,
    )
    ax1[1, 1].set_title("Sua taxa de acerto de questões")
    ax1[1, 1].set_facecolor("lightgray")
    # ax1[1, 1].set_xlabel("Acertos")
    # ax1[1, 1].set_ylabel("Erros")
    plt.show()


def login() -> dict:
    """Função para realizar o login do usuário, interagindo com o usuário para pedir dados.
    **Retorna:**
        _dict_: Dicionário com os dados do usuário"""
    global usuario
    global horario_login
    while True:
        retorno_usuario = input(
            "Digite seu RA, ou 'voltar' para retornar ao menu.\n"
        ).upper()
        if retorno_usuario == "VOLTAR":
            return
        usuario = get_usuario(retorno_usuario)
        limpar_console()
        if usuario:
            break
        print("RA inválido. ", end="")
    while True:
        entrada_senha = input(
            f'Olá, {" ".join(usuario["nome"].split()[:2])}! Favor, insira sua senha: '
        )
        limpar_console()
        if entrada_senha.upper() == "VOLTAR":
            return
        senha_hash = hashear_senha(entrada_senha, usuario["salt"])
        if senha_hash == usuario["senha"]:
            break
        else:
            print("Senha incorreta. Se desejar, digite 'voltar'")
    usuario.pop("senha")
    usuario.pop("salt")
    input("Login realizado com sucesso! Aperte ENTER para continuar.\n")
    horario_login = get_horario()
    return usuario


def recuperacao():
    """
    Função para ajudar o usuário a recuperar sua senha ou RA, através do console.
    Após o auxílio, retorna o usuário ao menu_login
    """
    while True:
        escolha = None
        while escolha not in ("1", "2", "3"):
            escolha = input(
                """O que você precisa?
1 - Perdi minha senha
2 - Perdi meu RA
3 - Voltar ao menu\n"""
            )
        if escolha == "1":
            cod_aluno = input("Para recuperarmos sua senha, insira o seu RA: ").upper()
            usuario = get_usuario(cod_aluno)
            if usuario is None:
                print("RA inválido.")
                continue
            else:
                entrada_nome = input(
                    "Insira seu nome conforme informado no cadastro: "
                ).title()
                if entrada_nome != usuario["nome"]:
                    print("Nome incorreto.")
                    continue
                else:
                    while True:
                        entrada_senha = input(
                            f'Olá, {" ".join(usuario["nome"].split()[:2])}! Favor, insira sua nova senha:\n'
                        )
                        limpar_console()
                        entrada_senha1 = input("Repita a senha: ")
                        limpar_console()
                        if entrada_senha == entrada_senha1:
                            if (
                                entrada_senha.isascii()
                                and entrada_senha.count(" ") == 0
                                and len(entrada_senha) >= 6
                            ):
                                usuario["senha"] = hashear_senha(
                                    entrada_senha, usuario["salt"]
                                )
                                update_json(cod_aluno, usuario)
                                print("Senha alterada com sucesso!")
                                return
                            else:
                                print(
                                    "Senha inválida, favor utilizar ao menos 6 letras, números e caracteres \
especiais, espaços não são válidos."
                                )
                                continue
                        else:
                            print(
                                "Senhas diferentes, insira duas senhas iguais para continuar."
                            )
        elif escolha == "2":
            entrada_nome = input("Para recuperarmos seu RA, insira seu nome: ").title()
            possiveis_usuarios = []
            file_data = descriptografar_json()
            for user in file_data.keys():
                if file_data[user]["nome"] == entrada_nome:
                    possiveis_usuarios.append(user)
            if not possiveis_usuarios:
                print("Sinto muito, não possível encontrar alguém com este nome.")
                continue
            else:
                print(
                    "Encontramos possíveis usuários, precisaremos de sua senha para ter certeza."
                )
                entrada_senha = input("Insira a senha cadastrada, por gentileza: ")
                limpar_console()
                for cod_aluno in possiveis_usuarios:
                    senha_hash = hashear_senha(
                        entrada_senha, file_data[cod_aluno]["salt"]
                    )
                    if senha_hash == file_data[cod_aluno]["senha"]:
                        input(
                            f"Sucesso! ANOTE seu RA: {cod_aluno} e depois aperte ENTER"
                        )
                        return
                print("Não foi possível localizar seu cadastro.")
                continue
        else:
            return


def quiz():
    """Função destinada a atividade QUIZ do programa, onde testa os conhecimentos do
    usuário com base no que foi ensinado na parte de #Aprender.
    Constituídos por 5 questões cada quiz, apresenta a resposta correta ao usuário,
    adiciona o resultado de sua pontuação ao próprio perfil."""
    global usuario
    limpar_console()
    while True:
        escolha = input(textos.menu_quiz)
        materias = {1: "logica", 2: "python", 3: "ciberseguranca"}
        while escolha not in ("1", "2", "3", "4"):
            limpar_console()
            escolha = input(textos.menu_quiz)
        if escolha == "4":
            return
        escolha = materias[int(escolha)]
        variavel_texto_materia = f"questoes_{escolha}"
        nota = 0
        for questao, alternativa in getattr(textos, variavel_texto_materia).items():
            limpar_console()
            entrada_usuario = input(questao).upper()
            while entrada_usuario not in ("A", "B", "C", "D"):
                limpar_console()
                print("Resposta inválida, utiliza as letras das alternativas.")
                entrada_usuario = input(questao).upper()
            if entrada_usuario == alternativa[0]:
                nota += 1
                print(
                    f"{choice(textos.mensagens_resposta_correta).format(entrada_usuario)} \
\n{alternativa[1]}\nAperte ENTER para continuar. "
                )
                input()
            else:
                print(
                    f"{choice(textos.mensagens_resposta_incorreta).format(entrada_usuario)} \
\n{alternativa[1]}\nAperte ENTER para continuar. "
                )
                input()
        input(
            f"Sua nota total do Quiz de {escolha.title()} foi {nota} de um total de 5 \
questões.\nAperte ENTER para continuar."
        )
        limpar_console()
        print("Quer fazer outro Quiz ou voltar para o Menu?")
        usuario["materias"][escolha].append(nota)
        update_json(usuario["RA"], usuario)


def editar_conta():
    """Imprime menu e através dele, ajuda usuário a editar sua conta, como alterar senha
    ou anonimizar seus dados.\n
    Caso usuário informe sua senha incorreta ou escolha anonimizar seus dados, retorna
    _str_ 'inseguro', com o intuito de indicar para a função origem para fazer o logoff()
    do usuário atual."""
    global usuario
    escolha = None
    while escolha not in ("1", "2", "3"):
        limpar_console()
        escolha = input(textos.menu_conta.format(" ".join(usuario["nome"].split()[:2])))
    limpar_console()
    if escolha == "1":  # Mudar senha
        usuario_completo = get_usuario(usuario["RA"])
        entrada_senha = input(
            f'Olá, {" ".join(usuario["nome"].split()[:2])}! Favor, insira sua senha atual: '
        )
        limpar_console()
        senha_hash = hashear_senha(entrada_senha, usuario_completo["salt"])
        if senha_hash != usuario_completo["senha"]:
            simular_carregamento(
                "Senha incorreta, saindo de sua conta...",
                "Logoff realizado por segurança",
            )
            logoff()
            return "inseguro"
        while True:  # Loop Senha
            senha = input("Insira sua nova senha: ")
            limpar_console()
            senha2 = input("Insira novamente a nova senha, por favor: ")
            limpar_console()
            if senha == senha2:
                if senha.isascii() and senha.count(" ") == 0 and len(senha) >= 6:
                    break
                else:
                    print(
                        "Senha inválida, favor utilizar ao menos 6 letras, números e/ou caracteres \
especiais, espaços não são válidos."
                    )
                    continue
            else:
                print("Senhas diferentes, insira duas senhas iguais para continuar.")
        senha_hash = hashear_senha(senha, usuario_completo["salt"])
        usuario["senha"] = senha_hash
        update_json(usuario["RA"], usuario)
        input("Senha alterada com sucesso, aperte ENTER para continuar.")

    elif escolha == "2":  # Anonimização
        entrada_usuario = input(
            """
Somente escolha esta opção caso queira remover os seus dados do sistema de modo que
todos seus dados pessoais sejam apagados, restando somente suas notas como medida de
estatística (completamente anônimos).
Caso esteja decidido(a) a realizar este passo, favor inserir sua senha, ou aperte
ENTER para voltar: """
        )
        usuario_completo = get_usuario(usuario["RA"])
        senha_hash = hashear_senha(entrada_usuario, usuario_completo["salt"])
        if senha_hash == usuario_completo["senha"]:
            confirmacao = input(
                "\nVOCÊ TER CERTEZA? NÃO SERÁ POSSÍVEL RECUPERAR SUA CONTA!\
\nDIGITE 'CANCELAR' PARA DESISTIR OU 'ENTER' PARA CONTINUAR: "
            ).lower()
            if confirmacao == "cancelar":
                return
            usuario["nome"], usuario["ano_nascimento"] = None, None
            usuario["senha"] = hashear_senha(
                os.urandom(8).hex(), usuario_completo["salt"]
            )
            update_json(usuario["RA"], usuario)
            usuario = None
            simular_carregamento("Excluindo dados...", "Dados excluídos!")
            return "inseguro"


def ranking(materia) -> None:
    """
    Função destinada a imprimir o ranking da matéria passada como argumento.

    **Argumentos**:
        _str_: materia
    """
    dados_ranking = []
    for user in descriptografar_json().values():
        lista_usuario = []
        for chave, valor in user.items():
            if chave == "nome":
                lista_usuario.append(valor)
            elif chave == "materias":
                if not valor.get(materia, []):
                    lista_usuario = [0, " "]
                else:
                    lista_usuario.insert(0, (valor[materia][0]))
        dados_ranking.append(lista_usuario)

    dados_ranking = sorted(dados_ranking, reverse=True)
    limpar_console()
    print(f" RANKING {materia.upper()} ".center(40, "="))
    print(f"Nome".center(26) + " Pontuação".center(14))
    print(f"|".rjust(27))
    medalhas = ["🥇 ", "🥈 ", "🥉 "]
    contagem = 0

    for index in range(0, 9):
        if index > len(dados_ranking) - 1:
            print("".ljust(26) + "|")
        else:
            if dados_ranking[index][0] == 0:
                continue
            print(" ".join(dados_ranking[index][1].split()[:2]).ljust(23, " "), end="")
            if contagem < 3:
                print(medalhas[contagem], end="")
            else:
                print("   ", end="")
            print("|" + str(dados_ranking[index][0]).rjust(7))
            contagem += 1


def logoff():
    """Função destinada a contabilizar o tempo que o usuário utilizou o programa e
    incrementar em seus perfil, também define a variável global usuario como None
    indicando que não sessão ativa."""
    global usuario
    tempo_uso = get_horario() - horario_login
    usuario["minutos_uso"] += int(tempo_uso.total_seconds() // 60)
    update_json(usuario["RA"], usuario)
    usuario = None
    print("Logoff realizado.")


def menu_aprender():
    """Menu destinado a escolha de qual lição o usuário quer fazer."""
    while True:
        escolha = None
        while escolha not in ("1", "2", "3", "4"):
            limpar_console()
            escolha = input(textos.menu_aprender)
        limpar_console()
        if escolha == "1":  # Lógica
            menu_aprender_logica(textos)
        elif escolha == "2":  # Python
            menu_aprender_python(textos)
        elif escolha == "3":  # Cibersegurança
            print(textos.aprender_ciberseguranca)
            input("Aperte ENTER para voltar.")
        elif escolha == "4":  # Voltar
            return


def menu_ranking():
    """Função ao menu para o usuário escolher sobre qual matéria ele quer ver o ranking"""
    limpar_console()
    dict_materias = {1: "logica", 2: "python", 3: "ciberseguranca"}
    escolha = None
    while escolha not in ("1", "2", "3", "4"):
        escolha = input(textos.menu_ranking)
    if escolha == "4":
        return
    else:
        ranking(dict_materias[int(escolha)])
        input("Aperte enter para voltar ao menu.")


def menu_principal():
    """Menu utilizado quando usuário está logado, ou seja:
    variável global 'usuario' está com usuário ativo no momento."""
    global usuario
    while True:
        escolha = None
        while escolha not in ("1", "2", "3", "4", "5", "6", "7"):
            limpar_console()
            escolha = input(
                textos.menu_principal.format(" ".join(usuario["nome"].split()[:2]))
            )
        if escolha == "1":  # Aprender
            menu_aprender()
        elif escolha == "2":  # Quiz
            quiz()
        elif escolha == "3":  # Progresso
            gerar_grafico()
        elif escolha == "4":  # Ranking
            menu_ranking()
        elif escolha == "5":  # Editar conta
            condicao = editar_conta()
            if condicao == "inseguro":
                return
        elif escolha == "6":  # Logoff
            logoff()
            limpar_console()
            return
        elif escolha == "7":  # Sair
            logoff()
            simular_carregamento("Saindo do programa", "Até a próxima!")
            exit()


def main():
    """Menu principal inicial com funções para acessar o programa com sua conta, ou criar uma."""
    criar_env()
    criar_json()
    global usuario
    while True:
        escolha = None
        limpar_console()
        if usuario is not None:
            menu_principal()
        while escolha not in ("1", "2", "3", "4", "5"):
            escolha = input(textos.menu_login)
            limpar_console()
        if escolha == "1":
            usuario = login()
        elif escolha == "2":
            cadastro()
        elif escolha == "3":
            recuperacao()
        elif escolha == "4":
            simular_carregamento("Saindo do programa", "Até a próxima.")
            exit()
        elif escolha == "5":
            senha = input("Digite a senha de admin: ")
            if senha == get_key(ENV_PATH, "ADMIN_PW"):
                gerar_dados_seguros()
                gerar_csv()
                limpar_console()


# # Função Quiz ou Menu, quando chamada no fim de qualquer conteudo sobre Python exibe a pergunta para o usuario se ele deseja fazer um quiz sobre o conteudo ou voltar ao menu
# def quizOUmenu():
#     print("\nDeseja fazer um Quiz sobre o conteúdo estudado ou voltar ao menu? ")
#     global escolha
#     escolha = input("Digite 1 para o Quiz e 2 para voltar ao menu: ")
#     return


# # Função sair. Quando chamada exibe a pergunta se o usuario realmente deseja sair do programa
# def Sair():
#     print("\nVocê escolheu sair do programa, tem certeza que deseja sair? ")
#     ver = str(input("Digite sim para sair e não para voltar ao menu\n"))
#     if ver.lower() == "sim":
#         print("Encerrando o Programa. . .")
#     elif ver.lower() == "não":
#         pass
#     else:
#         print("\nA opção escolhida é invalida, Digite conforme orientado.")
#     return


# função onde está a estrutura condicional do programa
def Ifs():
    global escolha
    global comecar
    global nome
    global idade
    global senha
    global horasTotais
    global qtdAcertos
    global qtdErros
    global mediaHoras
    global mediaAcertos
    global mediaErros
    global mediaIdade
    escolha = str(input("\nDigite o número referente a sua escolha para acessa-la: "))
    if escolha == "1":
        print("\nOpção Aprender escolhida. Escolha qual conteúdo estudar: ")
        print(" 1 - Comando Print()")
        print(" 2 - Comando Input()")
        escolha = input("Digite o número referente ao conteudo que deseja estudar: ")
        if escolha == "1":
            print("\n================ Função print() ================\n")
            print(
                "A função print() em Python é uma função embutida que exibe mensagens na tela, como no console ou terminal."
            )
            print("É uma das funções mais usadas na linguagem.")
            print("\n" "Explicação: \n")
            print(
                "Para usar a função print(), basta escrever "
                "print()"
                " seguido dos valores que deseja imprimir."
            )
            print(
                "Quando deseja exibir uma menssagem de texto, basta colocar a menssagem entre aspas dentro dos"
            )
            print("paranteses, veja abaixo: ")
            print('print("")')
            print("Por exemplo: print(" "Olá, Mundo!" """)""")
            print("O que a função print() pode exibir:")
            print("A função print() pode exibir qualquer tipo de dado,")
            print(
                "incluindo textos(strings), números, resultados de operações ou qualquer outro objeto dentro de Python."
            )
            print("O conteúdo será sempre convertido a uma string para ser exibido.")
            # quizOUmenu()
            if escolha == "1":
                print("\nIndentifique o erro de sintaxe no seguinte comando: ")
                print('print("Hello, World)')
                print(" A) - A lingua está em ingles")
                print(" B) - O espaço depois da virgula")
                print(" C) - Começar com letra maiuscula")
                print(" D) - As aspas não terem sido fechadas")
                RespQ = "h"
                RespQ = str(input("A, B, C ou D? "))
                if RespQ.upper() == "D":
                    print("Resposta Correta! Parabéns !\n")
                else:
                    print("Você errou")
            elif escolha == "2":
                pass
            else:
                print("opção invalida")
        elif escolha == "2":
            print("\n================ Função input() ================")
            print(
                "\nA função input() do Python permite que o programa receba dados do utilizador."
            )
            print(
                "É uma função built-in da linguagem ,ou seja, não é preciso instalá-la ou importá-la.\n"
            )
            print("Como funciona:\n")
            print("A função é invocada com os parênteses ao final.")
            print(
                "O programa abre para a entrada padrão, que é o terminal, o utilizador digita algo."
            )
            print("A função retorna os dados como string para a saída padrão.\n")
            print("Exemplos:")
            print("1 - input(" "Digite algo: " ") ")
            print("2 - n = input(" "Por favor digite o seu nome:" ")")
            print("3 - umNome = input('Por favor digite o seu nome: ')")
            print("\nConsiderações:")
            print("Por padrão, a função input() armazena os dados como strings.")
            print(
                "Para armazenar um número inteiro digitado pelo utilizador, pode-se usar o comando (int) antes do input."
            )
            print(
                "É possível fazer validações para verificar se o utilizador digitou algo ou não."
            )
            # quizOUmenu()
            if escolha == "1":
                print("\nO seguinte o comando esta dando erro:")
                print("int(input(input(" "Digite sua senha" "))" "")
                print("A)Não deveria ter Aspas")
                print("B)int só é valido com numeros")
                print("C)Não é necessario o input duas vezes")
                print("D)O certo seria (Digite sua senha)")
            elif escolha == "2":
                pass
            else:
                print("Opção invalida. Insira 1 ou 2 conforme foi informado.")
    elif escolha == "2":
        print("\n================ Quiz de Python ================\n")
        print("Deseja começar? ")
        comecar = str(input("Sim - Não: "))
        if comecar.lower() == "sim":
            print("\nQue ano o Python foi criado?")
            print(" A) - 2022")
            print(" B) - 1989")
            print(" C) - 1979")
            print(" D) - 1995")
            R1 = str(input("A, B, C ou D? "))
            if R1.upper() == "B":
                print("\n" "Resposta Correta! Parabéns!")
            else:
                print("Errouuuu!!!")
            print("\n" "Segunda pergunta: O nome Python foi inspirado em um")
            print(" A) - Nome de um algoritmo romano")
            print(" B) - Grupo de escola de samba")
            print(" C) - Grupo de comédia")
            print(" D) - Nome do pai do criador")
            R2 = str(input("A, B, C ou D? "))
            if R2.upper() == "C":
                print("Resposta Correta! Parabéns!")
            else:
                print("Errouuuu!!!")
            print(
                "\n"
                "Terceira pergunta: Indentifique o erro de sintaxe no seguinte comando"
            )
            print("print(Hello, World)")
            print(" A) - A lingua está em ingles")
            print(" B) - O espaço depois da virgula")
            print(" C) - Começar com letra maiuscula")
            print(" D) - As aspas não terem sido fechadas")
            R3 = str(input("A, B, C ou D? "))
            if R3.upper() == "D":
                print("Resposta Correta! Parabéns !")
            else:
                print("Errouuuu!!!")
            print(
                "\n"
                "Quarta e ultima pergunta parabénss!: O seguinte o comando esta dando erro: int(input(input("
                "Digite sua senha"
                ")) qual alternativa abaixo corrige o erro"
            )
            print(" A) - Não deveria ter Aspas")
            print(" B) - Não é necessario o input duas vezes")
            print(" C) - int só é valido com numeros")
            print(" D) - O certo seria int(input(input(Digite sua senha)))")
            R4 = str(input("A, B, C ou D? "))
            if R4.upper() == "B":
                print("Resposta Correta! Parabéns !")
            else:
                print("Errouuu!!!")
        elif comecar.lower() == "nao":
            print("\nVocê escolheu não fazer o QUIZ, iremos te direcionar ao MENU.\n")
        else:
            print("\nOpção invalida, estamos te direcionando ao MENU.\n")
    elif escolha == "3":
        print("\n================ Consultar Progresso ================\n")
        print("Nome: ", nome)
        print("Idade ", idade)
        print("Média da sua idade em relação aos outros usuários:", mediaIdade)
        print("\nQuantidade de acertos: ", qtdAcertos)
        print("Quantidade de erros: ", qtdErros)
        print("Média de acertos:", mediaAcertos)
        print("Média de erros:", mediaErros)
        print("\nHoras totais de uso do programa: ", horasTotais)
        print("Média de horas uso do programa: ", mediaHoras)
        print("\nDigite 'menu' para voltar ao menu")
        print("Digite 'ranking' para conferir sua pontuação no ranking")
        print("Digite 'exibir' para visualizar de forma gráfica ")
        if escolha.lower() == "menu":
            pass
        elif escolha.lower() == "ranking":
            print("ranking. . .")
        elif escolha.lower() == "exibir":
            print("Visualização dos grafico mil grau chique no ultimo")
        else:
            print("Opção invalida")
    elif escolha == "4":
        login()
    elif escolha == "5":
        # Sair()
        pass
    else:
        print("\nOpção invalida\n")
    return


# ============= CÓDIGO =============-
if __name__ == "__main__":
    main()
