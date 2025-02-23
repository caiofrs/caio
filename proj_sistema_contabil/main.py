from tkinter import Tk
from library.interface.home import Home


def main() -> None:
    """Main function to start the application"""
    root = Tk()
    try:
        root.tk.call("source", r"C:\Users\Caio\vscode\Proj_contabil\Azure-ttk-theme-main\azure.tcl")  # Atualize com o caminho correto para azure.tcl
        root.tk.call("set_theme", "dark")
        print("Tema Azure carregado com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar o tema Azure: {e}")
    app = Home(root)
    root.mainloop()

if __name__ == "__main__":
    main()