# Arquivo de textos para o projeto de Python


# ============================= MENUS =============================

menu_login = f"""{' Menu Login '.center(50, '=')}\n
Bem vindo ao menu! Escolha a opção desejada:
1 - Login
2 - Criar sua conta
3 - Recuperar seu login
4 - Sair (Encerra o programa)
5 - Administração (Acesso Restrito)\n"""

menu_principal = (
    f"{' Menu Principal '.center(50, '=')}\n"
    + """Bem vindo, {}! Escolha a opção desejada: 
1 - Aprender (Lições sobre diferentes assuntos)
2 - Quiz (Teste seus conhecimentos sobre as matérias apresentadas)
3 - Consulte seu progresso (Confira sua média de acertos ou seus minutos ativo no programa)
4 - Ranking
5 - Editar conta
6 - Logout (Sair da sua conta aluno)
7 - Sair (Encerra o programa)\n"""
)


menu_conta = (
    f"{' Editar Conta '.center(50, '=')}\n"
    + """Olá, {}! Escolha a opção desejada: 
1 - Mudar sua senha
2 - Retirar os seus dados do sistema
3 - Voltar\n"""
)

menu_ranking = (
    f"{' Você gostaria ver o ranking de qual assunto? '.center(50, '=')}\n"
    + """1 - Lógica
2 - Python
3 - Cibersegurança
4 - Voltar\n"""
)

menu_quiz = (
    f"{' Escolha um assunto para fazer o QUIZ: '.center(50, '=')}\n"
    + """1 - Lógica
2 - Python
3 - Cibersegurança
4 - Voltar\n"""
)

menu_aprender = f"""{' Menu Aprender '.center(50, '=')}\n
Escolha sobre qual assunto você gostaria de aprender:
1 - > Lógica de Programação
2 - > Python
3 - > Cibersegurança
4 - Voltar ao Menu\n"""

menu_aprender_logica = f"""{' Menu Aprender LÓGICA '.center(50, '=')}\n
Escolha uma lição sobre lógica:
1 - > O que seria lógica?
2 - > Qual número é maior?
3 - > Par ou ímpar?
4 - > Estamos pensando igual?
5 - > Gerar tabuada
6 - Voltar ao Menu Aprender\n"""

menu_aprender_python = f"""{' Menu Aprender PYTHON '.center(50, '=')}\n
Escolha uma lição sobre lógica:
1 - > O que é Python
2 - > Função print()
3 - > Função input()
4 - Voltar ao Menu Aprender()\n"""

# ============================ APRENDER ============================

aprender_py_historia = """
Python é uma linguagem de programação, isto é, usamos para passar instruções para o
computador de como fazer as coisas e os passos que ele deve seguir. Python teve sua 
primeira versão lançada em 1991 por seu criador Guido van Rossum e até hoje é uma
linguagem que cresce bastante por ter uma escrita mais fácil para o entendimento,
especialmente quando comparada a outras. Ainda sim, é uma tecnologia muito poderosa.
"""

aprender_py_print_um = """
=============================================================================
Em Python temos alguns comandos, na verdade são palavras reservadas que por anteceder um
par de parênteses "()" recebem o nome de FUNÇÃO, e cada uma dela tem suas tarefas
específicas, por isso devemos tentar utilizá-las somente quando temos a intenção,
de fato, de usufruir desta utilidade.

Um detalhe importante é que estas funções sempre são escritas em letras minúsculas; 
caso contrário o Python não entenderá corretamente.

Para exibirmos uma mensagem na tela, utilizaremos a função abaixo. Ela leva este nome por
ser a palavra em inglês de "imprimir".
print()
"""
aprender_py_print_dois = """
Mandou bem!!!
Pode não parecer que ele não fez nada ainda, mas o Python exibiu uma linha em branco! E 
por que isso acontece?

É que dentro destes parênteses ele espera justamente que informemos o que desejamos
exibir na tela, ou seja, os PARÂMETROS como são mais conhecidos.

Porém tem um detalhe, no nosso caso, como gostariamos de exibir um texto, precisamos 
nos atentar ao inserir um conjunto de ASPAS("") cercando a nossa mensagem, caso contrário
ele não irá entender bem.
"""
aprender_py_input_um = """
=============================================================================
    Um recurso extremamente útil quando pensamos em criar um programa, é obter
algum tipo de informação inserida pelo usuário, afinal, desde os primeiros
computadores criados (lá pela década de 40), já tinham o intuito de processar
dados de forma muito mais produtiva do que conseguiriamos manualmente.

Em Python temos uma FUNÇÃO (nome dado para palavras reservadas da linguagem,
que tem o objetivo definido de realizar atividades específicas; e sempre vem
seguidos de parênteses"()" e em letra minúscula.)

Neste caso a função input() seria como "entrada" como chamariamos em português.
Vamos tentar utilizar esta função? Tente você:
input()
"""
aprender_py_input_dois = """
^^^^^^^^^^^^^^^^^^^^
Como pode ver acima, ele recebeu sua mensagem e imprimiu, conforme você solicitou.
Parabéns!!
"""
aprender_logica = f"""
Hoje em dia, tudo que fazemos em nossos computadores e celulares só são possíveis devido
a uma série de instruções que alguém como nós, passou, passo a passo para esse dispositivo.
O detalhe importante é que ele precisa, diferente de nós humanos, de tudo muito bem
detalhado, pois irá executar da forma exatamente que foi passada.
Nessas instruções, podemos passar grandes listas das mais diferentes instruções, o
computador é muito bom e super rápido nisso!
Podemos inclusive pedir para ele fazer algo várias vezes, ou seja, em um loop; ou também
dizer para repetir um número de vezes!
Aperte ENTER e escolha alguma opção para ver alguns exemplos:
"""

