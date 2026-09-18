# Velaryon Marksman × Frey Assassin — teste pareado de campo

Plano: `data/combat_observations/test_queues/comparisons/2026-09-18-velaryon-frey.json`.
Classificação: planejamento prospectivo; nenhum resultado novo de batalha.

## Pergunta

A perícia maior do Frey é uma hipótese para investigar, não a nova regra de
seleção. O teste compara o resultado das duas tropas originais no mesmo combate.
Ele responde **qual conjunto rende mais nessas condições**, não quantos pontos
percentuais de desempenho foram causados exclusivamente por Crossbow.

| Entrada auditada | Velaryon Marksman | Frey Assassin |
|---|---:|---:|
| Crossbow | 130 | 250 |
| Dano-base da besta | 100 | 93 |
| Munição-base | 20 + 20 = 40 | 18 + 18 = 36 |
| Dano bruto do virote no XML | 2 | 5 |
| Athletics | 130 | 230 |
| OneHanded | 130 | 220 |

Diferença de perícia: **250 − 130 = 120 pontos**. Isso não significa 120%, nem
92,3% a mais de dano, recarga ou precisão. Os virotes, armaduras, espadas e outras
perícias também diferem. Não se deve atribuir todo o resultado à skill, nem
usar a razão 4000/3348 da capacidade-base para "descontar" o equipamento.
Os valores são do export versionado, não medições da instalação em execução.

## Execução de baixo atrito

Monte **50 Velaryon + 50 Frey no mesmo lado, na mesma formação de atiradores**,
com o mesmo capitão, ordens e efeitos de grupo. Mantenha a formação espaçada,
com linha de tiro livre e apoio de infantaria semelhante. Evite outros atiradores
elite disputando os abates. Não coloque as duas tropas para lutar entre si.

Faça um lote inicial de **cinco batalhas independentes de campo**. Mantenha-os
atirando; não ordene uma carga para comparar combate corpo a corpo. Preserve o
placar com as duas linhas e os totais do seu lado. Não precisa de mod para este
lote. Registrar contagens reais diferentes é melhor do que presumir 50/50 quando
houve reforços, baixas anteriores ou participação parcial.

A formação compartilhada reduz diferenças de comando, mas não garante posição,
exposição ou escolha de alvos idênticas. Contato em melee, cobertura desigual,
reforços ou interrupções devem ser sinalizados quando conhecidos, não inventados
quando o print não mostra. Capitão, líder, perks, dificuldade e mods devem ficar
estáveis; munição e skill efetivas podem não coincidir com o export-base.

## Leitura dos resultados

Compare, **dentro de cada batalha**, abates por empregado, participação nos abates
e nos empregados do lado do jogador, mortos, feridos e retenção. A diferença
principal é `abates_F / empregados_F − abates_V / empregados_V`. Depois publique
a média e a mediana dessas diferenças por batalha, além de vitórias/empates de
cada tropa nessa comparação. A batalha, não o soldado nem o print, é a amostra.

Um percentual relativo só existe quando a taxa Velaryon é positiva; com zero,
preserve a diferença absoluta e as contagens, sem inventar infinito ou epsilon.
A participação entre as duas tropas é separada da participação no exército todo.

Cinco batalhas pareadas e 20 empregados de cada tropa permitem a revisão mínima,
não garantem um vencedor nem identificação causal. Não misture os testes antigos
isolados do Frey com este lote. Prints complementares continuam na mesma batalha;
reengajamentos são batalhas novas. Um eventual print anterior ao melee é outro
momento da mesma batalha, não uma amostra adicional. O placar final sozinho não
mede recarga, precisão, tiros disparados nem a arma responsável por cada abate.

Todas as demais tropas visíveis continuam na análise normal. A comparação é um
aprofundamento adicional, nunca um filtro para descartar as outras linhas.

## Para medir somente a skill

Seria necessário usar **duas cópias da mesma tropa**, com equipamento, atributos,
outras perícias, buffs e condições iguais, alterando apenas **Crossbow 130 → 250**.
O plano registra esse desenho controlado, mas ele não foi implementado nem rodado.
Exige IDs experimentais próprios, composição adversária versionada e alternância
ou randomização das posições. Não editar silenciosamente as tropas da campanha.

Esse experimento isolado não é pré-requisito para o comparativo prático acima.
Resultados de perfis controlados e campanha permanecem separados.

## Estado da fila

Velaryon permanece a próxima tropa principal; Frey entra como referência pareada,
sem reabrir seu teste dedicado já concluído. Yi Ti permanece ativo até seus próprios
resultados resolverem o estado. Sem alteração dos modelos ou resultados históricos.
