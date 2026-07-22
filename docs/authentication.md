# Autenticação

## ⚠️ Pré-requisitos

Antes de qualquer chamada — **inclusive `GetToken`** — você precisa de duas coisas emitidas pela Digifarma:

1. **Usuário de integração** (`x-digifarma-user`) — não existe auto-cadastro; a Digifarma cria e entrega para a sua integradora. Solicite via [contato@digifarma.com.br](mailto:contato@digifarma.com.br).
2. **Liberação dos CNPJs das lojas** — cada CNPJ de farmácia que você pretende consultar precisa estar liberado para o seu usuário. Envie a lista junto do pedido do usuário (ou depois, quando adicionar novas lojas).

Sem os dois, todas as chamadas falham. Veja detalhes em [Introdução — Pré-requisitos](introduction.md#-pré-requisitos--leia-antes).

---

## Fluxo do token

A API utiliza autenticação baseada em **token**. O fluxo é:

1. Chamar [`GetToken`](endpoints/get-token.md) enviando o CNPJ da integradora → recebe um token
2. Enviar o token no header `x-digifarma-token` em todas as demais chamadas
3. Renovar chamando `GetToken` novamente quando o token expirar

## Headers obrigatórios (exceto `GetToken` e `SetSenha`)

| Header | Descrição |
| --- | --- |
| `x-digifarma-user` | Usuário fornecido pela Digifarma |
| `x-digifarma-token` | Token obtido via [`GetToken`](endpoints/get-token.md) |

## Exemplo

Obtendo o token:

```bash
curl -X POST https://sadi.digifarma.com.br/api/GetToken \
  -H "x-digifarma-user: SEU_USUARIO" \
  -F "cnpj=02695980000110"
```

Resposta:

```json
{
  "token": "seu-token-aqui"
}
```

Usando o token numa chamada subsequente:

```bash
curl -X POST https://sadi.digifarma.com.br/api/Ping \
  -H "x-digifarma-user: SEU_USUARIO" \
  -H "x-digifarma-token: SEU_TOKEN" \
  -F 'json={"cnpj":"02695980000110","params":null}'
```

## Erros comuns

| Situação | Sintoma | Solução |
| --- | --- | --- |
| Sem `x-digifarma-user` | Erro 401 ou resposta com `"erro":"sim"` | Configurar o header em todas as chamadas |
| Token expirado | Erro de autenticação ou resposta com `"erro":"sim","msg":"..."` | Renovar via `GetToken` |
| CNPJ da loja não vinculado à integradora | Resposta com `"erro":"sim"` explicando permissão | Verificar cadastro da integradora com a Digifarma |
