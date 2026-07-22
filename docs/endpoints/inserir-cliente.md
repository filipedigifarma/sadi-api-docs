# InserirCliente

Cadastra um **novo cliente** ou atualiza um existente.

- Para inserir: envie `CLIENTE_ID = "0"`.
- Para atualizar: envie o `CLIENTE_ID` do registro existente.

O array `CLIENTE` deve conter exatamente **1 objeto**.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/InserirCliente`

## Headers

| Header | Obrigatório | Descrição |
| --- | --- | --- |
| `x-digifarma-user` | Sim | Usuário fornecido pela Digifarma |
| `x-digifarma-token` | Sim | Token obtido via `GetToken` |

## Body

Envie via `form-data` com um único campo chamado **`json`** contendo o JSON abaixo:

### Estrutura de `params`

| Chave | Tipo | Descrição |
| --- | --- | --- |
| `CLIENTE` | array (1 objeto) | Dados do cliente a inserir/atualizar |

#### Campos de `CLIENTE`

| Campo | Tipo | Obrigatório | Default | Descrição |
| --- | --- | --- | --- | --- |
| `CLIENTE_ID` | string | Sim | — | `"0"` = novo cliente; ID existente = atualiza |
| `CLIENTE` | string | Sim | — | Nome completo do cliente (maiúsculas) |
| `CLI_CPF` | string | Sim | — | CPF sem formatação (11 dígitos) |
| `CLI_RG` | string | Não | — | RG do cliente |
| `CLI_ENDERECO` | string | Não | — | Logradouro |
| `CLI_NUMERO` | string | Não | — | Número do endereço |
| `CLI_BAIRRO` | string | Não | — | Bairro |
| `CLI_CIDADE` | string | Não | — | Cidade |
| `CLI_CEP` | string | Não | — | CEP sem formatação (8 dígitos) |
| `CLI_UF` | string | Não | — | Estado (sigla de 2 letras) |
| `CLI_TELEFONE` | string | Não | — | Telefone fixo |
| `CLI_CELULAR` | string | Não | — | Celular |
| `CLI_EMAIL` | string | Não | — | E-mail |
| `CLI_SEXO` | string | Não | — | `"M"` = Masculino, `"F"` = Feminino |
| `CLI_ESTADO_CIVIL` | string | Não | — | `"S"`=solteiro, `"C"`=casado, `"D"`=divorciado, `"V"`=viúvo |
| `CLI_NASCIMENTO` | string | Não | — | Data de nascimento `yyyy-mm-dd` |
| `CLI_CONJUGE` | string | Não | — | Nome do cônjuge |
| `CLI_PAI` | string | Não | — | Nome do pai |
| `CLI_MAE` | string | Não | — | Nome da mãe |
| `CADASTRO_VENDEDOR_ID` | string | Não | — | ID do vendedor que fez o cadastro |
| `CLI_SALARIO` | string | Não | — | Salário do cliente |
| `CLI_LIMITE` | string | Não | — | Limite de crediário |
| `CREDIARIO` | string | Não | "FALSE" | `"TRUE"` ou `"FALSE"` — habilita crediário |
| `CLI_BLOQUEADO` | string | Não | "FALSE" | `"TRUE"` ou `"FALSE"` — bloqueia cliente |
| `ORIGEM_CADASTRO_ID` | string | Não | — | Identificador da origem do cadastro (ex: nome do sistema) |

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": {
    "CLIENTE": [
      {
        "CLIENTE_ID": "0",
        "CLIENTE": "JOÃO DA SILVA",
        "CLI_CPF": "12345678901",
        "CLI_NASCIMENTO": "1985-05-20",
        "CLI_CELULAR": "31998765432",
        "CREDIARIO": "FALSE",
        "CLI_BLOQUEADO": "FALSE",
        "ORIGEM_CADASTRO_ID": "MEUAPP"
      }
    ]
  }
}
```

## Exemplo de resposta

```json
{
  "result": [
    {
      "success": true,
      "CLIENTE_ID": 12345
    }
  ]
}
```
