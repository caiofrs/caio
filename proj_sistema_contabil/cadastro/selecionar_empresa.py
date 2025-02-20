from tkinter import *
from tkinter import ttk
import sqlite3
import os
import cadastro.app_globals as app_globals
from tkinter import messagebox

def on_company_select(event):
    """Function to handle the selection of a company"""
    selected_item = tree.selection()
    if selected_item:
        selected_item = selected_item[0]
        app_globals.selected_company = tree.item(selected_item, 'values')[0]
        app_globals.selected_company_name = tree.item(selected_item, 'values')[1]
        print(f"Selected company: {app_globals.selected_company}, {app_globals.selected_company_name}")
        # Update the label in the Home class
        home_instance.update_selected_company_label(app_globals.selected_company_name)
        # Update the title in the Home class
        home_instance.update_title(f"Empresa Selecionada: {app_globals.selected_company_name}")

def edit_company(record, content_frame):
    """Function to edit the selected company"""
    edit_window = Toplevel()
    edit_window.title("Editar Empresa")
    edit_window.geometry("400x300")

    fields = ["CNPJ", "Empresa", "Apelido", "Inscrição Municipal"]
    entries = {}

    for i, field in enumerate(fields):
        ttk.Label(edit_window, text=field).grid(row=i, column=0, padx=10, pady=5)
        entry = ttk.Entry(edit_window)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entry.insert(0, record[i])
        entries[field] = entry

    def save_changes():
        new_values = {field: entry.get() for field, entry in entries.items()}
        try:
            conn = sqlite3.connect('cadastro_empresas.db')
            cursor = conn.cursor()
            
            # Verifica se o CNPJ foi alterado
            if new_values["CNPJ"] != record[0]:
                cursor.execute("SELECT cnpj FROM empresas WHERE cnpj = ?", (new_values["CNPJ"],))
                if cursor.fetchone():
                    messagebox.showerror("Erro", "CNPJ já existe. Use um CNPJ diferente.")
                    return
            
            cursor.execute('''
                UPDATE empresas
                SET cnpj = ?, empresa = ?, apelido = ?, inscricao_municipal = ?
                WHERE cnpj = ?
            ''', (new_values["CNPJ"], new_values["Empresa"], new_values["Apelido"], new_values["Inscrição Municipal"], record[0]))
            conn.commit()
            conn.close()
            edit_window.destroy()
            # Recarrega a lista de empresas
            create_select_company_frame(content_frame)
            messagebox.showinfo("Sucesso", "Empresa atualizada com sucesso!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao atualizar a empresa: {e}")

    def delete_record():
        try:
            conn = sqlite3.connect('cadastro_empresas.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM empresas WHERE cnpj = ?', (record[0],))
            conn.commit()
            conn.close()
            edit_window.destroy()
            # Recarrega a lista de empresas
            create_select_company_frame(content_frame)
            messagebox.showinfo("Sucesso", "Empresa excluída com sucesso!")
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao excluir a empresa: {e}")

    ttk.Button(edit_window, text="Salvar", command=save_changes).grid(row=len(fields), column=0, pady=10, padx=5, sticky=E)
    ttk.Button(edit_window, text="Cancelar", command=edit_window.destroy).grid(row=len(fields), column=1, pady=10, padx=5, sticky=W)
    Button(edit_window, text="Excluir registro", command=delete_record, bg="red", fg="white").grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

def create_select_company_frame(content_frame):
    """Creates the frame to select a company"""
    for widget in content_frame.winfo_children():
        widget.destroy()

    global tree
    global canvas
    # Create a Treeview widget to display the companies
    style = ttk.Style()
    style.theme_use("azure-dark")  # Use the Azure dark theme
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("Treeview", font=("Arial", 12), rowheight=50)  # Increase row height
    tree = ttk.Treeview(content_frame, columns=("cnpj", "company", "nickname", "municipal_registration"), show="headings")
    tree.heading("cnpj", text="CNPJ")
    tree.heading("company", text="Empresa")
    tree.heading("nickname", text="Apelido")
    tree.heading("municipal_registration", text="Inscrição Municipal")
    tree.grid(row=0, column=1, sticky=N+S+E+W, padx=10, pady=10)  # Add padding

    tree.bind("<Double-1>", on_company_select)

    # Create a Canvas to hold the buttons
    canvas = Canvas(content_frame, width=100)  # Set the width of the canvas to 100px
    canvas.grid(row=0, column=2, sticky=N+S, padx=10, pady=10)  # Add padding

    # Add a spacer column to the left
    content_frame.grid_columnconfigure(0, minsize=80)

    # Configure the grid to expand the Treeview
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)
    content_frame.grid_columnconfigure(2, weight=0)  # Ensure the second column does not expand

    # Define the path to the database
    db_path = 'cadastro_empresas.db'
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return

    # Connect to the database and fetch the records
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT cnpj, empresa, apelido, inscricao_municipal FROM empresas ORDER BY apelido")
        records = cursor.fetchall()
        conn.close()

        # Debug: Print the records to the console
        print("Records fetched from the database:")
        for record in records:
            print(record)

        # Insert the records into the Treeview and add edit buttons
        for i, record in enumerate(records):
            item_id = tree.insert("", "end", values=record)
            add_edit_button(i, record, content_frame)

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def add_edit_button(index, record, content_frame):
    """Adds an edit button next to the specified row in the Treeview"""
    button = ttk.Button(canvas, text="Editar", command=lambda r=record: edit_company(r, content_frame))
    canvas.create_window(10, index * 50 + 60, window=button, anchor=W)  # Adjusted position

# Reference to the Home instance
home_instance = None

def set_home_instance(instance):
    global home_instance
    home_instance = instance

if __name__ == "__main__":
    root = Tk()
    root.geometry("800x600")
    root.tk.call("source", r"C:\Users\Caio\vscode\Proj_contabil\Azure-ttk-theme-main\azure.tcl")  # Update with the correct path to azure.tcl
    root.tk.call("set_theme", "dark")
    content_frame = Frame(root)
    content_frame.pack(fill=BOTH, expand=True)
    create_select_company_frame(content_frame)
    root.mainloop()