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
    def nova_conta(self, cliente, numero):
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