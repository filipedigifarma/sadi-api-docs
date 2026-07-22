# GetDadosLoja

Retorna os **dados fiscais e cadastrais** da loja vinculada ao CNPJ informado. Utilizado tipicamente para exibir cabeçalho da loja em telas de integração.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/GetDadosLoja`

## Headers

| Header | Obrigatório | Descrição |
| --- | --- | --- |
| `x-digifarma-user` | Sim | Usuário fornecido pela Digifarma |
| `x-digifarma-token` | Sim | Token obtido via `GetToken` |

## Body

Envie via `form-data` com um único campo chamado **`json`** contendo o JSON abaixo:

Este endpoint não recebe parâmetros adicionais — envie `"params": null`.

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": null
}
```

## Exemplo de resposta

```json
{
  "result": [
    [
      {
        "CNPJ": "02695980000110",
        "FANTASIA": "FARMÁCIA EXEMPLO",
        "RAZAO_SOCIAL": "FARMÁCIA EXEMPLO LTDA",
        "INSCRICAO": "000000000",
        "ENDERECO": "RUA EXEMPLO",
        "NUMERO": "100",
        "BAIRRO": "CENTRO",
        "CIDADE": "BELO HORIZONTE",
        "ESTADO": "MG",
        "TELEFONE": "31-0000 0000",
        "EMAIL": "contato@farmacia.com.br"
      }
    ]
  ]
}
```

## Observações

- `params` deve ser enviado como `null` — este endpoint não recebe parâmetros adicionais.
