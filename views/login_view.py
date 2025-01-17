import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from networkx.algorithms.bipartite.basic import color

from utils.file_utils import read_excel, append_excel
from views.dashboard_view import DashboardView

USER_FILE = "data/users.xlsx"

class LoginView:
    def __init__(self, master):
        self.master = master
        self.master.title("Login - Chic Shawl")
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
        logo = logo.resize((300, 300), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo)
        self.logo_label = tk.Label(self.frame, image=logo_img, bg="#FFF9BF")
        self.logo_label.image = logo_img
        self.logo_label.grid(row=0, column=0, pady=10)

        tk.Label(
            self.frame,
            text="Selamat Datang di Chic Shawl",
            font=("Arial", 30, "bold"),
            bg="#FFF9BF",
            fg="#CB9DF0"
        ).grid(row=1, column=0, pady=10)

        form_frame = tk.Frame(self.frame, bg="#FFF9BF")
        form_frame.grid(row=2, column=0, pady=10, sticky="nsew")
        form_frame.grid_columnconfigure(1, weight=1)

        tk.Label(
            form_frame,
            text="Nama Pengguna",
            font=("Arial", 16, "bold"),
            bg="#FFF9BF",
            fg="#CB9DF0"
        ).grid(row=0, column=0, sticky="w", pady=5, padx=5)

        self.username_entry = tk.Entry(form_frame, font=("Arial", 16))
        self.username_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        tk.Label(
            form_frame,
            text="Kata Sandi",
            font=("Arial", 16, "bold"),
            bg="#FFF9BF",
            fg="#CB9DF0"
        ).grid(row=1, column=0, sticky="w", pady=5, padx=5)

        self.password_entry = tk.Entry(form_frame, show="*", font=("Arial", 16))
        self.password_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        button_frame = tk.Frame(self.frame, bg="#FFF9BF")
        button_frame.grid(row=3, column=0, pady=20)

        tk.Button(
            button_frame,
            text="Masuk",
            command=self.sign_in,
            bg="#7A5BAF",
            fg="#CB9DF0",
            font=("Arial", 16, "bold"),
            width=15
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Daftar",
            command=self.sign_up,
            bg="#7A5BAF",
            fg="#CB9DF0",
            font=("Arial", 16, "bold"),
            width=15
        ).grid(row=0, column=1, padx=5)

    def sign_in(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        users = read_excel(USER_FILE)
        for user in users:
            if user["username"] == username and user["password"] == password:
                self.frame.destroy()
                DashboardView(self.master)
                return
        messagebox.showerror("Login Gagal", "Nama pengguna atau kata sandi tidak valid.")

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showwarning("Kesalahan Input", "Harap isi semua kolom.")
            return
        users = read_excel(USER_FILE)
        for user in users:
            if user["username"] == username:
                messagebox.showerror("Daftar Gagal", "Nama pengguna sudah ada.")
                return

        user_data = {"username": username, "password": password}
        headers = ["username", "password"]
        append_excel(USER_FILE, user_data, headers)
        messagebox.showinfo("Daftar Sukses", "Akun berhasil dibuat!")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginView(root)
    root.mainloop()
