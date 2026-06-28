from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table

import api
import backup
import graficos

console = Console()


def pausar():
    # pausa simples para o usuario conseguir ler o resultado antes do menu voltar.
    Prompt.ask("\nPressione Enter para continuar", default="")


def mostrar_erro(erro):
    console.print(f"[bold red]Erro:[/bold red] {erro}")


def criar_tabela(titulo, colunas):
    # table do rich deixa as listagens mais organizadas no terminal.
    tabela = Table(title=titulo)
    for coluna in colunas:
        tabela.add_column(coluna)
    return tabela


def listar_alunos_tabela():
    # a API retorna uma lista de dicionarios, um dicionario para cada aluno.
    alunos = api.listar_alunos()
    tabela = criar_tabela("Alunos", ["ID", "Nome", "E-mail", "Telefone", "Matricula"])

    if not alunos:
        console.print("[yellow]Nenhum aluno cadastrado.[/yellow]")

    for aluno in alunos:
        tabela.add_row(
            str(aluno.get("id", "")),
            aluno.get("nome", ""),
            aluno.get("email", ""),
            aluno.get("telefone", ""),
            aluno.get("matricula", ""),
        )

    console.print(tabela)
    return alunos


def listar_livros_tabela():
    # a listagem tambem reutiliza a funcao da camada api.py.
    livros = api.listar_livros()
    tabela = criar_tabela("Livros", ["ID", "Titulo", "Autor", "Editora", "Quantidade"])

    if not livros:
        console.print("[yellow]Nenhum livro cadastrado.[/yellow]")

    for livro in livros:
        tabela.add_row(
            str(livro.get("id", "")),
            livro.get("titulo", ""),
            livro.get("autor", ""),
            livro.get("editora", ""),
            str(livro.get("quantidade", "")),
        )

    console.print(tabela)
    return livros


def listar_emprestimos_tabela(emprestimos=None):
    if emprestimos is None:
        emprestimos = api.listar_emprestimos()

    tabela = criar_tabela(
        "Emprestimos",
        ["ID", "Aluno", "Livro", "Data emprestimo", "Data devolucao"],
    )

    if not emprestimos:
        console.print("[yellow]Nenhum emprestimo cadastrado.[/yellow]")

    for emprestimo in emprestimos:
        # cada emprestimo vem com os dicionarios aluno e livro dentro dele.
        aluno = emprestimo.get("aluno") or {}
        livro = emprestimo.get("livro") or {}
        data_devolucao = emprestimo.get("data_devolucao") or "Em aberto"

        tabela.add_row(
            str(emprestimo.get("id", "")),
            aluno.get("nome", ""),
            livro.get("titulo", ""),
            emprestimo.get("data_emprestimo", ""),
            data_devolucao,
        )

    console.print(tabela)
    return emprestimos


def menu_alunos():
    # loop do submenu: ele continua ate o usuario escolher voltar.
    while True:
        console.print(
            Panel(
                "1 - Cadastrar aluno\n"
                "2 - Listar alunos\n"
                "3 - Editar aluno\n"
                "4 - Excluir aluno\n"
                "0 - Voltar",
                title="CRUD de alunos",
                style="green",
            )
        )
        opcao = Prompt.ask(
            "Escolha",
            choices=["1", "2", "3", "4", "0"],
            default="0",
        )

        try:
            if opcao == "1":
                nome = Prompt.ask("Nome")
                email = Prompt.ask("E-mail")
                telefone = Prompt.ask("Telefone")
                matricula = Prompt.ask("Matricula")
                aluno = api.criar_aluno(nome, email, telefone, matricula)
                console.print(f"[green]Aluno cadastrado com ID {aluno.get('id')}.[/green]")
            elif opcao == "2":
                listar_alunos_tabela()
            elif opcao == "3":
                listar_alunos_tabela()
                aluno_id = IntPrompt.ask("ID do aluno")
                atual = api.buscar_aluno(aluno_id)
                nome = Prompt.ask("Nome", default=atual.get("nome", ""))
                email = Prompt.ask("E-mail", default=atual.get("email", ""))
                telefone = Prompt.ask("Telefone", default=atual.get("telefone", ""))
                matricula = Prompt.ask("Matricula", default=atual.get("matricula", ""))
                api.atualizar_aluno(aluno_id, nome, email, telefone, matricula)
                console.print("[green]Aluno atualizado.[/green]")
            elif opcao == "4":
                listar_alunos_tabela()
                aluno_id = IntPrompt.ask("ID do aluno")
                if Confirm.ask("Deseja excluir este aluno?"):
                    api.deletar_aluno(aluno_id)
                    console.print("[green]Aluno excluido.[/green]")
            else:
                break
        except Exception as erro:
            mostrar_erro(erro)

        pausar()


