"""Tab Key Generator untuk GUI."""

import queue
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from core.rsa_keygen import generate_keypair
from io_handler.key_parser import save_public_key, save_private_key


class KeygenTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttk.Label(self, text="[ RSA-OAEP 2048-BIT KEY GENERATOR ]", font=("Segoe UI", 14, "bold")).pack(pady=20)
        
        self.btn_generate = ttk.Button(self, text="[ INIT KEYGEN ]", command=self.start_keygen)
        self.btn_generate.pack(pady=10)
        
        self.progress = ttk.Progressbar(self, mode="indeterminate")
        
        self.info_var = tk.StringVar(value="Klik tombol di atas untuk generate key.\nIni memakan waktu sekitar 5-30 detik.")
        ttk.Label(self, textvariable=self.info_var, justify=tk.CENTER).pack(pady=10)
        
        self.keys = None
        
        self.btn_frame = ttk.Frame(self)
        self.btn_save_pub = ttk.Button(self.btn_frame, text="[ SAVE PUBLIC ]", command=self.save_pub)
        self.btn_save_priv = ttk.Button(self.btn_frame, text="[ SAVE PRIVATE ]", command=self.save_priv)
        
        self.queue = queue.Queue()
        self.check_queue()
        
    def check_queue(self):
        try:
            msg = self.queue.get_nowait()
            if msg[0] == "done":
                self._keygen_done(msg[1])
            elif msg[0] == "error":
                self._keygen_error(msg[1])
        except queue.Empty:
            pass
        self.after(100, self.check_queue)
        
    def start_keygen(self):
        self.btn_generate.config(state=tk.DISABLED)
        self.progress.pack(fill=tk.X, padx=50, pady=10)
        self.progress.start()
        self.info_var.set("Generating prime numbers... Mohon tunggu.")
        self.btn_frame.pack_forget()
        
        thread = threading.Thread(target=self._keygen_worker, daemon=True)
        thread.start()
        
    def _keygen_worker(self):
        start_time = time.time()
        try:
            self.keys = generate_keypair(2048)
            elapsed = time.time() - start_time
            self.queue.put(("done", elapsed))
        except Exception as e:
            self.queue.put(("error", str(e)))
            
    def _keygen_done(self, elapsed):
        self.progress.stop()
        self.progress.pack_forget()
        self.btn_generate.config(state=tk.NORMAL)
        
        (n, e), (n2, d) = self.keys
        n_hex = hex(n)[2:]
        self.info_var.set(f"Selesai dalam {elapsed:.2f} detik!\nn={n_hex[:15]}...{n_hex[-15:]}\ne={hex(e)}\nd=... (private key)")
        
        self.btn_frame.pack(pady=20)
        self.btn_save_pub.pack(side=tk.LEFT, padx=10)
        self.btn_save_priv.pack(side=tk.LEFT, padx=10)
        
    def _keygen_error(self, err):
        self.progress.stop()
        self.progress.pack_forget()
        self.btn_generate.config(state=tk.NORMAL)
        self.info_var.set(f"Error: {err}")
        messagebox.showerror("Error", f"Gagal generate key:\n{err}")

    def save_pub(self):
        if not self.keys: return
        path = filedialog.asksaveasfilename(defaultextension=".hex", filetypes=[("Hex Key Files", "*.hex")])
        if path:
            (n, e), _ = self.keys
            save_public_key(path, n, e)
            messagebox.showinfo("Sukses", f"Public key disimpan ke:\n{path}")
            
    def save_priv(self):
        if not self.keys: return
        path = filedialog.asksaveasfilename(defaultextension=".hex", filetypes=[("Hex Key Files", "*.hex")])
        if path:
            _, (n, d) = self.keys
            save_private_key(path, n, d)
            messagebox.showinfo("Sukses", f"Private key disimpan ke:\n{path}")
