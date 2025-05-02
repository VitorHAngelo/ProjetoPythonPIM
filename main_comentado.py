import textos  # módulo textos.py
from time import (
    sleep,
)  # lib time traz a função sleep que pausa o console por tempo determinado
import json  # lib do Python para lidar com arquivos .JSON
import os  # diversas funções relacionadas ao sistema
from sys import exit  # função para sair do programa
from csv import (
    DictWriter,
)  # lib do Python para lidar com .csv, essa classe é pra escrever o CSV
from hashlib import sha256  # lib para hashear variáveis
from dotenv import get_key  # lib pra ler arquivo .env
from cryptography.fernet import Fernet  # lib para criptografar JSON

usuario = None  # Definindo variável a nível global, se tiver algum usuário logado, será
#                guardado nela, caso contrário, devemos definí-la como None novamente.
# Abaixo, as letras maiúsculas indicam que são CONSTANTES, ao contrário das variáveis, não
# devem ser alteradas durante a execução
FILES_PATH = "./files/"  # Caminho para a pasta com os arquivos diversos
USER_DATA_PATH = (
    FILES_PATH + "user_data.json"
)  # Juntando o caminho pasta c/ nome arquivo JSON
ENV_PATH = FILES_PATH + ".env"  # Juntando o caminho pasta c/ nome arquivo .env


# ============= ARQUIVO JSON =============
def gerar_salt():
    """Função para gerar salt hexadecimal usando urandom(n bytes)
    Converte para hexadecimal, retorna em _str_
    """  # Define descrição da função.
    return os.urandom(8).hex()  # Usaremos 8 bytes (16 caracteres)


def criar_fernet():
    """Criar objeto Fernet para criptografar arquivo JSON."""
    fernet_key = get_key(ENV_PATH, "FERNET_KEY")  # Acessando chave Fernet no .env
    fernet = Fernet(fernet_key)  # criando objeto da classe Fernet
    del fernet_key  # Apagando chave da memória
    return fernet  # Retorna o objeto para quem chamou a função


def criar_json():
    """Cria arquivo JSON, caso ainda não exista."""
    if not os.path.exists(USER_DATA_PATH):  # Verifica se arquivo JSON existe, se não v
        with open(USER_DATA_PATH, "w") as file:  # cria arquivo ('w' significa write) e
            json.dump({}, file)  # trata ele pelo nome 'file'. Pedi para ele colocar {}
            # no arquivo, pois será um dicionário vazio no começo.
        criptografar_json()
        # LEMBRANDO que o with open abre o arquivo, faz o que precisa e o fecha


# Retorna dados do usuário do arquivo JSON
def get_usuario(cod_aluno: str):  # o '-> dict' só serve para adicionar a descrição
    # da função que ele vai retornar um dict se possível
    """cod_aluno espera receber em _str_ o RA do aluno.\n
    Se não existir retorna None.\n

    **Retorna:**
        _dict_: dicionário com dados do usuário
    """
    file_data = (
        descriptografar_json()
    )  # Recupera o JSON, descript. e guarda na variável.
    if cod_aluno not in file_data:  # Se o RA não estiver no dicionário
        return None  # Retorna None (nenhum)
    return {"RA": cod_aluno, **file_data[cod_aluno]}
    # Caso exista, retorna dict c/ dados do usuário
    # O objetivo desses ** é desempacotar o dicionário que vem em seguida e só
    # colocar chaves:valores no local; ou seja, ele tirará tudo para fora do dict
    # que estava.
    # Detalhe que estamos organizando o dict a ser retornado de uma forma diferente
    # da que o JSON usa pra armazenar, quando formos salvar de volta na função
    # update_json() precisaremos reverter.
    # O JSON guarda : {'RA000': {'nome': 'Vitor', 'idade': '29', 'Cidade': 'Araraquara'}}
    # Mudamos p/: {'RA': 'RA000', 'nome': 'Vitor', 'idade': 30, 'Cidade': 'Araraquara'}
    # Foi escolhido assim para facilitar lidar com os dados durante o resto do programa.


def gerar_ra():
    """Abre o JSON para checar o último RA cadastrado e retorna _int_ incrementado.\n
    Ex: Se o último for RA004, ele retorna 5"""  # Define descrição da função.
    file_data = (
        descriptografar_json()
    )  # Chama a função para obter os dados do arq. JSON
    if not file_data:  # 'se não file_data' quer dizer 'se file_data estiver vazia'
        return 0  # Caso seja o caso, retorna 0 pois o primeiro usuário será RA000.
    else:
        ra = list(file_data)[
            -1
        ]  # Caso haja algum user, faz uma lista dos usuários e pega
        return int(ra[2:]) + 1  # o último, depois obtém somente os numerais e soma 1
        # Afinal, um novo cadastro terá o último RA + 1 (RA003 + 1 = RA004)


