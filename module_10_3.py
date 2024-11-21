import threading
from random import randint
import time


class Bank(threading.Thread):
    balance = 0
    lock = threading.Lock()
    deposit_transaction = 100
    take_transaction = 100

    def __init__(self):
        threading.Thread.__init__(self)

    def deposit(self):

        while self.deposit_transaction:
            if self.balance >= 500 and self.lock.locked() == True:
                self.lock.release()
                time.sleep(0.001)
            else:
                rand_int = randint(50, 500)
                self.balance += rand_int
                print(f"Пополнение: {rand_int}. Баланс: {self.balance} ")
                self.deposit_transaction -= 1
                time.sleep(0.001)

    def take(self):
        self.take_transaction = 100
        while self.take_transaction:
            rand_int = randint(50, 500)
            print(f'Запрос на {rand_int} ')
            if rand_int <= self.balance:
                self.balance -= rand_int
                print(f"Снятие: {rand_int}. Баланс: {self.balance}")
                self.take_transaction -= 1
                time.sleep(0.001)
            elif self.deposit_transaction == 0:
                exit()
            else:
                print("Запрос отклонён, недостаточно средств")
                self.lock.acquire()
                time.sleep(0.001)


bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
print(f'Было произведено {100-bk.deposit_transaction} транзакций пополнения счета.')
print(f'Было произведено {100-bk.take_transaction} транзакций снятия.')
