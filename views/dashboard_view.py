import tkinter as tk
from PIL.Image import Image
from PIL import Image, ImageTk
from views.persediaan_view import PersediaanView
from views.pembelian_view import PembelianView
from views.penjualan_view import PenjualanView

class DashboardView:
    def __init__(self, master):
        self.master = master
        self.master.title("Dashboard - Chic Shawl")
        self.master.geometry("1000x600")
        self.master.configure(bg="#FFF9BF")
        self.master.minsize(400, 500)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.frame = tk.Frame(self.master, bg="#FFF9BF", padx=20, pady=20)
        self.frame.grid(sticky="nsew")
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        logo = Image.open("cs_logo.png")
        logo = logo.resize((200, 200), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(self.frame, image=logo_img, bg="#FFF9BF")
        logo_label.image = logo_img
        logo_label.grid(row=0, column=0, pady=15)

        tk.Label(
            self.frame,
            text="Chic Shawl - Dashboard",
            font=("Arial", 30, "bold"),
            bg="#FFF9BF",
            fg="#CB9DF0"
        ).grid(row=1, column=0, pady=10)

        button_frame = tk.Frame(self.frame, bg="#FFF9BF")
        button_frame.grid(row=2, column=0, pady=20, sticky="nsew")
        button_frame.grid_columnconfigure(0, weight=1)

        tk.Button(button_frame, text="Persediaan", width=18, height=2, font=("Arial", 12, "bold"), fg=("#CB9DF0"), command=self.open_persediaan).grid(row=0, column=0, pady=5)
        tk.Button(button_frame, text="Pembelian", width=18, height=2, font=("Arial", 12, "bold"), fg=("#CB9DF0"), command=self.open_pembelian).grid(row=1, column=0, pady=5)
        tk.Button(button_frame, text="Penjualan", width=18, height=2, font=("Arial", 12, "bold"), fg=("#CB9DF0"), command=self.open_penjualan).grid(row=2, column=0, pady=5)
        tk.Button(button_frame, text="Keluar", width=16, height=2, font=("Arial", 10, "bold"), fg=("#B8001F"), command=self.master.quit).grid(row=3, column=0, pady=15)

    def open_persediaan(self):
        self.frame.destroy()
        PersediaanView(self.master)

    def open_pembelian(self):
        self.frame.destroy()
        PembelianView(self.master)

    def open_penjualan(self):
        self.frame.destroy()
        PenjualanView(self.master)

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardView(root)
    root.mainloop()