def gerar_dados_seguros() -> (
    dict
):  # '-> dict' só indica na descr. que vai retornar dict.
    """Gera _dict_ com todos usuários e seus dados, removendo os dados sensíveis."""
    file_data = descriptografar_json()  # Obtém dados do JSON e guarda em file_data.
    dados_seguros = {}  # Define um dicionário vazio para ser guardado o que é seguro.
    for user in file_data:  # Loop para iterar sobre cada usuário da lista.
        dados_seguros[user] = file_data[user]  # Copia o usuário inteiro do file_data p/
        dados_seguros[user].pop("senha")  # dict novo, e então usa o .pop para tirar o
        dados_seguros[user].pop("salt")  # conteúdo sensível, no caso senha e salt.
    del file_data  # Tira o file_data da memória, pois contém dados sensíveis.
    return dados_seguros  # Retorna o dict seguro.


# ============= ARQUIVO CSV =============


def gerar_csv():
    """Cria arquivo .csv (comma separated values / valores separados por vírgula).\n
    Arquivo este que contém uma tabela dos cadastros, sem os dados sensíveis."""
    file_data = (
        gerar_dados_seguros()
    )  # Estamos pegando os dados NÃO SENSÍVEIS para gerar
    if (
        not file_data
    ):  # Se puxar os dados e estiver vazio (se NÃO file_data, ou seja, vazia)
        print("Não existem dados a serem gerados.")
    else:
        primeiro_ra = list(file_data)[
            0
        ]  # Caso não esteja vazia, acessa primeiro usuário
        campos = []
        for campo in file_data[primeiro_ra].keys():
            campos.append(campo)
        # Na linha acima, vai pegar o RA do primeiro user, acessá-lo, usar método .keys()
        # Com isso vai iterar através do FOR chave por chave, lembrando que os dicionários
        # trabalham com chave: valor. queremos as chaves para gerar as colunas da tabela.
        # Iremos guardá-los em uma lista, com o método append(), ficará algo como:
        # campos = ['nome', 'idade', 'horas_totais], ...]
        campos.insert(0, "RA")  # O dict que ele usou não tem o campo RA, então
        # inseriremos no índice 0 (começo da lista)
        with open(FILES_PATH + "user_data.csv", mode="w", newline="") as file:
            # Abre o arquivo user_data.csv, modo 'w' (write), se não existir, será criado.
            writer = DictWriter(file, fieldnames=campos)  # Cria uma instância do Writer
            # Como passamos o arquivo através da variável file, e os nomes das colunas
            # através do fieldnames=campos (lembra que guardamos os nomes das colunas na
            # variável campos), abaixo criaremos o cabeçalho da tabela.
            writer.writeheader()

            # LEMBRANDO que o 'with open' abre o arquivo, faz o que precisa e o fecha

            # No nosso caso, estamos armazenando o dict mais ou menos assim:
            # {'RA000': {'nome': 'Vitor', 'idade': '29', 'Cidade': 'Araraquara'}}
            # Dicionários guardam {chave: valor, chave: valor...}
            # Estamos usando o RA como chave para facilitar buscarmos usuários por ele,
            # assim quando buscarmos dicionario['RA000'], retornará o valor dessa chave,
            # estamos usando todas as outras informações como valor, ou seja, um dict
            # dentro de outro.
            for cod_aluno, usuario in file_data.items():
                # Quando usamos o método .items() em um dicionário, neste caso junto com o loop
                # FOR, ele quer te dar TANTO a chave, QUANTO o valor. Quando ele acessar a
                # primeira entrada do dict na variável file_data, ele vai ter algo como:
                # {'RA000': {'nome': 'Vitor', 'idade': '29', 'Cidade': 'Araraquara'}}
                # A chave é 'RA000', e ele vai guardar na 1ª chave que passei (cod_aluno)
                # O valor vem depois dos dois pontos, no caso é outro dict, como falamos.
                # Criaremos uma variável 'linha' pois será uma linha da nossa tabela
                # Caso quisessemos guardar somente o valor, poderiamos só passar esse
                # dicionário valor do RA, mas como também queremos o RA do usuário, precisaremos
                # criar uma variavel que será um dict, chave 'RA', valor 'cod_aluno', e em
                # seguida adicionar o resto das informações, como é um dicionário, a forma
                # mais fácil de fazer isso é utilizando os dois asteristicos antes da variav.
                # O objetivo desses ** é desempacotar o dicionário e só colocar chaves:valores
                # no local; ou seja, ele tirará tudo para fora do dict que estava.
                linha = {"RA": cod_aluno, **usuario}
                writer.writerow(linha)  # Chama o writer e escreve a linha no arquivo


