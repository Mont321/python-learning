class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self.balance = 0

    def deposit (self, amount):
        self.balance += amount
        print(f"Пополнено на {amount}. Баланс: {self.balance}")

    def withdraw(self,amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Снято {amount}. Баланс: {self.balance}")
        else:
            print("Недостаточно средств")
    def get_balance(self):
        return self.balance
    


account = BankAccount("Иван")
account.deposit(1000)
account.withdraw(300)
account.withdraw(1000)

print(f"Баланс: {account.get_balance()}")