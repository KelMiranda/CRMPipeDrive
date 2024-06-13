from cryptography.fernet import Fernet

class PasswordManager:
    def __init__(self, key=None):
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.cipher_suite = Fernet(self.key)

    def encrypt_password(self, password):
        encrypted_password = self.cipher_suite.encrypt(password.encode())
        return encrypted_password

    def decrypt_password(self, encrypted_password):
        decrypted_password = self.cipher_suite.decrypt(encrypted_password).decode()
        return decrypted_password
