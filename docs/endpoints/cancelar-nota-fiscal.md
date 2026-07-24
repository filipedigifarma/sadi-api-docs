# CancelarNotaFiscal

Cancela uma **nota fiscal** previamente registrada via `InserirNotaFiscal`. Marca a nota como cancelada e **devolve o estoque** dos itens (operação simétrica à baixa feita na inserção).

Se a nota já foi transmitida à SEFAZ, esta rota **não** faz o cancelamento fiscal — apenas o cancelamento lógico no PDV. O cancelamento fiscal é responsabilidade do módulo de emissão.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/CancelarNotaFiscal`

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
| `id_nota` | integer | Sim | ID da nota a cancelar (deve ser > 0). Retornado por `InserirNotaFiscal` em `id_nota`. |

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": {
    "id_nota": 45678
  }
}
```

## Exemplo de resposta

```json
{
  "result": [
    {
      "success": true,
      "id_nota": 45678,
      "cancelado": "S"
    }
  ]
}
```

## Observações

- Nota não encontrada → `{ "success": false, "id_nota": 45678, "message": "Nota nao encontrada" }`
- `id_nota` ausente → `{ "success": false, "message": "id_nota nao informado" }`
- `id_nota` <= 0 → `{ "success": false, "message": "id_nota invalido" }`
- O estoque dos itens é **devolvido** automaticamente (simétrico ao baixado na inserção).
