# GetToken - Autenticação

Gera um **token de acesso** para a integradora. Este token deve ser enviado no header `x-digifarma-token` em todas as demais requisições da API.

O token tem validade limitada. Renove chamando este endpoint novamente quando expirar.

**Pré-requisitos:**

- O `x-digifarma-user` precisa ter sido **emitido pela Digifarma** — não há auto-cadastro. Solicite via filipe@digifarma.com.br.
- O `cnpj` informado precisa estar **liberado para o seu usuário** na base da Digifarma. Envie a lista de CNPJs que sua integradora atenderá junto do pedido do usuário.

**Método:** `POST`  
**URL:** `https://sadi.digifarma.com.br/api/GetToken`

## Headers

| Header | Obrigatório | Descrição |
| --- | --- | --- |
| `x-digifarma-user` | Sim | Usuário fornecido pela Digifarma |

## Body

Envie via `form-data` — campos diretos (sem o wrapper `json`):

| Campo | Tipo | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `cnpj` | string | Sim | CNPJ da integradora (somente dígitos, sem formatação) |

## Exemplo de envio

Envie como form-data (não como JSON):

```
cnpj=02695980000110
```

## Exemplo de resposta

```json
{
  "token": "seu-token-aqui"
}
```
