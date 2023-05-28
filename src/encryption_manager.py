import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

class EncryptionManager:
    def __init__(self):
        self.private_key = None

    def decrypt(self, data: bytes):
        private_key = serialization.load_pem_private_key(self.private_key.encode(), password=None)

        decrypted_data: bytes = private_key.decrypt(
            base64.b64decode(data),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data.decode()


encryption_manager = EncryptionManager()