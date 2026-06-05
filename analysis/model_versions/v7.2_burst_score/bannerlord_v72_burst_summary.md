# v7.2 Burst Score Summary

## Status

Implemented `burst_score_v72` as a context-specific score only.

Removed from scope for this iteration:

```txt
boarding_score
short_engagement_score
siege_defense_score
```

The v7.1 general model remains the baseline.

## Top 15 regular burst units — combined official scope

| Rank | Troop | Tier | Category | Scope | Burst | Source | General rank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Aserai Vanguard Faris | 6 | Offensive Cavalry | Vanilla pre-War-Sails modules | 93.845 | throw | 3 |
| 2 | Battanian Skipari | 5 | Offensive Infantry | War Sails / NavalDLC | 92.910 | throw | 38 |
| 3 | Imperial Naute | 5 | Offensive Infantry | War Sails / NavalDLC | 92.292 | throw | 42 |
| 4 | Battanian Fian Champion | 6 | Archer | Vanilla pre-War-Sails modules | 90.160 | ranged | 2 |
| 5 | Battanian River Raider | 4 | Offensive Infantry | War Sails / NavalDLC | 84.922 | throw | 58 |
| 6 | Battanian Mounted Skirmisher | 5 | Defensive Cavalry | Vanilla pre-War-Sails modules | 84.384 | throw | 13 |
| 7 | Imperial Coast Guard | 4 | Offensive Infantry | War Sails / NavalDLC | 81.968 | throw | 69 |
| 8 | Battanian Fian | 5 | Archer | Vanilla pre-War-Sails modules | 78.463 | ranged | 4 |
| 9 | Khuzait Khan's Guard | 6 | Horse Archer | Vanilla pre-War-Sails modules | 78.027 | ranged | 1 |
| 10 | Imperial Shipmate | 3 | Offensive Infantry | War Sails / NavalDLC | 73.343 | throw | 125 |
| 11 | Vlandian Banner Knight | 6 | Offensive Cavalry | Vanilla pre-War-Sails modules | 67.727 | charge | 12 |
| 12 | Aserai Master Archer | 5 | Archer | Vanilla pre-War-Sails modules | 67.473 | ranged | 34 |
| 13 | Khuzait Heavy Horse Archer | 5 | Horse Archer | Vanilla pre-War-Sails modules | 66.910 | ranged | 25 |
| 14 | Imperial Elite Cataphract | 6 | Defensive Cavalry | Vanilla pre-War-Sails modules | 66.856 | charge | 17 |
| 15 | Imperial Palatine Guard | 5 | Archer | Vanilla pre-War-Sails modules | 66.829 | ranged | 41 |

## Top 10 vanilla regular burst units

| Rank | Troop | Tier | Category | Burst | Source | General rank |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Aserai Vanguard Faris | 6 | Offensive Cavalry | 93.845 | throw | 3 |
| 2 | Battanian Fian Champion | 6 | Archer | 90.160 | ranged | 2 |
| 3 | Battanian Mounted Skirmisher | 5 | Defensive Cavalry | 84.384 | throw | 13 |
| 4 | Battanian Fian | 5 | Archer | 78.463 | ranged | 4 |
| 5 | Khuzait Khan's Guard | 6 | Horse Archer | 78.027 | ranged | 1 |
| 6 | Vlandian Banner Knight | 6 | Offensive Cavalry | 67.727 | charge | 12 |
| 7 | Aserai Master Archer | 5 | Archer | 67.473 | ranged | 34 |
| 8 | Khuzait Heavy Horse Archer | 5 | Horse Archer | 66.910 | ranged | 25 |
| 9 | Imperial Elite Cataphract | 6 | Defensive Cavalry | 66.856 | charge | 17 |
| 10 | Imperial Palatine Guard | 5 | Archer | 66.829 | ranged | 41 |

## Top 10 War Sails / NavalDLC regular burst units

| Rank | Troop | Tier | Category | Burst | Source | General rank |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Battanian Skipari | 5 | Offensive Infantry | 92.910 | throw | 38 |
| 2 | Imperial Naute | 5 | Offensive Infantry | 92.292 | throw | 42 |
| 3 | Battanian River Raider | 4 | Offensive Infantry | 84.922 | throw | 58 |
| 4 | Imperial Coast Guard | 4 | Offensive Infantry | 81.968 | throw | 69 |
| 5 | Imperial Shipmate | 3 | Offensive Infantry | 73.343 | throw | 125 |
| 6 | Nord Sky-Gods Chosen | 5 | Archer | 62.201 | ranged | 40 |
| 7 | Aserai Bahriyyah | 5 | Archer | 60.833 | ranged | 28 |
| 8 | Nord Ulfhedinn | 5 | Offensive Infantry | 57.342 | melee | 19 |
| 9 | Nord Marksman | 4 | Archer | 55.929 | ranged | 79 |
| 10 | Aserai Veteran Sailor | 4 | Archer | 55.709 | ranged | 73 |

## Key interpretation

The biggest intended correction is the Imperial Naute:

```txt
v7.1 regular general rank: #42
v7.2 regular burst rank: #3
```

This matches empirical screenshots better: Imperial Naute should not be promoted to S-tier general, but it should be treated as an elite short-contact javelin burst unit.

## Validation caution

Battanian Skipari ranks #2 because the XML/model inputs indicate 10 Hooked Javelins and high throwing skill. That result is formula-consistent but still needs direct screenshot validation, so issue #2 tracks that follow-up.
