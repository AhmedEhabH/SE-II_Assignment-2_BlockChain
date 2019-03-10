import hashlib
import datetime


class Block:
    block_hash = ''
    prev_hash = ''
    nonce = 0
    transactions = []

    def __init__(self, previous_hash):
        self.prev_hash = previous_hash
        self.timestamp = datetime.datetime.now()
        self.block_hash = self.calc_hash()

    def calc_hash(self):
        block_hash = hashlib.sha256()
        block_hash.update(str(self.prev_hash).encode('utf-8')
                          + str(self.timestamp).encode('utf-8')
                          + str(self.nonce).encode('utf-8'))
        return block_hash.hexdigest()

    def mine(self, difficulty):
        while self.block_hash[0: difficulty] != '0'*difficulty:
            self.nonce += 1
            self.block_hash = self.calc_hash()
        print("Block Mined " + self.block_hash)
        
        def add_transaction(self, transaction):
        # print(transaction)
        if transaction is not None: return False
        if self.prev_hash != '0' or not transaction:
            print("Transaction failed to process. Discarded.")
            return False
        self.transactions.append(transaction)
        print("Transaction Successfully added to Block")
        return True
