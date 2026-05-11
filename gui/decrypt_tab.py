"""Tab Dekripsi GUI."""

import queue
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

from core.rsa_oaep import decrypt_chunk
from io_handler.chunker import split_decrypt, join_chunks
from io_handler.file_handler import read_file, write_file
from io_handler.key_parser import load_private_key
from .widgets import FilePickerWidget, LogWidget, ProgressWidget


class DecryptTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttk.Label(self, text="[ DECRYPT FILE ]", font=("Segoe UI", 14, "bold")).pack(pady=10)
        
        self.fp_in = FilePickerWidget(self, "> Input Ciphertext:")
        self.fp_in.pack(fill=tk.X, padx=10, pady=5)
        
        self.fp_key = FilePickerWidget(self, "> Private Key (.hex):", filetypes=[("Hex Key Files", "*.hex"), ("All Files", "*.*")])
        self.fp_key.pack(fill=tk.X, padx=10, pady=5)
        
        self.btn_decrypt = ttk.Button(self, text="[ DECRYPT ]", command=self.start_decrypt)
        self.btn_decrypt.pack(pady=10)
        
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
                    self._decrypt_done(msg[1])
                elif msg_type == "error":
                    self._decrypt_error(msg[1])
        except queue.Empty:
            pass
        self.after(100, self.check_queue)
        
    def start_decrypt(self):
        fin = self.fp_in.get_path()
        fkey = self.fp_key.get_path()
        
        if not fin or not fkey:
            messagebox.showerror("Error", "Input ciphertext dan private key harus dipilih!")
            return
            
        import os
        from tkinter import filedialog
        base_name = os.path.basename(fin)
        if base_name.endswith(".enc"):
            suggested_fout = base_name[:-4]
        else:
            name, ext = os.path.splitext(base_name)
            suggested_fout = f"{name}_decrypted{ext}"
            
        fout = filedialog.asksaveasfilename(
            title="Save Plaintext As",
            initialfile=suggested_fout,
            filetypes=[("All Files", "*.*")]
        )
        
        if not fout:
            return
            
        self.btn_decrypt.config(state=tk.DISABLED)
        self.log_widget.clear()
        self.progress.set_progress(0)
        
        thread = threading.Thread(target=self._decrypt_worker, args=(fin, fkey, fout), daemon=True)
        thread.start()
        
    def _decrypt_worker(self, fin, fkey, fout):
        start_time = time.time()
        try:
            self.queue.put(("log", f"[INFO] Membaca private key dari: {fkey}"))
            n, d = load_private_key(fkey)
            
            self.queue.put(("log", f"[INFO] Membaca ciphertext dari: {fin}"))
            ciphertext = read_file(fin)
            self.queue.put(("log", f"[INFO] Ukuran ciphertext: {len(ciphertext)} bytes"))
            
            chunks = split_decrypt(ciphertext)
            total_chunks = len(chunks)
            self.queue.put(("log", f"[INFO] Terpecah menjadi {total_chunks} chunk(s)"))
            
            plaintext_chunks = []
            for i, chunk in enumerate(chunks):
                p_chunk = decrypt_chunk(chunk, n, d)
                plaintext_chunks.append(p_chunk)
                
                percent = ((i + 1) / total_chunks) * 100
                self.queue.put(("progress", percent))
                
                if i % max(1, total_chunks // 10) == 0 or i == total_chunks - 1:
                    self.queue.put(("log", f"[INFO] Decrypting chunk {i+1}/{total_chunks}..."))
            
            self.queue.put(("log", "[INFO] Menyambungkan dan menyimpan plaintext..."))
            plaintext_full = join_chunks(plaintext_chunks)
            write_file(fout, plaintext_full)
            self.queue.put(("log", f"[INFO] Ukuran plaintext: {len(plaintext_full)} bytes"))
            
            elapsed = time.time() - start_time
            self.queue.put(("done", elapsed))
            
        except Exception as err:
            self.queue.put(("error", str(err)))

    def _decrypt_done(self, elapsed):
        self.btn_decrypt.config(state=tk.NORMAL)
        self.log_widget.log(f"[SUCCESS] Proses dekripsi selesai dalam {elapsed:.2f} detik!")
        messagebox.showinfo("Sukses", f"Dekripsi selesai!\nWaktu: {elapsed:.2f} detik.")
        
    def _decrypt_error(self, err):
        self.btn_decrypt.config(state=tk.NORMAL)
        self.log_widget.log(f"[ERROR] {err}")
        messagebox.showerror("Error", f"Gagal dekripsi:\n{err}")
