# ListaProduto

Consulta o **catálogo de produtos** da loja. Suporta busca por código, EAN, nome ou data de atualização, com paginação, ordenação e filtro de saldo.

A resposta **sempre inclui também os `kits`** cadastrados (com seus itens) — listar produtos já traz tudo. Se quiser **somente os kits**, envie `"apenas_kits": true`.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/ListaProduto`

## Headers

| Header | Obrigatório | Descrição |
| --- | --- | --- |
| `x-digifarma-user` | Sim | Usuário fornecido pela Digifarma |
| `x-digifarma-token` | Sim | Token obtido via `GetToken` |
| `User-Agent` | Recomendado | Identificação da sua integradora — use o **nome da sua empresa** (ex: `MinhaEmpresa/1.0`). Boa prática **obrigatória**: nos ajuda a identificar a origem das chamadas e a dar suporte. Evite o User-Agent genérico da biblioteca HTTP (ex: `PostmanRuntime`, `python-requests`). |

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
| `apenas_kits` | boolean | Não | false | Se `true`, **não consulta produtos** e retorna **apenas os kits**. Na listagem normal os kits já vêm juntos — use isto só quando quiser exclusivamente os kits. Ver *Modo `apenas_kits`* abaixo. |
| `integracao` | string | Não | "" | **Legado / em desuso.** Filtra produtos vinculados a uma integração. Não afeta os kits. |
| `apenas_integracao` | boolean | Não | false | **Legado / em desuso.** Se `true`, retorna apenas produtos com vínculo em integração ativa. |

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
    "apenas_kits": false
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
          "produto_resumido": "BUSCOPAN COMP",
          "fabricante": "MEDLEY GENERICOS",
          "categoria": "GENERICOS",
          "sub_categoria": "ANALGESICOS",
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
          "fiscal": {
            "ncm": "30049099",
            "cest": "1300201",
            "unidade": "UND",
            "cst_pis": "04",
            "cst_cofins": "04",
            "cod_tributacao": "F",
            "registro_ms": "1781709440037",
            "info_adicional": ""
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
      ],
      "total_kits": 1,
      "kits": [
        {
          "kit_id": 12,
          "kit_nome": "KIT GRIPE",
          "kit_ativo": "S",
          "kit_saldo": 30,
          "lastupdate": "10/08/2026 09:12:00",
          "itens": [
            {
              "kit_item_id": 1,
              "produto_id": 3906,
              "produto": "BUTILB ESCOP+DIP-G 20-MD",
              "cod_barras": "7896422507967",
              "quantidade": 2,
              "valor": 5.0,
              "valor_kit": 5.0,
              "valor_promo": 0,
              "valor_base": 6.59
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
| `total_registros` | integer | Total de **produtos** que casam com a busca, **ignorando a paginação**. Útil para calcular quantas páginas você precisa buscar. |
| `produtos` | array | Produtos da página atual (tamanho ≤ `tamanho_pagina`) |
| `total_kits` | integer | Total de **kits** cadastrados. **Sempre presente.** |
| `kits` | array | Todos os kits do cadastro, com seus itens. **Sempre presente** na listagem de produtos (não é paginado). Ver estrutura abaixo. |

### Cada item em `produtos[]`

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `produto_id` | integer | ID interno do produto no SADI |
| `cod_barras` | string | EAN/código de barras. Vazio se não cadastrado. |
| `produto` | string | Nome/descrição do produto |
| `produto_resumido` | string | Descrição enxuta/reduzida do produto. Vazio se não cadastrada. |
| `fabricante` | string | Fabricante ou laboratório |
| `categoria` | string | Categoria comercial (ex: `GENERICOS`, `SIMILARES`, `ETICOS`, `PERFUMARIA`) |
| `sub_categoria` | string | Sub-categoria comercial do produto. Vazia se não cadastrada. |
| `apresentacao` | string | Código de apresentação/embalagem no cadastro |
| `cod_tributacao` | string | Código de tributação fiscal (ex: `F`, `T`, `I`). Também disponível dentro de `fiscal`. |
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
| `fiscal` | object | Dados fiscais do produto. **Sempre presente.** Ver estrutura abaixo. |
| `desconto_escalonado` | array | Faixas de desconto por quantidade. Vazio se não aplicável. |

### `fiscal`

Dados fiscais do cadastro do produto. Campos ausentes no cadastro vêm como string vazia (`""`).

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `ncm` | string | NCM (Nomenclatura Comum do Mercosul) do produto |
| `cest` | string | CEST (Código Especificador da Substituição Tributária). Vazio se não aplicável. |
| `unidade` | string | Unidade de medida do produto (ex: `UND`, `CX`, `FR`) |
| `cst_pis` | string | CST do PIS (ex: `01`, `04`, `06`) |
| `cst_cofins` | string | CST do COFINS (ex: `01`, `04`, `06`) |
| `cod_tributacao` | string | Código de tributação (CSOSN/CST de ICMS conforme o regime). Mesmo valor do `cod_tributacao` da raiz. |
| `registro_ms` | string | Registro no Ministério da Saúde / ANVISA. Vazio se não aplicável. |
| `info_adicional` | string | Informações adicionais/observação fiscal do produto. Vazio se não cadastrada. |

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

### Cada item em `kits[]`

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `kit_id` | integer | ID interno do kit |
| `kit_nome` | string | Nome/descrição do kit |
| `kit_ativo` | string | `"S"` = ativo, `"N"` = inativo |
| `kit_saldo` | number | Saldo do kit |
| `lastupdate` | string \| null | Data/hora da alteração mais recente entre os produtos do kit — `dd/mm/yyyy hh:mm:ss`. `null` se o kit não tiver itens ativos. |
| `itens` | array | Produtos que compõem o kit. Ver estrutura abaixo. |

### Cada item em `kits[].itens[]`

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `kit_item_id` | integer | ID do item dentro do kit |
| `produto_id` | integer | ID interno do produto no SADI |
| `produto` | string | Nome/descrição do produto |
| `cod_barras` | string | EAN/código de barras do produto |
| `quantidade` | number | Quantidade desse produto no kit |
| `valor` | number | Valor do item praticado **dentro do kit** |
| `valor_kit` | number | Igual a `valor` — preço do item no kit |
| `valor_promo` | number | Preço de promoção do produto (`0` se não houver promoção vigente) |
| `valor_base` | number | Preço de venda base do produto (fora do kit) |

### Modo `apenas_kits`

Com `"apenas_kits": true` a rota **não consulta produtos** e a raiz muda levemente: `produtos` vem vazio (`[]`) e o total de produtos aparece como `total_produtos` (sempre `0`) em vez de `total_registros`. Os arrays `kits` / `total_kits` seguem o **mesmo formato** descrito acima.

## Observações

- Os `kits` **sempre acompanham** a listagem de produtos — não é preciso pedir. Use `"apenas_kits": true` apenas quando quiser **exclusivamente os kits** (sem trafegar os produtos).
- O array `kits` **não é paginado**: traz todos os kits do cadastro em qualquer página. Já `produtos` respeita `pagina` / `tamanho_pagina`.
- Os parâmetros `integracao` / `apenas_integracao` são **legados** e estão em desuso; não têm efeito sobre os kits.
