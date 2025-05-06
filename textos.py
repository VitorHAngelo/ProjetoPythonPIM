# Arquivo de textos para o projeto de Python


# ============================= MENUS =============================

menu_login = f"""{' Menu Login '.center(50, '=')}\n
Bem vindo ao menu! Escolha a opção desejada:
1 - Login
2 - Criar sua conta
3 - Recuperar seu login
4 - Sair (Encerra o programa)\n"""

menu_principal = (
    f"{' Menu Principal '.center(50, '=')}\n"
    + """
Bem vindo, {}! Escolha a opção desejada: 
1 - Aprender (Lições sobre diferentes assuntos)
2 - Quiz (Teste seus conhecimentos sobre as matérias apresentadas)
3 - Consulte seu progresso (Confira sua média de acertos ou seus minutos ativo no programa)
4 - Logout (Sair da sua conta aluno)
5 - Sair (Encerra o programa)\n"""
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
5 - Voltar ao Menu Aprender\n"""

menu_aprender_python = f"""{' Menu Aprender PYTHON '.center(50, '=')}\n
Escolha uma lição sobre lógica:
1 - > O que é Python
2 - > Função print()
3 - > Função input()
4 - Voltar ao Menu Aprender()\n"""

# ============================ APRENDER ============================

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
Nessas instruções, podemos passar as mais diferentes instruções, o computador é muito bom
e super rápido nisso! Aperte ENTER e escolha alguma opção para ver alguns exemplos:
"""


aprender_ciberseguranca = f"""
aprender_segurança
"""

# Escrevi na parte de lógica, mas fugiu do assunto;
"""Com a invenção e frequentes avanços da tecnologia e computadores pessoais, foi fundamental
criarmos uma forma mais fácil entre a nossa linguagem e a que o computador entende.

Como ele lida com a transmissão elétrica entre suas 'peças', ele entende o número 0 como
'sem energia' e 1 como 'com energia', e essa mudança entre 0 e 1 frequentes são 
interpretadas como dados. Como seria muito complicado aprendermos a lidarmos com ele dessa
forma, foram criadas linguagens de programação, e utilizando algumas palavras e símbolos 
mais próximas do que conhecemos tornou essa comunicação bem mais fácil."""
