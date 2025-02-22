from tkinter import *
from tkinter.ttk import Style, Frame, Label, Button
import cadastro.cadastrar as cadastro
import cadastro.selecionar_empresa as selecionar_empresa
import cadastro.importar_notas as importar_notas
import cadastro.relatorios as relatorios
import cadastro.notas_fiscais as notas_fiscais
import cadastro.app_globals as app_globals

class Home:

    def __init__(self, root):
        """Initializes the main window"""
        self.root = root
        self.root.geometry("1280x720")
        self.style = Style()
        self.main_frame = Frame(self.root, padding=10)
        self.main_frame.grid(sticky=N+S+E+W)
        self.content_frame = Frame(self.main_frame)
        self.content_frame.grid(row=2, column=0, sticky=N+S+E+W)
        self.selected_company_label = Label(self.main_frame, text="", font=("Arial", 14), foreground="blue")
        self.selected_company_label.grid(row=1, column=0, columnspan=3, pady=10)
        self.title_label = Label(self.main_frame, text="", font=("Arial", 24, "bold"), foreground="white", background="#00008b")
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky=W+E)
        self._setup_layout()
        selecionar_empresa.set_home_instance(self)

    def update_selected_company_label(self, company_name):
        """Updates the label with the selected company name"""
        self.selected_company_label.config(text=f"Empresa Selecionada: {company_name}")

    def update_title(self, title: str) -> None:
        """Updates the title at the top of the main window"""
        self.title_label.config(text=title)

    def _register(self) -> None:
        """Creates the registration screen"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        cadastro.create_registration_frame(self.content_frame)

    def _import_notes(self) -> None:
        """Creates the import notes screen"""
        if app_globals.selected_company is None:
            print("No company selected. Please select a company first.")
            Label(self.content_frame, text="Por favor, selecione uma empresa primeiro.", foreground="red").grid(column=0, row=0, columnspan=3, pady=10)
        else:
            importar_notas.create_import_notes_frame(self.content_frame)

    def _export_revenue(self) -> None:
        """Creates the export revenue screen"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Label(self.content_frame, text="Tela de Exportar Faturamento").grid()

    def _issue_das(self) -> None:
        """Creates the issue DAS screen"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Label(self.content_frame, text="Tela de Emitir DAS").grid()

    def _issue_receipt(self) -> None:
        """Creates the issue receipt screen"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        Label(self.content_frame, text="Tela de Emitir Recibo").grid()

    def _select_company(self) -> None:
        """Creates the select company screen"""
        selecionar_empresa.create_select_company_frame(self.content_frame)

    def _reports(self) -> None:
        """Creates the reports screen"""
        relatorios.create_reports_frame(self.content_frame)

    def _show_invoices(self) -> None:
        """Shows all invoices for the last selected company"""
        notas_fiscais.show_client_invoices(self.content_frame)

    def _setup_layout(self) -> None:
        """Configures the layout of the main window"""

        # Dark style configuration
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#2e2e2e")
        self.style.configure("TLabel", background="#2e2e2e", foreground="#ffffff", font=("Arial", 12))
        self.style.configure("TButton", background="#4d4d4d", foreground="#ffffff", font=("Arial", 12), padding=10)
        self.style.configure("DarkBlue.TButton", background="#00008b", foreground="#ffffff", font=("Arial", 12), padding=10)
        
        # Grid positioning configuration
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
       
        # Main frame configuration
        self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Button configuration
        button_frame = Frame(self.main_frame)
        button_frame.grid(row=1, column=0, sticky=W+E)
        
        Button(button_frame, text="Selecionar Empresa", command=self._select_company, style="DarkBlue.TButton").grid(column=0, row=0, sticky=W+E, padx=5, pady=5)
        Button(button_frame, text="Notas Fiscais", command=self._show_invoices).grid(column=1, row=0, sticky=W+E, padx=5, pady=5)
        Button(button_frame, text="Cadastrar", command=self._register).grid(column=2, row=0, sticky=W+E, padx=5, pady=5)
        Button(button_frame, text="Importar Notas", command=self._import_notes).grid(column=3, row=0, sticky=W+E, padx=5, pady=5)
        Button(button_frame, text="Relatorios", command=self._reports).grid(column=4, row=0, sticky=W+E, padx=5, pady=5)
        Button(button_frame, text="Emitir DAS", command=self._issue_das).grid(column=5, row=0, sticky=W+E, padx=5, pady=5)
        Button(button_frame, text="Emitir Recibo", command=self._issue_receipt).grid(column=6, row=0, sticky=W+E, padx=5, pady=5)
        Button(button_frame, text="Quit", command=self.root.destroy).grid(column=7, row=0, sticky=W+E, padx=5, pady=5)

        # Configuring the grid to expand the buttons equally
        for i in range(8):
            button_frame.grid_columnconfigure(i, weight=1)

if __name__ == "__main__":
    root = Tk()
    app = Home(root)
    root.mainloop()