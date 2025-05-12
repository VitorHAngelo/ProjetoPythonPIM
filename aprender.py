from utilitarios import limpar_console
from random import randint


def aprender_python_print(textos):
    """
    Função destinada a apresentar a lição de Python print().
    """
    print(textos.aprender_py_print_um)  # Mostra a primeira parte do tutorial
    comando_usuario = input("Tente você mesmo! Digite a função acima.\n").replace(
        " ", ""
    )  # Recebe a tentativa do usuário de digitar a função e tira os espaços com replace
    if comando_usuario.lower() == "sair":
        return
    while (
        comando_usuario != "print()"
    ):  # Enquanto ele não digitar corretamente, será solicitado novamente
        comando_usuario = input(
            "Tente mais uma vez, digite a função abaixo:\nprint()\nLembre-se dos \
parênteses e de utilizar letras minúsculas.\n (Ou digite 'sair' para voltar ao Menu)\n"
        ).replace(
            " ", ""
        )  # Dicas caso o usuário erre o comando
        if comando_usuario.lower() == "sair":
            return

    print(f"\n{textos.aprender_py_print_dois}")  # Mostra a segunda parte do tutorial
    while True:
        entrada_split = (
            input('Tente você mesmo! Digite a função:  print("mensagem").\n')
            .replace('"', "'")
            .split("'")
        )

        if comando_usuario.lower() == "sair":
            return

        if len(entrada_split) != 3:
            print(
                "Tente mais uma vez, digite a função a seguir, o uso das aspas são \
imprescindíveis.  print(\"mensagem\")  (Ou digite 'sair' para voltar ao Menu)\n"
            )
            continue
        elif entrada_split[0] != "print(" and entrada_split[-1] != ")":
            print(
                "Tente mais uma vez, digite a função a seguir, o uso das aspas são \
imprescindíveis.  print(\"mensagem\")  (Ou digite 'sair' para voltar ao Menu)\n"
            )
            continue
        else:
            break
    print(
        f"\n{entrada_split[1]}\n\nMuito bem! É assim que se faz!! Como você pode ver acima,\n\
foi impresso o conteúdo que você definiu entre aspas em uma nova linha.\n"
    )
    input(f"Aperte ENTER para terminar esta atividade.\n")
    limpar_console()


def aprender_python_input(textos):
    """
    Função destinada a apresentar a lição de Python input().
    """
    print(textos.aprender_py_input_um)
    comando_usuario = input()
    if comando_usuario.lower() == "sair":
        return
    while comando_usuario != "input()":
        comando_usuario = input(
            "Vamos tentar mais uma vez, lembre-se: funções utilizam letras minúsculas e tem parênteses depois da palavra.\n"
        )
        if comando_usuario.lower() == "sair":
            return

    entrada_usuario = input(
        "Exatamente assim! Agora o Python vai querer receber sua mensagem, tente escrever algo:\n"
    )
    print(f"\n{entrada_usuario}")  # Imprime o que o usuário inseriu no input acima
    print(textos.aprender_py_input_dois)  # Imprime mensagem dois
    input(f"\nAperte ENTER para terminar esta atividade.")


def aprender_logica_numero_maior():
    while True:
        print("Vamos comparar qual número é maior.")
        entrada_um = input("Insira o primeiro número:\n")
        entrada_dois = input(f"Insira o segundo número:\n{entrada_um} é maior que ")
        limpar_console()
        print(f"> {entrada_dois} é maior que {entrada_um}?\n")
        try:
            entrada_um, entrada_dois = float(entrada_um), float(entrada_dois)
            if entrada_um > entrada_dois:
                print(f"> {entrada_um} é maior que {entrada_dois}")
            elif entrada_dois > entrada_um:
                print(f"> {entrada_dois} é maior que {entrada_um}")
            elif entrada_um == entrada_dois:
                print(f"> {entrada_um} e {entrada_dois} são iguais.")

            if (
                input(
                    "Caso queira tentar novamente, digite 's', ou aperte ENTER para voltar ao Menu\n\n"
                ).lower()
                == "s"
            ):
                limpar_console()
                continue
            limpar_console()
            break
        except:
            print("Entrada inválida, insira somente números. ", end="")
            continue


def aprender_logica_par_impar():
    while True:
        entrada_um = input("Digite um número e vou te dizer se é par ou ímpar: ")
        try:
            if int(entrada_um) % 2 == 0:
                print(f"{entrada_um} é par!")
            else:
                print(f"{entrada_um} é ímpar!")
            if (
                input(
                    "Caso queira tentar novamente, digite 's', ou aperte ENTER para voltar ao Menu\n"
                ).lower()
                == "s"
            ):
                limpar_console()
                continue
            limpar_console()
            break
        except:
            print("Entrada inválida, insira somente números. ", end="")


def aprender_logica_numeros_iguais():
    while True:
        entrada_um = input(
            "Vou tentar adivinhar um número que você pensou...\nDigite um número de 1 a 3 ou 'sair' para voltar: "
        ).lower()
        if entrada_um == "sair":
            break
        try:
            entrada_um = int(entrada_um)
        except:
            print("Entrada inválida.")
            continue
        numero_aleatorio = randint(1, 3)
        if entrada_um == numero_aleatorio:
            print(f"Pensamos juntos no número {entrada_um}!!!")
        elif entrada_um not in range(1, 4):
            print("Número inválido.")
            continue
        else:
            print(f"Pensei em {numero_aleatorio} e você em {entrada_um} hahah.")
        continue


def aprender_logica_tabuada():
    tabuada_escolhida = None
    quantidade_escolhida = None
    limpar_console()
    while True:
        tabuada_escolhida = input("Digite um número para ver sua tabuada: ")
        try:
            tabuada_escolhida = int(tabuada_escolhida)
            break
        except:
            print("Entrada inválida.")
    limpar_console()
    while True:
        quantidade_escolhida = input(
            f"Você gostaria de ver a tabuada do {tabuada_escolhida} até que número? "
        )
        try:
            quantidade_escolhida = int(quantidade_escolhida)
            break
        except:
            print("Entrada inválida.")
    limpar_console()
    print(f"Imprimindo tabuada do {tabuada_escolhida}, do 1 ao {quantidade_escolhida}:")
    for i in range(1, quantidade_escolhida + 1):
        print(
            f"{tabuada_escolhida}".rjust(3, " ")
            + " x "
            + f"{i}".ljust(3, " ")
            + " = "
            + str(tabuada_escolhida * i)
        )
    input(
        "Este é um exemplo de LOOP, onde o programa irá repetir a tabuada pelo tanto\
de vezes que você determinou!"
    )


def menu_aprender_logica(textos):
    while True:
        limpar_console()
        escolha = None
        while escolha not in ("1", "2", "3", "4", "5", "6"):
            escolha = input(textos.menu_aprender_logica)
        if escolha == "1":
            input(textos.aprender_logica)
            continue
        elif escolha == "2":
            aprender_logica_numero_maior()
        elif escolha == "3":
            aprender_logica_par_impar()
        elif escolha == "4":
            aprender_logica_numeros_iguais()
        elif escolha == "5":
            aprender_logica_tabuada()
        else:
            return


def menu_aprender_python(textos):
    while True:
        limpar_console()
        escolha = None
        while escolha not in ("1", "2", "3", "4"):
            escolha = input(textos.menu_aprender_python)
        if escolha == "1":  # O que é Python
            print("aprender_python")
            continue
        elif escolha == "2":  # Aprender print()
            aprender_python_print(textos)
        elif escolha == "3":  # Aprender input()
            aprender_python_input(textos)
        else:
            break