# ============= CRIPTOGRAFIA =============


def criptografar_json():
    """Criptografa os dados vulneráveis do JSON, não queremos que o JSON fique
    desprotegido NUNCA, portanto, será utilizado somente quando o arquivo for criado
    e só conter um dict vazio. Nas vezes subsequentes, sobrescreveremos já criptografado.
    """
    fernet = (
        criar_fernet()
    )  # cria instância do fernet, já aplicada chave de criptografia
    with open(
        USER_DATA_PATH, "r", encoding="utf-8"
    ) as file:  # abre JSON como 'r'(read)
        file_data = file.read()  # Lê e guarda conteúdo na variável

    dados_bytes = file_data.encode()  # Passa p/ bytes
    dados_criptografados = fernet.encrypt(
        dados_bytes
    )  # Criptografa usando inst. fernet

    with open(USER_DATA_PATH, "wb") as file:  # abre o mesmo arquivo, 'wb'(write bytes)
        # O fernet vai guardar tudo criptografado em BYTES.
        file.write(
            dados_criptografados
        )  # Python escrevo o arquivo com os bytes passados


def descriptografar_json():
    """Função para obter os dados do JSON. (Não deixa o arquivo descriptografado!!! Só
    puxa os dados criptografados, traduz e retorna como _dict_)"""
    with open(USER_DATA_PATH, "rb") as file:  # Abre JSON como 'rb'(read bytes)
        # Lembre-se que criptografamos como bytes, portanto leremos assim também
        dados_criptografados = file.read()  # usa o método read() do Python para ler e
        # guardar na variável.

    dados_json = criar_fernet().decrypt(dados_criptografados).decode()
    # Lembre-se que métodos sempre vem depois de algo através de: .método(), ou seja,
    # estamos usando alguma utilidade que esse método fornece para agir em cima de algo
    # que veio ANTES do método.
    # Exemplo: Se falarmos: 'Sabrino'.upper()    .upper() é um método q faria 'SABRINO'
    # Enfim, para lermos essa expressão alí acima, que está 'abreviada', o decode()
    # agirá em cima do .decrypt só depois que .decrypt() tiver agido sobre criar_fernet()
    # Eu sei que é complicado, mas numa forma mais fácil, ficaria:
    "fernet = criar_fernet()"  # Instanciariamos o fernet e atribuiriamos a variavel fernet
    "dados_descriptografados = fernet.decrypt(dados_criptografados)"
    # Com a instancia do fernet, utilizaremos o método para descriptografar
    # o conteudo do arquivo que guardamos na variavel dados_cript. Finalmente:
    "dados_json = dados_descriptografados.decode()"
    # pegariamos a variável anterior e decodificariamos de bytes para string essas três
    # linhas dariam o mesmo resultado da utilizada lá em cima, com mais variáveis e linhas

    return json.loads(dados_json)  # tendo o arquivo em json, utilizamos o método
    # .loads() da biblioteca json, para transformar a formatação json para string
    # O método .loads() é utilizado pq ele está em uma variável/string, se quisessemos ler
    # direto do arquivo, seria o método .load(arquivo)


def update_json(cod_aluno, usuario):
    """cod_aluno: RA em _str_\n
    usuario: _dict_ com dados do usuário\n
    Função utilizada para atualizar o JSON, sem que ele fique com os dados desproteg.
    em nenhum momento."""
    file_data = descriptografar_json()  # Obteremos o conteúdo do JSON
    file_data[cod_aluno] = dict(
        list(usuario.items())[1:]
    )  # Atualizaremos o dict do user
    # Aqui reverteremos a mudança no dict 'usuario' feita no get_usuario()
    # Usamos o método .items() para receber chaves:valores, depois com a função list()
    # irá transformar o dict em lista, e assim conseguiremos pegar do 1 índice até o
    # último e transformar de volta pra dict, isso pq não queremos a primeira chave
    # valor que haviamos inserido (era RA: cod_aluno)
    # Estava: {'RA': 'RA000', 'nome': 'Vitor', 'idade': 30, 'Cidade': 'Araraquara'}
    # O JSON guarda : {'RA000': {'nome': 'Vitor', 'idade': '29', 'Cidade': 'Araraquara'}}

    dados_bytes = json.dumps(file_data).encode()  # Passa p/ bytes
    dados_criptografados = criar_fernet().encrypt(dados_bytes)  # Criptografa_dados

    with open(USER_DATA_PATH, "wb") as file:  # Abre o arquivo como 'wb'(write bytes)
        file.write(dados_criptografados)  # Escreve os dados protegidos no arquivo.

    # Repare que desde o início da função, só desprotegemos o conteúdo do JSON que está
    # contido na variável file_data, nunca os colocamos vulneráveis no arquivo.


