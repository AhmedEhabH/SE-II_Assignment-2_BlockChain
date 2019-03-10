import ecdsa


class Wallet:
    transactions_in = []
    transactions_out = []
    balance = 0.0
    id = 0
    
    def __init__(self, balance, id=0):
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.balance = balance
        self.id = id

    def get_private_key(self):
        return self.private_key

    def get_public_key(self):
        return self.public_key

    def get_balance(self):
        return self.balance + self.get_input_values() - self.get_output_values()

    def get_input_values(self):
        total = 0.0
        if len(self.transactions_in) != 0:
            for trans in self.transactions_in:
                if trans.receiver_public_key == self.get_public_key():
                    total += trans.value
        return total

    def get_output_values(self):
        total = 0.0
        if len(self.transactions_out) != 0:
            for trans in self.transactions_out:
                if trans.sender_public_key == self.get_public_key():
                    total += trans.value
        return total

    def send_funds(self, receiver_public_key, value, receiver_port=0):
        print('Wallet in port ' + str(self.id) + ' try to send (' + str(value) + ') to Wallet in port ' + str(receiver_port))
        if self.get_balance() < value:
            print("Not Enough funds to send transaction. Transaction Discarded.")
            return False

        from Transaction import Transaction
        new_transaction = Transaction(sender_public_key=self.get_public_key(),
                                      receiver_public_key=receiver_public_key,
                                      value=value)
        if not new_transaction.verify_signature(self.get_public_key(),
                                                new_transaction.generate_signature(self.get_private_key())):
            print('Transaction failed wrong signature')
            return False
        self.transactions_out.append(new_transaction)
        self.transactions_in.append(new_transaction)
        return True
