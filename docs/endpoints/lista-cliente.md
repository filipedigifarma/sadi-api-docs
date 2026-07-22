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
    "tipo_consulta": "CPF",
    "parametro": "12345678909",
    "pagina": 1,
    "tamanho_pagina": 20
  }
}
```

## Exemplo de resposta

```json
{
  "result": [
    {
      "total_registros": 1,
      "clientes": [
        {
          "cliente_id": 4521,
          "cliente": "JOÃO DA SILVA",
          "cli_cpf": "12345678909",
          "cli_celular": "31999998888",
          "cli_email": "joao@exemplo.com",
          "cli_bloqueado": "FALSE"
        }
      ]
    }
  ]
}
```