mensagens_resposta_correta = (
    "Parabéns! Você acertou, a resposta era {}",
    "Correto, {} é a resposta certa.",
    "{} é a resposta certa, boa!",
    "Você acertou! ({})",
    "Sim, {} é a resposta.",
)

mensagens_resposta_incorreta = (
    "Oops, essa não é a resposta correta.",
    "Não é bem essa a resposta.",
    "A resposta não é {}",
    "Sinto muito, a alternativa {} está errada.",
    "Resposta incorreta, ops!",
)

aprender_ciberseguranca = f"""
Cibersegurança é um assunto que é de grande importância que saibamos.
Como utilizamos muito a internet hoje em dia, é fundamental que tomemos cuidado e
pensemos várias vezes antes de tomar atitudes online. É muito fácil se passar por 
outras pessoas na internet, e existem muitas pessoas maldosas que se aproveitam disso;
Portanto escolha senhas que não sejam fáceis de serem descobertas e não passem para ninguém.
Não fale com estranhos e desconfie de tudo que te prometer vantagens e benefícios gratuitos.
Cuidado com suas informações de quem você é, onde mora e com quem.
O mundo online é muito divertido e poderoso, mas precisamos nos proteger a todo momento!
"""

questoes_ciberseguranca = {
    """
É seguro compartilhar seu nome completo e endereço com outras pessoas?
A) Sim, porque todo mundo faz isso  \nB) Não, porque isso é informação pessoal
C) Somente se a pessoa parecer confiável  \nD) Só se pedirem de forma educada
""": [
        "B",
        "Não devemos compartilhar informações pessoais, porque isso protege nossa segurança.",
    ],
    """
O que você deve fazer se um jogo pedir o número do cartão de crédito?
A) Pegar o cartão dos pais para garantir que o número está certo  \nB) Procurar no Google um número de cartão qualquer
C) Colocar o número sozinho se você souber  \nD) Pedir para os pais ou responsáveis ajudarem
""": [
        "D",
        "Os adultos precisam ajudar com assuntos de dinheiro online para evitar problemas.\nMesmo que eles não deixem, NUNCA faça isso sem eles, é muito perigoso!",
    ],
    """
Como escolher uma senha?
A) Tentar misturar letras, números e símbolos mas não exagerar para não perder nem esquecer  \nB) Usar a data que você nasceu, para não esquecer
C) Usar uma sequencia como 12345678 já resolve   \nD) Pedir ajuda para um amigo
""": [
        "A",
        "Uma senha boa mistura letras, números e símbolos, mas DEVE ser FÁCIL DE LEMBRAR.",
    ],
    """
É seguro clicar em qualquer link que aparece nos jogos ou vídeos?
A) Sim, se o link for enviado por alguém que você conhece no jogo  \nB) Não, porque alguns links podem ter vírus ou enganar você
C) Só se o link dar prêmios ou moedas no jogo  \nD) Sim, porque todo link na internet é seguro
""": [
        "B",
        "Links desconhecidos podem conter vírus ou enganar você. Sempre tenha cuidado!",
    ],
    """
O que você deve fazer se alguém estranho mandar mensagem pelo jogo ou celular?
A) Se conhecer melhor para ver se a pessoa é confiável  \nB) Responder para fazer novas amizades
C) Contar para um adulto de confiança  \nD) Trocar fotos para ver se a pessoa existe mesmo
""": [
        "C",
        "Sempre devemos desconfiar de todas as pessoas que falamos na internet, é muito fácil uma pessoa se passar por outra..",
    ],
}

