"""
Gera `openapi.json` (OpenAPI 3.1) a partir do `sadi_api_docs.py`.

Uso:
    python scripts/gerar_openapi.py

O arquivo gerado pode ser consumido por Fern, Swagger UI, Redoc, Postman
(via "Import as OpenAPI") e ferramentas de geração de SDK.

Notas sobre a modelagem:
  - Todas as rotas são `POST` e usam `multipart/form-data`.
  - Salvo `GetToken` e `SetSenha`, o body tem um único campo `json` (string) —
    o schema desse campo é documentado na `description`, com `example`
    contendo o JSON exato que a rota espera.
  - Headers `x-digifarma-user` e `x-digifarma-token` são declarados como
    parameters `in: header`.
"""

import json
import os
from typing import Any

from sadi_api_docs import ENDPOINTS


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_FILE = os.path.join(ROOT, "openapi.json")


def _op_id(nome: str) -> str:
    """Converte 'GetToken - Autenticação' em 'getToken'."""
    base = nome.split(" - ")[0].strip()
    return base[0].lower() + base[1:] if base else base


def _path_name(nome: str) -> str:
    return "/" + nome.split(" - ")[0].strip()


def _tag(nome: str) -> str:
    """Categoriza endpoints em grupos para o Fern/Swagger."""
    base = nome.split(" - ")[0]
    if base == "GetToken":
        return "Autenticação"
    if base in {"GetDadosLoja", "GetLojas"}:
        return "Loja"
    if base in {"InserirCliente", "ListaCliente"}:
        return "Cliente"
    if base == "ListaProduto":
        return "Produto"
    if base in {"InserirVenda", "InserirPreVenda", "ListaVendas", "GetStatusVenda"}:
        return "Vendas"
    if base in {"GetPromocoes", "GetRecorrencias", "GetPedidosProntos", "GetPontos"}:
        return "SADI Online"
    return "Utilitários"


