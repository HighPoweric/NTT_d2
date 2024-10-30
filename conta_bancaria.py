import parameters
from datetime import datetime
from decimal import Decimal, ROUND_DOWN

class ContaBancaria:
    def __init__(self):
        self.saques_efetuados = 0
        self.saldo = 0
        self.transacoes = {} #dicionario que vai conter uma lista com dic de cada transacao {fecha [{trans 1}, {trans 2},... {trans n}]}
        self.opcoes = {
            'D': self.deposito,
            'S': self.saque,
            'E': self.extrato
        }

    def deposito (self):
        #saimos se não tem mais transações restantes
        if not self.transacoes_restantes():
            print("Limite de transações diarias alcançado!")
            return
        while True:
            try:
                print("indique um valor para deposito ou digite 0 para cancelar")
                #Obtendo o valor arredondando para baixo em duas casas decimais
                valor = Decimal(input("R$ ")).quantize(Decimal('0.01'), rounding=ROUND_DOWN) 
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
            self.transacoes.setdefault(datetime.now().date(), []).append({
                'data': datetime.now().isoformat(timespec='seconds'),
                'tipo':'deposito',
                'valor': valor
                })
            print(f"Depósito de R${valor} realizado com sucesso.")              
            break

    def saque (self):
        #saimos se não tem mais transações restantes
        if not self.transacoes_restantes():
            print("Limite de transações diarias alcançado!")
            return
        saques_restantes = self.saques_restantes()
        print(f"Seu saldo é de R${self.saldo} você tem {saques_restantes} saques restantes hoje")
        #saimos se não tem mais saques restantes
        if saques_restantes <= 0: return
        #iniciamos a funcionalidade de saque
        while True:
            try:                
                print("indique um valor para Saque ou digite 0 para cancelar")
                #Obtendo o valor arredondando para baixo em duas casas decimais
                valor = Decimal(input("R$ ")).quantize(Decimal('0.01'), rounding=ROUND_DOWN) 
            except ValueError: #valor nao numerico
                print('Por favor digite um valor numérico válido')
                continue

            if valor < 0:  # Verifica se o valor é positivo
                print("O valor do saque deve ser positivo.")
                continue
            #saindo do deposito
            elif valor == 0: 
                break
            #verificando se ultrapassa o limite de saque
            elif valor > parameters.LIMITE_VALOR_SAQUE:
                print(f'Valor acima do seu limite de saque de R${parameters.LIMITE_VALOR_SAQUE}')
                continue
            #Verificando saldo para saque
            elif not parameters.BOL_SAQUE_ALEM_SALDO and valor > self.saldo:
                print("O valor do saque não pode superar seu saldo.")
                continue

            #atualizando saldo, quantidade de saques e registrando a transacao
            self.saldo -= valor
            self.saques_efetuados += 1
            self.transacoes.setdefault(datetime.now().date(), []).append({
                'data': datetime.now().isoformat(timespec='seconds'),
                'tipo':'saque',
                'valor': valor
                })
            print(f"Saque de R${valor} realizado com sucesso.")              
            break

    def extrato (self):
        if not self.transacoes:
            print("Não existe transações")
            return
        total_depositado = 0
        total_saques = 0
        print("Extrato Bancario:")
        #percorremos nossa lista de transacoes
        for data, transacoes_data in self.transacoes.items():
            print(f"Data: {data}")
            for transacao in transacoes_data:
                if transacao['tipo'] == 'deposito':
                    print(f"{transacao['data']}, Depósito: R${transacao['valor']}")
                    total_depositado += transacao['valor']
                elif transacao['tipo'] == 'saque': #saque
                    print(f"{transacao['data']}, Saque: -R${transacao['valor']}")
                    total_saques += transacao['valor']
        print(f"Saldo final: R${self.saldo} - Total depositado: R${total_depositado} - Total retirado: R${total_saques}")


    def saques_restantes(self):
        return parameters.LIMITE_QUANT_SAQUE - self.saques_efetuados
    
    def transacoes_restantes(self): #retorna quantos transacoes restantes faltan ou 0 (False) se não tiver nenhuma restante
        return parameters.LIMITE_TRANS_DIA - len(self.transacoes.get(datetime.now().date(), []))
