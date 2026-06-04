# Empirical Battle Result Normalization Schema

`empirical_battle_results_normalized.csv`

| Column | Meaning |
|---|---|
| battle_id | Stable ID assigned from screenshot timestamp. |
| screenshot_file | Source screenshot filename. |
| screenshot_datetime | Timestamp inferred from filename. |
| battle_context | Manual context label. |
| battle_outcome | Victory/Defeat as shown in screenshot. |
| side | Attacker/defender side in result table. |
| party | Party label shown in screenshot. |
| troop_name | Troop name as displayed. |
| ready_alive | Green ready/alive count at battle end. |
| kills | Cyan kill count. |
| upgrades | White upgrade count if visible. |
| dead | Red dead count. |
| wounded | Yellow wounded count. |
| prisoners | Prisoner count if visible. |
| estimated_present | ready_alive + dead + wounded. |
| kills_per_present | kills / estimated_present. |
| casualty_rate | (dead + wounded) / estimated_present. |
| death_rate | dead / estimated_present. |
| transcription_confidence | high/medium. |
| notes | Manual caveats. |
| model_* fields | Joined from v7.1 model when troop name matched. |
