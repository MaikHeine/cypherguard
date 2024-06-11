# CypherGuard

CypherGuard is a file encryption and decryption tool with a modern UI built using Python and PySide6 (WIP). It allows users to securely encrypt and decrypt text files using `Fernet`, a encryption algorithm found in the `cryptography` library.

## Features

- Generate `Fernet` encryption keys
- Encrypt files
- Decrypt files
- Modern UI built with PySide6 (WIP)

## Prerequisites

- Python 3.6 or higher

## Installation

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/MaikHeine/cypherguard.git
cd cypherguard
```

### 2. Set Up a Virtual Environment

It's a good practice to use a virtual environment to manage dependencies. Follow these steps to create and activate a virtual environment:

#### On Windows

```bash
python -m venv cypherguardvenv
cypherguardvenv\Scripts\activate
```

#### On macOS and Linux

```bash
python3 -m venv cypherguardvenv
source cypherguardvenv/bin/activate
```

### 3. Install Requirements

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Program

Make sure you are in the project directory and the virtual environment is activated.
To start the CypherGuard application, run the following command:

```bash
python main.py
```

## Usage

1. **Generate Key:** Click on "Generate Key" to create a new `Fernet` encryption key.
2. **Encrypt File:** Click on "Encrypt File" to select a file you wish to encrypt.
3. **Decrypt File:** Click on "Decrypt File" to select an encrypted file you wish to decrypt.


