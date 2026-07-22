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
      "total_registros": 1,
      "produtos": [
        {
          "produto_id": 3906,
          "cod_barras": "7896422507967",
          "produto": "BUTILB ESCOP+DIP-G 20-MD",
          "fabricante": "MEDLEY GENERICOS",
          "categoria": "GENERICOS",
          "apresentacao": "008455",
          "cod_tributacao": "F",
          "localizacao": "",
          "localizacao_id": null,
          "localizacao_descricao": null,
          "psicotropico": "N",
          "antimicrobiano": "N",
          "lista": "",
          "lastupdate": "22/07/2026 17:35:31",
          "inicio_promocao": "01/01/2026",
          "termino_promocao": "31/12/2027",
          "saldo": 0,
          "preco_venda": 6.59,
          "preco_crediario": 0,
          "valor_venda": 5,
          "padrao_comissao": 0,
          "valor_ult_compra": 4.83,
          "leve_x_pague_y": {
            "leve": 6,
            "pague": 5,
            "tipo_preco": "V"
          },
          "desconto_escalonado": [
            {
              "quantidade": 2,
              "valor": 10
            },
            {
              "quantidade": 3,
              "valor": 9
            }
          ]
        }
      ]
    }
  ]
}
```

## Campos da resposta

A resposta é sempre um objeto no formato `{ "result": [ { ... } ] }` — o array `result` sempre tem um único elemento com os campos abaixo.

### Nível raiz — `result[0]`

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `total_registros` | integer | Total de registros que casam com a busca, **ignorando a paginação**. Útil para calcular quantas páginas você precisa buscar. |
| `produtos` | array | Produtos da página atual (tamanho ≤ `tamanho_pagina`) |

### Cada item em `produtos[]`

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `produto_id` | integer | ID interno do produto no SADI |
| `cod_barras` | string | EAN/código de barras. Vazio se não cadastrado. |
| `produto` | string | Nome/descrição do produto |
| `fabricante` | string | Fabricante ou laboratório |
| `categoria` | string | Categoria comercial (ex: `GENERICOS`, `SIMILARES`, `ETICOS`, `PERFUMARIA`) |
| `apresentacao` | string | Código de apresentação/embalagem no cadastro |
| `cod_tributacao` | string | Código de tributação fiscal (ex: `F`, `T`, `I`) |
| `localizacao` | string | Localização física do produto na loja (gôndola/prateleira). Vazio se não cadastrada. |
| `localizacao_id` | integer \| null | ID da localização, se houver |
| `localizacao_descricao` | string \| null | Descrição textual da localização |
| `psicotropico` | string | `"S"` = psicotrópico, `"N"` = comum |
| `antimicrobiano` | string | `"S"` = antimicrobiano, `"N"` = não |
| `lista` | string | Classificação da lista de controle (ex: `A1`, `A2`, `A3`, `B1`, `B2`, `C1`). Vazio se não aplicável. |
| `lastupdate` | string | Data/hora da última alteração no cadastro — formato `dd/mm/yyyy hh:mm:ss` |
| `inicio_promocao` | string | Início da promoção — `dd/mm/yyyy`. Vazio se sem promoção. |
| `termino_promocao` | string | Fim da promoção — `dd/mm/yyyy`. Vazio se sem promoção. |
| `saldo` | number | Saldo atual em estoque |
| `preco_venda` | number | Preço de venda normal (sem promoção) |
| `preco_crediario` | number | Preço à prazo (crediário). `0` se não aplicável. |
| `valor_venda` | number | Preço **efetivo** de venda considerando promoção ativa. Igual a `preco_venda` se não houver promoção. |
| `padrao_comissao` | number | Percentual padrão de comissão do produto |
| `valor_ult_compra` | number | Custo da última compra do produto (referência de custo) |
| `leve_x_pague_y` | object \| null | Promoção **leve X pague Y**, se aplicável. Ver estrutura abaixo. |
| `desconto_escalonado` | array | Faixas de desconto por quantidade. Vazio se não aplicável. |

### `leve_x_pague_y` (quando não é `null`)

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `leve` | integer | Quantidade que o cliente leva |
| `pague` | integer | Quantidade que o cliente paga |
| `tipo_preco` | string | `"V"` = base é o **preço de venda**; `"P"` = base é o **preço de promoção** |

### Cada item em `desconto_escalonado[]`

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `quantidade` | integer | Quantidade mínima a partir da qual a faixa se aplica |
| `valor` | number | Percentual de desconto (%) aplicado ao atingir a `quantidade` |

## Observações

- Quando `integracao` ou `apenas_integracao` é utilizado, a resposta também inclui o array `kits` com kits de produtos ativos vinculados à integração.
