class Transaction:
    transaction_id = 0
    sender_public_key = ''
    receiver_public_key = ''
    value = 0.0
    signature = ''
    transactions_in = []
    transactions_out = []

    def __init__(self, sender_public_key, receiver_public_key, value):
        self.sender_public_key = sender_public_key
        self.receiver_public_key = receiver_public_key
        self.value = value

    def generate_signature(self, private_key):
        data = str(self.sender_public_key) + str(self.receiver_public_key) + str(self.value)
        self.signature = private_key.sign(data.encode('utf-8'))
        return self.signature

    def verify_signature(self, public_key, signature):
        data = str(self.sender_public_key) + str(self.receiver_public_key) + str(self.value)
        return public_key.verify(signature, data.encode('utf-8'))
