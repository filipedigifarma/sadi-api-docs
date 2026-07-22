"""
Gera um arquivo markdown por endpoint em `docs/endpoints/`, consumindo o
`sadi_api_docs.py` como fonte única.

Uso:
    python scripts/gerar_mdx.py

Cada arquivo é auto-contido (H1 com o nome, tabelas de headers/params, exemplos,
respostas, observações), pronto pra ser servido via Fern, GitHub Pages, MkDocs
ou renderizado direto no GitHub.
"""

import json
import os
import re
import unicodedata
from typing import Any

from sadi_api_docs import ENDPOINTS, HEADERS_PADRAO


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "docs", "endpoints")


# ---------------------------------------------------------------------------
# Slug utilitário
# ---------------------------------------------------------------------------

def slug(nome: str) -> str:
    """`GetToken - Autenticação` -> `get-token`."""
    base = nome.split(" - ")[0].strip()
    normalized = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode()
    # Camel/Pascal -> kebab: GetToken -> Get-Token -> get-token
    kebab = re.sub(r"(?<=[a-z0-9])([A-Z])", r"-\1", normalized).lower()
    kebab = re.sub(r"[^a-z0-9]+", "-", kebab).strip("-")
    return kebab


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

def md_tabela(cabecalho: list[str], linhas: list[list[str]]) -> str:
    head = "| " + " | ".join(cabecalho) + " |"
    sep = "| " + " | ".join("---" for _ in cabecalho) + " |"
    body = "\n".join("| " + " | ".join(str(c) for c in linha) + " |" for linha in linhas)
    return "\n".join([head, sep, body])


def headers_do_endpoint(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    return [HEADERS_PADRAO[0]] if cfg.get("sem_token") else HEADERS_PADRAO


def tabela_params(params: list[dict[str, Any]]) -> str:
    tem_default = any(p.get("default") is not None for p in params)
    if tem_default:
        cab = ["Campo", "Tipo", "Obrigatório", "Default", "Descrição"]
        linhas = [
            [
                f"`{p['campo']}`",
                p["tipo"],
                p["obrigatorio"],
                p["default"] if p["default"] is not None else "—",
                p["descricao"],
            ]
            for p in params
        ]
    else:
        cab = ["Campo", "Tipo", "Obrigatório", "Descrição"]
        linhas = [
            [f"`{p['campo']}`", p["tipo"], p["obrigatorio"], p["descricao"]]
            for p in params
        ]
    return md_tabela(cab, linhas)


def fmt_json(valor: Any) -> str:
    return json.dumps(valor, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Geração do markdown de um endpoint
# ---------------------------------------------------------------------------

def gerar_endpoint_md(nome: str, cfg: dict[str, Any]) -> str:
    partes: list[str] = []
    partes.append(f"# {nome}")
    partes.append("")
    partes.append(cfg["descricao"].strip())
    partes.append("")

    partes.append("**Método:** `POST`  ")
    partes.append(f"**URL:** `https://sadi.digifarma.com.br/api/{nome.split(' - ')[0]}`")
    partes.append("")

    # Headers
    partes.append("## Headers")
    partes.append("")
    headers = headers_do_endpoint(cfg)
    linhas_h = [[f"`{h['nome']}`", h["obrigatorio"], h["descricao"]] for h in headers]
    partes.append(md_tabela(["Header", "Obrigatório", "Descrição"], linhas_h))
    partes.append("")

    body_tipo = cfg.get("body_tipo", "form-data-json")

    # Body
    if body_tipo == "form-data-direto":
        partes.append("## Body")
        partes.append("")
        partes.append("Envie via `form-data` — campos diretos (sem o wrapper `json`):")
        partes.append("")
        if cfg.get("params"):
            partes.append(tabela_params(cfg["params"]))
            partes.append("")
    else:
        partes.append("## Body")
        partes.append("")
        partes.append(
            "Envie via `form-data` com um único campo chamado **`json`** contendo o JSON abaixo:"
        )
        partes.append("")
        if cfg.get("params"):
            partes.append("### Parâmetros (`params`)")
            partes.append("")
            partes.append(tabela_params(cfg["params"]))
            partes.append("")
        elif cfg.get("params_grupos"):
            partes.append("### Estrutura de `params`")
            partes.append("")
            resumo = md_tabela(
                ["Chave", "Tipo", "Descrição"],
                [[f"`{g['nome']}`", g["tipo"], g["descricao"]] for g in cfg["params_grupos"]],
            )
            partes.append(resumo)
            partes.append("")
            for grupo in cfg["params_grupos"]:
                partes.append(f"#### Campos de `{grupo['nome']}`")
                partes.append("")
                partes.append(tabela_params(grupo["params"]))
                partes.append("")
        else:
            partes.append("Este endpoint não recebe parâmetros adicionais — envie `\"params\": null`.")
            partes.append("")

    # Exemplo de envio
    partes.append("## Exemplo de envio")
    partes.append("")
    if cfg.get("exemplo_body_raw"):
        partes.append("Envie como form-data (não como JSON):")
        partes.append("")
        partes.append("```")
        partes.append(cfg["exemplo_body_raw"])
        partes.append("```")
    else:
        ex = cfg.get("exemplo_body")
        if ex is not None:
            partes.append("Conteúdo do campo `json`:")
            partes.append("")
            partes.append("```json")
            partes.append(fmt_json(ex))
            partes.append("```")
    partes.append("")

    # Exemplo de resposta
    if cfg.get("exemplo_resposta") is not None:
        partes.append("## Exemplo de resposta")
        partes.append("")
        partes.append("```json")
        partes.append(fmt_json(cfg["exemplo_resposta"]))
        partes.append("```")
        partes.append("")

    # Notas
    notas = cfg.get("notas") or []
    if notas:
        partes.append("## Observações")
        partes.append("")
        for nota in notas:
            partes.append(f"- {nota}")
        partes.append("")

    return "\n".join(partes).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    gerados = []
    for nome, cfg in ENDPOINTS.items():
        arquivo = f"{slug(nome)}.md"
        caminho = os.path.join(OUT_DIR, arquivo)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(gerar_endpoint_md(nome, cfg))
        gerados.append((nome, arquivo))

    # Gera também um índice em docs/endpoints/README.md
    idx_lines = ["# Endpoints", "", "| Endpoint | Arquivo |", "| --- | --- |"]
    for nome, arquivo in gerados:
        idx_lines.append(f"| {nome} | [{arquivo}]({arquivo}) |")
    with open(os.path.join(OUT_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx_lines) + "\n")

    print(f"Gerados {len(gerados)} arquivos em {OUT_DIR}:")
    for nome, arquivo in gerados:
        print(f"  - {arquivo:<28} ({nome})")


if __name__ == "__main__":
    main()
