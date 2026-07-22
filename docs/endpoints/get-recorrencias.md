# GetRecorrencias

Retorna **produtos de compra recorrente** do cliente com base no histórico. Considera itens comprados 2 ou mais vezes, calcula o ciclo médio de dias entre compras e indica se o cliente está atrasado para renovar.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/GetRecorrencias`

## Headers

| Header | Obrigatório | Descrição |
| --- | --- | --- |
| `x-digifarma-user` | Sim | Usuário fornecido pela Digifarma |
| `x-digifarma-token` | Sim | Token obtido via `GetToken` |

## Body

Envie via `form-data` com um único campo chamado **`json`** contendo o JSON abaixo:

### Parâmetros (`params`)

| Campo | Tipo | Obrigatório | Default | Descrição |
| --- | --- | --- | --- | --- |
| `cod_cliente` | integer | Sim | — | ID interno do cliente |
| `quantidade_produtos` | integer | Não | 10 | Máximo de produtos retornados |

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": {
    "cod_cliente": 4521,
    "quantidade_produtos": 10
  }
}
```

## Exemplo de resposta

```json
{
  "success": true,
  "recorrencias": [
    {
      "cod_produto": "4521",
      "descricao": "LOSARTANA 50MG 30CPR",
      "ultima_compra": "2026-04-18",
      "ciclo_dias": 30,
      "dias_desde_ultima": 28,
      "atrasado": false
    }
  ]
}
```

## Observações

- `ciclo_dias` é a média de dias entre compras. `atrasado = true` quando `dias_desde_ultima >= ciclo_dias`.
