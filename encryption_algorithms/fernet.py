from cryptography.fernet import Fernet

class FernetEncryption:
    def __init__(self, key=None):
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key.encode()
        self.cipher = Fernet(self.key)

    def encrypt(self, data):
        return self.cipher.encrypt(data)

    def decrypt(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data)

    def get_key(self):
        return self.key.decode()