# ============= FUNÇÕES GERAIS =============


def limpar_console():
    """Função para limpar o console"""
    if os.name == "nt":  # Se Windows
        os.system("cls")  # Comando 'cls' do Windows limpa o console
    else:
        os.system("clear")  # Se Linux, 'clear' pra poder rodar em alguns sites online


def cadastro():
    """Função destinada a cadastrar um novo usuário e salvar no JSON"""
    print("Seja bem-vindo! Faremos seu cadastro a seguir:")
    while True:  # Loop do cadastro
        usuario = {}  # Cria um dict vazio para inserirmos os dados do usuário
        while True:  # Loop do nome
            nome = input("Insira seu nome com sobrenome: ").title()
            # Método .title() formata o nome para todas iniciais maiúsculas, por estética.
            if not nome.replace(" ", "").isalpha():
                # Aqui, nesse IF, utilizamos o método .replace() para trocar todos espaços ' '
                # por nada '', assim, tirando os caracteres de espaço, conseguimos depois
                # (na mesma linha), usar o método .isalpha() que verificará se todos caracteres
                # são do 'alphabet'(alfabeto), até pq não podemos aceitar nomes com números.
                # Se não tirassemos os espaços, sempre que tivesse espaços ia retornar
                # False, devido ao espaço (' ') não ser do alfabeto
                # Detalhe importante é que não salvamos o nome sem espaços em uma variável
                # Se fizessemos:
                'nome = nome.replace(" ", "")'
                # Aí sim estariamos alterando como o nome seria salvo.
                print("Utilize somente letras e espaços, por favor.")
            elif len(nome) < 3:  # Se nome com menos de 3 caracteres
                print("Nome muito curto, favor insira um nome válido")
            else:  # Caso contrário, sairemos do loop while e prosseguiremos
                break

        while True:  # Loop da Idade
            idade = input(
                f"Olá {' '.join(nome.split()[:2])}, por favor, insira sua idade: "
            )
            # O método .split() separa os nomes por espaços e retorna uma lista com cada um
            # Exemplo: ['Vitor', 'Hugo', 'Cincerre', 'Angelo']
            # Aí utilizamos o índice para imprimir do começo da lista até o índice dois (menos
            # o dois). Ou seja: nome.[:2] (desde o primeiro: até o segundo(menos ele))
            # Assim só mostraremos os dois primeiros nomes para não ficar muita coisa.
            if (
                not idade.isdecimal()
            ):  # Se a idade que usuário inserir não for decimal (0-9)
                print("Por gentileza, utilize somente números!")
                continue  # Usa o continue pra mandar de volta pro início do loop 'while True:'
            idade = int(
                idade
            )  # Como passou pela verif. que é número, podemos convert. pra int
            if (
                idade < 4 or idade > 120
            ):  # Caso verdadeiro, idade será inválida e pedirá dnv.
                print("Insira uma idade válida!")
            else:  # Caso chegue aqui, podemos sair do loop, pois temos uma idade válida.
                break

        confirmacao = input(
            f"Por favor, aperte ENTER se seus dados estiverem corretos:\nNome: {nome}\nIdade: \
{idade}\nCaso preferir, digite 'voltar'\n"
        ).lower()
        if confirmacao == "voltar":
            break
        while True:  # Loop
            senha = input("Insira sua senha: ")
            limpar_console()
            senha2 = input("Insira sua senha novamente, por favor: ")
            limpar_console()  # Pegamos a senha 2 vezes pra garantir q não tenha sido erro.
            # A função limpar_console() não deixa a senha exposta no console.
            if senha == senha2:  # Se as senhas inseridas forem iguais
                if senha.isascii() and senha.count(" ") == 0 and len(senha) >= 6:
                    # Se todos caracteres forem ASCII E contagem de espaços for 0 e tamanho >= 6
                    # Podemos sair do loop pois é uma senha válida.
                    break
                else:  # Caso contrário mandaremos de volta para o início do loop.
                    print(
                        "Senha inválida, favor utilizar ao menos 6 letras, números e caracteres \
    especiais, espaços não são válidos."
                    )
                    continue
            else:  # Se senhas 1 e 2 forem diferentes, volta pro início do loop.
                print("Senhas diferentes, insira duas senhas iguais para continuar.")
        # v Fora do loop v
        salt = gerar_salt()  # Gera um salt (código hexadecimal aleatório), caso queira
        # entender o que é, sugiro um vídeo simples e rápido:
        # https://www.youtube.com/watch?v=YLCoDK0OwYM
        senha_hash = hashear_senha(
            senha, salt
        )  # Função para proteger a senha, leia mais nela.
        cod_aluno = (
            f"RA{gerar_ra():03d}"  # Chamamos a função para gerar novo RA, com base no
        )
        # último RA cadastrado + 1. veja que a função só retorna um inteiro como 3 por exemplo.
        # utilizaremos f-string para:
        # ainda com o retorno inteiro, formataremos com 3 casas decimais com o :03d
        # : indica que um especificador de formatação.
        # 0 o caractere que vai preencher os espaços faltantes (zero, no caso).
        # 3 o número total de dígitos que você quer (3 dígitos).
        # d significa que o valor é um número inteiro (d de decimal).
        # Ainda aplicaremos o 'RA' no início da string, atribuiremos isso na variavel cod_aluno
        usuario = {
            "RA": cod_aluno,
            "nome": nome,
            "idade": idade,
            "senha": senha_hash,
            "horas_totais": 0,
            "qtd_acertos": 0,
            "qtd_erros": 0,
            "media_horas": 0,
            "media_acertos": 0,
            "media_erros": 0,
            "media_idade": 0,
            "salt": salt,
        }
        # Lá atrás criamos um dict vazio chamado usuario, acima criaremos nele a chave
        # cod_aluno e como valor desta chave um dict com todos os dados pertinentes ao usuário.
        # Ex: usuário = {RA: 'RA000', 'nome': 'Vitor', 'idade': '29', 'senha': 'srh9q1rh1u9he112'}}
        print(
            f"""============================= ATENÇÃO =============================
Seu RA é: {cod_aluno}. ANOTE este código pois será utilizado para realizar seu login!
Aperte ENTER para prosseguir"""
        )
        input("===================================================================\n")
        update_json(cod_aluno, usuario)
        # Chamaremos o método para salvar esse usuário no JSON, passando o RA dele e o dict
        # com suas infos.
        return


