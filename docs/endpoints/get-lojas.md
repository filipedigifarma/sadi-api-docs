# GetLojas

Retorna dados **cadastrais da farmácia** (nome fantasia, razão social, endereço, contato) para exibição no carregamento inicial da página via QR Code.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/GetLojas`

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
  "cnpj": "02695980000110"
}
```

## Exemplo de resposta

```json
{
  "success": true,
  "loja": {
    "cnpj": "02695980000110",
    "fantasia": "FARMÁCIA EXEMPLO",
    "razao_social": "FARMÁCIA EXEMPLO LTDA",
    "ie": "123456789",
    "logradouro": "Rua das Flores",
    "numero": "100",
    "bairro": "Centro",
    "cidade": "Belo Horizonte",
    "estado": "MG",
    "telefone": "3132001234",
    "email": "contato@farmacia.com.br",
    "ativo": "S"
  }
}
```

## Observações

- Este endpoint dispensa `params` — envie apenas `cnpj` no body.
