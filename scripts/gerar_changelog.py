"""
Gera a página de Changelog do Mintlify a partir da fonte única (CHANGELOG em
sadi_api_docs.py) e registra a aba "Changelog" na navegação do mint.json.

Saídas:
  - changelog/changelog.mdx  — timeline usando o componente <Update> do Mintlify
  - mint.json                — aba "Changelog" + grupo de navegação (idempotente)

Só mexe na aba/grupo "Changelog" do mint.json; preserva o resto (assim como
gerar_mintlify.py só reescreve o grupo "API Reference"). Rodar os dois em
qualquer ordem é seguro.

Uso:
    python scripts/gerar_changelog.py
"""

import json
import os

from sadi_api_docs import CHANGELOG


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHANGELOG_DIR = os.path.join(ROOT, "changelog")
CHANGELOG_MDX = os.path.join(CHANGELOG_DIR, "changelog.mdx")
MINT_JSON = os.path.join(ROOT, "mint.json")

# Página e aba na navegação. O prefixo do path ("changelog") tem que casar com
# a url da aba para o Mintlify agrupar a página sob ela.
PAGE_ID = "changelog/changelog"
TAB_NAME = "Changelog"
TAB_URL = "changelog"

# Rótulo humano por tipo de item.
ROTULO_TIPO = {
    "add": "Novo",
    "change": "Alterado",
    "fix": "Correção",
}


def gerar_mdx() -> str:
    # Mais recente no topo.
    entradas = sorted(CHANGELOG, key=lambda e: e["data"], reverse=True)

    linhas: list[str] = [
        "---",
        'title: "Changelog"',
        'description: "Histórico de mudanças da API SADI voltado ao integrador."',
        "---",
        "",
        "Mudanças relevantes para quem integra com a API SADI — endpoints novos, "
        "campos novos e alterações de comportamento. Do mais recente para o mais antigo.",
        "",
    ]

    for e in entradas:
        linhas.append(f'<Update label="{e["data"]}">')
        if e.get("titulo"):
            linhas.append(f'  **{e["titulo"]}**')
            linhas.append("")
        for item in e.get("itens", []):
            rotulo = ROTULO_TIPO.get(item.get("tipo", ""), "")
            prefixo = f"**{rotulo}:** " if rotulo else ""
            linhas.append(f'  - {prefixo}{item["texto"]}')
        linhas.append("</Update>")
        linhas.append("")

    return "\n".join(linhas).rstrip() + "\n"


def registrar_no_mint() -> None:
    with open(MINT_JSON, encoding="utf-8") as f:
        mint = json.load(f)

    # 1) Aba "Changelog" (adiciona se ausente; preserva as demais).
    tabs = mint.setdefault("tabs", [])
    if not any(t.get("name") == TAB_NAME for t in tabs):
        tabs.append({"name": TAB_NAME, "url": TAB_URL})

    # 2) Grupo de navegação "Changelog" (substitui as páginas se já existe).
    nav = mint.setdefault("navigation", [])
    grupo = {"group": TAB_NAME, "pages": [PAGE_ID]}
    for i, g in enumerate(nav):
        if g.get("group") == TAB_NAME:
            nav[i] = grupo
            break
    else:
        nav.append(grupo)

    with open(MINT_JSON, "w", encoding="utf-8") as f:
        json.dump(mint, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main() -> None:
    os.makedirs(CHANGELOG_DIR, exist_ok=True)
    with open(CHANGELOG_MDX, "w", encoding="utf-8") as f:
        f.write(gerar_mdx())

    registrar_no_mint()

    print(f"Gerado: {CHANGELOG_MDX}")
    print(f"  Entradas: {len(CHANGELOG)}")
    print(f"mint.json atualizado (aba '{TAB_NAME}').")


if __name__ == "__main__":
    main()
