from tkinter import *
from tkinter import ttk
import subprocess


def cadastrar():
    subprocess.Popen(['proj_sistema_contabil', 'cadastro.py'])

def importar_notas():
    print("Importar Notas selecionado")

def exportar_faturamento():
    print("Exportar Faturamento selecionado")

def emitir_das():
    print("Emitir DAS selecionado")

def emitir_recibo():
    print("Emitir Recibo selecionado")

root = Tk()
root.title("Sistema Contábil")

# Configurando o estilo dark
style = ttk.Style()
style.theme_use('clam')
style.configure("TFrame", background="#2e2e2e")
style.configure("TLabel", background="#2e2e2e", foreground="#ffffff", font=("Arial", 12))
style.configure("TButton", background="#4d4d4d", foreground="#ffffff", font=("Arial", 12), padding=10)

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Label(frm, text="Sistema Contábil").grid(column=0, row=0, columnspan=2, pady=10)

ttk.Button(frm, text="Cadastro", command=cadastrar).grid(column=0, row=1, sticky=W, pady=5)
ttk.Button(frm, text="Importar Notas", command=importar_notas).grid(column=0, row=2, sticky=W, pady=5)
ttk.Button(frm, text="Exportar Faturamento", command=exportar_faturamento).grid(column=0, row=3, sticky=W, pady=5)
ttk.Button(frm, text="Emitir DAS", command=emitir_das).grid(column=0, row=4, sticky=W, pady=5)
ttk.Button(frm, text="Emitir Recibo", command=emitir_recibo).grid(column=0, row=5, sticky=W, pady=5)

ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=6, sticky=W, pady=5)

root.mainloop()