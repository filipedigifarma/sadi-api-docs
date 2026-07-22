# API SADI — Documentação

Documentação oficial da **API do SADI** (sistema PDV da Digifarma) para parceiros e integradores.

- **Portal renderizado (Fern):** _link após o deploy_
- **Base URL:** `https://sadi.digifarma.com.br/api/`
- **Formato:** REST, `POST` com body em `form-data`, resposta em JSON

> **Antes de tentar usar a API**, sua integradora precisa: **(1)** de um usuário de integração emitido pela Digifarma (`x-digifarma-user`) — não há auto-cadastro, solicite via [filipe@digifarma.com.br](mailto:filipe@digifarma.com.br); e **(2)** liberação, na base da Digifarma, dos CNPJs de farmácia que pretende consultar. Sem essas duas coisas nenhuma rota funciona. Veja [`docs/introduction.md`](docs/introduction.md#-pré-requisitos--leia-antes).

## Onde ler

- [Introdução](docs/introduction.md) — o que é a API e a quem se destina
- [Autenticação](docs/authentication.md) — como obter e usar o token
- [Formato de requisição](docs/request-format.md) — form-data + campo `json`
- [Status de venda](docs/status-venda.md) — valores possíveis do campo `status`
- [Endpoints](docs/endpoints/) — um arquivo por rota

Também disponível como **OpenAPI 3.1** em [`openapi.json`](openapi.json) — importe em Swagger UI, Redoc, Postman ou use como fonte pro Fern.

## Estrutura do repo

```
sadi-api-docs/
├── README.md                    ← este arquivo
├── openapi.json                 ← spec OpenAPI 3.1 gerado
├── docs/
│   ├── introduction.md
│   ├── authentication.md
│   ├── request-format.md
│   ├── status-venda.md
│   └── endpoints/
│       ├── get-token.md
│       ├── inserir-cliente.md
│       └── ...                  ← um por endpoint
└── scripts/
    ├── sadi_api_docs.py         ← fonte única (dados dos endpoints)
    ├── gerar_mdx.py             ← gera docs/endpoints/*.md
    └── gerar_openapi.py         ← gera openapi.json
```

## Atualizando a doc

Todo o conteúdo é gerado a partir do módulo Python [`scripts/sadi_api_docs.py`](scripts/sadi_api_docs.py), que contém os dados estruturados de cada endpoint (headers, parâmetros com obrigatoriedade e default, exemplos, notas).

Fluxo pra atualizar:

```bash
# 1. Edita a fonte única
$EDITOR scripts/sadi_api_docs.py

# 2. Regera os artefatos
python scripts/gerar_mdx.py
python scripts/gerar_openapi.py

# 3. Commita e faz push
git add docs/ openapi.json scripts/
git commit -m "docs: atualiza X"
git push
```

Fern rebuilda o portal automaticamente após o push. Não é preciso rodar nenhum comando adicional lá.

## Contato

Dúvidas de integração: [filipe@digifarma.com.br](mailto:filipe@digifarma.com.br)
