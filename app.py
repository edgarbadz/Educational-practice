import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from table_engine import read_table, write_table

TABLE_FORMATS = {
    "CSV": ".csv", "TSV": ".tsv", "Excel": ".xlsx", "JSON": ".json", "HTML": ".html"
}

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DocConv — Конвертер таблиц")
        self.root.geometry("600x350")
        self.root.resizable(False, False)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True, fill="both")

        self.tab_table = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_table, text="Таблицы")

        self.setup_table_tab()

    def setup_table_tab(self):
        frame = ttk.LabelFrame(self.tab_table, text="Конвертация табличных данных", padding=15)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.table_src = tk.StringVar()
        ttk.Label(frame, text="Исходный файл:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(frame, textvariable=self.table_src, width=45, state="readonly").grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Обзор...", command=self.pick_table_src).grid(row=0, column=2)

        ttk.Label(frame, text="Сохранить как:").grid(row=1, column=0, sticky="w", pady=5)
        self.table_target_combo = ttk.Combobox(frame, values=list(TABLE_FORMATS.keys()), state="readonly", width=30)
        self.table_target_combo.grid(row=1, column=1, padx=5, sticky="w")
        self.table_target_combo.set("Excel")

        ttk.Button(frame, text="Конвертировать таблицу", command=self.run_table_convert).grid(row=2, column=0, columnspan=3, pady=20)

    def pick_table_src(self):
        path = filedialog.askopenfilename(title="Выберите таблицу", filetypes=[("Таблицы", "*.csv *.tsv *.xlsx *.xls *.json *.html")])
        if path: self.table_src.set(path)

    def run_table_convert(self):
        src = self.table_src.get()
        if not src:
            messagebox.showerror("Ошибка", "Выберите исходный файл!"); return
        
        target_name = self.table_target_combo.get()
        target_ext = TABLE_FORMATS[target_name]
        
        dst = filedialog.asksaveasfilename(title="Куда сохранить", defaultextension=target_ext, initialfile=Path(src).stem + target_ext)
        if not dst: return

        try:
            df = read_table(Path(src))
            write_table(df, Path(dst))
            messagebox.showinfo("Успех", f"Файл успешно конвертирован!\n{dst}")
        except Exception as e:
            messagebox.showerror("Ошибка конвертации", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()