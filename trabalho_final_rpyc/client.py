import rpyc


if __name__ == '__main__':
    conn = rpyc.connect('localhost', 4040)
    math = conn.root

    print("Digite sua Matrícula e Senha")
    matricula = int(input("Matrícula: ").strip())
    senha = int(input("Senha: ").strip())

    if math.exposed_validacao(matricula, senha):
        saldo_atual = math.exposed_consultar_saldo()
        print(saldo_atual)

        while True:
            menu = math.exposed_menu()
            print(menu)

            resp = int(input("Digite o número da opção desejada: "))

            resultados = math.exposed_fazer_pedido(resp)

            for resultado in resultados:
                print(resultado)

            if resp == 0:
                break  

    else:
        print("Login incorreto")
        exit()
