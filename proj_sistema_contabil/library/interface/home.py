from tkinter import *
from tkinter.ttk import Style, Frame, Label, Button
import cadastro.cadastro as cadastro

class Home:

    def __init__(self, root):
        """Inicializa a janela principal"""
        self.root = root
        self.style = Style()
        self.frm = Frame(self.root, padding=10)
        self.frm.grid(sticky=N+S+E+W)
        self.content_frame = Frame(self.frm)
        self.content_frame.grid(row=1, column=0, sticky=N+S+E+W)
        self._setup_layout()

    def _cadastrar(self) -> None:
        """Cria a tela de cadastro"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        cadastro.create_cadastro_frame(self.content_frame)

    def _importar_notas(self) -> None:
        """Cria a tela de importar notas"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Label(self.content_frame, text="Tela de Importar Notas").grid()

    def _exportar_faturamento(self) -> None:
        """Cria a tela de exportar faturamento"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Label(self.content_frame, text="Tela de Exportar Faturamento").grid()

    def _emitir_das(self) -> None:
        """Cria a tela de emitir DAS"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Label(self.content_frame, text="Tela de Emitir DAS").grid()

    def _emitir_recibo(self) -> None:
        """Cria a tela de emitir recibo"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Label(self.content_frame, text="Tela de Emitir Recibo").grid()

    def _selecionar_empresa(self) -> None:
        """Cria a tela de selecionar empresa"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Label(self.content_frame, text="Tela de Selecionar Empresa").grid()

    def _setup_layout(self) -> None:
        """Configura o layout da janela principal"""

        # Configuração do estilo dark
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#2e2e2e")
        self.style.configure("TLabel", background="#2e2e2e", foreground="#ffffff", font=("Arial", 12))
        self.style.configure("TButton", background="#4d4d4d", foreground="#ffffff", font=("Arial", 12), padding=10)
        self.style.configure("DarkBlue.TButton", background="#00008b", foreground="#ffffff", font=("Arial", 12), padding=10)
        
        # Configuração do posicionamento da grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
       
        # Configuração do frame principal
        self.frm.grid_rowconfigure(1, weight=1)
        self.frm.grid_columnconfigure(0, weight=1)
        
        # Configuração dos botões
        button_frame = Frame(self.frm)
        button_frame.grid(row=0, column=0, sticky=W+E)
        
        Button(button_frame, text="Selecionar Empresa", command=self._selecionar_empresa, style="DarkBlue.TButton").grid(column=0, row=0, sticky=W+E, padx=5, pady=5)
        Button(button_frame, text="Cadastro", command=self._cadastrar).grid(column=1, row=0, sticky=W+E, padx=5, pady=5)
        Button(button_frame, text="Importar Notas", command=self._importar_notas).grid(column=2, row=0, sticky=W+E, padx=5, pady=5)
        Button(button_frame, text="Exportar Faturamento", command=self._exportar_faturamento).grid(column=3, row=0, sticky=W+E, padx=5, pady=5)
        Button(button_frame, text="Emitir DAS", command=self._emitir_das).grid(column=4, row=0, sticky=W+E, padx=5, pady=5)
        Button(button_frame, text="Emitir Recibo", command=self._emitir_recibo).grid(column=5, row=0, sticky=W+E, padx=5, pady=5)
        Button(button_frame, text="Quit", command=self.root.destroy).grid(column=6, row=0, sticky=W+E, padx=5, pady=5)

        # Configurando a grid para expandir os botões igualmente
        for i in range(7):
            button_frame.grid_columnconfigure(i, weight=1)

if __name__ == "__main__":
    root = Tk()
    app = Home(root)
    root.mainloop()
