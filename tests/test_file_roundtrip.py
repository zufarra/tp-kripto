"""E2E File Roundtrip Test untuk Integrasi."""

import os
import unittest
from core.rsa_keygen import generate_keypair
from core.rsa_oaep import encrypt_chunk, decrypt_chunk
from io_handler.chunker import split_encrypt, split_decrypt, join_chunks

class TestFileRoundtrip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate full 2048-bit keypair for E2E testing
        # Ini bisa memakan waktu 5-20 detik.
        print("Generating 2048-bit keypair for E2E test. Please wait...")
        cls.keys = generate_keypair(2048)
        
    def test_roundtrip_random_bytes(self):
        (n, e), (n2, d) = self.keys
        
        # Uji dengan 500 bytes (melewati batas 190 bytes per chunk, menghasilkan 3 chunk)
        original_data = os.urandom(500)
        
        # -- ENCRYPT --
        chunks = split_encrypt(original_data)
        ciphertext_chunks = []
        for chunk in chunks:
            c_chunk = encrypt_chunk(chunk, n, e)
            ciphertext_chunks.append(c_chunk)
            
        full_ciphertext = join_chunks(ciphertext_chunks)
        
        # Panjang ciphertext harus (ceil(500/190) * 256) = 3 * 256 = 768 bytes
        self.assertEqual(len(full_ciphertext), 768)
        
        # -- DECRYPT --
        chunks_dec = split_decrypt(full_ciphertext)
        plaintext_chunks = []
        for chunk in chunks_dec:
            p_chunk = decrypt_chunk(chunk, n, d)
            plaintext_chunks.append(p_chunk)
            
        recovered_data = join_chunks(plaintext_chunks)
        
        # Harus presisi bit-by-bit
        self.assertEqual(original_data, recovered_data)

if __name__ == '__main__':
    unittest.main()
