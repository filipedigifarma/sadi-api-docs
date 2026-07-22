# InserirVenda

Registra uma **venda já finalizada** no PDV. Utilizado por integrações de marketplace (iFood, Rappi etc.) para dar baixa automática no estoque.

O `params` tem quatro chaves: `venda`, `venda_item`, `delivery` e `cab_vendas_fpagtos`.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/InserirVenda`

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
| `venda` | object | Cabeçalho da venda. |
| `venda_item` | array | Itens da venda. |
| `delivery` | object ou array | Endereço de entrega (opcional). |
| `cab_vendas_fpagtos` | array | Formas de pagamento detalhadas (uma por linha para pagamento multi-forma). |

#### Campos de `venda`

| Campo | Tipo | Obrigatório | Default | Descrição |
| --- | --- | --- | --- | --- |
| `venda_total` | number | Sim | — | Valor total da venda |
| `venda_recebido` | number | Sim | — | Valor recebido |
| `cartao_atd` | number | Não | — | Número do cartão de atendimento |
| `pedido` | string | Não | — | Número do pedido externo |
| `origem_venda` | string | Não | — | Identificador da origem (ex: `"ifood"`) |
| `v_id` | string | Não | — | ID do vendedor ou origem |
| `fpagto` | string | Sim | — | Código da forma de pagamento (ex: `"0"`) |
| `cpf_cliente` | string | Não | — | CPF do cliente |
| `frete` | number | Não | 0 | Valor do frete |
| `venda_desconto` | number | Não | 0 | Desconto aplicado |
| `troco` | number | Não | 0 | Valor do troco |
| `token` | string | Não | — | Token único do pedido (idempotência) |

#### Campos de `venda_item`

| Campo | Tipo | Obrigatório | Default | Descrição |
| --- | --- | --- | --- | --- |
| `p_id` | string | Sim | — | EAN/código de barras do produto |
| `qtde` | number | Sim | — | Quantidade |
| `prt` | number | Sim | — | Preço de tabela |
| `prv` | number | Sim | — | Preço de venda |
| `vv` | number | Sim | — | Valor da venda do item |
| `desc` | number | Não | 0 | Percentual de desconto |
| `c_tr` | string | Não | "F" | Código de tributação (ex: `"F"`) |
| `pc` | integer | Não | — | Número de parcelas |
| `v_id` | string | Não | — | ID do vendedor ou origem (ex: `"ifood"`) |

#### Campos de `delivery`

| Campo | Tipo | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `nom` | string | Sim | Nome do destinatário |
| `end` | string | Sim | Logradouro |
| `num` | string | Sim | Número |
| `bai` | string | Sim | Bairro |
| `cid` | string | Sim | Cidade |
| `cep` | string | Sim | CEP (8 dígitos) |
| `uf` | string | Sim | Estado (sigla) |
| `com` | string | Não | Complemento |
| `ref` | string | Não | Ponto de referência |
| `tel` | string | Não | Telefone |
| `cel` | string | Não | Celular |

#### Campos de `cab_vendas_fpagtos`

| Campo | Tipo | Obrigatório | Default | Descrição |
| --- | --- | --- | --- | --- |
| `f` | string | Sim | — | Nome da forma de pagamento (ex: `"cartao"`, `"dinheiro"`) |
| `a` | string | Sim | — | Valor pago nesta forma |
| `n` | string | Não | — | NSU / número da transação |
| `i` | string | Não | "1" | Número de parcelas |
| `b` | string | Não | — | Bandeira (ex: `"visa debito"`) |

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": {
    "venda": {
      "venda_total": 111.99,
      "venda_recebido": 111.99,
      "cartao_atd": 99858,
      "pedido": "11482-F17977756",
      "origem_venda": "ifood",
      "v_id": "ifood",
      "fpagto": "0",
      "cpf_cliente": "12345678909",
      "frete": 4,
      "venda_desconto": 0,
      "troco": 150,
      "token": "token único"
    },
    "venda_item": [
      {
        "p_id": "7891317003906",
        "desc": 15,
        "pc": 2,
        "c_tr": "F",
        "qtde": 1,
        "v_id": "ifood",
        "prt": 42.5,
        "prv": 42.5,
        "vv": 40
      }
    ],
    "delivery": {
      "tel": "xxxxxxxxxx",
      "cel": "xxxxxxxxxxx",
      "nom": "João Teste",
      "end": "Avenida Teste",
      "num": "5",
      "com": "casa",
      "ref": "na esquina do posto",
      "bai": "Centro",
      "cid": "Ipatinga",
      "cep": "35164000",
      "uf": "MG"
    },
    "cab_vendas_fpagtos": [
      {
        "f": "cartao",
        "a": "10",
        "n": "321654",
        "i": "1",
        "b": "visa debito"
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
      "venda_id": 12457
    }
  ]
}
```

## Observações

- Envie um `token` único por pedido para evitar duplicidade em caso de reenvio.
- A soma dos `a` em `cab_vendas_fpagtos` deve ser igual a `venda_recebido`.
