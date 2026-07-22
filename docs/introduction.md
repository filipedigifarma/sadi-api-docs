# Introdução

A **API SADI** permite que sistemas externos se integrem ao PDV Digifarma para:

- Consultar catálogo de **produtos**, com filtros de saldo, integração e ordenação
- Buscar **clientes** por CPF, nome, telefone ou código
- Cadastrar/atualizar clientes
- Registrar **vendas** finalizadas (marketplaces como iFood, Rappi) ou **pré-vendas** (delivery próprio)
- Consultar **vendas** por período, ID ou data de alteração
- Acessar dados de **fidelidade**, **recorrências** de compra, **pedidos prontos** para retirada e **promoções ativas** — usados pelo portal SADI Online

## Características

- **HTTP POST** em todas as rotas
- **Body em `form-data`** — não usa JSON no `Content-Type`, mas o payload é JSON serializado num campo chamado `json`
- **Respostas em JSON**
- **Base URL:** `https://sadi.digifarma.com.br/api/`
- **Autenticação por token** — obtido via [`GetToken`](endpoints/get-token.md) e enviado em `x-digifarma-token`

## Fluxo típico

1. Chamar [`GetToken`](endpoints/get-token.md) com o CNPJ da integradora → recebe um token
2. Usar o token em `x-digifarma-token` em todas as demais chamadas
3. Consultar os endpoints conforme a necessidade da integração
4. Renovar o token chamando `GetToken` novamente quando expirar

## Próximos passos

- Veja [Autenticação](authentication.md) para o fluxo completo do token
- Veja [Formato de requisição](request-format.md) para entender o body `form-data`
- Comece explorando os [endpoints](endpoints/)
