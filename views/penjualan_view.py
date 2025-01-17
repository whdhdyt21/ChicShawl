import tkinter as tk
from tkinter import messagebox, ttk
from utils.file_utils import read_excel, write_excel, append_excel

DATA_FILE = "data/penjualan.xlsx"

class PenjualanView:
    def __init__(self, master):
        self.master = master
        self.master.configure(bg="#FFF9BF")
        self.master.geometry("800x600")
        self.master.resizable(True, True)
        self.frame = tk.Frame(self.master, bg="#FFF9BF")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        # Judul
        tk.Label(self.frame, text="PENJUALAN", font=("Arial", 30, "bold"), fg="#CB9DF0", bg="#FFF9BF").pack(pady=10)

        # Tabel
        self.table = ttk.Treeview(self.frame, columns=("Tanggal", "Nama Produk", "Banyak Produk", "Harga"),
                                  show="headings", style="Custom.Treeview")
        self.table.heading("Tanggal", text="Tanggal")
        self.table.heading("Nama Produk", text="Nama Produk")
        self.table.heading("Banyak Produk", text="Banyak Produk")
        self.table.heading("Harga", text="Harga")
        self.table.pack(fill="both", expand=True, pady=10)

        # Scrollbars
        scrollbar_y = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.config(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.table.xview)
        self.table.config(xscrollcommand=scrollbar_x.set)
        scrollbar_x.pack(fill=tk.X)

        self.load_data()

        # Entry Fields (Kolom input)
        entry_frame = tk.Frame(self.frame, bg="#FFF9BF")
        entry_frame.pack(fill=tk.X, pady=10)

        self.entry_tanggal = tk.Entry(entry_frame, width=15)
        self.entry_tanggal.grid(row=0, column=0, padx=5)
        self.entry_tanggal.insert(0, "Tanggal")

        self.entry_nama = tk.Entry(entry_frame, width=20)
        self.entry_nama.grid(row=0, column=1, padx=5)
        self.entry_nama.insert(0, "Nama Produk")

        self.entry_banyak = tk.Entry(entry_frame, width=10)
        self.entry_banyak.grid(row=0, column=2, padx=5)
        self.entry_banyak.insert(0, "Banyak")

        self.entry_harga = tk.Entry(entry_frame, width=10)
        self.entry_harga.grid(row=0, column=3, padx=5)
        self.entry_harga.insert(0, "Harga")

        # Tombol aksi
        button_frame = tk.Frame(self.frame, bg="#FFF9BF")
        button_frame.pack(fill=tk.X, pady=10)

        tk.Button(button_frame, text="Simpan", command=self.add_data, font=("Arial", 16, "bold"), bg="#4CAF50", fg="#CB9DF0").grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Hapus", command=self.delete_data, font=("Arial", 16, "bold"), bg="#FF5722", fg="#CB9DF0").grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Kembali", command=self.back_to_dashboard, font=("Arial", 16, "bold"), bg="#2196F3", fg="#CB9DF0").grid(row=0, column=2, padx=5)

    def load_data(self):
        """Memuat data dari file Excel dan menampilkannya di tabel."""
        self.table.delete(*self.table.get_children())  # Menghapus data lama dari tabel
        data = read_excel(DATA_FILE)  # Membaca data dari file
        for row in data:
            self.table.insert("", "end", values=(row["Tanggal"], row["Nama Produk"], row["Banyak Produk"], row["Harga"]))

    def add_data(self):
        """Menambahkan data baru ke dalam tabel dan menyimpannya ke file Excel."""
        tanggal = self.entry_tanggal.get()
        nama = self.entry_nama.get()
        banyak = self.entry_banyak.get()
        harga = self.entry_harga.get()

        if not (tanggal and nama and banyak.isdigit() and harga.isdigit()):
            # Menampilkan pesan kesalahan jika input tidak valid
            messagebox.showwarning("Kesalahan Input", "Harap isi semua kolom dengan benar.")
            return

        # Menyimpan data ke file Excel
        append_excel(DATA_FILE, {"Tanggal": tanggal, "Nama Produk": nama, "Banyak Produk": banyak, "Harga": harga},
                     ["Tanggal", "Nama Produk", "Banyak Produk", "Harga"])
        self.load_data()  # Memuat ulang data ke tabel
        messagebox.showinfo("Berhasil", "Data berhasil disimpan!")

    def delete_data(self):
        """Menghapus data yang dipilih dari tabel dan file Excel."""
        selected_item = self.table.selection()  # Mendapatkan data yang dipilih
        if not selected_item:
            # Menampilkan pesan jika tidak ada data yang dipilih
            messagebox.showwarning("Kesalahan Hapus", "Pilih data yang ingin dihapus.")
            return

        selected_values = self.table.item(selected_item[0], "values")
        tanggal = selected_values[0]
        nama_produk = selected_values[1]
        banyak_produk = selected_values[2]
        harga_produk = selected_values[3]

        # Membaca data dari file Excel
        data = read_excel(DATA_FILE)

        # Memfilter data untuk menghapus baris yang dipilih
        data = [row for row in data if not (str(row["Tanggal"]) == tanggal and
                                            row["Nama Produk"] == nama_produk and
                                            str(row["Banyak Produk"]) == banyak_produk and
                                            str(row["Harga"]) == harga_produk)]

        # Menulis kembali data yang sudah difilter ke Excel
        write_excel(DATA_FILE, data, ["Tanggal", "Nama Produk", "Banyak Produk", "Harga"])
        self.load_data()  # Memuat ulang data ke tabel
        messagebox.showinfo("Berhasil", "Data berhasil dihapus!")

    def back_to_dashboard(self):
        """Kembali ke tampilan dashboard."""
        self.frame.destroy()
        from views.dashboard_view import DashboardView
        DashboardView(self.master)
