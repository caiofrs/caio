from tkinter import *
from tkinter import ttk
import sqlite3
import cadastro.app_globals as app_globals

def create_reports_frame(content_frame):
    """Creates the frame for the reports screen"""
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Create a frame to hold the buttons
    button_frame = Frame(content_frame)
    button_frame.grid(row=0, column=0, padx=10, pady=10, sticky=N+S+E+W)

    # Define the button names and their corresponding commands
    button_names = [
        ("Faturamento Mensal", show_faturamento_mensal),
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

def show_faturamento_mensal():
    """Shows the faturamento mensal page with the last 12 competencies"""
    root = Tk()
    root.geometry("800x600")
    content_frame = Frame(root)
    content_frame.pack(fill=BOTH, expand=True)

    # Fetch the last 12 competencies for the selected company
    competencias = fetch_last_12_competencias(app_globals.selected_company)

    # Create a frame to hold the buttons
    button_frame = Frame(content_frame)
    button_frame.grid(row=0, column=0, padx=10, pady=10, sticky=N+S+E+W)

    # Create and place the buttons in a 2-column grid
    for i, competencia in enumerate(competencias):
        button = ttk.Button(button_frame, text=competencia)
        button.grid(row=i//2, column=i%2, padx=5, pady=5, sticky=W+E)

    # Configure the grid to expand the buttons equally
    for row in range(6):
        button_frame.grid_rowconfigure(row, weight=1)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)

    root.mainloop()

def fetch_last_12_competencias(company_id):
    """Fetches the last 12 competencies for the given company"""
    conn = sqlite3.connect('cadastro_empresas.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT competencia
        FROM notas_fiscais
        WHERE empresa_id = ?
        ORDER BY competencia DESC
        LIMIT 12
    """, (company_id,))
    competencias = [row[0] for row in cursor.fetchall()]
    conn.close()
    return competencias

if __name__ == "__main__":
    root = Tk()
    root.geometry("800x600")
    content_frame = Frame(root)
    content_frame.pack(fill=BOTH, expand=True)
    create_reports_frame(content_frame)
    root.mainloop()