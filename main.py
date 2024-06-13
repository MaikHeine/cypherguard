from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
from cryptography.fernet import Fernet
import ctypes

# Setting App ID for Windows Taskbar
myappid = 'cypherguard.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set the window title and icon
        self.setWindowTitle("CypherGuard")
        self.setWindowIcon(QIcon("icon.ico"))

        # Create widgets
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap("icon.ico").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.text_label = QLabel("CypherGuard")
        self.text_label.setAlignment(Qt.AlignCenter)

        self.description_label = QLabel("Securely encrypt and decrypt your files with ease and the Fernet algorithm.")
        self.description_label.setAlignment(Qt.AlignCenter)

        self.key_line_edit = QLineEdit()
        self.key_line_edit.setPlaceholderText("Enter key or leave empty to generate a new key...")

        self.generate_key_button = QPushButton("Generate Key")
        self.encrypt_file_button = QPushButton("Encrypt File")
        self.decrypt_file_button = QPushButton("Decrypt File")
        self.clear_button = QPushButton()
        self.clear_button.setText("X")

        # Connect signals to slots
        self.generate_key_button.clicked.connect(self.generate_key)
        self.encrypt_file_button.clicked.connect(self.encrypt_file)
        self.decrypt_file_button.clicked.connect(self.decrypt_file)
        self.clear_button.clicked.connect(self.clear_key_line_edit)

        # Create layouts
        icon_text_layout = QHBoxLayout()
        icon_text_layout.addWidget(self.icon_label)
        icon_text_layout.addWidget(self.text_label)
        icon_text_layout.setAlignment(Qt.AlignCenter)

        key_layout = QHBoxLayout()
        key_layout.addWidget(self.key_line_edit)
        key_layout.addWidget(self.clear_button)

        layout = QVBoxLayout()
        layout.addLayout(icon_text_layout)
        layout.addWidget(self.description_label)
        layout.addLayout(key_layout)
        layout.addWidget(self.generate_key_button)
        layout.addWidget(self.encrypt_file_button)
        layout.addWidget(self.decrypt_file_button)

        # Create container widget and set the layout
        container = QWidget()
        container.setLayout(layout)

        # Set central widget of the main window
        self.setCentralWidget(container)

        # Apply CSS styling
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 28px;
                font-weight: bold;
                margin: 20px, 20px 0px 20px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel[description=true] {
                font-size: 16px;
                font-weight: normal;
                margin: 5px 20px 20px 20px;
                line-height: 20px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLineEdit {
                background-color: #000000;
                color: #FFFFFF;
                border: 2px solid #444444;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                margin: 10px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QPushButton {
                text-align: center;
                background-color: #000000;
                color: #FFFFFF;
                border: 2px solid #007ACC;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                margin: 10px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QPushButton:hover {
                background-color: #1a1a1a;
            }
            QPushButton:pressed {
                background-color: #1f1f1f;
            }
            QPushButton:disabled {
                background-color: #333333;
                color: #777777;
            }
            QMessageBox {
                background-color: #1E1E1E;
                color: #FFFFFF;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
        """)
        self.description_label.setProperty('description', True)

    def generate_key(self):
        # Generate a key using Fernet
        key = Fernet.generate_key()

        # Set the generated key in the QLineEdit
        self.key_line_edit.setText(key.decode())

    def clear_key_line_edit(self):
        # Clear the content of the key QLineEdit
        self.key_line_edit.clear()

    def get_key(self):
        key = self.key_line_edit.text().encode()
        if not key:
            QMessageBox.warning(self, 'No Key', 'Please enter or generate a key.')
            return None
        return key

    def encrypt_file(self):
        key = self.get_key()
        if key:
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

        if key:
            try:
                file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Decrypt", "", "All Files (*)")
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
