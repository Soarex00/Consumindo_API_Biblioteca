# Trabalho Python Biblioteca

Projeto em Python para consumir a API de biblioteca do repositorio `Soarex00/API_BIBLIOTECA`.

O objetivo do trabalho e demonstrar manipulacao de dados vindos de uma API usando Python, listas, dicionarios, CRUD, pesquisa, grafico, backup CSV e uma pagina web simples.

## Estrutura de pastas

```text
trabalho-python-biblioteca/
├── main.py
├── web.py
├── api.py
├── graficos.py
├── backup.py
├── requirements.txt
└── README.md
```

- `main.py`: menu principal no terminal usando `rich`.
- `api.py`: funcoes que fazem as chamadas HTTP para a API Node.
- `graficos.py`: gera grafico de barras dos emprestimos por livro.
- `backup.py`: gera o arquivo CSV dos emprestimos.
- `web.py`: pagina Flask com tabela HTML dos emprestimos.
- `requirements.txt`: dependencias do projeto Python.

## API reutilizada

Este projeto nao altera a regra de negocio da API existente. Ele apenas consome as rotas da API Node.js, Express e Prisma:

- `GET /alunos`
- `GET /alunos/:id`
- `POST /alunos`
- `PUT /alunos/:id`
- `DELETE /alunos/:id`
- `GET /livros`
- `GET /livros/:id`
- `POST /livros`
- `PUT /livros/:id`
- `DELETE /livros/:id`
- `GET /emprestimos`
- `POST /emprestimos`
- `PUT /emprestimos/:id/devolucao`
- `DELETE /emprestimos/:id`

A URL base usada pelo Python e:

```bash
http://localhost:3000
```

## Como rodar a API original

Entre na pasta da API Node:

```bash
cd "/home/conradosoares/Documentos/Trabalho API Banco/API_BIBLIOTECA"
npm install
npx prisma generate
npm run dev
```

A API precisa ficar rodando em:

```bash
http://localhost:3000
```

Se a API reclamar de `DATABASE_URL`, confira se existe um arquivo `.env` na pasta `API_BIBLIOTECA` com a conexao do banco. Neste ambiente local foi usado:

```text
DATABASE_URL="mysql://conrado:123456@localhost:3306/biblioteca"
```

## Como instalar o projeto Python

Em outro terminal, entre na pasta do projeto:

```bash
cd "/home/conradosoares/Documentos/Trabalho API Banco/trabalho-python-biblioteca"
python -m venv venv
source venv/bin/activate
```

No Windows:

```bash
venv\Scripts\activate
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

## Como rodar o menu

```bash
python main.py
```

O menu possui:

```text
1 - CRUD de alunos
2 - CRUD de livros
3 - CRUD de emprestimos
4 - Pesquisa avancada
5 - Gerar grafico
6 - Gerar backup CSV
7 - Abrir instrucao da pagina web
0 - Sair
```

## Como testar cada funcionalidade

Antes dos testes, deixe a API Node rodando em `http://localhost:3000`.

### Testar conexao com a API

```bash
python -c "import api; print(api.listar_alunos()); print(api.listar_livros()); print(api.listar_emprestimos())"
```

### Testar CRUD de alunos

No menu, escolha:

```text
1 - CRUD de alunos
```

Depois teste cadastrar, listar, editar e excluir aluno.

### Testar CRUD de livros

No menu, escolha:

```text
2 - CRUD de livros
```

Depois teste cadastrar, listar, editar e excluir livro.

### Testar CRUD de emprestimos

No menu, escolha:

```text
3 - CRUD de emprestimos
```

Na criacao de emprestimo, o sistema lista alunos e livros antes de pedir os IDs. Depois teste listar, criar, devolver livro e excluir emprestimo.

### Testar pesquisa avancada

No menu, escolha:

```text
4 - Pesquisa avancada
```

Digite parte do nome do aluno e parte do titulo do livro. A busca ignora diferenca entre letras maiusculas e minusculas.

## Como gerar o grafico

Rode o menu:

```bash
python main.py
```

Escolha a opcao:

```text
5 - Gerar grafico
```

O grafico de barras compara a quantidade de emprestimos por livro. A logica busca os emprestimos na API e agrupa os dados por titulo do livro usando um dicionario.

O arquivo tambem e salvo como:

```text
grafico_emprestimos_por_livro.png
```

## Como gerar o backup CSV

Rode o menu:

```bash
python main.py
```

Escolha a opcao:

```text
6 - Gerar backup CSV
```

O arquivo criado sera:

```text
backup_emprestimos.csv
```

Colunas do CSV:

- `id`
- `aluno`
- `livro`
- `data_emprestimo`
- `data_devolucao`

## Como abrir a pagina web

Com a API Node rodando, execute:

```bash
python web.py
```

Abra no navegador:

```bash
http://localhost:5000
```

A pagina mostra uma tabela HTML simples com os emprestimos, nome do aluno, titulo do livro, data do emprestimo e data da devolucao.

Se a API estiver desligada, a pagina mostra uma mensagem avisando para rodar a API em `http://localhost:3000`.

## Estruturas de dados usadas

- Listas: usadas para armazenar os registros recebidos da API, como lista de alunos, livros e emprestimos.
- Dicionarios: cada registro JSON recebido da API vira um dicionario em Python.
- Agrupamento: em `graficos.py`, um dicionario acumula a quantidade de emprestimos por titulo de livro.
- CSV: em `backup.py`, a biblioteca `csv` cria o arquivo `backup_emprestimos.csv` com os dados principais dos emprestimos.

## Checklist de Testes

- [x] API sobe na porta 3000
- [x] Rotas `GET /alunos`, `GET /livros` e `GET /emprestimos` respondem
- [x] Python conecta na API
- [x] Arquivos Python compilam sem erro de sintaxe
- [x] CRUD de alunos funcionando
- [x] CRUD de livros funcionando
- [x] CRUD de emprestimos funcionando
- [x] Pesquisa avancada funcionando
- [x] Grafico gerado em `grafico_emprestimos_por_livro.png`
- [x] Backup CSV gerado em `backup_emprestimos.csv`
- [x] Backup CSV vazio gera pelo menos o cabecalho
- [x] Pagina Flask funcionando
- [x] Pagina Flask mostra erro amigavel quando a API esta desligada

## Requisitos atendidos

- Projeto Python separado chamado `trabalho-python-biblioteca`.
- Consumo da API existente `Soarex00/API_BIBLIOTECA`.
- Arquivo `api.py` centralizando chamadas HTTP com `requests`.
- CRUD de alunos consumindo a API.
- CRUD de livros consumindo a API.
- CRUD de emprestimos consumindo a API.
- Criacao de emprestimo listando alunos e livros antes da escolha dos IDs.
- Pesquisa avancada de emprestimos por nome do aluno e titulo do livro.
- Uso de listas e dicionarios para filtrar e agrupar dados.
- Grafico de barras com `matplotlib`.
- Pagina web com Flask em `web.py`.
- Backup CSV da tabela principal `Emprestimo`.
- Menu no terminal com `rich`.
- Codigo simples, comentado nas partes principais e com nomes em portugues.
