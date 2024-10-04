class bank_account():
    def __init__(self, balance):
        self.balance = balance
    
    def getBalance(self):
        return self.balance
    
    def debited(self, amount):
        if(amount > self.balance):
            print("Insufficent Balance")
        self.balance -= amount
        print("Remaining balance after debited amount is: ", self.balance)
    
    def credited(self, amount):
        self.balance += amount
        print("Remaining balance after credited amount is: ", self.balance)


user1 = bank_account(7600)
print(user1.getBalance()) 
user1.credited(1000)
user1.debited(600)
user1.debited(100)
