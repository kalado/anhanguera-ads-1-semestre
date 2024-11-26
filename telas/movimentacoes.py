import tkinter as tk
from tkinter import ttk, messagebox
from banco.db_setup import db_cursor, db_connection


def abrir_tela_movimentacoes():
    def movimentar_estoque(produto_id, tipo, quantidade):
        if not produto_id or not tipo or not quantidade:
            messagebox.showerror(
                "Erro", "Por favor, preencha todos os campos.")
            return

        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError("A quantidade deve ser maior que zero.")
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        # Atualizar a quantidade no estoque
        db_cursor.execute(
            "SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
        produto = db_cursor.fetchone()
        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado.")
            return

        estoque_atual = produto[0]
        if tipo == "Saída" and estoque_atual < quantidade:
            messagebox.showerror("Erro", "Estoque insuficiente para a saída.")
            return

        nova_quantidade = estoque_atual + \
            quantidade if tipo == "Entrada" else estoque_atual - quantidade
        db_cursor.execute(
            "UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_quantidade, produto_id))

        # Registrar a movimentação
        db_cursor.execute("""
        INSERT INTO movimentacoes (produto_id, tipo, quantidade, data)
        VALUES (?, ?, ?, datetime('now'))
        """, (produto_id, tipo, quantidade))
        db_connection.commit()
        messagebox.showinfo("Sucesso", "Movimentação registrada com sucesso!")
        atualizar_tabela_movimentacoes()
        atualizar_estoque_disponivel()

    def atualizar_tabela_movimentacoes():
        for item in tabela_movimentacoes.get_children():
            tabela_movimentacoes.delete(item)
        db_cursor.execute("""
        SELECT movimentacoes.id, produtos.nome, movimentacoes.tipo, movimentacoes.quantidade, movimentacoes.data
        FROM movimentacoes
        INNER JOIN produtos ON movimentacoes.produto_id = produtos.id
        """)
        for row in db_cursor.fetchall():
            tabela_movimentacoes.insert("", "end", values=row)

    def atualizar_estoque_disponivel():
        produto_selecionado = combo_produto.get()
        if not produto_selecionado:
            label_estoque.config(text="Estoque disponível: -")
            return
        produto_id = produto_selecionado.split(" - ")[0]
        db_cursor.execute(
            "SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
        estoque = db_cursor.fetchone()
        if estoque:
            label_estoque.config(text=f"Estoque disponível: {estoque[0]}")
        else:
            label_estoque.config(text="Estoque disponível: -")

    janela = tk.Tk()
    janela.title("Movimentação de Estoque")
    janela.geometry("800x600")

    # Frame Movimentação
    frame_movimentacao = ttk.LabelFrame(janela, text="Registrar Movimentação")
    frame_movimentacao.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_movimentacao, text="Produto").grid(
        row=0, column=0, padx=5, pady=5)
    produtos = db_cursor.execute("SELECT id, nome FROM produtos").fetchall()
    combo_produto = ttk.Combobox(frame_movimentacao, values=[
                                 f"{p[0]} - {p[1]}" for p in produtos])
    combo_produto.grid(row=0, column=1, padx=5, pady=5)
    combo_produto.bind("<<ComboboxSelected>>",
                       lambda e: atualizar_estoque_disponivel())

    label_estoque = ttk.Label(frame_movimentacao, text="Estoque disponível: -")
    label_estoque.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    ttk.Label(frame_movimentacao, text="Tipo").grid(
        row=2, column=0, padx=5, pady=5)
    combo_tipo = ttk.Combobox(frame_movimentacao, values=["Entrada", "Saída"])
    combo_tipo.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_movimentacao, text="Quantidade").grid(
        row=3, column=0, padx=5, pady=5)
    entry_quantidade = ttk.Entry(frame_movimentacao)
    entry_quantidade.grid(row=3, column=1, padx=5, pady=5)

    ttk.Button(frame_movimentacao, text="Registrar Movimentação", command=lambda: movimentar_estoque(
        # Pega o ID do produto selecionado
        combo_produto.get().split(" - ")[0],
        combo_tipo.get(),
        entry_quantidade.get()
    )).grid(row=4, column=0, columnspan=2, pady=10)

    # Frame Histórico
    frame_historico = ttk.LabelFrame(janela, text="Histórico de Movimentações")
    frame_historico.pack(fill="both", expand=True, padx=10, pady=5)

    colunas = ("ID", "Produto", "Tipo", "Quantidade", "Data")
    tabela_movimentacoes = ttk.Treeview(
        frame_historico, columns=colunas, show="headings")
    for col in colunas:
        tabela_movimentacoes.heading(col, text=col)
        tabela_movimentacoes.column(col, width=150 if col != "Data" else 200)
    tabela_movimentacoes.pack(fill="both", expand=True)

    atualizar_tabela_movimentacoes()
    janela.mainloop()
