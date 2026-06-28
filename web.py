from flask import Flask
from html import escape

import api

app = Flask(__name__)


@app.route("/")
def pagina_inicial():
    try:
        # a pagina web usa a mesma camada api.py do menu.
        emprestimos = api.listar_emprestimos()
    except Exception as erro:
        return f"<h1>Erro ao carregar emprestimos</h1><p>{erro}</p>"

    linhas = ""
    for emprestimo in emprestimos:
        # monta uma linha HTML para cada emprestimo retornado pela API.
        aluno = emprestimo.get("aluno") or {}
        livro = emprestimo.get("livro") or {}
        data_devolucao = emprestimo.get("data_devolucao") or "Em aberto"

        # escape evita que textos vindos da API sejam interpretados como HTML.
        linhas += f"""
        <tr>
            <td>{escape(str(emprestimo.get("id", "")))}</td>
            <td>{escape(aluno.get("nome", ""))}</td>
            <td>{escape(livro.get("titulo", ""))}</td>
            <td>{escape(emprestimo.get("data_emprestimo", ""))}</td>
            <td>{escape(data_devolucao)}</td>
        </tr>
        """

    if not linhas:
        linhas = """
        <tr>
            <td colspan="5">Nenhum emprestimo cadastrado.</td>
        </tr>
        """

    return f"""
    <!doctype html>
    <html lang="pt-br">
    <head>
        <meta charset="utf-8">
        <title>Emprestimos da Biblioteca</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background: #f5f5f5;
            }}
            h1 {{
                color: #1b5e20;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
            }}
            th, td {{
                border: 1px solid #dddddd;
                padding: 10px;
                text-align: left;
            }}
            th {{
                background: #2e7d32;
                color: white;
            }}
        </style>
    </head>
    <body>
        <h1>Emprestimos da Biblioteca</h1>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Aluno</th>
                    <th>Livro</th>
                    <th>Data do emprestimo</th>
                    <th>Data da devolucao</th>
                </tr>
            </thead>
            <tbody>
                {linhas}
            </tbody>
        </table>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True, port=5000)
