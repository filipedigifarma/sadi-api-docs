# ListaProduto

Consulta o **catálogo de produtos** da loja. Suporta busca por código, EAN, nome ou data de atualização, com paginação, ordenação e filtros de saldo e integração.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/ListaProduto`

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
| `tipo_consulta` | string | Sim | — | `"COD_INTERNO"`, `"EAN"`, `"NOME"` ou `"DATA"` |
| `parametro` | string | Não | "" | Valor da busca. Para `DATA` use `"yyyy-mm-dd hh:nn:ss"` |
| `pagina` | integer | Não | 1 | Página desejada |
| `tamanho_pagina` | integer | Não | 20 | Registros por página |
| `saldo_positivo` | boolean | Não | false | Se `true`, retorna apenas produtos com saldo > 0 |
| `ordenar_por` | string | Não | "produto_id" | `"PRODUTO"`, `"COD_BARRAS"`, `"FABRICANTE"`, `"CATEGORIA"`, `"SALDO"`, `"PRECO_VENDA"` ou `"LASTUPDATE"` |
| `ordem` | string | Não | "ASC" | `"ASC"` ou `"DESC"` |
| `integracao` | string | Não | "" | Filtra produtos vinculados a uma integração (ex: `"DIGIFARMA"`) |
| `apenas_integracao` | boolean | Não | false | Se `true`, retorna apenas produtos com vínculo em qualquer integração ativa |

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": {
    "tipo_consulta": "EAN",
    "parametro": "7896422507967",
    "pagina": 1,
    "tamanho_pagina": 10,
    "saldo_positivo": false,
    "ordenar_por": "PRODUTO",
    "ordem": "ASC",
    "integracao": "",
    "apenas_integracao": false
  }
}
```

## Exemplo de resposta

```json
{
  "result": [
    {
      "total_registros": 150,
      "produtos": [
        {
          "produto_id": 12345,
          "cod_barras": "7891234567890",
          "produto": "PARACETAMOL 500MG",
          "fabricante": "EMS",
          "categoria": "ANALGÉSICO",
          "saldo": 35.0,
          "preco_venda": 12.5,
          "leve_x_pague_y": null,
          "desconto_escalonado": []
        }
      ]
    }
  ]
}
```

## Observações

- Quando `integracao` ou `apenas_integracao` é utilizado, a resposta também inclui o array `kits` com kits de produtos ativos vinculados à integração.
