# Prompt para o agente de análise

Cole o texto abaixo (da linha tracejada em diante) no agente, junto com o `analysis_pack`.

---

Você vai analisar tropas de Mount & Blade II: Bannerlord (v1.4.7) a partir de um pacote de
dados **já normalizado**. Não existe XML para você ler, e você não deve procurar por
nenhum: o pacote é a fonte da verdade (ADR-003 do projeto).

## Entrada

`analysis_pack/`, com quatro tracks — `vanilla`, `nightmare_sails`, `realm_of_thrones`,
`taom` — todas no mesmo schema. Leia `SCHEMA.md` antes de qualquer coisa; ele descreve
cada coluna e os filtros obrigatórios. `MANIFEST.csv` traz sha256 e contagem de linhas de
todos os arquivos.

A tabela principal é `<track>/<track>_troop_equipment_audit.csv`: uma linha por
**tropa × roster_index × slot**, já com os stats do item resolvidos na mesma linha, mais
skills, cultura, `default_group` e tier da tropa. Os outros CSVs são lookups.

## Regras que não são negociáveis

1. **Filtre `item_found == True`.** Linhas sem item resolvido não têm stats; incluí-las na
   média deprime a pontuação silenciosamente.
2. **Só soldados:** `occupation == Soldier`. Descarte notáveis, wanderers, lordes.
3. **Descarte tropas de multiplayer e obsoletas.** A detecção é por conteúdo, então ids
   definidos só em `mpcharacters.xml` / `obsolete_characters.xml` entram na amostra. No
   vanilla são 135 ids (95 soldados); sem eles a baseline limpa é de **272 soldados**.
4. **Mantenha as tropas do NavalDLC.** É conteúdo de War Sails (cultura Nord inteira +
   marines de cinco culturas), não teste.
5. `roster_index` são equipamentos **alternativos** — agregue por média ou fixe o índice 0.
   Nunca some entre rosters.
6. Dano `Cut` / `Pierce` / `Blunt` interage com armadura de formas diferentes. Não compare
   números crus entre tipos sem modelar isso.

## O que produzir

Para cada track, um ranking de soldados por papel — infantaria de choque, infantaria de
linha, arqueiro, besteiro, arremessador, cavalaria de choque, arqueiro montado — com:

- as métricas que sustentam a posição, com o cálculo explícito;
- tier e culture, para dar contexto de disponibilidade;
- as tropas do topo e as surpresas (unidades subestimadas pelo tier).

Feche com um `REPORT.md` por track e um `OVERVIEW.md` comparando as quatro.

## Cuidados

- Pontuação **só é comparável dentro da mesma track**. Não faça ranking cruzando tracks
  sem dizer explicitamente qual normalização você aplicou.
- `upgrade_requires` não está modelado — o gating de upgrade é invisível nesses dados.
- Um mod **não sobrescrever** uma tropa vanilla não significa que ela ainda apareça no
  jogo: uma total conversion pode substituí-la via party template sem tocar no XML dela.
- Se algum número parecer implausível (armadura média perto de zero, tropa de tier alto
  com dano baixo), suspeite de resolução de item antes de suspeitar do jogo, e confira
  quantas linhas daquela tropa têm `item_found == False`.
- Não recalcule nem sobrescreva modelos congelados (`analysis/model_versions/`, v7.1/v7.3).
  Se os dados contradisserem um ranking congelado, escreva a recomendação e pare.

## Contexto que muda leituras antigas

Até 2026-07-31 o track `taom` estava quebrado: as definições de item do mod moram em
`LOTRLOME_Armory` e `Alliance.Wargs`, que são symlinks ilegíveis na pasta `Modules\` do
jogo. Todo export anterior os lia como pastas vazias, então o catálogo TAOM tinha **4**
itens do mod e ~18.400 referências de equipamento não resolvidas liberadas em bloco — as
notas de corpo a corpo e de armadura eram ocas. Este pacote corrige isso (3.538 itens do
TAOM). Qualquer análise de TAOM anterior a essa data deve ser refeita.
