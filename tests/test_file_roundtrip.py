import os
import unittest
from core.oaep import OAEPError
from core.rsa_keygen import generate_keypair
from core.rsa_oaep import encrypt_chunk, decrypt_chunk

class TestFileRoundtrip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Generating 2048-bit keypair for E2E test. Please wait...")
        cls.keys = generate_keypair(2048)
        
    def test_roundtrip_random_bytes(self):
        (n, e), (n2, d) = self.keys
        original_data = os.urandom(190)
        full_ciphertext = encrypt_chunk(original_data, n, e)
        self.assertEqual(len(full_ciphertext), 256)
        recovered_data = decrypt_chunk(full_ciphertext, n, d)
        self.assertEqual(original_data, recovered_data)

    def test_plaintext_over_190_bytes_is_rejected(self):
        (n, e), _ = self.keys
        with self.assertRaises(OAEPError):
            encrypt_chunk(os.urandom(191), n, e)

if __name__ == '__main__':
    unittest.main()
