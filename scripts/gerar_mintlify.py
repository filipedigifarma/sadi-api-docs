"""
Gera arquivos MDX para o Mintlify — um por endpoint — e atualiza
a navegação do mint.json agrupando por tag.

Cada MDX é minimalista (só frontmatter):

    ---
    title: "GetToken"
    openapi: "POST /GetToken"
    ---

O Mintlify puxa toda a descrição, params, exemplos e Try It direto do
openapi.json — os MDX só existem pra dar entrada na navegação.

Uso:
    python scripts/gerar_mintlify.py
"""

import json
import os
import re
import unicodedata

from sadi_api_docs import ENDPOINTS


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINTS_DIR = os.path.join(ROOT, "api-reference", "endpoints")
MINT_JSON = os.path.join(ROOT, "mint.json")


# Mesma lógica do gerar_openapi.py — mantém consistência.
def slug(nome: str) -> str:
    base = nome.split(" - ")[0].strip()
    normalized = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode()
    kebab = re.sub(r"(?<=[a-z0-9])([A-Z])", r"-\1", normalized).lower()
    return re.sub(r"[^a-z0-9]+", "-", kebab).strip("-")


def tag(nome: str) -> str:
    base = nome.split(" - ")[0]
    if base == "GetToken":
        return "Autenticação"
    if base in {"GetDadosLoja", "GetLojas"}:
        return "Loja"
    if base in {"InserirCliente", "ListaCliente"}:
        return "Cliente"
    if base == "ListaProduto":
        return "Produto"
    if base in {"InserirPreVenda", "ListaVendas", "GetStatusVenda"}:
        return "Vendas"
    if base in {"GetPromocoes", "GetRecorrencias", "GetPedidosProntos", "GetPontos"}:
        return "SADI Online"
    return "Utilitários"


def endpoint_path(nome: str) -> str:
    return "/" + nome.split(" - ")[0].strip()


ORDEM_TAGS = [
    "Autenticação",
    "Loja",
    "Cliente",
    "Produto",
    "Vendas",
    "Utilitários",
    "SADI Online",
]


def main():
    os.makedirs(ENDPOINTS_DIR, exist_ok=True)

    slugs_por_tag: dict[str, list[str]] = {}

    for nome in ENDPOINTS:
        s = slug(nome)
        t = tag(nome)
        base = nome.split(" - ")[0].strip()
        path = endpoint_path(nome)

        mdx = f'---\ntitle: "{base}"\nopenapi: "POST {path}"\n---\n'
        with open(os.path.join(ENDPOINTS_DIR, f"{s}.mdx"), "w", encoding="utf-8") as f:
            f.write(mdx)

        slugs_por_tag.setdefault(t, []).append(s)

    # Monta a lista de páginas da aba API Reference — intro + grupos por tag.
    api_ref_pages: list = ["api-reference/introduction"]
    for t in ORDEM_TAGS:
        if t in slugs_por_tag:
            api_ref_pages.append({
                "group": t,
                "pages": [f"api-reference/endpoints/{s}" for s in slugs_por_tag[t]],
            })

    # Atualiza a seção "API Reference" no mint.json.
    with open(MINT_JSON, encoding="utf-8") as f:
        mint = json.load(f)

    encontrou = False
    for i, group in enumerate(mint.get("navigation", [])):
        if group.get("group") == "API Reference":
            mint["navigation"][i]["pages"] = api_ref_pages
            encontrou = True
            break

    if not encontrou:
        mint.setdefault("navigation", []).append({
            "group": "API Reference",
            "pages": api_ref_pages,
        })

    with open(MINT_JSON, "w", encoding="utf-8") as f:
        json.dump(mint, f, indent=2, ensure_ascii=False)
        f.write("\n")

    total = sum(len(v) for v in slugs_por_tag.values())
    print(f"Gerados {total} arquivos MDX em {ENDPOINTS_DIR}")
    for t in ORDEM_TAGS:
        if t in slugs_por_tag:
            print(f"  {t}: {', '.join(slugs_por_tag[t])}")
    print(f"\nmint.json atualizado.")


if __name__ == "__main__":
    main()
