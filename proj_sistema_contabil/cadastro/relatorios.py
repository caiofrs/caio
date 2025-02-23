from tkinter import *
from tkinter import ttk


def create_reports_frame(content_frame):
    """Creates the frame for the reports screen"""
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Create a frame to hold the buttons
    button_frame = Frame(content_frame)
    button_frame.grid(row=0, column=0, padx=10, pady=10, sticky=N+S+E+W)

    # Define the button names and their corresponding commands
    button_names = [
        ("Faturamento Mensal", lambda: print("Faturamento Mensal")),
        ("Faturamento Anual", lambda: print("Faturamento Anual")),
        ("Recibos", lambda: print("Recibos")),
        ("Em breve", lambda: print("Em breve")),
        ("Em breve", lambda: print("Em breve")),
        ("Em breve", lambda: print("Em breve")),
        ("Em breve", lambda: print("Em breve")),
        ("Em breve", lambda: print("Em breve")),
        ("Em breve", lambda: print("Em breve")),
        ("Em breve", lambda: print("Em breve"))
    ]

    # Create and place the buttons in a 2-column grid
    for i, (name, command) in enumerate(button_names):
        button = ttk.Button(button_frame, text=name, command=command)
        button.grid(row=i//2, column=i%2, padx=5, pady=5, sticky=W+E)

    # Configure the grid to expand the buttons equally
    for row in range(5):
        button_frame.grid_rowconfigure(row, weight=1)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

if __name__ == "__main__":
    root = Tk()
    root.geometry("800x600")
    content_frame = Frame(root)
    content_frame.pack(fill=BOTH, expand=True)
    create_reports_frame(content_frame)
    root.mainloop()
