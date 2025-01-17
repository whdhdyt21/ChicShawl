import tkinter as tk
from tkinter import messagebox, ttk
from utils.file_utils import read_excel, write_excel, append_excel

DATA_FILE = "data/persediaan.xlsx"

class PersediaanView:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x600")
        self.master.configure(bg="#FFF9BF")
        self.master.minsize(400, 500)
        self.frame = tk.Frame(self.master, bg="#FFF9BF")
        self.frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        # Label judul untuk halaman
        tk.Label(self.frame, text="PERSEDIAAN", font=("Arial", 30, "bold"), fg="#CB9DF0", bg="#FFF9BF").pack(pady=10)

        # Frame untuk tabel
        table_frame = tk.Frame(self.frame, bg="#FFF9BF")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Membuat tabel untuk menampilkan data persediaan
        self.table = ttk.Treeview(table_frame, columns=("Tanggal", "Nama Produk", "Banyak Produk"), show="headings")
        self.table.heading("Tanggal", text="Tanggal")
        self.table.heading("Nama Produk", text="Nama Produk")
        self.table.heading("Banyak Produk", text="Banyak Produk")
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertikal untuk tabel
        scrollbar_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.config(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Scrollbar horizontal untuk tabel
        scrollbar_x = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.table.xview)
        self.table.config(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(fill=tk.X)

        self.load_data()

        # Frame untuk input data
        entry_frame = tk.Frame(self.frame, bg="#FFF9BF")
        entry_frame.pack(fill=tk.X, pady=10)

        # Entry untuk tanggal
        self.entry_tanggal = tk.Entry(entry_frame, width=15)
        self.entry_tanggal.grid(row=0, column=0, padx=5)
        self.entry_tanggal.insert(0, "Tanggal")

        # Entry untuk nama produk
        self.entry_nama = tk.Entry(entry_frame, width=20)
        self.entry_nama.grid(row=0, column=1, padx=5)
        self.entry_nama.insert(0, "Nama Produk")

        # Entry untuk banyak produk
        self.entry_banyak = tk.Entry(entry_frame, width=10)
        self.entry_banyak.grid(row=0, column=2, padx=5)
        self.entry_banyak.insert(0, "Banyak")

        # Frame untuk tombol aksi
        button_frame = tk.Frame(self.frame, bg="#FFF9BF")
        button_frame.pack(fill=tk.X, pady=10)

        # Tombol untuk menambah data
        tk.Button(button_frame, text="Tambah", command=self.add_data, font=("Arial", 16, "bold"), fg="#CB9DF0", bg="#CB9DF0").grid(row=0, column=0, padx=5)

        # Tombol untuk menghapus data
        tk.Button(button_frame, text="Hapus", command=self.delete_data, font=("Arial", 16, "bold"), fg="#CB9DF0", bg="#CB9DF0").grid(row=0, column=1, padx=5)

        # Tombol untuk kembali ke dashboard
        tk.Button(button_frame, text="Kembali", command=self.back_to_dashboard, font=("Arial", 16, "bold"), fg="#CB9DF0", bg="#CB9DF0").grid(row=0, column=2, padx=5)

    def load_data(self):
        """Memuat data dari file dan menampilkan pada tabel"""
        self.table.delete(*self.table.get_children())
        data = read_excel(DATA_FILE)
        for row in data:
            self.table.insert("", "end", values=(row["Tanggal"], row["Nama Produk"], row["Banyak Produk"]))

    def add_data(self):
        """Menambahkan data ke dalam file Excel"""
        tanggal = self.entry_tanggal.get()
        nama = self.entry_nama.get()
        banyak = self.entry_banyak.get()

        # Validasi input sebelum menyimpan data
        if not (tanggal and nama and banyak.isdigit()):
            messagebox.showwarning("Kesalahan Input", "Harap isi semua kolom dengan benar.")  # Pesan peringatan jika input tidak valid
            return

        append_excel(DATA_FILE, {"Tanggal": tanggal, "Nama Produk": nama, "Banyak Produk": banyak},
                     ["Tanggal", "Nama Produk", "Banyak Produk"])
        self.load_data()
        messagebox.showinfo("Berhasil", "Data berhasil ditambahkan!")  # Pesan info setelah data berhasil disimpan

    def delete_data(self):
        """Menghapus data yang dipilih dari tabel"""
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Kesalahan Hapus", "Pilih data yang ingin dihapus.")  # Pesan peringatan jika tidak ada data yang dipilih
            return

        selected_values = self.table.item(selected_item[0], "values")
        tanggal = selected_values[0]
        nama_produk = selected_values[1]
        banyak_produk = selected_values[2]

        # Membaca data dari file Excel
        data = read_excel(DATA_FILE)

        # Filter data untuk menghapus row yang dipilih
        data = [row for row in data if not (str(row["Tanggal"]) == tanggal and
                                            row["Nama Produk"] == nama_produk and
                                            str(row["Banyak Produk"]) == banyak_produk)]

        # Tulis kembali data yang sudah terfilter ke Excel
        write_excel(DATA_FILE, data, ["Tanggal", "Nama Produk", "Banyak Produk"])
        self.load_data()
        messagebox.showinfo("Berhasil", "Data berhasil dihapus!")  # Pesan info setelah data berhasil dihapus

    def back_to_dashboard(self):
        """Kembali ke halaman dashboard"""
        self.frame.destroy()
        from views.dashboard_view import DashboardView
        DashboardView(self.master)
