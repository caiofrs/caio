from tkinter import *
from tkinter.ttk import Frame, Label, Entry, Button

def salvar_cadastro():
    cnpj = entry_cnpj.get()
    empresa = entry_empresa.get()
    apelido = entry_apelido.get()
    inscricao_municipal = entry_inscricao_municipal.get()
    print(f"CNPJ: {cnpj}, Empresa: {empresa}, Apelido: {apelido}, Inscrição Municipal: {inscricao_municipal}")

def create_cadastro_frame(content_frame):
    """Cria o frame de cadastro dentro do content_frame"""
    Label(content_frame, text="Cadastro de Empresa").grid(column=0, row=0, columnspan=2, pady=10)

    Label(content_frame, text="CNPJ:").grid(column=0, row=1, sticky=W, pady=5)
    global entry_cnpj
    entry_cnpj = Entry(content_frame, width=30)
    entry_cnpj.grid(column=1, row=1, pady=5)
    entry_cnpj.configure(foreground="black")

    Label(content_frame, text="Empresa:").grid(column=0, row=2, sticky=W, pady=5)
    global entry_empresa
    entry_empresa = Entry(content_frame, width=30)
    entry_empresa.grid(column=1, row=2, pady=5)
    entry_empresa.configure(foreground="black")

    Label(content_frame, text="Apelido:").grid(column=0, row=3, sticky=W, pady=5)
    global entry_apelido
    entry_apelido = Entry(content_frame, width=30)
    entry_apelido.grid(column=1, row=3, pady=5)
    entry_apelido.configure(foreground="black")

    Label(content_frame, text="Inscrição Municipal:").grid(column=0, row=4, sticky=W, pady=5)
    global entry_inscricao_municipal
    entry_inscricao_municipal = Entry(content_frame, width=30)
    entry_inscricao_municipal.grid(column=1, row=4, pady=5)
    entry_inscricao_municipal.configure(foreground="black")

    Button(content_frame, text="Salvar", command=salvar_cadastro).grid(column=0, row=5, columnspan=2, pady=10)