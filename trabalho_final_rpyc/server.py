import rpyc



class Servidor(rpyc.Service):
    def on_connect(self, conn):
        self.matricula = 123
        self.senha = 123
        self.saldo = 100
        self.produtos_adquiridos = []

    def on_disconnect(self, conn):
        pass

#A palavra "exposed" serve para indicar explicitamente quais métodos devem ser expostos e acessíveis remotamente
    def exposed_validacao(self, matricula, senha):
        if self.matricula == matricula and self.senha == senha:
            return True
        return False

    def exposed_consultar_saldo(self):
        return f"Seu saldo atual é: R$ {self.saldo}"

    def exposed_menu(self):
        return """
            1-Hamburger - R$ 10,00.
            2-Refrigerante - R$ 3,00.
            3-Batata Frita - R$ 2,00.
            4-Suco Natural - R$ 8,00.
            5-Maionese Extra - R$ 2,00.
            0-Finalizar Pedido.
            Digite sua escolha: """

    def exposed_fazer_pedido(self, escolha):
        if escolha == 0:
            resultado_final = [f"Pedido finalizado. Seu saldo final é: R$ {self.saldo}"]
            if self.produtos_adquiridos:
                resultado_final.append("Produtos adquiridos nesta compra:")
                for produto in self.produtos_adquiridos:
                    resultado_final.append(produto)
            return resultado_final

        resultados = []
        if escolha in [1, 2, 3, 4, 5]:
            produto, preco = self.obter_produto_e_preco(escolha)
            compra = preco
            if self.saldo >= compra:
                self.saldo -= compra
                self.produtos_adquiridos.append(f"{produto} - R$ {preco:.2f}")
                resultados.append(f"{produto} - R$ {preco:.2f}. Saldo atual: R$ {self.saldo}")
            else:
                resultados.append(f"Saldo insuficiente para {produto}.")
        else:
            resultados.append("Opção inválida. Por favor, escolha uma opção válida (1, 2, 3, 4, 5 ou 0 para finalizar).")

        return resultados

    def obter_produto_e_preco(self, escolha):
        produtos = {
            1: ("Hamburger", 10.00),
            2: ("Refrigerante", 3.00),
            3: ("Batata Frita", 2.00),
            4: ("Suco Natural", 8.00),
            5: ("Maionese Extra", 2.00),
        }
        return produtos[escolha]


def main():
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(Servidor, port=4040)
    t.start()

if __name__ == '__main__':
    main()