def hashear_senha(entrada_senha: str, salt: str):  # o salt: str indica que você deveria
    # passar uma str, mas não te impede de passar outra coisa.
    """Função para proteger senha do usuário, para que seja armazenado de forma segura
    e para que quando ele faça login, criptografamos a senha e então compararemos com a
    salva no arquivo .JSON (que sempre estará criptografada)

    **Argumentos:**
        entrada_senha (_str_): Senha crua inserida pelo usuário
        salt (_str_): String hexadecimal individual, armazenada no _dict_ de cada usuário

    **Retorna:**
        _str_: String protegida com salt, pepper e criptog. sha256
    """
    # Receberemos a senha 'crua' do usuário, e seu salt particular, lembrando que cada
    # usuário tem seu próprio salt, que está guardado em seu dict
    senha_salt_pepper = salt + entrada_senha + str(get_key(ENV_PATH, "PEPPER"))
    # Na linha acima concatenaremos o salt pessoal, a senha inserida e o PEPPER que ele
    # está buscando no arquivo .env
    objeto_hash = sha256(senha_salt_pepper.encode())
    # a função encode passa p/ bytes. O hashlib trabalha com bytes, depois utiliza sha256 pra hashear
    return (
        objeto_hash.hexdigest()
    )  # Transforma a variável em caracteres hexadecimais com
    # método .hexdigest().


def simular_carregamento(mensagem_carregamento, mensagem_completo):
    """Função para efeito estético, simula que o programa está carregando

    **Argumentos:**
        mensagem_carregamento (_str_): Ex: 'Carregando menu'
        mensagem_completo (_str_): Ex: 'Menu carregado!'
    """
    simbolos = [
        "\\",
        "|",
        "/",
        "-",
    ] * 4  # Lista com os símbolos a serem ciclados vezes 4
    # O '\\' será impresso somente uma \, a barra inversa é utilizada para indicar que o
    # próximo caracter não é 'especial' e deve ser impresso normalmente, se utilizassemos
    # somente uma \, ele indicaria que o caracter seguinte (no caso uma aspa simples) é
    # para ser impresso, no caso não é; é para ser entendido como final da string mesmo.
    # Se deixassemos print('\') daria erro, pois ele acharia que estamos indicando com a
    # barra inversa que é pra imprimir a segunda aspa simples e esperaria mais uma aspa
    # simples pra fechar a string.
    # Ao multiplicar a lista por 4, teremos algo como:
    # ['\\', '|', '/', '-', '\\', '|', '/', '-', '\\', '|', '/', '-', '\\', '|', '/', '-']
    limpar_console()
    for i in simbolos:  # para cada item da lista simbolos
        print(
            f"{mensagem_carregamento} {i}"
        )  # f-string para imprimir msg + cada caracter
        # da lista, que será iterado c/ laço FOR
        sleep(0.1)  # Utiliza a função sleep da lib 'os' para 'dormir' ou 'aguardar' 0.1
        # segundos antes de ir para a próxima linha.
        limpar_console()
    print(
        mensagem_completo
    )  # Ao finalizar o laço, imprime a mensagem de carreg. completo


