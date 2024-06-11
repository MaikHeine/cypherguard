from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, QWidget, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt

from cryptography.fernet import Fernet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CypherGuard")

         # Set the initial size of the window
        self.resize(500, 400)

        # Create widgets
        self.label = QLabel("Welcome to CypherGuard")
        self.key_line_edit = QLineEdit()
        self.key_line_edit.setPlaceholderText("Enter key or leave empty to generate a new key...")
        self.generate_key_button = QPushButton("Generate Key")
        self.encrypt_file_button = QPushButton("Encrypt File")
        self.decrypt_file_button = QPushButton("Decrypt File")

        # Connect signals to slots
        self.generate_key_button.clicked.connect(self.generate_key)
        self.encrypt_file_button.clicked.connect(self.encrypt_file)
        self.decrypt_file_button.clicked.connect(self.decrypt_file)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.key_line_edit)
        layout.addWidget(self.generate_key_button)
        layout.addWidget(self.encrypt_file_button)
        layout.addWidget(self.decrypt_file_button)

        # Create a container widget and set the layout
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the main window
        self.setCentralWidget(container)

    def generate_key(self):
        # Generate a key using Fernet
        key = Fernet.generate_key()

        # Set the generated key in the QLineEdit
        self.key_line_edit.setText(key.decode())

    def get_key(self):
        key = self.key_line_edit.text().encode()
        if not key:
            QMessageBox.warning(self, 'No Key', 'Please enter or generate a key.')
            return None
        return key

    def encrypt_file(self):
        key = self.get_key()

        if not key:
            QMessageBox.warning(self, "Warning", "Please generate or enter a key.")
            return

        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Encrypt", "", "All Files (*)")
            if file_path:
                with open(file_path, 'rb') as file:
                    data = file.read()

                fernet = Fernet(key)
                encrypted_data = fernet.encrypt(data)

                encrypted_file_path = file_path + '.encrypted'
                with open(encrypted_file_path, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_data)

                QMessageBox.information(self, "Success", "File encrypted successfully.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def decrypt_file(self):
        key = self.get_key()

        if not key:
            QMessageBox.warning(self, "Warning", "Please generate or enter a key.")
            return

        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Decrypt", "", "Encrypted Files (*.encrypted)")
            if file_path:
                with open(file_path, 'rb') as file:
                    encrypted_data = file.read()

                fernet = Fernet(key)
                decrypted_data = fernet.decrypt(encrypted_data)

                # Remove the '.encrypted' extension from the file name
                decrypted_file_path = file_path[:-10]  # assuming '.encrypted' is 10 characters long
                with open(decrypted_file_path, 'wb') as decrypted_file:
                    decrypted_file.write(decrypted_data)

                QMessageBox.information(self, "Success", "File decrypted successfully.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
