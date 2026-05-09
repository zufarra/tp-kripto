"""
RSA-OAEP-256 Encryption/Decryption — Main Entry Point
Menjalankan GUI aplikasi.
"""

import sys
import os

# Tambahkan root directory ke path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.app import RSAOAEPApp


def main():
    """Launch the RSA-OAEP-256 GUI application."""
    app = RSAOAEPApp()
    app.mainloop()


if __name__ == "__main__":
    main()