def login() -> dict:
    """Função para realizar o login do usuário, interagindo com o usuário para pedir dados.

    **Retorna:**
        _dict_: Dicionário com os dados do usuário"""
    global usuario  # Mostra que lidaremos com a variável global, caso contrário seu
    # conteúdo seria apagado após sair da função.
    file_data = descriptografar_json()
    retorno_usuario = input(
        "Digite seu RA, ou 'voltar' para retornar ao menu.\n"
    ).upper()
    # Recebe dados e transforma em maiúsculo, como todo RA
    if retorno_usuario == "VOLTAR":
        return
    # Se usuário inserir voltar, retorna ao menu_login
    usuario = get_usuario(retorno_usuario)  # Tenta obter dict do usuário
    if (
        usuario is None
    ):  # Se RA informado não existir, informa o usuário e manda p/ menu
        input(
            f'RA "{retorno_usuario}" não encontrado, aperte ENTER para retornar ao Menu'
        )
        return  # Retorna None
    del file_data  # Apaga referência aos dados do JSON, não iremos usar mais e é sensível
    while True:  # Loop p pedir senha até acertar ou pedir p/ voltar.
        entrada_senha = input(
            f'Olá, {" ".join(usuario["nome"].split()[:2])}! Favor, insira sua senha: '
        )
        limpar_console()
        if entrada_senha.upper() == "VOLTAR":
            return  # Se escolher voltar
        senha_hash = hashear_senha(
            entrada_senha, usuario["salt"]
        )  # Passa senha que usuário
        # digitou e seu 'salt' para aplicar hash
        if (
            senha_hash == usuario["senha"]
        ):  # Compara com o hash armazenado na variav user
            input("Login realizado com sucesso! Aperte ENTER para continuar.\n")
            # Usa o input pra mostrar msg e aguardar usuário apertar ENTER
            break  # Se senha certa, sai do loop de pedir senha
        else:  # Se senha inválida, avisa e informa a opção de voltar.
            print("Senha incorreta. Se desejar, digite 'voltar'")
    usuario.pop(
        "senha"
    )  # Antes de retornar o dict com dados do usuário, remove os dados
    usuario.pop("salt")  # cujas chaves são 'senha' e 'salt' por serem sensíveis.
    return usuario