def menu_livros():
    # CRUD de livros chama somente funcoes do api.py.
    while True:
        console.print(
            Panel(
                "1 - Cadastrar livro\n"
                "2 - Listar livros\n"
                "3 - Editar livro\n"
                "4 - Excluir livro\n"
                "0 - Voltar",
                title="CRUD de livros",
                style="green",
            )
        )
        opcao = Prompt.ask(
            "Escolha",
            choices=["1", "2", "3", "4", "0"],
            default="0",
        )

        try:
            if opcao == "1":
                titulo = Prompt.ask("Titulo")
                autor = Prompt.ask("Autor")
                editora = Prompt.ask("Editora")
                quantidade = IntPrompt.ask("Quantidade")
                livro = api.criar_livro(titulo, autor, editora, quantidade)
                console.print(f"[green]Livro cadastrado com ID {livro.get('id')}.[/green]")
            elif opcao == "2":
                listar_livros_tabela()
            elif opcao == "3":
                listar_livros_tabela()
                livro_id = IntPrompt.ask("ID do livro")
                atual = api.buscar_livro(livro_id)
                titulo = Prompt.ask("Titulo", default=atual.get("titulo", ""))
                autor = Prompt.ask("Autor", default=atual.get("autor", ""))
                editora = Prompt.ask("Editora", default=atual.get("editora", ""))
                quantidade = IntPrompt.ask("Quantidade", default=atual.get("quantidade", 0))
                api.atualizar_livro(livro_id, titulo, autor, editora, quantidade)
                console.print("[green]Livro atualizado.[/green]")
            elif opcao == "4":
                listar_livros_tabela()
                livro_id = IntPrompt.ask("ID do livro")
                if Confirm.ask("Deseja excluir este livro?"):
                    api.deletar_livro(livro_id)
                    console.print("[green]Livro excluido.[/green]")
            else:
                break
        except Exception as erro:
            mostrar_erro(erro)

        pausar()


def menu_emprestimos():
    # CRUD de emprestimos mostra alunos e livros antes de pedir os IDs.
    while True:
        console.print(
            Panel(
                "1 - Listar emprestimos\n"
                "2 - Criar emprestimo\n"
                "3 - Devolver livro\n"
                "4 - Excluir emprestimo\n"
                "0 - Voltar",
                title="CRUD de emprestimos",
                style="green",
            )
        )
        opcao = Prompt.ask(
            "Escolha",
            choices=["1", "2", "3", "4", "0"],
            default="0",
        )

        try:
            if opcao == "1":
                listar_emprestimos_tabela()
            elif opcao == "2":
                # primeiro lista as opcoes disponiveis para facilitar a escolha.
                listar_alunos_tabela()
                listar_livros_tabela()
                aluno_id = IntPrompt.ask("ID do aluno")
                livro_id = IntPrompt.ask("ID do livro")
                emprestimo = api.criar_emprestimo(aluno_id, livro_id)
                console.print(f"[green]Emprestimo criado com ID {emprestimo.get('id')}.[/green]")
            elif opcao == "3":
                listar_emprestimos_tabela()
                emprestimo_id = IntPrompt.ask("ID do emprestimo")
                api.devolver_emprestimo(emprestimo_id)
                console.print("[green]Livro devolvido.[/green]")
            elif opcao == "4":
                listar_emprestimos_tabela()
                emprestimo_id = IntPrompt.ask("ID do emprestimo")
                if Confirm.ask("Deseja excluir este emprestimo?"):
                    api.deletar_emprestimo(emprestimo_id)
                    console.print("[green]Emprestimo excluido.[/green]")
            else:
                break
        except Exception as erro:
            mostrar_erro(erro)

        pausar()


def pesquisa_avancada():
    try:
        nome_aluno = Prompt.ask("Digite parte do nome do aluno", default="").lower()
        titulo_livro = Prompt.ask("Digite parte do titulo do livro", default="").lower()
        emprestimos = api.listar_emprestimos()
        filtrados = []

        # filtragem usando lista e dicionarios recebidos da API.
        # o lower() faz a pesquisa ignorar maiusculas e minusculas.
        for emprestimo in emprestimos:
            aluno = emprestimo.get("aluno") or {}
            livro = emprestimo.get("livro") or {}
            nome = aluno.get("nome", "").lower()
            titulo = livro.get("titulo", "").lower()

            if nome_aluno in nome and titulo_livro in titulo:
                filtrados.append(emprestimo)

        listar_emprestimos_tabela(filtrados)
        console.print(f"[green]{len(filtrados)} emprestimo(s) encontrado(s).[/green]")
    except Exception as erro:
        mostrar_erro(erro)

    pausar()


def gerar_grafico():
    try:
        graficos.gerar_grafico_emprestimos_por_livro()
    except Exception as erro:
        mostrar_erro(erro)
    pausar()


def gerar_backup():
    try:
        arquivo = backup.gerar_backup_emprestimos()
        console.print(f"[green]Backup gerado em {arquivo}.[/green]")
    except Exception as erro:
        mostrar_erro(erro)
    pausar()


def mostrar_instrucao_web():
    console.print(
        Panel(
            "Para abrir a pagina web, execute em outro terminal:\n\n"
            "python web.py\n\n"
            "Depois acesse: http://localhost:5000",
            title="Pagina web",
            style="cyan",
        )
    )
    pausar()


def mostrar_menu_principal():
    console.print(
        Panel(
            "[bold]Sistema Python da Biblioteca[/bold]\n"
            "1 - CRUD de alunos\n"
            "2 - CRUD de livros\n"
            "3 - CRUD de emprestimos\n"
            "4 - Pesquisa avancada\n"
            "5 - Gerar grafico\n"
            "6 - Gerar backup CSV\n"
            "7 - Abrir instrucao da pagina web\n"
            "0 - Sair",
            style="bold green",
        )
    )


def main():
    # menu principal: direciona o usuario para cada funcionalidade do trabalho.
    while True:
        mostrar_menu_principal()
        opcao = Prompt.ask(
            "Escolha uma opcao",
            choices=["1", "2", "3", "4", "5", "6", "7", "0"],
            default="0",
        )

        if opcao == "1":
            menu_alunos()
        elif opcao == "2":
            menu_livros()
        elif opcao == "3":
            menu_emprestimos()
        elif opcao == "4":
            pesquisa_avancada()
        elif opcao == "5":
            gerar_grafico()
        elif opcao == "6":
            gerar_backup()
        elif opcao == "7":
            mostrar_instrucao_web()
        else:
            console.print("[bold green]Programa encerrado.[/bold green]")
            break


if __name__ == "__main__":
    main()
