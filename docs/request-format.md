---
title: "Formato de requisição"
description: "Como montar o body em form-data com o campo json"
---

Todas as requisições usam método **`POST`** e body em **`form-data`** — não JSON no `Content-Type`.

## Duas variações de body

### 1. Campo `json` (padrão da maioria das rotas)

O `form-data` tem um único campo `json` cujo valor é um **texto JSON** com esta estrutura:

```json
{
    "cnpj": "SEU_CNPJ",
    "params": { ...parâmetros específicos do endpoint... }
}
```

| Campo | Tipo | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `cnpj` | string | Sim | CNPJ da loja (somente dígitos) |
| `params` | object \| null | Varia | Parâmetros específicos do endpoint. Pode ser `null` quando a rota não recebe params. |

### 2. Campos diretos (`GetToken` e `SetSenha`)

Nessas duas rotas o `form-data` tem os campos diretamente — **sem** o wrapper `json`:

```
cnpj=02695980000110
```

Veja em cada endpoint qual variação usar.

## Exemplo com curl

Campo `json`:

```bash
curl -X POST https://sadi.digifarma.com.br/api/ListaCliente \
  -H "x-digifarma-user: SEU_USUARIO" \
  -H "x-digifarma-token: SEU_TOKEN" \
  -F 'json={"cnpj":"02695980000110","params":{"tipo_consulta":"CPF","parametro":"12345678909","pagina":1,"tamanho_pagina":20}}'
```

Campos diretos:

```bash
curl -X POST https://sadi.digifarma.com.br/api/GetToken \
  -H "x-digifarma-user: SEU_USUARIO" \
  -F "cnpj=02695980000110"
```

## Resposta

Todas as respostas são JSON. O corpo tipicamente segue um destes três padrões:

- **Sucesso "clássico"**: `{"result": [...]}` — a maior parte das rotas
- **Sucesso "moderno"**: `{"success": true, "<recurso>": ...}` — rotas do SADI Online (`GetLojas`, `GetPromocoes`, `GetRecorrencias`, `GetPedidosProntos`, `GetPontos`)
- **Erro**: `{"erro":"sim","msg":"..."}` — quando algo falha
