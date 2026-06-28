import requests

# endereco da API Node/Express que ja existe no outro projeto.
BASE_URL = "http://localhost:3000"


def converter_inteiro(valor, nome_campo):
    # garante que IDs e quantidades sejam numeros inteiros validos.
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        raise Exception(f"{nome_campo} precisa ser um numero inteiro.")

    if numero <= 0:
        raise Exception(f"{nome_campo} precisa ser maior que zero.")

    return numero


def tratar_resposta(resposta):
    # converte a resposta da API em dados Python ou mostra o erro recebido.
    try:
        dados = resposta.json()
    except ValueError:
        dados = {}

    if resposta.status_code >= 400:
        mensagem = dados.get("erro") or dados.get("message") or "Erro ao acessar a API."
        raise Exception(mensagem)

    return dados


def requisicao(metodo, caminho, dados=None):
    # funcao central: todas as chamadas HTTP passam por aqui.
    url = f"{BASE_URL}{caminho}"

    try:
        # requests envia a requisicao para a API e recebe a resposta em JSON.
        resposta = requests.request(metodo, url, json=dados, timeout=10)
        return tratar_resposta(resposta)
    except requests.exceptions.ConnectionError:
        raise Exception("Nao foi possivel conectar na API. Rode a API Node em http://localhost:3000.")
    except requests.exceptions.Timeout:
        raise Exception("A API demorou para responder.")


def listar_alunos():
    return requisicao("GET", "/alunos")


def buscar_aluno(aluno_id):
    return requisicao("GET", f"/alunos/{aluno_id}")


def criar_aluno(nome, email, telefone, matricula):
    # dicionario que sera enviado para a API como JSON.
    dados = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "matricula": matricula,
    }
    return requisicao("POST", "/alunos", dados)


def atualizar_aluno(aluno_id, nome, email, telefone, matricula):
    # a API espera todos os campos principais do aluno no PUT.
    dados = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "matricula": matricula,
    }
    return requisicao("PUT", f"/alunos/{aluno_id}", dados)


def deletar_aluno(aluno_id):
    return requisicao("DELETE", f"/alunos/{aluno_id}")


def listar_livros():
    return requisicao("GET", "/livros")


def buscar_livro(livro_id):
    return requisicao("GET", f"/livros/{livro_id}")


def criar_livro(titulo, autor, editora, quantidade):
    quantidade = converter_inteiro(quantidade, "Quantidade")
    # o campo quantidade precisa ir como numero para a API.
    dados = {
        "titulo": titulo,
        "autor": autor,
        "editora": editora,
        "quantidade": quantidade,
    }
    return requisicao("POST", "/livros", dados)


def atualizar_livro(livro_id, titulo, autor, editora, quantidade):
    quantidade = converter_inteiro(quantidade, "Quantidade")
    dados = {
        "titulo": titulo,
        "autor": autor,
        "editora": editora,
        "quantidade": quantidade,
    }
    return requisicao("PUT", f"/livros/{livro_id}", dados)


def deletar_livro(livro_id):
    return requisicao("DELETE", f"/livros/{livro_id}")


def listar_emprestimos():
    return requisicao("GET", "/emprestimos")


def criar_emprestimo(aluno_id, livro_id):
    aluno_id = converter_inteiro(aluno_id, "ID do aluno")
    livro_id = converter_inteiro(livro_id, "ID do livro")
    # a API cria o emprestimo usando apenas os IDs do aluno e do livro.
    dados = {
        "alunoId": aluno_id,
        "livroId": livro_id,
    }
    return requisicao("POST", "/emprestimos", dados)


def devolver_emprestimo(emprestimo_id):
    return requisicao("PUT", f"/emprestimos/{emprestimo_id}/devolucao")


def deletar_emprestimo(emprestimo_id):
    return requisicao("DELETE", f"/emprestimos/{emprestimo_id}")
