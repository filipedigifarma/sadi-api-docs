---
title: "Introdução"
description: "Visão geral da API SADI e pré-requisitos de integração"
---

## Pré-requisitos — leia antes

**Duas coisas precisam estar em ordem antes de você conseguir chamar qualquer rota.** Ambas são solicitadas junto à Digifarma pelo email [filipe@digifarma.com.br](mailto:filipe@digifarma.com.br) — informe o nome da sua integradora, contato técnico e a lista de CNPJs que pretende atender.

### 1. Usuário de integração (`x-digifarma-user`)

O valor do header `x-digifarma-user` **precisa ter sido emitido pela Digifarma**. Não existe auto-cadastro — a Digifarma cria e entrega esse usuário à sua integradora. Sem ele **nenhuma rota funciona**, nem mesmo o [`GetToken`](endpoints/get-token.md).

### 2. Liberação dos CNPJs das lojas

Ter o usuário **não é suficiente**. Cada **CNPJ de farmácia** que sua integradora pretende consultar precisa estar **explicitamente liberado** para o seu usuário na base da Digifarma. Sem essa liberação, o `GetToken` falha para aquela loja e nenhuma outra rota responde.

Envie a lista de CNPJs junto do pedido do usuário (ou depois, pelo mesmo canal) sempre que adicionar uma loja nova à sua base.

---

## O que a API faz

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
