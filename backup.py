import csv

import api


def gerar_backup_emprestimos(nome_arquivo="backup_emprestimos.csv"):
    # a tabela principal do trabalho e emprestimo.
    emprestimos = api.listar_emprestimos()

    # newline="" evita linhas em branco extras no CSV.
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as arquivo:
        colunas = ["id", "aluno", "livro", "data_emprestimo", "data_devolucao"]
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()

        for emprestimo in emprestimos:
            # aluno e livro sao dicionarios internos dentro do emprestimo.
            aluno = emprestimo.get("aluno") or {}
            livro = emprestimo.get("livro") or {}

            escritor.writerow(
                {
                    "id": emprestimo.get("id"),
                    "aluno": aluno.get("nome", ""),
                    "livro": livro.get("titulo", ""),
                    "data_emprestimo": emprestimo.get("data_emprestimo", ""),
                    "data_devolucao": emprestimo.get("data_devolucao") or "",
                }
            )

    return nome_arquivo
