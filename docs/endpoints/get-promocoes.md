# GetPromocoes

Retorna **promoções ativas** da farmácia em duas categorias:

- `gerais` — ofertas de preço com desconto
- `compra_leva` — promoções do tipo *leve X, pague Y*

Apenas produtos com saldo > 0 e dentro do período de validade. Máximo 20 itens por categoria.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/GetPromocoes`

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
  "gerais": [
    {
      "id": 1234,
      "titulo": "DIPIRONA 500MG 20CPR",
      "preco_de": 12.5,
      "preco_por": 9.9,
      "percentual_desconto": 21,
      "tipo": "OFERTA",
      "validade": "2026-05-31"
    }
  ],
  "compra_leva": [
    {
      "id": 5678,
      "titulo": "Leve 3, Pague 2",
      "produto": "PROTETOR SOLAR FPS 60",
      "detalhe": "Leve 3 unidades e pague apenas 2",
      "validade": "2026-06-30"
    }
  ]
}
```

## Observações

- Este endpoint dispensa `params` — envie apenas `cnpj` no body.
