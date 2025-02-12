from tkinter import *
from tkinter import ttk

def salvar_cadastro():
    cnpj = entry_cnpj.get()
    empresa = entry_empresa.get()
    inscricao_municipal = entry_inscricao_municipal.get()
    print(f"CNPJ: {cnpj}, Empresa: {empresa}, Inscrição Municipal: {inscricao_municipal}")

root = Tk()
root.title("Cadastro de Empresa")

# Configurando o estilo dark
style = ttk.Style()
style.theme_use('clam')
style.configure("TFrame", background="#2e2e2e")
style.configure("TLabel", background="#2e2e2e", foreground="#ffffff", font=("Arial", 12))
style.configure("TButton", background="#4d4d4d", foreground="#ffffff", font=("Arial", 12), padding=10)
style.configure("TEntry", background="#4d4d4d", foreground="#ffffff", font=("Arial", 12))

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Cadastro de Empresa").grid(column=0, row=0, columnspan=2, pady=10)

ttk.Label(frm, text="CNPJ:").grid(column=0, row=1, sticky=W, pady=5)
entry_cnpj = ttk.Entry(frm, width=30)
entry_cnpj.grid(column=1, row=1, pady=5)

ttk.Label(frm, text="Empresa:").grid(column=0, row=2, sticky=W, pady=5)
entry_empresa = ttk.Entry(frm, width=30)
entry_empresa.grid(column=1, row=2, pady=5)

ttk.Label(frm, text="Inscrição Municipal:").grid(column=0, row=3, sticky=W, pady=5)
entry_inscricao_municipal = ttk.Entry(frm, width=30)
entry_inscricao_municipal.grid(column=1, row=3, pady=5)

ttk.Button(frm, text="Salvar", command=salvar_cadastro).grid(column=0, row=4, columnspan=2, pady=10)

root.mainloop()