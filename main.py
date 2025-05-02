import textos
from time import sleep
from datetime import datetime
import json
import os
from sys import exit
from csv import DictWriter
from hashlib import sha256
from dotenv import get_key
from cryptography.fernet import Fernet

# Variáveis globais
usuario = None
horario_login = None

# Constantes
FILES_PATH = "./files/"
USER_DATA_PATH = FILES_PATH + "user_data.json"
ENV_PATH = FILES_PATH + ".env"


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
    print(file_data)
    dados_seguros = {}
    for user in file_data:
        dados_seguros[user] = file_data[user]
        dados_seguros[user].pop("senha")
        dados_seguros[user].pop("salt")
    del file_data
    return dados_seguros


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


# ============= FUNÇÕES GERAIS =============
def limpar_console():
    """Função para limpar o console"""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def get_horario() -> datetime:
    """Retorna a data/horário atual"""
    return datetime.now()


def cadastro():
    """Função destinada a cadastrar um novo usuário e salvar no JSON"""
    usuario = {}
    print("Seja bem-vindo! Faremos seu cadastro a seguir:")
    while True:
        while True:
            nome = input("Insira seu nome com sobrenome: ").title()
            if not nome.replace(" ", "").isalpha():
                'nome = nome.replace(" ", "")'
                print("Utilize somente letras e espaços, por favor.")
            elif len(nome) < 3:
                print("Nome muito curto, favor insira um nome válido")
            else:
                break
        while True:
            idade = input(
                f"Olá {' '.join(nome.split()[:2])}, por favor, insira sua idade: "
            )
            if not idade.isdecimal():
                print("Por gentileza, utilize somente números!")
                continue
            idade = int(idade)
            if idade < 4 or idade > 120:
                print("Insira uma idade válida!")
            else:
                break
        while True:
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
            "idade": idade,
            "senha": senha_hash,
            "minutos_uso": 0,
            "qtd_acertos": 0,
            "qtd_erros": 0,
            "media_horas": 0,
            "media_acertos": 0,
            "media_erros": 0,
            "media_idade": 0,
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
        _str_: String protegida com salt, pepper e criptog. sha256
    """
    senha_salt_pepper = salt + entrada_senha + str(get_key(ENV_PATH, "PEPPER"))
    objeto_hash = sha256(senha_salt_pepper.encode())
    return objeto_hash.hexdigest()


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


def login() -> dict:
    """Função para realizar o login do usuário, interagindo com o usuário para pedir dados.
    **Retorna:**
        _dict_: Dicionário com os dados do usuário"""
    global usuario
    global horario_login
    file_data = descriptografar_json()
    retorno_usuario = input(
        "Digite seu RA, ou 'voltar' para retornar ao menu.\n"
    ).upper()
    if retorno_usuario == "VOLTAR":
        return
    usuario = get_usuario(retorno_usuario)
    if usuario is None:
        input(
            f'RA "{retorno_usuario}" não encontrado, aperte ENTER para retornar ao Menu'
        )
        return
    del file_data
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


def menu_principal():
    global usuario
    while True:
        escolha = None
        while escolha not in ["1", "2", "3", "4", "5"]:
            escolha = input(textos.menu_principal)
        if escolha == "1":
            print("Pendente")
        elif escolha == "2":
            print("Pendente")
        elif escolha == "3":
            print("Pendente")
        elif escolha == "4":
            tempo_uso = get_horario() - horario_login
            usuario["minutos_uso"] = int(tempo_uso.total_seconds() // 60)
            file_data = descriptografar_json()
            update_json(usuario["RA"], usuario)
            usuario = None
            print("Logoff realizado.")
            return
        elif escolha == "5":
            simular_carregamento("Saindo do programa", "Até a próxima!")
            exit()


def main():
    criar_json()
    global usuario
    while True:
        escolha = None
        if usuario is not None:
            menu_principal()
        while escolha not in ["1", "2", "3", "4", "5", "6", "7"]:
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
            break
        elif escolha == "5":
            senha = input("Digite a senha de admin: ")
            if senha == get_key(ENV_PATH, "ADMIN_PW"):
                gerar_dados_seguros()
                limpar_console()
                gerar_csv()


# Função Quiz ou Menu, quando chamada no fim de qualquer conteuto sobre Python exibe a pergunta para o usuario se ele deseja fazer um quiz sobre o conteudo ou voltar ao menu
def quizOUmenu():
    print("\nDeseja fazer um Quiz sobre o conteúdo estudado ou voltar ao menu? ")
    global escolha
    escolha = input("Digite 1 para o Quiz e 2 para voltar ao menu: ")
    return


# Função sair. Quando chamada exibe a pergunta se o usuario realmente deseja sair do programa
def Sair():
    print("\nVocê escolheu sair do programa, tem certeza que deseja sair? ")
    ver = str(input("Digite sim para sair e não para voltar ao menu\n"))
    if ver.lower() == "sim":
        print("Encerrando o Programa. . .")
    elif ver.lower() == "não":
        pass
    else:
        print("\nA opção escolhida é invalida, Digite conforme orientado.")
    return


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
            quizOUmenu()
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
            quizOUmenu()
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
        Sair()
    else:
        print("\nOpção invalida\n")
    return


# ============= CÓDIGO =============-
if __name__ == "__main__":
    main()