questoes_logica = {
    """
"Lógica de programação só serve para computador. Celular e outros aparelhos não precisam."
Está correta essa afirmação?
A) Sim, os estes outros aparelhos são mais modernos  \nB) Não, todos os dispositivos usam lógica
C) Depende, somente se o dispositivo tiver teclado  \nD) Nenhuma das opções
""": [
        "B",
        "Celulares, videogames e outros aparelhos também precisam de lógica para funcionar.",
    ],
    """
O que um "algoritmo" faz?
A) Instala um aplicativo ou programa  \nB) Ensina o computador a desenhar
C) Dá uma sequência de instruções para o computador seguir  \nD) Organiza uma lista de músicas
""": [
        "C",
        "Um algoritmo é uma sequência de passos que o computador segue para resolver um problema.",
    ],
    """
Se passarmos uma sequência de instruções para o computador, como ele irá fazer?
A) Vai seguir a ordem que quiser  \nB) Fazer as mais fáceis primeiro
C) Irá seguir na ordem que foi passada  \nD) Só se pode passar um comando por vez
""": [
        "C",
        "O computador segue as instruções exatamente na ordem em que foram dadas.",
    ],
    """
O que significa um LOOP em programação?
A) Repetir algo sem parar  \nB) Quando pedimos para ele trocar o que está fazendo
C) Um tipo de erro  \nD) Quando pedimos para ele fechar
""": [
        "A",
        "Um loop serve para repetir uma ação várias vezes.",
    ],
    """
Se pedirmos para ele fazer uma conta muito difícil de matemática, o que aconteceria?
A) Ele não sabe fazer contas de matemática  \nB) Ele só pode fazer uma conta de cada vez
C) Somente se usar uma linguagem de programação de matemática  \nD) Ele fará sem problemas
""": [
        "D",
        "O computador consegue fazer contas muito difíceis rapidamente.",
    ],
}

questoes_python = {
    """
O que o comando print() executa em Python?
A) Recebe dados do usuário  \nB) Compara dois números
C) Mostra mensagem ou informação na tela  \nD) Pede para o usuário enviar algum dado
""": [
        "C",
        "O comando print() serve para mostrar textos, números ou mensagens na tela.",
    ],
    """
O que acontece se você escrever print(Olá) (sem aspas)?
A) Vai imprimir a palavra Olá corretamente  \nB) Vai dar erro, pois Olá não está entre aspas
C) Vai pedir para o usuário digitar algo  \nD) Vai imprimir 'print(Olá)'
""": [
        "B",
        "Vai dar erro, porque textos precisam estar entre aspas para o Python entender.",
    ],
    """
O que acontece quando passamos o comando abaixo em Python?
input("Digite sua idade: ")
A) O computador irá exibir a idade da pessoa  \nB) A idade aparece sozinha
C) A pessoa digita a idade e o computador recebe essa informação  \nD) Nada irá acontecer
""": [
        "C",
        "O comando input() faz o computador esperar que a pessoa digite alguma informação.",
    ],
    """
O que é Python?
A) Uma linguagem de programação  \nB) Um idioma
C) Um jogo de computador  \nD) Um personagem de filme
""": [
        "A",
        "Python é uma linguagem usada para criar programas de computador.",
    ],
    """
Para que serve uma linguagem de programação?
A) Para ouvir músicas no computador  \nB) Para deixar o computador mais rápido
C) Para ensinar outros idiomas para o computador  \nD) Para passar informações para o computador de como fazer as coisas
""": [
        "D",
        "Com a linguagem de programação, dizemos ao computador o que ele deve fazer e como fazer.",
    ],
}


# Escrevi na parte de lógica, mas fugiu do assunto;
"""Com a invenção e frequentes avanços da tecnologia e computadores pessoais, foi fundamental
criarmos uma forma mais fácil entre a nossa linguagem e a que o computador entende.

Como ele lida com a transmissão elétrica entre suas 'peças', ele entende o número 0 como
'sem energia' e 1 como 'com energia', e essa mudança entre 0 e 1 frequentes são 
interpretadas como dados. Como seria muito complicado aprendermos a lidarmos com ele dessa
forma, foram criadas linguagens de programação, e utilizando algumas palavras e símbolos 
mais próximas do que conhecemos tornou essa comunicação bem mais fácil."""
