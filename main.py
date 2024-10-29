#imports
from conta_bancaria import ContaBancaria
import time  
#Vars
cc = ContaBancaria()

MENU_INICIAL = f'''

Escolhas as seguintes opções
(D) - Depósito
(S) - Saque (disponiveis hoje: {cc.saques_restantes()})
(E) - Extrato
-------------------
(X) - Sair

'''



########## Begin ###################
print('''##################################
####### Programa Bancario ########
##################################''')


while True:
    i = input(MENU_INICIAL).upper()
    if i == "X": break #Saindo do Menu
    cc.opcoes.get(i, lambda: print("Opção indisponível, tente novamente... \n\n"))()
    time.sleep(2)


########## END ###################
print('''##################################
####### Obrigado por usar ########
####### nossos Serviços!  ########
##################################''')
