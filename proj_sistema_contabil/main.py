from tkinter import Tk
from library.interface.home import Home


def main() -> None:
    """Função principal"""
    home = Home()
    home.start()
    home.root.mainloop()



if __name__ == "__main__":
    root = Tk()
    app = Home(root)
    root.mainloop()
