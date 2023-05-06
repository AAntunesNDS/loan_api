
<h1 align="center">Loan Api </h1>

<p align="center">Uma API de empréstimo para usuários</p>

## Descrição do projeto

Esse projeto é uma proposta de API para uma aplicação que permite usuários a tomarem empréstimos financeiros. (Até aqui os valores são dummies, não existe uma integração com nenhum serviço financeiro) 
É um projeto web Python que utiliza Django e Django Rest Framework como ferramentas principais.


## Pré-requisitos

Para rodar o projeto é preciso ter instalado em sua máquina as seguintes ferramentas:

* [Git](https:/git-scm.com) 

* [Python 3.8](https://www.python.org/downloads/release/python-380/) 

* [Poetry](https://python-poetry.org/)

* [Docker](https://docs.docker.com/engine/install/) 

* [Docker-Compose](https://www.digitalocean.com/community/tutorial_collections/how-to-install-docker-compose).

Também será necessária a instalção global libpq-dev para as permissões necessárias do Postgres:

```bash
sudo apt install python3-dev libpq-dev
```

### Setup Inicial

```bash
# Clone este repositório
$ git clone https://github.com/AAntunesNDS/loan_api.git

# Crie uma instância postgres com docker-compose (se você já tiver um postgres na porta 5432 pode dar conflito. Se certifique que não tem)
$ make build_database

# Agora rode essa instancia
$ make run_database

# Instala as dependências da API 
$ make build_api

```

Nesse momento, crie um arquivo .env na raiz do projeto e coloque as seguintes envs: (Pode personalizar, só precisa alterar também no yml do database)

```env
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=example
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

A partir daqui, com a venv do Poetry ativada, voce já pode utilizar os comandos padrões do Django para criar um superusuario, realizar migrações de banco, rodar os testes unitários, e por fim, rodar o servidor.


## Instruções adicionais

Todos os endpoints estão pedindo autenticação JWT, então mesmo que você consiga ver a documentação e a interface da API em http://localhost:8000/, você precisará antes criar um Token de Autenticação.

Faça uma requisição na rota http://127.0.0.1:8000/api/token/ e passe as credenciais do seu super usuario com seguinte json:

```json
{
	"username":"example",
	"password":"example"
}
```

Pode usar insomnia ou postmanpara isso. O resultado vai ser 2 tokens, o token de acesso e um token de Refresh. O primeiro vai ser usado no header das demais requisições com um parametro Authorization e com valor do token dessa forma: 

```
Bearer f'{token}' 
```


Caso seu token expire, acesse a rota http://127.0.0.1:8000/api/token/refresh/ com o seguinte json:

```json
{
	"refresh":"token_refresh_example"
}
```

com isso, vai ser gerado um novo token.


## Visão de usuários

Para conseguir testar a visão de usuários, pode ser utilizado o admin. Lá, com seu superusuario, crie um grupo de usuários com 2 tipos de permissão:

```
api_loans | emprestimo | can view emprestimo
api_loans | emprestimo | can view pagamento
```

E depois crie um novo usuario, e atribua esse grupo de usuario a ele. Para conseguir visualizar os emprestimos e pagamentos desse usuario, também marque a opção de staff na criação desse usuario. 

Quando logar com ele, voce conseguirá ver os emprestimos e pagamentos vinculados a ele. Dessa forma, apenas o superusuario vai ser capaz de inputar novos emprestimos e pagamentos, e cada usuario criado nesse grupo podera apenas visualizar.


## Cenário de Teste

Com super usuário logado crie um emprestimo, para um usuario previamente cadastrado, com uma data de "2022-01-01" e não realize nenhum pagamento vinculado. 

Voce pode nesse momento consultar o saldo devedor (com juros compostos) através do endpoint:

```
http://127.0.0.1:8000/loans/{id-do-emprestimo}/saldo-devedor
```

Lembre de colocar o Authorization no header e um token válido.

Nos testes unitários tem mais cenário de exemplo.


## Observações finais

Alguns pontos de melhoria para o projeto atual:

- Adicionar CI com githubactions seria o próximo passo
- Refatorar a action de saldo-devedor utilizando signals para realizar automaticamente o calculo de saldo devedor no momento que é criado um pagamento pra um empréstimo



