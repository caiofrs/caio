from tkinter import *
from tkinter import ttk
import sqlite3
import pandas as pd
import os
import cadastro.app_globals as app_globals

def show_client_invoices(content_frame):
    """Shows the invoices of the selected client grouped by month"""
    for widget in content_frame.winfo_children():
        widget.destroy()

    if app_globals.selected_company is None:
        print("No company selected. Please select a company first.")
        Label(content_frame, text="Por favor, selecione uma empresa primeiro.", foreground="red").grid(column=0, row=0, columnspan=3, pady=10)
        return

    company_name = app_globals.selected_company_name

    # Frame para o bloco de botões (esquerda)
    button_frame = Frame(content_frame)
    button_frame.grid(row=0, column=0, sticky=N+S+E+W, padx=10, pady=10)

    # Adicionar uma barra de rolagem ao bloco de botões
    canvas = Canvas(button_frame)
    scrollbar = ttk.Scrollbar(button_frame, orient=VERTICAL, command=canvas.yview)
    scrollable_button_frame = Frame(canvas)

    # Configurar a barra de rolagem
    scrollable_button_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_button_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Frame para o bloco de informações das notas fiscais (direita)
    invoice_frame = Frame(content_frame)
    invoice_frame.grid(row=0, column=1, sticky=N+S+E+W, padx=10, pady=10)

    # Configurar o Treeview para exibir as notas fiscais
    style = ttk.Style()
    style.configure("Treeview.Heading", anchor=CENTER)
    style.configure("Treeview", rowheight=25)
    invoice_tree = ttk.Treeview(invoice_frame, columns=("data_emissao", "numero_nota", "nome_cliente", "valor_nota"), show="headings")
    invoice_tree.heading("data_emissao", text="Data de Emissão", anchor=CENTER)
    invoice_tree.heading("numero_nota", text="Número da Nota", anchor=CENTER)
    invoice_tree.heading("nome_cliente", text="Nome do Tomador", anchor=CENTER)
    invoice_tree.heading("valor_nota", text="Valor da Nota", anchor=CENTER)
    invoice_tree.column("data_emissao", anchor=CENTER)
    invoice_tree.column("numero_nota", anchor=CENTER)
    invoice_tree.column("nome_cliente", anchor=CENTER)
    invoice_tree.column("valor_nota", anchor=CENTER)

    # Adicionar barra de rolagem ao Treeview
    vsb = ttk.Scrollbar(invoice_frame, orient=VERTICAL, command=invoice_tree.yview)
    invoice_tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side=RIGHT, fill=Y)
    invoice_tree.pack(side=LEFT, fill=BOTH, expand=True)

    # Configurar o grid para expansão
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=1)

    # Conectar ao banco de dados e buscar as notas fiscais
    db_path = 'notas_fiscais.db'
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Buscar as tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        # DataFrame para armazenar as notas fiscais
        df_invoices = pd.DataFrame(columns=['data_emissao', 'numero_nota', 'nome_cliente', 'valor_nota'])

        # Buscar as notas fiscais da empresa selecionada
        for table in tables:
            table_name = table[0]
            query = f'''
                SELECT data_emissao, numero_nota, nome_cliente, valor_nota
                FROM {table_name}
                WHERE nome_fantasia_prestador = ?
            '''
            cursor.execute(query, (company_name,))
            records = cursor.fetchall()
            df_table = pd.DataFrame(records, columns=['data_emissao', 'numero_nota', 'nome_cliente', 'valor_nota'])
            df_invoices = pd.concat([df_invoices, df_table], ignore_index=True)

        conn.close()

        # Processar os dados
        df_invoices['data_emissao'] = pd.to_datetime(df_invoices['data_emissao'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
        df_invoices['competencia'] = df_invoices['data_emissao'].dt.strftime('%Y-%m')
        df_invoices['valor_nota'] = pd.to_numeric(df_invoices['valor_nota'].str.replace(',', '.'), errors='coerce')
        df_invoices['valor_nota'] = df_invoices['valor_nota'].fillna(0)

        # Agrupar por competência
        df_grouped = df_invoices.groupby('competencia').agg({'valor_nota': 'sum'}).reset_index()
        df_grouped = df_grouped.sort_values(by='competencia', ascending=False)

        # Adicionar botões para cada competência
        for i, row in enumerate(df_grouped.iterrows()):
            total_text = f"{row[1]['competencia']}: {row[1]['valor_nota']:,.2f}"
            total_label = Label(scrollable_button_frame, text=total_text, font=("Arial", 10, "bold"))
            total_label.grid(row=i, column=0, sticky=W, pady=5)
            Button(scrollable_button_frame, text=row[1]['competencia'], command=lambda c=row[1]['competencia']: show_invoices_by_month(invoice_tree, df_invoices, c), width=15).grid(row=i, column=1, padx=5, pady=5)

        # Exibir todas as notas fiscais inicialmente
        for _, row in df_invoices.iterrows():
            invoice_tree.insert("", "end", values=(row['data_emissao'], row['numero_nota'], row['nome_cliente'], f"{row['valor_nota']:,.2f}"))

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def show_invoices_by_month(tree, df_invoices, competencia):
    """Filtra as notas fiscais por mês selecionado"""
    for item in tree.get_children():
        tree.delete(item)

    df_filtered = df_invoices[df_invoices['competencia'] == competencia]
    for _, row in df_filtered.iterrows():
        tree.insert("", "end", values=(row['data_emissao'], row['numero_nota'], row['nome_cliente'], f"{row['valor_nota']:,.2f}"))