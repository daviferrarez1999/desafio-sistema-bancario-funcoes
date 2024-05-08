import textwrap

def menu():
    menu = """

    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Criar usuario
    [5] Criar conta corrente
    [6] Listar contas
    [7] Sair

    => """

    return input(textwrap.dedent(menu))


def deposito(saldo, valor, extrato, /):   
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R${valor:.2f}\n"
    else:
        print("Deposite apenas valores maiores que zero")

    return saldo, extrato

def saque(*,saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saque = numero_saques >= limite_saques
    if excedeu_saldo:
        print("Operação inválida! Você excedeu seu saldo.")
    elif excedeu_limite:
        print("Operação inválida! O valor do saque excedeu o limite.")
    elif excedeu_saque:
        print("Operação inválida! Você excedeu o número máximo de saques.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R${valor:.2f}\n"
        numero_saques += 1
    else:
        print("Operação inválida! O valor informado está inválido.")

    return saldo, extrato 
    
def mostrar_extrato(saldo, /, *, extrato):
    print("=============Extrato=============")
    print("Não foram feitas movimentações." if not extrato else extrato)
    print(f"Saldo: R$ {saldo:.2f}") 
    print("====================================")

def criar_usuario(usuarios):
    cpf = input("Informe seu CPF (apenas números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá possui um usuário com o CPF informado! ")
        return
    
    nome = input("Informe seu nome completo: ")
    data_nascimento = input("Informe sua data de nascimento: ")
    endereco = input("Informe seu endereço com o padrão: logradouro, numero - bairro - cidade/sigla do estado:  ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None 

def criar_conta_corrente(agencia, numero_conta, usuarios):
    cpf = input("Informe seu CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\nO usuario não foi encontrado. Processo de criação de conta encerrado!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência: \t{conta['agencia']}
            Conta Corrente: \t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    usuarios = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "1":
            valor = float(input("Informe o valor que deseja depositar: "))
            saldo, extrato = deposito(saldo, valor, extrato)

        elif opcao == "2":
            valor = float(input("Informe o valor que deseja sacar: "))

            saldo, extrato = saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "3":
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta_corrente(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()