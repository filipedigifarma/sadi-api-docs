"""
Fonte única da verdade para a documentação da API do SADI.

Cada endpoint é descrito como um dict com:
- descricao        : texto de abertura (aceita markdown)
- headers_extras   : headers além dos padrão x-digifarma-user/x-digifarma-token
                     (ex: GetToken só usa x-digifarma-user)
- sem_token        : True se não precisa de x-digifarma-token (só GetToken)
- body_tipo        : "form-data-direto" (GetToken/SetSenha) ou "form-data-json" (default)
- params           : lista simples de campos em params (dicts com campo/tipo/obrigatorio/default/descricao)
- params_grupos    : lista de grupos, cada um com params (para endpoints com body estruturado, ex: InserirPreVenda)
- exemplo_body     : dict Python (será serializado como JSON no exemplo)
- exemplo_resposta : dict/list Python (idem)
- notas            : lista de observações (markdown)

Este módulo é consumido por:
  - atualizar_postman.py  -> gera a description markdown de cada endpoint no collection JSON
  - (futuro) gerar_doc_api.py  -> pode ser refatorado pra ler daqui e evitar duplicação
"""

from typing import Any


# Header padrão que aparece em quase todos os endpoints.
HEADERS_PADRAO: list[dict[str, Any]] = [
    {
        "nome": "x-digifarma-user",
        "obrigatorio": "Sim",
        "descricao": "Usuário fornecido pela Digifarma",
    },
    {
        "nome": "x-digifarma-token",
        "obrigatorio": "Sim",
        "descricao": "Token obtido via `GetToken`",
    },
]


# Header recomendado em TODAS as rotas (inclusive GetToken/SetSenha).
# Não bloqueia a chamada se ausente, mas é uma boa prática obrigatória para
# integradores: permite à Digifarma identificar a origem das requisições,
# dar suporte e diagnosticar problemas por integradora.
HEADER_USER_AGENT: dict[str, Any] = {
    "nome": "User-Agent",
    "obrigatorio": "Recomendado",
    "descricao": (
        "Identificação da sua integradora — use o **nome da sua empresa** "
        "(ex: `MinhaEmpresa/1.0`). Boa prática **obrigatória**: nos ajuda a "
        "identificar a origem das chamadas e a dar suporte. Evite o User-Agent "
        "genérico da biblioteca HTTP (ex: `PostmanRuntime`, `python-requests`)."
    ),
}


