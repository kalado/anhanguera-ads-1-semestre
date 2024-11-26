import tkinter as tk
from tkinter import ttk, messagebox
from banco.db_setup import db_cursor, db_connection


def abrir_tela_produtos():
    def cadastrar_produto(nome, categoria_id, quantidade, preco, localizacao):
        if not nome or not quantidade or not preco:
            messagebox.showerror(
                "Erro", "Por favor, preencha os campos obrigatórios.")
            return

        db_cursor.execute("""
        INSERT INTO produtos (nome, categoria_id, quantidade, preco, localizacao)
        VALUES (?, ?, ?, ?, ?)
        """, (nome, categoria_id, quantidade, preco, localizacao))
        db_connection.commit()
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        atualizar_tabela()

    def atualizar_tabela():
        for item in tabela.get_children():
            tabela.delete(item)
        db_cursor.execute("""
        SELECT produtos.id, produtos.nome, categorias.nome, produtos.quantidade, produtos.preco, produtos.localizacao
        FROM produtos
        LEFT JOIN categorias ON produtos.categoria_id = categorias.id
        """)
        for row in db_cursor.fetchall():
            tabela.insert("", "end", values=row)

    def atualizar_registro():
        selected_item = tabela.selection()
        if not selected_item:
            messagebox.showerror(
                "Erro", "Selecione um registro para atualizar.")
            return

        item = tabela.item(selected_item)["values"]
        produto_id = item[0]

        # Exemplo de atualização, pode ser adaptado
        novo_nome = entry_nome.get()
        if not novo_nome:
            messagebox.showerror("Erro", "Por favor, insira um novo nome.")
            return

        db_cursor.execute("""
        UPDATE produtos SET nome = ? WHERE id = ?
        """, (novo_nome, produto_id))
        db_connection.commit()
        messagebox.showinfo("Sucesso", "Registro atualizado com sucesso!")
        atualizar_tabela()

    def deletar_registro():
        selected_item = tabela.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione um registro para deletar.")
            return

        item = tabela.item(selected_item)["values"]
        produto_id = item[0]

        resposta = messagebox.askyesno(
            "Confirmação", "Tem certeza que deseja deletar este registro?")
        if resposta:
            db_cursor.execute("""
            DELETE FROM produtos WHERE id = ?
            """, (produto_id,))
            db_connection.commit()
            messagebox.showinfo("Sucesso", "Registro deletado com sucesso!")
            atualizar_tabela()

    janela = tk.Tk()
    janela.title("Cadastro de Produtos")
    janela.geometry("800x600")

    # Frame Cadastro
    frame_cadastro = ttk.LabelFrame(janela, text="Cadastro de Produtos")
    frame_cadastro.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_cadastro, text="Nome").grid(
        row=0, column=0, padx=5, pady=5)
    entry_nome = ttk.Entry(frame_cadastro)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_cadastro, text="Categoria").grid(
        row=1, column=0, padx=5, pady=5)
    categorias = [("", "Selecione")] + \
        db_cursor.execute("SELECT id, nome FROM categorias").fetchall()
    combo_categoria = ttk.Combobox(frame_cadastro, values=[
                                   cat[1] for cat in categorias])
    combo_categoria.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_cadastro, text="Quantidade").grid(
        row=2, column=0, padx=5, pady=5)
    entry_quantidade = ttk.Entry(frame_cadastro)
    entry_quantidade.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_cadastro, text="Preço").grid(
        row=3, column=0, padx=5, pady=5)
    entry_preco = ttk.Entry(frame_cadastro)
    entry_preco.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame_cadastro, text="Localização").grid(
        row=4, column=0, padx=5, pady=5)
    entry_localizacao = ttk.Entry(frame_cadastro)
    entry_localizacao.grid(row=4, column=1, padx=5, pady=5)

    ttk.Button(frame_cadastro, text="Cadastrar Produto", command=lambda: cadastrar_produto(
        entry_nome.get(),
        categorias[combo_categoria.current()][0],
        entry_quantidade.get(),
        entry_preco.get(),
        entry_localizacao.get()
    )).grid(row=5, column=0, columnspan=2, pady=10)

    # Frame Tabela
    frame_tabela = ttk.LabelFrame(janela, text="Estoque Atual")
    frame_tabela.pack(fill="both", expand=True, padx=10, pady=5)

    colunas = ("ID", "Nome", "Categoria", "Quantidade", "Preço", "Localização")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=100)

    # Scrollbar
    scrollbar = ttk.Scrollbar(
        frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabela.pack(fill="both", expand=True)

    # Botões de Atualizar e Deletar
    ttk.Button(janela, text="Atualizar Registro", command=atualizar_registro).pack(
        side="left", padx=10, pady=5)
    ttk.Button(janela, text="Deletar Registro", command=deletar_registro).pack(
        side="right", padx=10, pady=5)

    atualizar_tabela()
    janela.mainloop()
