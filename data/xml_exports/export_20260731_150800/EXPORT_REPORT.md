# Bannerlord — analysis_pack 2026-07-31 (jogo v1.4.7)

## O que tem aqui

| caminho | o que é |
|---|---|
| `analysis_pack/AGENT_PROMPT.md` | **começa aqui** — prompt pronto para colar no agente de análise |
| `analysis_pack/SCHEMA.md` | schema das colunas + filtros obrigatórios |
| `analysis_pack/README.md` | índice, contagens e URLs raw (funcionam após o push) |
| `analysis_pack/MANIFEST.csv` | sha256 + linhas + bytes de cada CSV |
| `analysis_pack/<track>/` | os dados: 4 tracks × 6 CSVs |
| `analysis-pack-20260731.bundle` | commit git pronto para push |
| `PUBLICAR_ANALYSIS_PACK.md` | os 4 comandos para publicar no GitHub |

Tracks: `vanilla`, `nightmare_sails`, `realm_of_thrones`, `taom` — mesmo schema nas quatro.
A tabela principal é `<track>_troop_equipment_audit.csv` (tropa × roster × slot, com stats
do item já resolvidos na linha).

| track | linhas de equipamento | itens | tropas |
|---|---:|---:|---:|
| vanilla | 18.153 | 2.316 | 1.937 |
| nightmare_sails | 18.736 | 2.430 | 1.989 |
| realm_of_thrones | 55.436 | 3.795 | 6.187 |
| taom | 40.351 | 5.858 | 5.257 |

## Por que este pacote existe

As definições de item do TAOM moram em `LOTRLOME_Armory` e `Alliance.Wargs`, que são
**symlinks ilegíveis** dentro de `Modules\`. Todo export anterior os percorreu como pastas
vazias — daí o catálogo TAOM com 4 itens do mod e ~18.400 referências de equipamento não
resolvidas liberadas em bloco, com notas de corpo a corpo e armadura ocas. Re-exportar
nunca ia consertar isso.

Aqui os dois módulos vieram do `TAOM_2_0_12.zip`:

- itens do TAOM no catálogo: **4 → 3.538**
- allowlist de não resolvidos: **18.415 linhas → 13 ids**

Os 13 são `orc_rider_*`, referenciados só por um roster de teste multiplayer que nunca
ganhou definição `<Item>` — bug do mod, e o filtro de multiplayer já descarta essas tropas.
Rebuild passou fail-closed, sem `--allow-unknown-items`.

`vanilla`, `nightmare_sails` e `realm_of_thrones` já estavam saudáveis.

## Pendência

`analysis/theoretical/taom/export_20260729_025002/` foi calculado sobre o catálogo de 4
itens. Está errado — marcar como obsoleto e refazer com estes dados.

## Como não precisar exportar de novo

1. Sua pasta `bannerlord-troop-analysis-main` **não é um clone git** (é ZIP antigo), e o
   `main` no GitHub já está bem à frente. Troque por um clone de verdade.
2. `data/*/raw_xml/` é gitignorado, então o XML bruto nunca viaja — o pacote normalizado
   é o que deve circular. É exatamente o ADR-003.
3. Antes de extrair qualquer coisa, compare o sha256 do install com o `manifest.csv`. Igual
   → não extraia.
