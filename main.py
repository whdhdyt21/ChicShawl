import tkinter as tk
from views.login_view import LoginView

def main():
    root = tk.Tk()
    root.title("Chic Shawl - Aplikasi Akuntansi")
    root.geometry("800x600")
    app = LoginView(root)
    root.mainloop()

if __name__ == "__main__":
    main()