from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

class AESEncryption:
    def __init__(self, key=None):
        if key is None:
            self.key = get_random_bytes(16)  # 128-bit key
        else:
            self.key = base64.b64decode(key)
        self.cipher = AES.new(self.key, AES.MODE_EAX)

    def encrypt(self, data):
        self.cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = self.cipher.nonce
        encrypted_data, tag = self.cipher.encrypt_and_digest(data)
        return nonce + encrypted_data  # Nonce is required for decryption

    def decrypt(self, encrypted_data):
        nonce = encrypted_data[:16]
        self.cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        return self.cipher.decrypt(encrypted_data[16:])

    def get_key(self):
        return base64.b64encode(self.key).decode()
