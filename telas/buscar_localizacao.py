import tkinter as tk
from tkinter import ttk, messagebox
from banco.db_setup import db_cursor


def buscar_localizacao_produto():
    def buscar():
        produto_id = entry_id.get()
        if not produto_id:
            messagebox.showerror("Erro", "Por favor, insira o ID do produto.")
            return

        try:
            produto_id = int(produto_id)
        except ValueError:
            messagebox.showerror("Erro", "O ID do produto deve ser um número.")
            return

        # Consulta ao banco para buscar a localização pelo ID
        db_cursor.execute("""
        SELECT nome, localizacao FROM produtos WHERE id = ?
        """, (produto_id,))
        resultado = db_cursor.fetchone()

        if not resultado:
            messagebox.showinfo("Resultado", "Produto não encontrado.")
        else:
            nome, localizacao = resultado
            messagebox.showinfo(
                "Localização do Produto",
                f"Produto: {nome}\nLocalização: {localizacao}"
            )

    # Interface gráfica
    janela_busca = tk.Tk()
    janela_busca.title("Buscar Localização do Produto")
    janela_busca.geometry("400x200")

    frame_busca = ttk.LabelFrame(janela_busca, text="Buscar Localização")
    frame_busca.pack(fill="both", expand=True, padx=10, pady=10)

    ttk.Label(frame_busca, text="ID do Produto").grid(
        row=0, column=0, padx=5, pady=5)
    entry_id = ttk.Entry(frame_busca)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    ttk.Button(frame_busca, text="Buscar", command=buscar).grid(
        row=1, column=0, columnspan=2, pady=10
    )

    janela_busca.mainloop()


if __name__ == "__main__":
    buscar_localizacao_produto()
