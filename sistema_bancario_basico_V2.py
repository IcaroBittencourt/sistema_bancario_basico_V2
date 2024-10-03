import sys
import time
import textwrap

#PROCESSANDO...
def processando(duracao):
    fim_processando = time.time() + duracao
    while time.time() < fim_processando:
        for pontinhos in range(4):
            sys.stdout.write("\r\033[1mProcessando" + "." * pontinhos + "   \033[m")
            sys.stdout.flush()
            time.sleep(0.7)
            
    sys.stdout.write(" ")


def menu():
    menu = """\n \033[1m
    ==================== MENU ====================
     [1]  Depositar
     [2]  Sacar
     [3]  Extrato
     [4]  Nova Conta
     [5]  Novo Usuário
     [6]  Sair
     
    => \033[m"""
    return input(textwrap.dedent(menu))

#DEPOSITAR
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        processando(3)
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n \033[1m===\033[m \033[1;32mDepósito realizado com sucesso!\033[m \033[1m===\033[m")
        processando(1)
    else:
        processando(3)
        print("\n\033[1m===\033[m \033[1;31mA operação falhou! O valor informado é invalido.\033[m \033[1m===\033[m")
    return saldo, extrato


#SACAR
def sacar(*, saldo,valor, extrato, limite, numero_saques, limite_saques):
    exedeu_saldo = valor > saldo
    exedeu_limite = valor > limite
    exedeu_saques = numero_saques >= limite_saques
    
    if exedeu_saldo:
        processando(3)
        print("\n \033[1m===\033[m \033[1;31mA Operação falhou! Você não tem saldo suficiente.\033[m \033[1m===\033[m")
        
    elif exedeu_limite:
        processando(3)
        print("\n \033[1m===\033[m \033[1;31mA operação falhou! O valor do saque execede o seu limite.\033[m \033[1m===\033[m")
    
    elif exedeu_saques:
        processando(3)
        print("\n \033[1m===\033[m \033[1;31mA operação falhou! O número máximo de saques foi exedido.\033[m \033[1m===\033[m")
    
    elif valor > 0:
        processando(3)
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n \033[1m===\033[m \033[1;32mSaque realizado com sucesso!\033[m \033[1m===\033[m")
        
    else:
        processando(3) 
        print("\n \033[1m===\033[m \033[1;31mA operação falhou! O valor informado é inválido.\033[m \033[1m===\033[m")
        
    return saldo, extrato

#EXTRATO
def exibir_extrato(saldo, /, *, extrato):
    processando(2)
    print("\n\033[1m================== EXTRATO ==================\033[m")
    print("\n\033[1mAinda não foram realizadas movimentações.\033[m" if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("\033[1m=============================================\033[m")
    
    
 #CRIAR_USUARIO  
def criar_usuario(usuarios):
    cpf = input("\033[1minforme o CPF (somente números): \033[m")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario: 
        processando(3)
        print("\n \033[1m===\033[m \033[1;31mJá existe um usuário com este CPF\033[m \033[1m===\033[m")
        return
    
    nome = input("\033[1mInforme o seu nome completo: \033[m")
    data_nascimento = input("\033[1mInforme a sua data de nascimento (dd-mm-aaaa): \033[m")
    endereco = input("\033[1mInforme o endereço (logadouro, numero - bairro - cidade - sigla do estado): \033[1m")
    
    usuarios.append({
        "nome": nome, 
        "data_nascimento": data_nascimento, 
        "cpf": cpf, 
        "esdereco": endereco
        })
    processando(3)
    print("\n\033[1m===\033[m \033[1;32mUsuário criado com sucesso!\033[m \033[1m===\033[m")
   
#FILTRAR_USUARIOS
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

#CRIAR_CONTA
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("\033[1mInforme o seu CPF: \033[m")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        processando(3)
        print("\n\033[1m===\033[m \033[1;32mConta criada com sucesso!\033[m \033[1m===\033[m")
        return {
            "agencia": agencia, 
            "numero_conta": numero_conta, 
            "usuario": usuario
            }
    print("\n \033[1m===\033[m \033[1;31mUsuário não encontrado, criação de conta encerrada!\033[m \033[1m===\033[m")
   
#LISTA_DE_CONTAS
def lista_contas(contas):
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            c/c:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("\033[1m=\033[m" * 100)
        print(textwrap.dedent(linha))
        
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    
    while True:
        opcao = menu()
        
        if opcao == "1":
            valor = float(input("\033[1mInforme o valor do depósito: \033[m"))
            
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("\033[1mInforme o valor do saque: \033[m"))
            
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )
            
        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == "4":
            criar_usuario(usuarios)
            
        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == "6":
            lista_contas(contas)
        
        elif opcao == "7":
            break
        
        else:
            print("\033[1;31mOperação inválida, por favor selecione novamente a operação desejada.\033[m")            
            
main()