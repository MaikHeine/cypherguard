import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox, QComboBox
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
import ctypes

# Import your encryption classes
from encryption_algorithms.fernet import FernetEncryption
from encryption_algorithms.aes import AESEncryption
from encryption_algorithms.rsa import RSAEncryption
from encryption_algorithms.sha256 import SHA256Hashing

# Setting App ID for Windows Taskbar
myappid = 'cypherguard.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set the window title and icon
        self.setWindowTitle("CypherGuard")
        self.setWindowIcon(QIcon("icon.ico"))

        # Set initial window size
        #self.resize(800, 600)  # Width: 800, Height: 600

        # Create widgets
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap("icon.ico").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.text_label = QLabel("CypherGuard")
        self.text_label.setAlignment(Qt.AlignCenter)

        self.description_label = QLabel("Securely encrypt and decrypt your files with ease and the Fernet algorithm.")
        self.description_label.setAlignment(Qt.AlignCenter)

        self.key_line_edit = QLineEdit()
        self.key_line_edit.setPlaceholderText("Enter key or leave empty to generate a new key...")

        self.key_text_edit = QTextEdit()
        self.key_text_edit.setPlaceholderText("Enter key or leave empty to generate a new key...")
        self.key_text_edit.setVisible(False)  # Hide by default

        self.encryption_algorithm_combobox = QComboBox()
        self.encryption_algorithm_combobox.addItem("Fernet")
        self.encryption_algorithm_combobox.addItem("AES")
        self.encryption_algorithm_combobox.addItem("RSA")

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
        self.encryption_algorithm_combobox.currentTextChanged.connect(self.switch_key_input)

        # Create layouts
        icon_text_layout = QHBoxLayout()
        icon_text_layout.addWidget(self.icon_label)
        icon_text_layout.addWidget(self.text_label)
        icon_text_layout.setAlignment(Qt.AlignCenter)

        key_layout = QHBoxLayout()
        key_layout.addWidget(self.encryption_algorithm_combobox)
        key_layout.addWidget(self.key_line_edit)
        key_layout.addWidget(self.key_text_edit)
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

        # Change cursor to pointer
        self.generate_key_button.setCursor(Qt.PointingHandCursor)
        self.encrypt_file_button.setCursor(Qt.PointingHandCursor)
        self.decrypt_file_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setCursor(Qt.PointingHandCursor)

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
            QComboBox {
                background-color: #000000;
                color: #FFFFFF;
                border: 2px solid #444444;
                border-radius: 10px;
                padding: 10px;
                margin: 10px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            }
            QLineEdit, QTextEdit {
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
                border: 2px solid #ffffff;
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

    def switch_key_input(self):
        if self.encryption_algorithm_combobox.currentText() == "RSA":
            self.key_line_edit.setVisible(False)
            self.key_text_edit.setVisible(True)
        else:
            self.key_line_edit.setVisible(True)
            self.key_text_edit.setVisible(False)

    def generate_key(self):
        algorithm = self.encryption_algorithm_combobox.currentText()
        if algorithm == "Fernet":
            encryption = FernetEncryption()
        elif algorithm == "AES":
            encryption = AESEncryption()
        elif algorithm == "RSA":
            encryption = RSAEncryption()
        else:
            encryption = None
        
        if encryption:
            if algorithm == "RSA":
                self.key_text_edit.setPlainText(encryption.get_key())
            else:
                self.key_line_edit.setText(encryption.get_key())

    def clear_key_line_edit(self):
        self.key_line_edit.clear()
        self.key_text_edit.clear()

    def get_key(self):
        algorithm = self.encryption_algorithm_combobox.currentText()
        if algorithm == "RSA":
            key = self.key_text_edit.toPlainText()
        else:
            key = self.key_line_edit.text()

        if not key:
            QMessageBox.warning(self, 'No Key', 'Please enter or generate a key.')
            return None
        
        if algorithm in ["AES", "RSA"]:
            key = key.encode()  # Encoding only for AES and RSA
        return key

    def encrypt_file(self):
        algorithm = self.encryption_algorithm_combobox.currentText()
        key = self.get_key()
        encryption = None
        if key:
            try:
                if algorithm == "Fernet":
                    encryption = FernetEncryption(key)
                elif algorithm == "AES":
                    encryption = AESEncryption(key)
                elif algorithm == "RSA":
                    encryption = RSAEncryption(key)
                else:
                    encryption = None

                if encryption:
                    file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Encrypt", "", "All Files (*)")
                    if file_path:
                        with open(file_path, 'rb') as file:
                            data = file.read()

                        encrypted_data = encryption.encrypt(data)

                        encrypted_file_path = file_path + '.encrypted'
                        with open(encrypted_file_path, 'wb') as encrypted_file:
                            encrypted_file.write(encrypted_data)

                        QMessageBox.information(self, "Success", "File encrypted successfully.")

            except ValueError as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


    def decrypt_file(self):
        algorithm = self.encryption_algorithm_combobox.currentText()
        key = self.get_key()
        encryption = None
        if key:
            try:
                if algorithm == "Fernet":
                    encryption = FernetEncryption(key)
                elif algorithm == "AES":
                    encryption = AESEncryption(key)
                elif algorithm == "RSA":
                    encryption = RSAEncryption(key)
                else:
                    encryption = None

                if encryption:
                    file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Decrypt", "", "All Files (*)")
                    if file_path:
                        with open(file_path, 'rb') as file:
                            encrypted_data = file.read()

                        decrypted_data = encryption.decrypt(encrypted_data)

                        decrypted_file_path = file_path.replace('.encrypted', '')
                        with open(decrypted_file_path, 'wb') as decrypted_file:
                            decrypted_file.write(decrypted_data)

                        QMessageBox.information(self, "Success", "File decrypted successfully.")

            except ValueError as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
