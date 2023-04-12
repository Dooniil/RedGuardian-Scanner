import os
import ssl


class SslManager:
    KEY_FILE = os.sep.join([os.getcwd(), 'certificate', 'private.key'])
    CERT_FILE = os.sep.join([os.getcwd(), 'certificate', 'selfsigned.crt'])

    def __init__(self):
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.ssl_context.load_cert_chain(SslManager.CERT_FILE, SslManager.KEY_FILE)
        # cipher = 'DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:ECDHE-ECDSA-AES128-GCM-SHA256'
        # self.ssl_context.set_ciphers(cipher)

    @property
    def context(self):
        return self.ssl_context


ssl_manager = SslManager()