# Autenticação

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
