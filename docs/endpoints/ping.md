# Ping

Verifica se a API está **online e respondendo**. Útil como heartbeat.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/Ping`

## Headers

| Header | Obrigatório | Descrição |
| --- | --- | --- |
| `x-digifarma-user` | Sim | Usuário fornecido pela Digifarma |
| `x-digifarma-token` | Sim | Token obtido via `GetToken` |

## Body

Envie via `form-data` com um único campo chamado **`json`** contendo o JSON abaixo:

Este endpoint não recebe parâmetros adicionais — envie `"params": null`.

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": null
}
```

## Exemplo de resposta

```json
{
  "result": [
    "ok"
  ]
}
```
