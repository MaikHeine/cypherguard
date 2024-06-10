import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit
from cryptography.fernet import Fernet

class EncryptDecryptApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Encrypt & Decrypt Tool')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.key_input = QLineEdit(self)
        self.key_input.setPlaceholderText('Enter key or leave empty to generate a new key')
        layout.addWidget(self.key_input)

        self.generate_key_btn = QPushButton('Generate Key', self)
        self.generate_key_btn.clicked.connect(self.generate_key)
        layout.addWidget(self.generate_key_btn)

        self.encrypt_btn = QPushButton('Encrypt File', self)
        self.encrypt_btn.clicked.connect(self.encrypt_file)
        layout.addWidget(self.encrypt_btn)

        self.decrypt_btn = QPushButton('Decrypt File', self)
        self.decrypt_btn.clicked.connect(self.decrypt_file)
        layout.addWidget(self.decrypt_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def generate_key(self):
        key = Fernet.generate_key()
        self.key_input.setText(key.decode())
        QMessageBox.information(self, 'Key Generated', 'A new key has been generated and set in the key field.')

    def get_key(self):
        key = self.key_input.text().encode()
        if not key:
            QMessageBox.warning(self, 'No Key', 'Please enter or generate a key.')
            return None
        return key

    def encrypt_file(self):
        key = self.get_key()
        if not key:
            return
        
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file to encrypt', '', 'Text Files (*.txt)')
        if not file_path:
            return
        
        with open(file_path, 'rb') as file:
            data = file.read()

        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)

        save_path, _ = QFileDialog.getSaveFileName(self, 'Save encrypted file', '', 'Text Files (*.txt)')
        if not save_path:
            return

        with open(save_path, 'wb') as file:
            file.write(encrypted_data)

        QMessageBox.information(self, 'File Encrypted', 'The file has been encrypted and saved.')

    def decrypt_file(self):
        key = self.get_key()
        if not key:
            return
        
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file to decrypt', '', 'Text Files (*.txt)')
        if not file_path:
            return

        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        fernet = Fernet(key)
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
        except Exception as e:
            QMessageBox.critical(self, 'Decryption Failed', 'Invalid key or corrupted file.')
            return

        save_path, _ = QFileDialog.getSaveFileName(self, 'Save decrypted file', '', 'Text Files (*.txt)')
        if not save_path:
            return

        with open(save_path, 'wb') as file:
            file.write(decrypted_data)

        QMessageBox.information(self, 'File Decrypted', 'The file has been decrypted and saved.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EncryptDecryptApp()
    ex.show()
    sys.exit(app.exec_())
