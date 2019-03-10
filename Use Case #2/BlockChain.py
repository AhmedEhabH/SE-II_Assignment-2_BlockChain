from Block import Block


class BlockChain:
    block_chain = []
    difficulty = 2
    transactions = []

    def __init__(self, difficulty=2):
        self.difficulty = difficulty

    def add_block(self, new_block):
        new_block.mine(difficulty=self.difficulty)
        self.block_chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.block_chain)):
            current_block = self.block_chain[i]
            prev_block = self.block_chain[i-1]

            if current_block.block_hash != current_block.calc_hash():
                print("Current Hashes not equal")
                return False

            if prev_block.block_hash != current_block.prev_hash:
                print("Previous Hashes not equal")
                return False

            if current_block.block_hash[0: self.difficulty] != '0' * self.difficulty:
                print("This block hasn't been mined")
                return False

            print("Block Chain is valid")
            return True

    def main(self):
        from Wallet import Wallet
        wallet_a = Wallet(150.0, 8081)
        wallet_b = Wallet(200.0, 8082)
        base_wallet = Wallet(100.0, 8080)

        from Transaction import Transaction
        genesis_transaction = Transaction(base_wallet.get_public_key(), wallet_a.get_public_key(), 100.0)
        signature = genesis_transaction.generate_signature(base_wallet.get_private_key())
        genesis_transaction.transaction_id = 0
        genesis_transaction.transactions_out.append(genesis_transaction)
        self.transactions.append(genesis_transaction)

        print("Creating and Mining Genesis block... ")
        genesis_block = Block(0)
        genesis_block.add_transaction(transaction=genesis_transaction)
        self.add_block(genesis_block)

        # testing
        block_1 = Block(genesis_block.block_hash)
        print("\n\nWalletA's balance is:", wallet_a.get_balance())
        print("\nWalletA is Attempting to send funds (40) to WalletB")
        value = 40.0
        if wallet_a.send_funds(wallet_b.get_public_key(), value=value, receiver_port=wallet_b.id):
            block_1.add_transaction(Transaction(wallet_a.get_public_key(), wallet_b.get_public_key(), value=value))
            self.add_block(block_1)
        print("\nWalletA's balance is: " , wallet_a.get_balance())
        print("WalletB's balance is: ", wallet_b.get_balance())

        block_2 = Block(block_1.block_hash)
        print("\n\nWalletA's balance is:", wallet_a.get_balance())
        print("\nWalletA is Attempting to send funds (1000) to WalletB")
        value = 1000.0
        if wallet_a.send_funds(wallet_b.get_public_key(), value=value, receiver_port=wallet_b.id):
            block_2.add_transaction(Transaction(wallet_a.get_public_key(), wallet_b.get_public_key(), value=value))
            self.add_block(block_2)
        print("\nWalletA's balance is: ", wallet_a.get_balance())
        print("WalletB's balance is: ", wallet_b.get_balance())

        block_3 = Block(block_2.block_hash)
        print("\nWalletB is Attempting to send funds (10) to WalletA")
        value = 10.0
        if wallet_b.send_funds(wallet_a.get_public_key(), value=value, receiver_port=wallet_a.id):
            block_3.add_transaction(Transaction(wallet_b.get_public_key(), wallet_a.get_public_key(), value=value))
            self.add_block(block_3)
        print("\nWalletA's balance is: ", wallet_a.get_balance())
        print("WalletB's balance is: ", wallet_b.get_balance())

        self.is_valid()



block_chain = BlockChain()
block_chain.main()
