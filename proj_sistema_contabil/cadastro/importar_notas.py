from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Button, Label
import pandas as pd
import sqlite3
import os
import cadastro.app_globals as app_globals

def import_csv_files():
    """Function to import multiple CSV files and display their names"""
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    if file_paths:
        file_names.set(", ".join([os.path.basename(file_path) for file_path in file_paths]))
        # Create Confirm and Cancel buttons
        Button(content_frame, text="Confirmar", command=lambda: confirm_selection(file_paths)).grid(column=1, row=2, pady=10)
        Button(content_frame, text="Cancelar", command=cancel_selection).grid(column=2, row=2, pady=10)

def confirm_selection(file_paths):
    """Function to confirm the file selection and process the CSV files"""
    print(f"Files confirmed: {file_names.get()}")
    duplicate_notes = []
    try:
        for file_path in file_paths:
            df = pd.read_csv(file_path, encoding='latin1', delimiter=';')
            print(f"DataFrame loaded successfully from {file_path}:")
            print(df.head())  # Print the first few rows of the dataframe for debugging

            # Filter the columns of interest
            df_filtered = df[['Data Hora da Emissão da Nota Fiscal', 'Nº da Nota Fiscal Eletrônica', 'Razão Social do Tomador', 'Valor dos Serviços', 'Nome Fantasia do Prestador']].copy()
            df_filtered.columns = ['data_emissao', 'numero_nota', 'nome_cliente', 'valor_nota', 'nome_fantasia_prestador']
            print("Filtered DataFrame:")
            print(df_filtered.head())  # Print the first few rows of the filtered dataframe for debugging
            
            # Process the data to extract month and year
            df_filtered['data_emissao'] = pd.to_datetime(df_filtered['data_emissao'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
            df_filtered['mes'] = df_filtered['data_emissao'].dt.strftime('%Y_%m')

            # Convert data_emissao to string format
            df_filtered['data_emissao'] = df_filtered['data_emissao'].dt.strftime('%Y-%m-%d %H:%M:%S')

            # Store the data in the database
            db_path = 'notas_fiscais.db'
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            for mes, group in df_filtered.groupby('mes'):
                table_name = f'notas_{mes}'
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        data_emissao TEXT,
                        numero_nota INTEGER,
                        nome_cliente TEXT,
                        valor_nota REAL,
                        nome_fantasia_prestador TEXT,
                        empresa TEXT,
                        PRIMARY KEY (numero_nota, empresa)
                    )
                ''')
                group['empresa'] = app_globals.selected_company

                # Check for duplicate notes
                for _, row in group.iterrows():
                    cursor.execute(f'''
                        SELECT COUNT(*)
                        FROM {table_name}
                        WHERE numero_nota = ? AND empresa = ?
                    ''', (row['numero_nota'], row['empresa']))
                    if cursor.fetchone()[0] == 0:
                        cursor.execute(f'''
                            INSERT INTO {table_name} (data_emissao, numero_nota, nome_cliente, valor_nota, nome_fantasia_prestador, empresa)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (row['data_emissao'], row['numero_nota'], row['nome_cliente'], row['valor_nota'], row['nome_fantasia_prestador'], row['empresa']))
                    else:
                        duplicate_notes.append(row['numero_nota'])

            conn.commit()
            conn.close()
            print(f"Data stored in the database successfully from {file_path}.")

        if duplicate_notes:
            messagebox.showwarning("Notas Duplicadas", f"As seguintes notas foram duplicadas e não foram inseridas: {', '.join(map(str, duplicate_notes))}")
        
        messagebox.showinfo("Importação Concluída", "A importação foi realizada com sucesso!")

    except Exception as e:
        print(f"An error occurred while reading the CSV files: {e}")

def cancel_selection():
    """Function to cancel the file selection"""
    file_names.set("")
    # Remove Confirm and Cancel buttons
    for widget in content_frame.grid_slaves(row=2, column=1):
        widget.grid_forget()
    for widget in content_frame.grid_slaves(row=2, column=2):
        widget.grid_forget()

def create_import_notes_frame(frame):
    """Creates the frame to import notes"""
    global content_frame
    content_frame = frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    global file_names
    file_names = StringVar()

    Label(content_frame, text="Importar Notas").grid(column=0, row=0, columnspan=3, pady=10)

    Button(content_frame, text="Selecionar Arquivo CSV", command=import_csv_files).grid(column=0, row=1, pady=5)
    Label(content_frame, textvariable=file_names).grid(column=1, row=1, pady=5, columnspan=2, sticky=W+E)

    # Configure the grid to expand the Label
    content_frame.grid_columnconfigure(1, weight=1)

if __name__ == "__main__":
    root = Tk()
    root.geometry("400x200")
    content_frame = Frame(root)
    content_frame.pack(fill=BOTH, expand=True)
    create_import_notes_frame(content_frame)
    root.mainloop()