def recuperacao():
    """
    Função para ajudar o usuário a recuperar sua senha ou RA, através do console.
    Após o auxílio, retorna o usuário ao menu_login
    """
    while True:  # Loop para ficar na função
        escolha = (
            None  # Defino var como None pra entrar no Loop de aguardar entrada válida
        )
        while escolha not in (
            "1",
            "2",
            "3",
        ):  # Enquanto não inserir entrada q ta na tupla
            escolha = input(
                """O que você precisa?
1 - Perdi minha senha
2 - Perdi meu RA
3 - Voltar ao menu\n"""
            )  # Recebe opção do usuário e se válida sai do laço while
        if escolha == "1":  # Alterar senha informando RA e Nome
            cod_aluno = input(  # usuário informa RA
                "Para recuperarmos sua senha, insira o seu RA: "
            ).upper()
            usuario = get_usuario(cod_aluno)  # Tenta obter usuário com RA informado
            if usuario is None:  # Se recebermos None da função acima (RA inexistente)
                limpar_console()
                print("RA inválido.")
                continue  # Volta pro começo do loop
            else:  # Se RA válido
                entrada_nome = input(
                    "Insira seu nome conforme informado no cadastro: "
                ).title()  # método title pro nome ficar como no cadastro, com iniciais maiúsc.
                if (
                    entrada_nome != usuario["nome"]
                ):  # Se informado não bater c/ cadastro..
                    limpar_console()
                    print("Nome incorreto.")
                    continue  # Volta pro início do menu
                else:  # Se tiver o nome certo...
                    while True:  # Loop para cadastrar senha
                        entrada_senha = input(
                            f'Olá, {" ".join(usuario["nome"].split()[:2])}! Favor, insira sua nova senha:\n'
                        )
                        limpar_console()  # Limpa pra senha não ficar na tela
                        entrada_senha1 = input("Repita a senha: ")
                        limpar_console()  # Limpa pra senha não ficar na tela
                        if entrada_senha == entrada_senha1:
                            # Se inseriu 2x iguais, prosseguimos, se não , volta.
                            if (
                                entrada_senha.isascii()
                                and entrada_senha.count(" ") == 0
                                and len(entrada_senha) >= 6
                            ):
                                # Se senha for ASCII, sem espaços e maior/igual a 6 caracteres, prosseguiremos
                                usuario["senha"] = hashear_senha(
                                    entrada_senha, usuario["salt"]
                                )
                                # Acima, protegeremos a senha antes de guardar
                                update_json(cod_aluno, usuario)  # Atualiza JSON
                                print("Senha alterada com sucesso!")
                                return  # Volta pro menu_login, já que deu certo
                            else:  # Se senha inválida:
                                print(
                                    "Senha inválida, favor utilizar ao menos 6 letras, números e caracteres \
especiais, espaços não são válidos."
                                )
                                continue  # Voltaremos pra tentar novamente
                        else:  # Se senhas inseridas forem diferentes uma da outra:
                            print(
                                "Senhas diferentes, insira duas senhas iguais para continuar."
                            )
        elif escolha == "2":  # Se esqueceu o RA:
            entrada_nome = input(
                "Para recuperarmos seu RA, insira seu nome: "
            ).title()  # Aplica .title()
            # que deixa iniciais maiúsculas, igual cadastrado.
            possiveis_usuarios = []  # Define lista vazia p/ salvarmos possíveis matches
            file_data = descriptografar_json()  # Obtemos conteúdo do JSON
            for user in file_data.keys():  # FOR iterando sobre todas os RAs
                # Ele usa o método .keys(), pois no JSON estão como:
                # {'RA000': {'nome': 'Vitor'...} e queremos a chave que seria o 'RA000'
                # que será armazenado na variável user do FOR e assim olharmos no
                # file_data['RA000']['nome'] e iterar sobre cada nome para compararmos
                # com o que usuário informou.
                if file_data[user]["nome"] == entrada_nome:  # Se bater a comparação...
                    possiveis_usuarios.append(
                        user
                    )  # Vamos salvar o usuário na lista criada
            if not possiveis_usuarios:  # Se no final do FOR não houver matches...
                print("Sinto muito, não possível encontrar alguém com este nome.")
                continue  # Retorna ao início para tentar novamente.
            else:  # Caso encontremos matches
                print(
                    "Encontramos possíveis usuários, precisaremos de sua senha para ter certeza."
                )
                entrada_senha = input(  # Pediremos a senha cadastrada.
                    "Insira a senha cadastrada, por gentileza: "
                )
                limpar_console()  # Limpa console para não ficar senha a mostra.
                for cod_aluno in possiveis_usuarios:  # Outro for para procurarmos senha
                    # informada em cada usuário
                    senha_hash = hashear_senha(
                        entrada_senha, file_data[cod_aluno]["salt"]
                    )
                    # Protegeremos a senha informada para comparar c/ a do cadastro.
                    if senha_hash == file_data[cod_aluno]["senha"]:  # Se senha bater
                        input(
                            f"Sucesso! ANOTE seu RA: {cod_aluno} e depois aperte ENTER"
                        )
                        return  # Volta ao menu
                limpar_console()
                print("Não foi possível localizar seu cadastro.")
                continue  # Tentar novamente
        else:
            return  # Se escolher 3, sai pro menu


def menu_principal():
    global usuario  # Pega a variável global usuário
    while True:  # Loop pra não sair do menu
        escolha = (
            None  # Defino variável como None para entrar no loop, se não fizer isso
        )
        # ele não vai conseguir verificar se escolha está na lista abaixo e vai dar erro.
        while escolha not in ["1", "2", "3", "4", "5"]:
            escolha = input(
                textos.menu_principal
            )  # Vai perguntar dnv enquando inválida
        if escolha == "1":  # Aprender
            print("Pendente")  # Chamar função responsável
        elif escolha == "2":  # Quiz
            print("Pendente")  # Chamar função responsável
        elif escolha == "3":  # Consulte seu progresso
            print("Pendente")  # Chamar função responsável
        elif escolha == "4":  # Lougout
            usuario = None
            print("Logoff realizado.")
            return
        elif escolha == "5":  # Sair do programa
            simular_carregamento("Saindo do programa", "Até a próxima!")
            exit()


