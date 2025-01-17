import tkinter as tk
from tkinter import messagebox, ttk
from utils.file_utils import read_excel, write_excel, append_excel

DATA_FILE = "data/pembelian.xlsx"

class PembelianView:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg="#FFF9BF")
        self.master.geometry("800x600")
        self.master.resizable(True, True)
        self.frame = tk.Frame(self.master, bg="#FFF9BF")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        # Label untuk judul
        tk.Label(self.frame, text="PEMBELIAN", font=("Arial", 30, "bold"), fg="#CB9DF0", bg="#FFF9BF").pack(pady=10)

        # Membuat tabel untuk menampilkan data
        self.table = ttk.Treeview(self.frame, columns=("Tanggal", "Nama Produk", "Jumlah Produk", "Harga"),
                                  show="headings", style="Custom.Treeview")
        self.table.heading("Tanggal", text="Tanggal")
        self.table.heading("Nama Produk", text="Nama Produk")
        self.table.heading("Jumlah Produk", text="Jumlah Produk")
        self.table.heading("Harga", text="Harga")
        self.table.pack(fill="both", expand=True, pady=10)

        # Menambahkan scrollbar vertikal
        scrollbar_y = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.config(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Menambahkan scrollbar horizontal
        scrollbar_x = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.table.xview)
        self.table.config(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(fill=tk.X)

        self.load_data()

        # Frame untuk field input
        entry_frame = tk.Frame(self.frame, bg="#FFF9BF")
        entry_frame.pack(fill=tk.X, pady=10)

        # Input untuk tanggal
        self.entry_tanggal = tk.Entry(entry_frame, width=15)
        self.entry_tanggal.grid(row=0, column=0, padx=5)
        self.entry_tanggal.insert(0, "Tanggal")

        # Input untuk nama produk
        self.entry_nama = tk.Entry(entry_frame, width=20)
        self.entry_nama.grid(row=0, column=1, padx=5)
        self.entry_nama.insert(0, "Nama Produk")

        # Input untuk jumlah produk
        self.entry_jumlah = tk.Entry(entry_frame, width=10)
        self.entry_jumlah.grid(row=0, column=2, padx=5)
        self.entry_jumlah.insert(0, "Jumlah")

        # Input untuk harga produk
        self.entry_harga = tk.Entry(entry_frame, width=10)
        self.entry_harga.grid(row=0, column=3, padx=5)
        self.entry_harga.insert(0, "Harga")

        # Frame untuk tombol aksi
        button_frame = tk.Frame(self.frame, bg="#FFF9BF")
        button_frame.pack(fill=tk.X, pady=10)

        # Tombol untuk menyimpan data
        tk.Button(button_frame, text="Simpan", command=self.add_data, font=("Arial", 16, "bold"), bg="#4CAF50", fg="#CB9DF0").grid(row=0, column=0, padx=5)

        # Tombol untuk menghapus data
        tk.Button(button_frame, text="Hapus", command=self.delete_data, font=("Arial", 16, "bold"), bg="#FF5722", fg="#CB9DF0").grid(row=0, column=1, padx=5)

        # Tombol untuk kembali ke dashboard
        tk.Button(button_frame, text="Kembali", command=self.back_to_dashboard, font=("Arial", 16, "bold"), bg="#2196F3", fg="#CB9DF0").grid(row=0, column=2, padx=5)

    def load_data(self):
        """Memuat data dari file dan menampilkan pada tabel"""
        self.table.delete(*self.table.get_children())
        data = read_excel(DATA_FILE)
        for row in data:
            self.table.insert("", "end", values=(row["Tanggal"], row["Nama Produk"], row["Jumlah Produk"], row["Harga"]))

    def add_data(self):
        """Menambahkan data ke dalam file Excel"""
        tanggal = self.entry_tanggal.get()
        nama = self.entry_nama.get()
        jumlah = self.entry_jumlah.get()
        harga = self.entry_harga.get()

        # Validasi input sebelum menyimpan data
        if not (tanggal and nama and jumlah.isdigit() and harga.isdigit()):
            messagebox.showwarning("Kesalahan Input", "Harap isi semua kolom dengan benar.")  # Pesan peringatan jika input tidak valid
            return

        append_excel(DATA_FILE, {"Tanggal": tanggal, "Nama Produk": nama, "Jumlah Produk": jumlah, "Harga": harga},
                     ["Tanggal", "Nama Produk", "Jumlah Produk", "Harga"])
        self.load_data()
        messagebox.showinfo("Berhasil", "Data berhasil disimpan!")  # Pesan info setelah data berhasil disimpan

    def delete_data(self):
        """Menghapus data yang dipilih dari tabel"""
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Kesalahan Hapus", "Pilih data yang ingin dihapus.")  # Pesan peringatan jika tidak ada data yang dipilih
            return

        selected_values = self.table.item(selected_item[0], "values")
        tanggal = selected_values[0]
        nama_produk = selected_values[1]
        jumlah_produk = selected_values[2]
        harga_produk = selected_values[3]

        data = read_excel(DATA_FILE)

        # Filter data untuk menghapus row yang dipilih
        data = [row for row in data if not (str(row["Tanggal"]) == tanggal and
                                            row["Nama Produk"] == nama_produk and
                                            str(row["Jumlah Produk"]) == jumlah_produk and
                                            str(row["Harga"]) == harga_produk)]

        write_excel(DATA_FILE, data, ["Tanggal", "Nama Produk", "Jumlah Produk", "Harga"])
        self.load_data()
        messagebox.showinfo("Berhasil", "Data berhasil dihapus!")  # Pesan info setelah data berhasil dihapus

    def back_to_dashboard(self):
        """Kembali ke halaman dashboard"""
        self.frame.destroy()
        from views.dashboard_view import DashboardView
        DashboardView(self.master)
