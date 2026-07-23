# CancelarPreVenda

Cancela uma **pré-venda** previamente registrada via `InserirPreVenda`. O cancelamento é **lógico** — não devolve saldo de estoque, não mexe em NFC-e nem em valores de pagamento. É idempotente: chamar novamente sobre uma venda já cancelada não gera erro.

Efeitos no banco do PDV:

- `cab_vendas`: `cancelado = 'S'`, `cartao_fechado = 'N'`
- `item_vendas`: `cancelado = 'S'`, `itemvend_cancelado_cupom = 'S'`

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/CancelarPreVenda`

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
| `id_venda` | integer | Sim | ID da venda a cancelar (deve ser > 0) |

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": {
    "id_venda": 12345
  }
}
```

## Exemplo de resposta

```json
{
  "result": [
    {
      "success": true,
      "id_venda": 12345,
      "cancelado": "S"
    }
  ]
}
```

## Observações

- Venda não encontrada → `{ "success": false, "id_venda": 12345, "message": "Venda não encontrada" }`
- `id_venda` ausente → `{ "success": false, "message": "id_venda não informado" }`
- `id_venda` <= 0 → `{ "success": false, "message": "id_venda inválido" }`
- JSON inválido → `{ "success": false, "message": "JSON inválido" }`
