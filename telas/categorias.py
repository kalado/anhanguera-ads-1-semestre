import tkinter as tk
from tkinter import ttk, messagebox
from banco.db_setup import db_cursor, db_connection


def abrir_tela_categorias():
    def cadastrar_categoria(nome):
        if not nome:
            messagebox.showerror(
                "Erro", "Por favor, preencha o nome da categoria.")
            return

        db_cursor.execute("""
        INSERT INTO categorias (nome)
        VALUES (?)
        """, (nome,))
        db_connection.commit()
        messagebox.showinfo("Sucesso", "Categoria cadastrada com sucesso!")
        atualizar_tabela()

    def atualizar_tabela():
        for item in tabela.get_children():
            tabela.delete(item)
        db_cursor.execute("SELECT * FROM categorias")
        for row in db_cursor.fetchall():
            tabela.insert("", "end", values=row)

    def deletar_categoria():
        selected_item = tabela.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione uma categoria.")
            return

        item = tabela.item(selected_item)
        categoria_id = item["values"][0]

        db_cursor.execute(
            "DELETE FROM categorias WHERE id = ?", (categoria_id,))
        db_connection.commit()
        messagebox.showinfo("Sucesso", "Categoria deletada com sucesso!")
        atualizar_tabela()

    def atualizar_categoria():
        selected_item = tabela.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Por favor, selecione uma categoria.")
            return

        item = tabela.item(selected_item)
        categoria_id = item["values"][0]
        novo_nome = entry_nome.get()

        if not novo_nome:
            messagebox.showerror(
                "Erro", "Por favor, preencha o novo nome da categoria.")
            return

        db_cursor.execute(
            "UPDATE categorias SET nome = ? WHERE id = ?", (novo_nome, categoria_id))
        db_connection.commit()
        messagebox.showinfo("Sucesso", "Categoria atualizada com sucesso!")
        atualizar_tabela()

    janela = tk.Tk()
    janela.title("Cadastro de Categorias")
    janela.geometry("500x400")  # Ajusta o tamanho inicial da janela

    # Frame Cadastro
    frame_cadastro = ttk.LabelFrame(janela, text="Cadastro de Categorias")
    frame_cadastro.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_cadastro, text="Nome").grid(
        row=0, column=0, padx=5, pady=5, sticky="w")
    entry_nome = ttk.Entry(frame_cadastro)
    entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Button(frame_cadastro, text="Cadastrar Categoria", command=lambda: cadastrar_categoria(
        entry_nome.get()
    )).grid(row=1, column=0, columnspan=2, pady=10)

    # Tornar o campo de entrada expansível
    frame_cadastro.columnconfigure(1, weight=1)

    # Frame Tabela
    frame_tabela = ttk.LabelFrame(janela, text="Categorias")
    frame_tabela.pack(fill="both", expand=True, padx=10, pady=5)

    colunas = ("ID", "Nome")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=150)

    # Adiciona barra de rolagem
    scroll_y = ttk.Scrollbar(
        frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    tabela.pack(fill="both", expand=True)

    # Frame Ações
    frame_acoes = ttk.Frame(janela)
    frame_acoes.pack(fill="x", padx=10, pady=5)

    ttk.Button(frame_acoes, text="Deletar Categoria",
               command=deletar_categoria).pack(side="left", padx=5)
    ttk.Button(frame_acoes, text="Atualizar Categoria",
               command=atualizar_categoria).pack(side="left", padx=5)

    atualizar_tabela()
    janela.mainloop()
