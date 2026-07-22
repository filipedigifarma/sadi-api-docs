---
title: "Status de venda"
description: "Valores possíveis do campo status em ListaVendas e GetStatusVenda"
---

Os endpoints [`ListaVendas`](endpoints/lista-vendas.md) e [`GetStatusVenda`](endpoints/get-status-venda.md) retornam o campo `status` com os valores possíveis abaixo.

| Status | Descrição |
| --- | --- |
| `VENDA_PENDENTE` | Venda aguardando fechamento pelo operador |
| `VENDA_CONCLUIDA` | Venda finalizada com sucesso |
| `SEPARADO_PARA_ENTREGA` | Pedido separado, aguardando entregador |
| `ADICIONADO_ROTA_ENTREGA` | Pedido adicionado à rota de entrega |
| `SAIU_PARA_ENTREGA` | Pedido saiu para entrega |
| `PEDIDO_ENTREGUE` | Pedido entregue ao cliente |

## Fluxo típico

```
VENDA_PENDENTE
      │
      ▼
VENDA_CONCLUIDA
      │
      ▼ (se houver delivery)
SEPARADO_PARA_ENTREGA
      │
      ▼
ADICIONADO_ROTA_ENTREGA
      │
      ▼
SAIU_PARA_ENTREGA
      │
      ▼
PEDIDO_ENTREGUE
```

Vendas sem delivery vão direto de `VENDA_PENDENTE` para `VENDA_CONCLUIDA` e não passam pelos status de entrega.
