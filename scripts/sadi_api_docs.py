"""
Fonte única da verdade para a documentação da API do SADI.

Cada endpoint é descrito como um dict com:
- descricao        : texto de abertura (aceita markdown)
- headers_extras   : headers além dos padrão x-digifarma-user/x-digifarma-token
                     (ex: GetToken só usa x-digifarma-user)
- sem_token        : True se não precisa de x-digifarma-token (só GetToken)
- body_tipo        : "form-data-direto" (GetToken/SetSenha) ou "form-data-json" (default)
- params           : lista simples de campos em params (dicts com campo/tipo/obrigatorio/default/descricao)
- params_grupos    : lista de grupos, cada um com params (para InserirPreVenda/InserirCliente)
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
    "InserirCliente": {
        "descricao": (
            "Cadastra um **novo cliente** ou atualiza um existente.\n\n"
            "- Para inserir: envie `CLIENTE_ID = \"0\"`.\n"
            "- Para atualizar: envie o `CLIENTE_ID` do registro existente.\n\n"
            "O array `CLIENTE` deve conter exatamente **1 objeto**."
        ),
        "params_grupos": [
            {
                "nome": "CLIENTE",
                "tipo": "array (1 objeto)",
                "descricao": "Dados do cliente a inserir/atualizar",
                "params": [
                    {"campo": "CLIENTE_ID",         "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": '`"0"` = novo cliente; ID existente = atualiza'},
                    {"campo": "CLIENTE",            "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "Nome completo do cliente (maiúsculas)"},
                    {"campo": "CLI_CPF",            "tipo": "string", "obrigatorio": "Sim", "default": None, "descricao": "CPF sem formatação (11 dígitos)"},
                    {"campo": "CLI_RG",             "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "RG do cliente"},
                    {"campo": "CLI_ENDERECO",      "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Logradouro"},
                    {"campo": "CLI_NUMERO",         "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Número do endereço"},
                    {"campo": "CLI_BAIRRO",         "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Bairro"},
                    {"campo": "CLI_CIDADE",         "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Cidade"},
                    {"campo": "CLI_CEP",            "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "CEP sem formatação (8 dígitos)"},
                    {"campo": "CLI_UF",             "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Estado (sigla de 2 letras)"},
                    {"campo": "CLI_TELEFONE",       "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Telefone fixo"},
                    {"campo": "CLI_CELULAR",        "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Celular"},
                    {"campo": "CLI_EMAIL",          "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "E-mail"},
                    {"campo": "CLI_SEXO",           "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": '`"M"` = Masculino, `"F"` = Feminino'},
                    {"campo": "CLI_ESTADO_CIVIL",   "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": '`"S"`=solteiro, `"C"`=casado, `"D"`=divorciado, `"V"`=viúvo'},
                    {"campo": "CLI_NASCIMENTO",     "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Data de nascimento `yyyy-mm-dd`"},
                    {"campo": "CLI_CONJUGE",        "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Nome do cônjuge"},
                    {"campo": "CLI_PAI",            "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Nome do pai"},
                    {"campo": "CLI_MAE",            "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Nome da mãe"},
                    {"campo": "CADASTRO_VENDEDOR_ID","tipo":"string", "obrigatorio": "Não", "default": None, "descricao": "ID do vendedor que fez o cadastro"},
                    {"campo": "CLI_SALARIO",        "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Salário do cliente"},
                    {"campo": "CLI_LIMITE",         "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Limite de crediário"},
                    {"campo": "CREDIARIO",          "tipo": "string", "obrigatorio": "Não", "default": '"FALSE"', "descricao": '`"TRUE"` ou `"FALSE"` — habilita crediário'},
                    {"campo": "CLI_BLOQUEADO",      "tipo": "string", "obrigatorio": "Não", "default": '"FALSE"', "descricao": '`"TRUE"` ou `"FALSE"` — bloqueia cliente'},
                    {"campo": "ORIGEM_CADASTRO_ID", "tipo": "string", "obrigatorio": "Não", "default": None, "descricao": "Identificador da origem do cadastro (ex: nome do sistema)"},
                ],
            }
        ],
        "exemplo_body": {
            "cnpj": "02695980000110",
            "params": {
                "CLIENTE": [{
                    "CLIENTE_ID": "0",
                    "CLIENTE": "JOÃO DA SILVA",
                    "CLI_CPF": "12345678901",
                    "CLI_NASCIMENTO": "1985-05-20",
                    "CLI_CELULAR": "31998765432",
                    "CREDIARIO": "FALSE",
                    "CLI_BLOQUEADO": "FALSE",
                    "ORIGEM_CADASTRO_ID": "MEUAPP",
                }]
            }
        },
        "exemplo_resposta": {
            "result": [{"success": True, "CLIENTE_ID": 12345}]
        },
        "notas": [],
    },

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
                "tipo_consulta": "CPF",
                "parametro": "12345678909",
                "pagina": 1,
                "tamanho_pagina": 20,
            }
        },
        "exemplo_resposta": {
            "result": [{
                "total_registros": 1,
                "clientes": [{
                    "cliente_id": 4521,
                    "cliente": "JOÃO DA SILVA",
                    "cli_cpf": "12345678909",
                    "cli_celular": "31999998888",
                    "cli_email": "joao@exemplo.com",
                    "cli_bloqueado": "FALSE",
                }]
            }]
        },
        "notas": [],
    },

    # ==================================================================
    # Produto
    # ==================================================================
    "ListaProduto": {
        "descricao": (
            "Consulta o **catálogo de produtos** da loja. Suporta busca por código, "
            "EAN, nome ou data de atualização, com paginação, ordenação e filtros de "
            "saldo e integração."
        ),
        "params": [
            {"campo": "tipo_consulta",    "tipo": "string",  "obrigatorio": "Sim", "default": None,          "descricao": '`"COD_INTERNO"`, `"EAN"`, `"NOME"` ou `"DATA"`'},
            {"campo": "parametro",        "tipo": "string",  "obrigatorio": "Não", "default": '""',          "descricao": 'Valor da busca. Para `DATA` use `"yyyy-mm-dd hh:nn:ss"`'},
            {"campo": "pagina",           "tipo": "integer", "obrigatorio": "Não", "default": "1",           "descricao": "Página desejada"},
            {"campo": "tamanho_pagina",   "tipo": "integer", "obrigatorio": "Não", "default": "20",          "descricao": "Registros por página"},
            {"campo": "saldo_positivo",   "tipo": "boolean", "obrigatorio": "Não", "default": "false",       "descricao": "Se `true`, retorna apenas produtos com saldo > 0"},
            {"campo": "ordenar_por",      "tipo": "string",  "obrigatorio": "Não", "default": '"produto_id"', "descricao": '`"PRODUTO"`, `"COD_BARRAS"`, `"FABRICANTE"`, `"CATEGORIA"`, `"SALDO"`, `"PRECO_VENDA"` ou `"LASTUPDATE"`'},
            {"campo": "ordem",            "tipo": "string",  "obrigatorio": "Não", "default": '"ASC"',       "descricao": '`"ASC"` ou `"DESC"`'},
            {"campo": "integracao",       "tipo": "string",  "obrigatorio": "Não", "default": '""',          "descricao": 'Filtra produtos vinculados a uma integração (ex: `"DIGIFARMA"`)'},
            {"campo": "apenas_integracao","tipo": "boolean", "obrigatorio": "Não", "default": "false",       "descricao": "Se `true`, retorna apenas produtos com vínculo em qualquer integração ativa"},
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
                "integracao": "",
                "apenas_integracao": False,
            }
        },
        "exemplo_resposta": {
            "result": [{
                "total_registros": 150,
                "produtos": [{
                    "produto_id": 12345,
                    "cod_barras": "7891234567890",
                    "produto": "PARACETAMOL 500MG",
                    "fabricante": "EMS",
                    "categoria": "ANALGÉSICO",
                    "saldo": 35.0,
                    "preco_venda": 12.50,
                    "leve_x_pague_y": None,
                    "desconto_escalonado": [],
                }]
            }]
        },
        "notas": [
            "Quando `integracao` ou `apenas_integracao` é utilizado, a resposta também "
            "inclui o array `kits` com kits de produtos ativos vinculados à integração.",
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
            "Define uma **senha alfanumérica** vinculada ao CNPJ de uma loja, funcionando "
            "como camada adicional de autenticação da integradora.\n\n"
            "**⚠ Comportamento importante:** a partir do momento em que uma senha é "
            "definida para um CNPJ, **todas as chamadas subsequentes da API a esse CNPJ "
            "passam a exigir o header `x-digifarma-senha`** com a senha correspondente. "
            "Requisições sem o header, ou com valor incorreto, são rejeitadas.\n\n"
            "Usar este endpoint é **opcional** — se você nunca chamar `SetSenha` para um "
            "CNPJ, a autenticação padrão (`x-digifarma-user` + `x-digifarma-token`) "
            "continua bastando. Chame apenas se quiser um segundo fator vinculado ao "
            "CNPJ atendido.\n\n"
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
