# SetSenha

Define uma **senha alfanumérica** vinculada ao CNPJ de uma loja, usada como **camada opcional de autenticação** pela integradora.

Depois de definida, a integradora pode enviar essa senha no header `x-digifarma-senha` nas demais chamadas da API. Se a senha corresponder, a requisição é autenticada; se não corresponder, é rejeitada. Se o header não for enviado, a autenticação padrão (`x-digifarma-user` + `x-digifarma-token`) já basta.

Essa camada é **opcional** — serve pra integradoras que queiram um segundo fator vinculado ao CNPJ atendido.

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
