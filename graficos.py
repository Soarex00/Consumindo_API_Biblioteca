import os

# evita aviso do Matplotlib
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt

import api


def gerar_grafico_emprestimos_por_livro(nome_arquivo="grafico_emprestimos_por_livro.png"):
    # busca todos os emprestimos na API antes de montar o grafico.
    emprestimos = api.listar_emprestimos()
    quantidade_por_livro = {}

    # agrupamento usando dicionario: chave = titulo do livro, valor = quantidade.
    for emprestimo in emprestimos:
        livro = emprestimo.get("livro") or {}
        titulo = livro.get("titulo", "Livro sem titulo")
        quantidade_por_livro[titulo] = quantidade_por_livro.get(titulo, 0) + 1

    if not quantidade_por_livro:
        print("Nao existem emprestimos para gerar o grafico.")
        return

    titulos = list(quantidade_por_livro.keys())
    quantidades = list(quantidade_por_livro.values())

    # matplotlib monta o grafico de barras com os dados agrupados.
    plt.figure(figsize=(10, 6))
    plt.bar(titulos, quantidades, color="#2e7d32")
    plt.title("Quantidade de emprestimos por livro")
    plt.xlabel("Livro")
    plt.ylabel("Quantidade de emprestimos")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    # salvar em arquivo ajuda quando o computador nao abre janela grafica.
    plt.savefig(nome_arquivo)
    print(f"Grafico salvo em {nome_arquivo}.")
    plt.show()
    return nome_arquivo
