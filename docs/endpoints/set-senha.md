# SetSenha

Define uma **senha alfanumérica** vinculada ao CNPJ de uma loja. Recurso **opt-in**, criado a pedido de parceiro que preferia trafegar a própria senha como reforço adicional em cada requisição.

**Como funciona:**

- Se, numa chamada da API, a integradora **enviar** o header `x-digifarma-senha` → a API valida contra a senha definida. Se bater, aprova; se não bater, rejeita.
- Se **não enviar** o header → a API ignora essa camada e segue com a autenticação padrão (`x-digifarma-user` + `x-digifarma-token`) normalmente.

Ou seja: mesmo depois de definir a senha, você continua livre para chamar as rotas sem o header. A senha só é conferida quando o header aparece — é **decisão da integradora**, chamada a chamada.

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
