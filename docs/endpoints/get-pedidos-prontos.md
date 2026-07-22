# GetPedidosProntos

Retorna **pedidos de manipulação** do cliente prontos para retirada. Identifica itens com flag `PEDIDO_MANIPULACAO` não cancelados. Máximo 20 registros, ordem cronológica decrescente.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/GetPedidosProntos`

## Headers

| Header | Obrigatório | Descrição |
| --- | --- | --- |
| `x-digifarma-user` | Sim | Usuário fornecido pela Digifarma |
| `x-digifarma-token` | Sim | Token obtido via `GetToken` |

## Body

Envie via `form-data` com um único campo chamado **`json`** contendo o JSON abaixo:

### Parâmetros (`params`)

| Campo | Tipo | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `cod_cliente` | integer | Sim | ID interno do cliente |

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": {
    "cod_cliente": 4521
  }
}
```

## Exemplo de resposta

```json
{
  "success": true,
  "pedidos": [
    {
      "numero": "8542",
      "descricao": "FÓRMULA MAGISTRAL SÉRUM",
      "tipo": "MANIPULADO",
      "data_previsao": "2026-05-10",
      "status": "PRONTO"
    }
  ]
}
```
