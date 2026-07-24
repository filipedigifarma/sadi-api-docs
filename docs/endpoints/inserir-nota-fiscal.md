# InserirNotaFiscal

Grava uma **nota fiscal de saída** para pedidos de e-commerce.

- Grava em `CAB_NOTAS` / `ITEM_NOTAS` / `CAB_NOTAS_FPAGTOS`.
- Baixa o **estoque** dos produtos vendidos.
- Cria (ou reusa) um registro de destinatário em `FORNECEDORES` a partir do CPF/CNPJ.

Esta rota **não emite** NFC-e/NF-e via SEFAZ — apenas grava a nota no banco. A emissão fiscal é responsabilidade de outro módulo que consome a nota gravada.

**Idempotência:** se `pedido` vier preenchido e já existir uma nota de saída com esse `NUMERO_PEDIDO`, a rota retorna o `nota_id` existente em vez de duplicar.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/InserirNotaFiscal`

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
| `venda` | object | Cabeçalho da nota — totais, número do pedido, origem. |
| `destinatario` | object | Dados fiscais e endereço do destinatário da NF. Traz os campos que a SEFAZ exige. |
| `venda_item` | array | Itens da nota — um objeto por produto. |
| `pagamento` | array | Formas de pagamento (opcional). |

#### Campos de `venda`

| Campo | Tipo | Obrigatório | Default | Descrição |
| --- | --- | --- | --- | --- |
| `venda_total` | number | Sim | — | Valor total da nota |
| `pedido` | string | Não | "" | Número do pedido externo (usado para idempotência) |
| `origem_venda` | string | Não | — | Identificador da origem (ex: `"ECOMMERCE"`). Cria/reusa registro em `ORIGEM_NFE`. |
| `vendedor` | string | Não | "0" | Vendedor responsável pela nota — aceita **ID (numérico)** ou **nome**. Se vier nome, o Sadi resolve pra ID via cadastro. |
| `cfop` | string | Não | — | CFOP da nota (ex: `"5102"` intra, `"6108"` inter, consumidor final). Se ausente, o módulo de emissão preenche. Pode ser sobrescrito por item. |
| `frete` | number | Não | 0 | Valor do frete |
| `venda_desconto` | number | Não | 0 | Desconto aplicado |

#### Campos de `destinatario`

| Campo | Tipo | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `cpf_cnpj` | string | Sim | CPF (11 dígitos) ou CNPJ (14 dígitos), só números. |
| `nome` | string | Sim | Nome do destinatário (PF) ou razão social (PJ). |
| `ie` | string | Cond. | Inscrição Estadual. Obrigatória para PJ contribuinte de ICMS; use `"ISENTO"` para PF ou PJ isento. |
| `email` | string | Não | E-mail para envio da DANFE. |
| `end` | string | Sim | Logradouro |
| `num` | string | Sim | Número |
| `com` | string | Não | Complemento |
| `bai` | string | Sim | Bairro |
| `cid` | string | Sim | Cidade |
| `cep` | string | Sim | CEP (só dígitos) |
| `uf` | string | Sim | Estado (sigla) |
| `tel` | string | Não | Telefone fixo |
| `cel` | string | Não | Celular |

#### Campos de `venda_item`

| Campo | Tipo | Obrigatório | Default | Descrição |
| --- | --- | --- | --- | --- |
| `p_id` | string | Sim | — | EAN ou PRODUTO_ID |
| `qtde` | number | Sim | — | Quantidade |
| `prv` | number | Sim | — | Preço de venda unitário |
| `desc` | number | Não | 0 | Desconto do item |
| `cfop` | string | Não | — | CFOP específico do item (sobrescreve `venda.cfop`). Útil quando o item tem ST diferente. |

#### Campos de `pagamento`

| Campo | Tipo | Obrigatório | Default | Descrição |
| --- | --- | --- | --- | --- |
| `f` | string | Sim | — | Nome da forma (ex: `"dinheiro"`, `"cartao"`) |
| `a` | string | Sim | — | Valor pago nesta forma |
| `n` | string | Não | "" | NSU / número da transação |
| `i` | string | Não | "1" | Número de parcelas |
| `b` | string | Não | "" | Bandeira (ex: `"visa credito"`) |

## Exemplo de envio

Conteúdo do campo `json`:

```json
{
  "cnpj": "02695980000110",
  "params": {
    "venda": {
      "venda_total": 77.59,
      "pedido": "ECOM-12345",
      "origem_venda": "ECOMMERCE",
      "vendedor": "1",
      "cfop": "5102",
      "frete": 0,
      "venda_desconto": 0
    },
    "destinatario": {
      "cpf_cnpj": "11658675673",
      "nome": "Tamer Sammour",
      "ie": "ISENTO",
      "email": "tamer@exemplo.com",
      "end": "R. Cândido Neiva",
      "num": "59",
      "com": "Casa De Pedra",
      "bai": "Centro",
      "cid": "PARACATU",
      "cep": "38600000",
      "uf": "MG",
      "cel": "38999999999"
    },
    "venda_item": [
      {
        "p_id": "7891800662122",
        "qtde": 2,
        "prv": 33.8,
        "desc": 0
      },
      {
        "p_id": "7899547500363",
        "qtde": 1,
        "prv": 9.99,
        "desc": 0
      }
    ],
    "pagamento": [
      {
        "f": "cartao",
        "a": "77.59",
        "n": "123456",
        "i": "1",
        "b": "visa credito"
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
      "id_nota": 45678,
      "numero_nota_fiscal": "12345",
      "id_destinatario": 1234,
      "numero_pedido": "ECOM-12345"
    }
  ]
}
```

## Observações

- `numero_nota_fiscal` é o número fiscal sequencial da NF de saída (gerado no momento da gravação). Fica alocado desde já — numeração fiscal brasileira não pode ser reusada.
- `id_destinatario` é o ID interno do destinatário nos cadastros do PDV.
- **CFOP/CST/CSOSN preenchidos automaticamente**: o PDV usa a config fiscal da loja + tributação de cada produto, compara UF do destinatário com UF da loja (`dentro`/`fora`) e aplica CST ou CSOSN conforme o regime tributário. Se `venda.cfop` ou `venda_item[].cfop` vierem no payload, sobrescrevem o CFOP calculado.
- `destinatario.cpf_cnpj` ausente → `{ "success": false, "message": "cpf_cnpj do destinatario obrigatorio para emissao de nota fiscal" }`
- Produto não localizado → `{ "success": false, "message": "Produto nao encontrado: <p_id>" }`
- **Validação de saldo:** se a loja não permite venda com estoque negativo, a rota rejeita quando algum produto não tem saldo suficiente, retornando `{ "success": false, "message": "Produto sem saldo suficiente", "produtos_sem_saldo": [{ "produto_id": 123, "produto": "NIMESULIDA 100MG", "saldo": 3, "solicitado": 10 }] }`.
- Idempotência: se `pedido` já existir em outra nota, retorna a nota existente sem erro (`success: true`) — incluindo o `numero_nota_fiscal` já atribuído.
- A rota **não transmite** NFC-e/NF-e à SEFAZ — a transmissão fiscal é feita por outro módulo consumindo a nota gravada.
