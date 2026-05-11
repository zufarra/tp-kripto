import tkinter as tk
from tkinter import ttk, filedialog


class FilePickerWidget(ttk.Frame):
    def __init__(self, parent, label_text, filetypes=None):
        super().__init__(parent)
        self.filetypes = filetypes if filetypes else [("All Files", "*.*")]
        
        ttk.Label(self, text=label_text, width=20).pack(side=tk.LEFT, padx=5)
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.entry_var, width=50)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.btn = ttk.Button(self, text="Browse...", command=self.browse)
        self.btn.pack(side=tk.LEFT, padx=5)

    def browse(self):
        path = filedialog.askopenfilename(filetypes=self.filetypes)
        if path:
            self.entry_var.set(path)
            
    def set_path(self, path):
        self.entry_var.set(path)

    def get_path(self):
        return self.entry_var.get()


class LogWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.text = tk.Text(self, height=10, state=tk.DISABLED, wrap=tk.WORD,
                            bg="#ffffff", fg="#000000", font=("Segoe UI", 10),
                            insertbackground="#000000", borderwidth=1, relief=tk.SOLID)
        self.scroll = ttk.Scrollbar(self, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scroll.set)
        
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def log(self, message):
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)
        self.update_idletasks()
        
    def clear(self):
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.config(state=tk.DISABLED)
        self.update_idletasks()


class ProgressWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.var = tk.DoubleVar()
        self.bar = ttk.Progressbar(self, variable=self.var, maximum=100)
        self.label_var = tk.StringVar(value="0%")
        self.label = ttk.Label(self, textvariable=self.label_var, width=5)
        
        self.bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.label.pack(side=tk.LEFT, padx=5)
        
    def set_progress(self, percent):
        self.var.set(percent)
        self.label_var.set(f"{int(percent)}%")
        self.update_idletasks()
