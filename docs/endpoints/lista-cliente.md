# ListaCliente

Busca clientes cadastrados na loja por CPF, nome, código interno ou telefone. Suporta paginação.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/ListaCliente`

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
| `tipo_consulta` | string | Sim | — | `"COD_INTERNO"`, `"NOME"`, `"CPF"` ou `"TELEFONE"` |
| `parametro` | string | Sim | — | Valor a ser pesquisado |
| `pagina` | integer | Não | 1 | Página desejada |
| `tamanho_pagina` | integer | Não | 20 | Registros por página |

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": {
    "tipo_consulta": "NOME",
    "parametro": "MARIA",
    "pagina": 1,
    "tamanho_pagina": 20
  }
}
```

## Exemplo de resposta

```json
{
  "result": [
    [
      {
        "cliente_id": "759",
        "cliente": "MARIA EXEMPLO SILVA",
        "cli_cpf": "12345678909",
        "telefone": "3134742191",
        "celular": "",
        "enderecos": [
          {
            "endereco": "AV EXEMPLO 2004",
            "bairro": "CENTRO",
            "cidade": "BELO HORIZONTE",
            "uf": "MG",
            "numero": "0",
            "complemento": "",
            "referencia": "",
            "origem": "CLIENTES"
          }
        ]
      },
      {
        "cliente_id": "739",
        "cliente": "MARIA MODELO SANTOS",
        "cli_cpf": "",
        "telefone": "",
        "celular": "31988887777",
        "enderecos": [
          {
            "endereco": "RUA EXEMPLO",
            "bairro": "CENTRO",
            "cidade": "BELO HORIZONTE",
            "uf": "MG",
            "numero": "220",
            "complemento": "",
            "referencia": "",
            "origem": "CLIENTES"
          },
          {
            "endereco": "RUA EXEMPLO",
            "numero": "220",
            "complemento": "APT 302",
            "referencia": "",
            "bairro": "CENTRO",
            "cidade": "BELO HORIZONTE",
            "cep": "30880000",
            "uf": "MG",
            "origem": "CLIENTES_ENDERECO"
          }
        ]
      }
    ]
  ]
}
```

## Campos da resposta

A resposta é **aninhada duas vezes**: `result` é um array contendo um único elemento, que por sua vez é o array de clientes encontrados. Ou seja, os clientes estão em `result[0][]`.

### Cada cliente em `result[0][]`

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `cliente_id` | string | ID interno do cliente no SADI. **Retornado como string**, mesmo sendo numérico. |
| `cliente` | string | Nome do cliente conforme cadastrado (pode ter capitalização mista) |
| `cli_cpf` | string | CPF sem formatação (11 dígitos). Vazio (`""`) se não cadastrado. |
| `telefone` | string | Telefone fixo. Vazio se não cadastrado. |
| `celular` | string | Celular. Vazio se não cadastrado. |
| `enderecos` | array | Endereços vinculados ao cliente — pode ter mais de um (ver estrutura abaixo) |

### Cada item em `enderecos[]`

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `endereco` | string | Logradouro do endereço |
| `bairro` | string | Bairro |
| `cidade` | string | Cidade |
| `uf` | string | Sigla do estado (2 letras) |
| `numero` | string | Número do endereço. Frequentemente vem `"0"` em endereços de origem `CLIENTES` (legado). |
| `complemento` | string | Complemento (apto, bloco, casa, etc.) |
| `referencia` | string | Ponto de referência |
| `cep` | string | CEP sem formatação. **Só aparece quando `origem = "CLIENTES_ENDERECO"`**. |
| `origem` | string | Fonte do endereço — enum abaixo |

### Enum de `origem` em `enderecos[]`

| Valor | Descrição |
| --- | --- |
| `CLIENTES` | Endereço legado, gravado direto no cadastro básico do cliente. Sem CEP estruturado — `numero` pode vir `"0"`, dados podem estar concatenados dentro de `endereco`. |
| `CLIENTES_ENDERECO` | Endereço da tabela de endereços múltiplos, mais estruturado — traz `cep` e campos separados corretamente. |

Um cliente pode ter endereços das duas origens simultaneamente (o do cadastro básico + um ou mais da tabela de endereços). **Priorize `CLIENTES_ENDERECO`** quando disponível — os dados são mais confiáveis pra integração.

## Observações

- Nomes retornados refletem o cadastro real da loja e podem ter erros de digitação, capitalização ou caracteres especiais. Não normalize sem confirmar com o operador.
