import queue
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

from core.rsa_oaep import encrypt_chunk
from io_handler.chunker import MAX_PLAINTEXT_BYTES
from io_handler.file_handler import read_file, write_file
from io_handler.key_parser import load_public_key
from .widgets import FilePickerWidget, LogWidget, ProgressWidget


class EncryptTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttk.Label(self, text="[ ENCRYPT FILE ]", font=("Segoe UI", 14, "bold")).pack(pady=10)
        
        self.fp_in = FilePickerWidget(self, "> Input Plaintext:")
        self.fp_in.pack(fill=tk.X, padx=10, pady=5)
        
        self.fp_key = FilePickerWidget(self, "> Public Key (.hex):", filetypes=[("Hex Key Files", "*.hex"), ("All Files", "*.*")])
        self.fp_key.pack(fill=tk.X, padx=10, pady=5)
        
        self.btn_encrypt = ttk.Button(self, text="[ ENCRYPT ]", command=self.start_encrypt)
        self.btn_encrypt.pack(pady=10)
        
        self.progress = ProgressWidget(self)
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
        self.log_widget = LogWidget(self)
        self.log_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.queue = queue.Queue()
        self.check_queue()
        
    def check_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                msg_type = msg[0]
                if msg_type == "log":
                    self.log_widget.log(msg[1])
                elif msg_type == "progress":
                    self.progress.set_progress(msg[1])
                elif msg_type == "done":
                    self._encrypt_done(msg[1])
                elif msg_type == "error":
                    self._encrypt_error(msg[1])
        except queue.Empty:
            pass
        self.after(100, self.check_queue)
        
    def start_encrypt(self):
        fin = self.fp_in.get_path()
        fkey = self.fp_key.get_path()
        
        if not fin or not fkey:
            messagebox.showerror("Error", "Input plaintext dan public key harus dipilih!")
            return
            
        import os
        from tkinter import filedialog
        base_name = os.path.basename(fin)
        suggested_fout = f"{base_name}.enc"
        
        fout = filedialog.asksaveasfilename(
            title="Save Ciphertext As",
            initialfile=suggested_fout,
            filetypes=[("Encrypted Files", "*.enc"), ("All Files", "*.*")]
        )
        
        if not fout:
            return
            
        self.btn_encrypt.config(state=tk.DISABLED)
        self.log_widget.clear()
        self.progress.set_progress(0)
        
        thread = threading.Thread(target=self._encrypt_worker, args=(fin, fkey, fout), daemon=True)
        thread.start()
        
    def _encrypt_worker(self, fin, fkey, fout):
        start_time = time.time()
        try:
            self.queue.put(("log", f"[INFO] Membaca public key dari: {fkey}"))
            n, e = load_public_key(fkey)
            
            self.queue.put(("log", f"[INFO] Membaca input file: {fin}"))
            plaintext = read_file(fin)
            self.queue.put(("log", f"[INFO] Ukuran plaintext: {len(plaintext)} bytes"))
            if len(plaintext) > MAX_PLAINTEXT_BYTES:
                raise ValueError(
                    f"Ukuran plaintext maksimal {MAX_PLAINTEXT_BYTES} bytes. "
                    "RSA-OAEP 2048-bit tidak mendukung chunking otomatis."
                )

            self.queue.put(("log", "[INFO] Mengenkripsi 1 blok plaintext..."))
            ciphertext_full = encrypt_chunk(plaintext, n, e)

            self.queue.put(("log", "[INFO] Menyimpan ciphertext..."))
            write_file(fout, ciphertext_full)
            self.queue.put(("progress", 100))
            self.queue.put(("log", f"[INFO] Ukuran ciphertext: {len(ciphertext_full)} bytes"))
            
            elapsed = time.time() - start_time
            self.queue.put(("done", elapsed))
            
        except Exception as err:
            self.queue.put(("error", str(err)))

    def _encrypt_done(self, elapsed):
        self.btn_encrypt.config(state=tk.NORMAL)
        self.log_widget.log(f"[SUCCESS] Proses enkripsi selesai dalam {elapsed:.2f} detik!")
        messagebox.showinfo("Sukses", f"Enkripsi selesai!\nWaktu: {elapsed:.2f} detik.")
        
    def _encrypt_error(self, err):
        self.btn_encrypt.config(state=tk.NORMAL)
        self.log_widget.log(f"[ERROR] {err}")
        messagebox.showerror("Error", f"Gagal enkripsi:\n{err}")
