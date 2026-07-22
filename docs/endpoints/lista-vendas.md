# ListaVendas

Lista vendas com seus itens e pagamentos. Suporta **três modos de consulta** — escolha via `tipo_consulta`. Ideal para sincronizações incrementais usando o modo `ALTERACAO`.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/ListaVendas`

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
| `tipo_consulta` | string | Sim | — | `"DATA"`, `"CODIGO"` ou `"ALTERACAO"` |
| `data_inicio` | string | Condicional | — | Formato `yyyy-mm-dd`. Obrigatório se `tipo_consulta = "DATA"` |
| `data_fim` | string | Condicional | — | Formato `yyyy-mm-dd`. Obrigatório se `tipo_consulta = "DATA"` |
| `venda_id` | string | Condicional | — | ID da venda. Obrigatório se `tipo_consulta = "CODIGO"` |
| `data_hora_alteracao` | string | Condicional | — | Formato `yyyy-mm-dd hh:nn:ss`. Obrigatório se `tipo_consulta = "ALTERACAO"` |
| `origem_venda` | string | Não | "" | Filtra por origem (ex: `"IFOOD"`). Opcional em qualquer modo |

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": {
    "tipo_consulta": "DATA",
    "data_inicio": "2025-10-01",
    "data_fim": "2025-10-09",
    "origem_venda": ""
  }
}
```

## Exemplo de resposta

```json
[
  {
    "venda_id": 12457,
    "cnpj": "02695980000110",
    "data_venda": "2025-09-28 14:32:00.0000",
    "valor_total": 253.9,
    "cliente": "JOÃO SILVA",
    "status": "VENDA_CONCLUIDA",
    "descricao": "Venda concluída",
    "nfce_chave": "31250902695980000110650010000001231000012310",
    "itens": [
      {
        "produto_id": 4855,
        "produto": "DIPIRONA 500MG"
      }
    ],
    "pagamentos": [
      {
        "tipo_pagamento": "Cartão de Débito"
      }
    ]
  }
]
```

## Observações

- O modo `ALTERACAO` considera criação, encerramento, emissão de NFC-e e lançamento de comissão — ideal para **sincronização incremental**.
- Ver seção *Status de venda* na descrição da coleção para todos os valores possíveis do campo `status`.
