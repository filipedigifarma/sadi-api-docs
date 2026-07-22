# InserirPreVenda

Registra um **pedido de pré-venda** (ex: pedido delivery). A pré-venda fica pendente no PDV até ser processada pelo operador da farmácia.

O `params` tem três chaves: `venda` (cabeçalho), `venda_item` (itens) e `delivery` (endereço).

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/InserirPreVenda`

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
| `venda` | object | Cabeçalho da venda — totais, cliente e forma de pagamento. |
| `venda_item` | array | Itens da venda — um objeto por produto. |
| `pagamento` | array | Formas de pagamento utilizadas. |
| `delivery` | object | Endereço de entrega. Pode ser omitido se não houver delivery. |

#### Campos de `venda`

| Campo | Tipo | Obrigatório | Default | Descrição |
| --- | --- | --- | --- | --- |
| `venda_total` | number | Sim | — | Valor total da venda |
| `venda_recebido` | number | Sim | — | Valor recebido do cliente |
| `cartao_atd` | string | Não | — | Número do cartão de atendimento |
| `pedido` | string | Não | "" | Número do pedido externo |
| `v_id` | string | Sim | — | ID do vendedor ou origem |
| `origem_venda` | string | Não | — | Identificador da origem (ex: `"IFOOD"`, `"POSTMAN"`) |
| `cliente_id` | string | Não | "0" | ID do cliente (`"0"` = venda avulsa) |
| `delivery_id` | string | Não | "0" | ID do endereço de delivery |
| `cliente` | string | Não | — | Nome do cliente |
| `comprador` | string | Não | — | Nome do comprador |
| `fpagto` | string | Sim | — | Código da forma de pagamento (ex: `"0"` = dinheiro) |
| `cpf_cliente` | string | Não | — | CPF do cliente (sem formatação) |
| `token` | string | Não | — | Token único do pedido (idempotência) |
| `frete` | number | Não | 0 | Valor do frete |
| `troco` | number | Não | 0 | Valor do troco |
| `obs` | string | Não | "" | Observações do pedido |

#### Campos de `venda_item`

| Campo | Tipo | Obrigatório | Default | Descrição |
| --- | --- | --- | --- | --- |
| `p_id` | string | Sim | — | EAN/código de barras do produto |
| `qtde` | number | Sim | — | Quantidade |
| `prt` | number | Sim | — | Preço de tabela |
| `prv` | number | Sim | — | Preço de venda |
| `vv` | number | Sim | — | Valor total do item |
| `desc` | number | Não | 0 | Valor de desconto |
| `c_tr` | string | Não | "F" | Código de tributação (ex: `"F"`) |
| `v_id` | string | Não | — | ID do vendedor |
| `padrao_comissao` | number | Não | 0 | Percentual de comissão |

#### Campos de `pagamento`

| Campo | Tipo | Obrigatório | Default | Descrição |
| --- | --- | --- | --- | --- |
| `f` | string | Sim | — | Nome da forma (ex: `"dinheiro"`, `"cartao"`) |
| `a` | string | Sim | — | Valor pago nesta forma |
| `n` | string | Não | "" | NSU / número da transação |
| `i` | string | Não | "1" | Número de parcelas |
| `b` | string | Não | "" | Bandeira (ex: `"visa"`) |

#### Campos de `delivery`

| Campo | Tipo | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `nom` | string | Sim | Nome do destinatário |
| `end` | string | Sim | Logradouro |
| `num` | string | Sim | Número |
| `bai` | string | Sim | Bairro |
| `cid` | string | Sim | Cidade |
| `cep` | string | Sim | CEP (8 dígitos, sem formatação) |
| `uf` | string | Sim | Estado (sigla de 2 letras) |
| `com` | string | Não | Complemento |
| `ref` | string | Não | Ponto de referência |
| `tel` | string | Não | Telefone fixo |
| `cel` | string | Não | Celular |

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": {
    "venda": {
      "venda_total": 77.59,
      "venda_recebido": 77.59,
      "cartao_atd": "1833197",
      "pedido": "",
      "v_id": "1",
      "origem_venda": "POSTMAN",
      "cliente_id": "0",
      "delivery_id": "0",
      "cliente": "Cliente Exemplo",
      "comprador": "Cliente Exemplo",
      "fpagto": "0",
      "cpf_cliente": "12345678909",
      "token": "identificador-unico-do-pedido",
      "frete": 0,
      "troco": 0,
      "obs": ""
    },
    "venda_item": [
      {
        "p_id": "7891800662122",
        "qtde": 2,
        "prt": 33.8,
        "prv": 33.8,
        "vv": 33.8,
        "desc": 0,
        "c_tr": "F",
        "v_id": "1",
        "padrao_comissao": 0
      }
    ],
    "pagamento": [
      {
        "f": "dinheiro",
        "a": "77.59",
        "n": "",
        "i": "1",
        "b": ""
      }
    ],
    "delivery": {
      "tel": "",
      "cel": "",
      "nom": "Cliente Exemplo",
      "end": "Rua Exemplo",
      "num": "100",
      "com": "Casa",
      "ref": "",
      "bai": "Centro",
      "cid": "Belo Horizonte",
      "cep": "30000000",
      "uf": "MG"
    }
  }
}
```

## Exemplo de resposta

```json
{
  "result": [
    {
      "success": true,
      "venda_id": 45678,
      "msg": "Pré-venda criada"
    }
  ]
}
```

## Observações

- Envie um `token` único por pedido para evitar duplicidade em caso de reenvio.
