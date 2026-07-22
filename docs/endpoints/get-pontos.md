# GetPontos

Retorna o **saldo de pontos de fidelidade** do cliente e progresso para o próximo prêmio. **Cálculo atual**: 1 ponto a cada R$ 10 em compras efetivadas.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/GetPontos`

## Headers

| Header | Obrigatório | Descrição |
| --- | --- | --- |
| `x-digifarma-user` | Sim | Usuário fornecido pela Digifarma |
| `x-digifarma-token` | Sim | Token obtido via `GetToken` |

## Body

Envie via `form-data` com um único campo chamado **`json`** contendo o JSON abaixo:

### Parâmetros (`params`)

| Campo | Tipo | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `cod_cliente` | integer | Sim | ID interno do cliente |

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": {
    "cod_cliente": 4521
  }
}
```

## Exemplo de resposta

```json
{
  "success": true,
  "pontos": {
    "saldo": 150,
    "proximo_premio_pontos": 1500,
    "proximo_premio_descricao": "Vale-desconto R$ 15,00",
    "pode_resgatar": false
  }
}
```

## Observações

- `pode_resgatar = true` quando `saldo >= proximo_premio_pontos`.