def main():
    criar_json()  # Sempre ao iniciar programa verifica se JSON está criado, se não, cria
    global usuario  # Indicando que a variável usuário é global
    while True:  # Loop para programa não terminar
        escolha = (
            None  # Defino variável como None para entrar no loop, se não fizer isso
        )
        # ele não vai conseguir verificar se escolha está na lista abaixo e vai dar erro.
        if (
            usuario is not None
        ):  # Verifica se há algo na var usuario, se tiver, está logado
            menu_principal()  # Sendo assim, manda pro menu principal
        while escolha not in ["1", "2", "3", "4", "5"]:  # Enquanto escolha invál.
            limpar_console()
            escolha = input(
                textos.menu_login
            )  # textos.meu_login puxa texto do arquivo textos
            limpar_console()
        if escolha == "1":  # Login
            usuario = login()
        elif escolha == "2":  # Cadastrar
            cadastro()
        elif escolha == "3":  # Recuperação senha/RA
            recuperacao()
        elif escolha == "4":  # Sair
            simular_carregamento("Saindo do programa", "Até a próxima.")
            break
        elif escolha == "5":  # Painel ADMIN secreto
            senha = input("Digite a senha de admin: ")
            if senha == get_key(
                ENV_PATH, "ADMIN_PW"
            ):  # se senha inserida for igual do .env
                limpar_console()
                gerar_csv()

                # funcao = input('Teste uma função (gerar_csv, gerar_dados_seguros)\n')
                # print(eval(funcao))


# Função Quiz ou Menu, quando chamada no fim de qualquer conteuto sobre Python exibe a pergunta para o usuario se ele deseja fazer um quiz sobre o conteudo ou voltar ao menu


def quizOUmenu():

    print("\nDeseja fazer um Quiz sobre o conteúdo estudado ou voltar ao menu? ")

    # identifica escolha como global para a função

    global escolha

    escolha = input("Digite 1 para o Quiz e 2 para voltar ao menu: ")

    return


# Função sair. Quando chamada exibe a pergunta se o usuario realmente deseja sair do programa


def Sair():

    print("\nVocê escolheu sair do programa, tem certeza que deseja sair? ")

    ver = str(input("Digite sim para sair e não para voltar ao menu\n"))

    # verifica se o usuario quer mesmo sair do programa. Com o .lower o valor armazenado na var é forçado a ficar minusculo.

    if ver.lower() == "sim":

        print("Encerrando o Programa. . .")

    elif ver.lower() == "não":
        pass
        # Menu()

        # Ifs()

    else:

        print("\nA opção escolhida é invalida, Digite conforme orientado.")

        # Sair()

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

    # Verifica qual modulo o usuário escolheu

    if escolha == "1":

        print("\nOpção Aprender escolhida. Escolha qual conteúdo estudar: ")

        print(" 1 - Comando Print()")

        print(" 2 - Comando Input()")

        escolha = input("Digite o número referente ao conteudo que deseja estudar: ")

        # Verifica se foi o conteudo 1

        if escolha == "1":

            # Mostra o conteudo

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

            quizOUmenu()  # Chama a fução quizORmenu

            if escolha == "1":

                # INICIA O QUIZ DA OP1

                print("\nIndentifique o erro de sintaxe no seguinte comando: ")

                print('print("Hello, World)')

                print(" A) - A lingua está em ingles")

                print(" B) - O espaço depois da virgula")

                print(" C) - Começar com letra maiuscula")

                print(" D) - As aspas não terem sido fechadas")

                # Var local recebe a resposta

                RespQ = "h"

                RespQ = str(input("A, B, C ou D? "))

                # verifica se a resposta está correta

                if RespQ.upper() == "D":

                    print("Resposta Correta! Parabéns !\n")

                else:

                    print("Você errou")

            # Verifica se fo iescolhido voltar ao menu apartir dp conteudo 1

            elif escolha == "2":
                pass
                # Menu()  #função menu chamada

                # se nao for 1 nem 2 é opção invalida

            else:

                print("opção invalida")

        # verifica se o conteudo 2 foi selecionado

        elif escolha == "2":

            # mostra o conteudo 2

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
                # Menu()

                # Ifs()

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

            # Menu()

            # Ifs()

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
            # Menu()
            # Ifs()
        elif escolha.lower() == "ranking":
            print("ranking. . .")
        elif escolha.lower() == "exibir":
            print("Visualização dos grafico mil grau chique no ultimo")
        else:
            print("Opção invalida")
            # chamar função Modulo consultar progresso()

    elif escolha == "4":
        login()

    elif escolha == "5":
        Sair()
    else:
        print("\nOpção invalida\n")
        # Menu()
        # Ifs()
    return


# ============= CÓDIGO =============-

if __name__ == "__main__":  # Só executa main() se este arquivo for rodado diretamente,
    main()  # não importado
