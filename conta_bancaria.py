import parameters
from datetime import datetime

class ContaBancaria:
    def __init__(self):
        self.saques_efetuados = 0
        self.saldo = 0
        self.transacoes = [] #lista que vai conter um dic com a data e valor da transacao
        self.opcoes = {
            'D': self.deposito,
            'S': self.saque,
            'E': self.extrato
        }

    def deposito (self):
        while True:
            try:
                print("indique um valor para deposito ou digite 0 para cancelar")
                valor = int(float(input("R$ ")) * 100)/100 #metodo patenteado do Eric para truncar em duas casas decimais
            except ValueError: #valor nao numerico
                print('Por favor digite um valor numérico válido')
                continue

            if valor < 0:  # Verifica se o valor é positivo
                print("O valor do depósito deve ser positivo.")
                continue
            elif valor == 0: #saindo do deposito
                break
            #atualizando saldo e registrando a transacao
            self.saldo += valor 
            self.transacoes.append({
                'data': datetime.now().isoformat(timespec='seconds'),
                'tipo':'deposito',
                'valor': valor
                })
            print(f"Depósito de R${valor} realizado com sucesso.")              
            break

    def saque (self, valor):
        pass

    def extrato (self):
        if not self.transacoes:
            print("Não existe transações")
            return
        total_depositado = 0
        total_saques = 0
        print("Extrato Bancario:")
        #percorremos nossa lista de transacoes
        for transacao in self.transacoes:
            if transacao['tipo'] == 'deposito':
                print(f"{transacao['data']}, Depósito: R${transacao['valor']}")
                total_depositado += transacao['valor']
            elif transacao['tipo'] == 'saque': #saque
                print(f"{transacao['data']}, Saque: -R${transacao['valor']}")
                total_saques += transacao['valor']
        print(f"Saldo final: R${self.saldo} - Total depositado: R${total_depositado} - Total retirado: R${total_saques}")


    def saques_restantes(self):
        return parameters.LIMITE_QUANT_SAQUE - self.saques_efetuados