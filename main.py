from telas.categorias import abrir_tela_categorias
from telas.movimentacoes import abrir_tela_movimentacoes
from telas.produtos import abrir_tela_produtos
from telas.relatorio_estoque import gerar_relatorio_produtos_com_baixo_estoque
from telas.buscar_localizacao import buscar_localizacao_produto


def main():
    import tkinter as tk
    app = tk.Tk()
    app.title("Sistema de Estoque")
    app.geometry("300x250")

    tk.Button(app, text="Gerenciar Produtos",
              command=abrir_tela_produtos).pack(pady=10)
    tk.Button(app, text="Gerenciar Categorias",
              command=abrir_tela_categorias).pack(pady=10)
    tk.Button(app, text="Movimentar Estoque",
              command=abrir_tela_movimentacoes).pack(pady=10)
    tk.Button(app, text="Relatório de Estoque Baixo",
              command=gerar_relatorio_produtos_com_baixo_estoque).pack(pady=10)
    tk.Button(app, text="Localizar Produto",
              command=buscar_localizacao_produto).pack(pady=10)

    app.mainloop()


if __name__ == "__main__":
    main()
