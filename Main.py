from abc import ABC, abstractclassmethod, abstractproperty

class Conta:
    def __init__(self, saldo, numero, agencia, cliente):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
    
    def saldo(self):
        return f'{float(self._saldo)}'
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente) 
    
    def sacar(self):
        qtde = float(input('Quando vc quer sacar? '))
        if qtde < 0:
            print('Digite um número positivo!')
        if qtde < self._saldo:
            self._saldo -= qtde
            print(f'{qtde} sacado com sucesso! ')
        else:
            print(f'Você não tem saldo o suficiente!')

    
    def depositar(self):
        deposito = float(input('Quanto você quer depositar? '))
        self._saldo += deposito
        print(f'{deposito} adicionado com sucesso!')
        if deposito < 0:
            print('Digite um número positivo!')
        
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len([t for t in self._historico.transações if t['tipo'] == Saque.__name__])

        if valor > self.limite:
            print('O valor do saque excedeu o limite! Falha!')
        elif numero_saques > self.limite_saques:
            print('O número limite de saques foi excedido! Falha!')
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f'Agência -> {self.agencia}, C/C -> {self.numero}, Titular -> {self._cliente.nome}'
    
class Historico:
    def __init__(self):
        self._transações = []
    
    @property
    def transações(self):
        return self._transações
    def adicionar_transação(self, transação):
        self._transações.append({'tipo': transação.__class__.name__, 'valor': transação.valor})

class Transação(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transação):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        boa = conta.sacar(self.valor)
        if boa:
            conta.historico.adicionar_transação(self)

class Deposito(Transação):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    def registrar(self, conta):
        boa = conta.depositar(self.valor)
        if boa:
            conta.historico.adicionar_transação(self)

class Cliente:
    def __init__(self, end):
        self.endereço = end
        self.contas = []
    
    def realizar_transaçao(self, conta, transação):
        transação.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Pessoa(Cliente):
    def __init__(self, cpf, nome, data, end):
        self._cpf = cpf
        self.nome = nome 
        self.data = data
        super().__init__(end)

def menu():
    menu = """\n
    ++++++++++MENU++++++++++
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [nc] Nova Conta
    [lc] Listar Contas
    [nu] Novo Usuário
    [q] Sair
    ->
"""
    return input(menu)

def depositar(clientes):
    cpf = input('CPF -> ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não foi encontrado!')
        return
    valor = float(input('Valor do depósito -> '))
    transação = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.realizar_transação(conta, transação)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [c for c in clientes if c._cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('Esse cliente não possui conta!')
        return
    return cliente.contas[0]

def sacar(clientes):
    cpf = input('CPF -> ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não foi encontrado!')
        return 
    valor = float(input('Saque -> '))
    transação = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return 
    cliente.realizar_transação(conta, transação)

def exibir_extrato(clientes):
    cpf = input('CPF -> ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não foi encontrado!')
        return 
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return 
    print('==EXTARTO==')
    transações = conta.hitorico.transações

    extrato = ''
    if not transações:
        extrato = 'Não há movimentação'
    else:
        for transação in transações:
            extrato += f'{transação['tipo']}: R$ {transação['valor']:.2f}'
    
    print(extrato)
    print(f'Saldo -> {conta.saldo:.2f}')

def criar_conta(n_conta, clientes, contas):
    cpf = input('CPf -> ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não foi encontrado!')
        return 
    conta = ContaCorrente.nova_conta(cliente = cliente, numero = n_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print('Conta realizada com sucesso!')

def listar_contas(contas):
    for c in contas:
        print('-=-' * 10)
        print((str(c)))

def criar_cliente(clientes):
    cpf = input('CPF -> ')
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print('Já tem cliente com o mesmo cpf.')
        return 
    nome = input('Nome -> ')
    data = input('Data de Nascimento -> ')
    end = input('Endereço -> ')
    cliente = Pessoa(nome = nome, data = data, cpf = cpf, end = end)
    clientes.append(cliente)
    print('Cliente criado com suceso!')

def main():
    clientes = []
    contas = []

    while True:
        op = menu()

        if op == 'd':
            depositar(clientes)
        elif op == 's':
            sacar(clientes)
        elif op == 'e':
            exibir_extrato(clientes)
        elif op  == 'nu':
            criar_cliente(clientes)
        elif op == 'nc':
            numero_conta = len(contas) +1
            criar_conta(numero_conta, clientes, contas)
        elif op == 'lc':
            listar_contas(contas)
        elif op == 'q':
            break

main()