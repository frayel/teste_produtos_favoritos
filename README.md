# Teste Backend Rest

Este teste consiste em um backend REST para gerenciar um cadastro de clientes e 
seus produtos favoritos.

## Documentação da API
http://localhost:8000/swagger/

## Tecnologias
    Python
    Django
    Docker
    Postgresql

## Estrutura
```
├─── api                
│    ├─── dto          Objetos para transferencia de dados entre camadas
│    ├─── exceptions   Classe de exceções customizadas
│    ├─── models       Entidades de dados relacionais (database models)
│    ├─── repository   Camada de persistência
│    ├─── service      Camada de serviço  
│    ├─── tests        Testes automatizados
│    └─── views        Camada de exposição dos serviços (endpoints)
└─── customer         
     ├─── settings.py      Arquivo de configuração
```    

## Setup

### Para criar e executar os containers:
```bash
$> docker-compose up --build
``` 
### Para executar um script que cria 20 clientes e adiciona produto a sua lista
```bash
$> python teste_api.py
``` 

## Ambiente de Desenvolvimento 
Para rodar o ambiente de desenvolvimento localmente:
```bash
$> cd app_customer
$> python manage.py migrate
$> python manage.py loaddata initial_data
$> python manage.py runserver 8000
```
Para rodar os testes unitarios
```bash
$> python manage.py test
```
## Banco de dados
```
ip: 127.0.0.1:5432
db: postgres
username: postgres
password: pg123
```  

## Realizando chamadas

### Autenticação
Para autenticar nas apis deve-se usar o modo Basic (username: admin, password: teste123)  

### Exemplo: Cadastrando um cliente
```
POST http://localhost:8000/app/customer/

HEADER 
content-type: application/json
authorization: Basic YWRtaW46dGVzdGUxMjM=
    
BODY
{
    "name": "Felipe Rayel",
    "email": "felipe.rayel@gmail.com"
}
```


### Exemplo: Adicionando produto à lista do cliente
```
POST http://localhost:8000/app/customer/<ID_DO_CLIENTE>/favorite/

HEADER 
content-type: application/json
authorization: Basic YWRtaW46dGVzdGUxMjM=
    
BODY
{
    "product": "79b1c283-00ef-6b22-1c8d-b0721999e2f0",
}
```

### Exemplo: Recuperando a lista de produtos favoritos
```
GET http://localhost:8000/app/customer/<ID_DO_CLIENTE>/favorite/

HEADER 
content-type: application/json
authorization: Basic YWRtaW46dGVzdGUxMjM=

```