# Cada chave é o nome do endpoint (tem que bater com o `name` do item no Postman collection).
ENDPOINTS: dict[str, dict[str, Any]] = {

    # ==================================================================
    # Autenticação
    # ==================================================================
    "GetToken - Autenticação": {
        "descricao": (
            "Gera um **token de acesso** para a integradora. Este token deve ser enviado "
            "no header `x-digifarma-token` em todas as demais requisições da API.\n\n"
            "O token tem validade limitada. Renove chamando este endpoint novamente quando "
            "expirar.\n\n"
            "**Pré-requisitos:**\n\n"
            "- O `x-digifarma-user` precisa ter sido **emitido pela Digifarma** — "
            "não há auto-cadastro. Solicite via filipe@digifarma.com.br.\n"
            "- O `cnpj` informado precisa estar **liberado para o seu usuário** na base "
            "da Digifarma. Envie a lista de CNPJs que sua integradora atenderá junto do "
            "pedido do usuário."
        ),
        "sem_token": True,
        "body_tipo": "form-data-direto",
        "params": [
            {
                "campo": "cnpj",
                "tipo": "string",
                "obrigatorio": "Sim",
                "default": None,
                "descricao": "CNPJ da integradora (somente dígitos, sem formatação)",
            },
        ],
        "exemplo_body_raw": "cnpj=02695980000110",
        "exemplo_resposta": {
            "token": "seu-token-aqui",
        },
        "notas": [],
    },

    # ==================================================================
    # Dados da loja
    # ==================================================================
    "GetDadosLoja": {
        "descricao": (
            "Retorna os **dados fiscais e cadastrais** da loja vinculada ao CNPJ informado. "
            "Utilizado tipicamente para exibir cabeçalho da loja em telas de integração."
        ),
        "exemplo_body": {"cnpj": "02695980000110", "params": None},
        "exemplo_resposta": {
            "result": [[{
                "CNPJ": "02695980000110",
                "FANTASIA": "FARMÁCIA EXEMPLO",
                "RAZAO_SOCIAL": "FARMÁCIA EXEMPLO LTDA",
                "INSCRICAO": "000000000",
                "ENDERECO": "RUA EXEMPLO",
                "NUMERO": "100",
                "BAIRRO": "CENTRO",
                "CIDADE": "BELO HORIZONTE",
                "ESTADO": "MG",
                "TELEFONE": "31-0000 0000",
                "EMAIL": "contato@farmacia.com.br",
            }]]
        },
        "notas": ["`params` deve ser enviado como `null` — este endpoint não recebe parâmetros adicionais."],
    },

    # ==================================================================
    # Cliente
    # ==================================================================
    "ListaCliente": {
        "descricao": (
            "Busca clientes cadastrados na loja por CPF, nome, código interno ou telefone. "
            "Suporta paginação."
        ),
        "params": [
            {"campo": "tipo_consulta",  "tipo": "string",  "obrigatorio": "Sim", "default": None,  "descricao": '`"COD_INTERNO"`, `"NOME"`, `"CPF"` ou `"TELEFONE"`'},
            {"campo": "parametro",      "tipo": "string",  "obrigatorio": "Sim", "default": None,  "descricao": "Valor a ser pesquisado"},
            {"campo": "pagina",         "tipo": "integer", "obrigatorio": "Não", "default": "1",   "descricao": "Página desejada"},
            {"campo": "tamanho_pagina", "tipo": "integer", "obrigatorio": "Não", "default": "20",  "descricao": "Registros por página"},
        ],
        "exemplo_body": {
            "cnpj": "02695980000110",
            "params": {
                "tipo_consulta": "NOME",
                "parametro": "MARIA",
                "pagina": 1,
                "tamanho_pagina": 20,
            }
        },
        "exemplo_resposta": {
            "result": [
                [
                    {
                        "cliente_id": "759",
                        "cliente": "MARIA EXEMPLO SILVA",
                        "cli_cpf": "12345678909",
                        "telefone": "3134742191",
                        "celular": "",
                        "enderecos": [
                            {
                                "endereco": "AV EXEMPLO 2004",
                                "bairro": "CENTRO",
                                "cidade": "BELO HORIZONTE",
                                "uf": "MG",
                                "numero": "0",
                                "complemento": "",
                                "referencia": "",
                                "origem": "CLIENTES",
                            }
                        ],
                    },
                    {
                        "cliente_id": "739",
                        "cliente": "MARIA MODELO SANTOS",
                        "cli_cpf": "",
                        "telefone": "",
                        "celular": "31988887777",
                        "enderecos": [
                            {
                                "endereco": "RUA EXEMPLO",
                                "bairro": "CENTRO",
                                "cidade": "BELO HORIZONTE",
                                "uf": "MG",
                                "numero": "220",
                                "complemento": "",
                                "referencia": "",
                                "origem": "CLIENTES",
                            },
                            {
                                "endereco": "RUA EXEMPLO",
                                "numero": "220",
                                "complemento": "APT 302",
                                "referencia": "",
                                "bairro": "CENTRO",
                                "cidade": "BELO HORIZONTE",
                                "cep": "30880000",
                                "uf": "MG",
                                "origem": "CLIENTES_ENDERECO",
                            }
                        ],
                    },
                ]
            ]
        },
        "descricao_resposta": (
            "A resposta é **aninhada duas vezes**: `result` é um array contendo um único "
            "elemento, que por sua vez é o array de clientes encontrados. Ou seja, os "
            "clientes estão em `result[0][]`.\n\n"
            "### Cada cliente em `result[0][]`\n\n"
            "| Campo | Tipo | Descrição |\n"
            "| --- | --- | --- |\n"
            "| `cliente_id` | string | ID interno do cliente no SADI. **Retornado como string**, mesmo sendo numérico. |\n"
            "| `cliente` | string | Nome do cliente conforme cadastrado (pode ter capitalização mista) |\n"
            "| `cli_cpf` | string | CPF sem formatação (11 dígitos). Vazio (`\"\"`) se não cadastrado. |\n"
            "| `telefone` | string | Telefone fixo. Vazio se não cadastrado. |\n"
            "| `celular` | string | Celular. Vazio se não cadastrado. |\n"
            "| `enderecos` | array | Endereços vinculados ao cliente — pode ter mais de um (ver estrutura abaixo) |\n\n"
            "### Cada item em `enderecos[]`\n\n"
            "| Campo | Tipo | Descrição |\n"
            "| --- | --- | --- |\n"
            "| `endereco` | string | Logradouro do endereço |\n"
            "| `bairro` | string | Bairro |\n"
            "| `cidade` | string | Cidade |\n"
            "| `uf` | string | Sigla do estado (2 letras) |\n"
            "| `numero` | string | Número do endereço. Frequentemente vem `\"0\"` em endereços de origem `CLIENTES` (legado). |\n"
            "| `complemento` | string | Complemento (apto, bloco, casa, etc.) |\n"
            "| `referencia` | string | Ponto de referência |\n"
            "| `cep` | string | CEP sem formatação. **Só aparece quando `origem = \"CLIENTES_ENDERECO\"`**. |\n"
            "| `origem` | string | Fonte do endereço — enum abaixo |\n\n"
            "### Enum de `origem` em `enderecos[]`\n\n"
            "| Valor | Descrição |\n"
            "| --- | --- |\n"
            "| `CLIENTES` | Endereço legado, gravado direto no cadastro básico do cliente. Sem CEP estruturado — `numero` pode vir `\"0\"`, dados podem estar concatenados dentro de `endereco`. |\n"
            "| `CLIENTES_ENDERECO` | Endereço da tabela de endereços múltiplos, mais estruturado — traz `cep` e campos separados corretamente. |\n\n"
            "Um cliente pode ter endereços das duas origens simultaneamente (o do cadastro básico + um ou mais da tabela de endereços). **Priorize `CLIENTES_ENDERECO`** quando disponível — os dados são mais confiáveis pra integração."
        ),
        "notas": [
            "Nomes retornados refletem o cadastro real da loja e podem ter erros de "
            "digitação, capitalização ou caracteres especiais. Não normalize sem confirmar "
            "com o operador.",
        ],
    },

    # ==================================================================
    # Produto
    # ==================================================================
    "ListaProduto": {
        "descricao": (
            "Consulta o **catálogo de produtos** da loja. Suporta busca por código, "
            "EAN, nome ou data de atualização, com paginação, ordenação e filtro de "
            "saldo.\n\n"
            "A resposta **sempre inclui também os `kits`** cadastrados (com seus itens) — "
            "listar produtos já traz tudo. Se quiser **somente os kits**, envie "
            "`\"apenas_kits\": true`."
        ),
        "params": [
            {"campo": "tipo_consulta",    "tipo": "string",  "obrigatorio": "Sim", "default": None,          "descricao": '`"COD_INTERNO"`, `"EAN"`, `"NOME"` ou `"DATA"`'},
            {"campo": "parametro",        "tipo": "string",  "obrigatorio": "Não", "default": '""',          "descricao": 'Valor da busca. Para `DATA` use `"yyyy-mm-dd hh:nn:ss"`'},
            {"campo": "pagina",           "tipo": "integer", "obrigatorio": "Não", "default": "1",           "descricao": "Página desejada"},
            {"campo": "tamanho_pagina",   "tipo": "integer", "obrigatorio": "Não", "default": "20",          "descricao": "Registros por página"},
            {"campo": "saldo_positivo",   "tipo": "boolean", "obrigatorio": "Não", "default": "false",       "descricao": "Se `true`, retorna apenas produtos com saldo > 0"},
            {"campo": "ordenar_por",      "tipo": "string",  "obrigatorio": "Não", "default": '"produto_id"', "descricao": '`"PRODUTO"`, `"COD_BARRAS"`, `"FABRICANTE"`, `"CATEGORIA"`, `"SALDO"`, `"PRECO_VENDA"` ou `"LASTUPDATE"`'},
            {"campo": "ordem",            "tipo": "string",  "obrigatorio": "Não", "default": '"ASC"',       "descricao": '`"ASC"` ou `"DESC"`'},
            {"campo": "apenas_kits",      "tipo": "boolean", "obrigatorio": "Não", "default": "false",       "descricao": "Se `true`, **não consulta produtos** e retorna **apenas os kits**. Na listagem normal os kits já vêm juntos — use isto só quando quiser exclusivamente os kits. Ver *Modo `apenas_kits`* abaixo."},
            {"campo": "integracao",       "tipo": "string",  "obrigatorio": "Não", "default": '""',          "descricao": "**Legado / em desuso.** Filtra produtos vinculados a uma integração. Não afeta os kits."},
            {"campo": "apenas_integracao","tipo": "boolean", "obrigatorio": "Não", "default": "false",       "descricao": "**Legado / em desuso.** Se `true`, retorna apenas produtos com vínculo em integração ativa."},
        ],
        "exemplo_body": {
            "cnpj": "02695980000110",
            "params": {
                "tipo_consulta": "EAN",
                "parametro": "7896422507967",
                "pagina": 1,
                "tamanho_pagina": 10,
                "saldo_positivo": False,
                "ordenar_por": "PRODUTO",
                "ordem": "ASC",
                "apenas_kits": False,
            }
        },
        "exemplo_resposta": {
            "result": [{
                "total_registros": 1,
                "produtos": [{
                    "produto_id": 3906,
                    "cod_barras": "7896422507967",
                    "produto": "BUTILB ESCOP+DIP-G 20-MD",
                    "produto_resumido": "BUSCOPAN COMP",
                    "fabricante": "MEDLEY GENERICOS",
                    "categoria": "GENERICOS",
                    "sub_categoria": "ANALGESICOS",
                    "apresentacao": "008455",
                    "cod_tributacao": "F",
                    "localizacao": "",
                    "localizacao_id": None,
                    "localizacao_descricao": None,
                    "psicotropico": "N",
                    "antimicrobiano": "N",
                    "lista": "",
                    "lastupdate": "22/07/2026 17:35:31",
                    "inicio_promocao": "01/01/2026",
                    "termino_promocao": "31/12/2027",
                    "saldo": 0,
                    "preco_venda": 6.59,
                    "preco_crediario": 0,
                    "valor_venda": 5,
                    "padrao_comissao": 0,
                    "valor_ult_compra": 4.83,
                    "leve_x_pague_y": {
                        "leve": 6,
                        "pague": 5,
                        "tipo_preco": "V",
                    },
                    "fiscal": {
                        "ncm": "30049099",
                        "cest": "1300201",
                        "unidade": "UND",
                        "cst_pis": "04",
                        "cst_cofins": "04",
                        "cod_tributacao": "F",
                        "registro_ms": "1781709440037",
                        "info_adicional": "",
                    },
                    "desconto_escalonado": [
                        {"quantidade": 2, "valor": 10},
                        {"quantidade": 3, "valor": 9},
                    ],
                }],
                "total_kits": 1,
                "kits": [{
                    "kit_id": 12,
                    "kit_nome": "KIT GRIPE",
                    "kit_ativo": "S",
                    "kit_saldo": 30,
                    "lastupdate": "10/08/2026 09:12:00",
                    "itens": [{
                        "kit_item_id": 1,
                        "produto_id": 3906,
                        "produto": "BUTILB ESCOP+DIP-G 20-MD",
                        "cod_barras": "7896422507967",
                        "quantidade": 2,
                        "valor": 5.00,
                        "valor_kit": 5.00,
                        "valor_promo": 0,
                        "valor_base": 6.59,
                    }],
                }],
            }],
        },
        "descricao_resposta": (
            "A resposta é sempre um objeto no formato `{ \"result\": [ { ... } ] }` — "
            "o array `result` sempre tem um único elemento com os campos abaixo.\n\n"
            "### Nível raiz — `result[0]`\n\n"
            "| Campo | Tipo | Descrição |\n"
            "| --- | --- | --- |\n"
            "| `total_registros` | integer | Total de **produtos** que casam com a busca, **ignorando a paginação**. Útil para calcular quantas páginas você precisa buscar. |\n"
            "| `produtos` | array | Produtos da página atual (tamanho ≤ `tamanho_pagina`) |\n"
            "| `total_kits` | integer | Total de **kits** cadastrados. **Sempre presente.** |\n"
            "| `kits` | array | Todos os kits do cadastro, com seus itens. **Sempre presente** na listagem de produtos (não é paginado). Ver estrutura abaixo. |\n\n"
            "### Cada item em `produtos[]`\n\n"
            "| Campo | Tipo | Descrição |\n"
            "| --- | --- | --- |\n"
            "| `produto_id` | integer | ID interno do produto no SADI |\n"
            "| `cod_barras` | string | EAN/código de barras. Vazio se não cadastrado. |\n"
            "| `produto` | string | Nome/descrição do produto |\n"
            "| `produto_resumido` | string | Descrição enxuta/reduzida do produto. Vazio se não cadastrada. |\n"
            "| `fabricante` | string | Fabricante ou laboratório |\n"
            "| `categoria` | string | Categoria comercial (ex: `GENERICOS`, `SIMILARES`, `ETICOS`, `PERFUMARIA`) |\n"
            "| `sub_categoria` | string | Sub-categoria comercial do produto. Vazia se não cadastrada. |\n"
            "| `apresentacao` | string | Código de apresentação/embalagem no cadastro |\n"
            "| `cod_tributacao` | string | Código de tributação fiscal (ex: `F`, `T`, `I`). Também disponível dentro de `fiscal`. |\n"
            "| `localizacao` | string | Localização física do produto na loja (gôndola/prateleira). Vazio se não cadastrada. |\n"
            "| `localizacao_id` | integer \\| null | ID da localização, se houver |\n"
            "| `localizacao_descricao` | string \\| null | Descrição textual da localização |\n"
            "| `psicotropico` | string | `\"S\"` = psicotrópico, `\"N\"` = comum |\n"
            "| `antimicrobiano` | string | `\"S\"` = antimicrobiano, `\"N\"` = não |\n"
            "| `lista` | string | Classificação da lista de controle (ex: `A1`, `A2`, `A3`, `B1`, `B2`, `C1`). Vazio se não aplicável. |\n"
            "| `lastupdate` | string | Data/hora da última alteração no cadastro — formato `dd/mm/yyyy hh:mm:ss` |\n"
            "| `inicio_promocao` | string | Início da promoção — `dd/mm/yyyy`. Vazio se sem promoção. |\n"
            "| `termino_promocao` | string | Fim da promoção — `dd/mm/yyyy`. Vazio se sem promoção. |\n"
            "| `saldo` | number | Saldo atual em estoque |\n"
            "| `preco_venda` | number | Preço de venda normal (sem promoção) |\n"
            "| `preco_crediario` | number | Preço à prazo (crediário). `0` se não aplicável. |\n"
            "| `valor_venda` | number | Preço **efetivo** de venda considerando promoção ativa. Igual a `preco_venda` se não houver promoção. |\n"
            "| `padrao_comissao` | number | Percentual padrão de comissão do produto |\n"
            "| `valor_ult_compra` | number | Custo da última compra do produto (referência de custo) |\n"
            "| `leve_x_pague_y` | object \\| null | Promoção **leve X pague Y**, se aplicável. Ver estrutura abaixo. |\n"
            "| `fiscal` | object | Dados fiscais do produto. **Sempre presente.** Ver estrutura abaixo. |\n"
            "| `desconto_escalonado` | array | Faixas de desconto por quantidade. Vazio se não aplicável. |\n\n"
            "### `fiscal`\n\n"
            "Dados fiscais do cadastro do produto. Campos ausentes no cadastro vêm como string vazia (`\"\"`).\n\n"
            "| Campo | Tipo | Descrição |\n"
            "| --- | --- | --- |\n"
            "| `ncm` | string | NCM (Nomenclatura Comum do Mercosul) do produto |\n"
            "| `cest` | string | CEST (Código Especificador da Substituição Tributária). Vazio se não aplicável. |\n"
            "| `unidade` | string | Unidade de medida do produto (ex: `UND`, `CX`, `FR`) |\n"
            "| `cst_pis` | string | CST do PIS (ex: `01`, `04`, `06`) |\n"
            "| `cst_cofins` | string | CST do COFINS (ex: `01`, `04`, `06`) |\n"
            "| `cod_tributacao` | string | Código de tributação (CSOSN/CST de ICMS conforme o regime). Mesmo valor do `cod_tributacao` da raiz. |\n"
            "| `registro_ms` | string | Registro no Ministério da Saúde / ANVISA. Vazio se não aplicável. |\n"
            "| `info_adicional` | string | Informações adicionais/observação fiscal do produto. Vazio se não cadastrada. |\n\n"
            "### `leve_x_pague_y` (quando não é `null`)\n\n"
            "| Campo | Tipo | Descrição |\n"
            "| --- | --- | --- |\n"
            "| `leve` | integer | Quantidade que o cliente leva |\n"
            "| `pague` | integer | Quantidade que o cliente paga |\n"
            "| `tipo_preco` | string | `\"V\"` = base é o **preço de venda**; `\"P\"` = base é o **preço de promoção** |\n\n"
            "### Cada item em `desconto_escalonado[]`\n\n"
            "| Campo | Tipo | Descrição |\n"
            "| --- | --- | --- |\n"
            "| `quantidade` | integer | Quantidade mínima a partir da qual a faixa se aplica |\n"
            "| `valor` | number | Percentual de desconto (%) aplicado ao atingir a `quantidade` |\n\n"
            "### Cada item em `kits[]`\n\n"
            "| Campo | Tipo | Descrição |\n"
            "| --- | --- | --- |\n"
            "| `kit_id` | integer | ID interno do kit |\n"
            "| `kit_nome` | string | Nome/descrição do kit |\n"
            "| `kit_ativo` | string | `\"S\"` = ativo, `\"N\"` = inativo |\n"
            "| `kit_saldo` | number | Saldo do kit |\n"
            "| `lastupdate` | string \\| null | Data/hora da alteração mais recente entre os produtos do kit — `dd/mm/yyyy hh:mm:ss`. `null` se o kit não tiver itens ativos. |\n"
            "| `itens` | array | Produtos que compõem o kit. Ver estrutura abaixo. |\n\n"
            "### Cada item em `kits[].itens[]`\n\n"
            "| Campo | Tipo | Descrição |\n"
            "| --- | --- | --- |\n"
            "| `kit_item_id` | integer | ID do item dentro do kit |\n"
            "| `produto_id` | integer | ID interno do produto no SADI |\n"
            "| `produto` | string | Nome/descrição do produto |\n"
            "| `cod_barras` | string | EAN/código de barras do produto |\n"
            "| `quantidade` | number | Quantidade desse produto no kit |\n"
            "| `valor` | number | Valor do item praticado **dentro do kit** |\n"
            "| `valor_kit` | number | Igual a `valor` — preço do item no kit |\n"
            "| `valor_promo` | number | Preço de promoção do produto (`0` se não houver promoção vigente) |\n"
            "| `valor_base` | number | Preço de venda base do produto (fora do kit) |\n\n"
            "### Modo `apenas_kits`\n\n"
            "Com `\"apenas_kits\": true` a rota **não consulta produtos** e a raiz muda "
            "levemente: `produtos` vem vazio (`[]`) e o total de produtos aparece como "
            "`total_produtos` (sempre `0`) em vez de `total_registros`. Os arrays `kits` / "
            "`total_kits` seguem o **mesmo formato** descrito acima.\n"
        ),
        "notas": [
            "Os `kits` **sempre acompanham** a listagem de produtos — não é preciso pedir. "
            "Use `\"apenas_kits\": true` apenas quando quiser **exclusivamente os kits** "
            "(sem trafegar os produtos).",
            "O array `kits` **não é paginado**: traz todos os kits do cadastro em qualquer "
            "página. Já `produtos` respeita `pagina` / `tamanho_pagina`.",
            "Os parâmetros `integracao` / `apenas_integracao` são **legados** e estão em "
            "desuso; não têm efeito sobre os kits.",
        ],
    },

    # ==================================================================
    # Vendas
    # ==================================================================
    "InserirPreVenda": {
        "descricao": (
            "Registra um **pedido de pré-venda** (ex: pedido delivery). A pré-venda fica "
            "pendente no PDV até ser processada pelo operador da farmácia.\n\n"
            "O `params` tem três chaves: `venda` (cabeçalho), `venda_item` (itens) e "
            "`delivery` (endereço)."
        ),
        "params_grupos": [
            {
                "nome": "venda",
                "tipo": "object",
                "descricao": "Cabeçalho da venda — totais, cliente e forma de pagamento.",
                "params": [
                    {"campo": "venda_total",    "tipo": "number",  "obrigatorio": "Sim", "default": None,  "descricao": "Valor total da venda"},
                    {"campo": "venda_recebido", "tipo": "number",  "obrigatorio": "Sim", "default": None,  "descricao": "Valor recebido do cliente"},
                    {"campo": "cartao_atd",     "tipo": "string",  "obrigatorio": "Não", "default": None,  "descricao": "Número do cartão de atendimento"},
                    {"campo": "pedido",         "tipo": "string",  "obrigatorio": "Não", "default": '""',  "descricao": "Número do pedido externo"},
                    {"campo": "v_id",           "tipo": "string",  "obrigatorio": "Sim", "default": None,  "descricao": "ID do vendedor ou origem"},
                    {"campo": "origem_venda",   "tipo": "string",  "obrigatorio": "Não", "default": None,  "descricao": "Identificador da origem (ex: `\"IFOOD\"`, `\"POSTMAN\"`)"},
                    {"campo": "cliente_id",     "tipo": "string",  "obrigatorio": "Não", "default": '"0"', "descricao": "ID do cliente (`\"0\"` = venda avulsa)"},
                    {"campo": "delivery_id",    "tipo": "string",  "obrigatorio": "Não", "default": '"0"', "descricao": "ID do endereço de delivery"},
                    {"campo": "cliente",        "tipo": "string",  "obrigatorio": "Não", "default": None,  "descricao": "Nome do cliente"},
                    {"campo": "comprador",      "tipo": "string",  "obrigatorio": "Não", "default": None,  "descricao": "Nome do comprador"},
                    {"campo": "fpagto",         "tipo": "string",  "obrigatorio": "Sim", "default": None,  "descricao": 'Código da forma de pagamento (ex: `"0"` = dinheiro)'},
                    {"campo": "cpf_cliente",    "tipo": "string",  "obrigatorio": "Não", "default": None,  "descricao": "CPF do cliente (sem formatação)"},
                    {"campo": "token",          "tipo": "string",  "obrigatorio": "Não", "default": None,  "descricao": "Token único do pedido (idempotência)"},
                    {"campo": "frete",          "tipo": "number",  "obrigatorio": "Não", "default": "0",   "descricao": "Valor do frete"},
                    {"campo": "troco",          "tipo": "number",  "obrigatorio": "Não", "default": "0",   "descricao": "Valor do troco"},
                    {"campo": "obs",            "tipo": "string",  "obrigatorio": "Não", "default": '""',  "descricao": "Observações do pedido"},
                ],
            },
            {
                "nome": "venda_item",
                "tipo": "array",
                "descricao": "Itens da venda — um objeto por produto.",
                "params": [
                    {"campo": "p_id",            "tipo": "string",  "obrigatorio": "Sim", "default": None, "descricao": "EAN/código de barras do produto"},
                    {"campo": "qtde",            "tipo": "number",  "obrigatorio": "Sim", "default": None, "descricao": "Quantidade"},
                    {"campo": "prt",             "tipo": "number",  "obrigatorio": "Sim", "default": None, "descricao": "Preço de tabela"},
                    {"campo": "prv",             "tipo": "number",  "obrigatorio": "Sim", "default": None, "descricao": "Preço de venda"},
                    {"campo": "vv",              "tipo": "number",  "obrigatorio": "Sim", "default": None, "descricao": "Valor total do item"},
                    {"campo": "desc",            "tipo": "number",  "obrigatorio": "Não", "default": "0",  "descricao": "Valor de desconto"},
                    {"campo": "c_tr",            "tipo": "string",  "obrigatorio": "Não", "default": '"F"',"descricao": 'Código de tributação (ex: `"F"`)'},
                    {"campo": "v_id",            "tipo": "string",  "obrigatorio": "Não", "default": None, "descricao": "ID do vendedor"},
                    {"campo": "padrao_comissao", "tipo": "number",  "obrigatorio": "Não", "default": "0",  "descricao": "Percentual de comissão"},
                ],
            },
            {
                "nome": "pagamento",
                "tipo": "array",
                "descricao": "Formas de pagamento utilizadas.",
                "params": [
                    {"campo": "f", "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": 'Nome da forma (ex: `"dinheiro"`, `"cartao"`)'},
                    {"campo": "a", "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "Valor pago nesta forma"},
                    {"campo": "n", "tipo": "string", "obrigatorio": "Não", "default": '""', "descricao": "NSU / número da transação"},
                    {"campo": "i", "tipo": "string", "obrigatorio": "Não", "default": '"1"',"descricao": "Número de parcelas"},
                    {"campo": "b", "tipo": "string", "obrigatorio": "Não", "default": '""', "descricao": 'Bandeira (ex: `"visa"`)'},
                ],
            },
            {
                "nome": "delivery",
                "tipo": "object",
                "descricao": "Endereço de entrega. Pode ser omitido se não houver delivery.",
                "params": [
                    {"campo": "nom", "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "Nome do destinatário"},
                    {"campo": "end", "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "Logradouro"},
                    {"campo": "num", "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "Número"},
                    {"campo": "bai", "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "Bairro"},
                    {"campo": "cid", "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "Cidade"},
                    {"campo": "cep", "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "CEP (8 dígitos, sem formatação)"},
                    {"campo": "uf",  "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "Estado (sigla de 2 letras)"},
                    {"campo": "com", "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Complemento"},
                    {"campo": "ref", "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Ponto de referência"},
                    {"campo": "tel", "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Telefone fixo"},
                    {"campo": "cel", "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Celular"},
                ],
            },
        ],
        "exemplo_body": {
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
                    "obs": "",
                },
                "venda_item": [{
                    "p_id": "7891800662122",
                    "qtde": 2,
                    "prt": 33.8,
                    "prv": 33.8,
                    "vv": 33.8,
                    "desc": 0,
                    "c_tr": "F",
                    "v_id": "1",
                    "padrao_comissao": 0,
                }],
                "pagamento": [{"f": "dinheiro", "a": "77.59", "n": "", "i": "1", "b": ""}],
                "delivery": {
                    "tel": "", "cel": "",
                    "nom": "Cliente Exemplo",
                    "end": "Rua Exemplo", "num": "100",
                    "com": "Casa", "ref": "",
                    "bai": "Centro", "cid": "Belo Horizonte",
                    "cep": "30000000", "uf": "MG",
                },
            }
        },
        "exemplo_resposta": {
            "result": [{"success": True, "venda_id": 45678, "msg": "Pré-venda criada"}]
        },
        "notas": [
            "Envie um `token` único por pedido para evitar duplicidade em caso de reenvio.",
        ],
    },

    "CancelarPreVenda": {
        "descricao": (
            "Cancela uma **pré-venda** previamente registrada via `InserirPreVenda`. "
            "O cancelamento é **lógico** — não devolve saldo de estoque, não mexe em "
            "NFC-e nem em valores de pagamento. É idempotente: chamar novamente sobre "
            "uma venda já cancelada não gera erro."
        ),
        "params": [
            {"campo": "id_venda", "tipo": "integer", "obrigatorio": "Sim", "default": None, "descricao": "ID da venda a cancelar (deve ser > 0)"},
        ],
        "exemplo_body": {
            "cnpj": "02695980000110",
            "params": {"id_venda": 12345}
        },
        "exemplo_resposta": {
            "result": [{"success": True, "id_venda": 12345, "cancelado": "S"}]
        },
        "notas": [
            "Venda não encontrada → `{ \"success\": false, \"id_venda\": 12345, \"message\": \"Venda não encontrada\" }`",
            "`id_venda` ausente → `{ \"success\": false, \"message\": \"id_venda não informado\" }`",
            "`id_venda` <= 0 → `{ \"success\": false, \"message\": \"id_venda inválido\" }`",
            "JSON inválido → `{ \"success\": false, \"message\": \"JSON inválido\" }`",
        ],
    },

    "InserirNotaFiscal": {
        "descricao": (
            "Grava uma **nota fiscal de saída** para pedidos de e-commerce.\n\n"
            "- Registra cabeçalho, itens e formas de pagamento da nota.\n"
            "- Baixa o **estoque** dos produtos vendidos.\n"
            "- Cria (ou reusa) automaticamente o cadastro do destinatário a partir do CPF/CNPJ.\n\n"
            "Esta rota **não emite** NFC-e/NF-e via SEFAZ — apenas grava a nota no Sadi. "
            "A emissão fiscal é responsabilidade de outro módulo que consome a nota gravada.\n\n"
            "**Idempotência:** se `pedido` vier preenchido e já existir uma nota de saída "
            "com esse número de pedido, a rota retorna o `nota_id` existente em vez de duplicar."
        ),
        "params_grupos": [
            {
                "nome": "venda",
                "tipo": "object",
                "descricao": "Cabeçalho da nota — totais, número do pedido, origem.",
                "params": [
                    {"campo": "venda_total",    "tipo": "number", "obrigatorio": "Sim", "default": None,  "descricao": "Valor total da nota"},
                    {"campo": "pedido",         "tipo": "string", "obrigatorio": "Não", "default": '""',  "descricao": "Número do pedido externo (usado para idempotência)"},
                    {"campo": "origem_venda",   "tipo": "string", "obrigatorio": "Não", "default": None,  "descricao": 'Identificador da origem (ex: `"ECOMMERCE"`). Cria/reusa automaticamente o cadastro dessa origem.'},
                    {"campo": "v_id",           "tipo": "string", "obrigatorio": "Não", "default": '"0"', "descricao": "Vendedor responsável pela nota — aceita **ID (numérico)** ou **código/nome**. Se não for numérico, o Sadi resolve pra ID via cadastro (mesma regra do `InserirPreVenda`). Padrão `0`."},
                    {"campo": "cfop",           "tipo": "string", "obrigatorio": "Não", "default": None,  "descricao": 'CFOP da nota (ex: `"5102"` intra, `"6108"` inter, consumidor final). Se ausente, o módulo de emissão preenche. Pode ser sobrescrito por item.'},
                    {"campo": "frete",          "tipo": "number", "obrigatorio": "Não", "default": "0",   "descricao": "Valor do frete"},
                    {"campo": "venda_desconto", "tipo": "number", "obrigatorio": "Não", "default": "0",   "descricao": "Desconto aplicado"},
                ],
            },
            {
                "nome": "destinatario",
                "tipo": "object",
                "descricao": "Dados fiscais e endereço do destinatário da NF. Traz os campos que a SEFAZ exige.",
                "params": [
                    {"campo": "cpf_cnpj", "tipo": "string", "obrigatorio": "Sim",   "default": None, "descricao": "CPF (11 dígitos) ou CNPJ (14 dígitos), só números."},
                    {"campo": "nome",     "tipo": "string", "obrigatorio": "Sim",   "default": None, "descricao": "Nome do destinatário (PF) ou razão social (PJ)."},
                    {"campo": "ie",       "tipo": "string", "obrigatorio": "Cond.", "default": None, "descricao": 'Inscrição Estadual. **Obrigatória para CNPJ** — se ausente, a nota é rejeitada. Para **CPF**, se omitida o Sadi grava `ISENTO` automaticamente. PJ isento pode enviar `"ISENTO"` explicitamente.'},
                    {"campo": "email",    "tipo": "string", "obrigatorio": "Não",   "default": None, "descricao": "E-mail para envio da DANFE."},
                    {"campo": "end",      "tipo": "string", "obrigatorio": "Sim",   "default": None, "descricao": "Logradouro"},
                    {"campo": "num",      "tipo": "string", "obrigatorio": "Sim",   "default": None, "descricao": "Número"},
                    {"campo": "com",      "tipo": "string", "obrigatorio": "Não",   "default": None, "descricao": "Complemento"},
                    {"campo": "bai",      "tipo": "string", "obrigatorio": "Sim",   "default": None, "descricao": "Bairro"},
                    {"campo": "cid",      "tipo": "string", "obrigatorio": "Sim",   "default": None, "descricao": "Cidade"},
                    {"campo": "cep",      "tipo": "string", "obrigatorio": "Sim",   "default": None, "descricao": "CEP (só dígitos)"},
                    {"campo": "uf",       "tipo": "string", "obrigatorio": "Sim",   "default": None, "descricao": "Estado (sigla)"},
                    {"campo": "tel",      "tipo": "string", "obrigatorio": "Não",   "default": None, "descricao": "Telefone fixo"},
                    {"campo": "cel",      "tipo": "string", "obrigatorio": "Não",   "default": None, "descricao": "Celular"},
                ],
            },
            {
                "nome": "venda_item",
                "tipo": "array",
                "descricao": "Itens da nota — um objeto por produto.",
                "params": [
                    {"campo": "p_id", "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "EAN ou PRODUTO_ID"},
                    {"campo": "qtde", "tipo": "number", "obrigatorio": "Sim", "default": None, "descricao": "Quantidade"},
                    {"campo": "prv",  "tipo": "number", "obrigatorio": "Sim", "default": None, "descricao": "Preço de venda unitário"},
                    {"campo": "desc", "tipo": "number", "obrigatorio": "Não", "default": "0",  "descricao": "Desconto do item"},
                    {"campo": "cfop", "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "CFOP específico do item (sobrescreve `venda.cfop`). Útil quando o item tem ST diferente."},
                ],
            },
            {
                "nome": "pagamento",
                "tipo": "array",
                "descricao": "Formas de pagamento (opcional).",
                "params": [
                    {"campo": "f", "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": 'Nome da forma (ex: `"dinheiro"`, `"cartao"`, `"pix"`, `"boleto"`). Qualquer variante de cartão mapeia para Cartão; forma não reconhecida cai em Dinheiro.'},
                    {"campo": "a", "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "Valor pago nesta forma"},
                    {"campo": "n", "tipo": "string", "obrigatorio": "Não", "default": '""', "descricao": "NSU / número da transação"},
                    {"campo": "i", "tipo": "string", "obrigatorio": "Não", "default": '"1"',"descricao": "Número de parcelas"},
                    {"campo": "b", "tipo": "string", "obrigatorio": "Não", "default": '""', "descricao": 'Bandeira (ex: `"visa credito"`)'},
                ],
            },
        ],
        "exemplo_body": {
            "cnpj": "02695980000110",
            "params": {
                "venda": {
                    "venda_total": 77.59,
                    "pedido": "ECOM-12345",
                    "origem_venda": "ECOMMERCE",
                    "v_id": "1",
                    "cfop": "5102",
                    "frete": 0,
                    "venda_desconto": 0,
                },
                "destinatario": {
                    "cpf_cnpj": "11658675673",
                    "nome": "Tamer Sammour",
                    "ie": "ISENTO",
                    "email": "tamer@exemplo.com",
                    "end": "R. Cândido Neiva", "num": "59",
                    "com": "Casa De Pedra",
                    "bai": "Centro", "cid": "PARACATU",
                    "cep": "38600000", "uf": "MG",
                    "cel": "38999999999",
                },
                "venda_item": [
                    {"p_id": "7891800662122", "qtde": 2, "prv": 33.8, "desc": 0},
                    {"p_id": "7899547500363", "qtde": 1, "prv": 9.99, "desc": 0},
                ],
                "pagamento": [{"f": "cartao", "a": "77.59", "n": "123456", "i": "1", "b": "visa credito"}],
            }
        },
        "exemplo_resposta": {
            "result": [{
                "success": True,
                "id_nota": 45678,
                "numero_nota_fiscal": "12345",
                "id_destinatario": 1234,
                "numero_pedido": "ECOM-12345",
            }]
        },
        "notas": [
            "`numero_nota_fiscal` é o número fiscal sequencial da NF de saída (gerado no momento da gravação). Fica alocado desde já — numeração fiscal brasileira não pode ser reusada.",
            "`id_destinatario` é o ID interno do destinatário nos cadastros do PDV.",
            "**CFOP/CST/CSOSN preenchidos automaticamente**: o PDV usa a config fiscal da loja + tributação de cada produto, compara UF do destinatário com UF da loja (`dentro`/`fora`) e aplica CST ou CSOSN conforme o regime tributário. Se `venda.cfop` ou `venda_item[].cfop` vierem no payload, sobrescrevem o CFOP calculado.",
            "`destinatario.cpf_cnpj` ausente → `{ \"success\": false, \"message\": \"cpf_cnpj do destinatario obrigatorio para emissao de nota fiscal\" }`",
            "**IE obrigatória para CNPJ**: destinatário PJ sem `ie` → `{ \"success\": false, \"message\": \"IE do destinatario obrigatoria para CNPJ — informe o campo \\\"ie\\\" no JSON\" }`. Para CPF, a ausência de `ie` grava `ISENTO` automaticamente.",
            "**Cadastro do destinatário:** se o CPF/CNPJ já existe, o Sadi apenas **completa os campos vazios** (IE, endereço, contato) com o que vier no JSON — nunca sobrescreve dados já preenchidos. Se não existe, cria o cadastro.",
            "**Frete rateado:** o `venda.frete` do cabeçalho é distribuído proporcionalmente entre os itens (pelo valor líquido de cada linha); o resíduo de arredondamento vai no último item.",
            "Produto não localizado → `{ \"success\": false, \"message\": \"Produto nao encontrado: <p_id>\" }`",
            "**Validação de saldo:** se a loja não permite venda com estoque negativo, a rota rejeita quando algum produto não tem saldo suficiente, retornando `{ \"success\": false, \"message\": \"Produto sem saldo suficiente\", \"produtos_sem_saldo\": [{ \"produto_id\": 123, \"produto\": \"NIMESULIDA 100MG\", \"saldo\": 3, \"solicitado\": 10 }] }`.",
            "Idempotência: se `pedido` já existir em outra nota, retorna a nota existente sem erro (`success: true`) — incluindo o `numero_nota_fiscal` já atribuído.",
            "A rota **não transmite** NFC-e/NF-e à SEFAZ — a transmissão fiscal é feita por outro módulo consumindo a nota gravada.",
        ],
    },

    "CancelarNotaFiscal": {
        "descricao": (
            "Cancela uma **nota fiscal** previamente registrada via `InserirNotaFiscal`. "
            "Marca a nota como cancelada e **devolve o estoque** dos itens "
            "(operação simétrica à baixa feita na inserção).\n\n"
            "Se a nota já foi transmitida à SEFAZ, esta rota **não** faz o cancelamento fiscal — "
            "apenas o cancelamento lógico no PDV. O cancelamento fiscal é responsabilidade "
            "do módulo de emissão."
        ),
        "params": [
            {"campo": "id_nota", "tipo": "integer", "obrigatorio": "Sim", "default": None, "descricao": "ID da nota a cancelar (deve ser > 0). Retornado por `InserirNotaFiscal` em `id_nota`."},
        ],
        "exemplo_body": {
            "cnpj": "02695980000110",
            "params": {"id_nota": 45678}
        },
        "exemplo_resposta": {
            "result": [{"success": True, "id_nota": 45678, "cancelado": "S"}]
        },
        "notas": [
            "Nota não encontrada → `{ \"success\": false, \"id_nota\": 45678, \"message\": \"Nota nao encontrada\" }`",
            "`id_nota` ausente → `{ \"success\": false, \"message\": \"id_nota nao informado\" }`",
            "`id_nota` <= 0 → `{ \"success\": false, \"message\": \"id_nota invalido\" }`",
            "O estoque dos itens é **devolvido** automaticamente (simétrico ao baixado na inserção).",
        ],
    },

    "ListaVendas": {
        "descricao": (
            "Lista vendas com seus itens e pagamentos. Suporta **três modos de consulta** — "
            "escolha via `tipo_consulta`. Ideal para sincronizações incrementais usando o modo "
            "`ALTERACAO`."
        ),
        "params": [
            {"campo": "tipo_consulta",       "tipo": "string", "obrigatorio": "Sim",         "default": None, "descricao": '`"DATA"`, `"CODIGO"` ou `"ALTERACAO"`'},
            {"campo": "data_inicio",         "tipo": "string", "obrigatorio": "Condicional", "default": None, "descricao": 'Formato `yyyy-mm-dd`. Obrigatório se `tipo_consulta = "DATA"`'},
            {"campo": "data_fim",            "tipo": "string", "obrigatorio": "Condicional", "default": None, "descricao": 'Formato `yyyy-mm-dd`. Obrigatório se `tipo_consulta = "DATA"`'},
            {"campo": "venda_id",            "tipo": "string", "obrigatorio": "Condicional", "default": None, "descricao": 'ID da venda. Obrigatório se `tipo_consulta = "CODIGO"`'},
            {"campo": "data_hora_alteracao", "tipo": "string", "obrigatorio": "Condicional", "default": None, "descricao": 'Formato `yyyy-mm-dd hh:nn:ss`. Obrigatório se `tipo_consulta = "ALTERACAO"`'},
            {"campo": "origem_venda",        "tipo": "string", "obrigatorio": "Não",         "default": '""',"descricao": 'Filtra por origem (ex: `"IFOOD"`). Opcional em qualquer modo'},
        ],
        "exemplo_body": {
            "cnpj": "02695980000110",
            "params": {
                "tipo_consulta": "DATA",
                "data_inicio": "2025-10-01",
                "data_fim": "2025-10-09",
                "origem_venda": "",
            }
        },
        "exemplo_resposta": [{
            "venda_id": 12457,
            "cnpj": "02695980000110",
            "data_venda": "2025-09-28 14:32:00.0000",
            "valor_total": 253.90,
            "cliente": "JOÃO SILVA",
            "status": "VENDA_CONCLUIDA",
            "descricao": "Venda concluída",
            "nfce_chave": "31250902695980000110650010000001231000012310",
            "itens": [{"produto_id": 4855, "produto": "DIPIRONA 500MG"}],
            "pagamentos": [{"tipo_pagamento": "Cartão de Débito"}],
        }],
        "notas": [
            "O modo `ALTERACAO` considera criação, encerramento, emissão de NFC-e e "
            "lançamento de comissão — ideal para **sincronização incremental**.",
            "Ver seção *Status de venda* na descrição da coleção para todos os valores possíveis do campo `status`.",
        ],
    },

    "GetStatusVenda": {
        "descricao": "Retorna o **status atual** de uma venda pelo seu ID interno.",
        "params": [
            {"campo": "venda_id", "tipo": "integer", "obrigatorio": "Sim", "default": None, "descricao": "ID interno da venda"},
        ],
        "exemplo_body": {
            "cnpj": "02695980000110",
            "params": {"venda_id": 12457}
        },
        "exemplo_resposta": {
            "venda_id": 12457,
            "data_venda": "2025-09-28 14:32:00.0000",
            "valor_total": 253.90,
            "status": "PEDIDO_ENTREGUE",
            "descricao": "Pedido entregue",
        },
        "notas": [
            "Valores possíveis do campo `status`: `VENDA_PENDENTE`, `VENDA_CONCLUIDA`, "
            "`SEPARADO_PARA_ENTREGA`, `ADICIONADO_ROTA_ENTREGA`, `SAIU_PARA_ENTREGA`, "
            "`PEDIDO_ENTREGUE`.",
        ],
    },

    # ==================================================================
    # Utilitários
    # ==================================================================
    "Ping": {
        "descricao": "Verifica se a API está **online e respondendo**. Útil como heartbeat.",
        "exemplo_body": {"cnpj": "02695980000110", "params": None},
        "exemplo_resposta": {"result": ["ok"]},
        "notas": [],
    },

    "SetSenha": {
        "descricao": (
            "Define uma **senha alfanumérica** vinculada ao CNPJ de uma loja. "
            "Recurso **opt-in**, criado a pedido de parceiro que preferia trafegar a "
            "própria senha como reforço adicional em cada requisição.\n\n"
            "**Como funciona:**\n\n"
            "- Se, numa chamada da API, a integradora **enviar** o header "
            "`x-digifarma-senha` → a API valida contra a senha definida. Se bater, "
            "aprova; se não bater, rejeita.\n"
            "- Se **não enviar** o header → a API ignora essa camada e segue com a "
            "autenticação padrão (`x-digifarma-user` + `x-digifarma-token`) normalmente.\n\n"
            "Ou seja: mesmo depois de definir a senha, você continua livre para chamar "
            "as rotas sem o header. A senha só é conferida quando o header aparece — é "
            "**decisão da integradora**, chamada a chamada.\n\n"
            "**Body enviado como form-data direto** (sem o campo `json` — diferente das demais rotas)."
        ),
        "body_tipo": "form-data-direto",
        "params": [
            {"campo": "cnpj",  "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "CNPJ da loja para a qual a senha será definida"},
            {"campo": "senha", "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "Senha alfanumérica a ser vinculada ao CNPJ"},
        ],
        "exemplo_body_raw": "cnpj=02695980000110\nsenha=1234567",
        "exemplo_resposta": {"success": True},
        "notas": [],
    },

}


# Doc geral que fica em info.description do collection — mantida enxuta.
INFO_DESCRICAO_GERAL = """# API SADI — Documentação de integração

Base URL: `https://sadi.digifarma.com.br/api/`

Cada endpoint tem sua **própria página de documentação** com parâmetros, campos obrigatórios/opcionais e exemplos — abra o endpoint desejado na coluna à esquerda.

---

## Autenticação

Todas as requisições — exceto `GetToken` e `SetSenha` — exigem os headers:

| Header | Descrição |
| --- | --- |
| `x-digifarma-user` | Usuário fornecido pela Digifarma |
| `x-digifarma-token` | Token obtido via `GetToken` |

Fluxo:

1. Chame `GetToken` enviando o CNPJ da integradora → recebe um `token`.
2. Envie o `token` no header `x-digifarma-token` em todas as chamadas subsequentes.
3. Renove chamando `GetToken` novamente quando expirar.

---

## Formato padrão do body

Todas as requisições usam método **`POST`** e body como **`form-data`**.

Salvo **`GetToken`** e **`SetSenha`** (que enviam os campos diretamente), o form-data tem **um único campo `json`** com o seguinte conteúdo:

```json
{
    "cnpj": "SEU_CNPJ",
    "params": { ...parâmetros específicos do endpoint... }
}
```

| Campo | Tipo | Obrigatório | Descrição |
| --- | --- | --- | --- |
| `cnpj` | string | Sim | CNPJ da loja (somente dígitos) |
| `params` | object \\| null | Varia | Parâmetros específicos do endpoint. Pode ser `null` quando não há parâmetros. |

---

## Status de venda — referência

Os endpoints `ListaVendas` e `GetStatusVenda` retornam o campo `status` com estes valores possíveis:

| Status | Descrição |
| --- | --- |
| `VENDA_PENDENTE` | Venda aguardando fechamento pelo operador |
| `VENDA_CONCLUIDA` | Venda finalizada com sucesso |
| `SEPARADO_PARA_ENTREGA` | Pedido separado, aguardando entregador |
| `ADICIONADO_ROTA_ENTREGA` | Pedido adicionado à rota de entrega |
| `SAIU_PARA_ENTREGA` | Pedido saiu para entrega |
| `PEDIDO_ENTREGUE` | Pedido entregue ao cliente |
"""
