from tkinter import *
from tkinter.ttk import Frame, Label, Entry, Button
import sqlite3
from tkinter import messagebox
import re

class Cliente:
    def __init__(self, cnpj, empresa, apelido, inscricao_municipal):
        self.cnpj = cnpj
        self.empresa = empresa
        self.apelido = apelido
        self.inscricao_municipal = inscricao_municipal

def validate_cnpj(cnpj):
    """Valida o formato do CNPJ"""
    pattern = r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$'
    return re.match(pattern, cnpj) is not None

def save_registration():
    cnpj = entry_cnpj.get()
    company = entry_company.get()
    nickname = entry_nickname.get()
    municipal_registration = entry_municipal_registration.get()

    # Valida o CNPJ
    if not validate_cnpj(cnpj):
        messagebox.showerror("Erro", "CNPJ inválido. Use o formato XX.XXX.XXX/XXXX-XX.")
        return

    # Create a Cliente object
    cliente = Cliente(cnpj, company, nickname, municipal_registration)

    # Connect to the database and insert the record
    try:
        conn = sqlite3.connect('cadastro_empresas.db')
        cursor = conn.cursor()
        
        # Create the table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS empresas (
                cnpj TEXT PRIMARY KEY,
                empresa TEXT NOT NULL,
                apelido TEXT,
                inscricao_municipal TEXT
            )
        ''')
        
        # Insert the record
        cursor.execute('''
            INSERT INTO empresas (cnpj, empresa, apelido, inscricao_municipal)
            VALUES (?, ?, ?, ?)
        ''', (cliente.cnpj, cliente.empresa, cliente.apelido, cliente.inscricao_municipal))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Empresa cadastrada com sucesso!")
        
        # Limpa os campos
        entry_cnpj.delete(0, END)
        entry_company.delete(0, END)
        entry_nickname.delete(0, END)
        entry_municipal_registration.delete(0, END)
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao salvar a empresa: {e}")

def create_registration_frame(content_frame):
    """Creates the registration frame inside the content_frame"""
    for widget in content_frame.winfo_children():
        widget.destroy()

    inner_frame = Frame(content_frame)
    inner_frame.grid(column=0, row=0, padx=10, pady=10, sticky=W)

    Label(inner_frame, text="Cadastro de Empresa").grid(column=0, row=0, columnspan=2, pady=5, sticky=W)

    Label(inner_frame, text="CNPJ:").grid(column=0, row=1, sticky=E, pady=2)
    global entry_cnpj
    entry_cnpj = Entry(inner_frame, width=30)
    entry_cnpj.grid(column=1, row=1, pady=2, sticky=W)
    entry_cnpj.configure(foreground="black")

    Label(inner_frame, text="Empresa:").grid(column=0, row=2, sticky=E, pady=2)
    global entry_company
    entry_company = Entry(inner_frame, width=30)
    entry_company.grid(column=1, row=2, pady=2, sticky=W)
    entry_company.configure(foreground="black")

    Label(inner_frame, text="Apelido:").grid(column=0, row=3, sticky=E, pady=2)
    global entry_nickname
    entry_nickname = Entry(inner_frame, width=30)
    entry_nickname.grid(column=1, row=3, pady=2, sticky=W)
    entry_nickname.configure(foreground="black")

    Label(inner_frame, text="Inscrição Municipal:").grid(column=0, row=4, sticky=E, pady=2)
    global entry_municipal_registration
    entry_municipal_registration = Entry(inner_frame, width=30)
    entry_municipal_registration.grid(column=1, row=4, pady=2, sticky=W)
    entry_municipal_registration.configure(foreground="black")

    Button(inner_frame, text="Salvar", command=save_registration).grid(column=0, row=5, columnspan=2, pady=5, sticky=W)

    # Configure the grid to not expand the inner frame
    content_frame.grid_rowconfigure(0, weight=0)
    content_frame.grid_columnconfigure(0, weight=0)