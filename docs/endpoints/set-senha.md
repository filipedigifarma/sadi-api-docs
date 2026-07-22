# SetSenha

Define uma **senha alfanumérica** vinculada ao CNPJ de uma loja, funcionando como camada adicional de autenticação da integradora.

**⚠ Comportamento importante:** a partir do momento em que uma senha é definida para um CNPJ, **todas as chamadas subsequentes da API a esse CNPJ passam a exigir o header `x-digifarma-senha`** com a senha correspondente. Requisições sem o header, ou com valor incorreto, são rejeitadas.

Usar este endpoint é **opcional** — se você nunca chamar `SetSenha` para um CNPJ, a autenticação padrão (`x-digifarma-user` + `x-digifarma-token`) continua bastando. Chame apenas se quiser um segundo fator vinculado ao CNPJ atendido.

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
| `cnpj` | string | Sim | CNPJ da loja para a qual a senha será definida |
| `senha` | string | Sim | Senha alfanumérica a ser vinculada ao CNPJ |

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
