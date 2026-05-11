from __future__ import annotations
import unittest
from core.bigint_math import I2OSP, OS2IP, gcd, modexp, modinv
from core.mgf1 import mgf1
from core.miller_rabin import is_prime
from core.oaep import OAEPError, oaep_decode, oaep_encode
from core.prime_gen import generate_prime
from core.rsa_keygen import generate_keypair
from core.rsa_oaep import decrypt_chunk, encrypt_chunk
from core.sha256 import sha256


class TestBigIntMath(unittest.TestCase):
    def test_modexp_matches_builtin_pow(self) -> None:
        cases = [
            (2, 0, 5),
            (2, 10, 17),
            (123456789, 12345, 97),
            (-7, 13, 19),
        ]
        for base, exponent, modulus in cases:
            with self.subTest(case=(base, exponent, modulus)):
                self.assertEqual(modexp(base, exponent, modulus), pow(base, exponent, modulus))

    def test_gcd_and_modinv(self) -> None:
        self.assertEqual(gcd(54, 24), 6)
        self.assertEqual(modinv(17, 3120), 2753)
        self.assertEqual((17 * modinv(17, 3120)) % 3120, 1)

    def test_i2osp_and_os2ip_roundtrip(self) -> None:
        value = 0xDEADBEEF
        encoded = I2OSP(value, 8)
        self.assertEqual(encoded, b"\x00\x00\x00\x00\xDE\xAD\xBE\xEF")
        self.assertEqual(OS2IP(encoded), value)


class TestSHA256(unittest.TestCase):
    def test_nist_vectors(self) -> None:
        vectors = {
            b"": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            b"abc": "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
            b"message digest": "f7846f55cf23e14eebeab5b4e1550cad5b509e3348fbc4efa3a1413d393cb650",
            b"The quick brown fox jumps over the lazy dog": "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592",
        }
        for message, expected in vectors.items():
            with self.subTest(message=message):
                self.assertEqual(sha256(message).hex(), expected)


class TestMGF1(unittest.TestCase):
    def test_output_length_and_determinism(self) -> None:
        seed = b"seed"
        self.assertEqual(mgf1(seed, 0), b"")
        self.assertEqual(len(mgf1(seed, 1)), 1)
        self.assertEqual(len(mgf1(seed, 64)), 64)
        self.assertEqual(mgf1(seed, 64), mgf1(seed, 64))

    def test_counter_expansion(self) -> None:
        seed = b"abc"
        expected = sha256(seed + b"\x00\x00\x00\x00") + sha256(seed + b"\x00\x00\x00\x01")
        self.assertEqual(mgf1(seed, 64), expected)


class TestMillerRabinAndPrimes(unittest.TestCase):
    def test_known_primes_and_composites(self) -> None:
        primes = [2, 3, 5, 17, 101, 65537]
        composites = [0, 1, 4, 9, 21, 221, 65535]
        for value in primes:
            with self.subTest(prime=value):
                self.assertTrue(is_prime(value))
        for value in composites:
            with self.subTest(composite=value):
                self.assertFalse(is_prime(value))

    def test_generate_prime_bit_length(self) -> None:
        prime = generate_prime(64)
        self.assertTrue(is_prime(prime))
        self.assertEqual(prime.bit_length(), 64)
        self.assertEqual(prime & 1, 1)


class TestOAEPAndRSA(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.public_key, cls.private_key = generate_keypair(640)

    def test_oaep_roundtrip(self) -> None:
        k = 128
        message = b"oaep"
        em = oaep_encode(message, k)
        self.assertEqual(len(em), k)
        self.assertEqual(oaep_decode(em, k), message)

    def test_oaep_invalid_padding(self) -> None:
        k = 128
        em = bytearray(oaep_encode(b"hello", k))
        em[10] ^= 0x01
        with self.assertRaises(OAEPError):
            oaep_decode(bytes(em), k)

    def test_rsa_oaep_roundtrip(self) -> None:
        (n, e) = self.public_key
        (n2, d) = self.private_key
        self.assertEqual(n, n2)
        max_len = (n.bit_length() + 7) // 8 - 2 * 32 - 2
        message = b"hello rsa oaep"
        self.assertLessEqual(len(message), max_len)
        ciphertext = encrypt_chunk(message, n, e)
        plaintext = decrypt_chunk(ciphertext, n, d)
        self.assertEqual(plaintext, message)

    def test_rsa_oaep_empty_message(self) -> None:
        (n, e) = self.public_key
        (n2, d) = self.private_key
        self.assertEqual(n, n2)
        ciphertext = encrypt_chunk(b"", n, e)
        self.assertEqual(decrypt_chunk(ciphertext, n, d), b"")


if __name__ == "__main__":
    unittest.main()
