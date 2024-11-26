import tkinter as tk
from tkinter import ttk, messagebox
from banco.db_setup import db_cursor


def gerar_relatorio_produtos_com_baixo_estoque():
    # Consulta para obter produtos com estoque menor que 5
    db_cursor.execute("""
    SELECT produtos.id, produtos.nome, categorias.nome, produtos.quantidade, produtos.preco, produtos.localizacao
    FROM produtos
    LEFT JOIN categorias ON produtos.categoria_id = categorias.id
    WHERE produtos.quantidade < 5
    """)
    produtos_baixo_estoque = db_cursor.fetchall()

    if not produtos_baixo_estoque:
        messagebox.showinfo(
            "Relatório", "Nenhum produto com estoque abaixo de 5.")
        return

    # Criação da janela do relatório
    janela_relatorio = tk.Tk()
    janela_relatorio.title("Relatório: Produtos com Baixo Estoque")
    janela_relatorio.geometry("800x400")

    frame_relatorio = ttk.LabelFrame(
        janela_relatorio, text="Produtos com Estoque Baixo")
    frame_relatorio.pack(fill="both", expand=True, padx=10, pady=5)

    colunas = ("ID", "Nome", "Categoria", "Quantidade", "Preço", "Localização")
    tabela = ttk.Treeview(frame_relatorio, columns=colunas, show="headings")
    for col in colunas:
        tabela.heading(col, text=col)
        tabela.column(col, width=100)

    # Scrollbar
    scrollbar = ttk.Scrollbar(
        frame_relatorio, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tabela.pack(fill="both", expand=True)

    # Preenchendo a tabela com os dados
    for produto in produtos_baixo_estoque:
        tabela.insert("", "end", values=produto)

    janela_relatorio.mainloop()


if __name__ == "__main__":
    gerar_relatorio_produtos_com_baixo_estoque()
