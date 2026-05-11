"""Entry point aplikasi GUI."""

import tkinter as tk
from tkinter import ttk

from .keygen_tab import KeygenTab
from .encrypt_tab import EncryptTab
from .decrypt_tab import DecryptTab

class RSAOAEPApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("RSA-OAEP-256 Encryptor/Decryptor")
        self.geometry("750x550")
        self.resizable(False, False)
        
        self.configure(bg="#ffffff")
        style = ttk.Style(self)
        style.theme_use('clam')
        
        bg_color = "#ffffff"
        fg_color = "#000000"
        accent_color = "#f0f0f0"
        entry_bg = "#ffffff"
        
        style.configure(".", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        
        style.configure("TButton", background=accent_color, foreground=fg_color, 
                        borderwidth=1, bordercolor="#000000", focuscolor=fg_color,
                        font=("Segoe UI", 10))
        style.map("TButton", background=[("active", "#e0e0e0")])
        
        style.configure("TEntry", fieldbackground=entry_bg, foreground=fg_color, 
                        borderwidth=1, bordercolor="#000000")
        
        style.configure("TNotebook", background=bg_color, tabmargins=[5, 5, 2, 0])
        style.configure("TNotebook.Tab", background=accent_color, foreground=fg_color, 
                        padding=[15, 5], font=("Segoe UI", 10))
        style.map("TNotebook.Tab", background=[("selected", "#ffffff")], expand=[("selected", [1, 1, 1, 0])])
        
        style.configure("Horizontal.TProgressbar", background="#000000", bordercolor="#000000", thickness=15)
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Tabs
        self.tab_keygen = KeygenTab(self.notebook)
        self.tab_encrypt = EncryptTab(self.notebook)
        self.tab_decrypt = DecryptTab(self.notebook)
        
        self.notebook.add(self.tab_keygen, text="Key Generator")
        self.notebook.add(self.tab_encrypt, text="Encrypt")
        self.notebook.add(self.tab_decrypt, text="Decrypt")
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready.")
        self.status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
