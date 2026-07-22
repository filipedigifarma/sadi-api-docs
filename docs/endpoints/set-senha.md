# SetSenha

Define uma **senha alfanumérica** associada ao CNPJ do cliente, usada em fluxos de autoatendimento onde ele precisa se identificar.

**Body enviado como form-data direto** (sem o campo `json` — diferente das demais rotas).

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/SetSenha`

## Headers

| Header | Obrigatório | Descrição |
| --- | --- | --- |
| `x-digifarma-user` | Sim | Usuário fornecido pela Digifarma |
| `x-digifarma-token` | Sim | Token obtido via `GetToken` |

## Body

Envie via `form-data` — campos diretos (sem o wrapper `json`):

| Campo | Tipo | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `cnpj` | string | Sim | CNPJ do cliente |
| `senha` | string | Sim | Senha alfanumérica |

## Exemplo de envio

Envie como form-data (não como JSON):

```
cnpj=02695980000110
senha=1234567
```

## Exemplo de resposta

```json
{
  "success": true
}
```
