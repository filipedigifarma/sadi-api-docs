# GetStatusVenda

Retorna o **status atual** de uma venda pelo seu ID interno.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/GetStatusVenda`

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
| `venda_id` | integer | Sim | ID interno da venda |

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": {
    "venda_id": 12457
  }
}
```

## Exemplo de resposta

```json
{
  "venda_id": 12457,
  "data_venda": "2025-09-28 14:32:00.0000",
  "valor_total": 253.9,
  "status": "PEDIDO_ENTREGUE",
  "descricao": "Pedido entregue"
}
```

## Observações

- Valores possíveis do campo `status`: `VENDA_PENDENTE`, `VENDA_CONCLUIDA`, `SEPARADO_PARA_ENTREGA`, `ADICIONADO_ROTA_ENTREGA`, `SAIU_PARA_ENTREGA`, `PEDIDO_ENTREGUE`.
