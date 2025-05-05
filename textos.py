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
1 - Aprender (Acesse um texto informativo sobre Phyton)
2 - Quiz (Comece o Quiz de perguntas sobre Python)
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

aprender_ciberseguranca = f"""
aprender_segurança
"""

aprender_logica = f"""
aprender_lógica
"""
