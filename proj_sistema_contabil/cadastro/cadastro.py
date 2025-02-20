from tkinter import *
from tkinter.ttk import Frame, Label, Entry, Button

def save_register():
    cnpj = entry_cnpj.get()
    company = entry_company.get()
    nickName = entry_nickName.get()
    inscricao_municipal = entry_inscricao_municipal.get()
    print(f"CNPJ: {cnpj}, Empresa: {company}, Apelido: {nickName}, Inscrição Municipal: {inscricao_municipal}")

def create_register_frame(content_frame):
    """create the frame of register into the content_frame"""
    Label(content_frame, text="Cadastro de Empresa").grid(column=0, row=0, columnspan=2, pady=10)

    Label(content_frame, text="CNPJ:").grid(column=0, row=1, sticky=W, pady=5)
    global entry_cnpj
    entry_cnpj = Entry(content_frame, width=30)
    entry_cnpj.grid(column=1, row=1, pady=5)
    entry_cnpj.configure(foreground="black")

    Label(content_frame, text="Empresa:").grid(column=0, row=2, sticky=W, pady=5)
    global entry_company
    entry_company = Entry(content_frame, width=30)
    entry_company.grid(column=1, row=2, pady=5)
    entry_company.configure(foreground="black")

    Label(content_frame, text="Apelido:").grid(column=0, row=3, sticky=W, pady=5)
    global entry_nickName
    entry_nickName = Entry(content_frame, width=30)
    entry_nickName.grid(column=1, row=3, pady=5)
    entry_nickName.configure(foreground="black")

    Label(content_frame, text="Inscrição Municipal:").grid(column=0, row=4, sticky=W, pady=5)
    global entry_inscricao_municipal
    entry_inscricao_municipal = Entry(content_frame, width=30)
    entry_inscricao_municipal.grid(column=1, row=4, pady=5)
    entry_inscricao_municipal.configure(foreground="black")

    Button(content_frame, text="Salvar", command=salvar_cadastro).grid(column=0, row=5, columnspan=2, pady=10)
