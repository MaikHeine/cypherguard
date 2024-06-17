# In your RSAEncryption class (encryption_algorithms/rsa.py)
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

class RSAEncryption:
    def __init__(self, key=None):
        if key:
            if isinstance(key, bytes):
                self.key = RSA.import_key(key)
            elif isinstance(key, str):  # Assuming key might also be a string in some cases
                self.key = RSA.import_key(key.encode())
            else:
                raise ValueError("Unsupported key type")
        else:
            # Generate a new RSA key pair if no key is provided
            self.key = RSA.generate(2048)

    def get_key(self):
        return self.key.export_key().decode()

    def encrypt(self, data):
        cipher = PKCS1_OAEP.new(self.key)
        encrypted_data = cipher.encrypt(data)
        return encrypted_data

    def decrypt(self, encrypted_data):
        cipher = PKCS1_OAEP.new(self.key)
        decrypted_data = cipher.decrypt(encrypted_data)
        return decrypted_data