def _headers(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    params: list[dict[str, Any]] = [
        {
            "name": "x-digifarma-user",
            "in": "header",
            "required": True,
            "description": "Usuário fornecido pela Digifarma",
            "schema": {"type": "string"},
        }
    ]
    if not cfg.get("sem_token"):
        params.append({
            "name": "x-digifarma-token",
            "in": "header",
            "required": True,
            "description": "Token obtido via `GetToken`",
            "schema": {"type": "string"},
        })
    return params


def _params_descricao(cfg: dict[str, Any]) -> str:
    """Constrói descrição legível dos parâmetros para incluir no description do body."""
    linhas: list[str] = []
    if cfg.get("params"):
        linhas.append("**Parâmetros (`params`):**\n")
        linhas.append("| Campo | Tipo | Obrigatório | Descrição |")
        linhas.append("| --- | --- | --- | --- |")
        for p in cfg["params"]:
            linhas.append(
                f"| `{p['campo']}` | {p['tipo']} | {p['obrigatorio']} | {p['descricao']} |"
            )
    elif cfg.get("params_grupos"):
        linhas.append("**Estrutura de `params`:**\n")
        linhas.append("| Chave | Tipo | Descrição |")
        linhas.append("| --- | --- | --- |")
        for g in cfg["params_grupos"]:
            linhas.append(f"| `{g['nome']}` | {g['tipo']} | {g['descricao']} |")
        for g in cfg["params_grupos"]:
            linhas.append(f"\n**Campos de `{g['nome']}`:**\n")
            linhas.append("| Campo | Tipo | Obrigatório | Descrição |")
            linhas.append("| --- | --- | --- | --- |")
            for p in g["params"]:
                linhas.append(
                    f"| `{p['campo']}` | {p['tipo']} | {p['obrigatorio']} | {p['descricao']} |"
                )
    return "\n".join(linhas)


def _request_body(cfg: dict[str, Any]) -> dict[str, Any]:
    body_tipo = cfg.get("body_tipo", "form-data-json")

    if body_tipo == "form-data-direto":
        # GetToken/SetSenha — cada campo declarado como propriedade do multipart.
        props: dict[str, Any] = {}
        required: list[str] = []
        for p in cfg.get("params") or []:
            props[p["campo"]] = {
                "type": "string" if p["tipo"] in {"string", "number", "integer", "boolean"} else "string",
                "description": p["descricao"],
            }
            if p["obrigatorio"] == "Sim":
                required.append(p["campo"])
        schema: dict[str, Any] = {"type": "object", "properties": props}
        if required:
            schema["required"] = required
        return {
            "required": True,
            "content": {
                "multipart/form-data": {
                    "schema": schema,
                }
            },
        }

    # form-data-json — um único campo `json` (string) contendo o JSON
    descricao_body = "String JSON com `cnpj` e `params`.\n\n" + _params_descricao(cfg)
    exemplo = cfg.get("exemplo_body")
    exemplo_str = json.dumps(exemplo, indent=2, ensure_ascii=False) if exemplo is not None else ""

    return {
        "required": True,
        "content": {
            "multipart/form-data": {
                "schema": {
                    "type": "object",
                    "required": ["json"],
                    "properties": {
                        "json": {
                            "type": "string",
                            "description": descricao_body,
                            "example": exemplo_str,
                        }
                    },
                }
            }
        },
    }


def _response(cfg: dict[str, Any]) -> dict[str, Any]:
    exemplo = cfg.get("exemplo_resposta")
    resp: dict[str, Any] = {
        "200": {
            "description": "Sucesso",
        }
    }
    if exemplo is not None:
        resp["200"]["content"] = {
            "application/json": {"example": exemplo}
        }
    return resp


def build_openapi() -> dict[str, Any]:
    paths: dict[str, Any] = {}
    for nome, cfg in ENDPOINTS.items():
        paths[_path_name(nome)] = {
            "post": {
                "operationId": _op_id(nome),
                "summary": nome,
                "description": cfg["descricao"].strip(),
                "tags": [_tag(nome)],
                "parameters": _headers(cfg),
                "requestBody": _request_body(cfg),
                "responses": _response(cfg),
            }
        }

    return {
        "openapi": "3.1.0",
        "info": {
            "title": "API SADI",
            "version": "1.0.0",
            "description": (
                "API REST do sistema SADI (Digifarma) para integração de parceiros. "
                "Consulta de produtos, clientes e vendas, além de registro de pedidos "
                "e pré-vendas.\n\n"
                "## ⚠️ Pré-requisitos\n\n"
                "Antes de conseguir chamar qualquer rota, sua integradora precisa de "
                "**duas coisas emitidas pela Digifarma**:\n\n"
                "1. **Usuário de integração** — o valor do header `x-digifarma-user` "
                "só é válido se emitido pela Digifarma. Não existe auto-cadastro.\n"
                "2. **Liberação dos CNPJs das lojas** — cada CNPJ de farmácia que "
                "você pretende consultar precisa estar liberado para o seu usuário "
                "na base da Digifarma.\n\n"
                "Solicite ambos via **contato@digifarma.com.br** informando o nome "
                "da integradora, contato técnico e a lista de CNPJs a atender."
            ),
            "contact": {
                "name": "Digifarma",
                "url": "https://digifarma.com.br",
            },
        },
        "servers": [
            {"url": "https://sadi.digifarma.com.br/api", "description": "Produção"},
        ],
        "tags": [
            {"name": "Autenticação"},
            {"name": "Loja"},
            {"name": "Cliente"},
            {"name": "Produto"},
            {"name": "Vendas"},
            {"name": "SADI Online"},
            {"name": "Utilitários"},
        ],
        "paths": paths,
    }


def main():
    spec = build_openapi()
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Gerado: {OUT_FILE}")
    print(f"  Endpoints: {len(spec['paths'])}")
    print(f"  Tags: {len(spec['tags'])}")


if __name__ == "__main__":
    main()
