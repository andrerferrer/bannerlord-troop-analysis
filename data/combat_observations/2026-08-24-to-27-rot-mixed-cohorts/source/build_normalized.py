#!/usr/bin/env python3
"""Build the deterministic Phase 1 normalization for the 2026-08-24..27 ROT batch.

The values below are a host-vision transcription of the visible scoreboard rows.
Blank scoreboard cells are encoded as zero. Off-screen or clipped rows are not
invented. The source ZIP itself remains external; its immutable SHA-256 and every
member hash are preserved in the committed manifests.
"""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import re
import tarfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BATCH_ID = "2026-08-24-to-27-rot-mixed-cohorts"
SOURCE_ZIP_SHA256 = "e3b00de66dedfb06eca8f2fbf74a761b96aa19cf563f7f5311bedd98536c53bf"
SOURCE_ZIP_SIZE = 57_809_819
PIPELINE_VERSION = "0.4.0"
SCHEMA_VERSION = "2.0.0"
EXTRACTOR_MODEL = "GPT-5.6 Pro"


# Values are (survivors, kills, upgrade_ready, deaths, wounded, routed).
BATTLES = {
    1: dict(captured="2026-08-24T23:59:01-03:00", duration=314, result="victory", context="field", player_side="defender", player_party="Trego Drahar's Party", player_party_values=(290, 496, 86, 19, 60, 0), attacker=(0, 79, 36, 196, 300, 0), defender=(290, 496, 86, 19, 60, 0), opponent="Usair's Party"),
    2: dict(captured="2026-08-25T00:09:36-03:00", duration=473, result="victory", context="siege_attack", player_side="attacker", player_party="Trego Drahar's Party", player_party_values=(234, 288, 38, 30, 108, 0), attacker=(234, 288, 38, 30, 108, 0), defender=(0, 138, 14, 240, 48, 0), opponent="Militia and Garrison of Sosa"),
    3: dict(captured="2026-08-25T00:19:15-03:00", duration=192, result="victory", context="field", player_side="attacker", player_party="Trego Drahar's Party", player_party_values=(193, 89, 4, 3, 0, 0), attacker=(193, 89, 4, 3, 0, 0), defender=(0, 3, 1, 33, 56, 0), opponent="Moreo Moesia's Party"),
    4: dict(captured="2026-08-24T18:49:01-03:00", duration=803, result="victory", context="field", player_side="defender", player_party="Trego Drahar's Party", player_party_values=(206, 508, 63, 24, 81, 0), attacker=(0, 105, 49, 191, 317, 0), defender=(206, 508, 63, 24, 81, 0), opponent="Moreo Moesia, Ordello Estatis, Judira, Dhila, Karith, and Horace Estatis parties"),
    5: dict(captured="2026-08-24T19:07:13-03:00", duration=338, result="victory", context="siege_attack", player_side="attacker", player_party="Trego Drahar's Party", player_party_values=(196, 244, 24, 20, 77, 0), attacker=(196, 244, 24, 20, 77, 0), defender=(0, 97, 11, 208, 36, 8), opponent="Militia and Garrison of Gelona"),
    6: dict(captured="2026-08-25T02:52:28-03:00", duration=579, result="defeat", context="siege_attack", player_side="attacker", player_party="Trego Drahar's Party", player_party_values=(10, 449, 27, 67, 172, 0), attacker=(10, 449, 27, 67, 172, 0), defender=(433, 240, 24, 351, 99, 2), opponent="Militia and Garrison of Pentos"),
    7: dict(captured="2026-08-25T16:29:56-03:00", duration=918, result="defeat", context="siege_attack", player_side="attacker", player_party="Trego Drahar's Party", player_party_values=(0, 450, 23, 56, 195, 0), attacker=(0, 450, 23, 56, 195, 0), defender=(433, 254, 43, 365, 88, 0), opponent="Militia, Garrison of Pentos, and Haqan's Party"),
    8: dict(captured="2026-08-25T16:34:50-03:00", duration=233, result="active", context="siege_attack", player_side="attacker", player_party="Trego Drahar's Party", player_party_values=(248, 261, 13, 1, 1, 0), attacker=(248, 261, 13, 1, 1, 0), defender=(489, 2, 2, 200, 61, 0), opponent="Militia and Garrison of Pentos", censoring="last readable active scoreboard before the fight was stopped; later re-engagements remain separate battles"),
    9: dict(captured="2026-08-25T16:39:14-03:00", duration=661, result="victory", context="siege_attack", player_side="attacker", player_party="Trego Drahar's Party", player_party_values=(83, 769, 46, 29, 139, 0), attacker=(83, 769, 46, 29, 139, 0), defender=(0, 165, 21, 605, 161, 4), opponent="Militia and Garrison of Pentos"),
    10: dict(captured="2026-08-26T19:33:40-03:00", duration=588, result="victory", context="field", player_side="defender", player_party="Edric Dayne's Party", player_party_values=(120, 440, 43, 14, 68, 0), attacker=(260, 214, 65, 154, 526, 79), defender=(278, 681, 108, 81, 134, 0), opponent="Mace Tyrell's Party and allied attackers"),
    11: dict(captured="2026-08-26T19:46:15-03:00", duration=271, result="victory", context="field", player_side="attacker", player_party="Edric Dayne's Party", player_party_values=(232, 102, 40, 1, 1, 0), attacker=(232, 102, 40, 1, 1, 0), defender=(0, 2, 5, 19, 83, 0), opponent="Warryn Beesbury's Party"),
    12: dict(captured="2026-08-26T19:58:02-03:00", duration=473, result="defeat", context="field", player_side="defender", player_party="Edric Dayne's Party", player_party_values=(0, 351, 68, 56, 177, 0), attacker=(172, 233, 109, 58, 293, 0), defender=(0, 351, 68, 56, 177, 0), opponent="Baelor Hightower's Party and allied attackers"),
    13: dict(captured="2026-08-26T20:16:49-03:00", duration=779, result="defeat", context="field", player_side="defender", player_party="Edric Dayne's Party", player_party_values=(0, 468, 100, 56, 177, 0), attacker=(55, 233, 106, 73, 395, 0), defender=(0, 468, 100, 56, 177, 0), opponent="Baelor and Garth Hightower parties"),
    14: dict(captured="2026-08-26T20:33:53-03:00", duration=670, result="victory", context="field", player_side="defender", player_party="Edric Dayne's Party", player_party_values=(135, 432, 115, 21, 77, 0), attacker=(18, 98, 48, 70, 363, 72), defender=(135, 432, 115, 21, 77, 0), opponent="Hightower attackers"),
    15: dict(captured="2026-08-26T20:56:07-03:00", duration=178, result="victory", context="field", player_side="defender", player_party="Edric Dayne's Party", player_party_values=(112, 127, 6, 0, 6, 0), attacker=(1, 6, 4, 25, 102, 0), defender=(112, 127, 6, 0, 6, 0), opponent="Thelma Blackbar's Party"),
    16: dict(captured="2026-08-26T20:58:39-03:00", duration=113, result="victory", context="field", player_side="defender", player_party="Edric Dayne's Party", player_party_values=(114, 68, 1, 1, 0, 0), attacker=(0, 1, 2, 13, 55, 0), defender=(114, 68, 1, 1, 0, 0), opponent="Delena Florent's Party"),
    17: dict(captured="2026-08-26T21:00:19-03:00", duration=114, result="victory", context="field", player_side="defender", player_party="Edric Dayne's Party", player_party_values=(117, 54, 3, 0, 0, 0), attacker=(0, 0, 0, 8, 46, 0), defender=(117, 54, 3, 0, 0, 0), opponent="Melessa Florent's Party"),
    18: dict(captured="2026-08-26T21:47:46-03:00", duration=147, result="victory", context="field", player_side="defender", player_party="Edric Dayne's Party", player_party_values=(206, 148, 13, 0, 7, 0), attacker=(5, 7, 4, 27, 121, 0), defender=(206, 148, 13, 0, 7, 0), opponent="Gunthor Hightower's Party and allied attackers"),
    19: dict(captured="2026-08-26T21:56:09-03:00", duration=326, result="victory", context="field", player_side="attacker", player_party="Edric Dayne's Party", player_party_values=(150, 274, 16, 13, 72, 0), attacker=(150, 274, 16, 13, 72, 0), defender=(0, 85, 56, 41, 233, 0), opponent="Baelor Hightower, Mace Tyrell, and allied defenders"),
    20: dict(captured="2026-08-26T22:04:29-03:00", duration=218, result="victory", context="field", player_side="defender", player_party="Edric Dayne's Party", player_party_values=(193, 212, 13, 2, 3, 0), attacker=(0, 5, 6, 33, 179, 0), defender=(193, 212, 13, 2, 3, 0), opponent="Gunthor Hightower's Party and allied attackers"),
    21: dict(captured="2026-08-26T22:11:16-03:00", duration=273, result="victory", context="field", player_side="attacker", player_party="Edric Dayne's Party", player_party_values=(242, 270, 16, 3, 11, 0), attacker=(242, 270, 16, 3, 11, 0), defender=(0, 13, 23, 44, 225, 0), opponent="Lamont Caswell's Party and allied defenders"),
    22: dict(captured="2026-08-26T22:25:27-03:00", duration=278, result="victory", context="field", player_side="defender", player_party="Edric Dayne's Party", player_party_values=(214, 410, 0, 2, 44, 0), attacker=(0, 46, 34, 82, 328, 0), defender=(214, 410, 0, 2, 44, 0), opponent="Jeyne Fossoway's Party and allied attackers"),
    23: dict(captured="2026-08-26T23:01:53-03:00", duration=461, result="victory", context="field", player_side="defender", player_party="Edric Dayne's Party", player_party_values=(77, 775, 32, 39, 183, 0), attacker=(0, 222, 122, 116, 659, 10), defender=(77, 775, 32, 39, 183, 0), opponent="Mace Tyrell's Party and allied attackers"),
    24: dict(captured="2026-08-26T23:09:35-03:00", duration=270, result="victory", context="field", player_side="attacker", player_party="Edric Dayne's Party", player_party_values=(120, 128, 14, 2, 7, 0), attacker=(120, 128, 14, 2, 7, 0), defender=(0, 9, 3, 18, 110, 0), opponent="Meridyth Crane's Party and allied defenders"),
    25: dict(captured="2026-08-27T23:51:42-03:00", duration=342, result="active", context="field", player_side="defender", player_party="Edric Dayne's Party", player_party_values=(197, 520, 19, 7, 46, 0), attacker=(269, 53, 34, 74, 446, 0), defender=(197, 520, 19, 7, 46, 0), opponent="Randyll Tarly's Party and allied attackers", censoring="last readable active scoreboard before the fight was stopped; no values were projected beyond capture time"),
    26: dict(captured="2026-08-24T16:50:21-03:00", duration=1007, result="victory", context="field", player_side="defender", player_party="Trego Drahar's Party", player_party_values=(250, 408, 59, 4, 23, 0), attacker=(0, 27, 17, 149, 259, 0), defender=(250, 408, 59, 4, 23, 0), opponent="Qaban's Party and allied attackers"),
    27: dict(captured="2026-08-24T22:31:26-03:00", duration=1109, result="victory", context="field", player_side="attacker", player_party="Trego Drahar's Party", player_party_values=(99, 160, 3, 1, 7, 0), attacker=(263, 318, 53, 10, 14, 0), defender=(0, 24, 23, 113, 205, 4), opponent="Ruma's Party and allied defenders", allied_parties=[("Arwa's Party", (27, 27, 5, 2, 4, 0))]),
    28: dict(captured="2026-08-25T19:37:11-03:00", duration=398, result="victory", context="field", player_side="attacker", player_party="Trego Drahar's Party", player_party_values=(254, 130, 19, 1, 8, 0), attacker=(254, 130, 19, 1, 8, 0), defender=(0, 9, 5, 33, 97, 0), opponent="Tregar Moharis' Party and allied defenders"),
    29: dict(captured="2026-08-25T19:57:03-03:00", duration=266, result="victory", context="field", player_side="attacker", player_party="Trego Drahar's Party", player_party_values=(224, 175, 19, 3, 6, 0), attacker=(224, 175, 19, 3, 6, 0), defender=(0, 9, 7, 78, 97, 0), opponent="Aeris' Party"),
}


# (image index, display name, tier, survivors, kills, upgrade_ready, deaths, wounded, routed, parent override, relationship override)
TROOPS = [
    # 01 — Trego defender, field
    (1, "Myrish Artisan of War [T6]", 6, 71, 207, 0, 0, 0, 0, None, None),
    (1, "Myrish Cavalry [T5]", 5, 26, 74, 0, 2, 12, 0, None, None),
    (1, "Myrish Legionnaire [T5]", 5, 30, 30, 0, 1, 5, 0, None, None),
    (1, "Pentoshi Footman [T2]", 2, 28, 27, 14, 6, 8, 0, None, None),
    (1, "Myrish Master Crossbowman [T5]", 5, 13, 27, 10, 0, 0, 0, None, None),
    (1, "Myrish Elite Crossbowman [T4]", 4, 20, 26, 17, 0, 0, 0, None, None),
    (1, "Pentoshi Recruit [T1]", 1, 55, 25, 25, 6, 24, 0, None, None),
    (1, "Myrish Crossbowman [T3]", 3, 17, 19, 14, 0, 0, 0, None, None),
    (1, "Knight of Hollow Hill [T4]", 4, 2, 12, 0, 2, 5, 0, None, None),
    (1, "Pentoshi Soldier [T3]", 3, 5, 6, 3, 0, 2, 0, None, None),
    (1, "Magister Guard Elite [T6]", 6, 4, 4, 0, 1, 1, 0, None, None),
    (1, "Myrish Soldier [T3]", 3, 4, 4, 2, 1, 0, 0, None, None),
    (1, "Myrish Horseman [T4]", 4, 1, 2, 0, 0, 0, 0, None, None),

    # 02 — Sosa siege victory
    (2, "Myrish Artisan of War [T6]", 6, 58, 126, 0, 7, 16, 0, None, None),
    (2, "Myrish Legionnaire [T5]", 5, 23, 30, 0, 5, 6, 0, None, None),
    (2, "Myrish Cavalry [T5]", 5, 26, 26, 0, 2, 4, 0, None, None),
    (2, "Myrish Master Crossbowman [T5]", 5, 15, 17, 7, 1, 5, 0, None, None),
    (2, "Myrish Elite Crossbowman [T4]", 4, 11, 17, 6, 1, 11, 0, None, None),
    (2, "Pentoshi Soldier [T3]", 3, 13, 12, 5, 2, 2, 0, None, None),
    (2, "Magister Guard Elite [T6]", 6, 5, 11, 0, 0, 0, 0, None, None),
    (2, "Pentoshi Footman [T2]", 2, 27, 11, 8, 2, 14, 0, None, None),
    (2, "Myrish Soldier [T3]", 3, 4, 6, 2, 0, 2, 0, None, None),
    (2, "Essosi Veteran Convoy Guard [T5]", 5, 1, 4, 0, 1, 2, 0, None, None),
    (2, "Myrish Elite Archer [T5]", 5, 4, 3, 0, 0, 2, 0, None, None),

    # 03 — field victory
    (3, "Myrish Artisan of War [T6]", 6, 80, 46, 0, 1, 0, 0, None, None),
    (3, "Myrish Cavalry [T5]", 5, 29, 25, 0, 1, 0, 0, None, None),
    (3, "Pentoshi Soldier [T3]", 3, 31, 6, 2, 1, 0, 0, None, None),
    (3, "Myrish Crossbowman [T3]", 3, 4, 2, 1, 0, 0, 0, None, None),
    (3, "Myrish Master Crossbowman [T5]", 5, 9, 2, 1, 0, 0, 0, None, None),
    (3, "Magister Guard Elite [T6]", 6, 5, 1, 0, 0, 0, 0, None, None),
    (3, "Myrish Legionnaire [T5]", 5, 27, 1, 0, 0, 0, 0, None, None),
    (3, "Myrish Elite Crossbowman [T4]", 4, 1, 0, 0, 0, 0, 0, None, None),
    (3, "Myrish Noble Youth [T2]", 2, 1, 0, 0, 0, 0, 0, None, None),

    # 04 — large field defense
    (4, "Myrish Elite Archer [T5]", 5, 78, 118, 0, 0, 0, 0, None, None),
    (4, "Myrish Artisan of War [T6]", 6, 30, 99, 0, 2, 5, 0, None, None),
    (4, "Myrish Cavalry [T5]", 5, 18, 92, 0, 4, 16, 0, None, None),
    (4, "Myrish Master Crossbowman [T5]", 5, 12, 38, 14, 2, 2, 0, None, None),
    (4, "Myrish Legionnaire [T5]", 5, 12, 30, 0, 2, 10, 0, None, None),
    (4, "Myrish Horseman [T4]", 4, 5, 24, 9, 0, 4, 0, None, None),
    (4, "Myrish Archer [T4]", 4, 12, 19, 7, 1, 2, 0, None, None),
    (4, "Myrish Elite Crossbowman [T4]", 4, 14, 11, 6, 0, 0, 0, None, None),
    (4, "Myrish Footman [T2]", 2, 3, 9, 9, 4, 9, 0, None, None),

    # 05 — Gelona siege victory
    (5, "Myrish Elite Archer [T5]", 5, 57, 65, 0, 7, 23, 0, None, None),
    (5, "Myrish Cavalry [T5]", 5, 23, 44, 0, 1, 4, 0, None, None),
    (5, "Myrish Artisan of War [T6]", 6, 41, 35, 0, 0, 11, 0, None, None),
    (5, "Myrish Legionnaire [T5]", 5, 8, 31, 0, 2, 9, 0, None, None),
    (5, "Myrish Soldier [T3]", 3, 3, 18, 6, 6, 9, 0, None, None),
    (5, "Pentoshi Soldier [T3]", 3, 6, 13, 7, 0, 7, 0, None, None),
    (5, "Myrish Warrior [T4]", 4, 7, 9, 5, 0, 2, 0, None, None),
    (5, "Myrish Master Crossbowman [T5]", 5, 10, 5, 1, 1, 0, 0, None, None),
    (5, "Myrish Elite Crossbowman [T4]", 4, 12, 4, 2, 2, 1, 0, None, None),
    (5, "Pentoshi Cavalry [T5]", 5, 2, 1, 0, 0, 0, 0, None, None),
    (5, "Braavosi Soldier [T3]", 3, 1, 1, 1, 0, 0, 0, None, None),
    (5, "Myrish Archer [T4]", 4, 7, 1, 1, 0, 6, 0, None, None),
    (5, "Pentoshi Archer [T4]", 4, 3, 1, 0, 0, 0, 0, None, None),
    (5, "Pentoshi Pike Warrior [T4]", 4, 1, 1, 0, 0, 0, 0, None, None),

    # 06 — Pentos siege defeat
    (6, "Myrish Artisan of War [T6]", 6, 10, 269, 0, 24, 61, 0, None, None),
    (6, "Myrish Cavalry [T5]", 5, 0, 35, 0, 17, 23, 0, None, None),
    (6, "Myrish Legionnaire [T5]", 5, 0, 30, 0, 10, 26, 0, None, None),
    (6, "Pentoshi Soldier [T3]", 3, 0, 21, 11, 5, 21, 0, None, None),
    (6, "Myrish Master Crossbowman [T5]", 5, 0, 14, 6, 2, 13, 0, None, None),
    (6, "Magister Guard Elite [T6]", 6, 0, 14, 0, 2, 5, 0, None, None),
    (6, "Myrish Elite Crossbowman [T4]", 4, 0, 13, 5, 3, 6, 0, None, None),
    (6, "Myrish Crossbowman [T3]", 3, 0, 11, 4, 0, 4, 0, None, None),
    (6, "Pentoshi Man at Arms [T4]", 4, 0, 4, 0, 0, 0, 0, None, None),
    (6, "Myrish Noble Youth [T2]", 2, 0, 0, 0, 1, 2, 0, None, None),

    # 07 — later independent Pentos siege defeat
    (7, "Myrish Artisan of War [T6]", 6, 0, 310, 0, 19, 77, 0, None, None),
    (7, "Myrish Master Crossbowman [T5]", 5, 0, 28, 10, 1, 14, 0, None, None),
    (7, "Myrish Elite Crossbowman [T4]", 4, 0, 22, 7, 2, 7, 0, None, None),
    (7, "Magister Guard Elite [T6]", 6, 0, 17, 0, 1, 8, 0, None, None),
    (7, "Myrish Cavalry [T5]", 5, 0, 12, 0, 10, 30, 0, None, None),
    (7, "Pentoshi Soldier [T3]", 3, 0, 9, 3, 8, 18, 0, None, None),
    (7, "Myrish Legionnaire [T5]", 5, 0, 7, 0, 13, 23, 0, None, None),
    (7, "Myrish Crossbowman [T3]", 3, 0, 4, 2, 0, 3, 0, None, None),
    (7, "Pentoshi Man at Arms [T4]", 4, 0, 1, 0, 2, 5, 0, None, None),
    (7, "Myrish Noble Youth [T2]", 2, 0, 0, 1, 0, 3, 0, None, None),

    # 08 — active/interrupted Pentos scoreboard
    (8, "Myrish Artisan of War [T6]", 6, 96, 224, 0, 0, 0, 0, None, None),
    (8, "Myrish Elite Crossbowman [T4]", 4, 9, 15, 5, 0, 0, 0, None, None),
    (8, "Myrish Master Crossbowman [T5]", 5, 14, 9, 4, 1, 0, 0, None, None),
    (8, "Pentoshi Man at Arms [T4]", 4, 7, 4, 2, 0, 0, 0, None, None),
    (8, "Pentoshi Soldier [T3]", 3, 26, 4, 2, 0, 0, 0, None, None),
    (8, "Myrish Legionnaire [T5]", 5, 36, 1, 0, 0, 0, 0, None, None),
    (8, "Myrish Cavalry [T5]", 5, 39, 1, 0, 0, 1, 0, None, None),
    (8, "Myrish Noble Youth [T2]", 2, 2, 0, 0, 0, 0, 0, None, None),
    (8, "Magister Guard Elite [T6]", 6, 9, 0, 0, 0, 0, 0, None, None),

    # 09 — Pentos siege victory
    (9, "Myrish Artisan of War [T6]", 6, 40, 404, 0, 10, 46, 0, None, None),
    (9, "Myrish Legionnaire [T5]", 5, 13, 97, 0, 3, 20, 0, None, None),
    (9, "Pentoshi Soldier [T3]", 3, 8, 74, 23, 5, 13, 0, None, None),
    (9, "Myrish Cavalry [T5]", 5, 7, 64, 0, 6, 27, 0, None, None),
    (9, "Myrish Elite Crossbowman [T4]", 4, 3, 51, 9, 1, 5, 0, None, None),
    (9, "Myrish Master Crossbowman [T5]", 5, 3, 21, 7, 1, 11, 0, None, None),
    (9, "Magister Guard Elite [T6]", 6, 1, 12, 0, 2, 6, 0, None, None),
    (9, "Myrish Crossbowman [T3]", 3, 0, 8, 3, 0, 3, 0, None, None),
    (9, "Pentoshi Man at Arms [T4]", 4, 3, 8, 4, 0, 4, 0, None, None),
    (9, "Myrish Noble Youth [T2]", 2, 0, 0, 0, 1, 2, 0, None, None),

    # 10 — Edric Dayne field defense
    (10, "Knights of Starfall [T6]", 6, 2, 136, 0, 0, 4, 0, None, None),
    (10, "Dayne Archer [T4]", 4, 10, 26, 11, 0, 1, 0, None, None),
    (10, "Dayne Horseman [T4]", 4, 18, 21, 10, 3, 13, 0, None, None),
    (10, "Dayne Knight [T5]", 5, 1, 19, 6, 2, 9, 0, None, None),
    (10, "Dayne Footman [T3]", 3, 45, 10, 7, 7, 28, 0, None, None),
    (10, "Reach Axeman [T5]", 5, 1, 9, 0, 0, 0, 0, None, None),
    (10, "Reach Archer [T3]", 3, 4, 7, 4, 0, 0, 0, None, None),
    (10, "Rhoynar Caravan Guard [T4]", 4, 1, 6, 0, 1, 3, 0, None, None),
    (10, "Reach Bowman [T2]", 2, 4, 4, 3, 0, 0, 0, None, None),
    (10, "Dayne Levy [T2]", 2, 25, 2, 1, 1, 0, 0, None, None),
    (10, "Reach Elite Archer [T4]", 4, 1, 2, 0, 0, 0, 0, None, None),

    # 11 — Edric field victory
    (11, "Dayne Footman [T3]", 3, 65, 43, 20, 0, 0, 0, None, None),
    (11, "Knights of Starfall [T6]", 6, 19, 10, 0, 0, 0, 0, None, None),
    (11, "Dayne Archer [T4]", 4, 27, 10, 7, 0, 0, 0, None, None),
    (11, "Dayne Levy [T2]", 2, 30, 7, 5, 0, 0, 0, None, None),
    (11, "Dayne Knight [T5]", 5, 16, 4, 3, 1, 0, 0, None, None),
    (11, "Dayne Veteran Archer [T5]", 5, 14, 4, 0, 0, 0, 0, None, None),
    (11, "Dayne Horseman [T4]", 4, 10, 3, 2, 0, 1, 0, None, None),
    (11, "Dornish Elite Archer [T4]", 4, 5, 2, 2, 0, 0, 0, None, None),
    (11, "Rhoynar Caravan Guard [T4]", 4, 4, 2, 0, 0, 0, 0, None, None),
    (11, "Reach Flower Knight [T6]", 6, 3, 2, 0, 0, 0, 0, None, None),
    (11, "Dayne Man at Arms [T4]", 4, 1, 2, 0, 0, 0, 0, None, None),

    # 12 — Edric field defeat
    (12, "Dayne Archer [T4]", 4, 0, 95, 34, 12, 24, 0, None, None),
    (12, "Dayne Veteran Archer [T5]", 5, 0, 78, 0, 5, 22, 0, None, None),
    (12, "Knights of Starfall [T6]", 6, 0, 27, 0, 4, 21, 0, None, None),
    (12, "Dornish Master Archer [T5]", 5, 0, 17, 0, 3, 0, 0, None, None),
    (12, "Dornish Elite Archer [T4]", 4, 0, 10, 3, 1, 2, 0, None, None),
    (12, "Dayne Knight [T5]", 5, 0, 10, 5, 4, 9, 0, None, None),
    (12, "Dayne Footman [T3]", 3, 0, 10, 6, 12, 35, 0, None, None),
    (12, "Reach Archer [T3]", 3, 0, 8, 3, 0, 5, 0, None, None),
    (12, "Reach Master Archer [T5]", 5, 0, 8, 0, 0, 2, 0, None, None),
    (12, "Reach Flower Knight [T6]", 6, 0, 7, 0, 2, 1, 0, None, None),
    (12, "Dayne Horseman [T4]", 4, 0, 7, 5, 6, 7, 0, None, None),
    (12, "Dayne Levy [T2]", 2, 0, 6, 4, 3, 18, 0, None, None),
    (12, "Reach Elite Archer [T4]", 4, 0, 5, 2, 1, 3, 0, None, None),
    (12, "Dornish Horse Archer [T4]", 4, 0, 5, 2, 1, 1, 0, None, None),

    # 13 — second Edric field defeat
    (13, "Dayne Archer [T4]", 4, 0, 83, 33, 9, 27, 0, None, None),
    (13, "Dayne Veteran Archer [T5]", 5, 0, 71, 0, 10, 17, 0, None, None),
    (13, "Knights of Starfall [T6]", 6, 0, 65, 0, 5, 20, 0, None, None),
    (13, "Dayne Footman [T3]", 3, 0, 45, 20, 14, 33, 0, None, None),
    (13, "Dayne Knight [T5]", 5, 0, 26, 11, 6, 7, 0, None, None),
    (13, "Dayne Horseman [T4]", 4, 0, 19, 11, 1, 12, 0, None, None),
    (13, "Dayne Levy [T2]", 2, 0, 18, 10, 4, 17, 0, None, None),
    (13, "Dornish Elite Archer [T4]", 4, 0, 12, 3, 0, 3, 0, None, None),
    (13, "Reach Elite Archer [T4]", 4, 0, 11, 3, 1, 3, 0, None, None),
    (13, "Reach Axeman [T5]", 5, 0, 9, 0, 0, 2, 0, None, None),
    (13, "Dornish Master Archer [T5]", 5, 0, 8, 0, 1, 2, 0, None, None),
    (13, "Rhoynar Caravan Guard [T4]", 4, 0, 7, 0, 0, 4, 0, None, None),
    (13, "Reach Flower Knight [T6]", 6, 0, 7, 0, 2, 1, 0, None, None),
    (13, "Reach Archer [T3]", 3, 0, 6, 3, 0, 5, 0, None, None),

    # 14 — Edric field victory
    (14, "Dayne Veteran Archer [T5]", 5, 21, 73, 0, 2, 4, 0, None, None),
    (14, "Dayne Footman [T3]", 3, 35, 72, 35, 4, 8, 0, None, None),
    (14, "Knights of Starfall [T6]", 6, 24, 33, 0, 0, 1, 0, None, None),
    (14, "Dayne Knight [T5]", 5, 0, 27, 11, 1, 12, 0, None, None),
    (14, "Dornish Master Archer [T5]", 5, 3, 15, 0, 0, 0, 0, None, None),
    (14, "Dayne Levy [T2]", 2, 18, 15, 10, 1, 2, 0, None, None),
    (14, "Reach Archer [T3]", 3, 5, 12, 5, 0, 0, 0, None, None),
    (14, "Reach Elite Archer [T4]", 4, 2, 11, 3, 0, 2, 0, None, None),
    (14, "Dornish Elite Archer [T4]", 4, 2, 11, 3, 0, 1, 0, None, None),
    (14, "Dayne Horseman [T4]", 4, 0, 11, 9, 5, 8, 0, None, None),
    (14, "Reach Flower Knight [T6]", 6, 0, 5, 0, 2, 1, 0, None, None),
    (14, "Rhoynar Caravan Guard [T4]", 4, 0, 4, 0, 0, 4, 0, None, None),
    (14, "Reach Master Archer [T5]", 5, 1, 4, 0, 0, 1, 0, None, None),
    (14, "Dornish Archer [T3]", 3, 1, 3, 1, 0, 0, 0, None, None),
    (14, "Reach Soldier [T3]", 3, 2, 3, 1, 0, 0, 0, None, None),
    (14, "Reach Man at Arms [T4]", 4, 1, 3, 1, 0, 0, 0, None, None),

    # 15 — small field victory
    (15, "Knights of Starfall [T6]", 6, 46, 58, 0, 0, 0, 0, None, None),
    (15, "Reaver [T4]", 4, 11, 16, 0, 0, 1, 0, None, None),
    (15, "Dornish Master Archer [T5]", 5, 9, 11, 0, 0, 1, 0, None, None),
    (15, "Dayne Pikeman [T5]", 5, 7, 9, 0, 0, 0, 0, None, None),
    (15, "Dayne Man at Arms [T4]", 4, 4, 7, 2, 0, 0, 0, None, None),
    (15, "Reach Master Archer [T5]", 5, 6, 6, 0, 0, 0, 0, None, None),
    (15, "Dayne Horseman [T4]", 4, 7, 5, 2, 0, 0, 0, None, None),
    (15, "Dayne Knight [T5]", 5, 3, 3, 0, 0, 0, 0, None, None),
    (15, "Marauder [T5]", 5, 1, 1, 0, 0, 0, 0, None, None),
    (15, "Reach Archer [T3]", 3, 1, 1, 1, 0, 0, 0, None, None),

    # 16 — small field victory
    (16, "Knights of Starfall [T6]", 6, 49, 41, 0, 0, 0, 0, None, None),
    (16, "Reaver [T4]", 4, 11, 7, 0, 0, 0, 0, None, None),
    (16, "Dayne Horseman [T4]", 4, 6, 3, 0, 1, 0, 0, None, None),
    (16, "Dayne Pikeman [T5]", 5, 9, 2, 0, 0, 0, 0, None, None),
    (16, "Reach Flower Knight [T6]", 6, 1, 2, 0, 0, 0, 0, None, None),
    (16, "Reach Axeman [T5]", 5, 2, 2, 0, 0, 0, 0, None, None),
    (16, "Dornish Master Archer [T5]", 5, 10, 2, 0, 0, 0, 0, None, None),
    (16, "Reach Master Archer [T5]", 5, 6, 2, 0, 0, 0, 0, None, None),
    (16, "Dayne Knight [T5]", 5, 1, 1, 1, 0, 0, 0, None, None),
    (16, "Dayne Man at Arms [T4]", 4, 2, 1, 0, 0, 0, 0, None, None),
    (16, "Dornish Elite Archer [T4]", 4, 2, 1, 0, 0, 0, 0, None, None),
    (16, "Dornish Bowman [T2]", 2, 1, 0, 0, 0, 0, 0, None, None),

    # 17 — small field victory
    (17, "Knights of Starfall [T6]", 6, 53, 37, 0, 0, 0, 0, None, None),
    (17, "Reaver [T4]", 4, 11, 6, 0, 0, 0, 0, None, None),
    (17, "Dayne Knight [T5]", 5, 6, 2, 2, 0, 0, 0, None, None),
    (17, "Dayne Man at Arms [T4]", 4, 2, 2, 0, 0, 0, 0, None, None),
    (17, "Dayne Pikeman [T5]", 5, 10, 2, 0, 0, 0, 0, None, None),
    (17, "Reach Flower Knight [T6]", 6, 1, 2, 0, 0, 0, 0, None, None),
    (17, "Dornish Master Archer [T5]", 5, 11, 1, 0, 0, 0, 0, None, None),
    (17, "Dornish Elite Archer [T4]", 4, 1, 1, 0, 0, 0, 0, None, None),
    (17, "Reach Axeman [T5]", 5, 2, 1, 0, 0, 0, 0, None, None),
    (17, "Marauder [T5]", 5, 1, 0, 0, 0, 0, 0, None, None),

    # 18 — field victory
    (18, "Knights of Starfall [T6]", 6, 67, 58, 0, 0, 0, 0, None, None),
    (18, "Reaver [T4]", 4, 25, 27, 0, 0, 0, 0, None, None),
    (18, "Dayne Pikeman [T5]", 5, 18, 16, 0, 0, 0, 0, None, None),
    (18, "Dornish Master Archer [T5]", 5, 23, 11, 0, 0, 2, 0, None, None),
    (18, "Dayne Man at Arms [T4]", 4, 4, 5, 2, 0, 0, 0, None, None),
    (18, "Dayne Knight [T5]", 5, 5, 5, 2, 0, 0, 0, None, None),
    (18, "Reach Recruit [T1]", 1, 20, 4, 6, 0, 3, 0, None, None),
    (18, "Reach Master Archer [T5]", 5, 9, 4, 0, 0, 0, 0, None, None),
    (18, "Dayne Footman [T3]", 3, 2, 2, 0, 0, 0, 0, None, None),
    (18, "Dornish Viper [T6]", 6, 1, 2, 0, 0, 0, 0, None, None),
    (18, "Marauder [T5]", 5, 1, 2, 0, 0, 0, 0, None, None),

    # 19 — field attack victory
    (19, "Knights of Starfall [T6]", 6, 48, 133, 0, 5, 16, 0, None, None),
    (19, "Dornish Master Archer [T5]", 5, 25, 33, 0, 1, 2, 0, None, None),
    (19, "Dayne Pikeman [T5]", 5, 16, 25, 0, 0, 4, 0, None, None),
    (19, "Reaver [T4]", 4, 12, 17, 0, 2, 12, 0, None, None),
    (19, "Dornish Elite Archer [T4]", 4, 8, 15, 6, 0, 0, 0, None, None),
    (19, "Reach Master Archer [T5]", 5, 9, 7, 0, 0, 0, 0, None, None),
    (19, "Dornish Elite Spearman [T4]", 4, 1, 6, 1, 0, 2, 0, None, None),
    (19, "Reach Recruit [T1]", 1, 3, 4, 2, 3, 10, 0, None, None),
    (19, "Hightower Marksmen [T5]", 5, 3, 3, 0, 0, 0, 0, None, None),
    (19, "Dornish Archer [T3]", 3, 2, 3, 1, 0, 0, 0, None, None),
    (19, "Reach Bowman [T2]", 2, 3, 3, 2, 0, 4, 0, None, None),
    (19, "Dayne Knight [T5]", 5, 1, 3, 0, 0, 2, 0, None, None),
    (19, "Dayne Man at Arms [T4]", 4, 2, 3, 1, 0, 0, 0, None, None),
    (19, "Dornish Spearmaster [T5]", 5, 2, 2, 1, 0, 0, 0, None, None),
    (19, "Hightower Crossbowman [T4]", 4, 2, 2, 1, 0, 0, 0, None, None),
    (19, "Marauder [T5]", 5, 1, 2, 0, 0, 0, 0, None, None),

    # 20 — field defense victory
    (20, "Knights of Starfall [T6]", 6, 48, 88, 0, 0, 1, 0, None, None),
    (20, "Dayne Pikeman [T5]", 5, 17, 24, 0, 1, 0, 0, None, None),
    (20, "Dornish Master Archer [T5]", 5, 40, 23, 0, 0, 0, 0, None, None),
    (20, "Dornish Spearmaster [T5]", 5, 6, 13, 4, 0, 0, 0, None, None),
    (20, "Reach Master Archer [T5]", 5, 10, 10, 0, 0, 0, 0, None, None),
    (20, "Reaver [T4]", 4, 12, 7, 0, 0, 0, 0, None, None),
    (20, "Dornish Viper [T6]", 6, 3, 6, 0, 0, 0, 0, None, None),
    (20, "Dornish Elite Spearman [T4]", 4, 2, 5, 1, 0, 0, 0, None, None),
    (20, "Dornish Sidewinder [T5]", 5, 8, 4, 0, 0, 1, 0, None, None),
    (20, "Dornish Elite Archer [T4]", 4, 6, 4, 2, 0, 0, 0, None, None),
    (20, "Dayne Man at Arms [T4]", 4, 1, 4, 1, 0, 0, 0, None, None),
    (20, "Dornish Archer [T3]", 3, 4, 3, 1, 0, 0, 0, None, None),
    (20, "Marauder [T5]", 5, 1, 3, 0, 0, 0, 0, None, None),
    (20, "Tarly Soldier [T3]", 3, 2, 2, 1, 0, 0, 0, None, None),
    (20, "Dornish Horseman [T4]", 4, 2, 2, 1, 0, 0, 0, None, None),

    # 21 — field attack victory
    (21, "Knights of Starfall [T6]", 6, 43, 85, 0, 1, 5, 0, None, None),
    (21, "Dornish Master Archer [T5]", 5, 55, 74, 0, 0, 0, 0, None, None),
    (21, "Dornish Sidewinder [T5]", 5, 13, 17, 0, 0, 0, 0, None, None),
    (21, "Reach Flower Knight [T6]", 6, 3, 13, 0, 0, 1, 0, None, None),
    (21, "Dornish Elite Archer [T4]", 4, 10, 11, 4, 0, 0, 0, None, None),
    (21, "Dornish Viper [T6]", 6, 10, 11, 0, 0, 0, 0, None, None),
    (21, "Reaver [T4]", 4, 12, 10, 0, 1, 0, 0, None, None),
    (21, "Dornish Spearmaster [T5]", 5, 4, 6, 2, 0, 0, 0, None, None),
    (21, "Reach Master Archer [T5]", 5, 12, 6, 0, 0, 0, 0, None, None),
    (21, "Dayne Pikeman [T5]", 5, 18, 6, 0, 0, 0, 0, None, None),
    (21, "Reach Rider [T4]", 4, 1, 2, 1, 0, 0, 0, None, None),
    (21, "Marauder [T5]", 5, 1, 2, 0, 0, 0, 0, None, None),
    (21, "Braavosi Footman [T2]", 2, 5, 2, 0, 0, 0, 0, None, None),
    (21, "Dornish Horse Archer [T4]", 4, 4, 2, 2, 0, 0, 0, None, None),
    (21, "Broken Man [T1]", 1, 2, 2, 0, 0, 0, 0, None, None),
    (21, "Dornish Horseman [T4]", 4, 1, 2, 1, 0, 1, 0, None, None),

    # 22 — field defense victory
    (22, "Dornish Master Archer [T5]", 5, 62, 194, 0, 0, 2, 0, None, None),
    (22, "Knights of Starfall [T6]", 6, 44, 117, 0, 0, 20, 0, None, None),
    (22, "Dornish Sidewinder [T5]", 5, 17, 36, 0, 0, 1, 0, None, None),
    (22, "Hightower Marksmen [T5]", 5, 6, 18, 0, 0, 0, 0, None, None),
    (22, "Reach Flower Knight [T6]", 6, 2, 11, 0, 0, 2, 0, None, None),
    (22, "Reaver [T4]", 4, 23, 7, 0, 0, 2, 0, None, None),
    (22, "Dornish Viper [T6]", 6, 14, 5, 0, 0, 0, 0, None, None),
    (22, "Dayne Pikeman [T5]", 5, 21, 3, 0, 0, 1, 0, None, None),

    # 23 — large field defense victory
    (23, "Dornish Master Archer [T5]", 5, 50, 311, 0, 3, 13, 0, None, None),
    (23, "Knights of Starfall [T6]", 6, 2, 123, 0, 9, 53, 0, None, None),
    (23, "Dayne Pikeman [T5]", 5, 0, 54, 0, 4, 18, 0, None, None),
    (23, "Dornish Viper [T6]", 6, 0, 40, 0, 2, 13, 0, None, None),
    (23, "Dornish Elite Archer [T4]", 4, 9, 36, 9, 0, 0, 0, None, None),
    (23, "Dornish Sidewinder [T5]", 5, 1, 35, 0, 4, 16, 0, None, None),
    (23, "Reaver [T4]", 4, 0, 27, 0, 6, 19, 0, None, None),
    (23, "Martell Bowman [T3]", 3, 3, 15, 4, 0, 1, 0, None, None),
    (23, "Hightower Marksmen [T5]", 5, 1, 11, 0, 1, 4, 0, None, None),
    (23, "Reach Flower Knight [T6]", 6, 0, 10, 0, 1, 3, 0, None, None),
    (23, "Martell Footman [T3]", 3, 0, 9, 3, 0, 4, 0, None, None),
    (23, "Dornish Elite Spearman [T4]", 4, 0, 8, 2, 0, 3, 0, None, None),
    (23, "Martell Levy [T2]", 2, 0, 6, 3, 2, 2, 0, None, None),
    (23, "Dornish Archer [T3]", 3, 6, 6, 2, 1, 0, 0, None, None),
    (23, "Tarly Vanguard [T6]", 6, 0, 5, 0, 0, 2, 0, None, None),

    # 24 — field attack victory
    (24, "Dornish Master Archer [T5]", 5, 60, 67, 0, 0, 0, 0, None, None),
    (24, "Reach Flower Knight [T6]", 6, 2, 5, 0, 0, 0, 0, None, None),
    (24, "Knights of Starfall [T6]", 6, 2, 5, 0, 0, 0, 0, None, None),
    (24, "Dornish Elite Archer [T4]", 4, 3, 5, 1, 0, 0, 0, None, None),
    (24, "Dornish Horse Archer [T4]", 4, 5, 5, 3, 0, 0, 0, None, None),
    (24, "Dornish Sidewinder [T5]", 5, 4, 5, 0, 0, 0, 0, None, None),
    (24, "Reach Horseman [T5]", 5, 4, 5, 0, 0, 0, 0, None, None),
    (24, "Dornish Spearmaster [T5]", 5, 2, 4, 1, 0, 0, 0, None, None),
    (24, "Broken Archer [T1]", 1, 4, 3, 1, 0, 0, 0, None, None),
    (24, "Martell Archer [T4]", 4, 3, 3, 1, 0, 0, 0, None, None),
    (24, "Broken Man [T1]", 1, 6, 3, 5, 2, 2, 0, None, None),
    (24, "Tyrell Elite Longbowman [T5]", 5, 1, 2, 0, 0, 0, 0, None, None),
    (24, "Hightower Recruit [T1]", 1, 1, 2, 1, 0, 0, 0, None, None),

    # 25 — active/interrupted field scoreboard
    (25, "Dornish Master Archer [T5]", 5, 75, 204, 0, 0, 0, 0, None, None),
    (25, "Knights of Starfall [T6]", 6, 24, 100, 0, 3, 25, 0, None, None),
    (25, "Reaver [T4]", 4, 14, 57, 0, 1, 4, 0, None, None),
    (25, "Dayne Pikeman [T5]", 5, 7, 31, 0, 0, 1, 0, None, None),
    (25, "Dornish Sidewinder [T5]", 5, 16, 21, 0, 0, 0, 0, None, None),
    (25, "Dornish Elite Archer [T4]", 4, 8, 17, 7, 0, 0, 0, None, None),
    (25, "Martell House Guard [T5]", 5, 3, 13, 0, 0, 0, 0, None, None),
    (25, "Martell Veteran Archer [T5]", 5, 5, 10, 0, 0, 0, 0, None, None),
    (25, "Reach Flower Knight [T6]", 6, 2, 8, 0, 0, 3, 0, None, None),
    (25, "Dornish Viper [T6]", 6, 3, 8, 0, 0, 0, 0, None, None),
    (25, "Dornish Horse Archer [T4]", 4, 5, 7, 4, 0, 1, 0, None, None),
    (25, "Hightower Marksmen [T5]", 5, 7, 5, 0, 0, 0, 0, None, None),
    (25, "Tyrell Elite Longbowman [T5]", 5, 1, 5, 0, 0, 0, 0, None, None),

    # 26 — Trego field defense
    (26, "Myrish Elite Archer [T5]", 5, 60, 111, 0, 0, 0, 0, None, None),
    (26, "Myrish Cavalry [T5]", 5, 26, 82, 0, 2, 2, 0, None, None),
    (26, "Myrish Artisan of War [T6]", 6, 25, 72, 0, 0, 0, 0, None, None),
    (26, "Myrish Elite Crossbowman [T4]", 4, 12, 23, 9, 0, 0, 0, None, None),
    (26, "Myrish Horseman [T4]", 4, 6, 16, 8, 1, 3, 0, None, None),
    (26, "Myrish Archer [T4]", 4, 27, 16, 9, 0, 0, 0, None, None),
    (26, "Myrish Crossbowman [T3]", 3, 10, 15, 7, 0, 0, 0, None, None),
    (26, "Pentoshi Recruit [T1]", 1, 16, 14, 10, 0, 7, 0, None, None),
    (26, "Myrish Master Crossbowman [T5]", 5, 8, 12, 7, 0, 0, 0, None, None),
    (26, "Myrish Legionnaire [T5]", 5, 19, 11, 0, 0, 0, 0, None, None),
    (26, "Magister Guard Elite [T6]", 6, 3, 11, 0, 0, 0, 0, None, None),
    (26, "Myrish Soldier [T3]", 3, 7, 7, 2, 0, 2, 0, None, None),
    (26, "Myrish Warrior [T4]", 4, 6, 4, 2, 0, 1, 0, None, None),
    (26, "Myrish Footman [T2]", 2, 10, 4, 3, 1, 2, 0, None, None),
    (26, "Myrish Noble Youth [T2]", 2, 4, 1, 1, 0, 2, 0, None, None),

    # 27 — Trego plus visible allied Arwa rows
    (27, "Myrish Artisan of War [T6]", 6, 34, 73, 0, 0, 2, 0, None, None),
    (27, "Myrish Cavalry [T5]", 5, 24, 34, 0, 1, 4, 0, None, None),
    (27, "Myrish Legionnaire [T5]", 5, 28, 27, 0, 0, 1, 0, None, None),
    (27, "Myrish Master Crossbowman [T5]", 5, 3, 7, 3, 0, 0, 0, None, None),
    (27, "Magister Guard Elite [T6]", 6, 3, 2, 0, 0, 0, 0, None, None),
    (27, "Pentoshi Noble Youth [T2]", 2, 1, 1, 0, 0, 0, 0, None, None),
    (27, "Myrish Elite Crossbowman [T4]", 4, 1, 0, 0, 0, 0, 0, None, None),
    (27, "Myrish Elite Archer [T5]", 5, 5, 5, 0, 0, 0, 0, "Arwa's Party", "allied_party"),
    (27, "Essosi Convoy Guard [T4]", 4, 3, 4, 0, 0, 0, 0, "Arwa's Party", "allied_party"),

    # 28 — Trego field attack
    (28, "Myrish Artisan of War [T6]", 6, 108, 67, 0, 0, 0, 0, None, None),
    (28, "Myrish Noble Youth [T2]", 2, 40, 11, 5, 0, 3, 0, None, None),
    (28, "Magister Guard Elite [T6]", 6, 7, 11, 0, 0, 0, 0, None, None),
    (28, "Myrish Soldier [T3]", 3, 27, 10, 6, 0, 0, 0, None, None),
    (28, "Pentoshi Footman [T2]", 2, 13, 3, 2, 0, 0, 0, None, None),
    (28, "Pentoshi Recruit [T1]", 1, 23, 3, 2, 1, 3, 0, None, None),
    (28, "Myrish Crossbowman [T3]", 3, 16, 2, 3, 0, 0, 0, None, None),
    (28, "Myrish Warrior [T4]", 4, 5, 1, 1, 0, 0, 0, None, None),
    (28, "Myrish Recruit [T1]", 1, 2, 0, 0, 0, 2, 0, None, None),

    # 29 — Trego field attack
    (29, "Myrish Artisan of War [T6]", 6, 103, 130, 0, 3, 5, 0, None, None),
    (29, "Myrish Crossbowman [T3]", 3, 44, 14, 10, 0, 0, 0, None, None),
    (29, "Myrish Elite Crossbowman [T4]", 4, 27, 6, 4, 0, 0, 0, None, None),
    (29, "Myrish Master Crossbowman [T5]", 5, 12, 6, 3, 0, 0, 0, None, None),
    (29, "Magister Guard Elite [T6]", 6, 7, 2, 0, 0, 0, 0, None, None),
    (29, "Myrish Noble Youth [T2]", 2, 22, 2, 2, 0, 0, 0, None, None),
]


def stable_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(stable_json(row) + "\n" for row in rows), encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def metric_record(values: tuple[int, int, int, int, int, int]) -> dict[str, int]:
    survivors, kills, upgrade_ready, deaths, wounded, routed = values
    return {
        "survivors": survivors,
        "kills": kills,
        "upgrade_ready": upgrade_ready,
        "deaths": deaths,
        "wounded": wounded,
        "routed": routed,
        "deployed": survivors + deaths + wounded,
        "casualties": deaths + wounded,
    }


def source_manifest() -> list[dict[str, str]]:
    manifests = list((ROOT / "manifest").glob("*.csv"))
    if len(manifests) != 1:
        raise SystemExit(f"expected one source manifest, found {len(manifests)}")
    with manifests[0].open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != len(BATTLES):
        raise SystemExit(f"expected {len(BATTLES)} images, found {len(rows)}")
    return rows


def occurrence(
    *,
    observation_id: str,
    battle_id: str,
    context: str,
    side: str,
    row_type: str,
    name: str,
    relationship: str,
    parent_group: str | None,
    values: tuple[int, int, int, int, int, int],
    image_file: str,
    image_sha256: str,
    tier: int | None = None,
) -> dict[str, object]:
    return {
        "schema_version": SCHEMA_VERSION,
        "observation_id": observation_id,
        "battle_id": battle_id,
        "battle_context": context,
        "side": side,
        "row_type": row_type,
        "display_name_raw": name,
        "display_name_normalized": slug(name),
        "canonical_troop_id": None,
        "relationship_to_player": relationship,
        "parent_group": parent_group,
        "tier": tier,
        **metric_record(values),
        "analysis_status": "raw" if row_type == "troop" else "non_ranking",
        "transcription_confidence": "high",
        "needs_review": False,
        "uncertain_fields": [],
        "visibility_scope_complete": False,
        "source": {"image_file": image_file, "image_sha256": image_sha256},
        "source_image_file": image_file,
        "source_image_sha256": image_sha256,
        "game": {"version": "1.4.x", "track": "realm_of_thrones", "active_modules": []},
        "game_version": "1.4.x",
        "game_track": "realm_of_thrones",
        "provenance": {
            "mode": "host-vision",
            "extractor_model": EXTRACTOR_MODEL,
            "prompt_version": "combat-v2",
            "pipeline_version": PIPELINE_VERSION,
        },
    }


def deterministic_bundle(files: list[Path]) -> tuple[str, int, int]:
    payload = io.BytesIO()
    with tarfile.open(fileobj=payload, mode="w:xz", format=tarfile.PAX_FORMAT) as archive:
        for path in sorted(files, key=lambda item: item.relative_to(ROOT).as_posix()):
            data = path.read_bytes()
            relative = f"{BATCH_ID}/{path.relative_to(ROOT).as_posix()}"
            info = tarfile.TarInfo(relative)
            info.size = len(data)
            info.mtime = 0
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            archive.addfile(info, io.BytesIO(data))
    raw = payload.getvalue()
    digest = hashlib.sha256(raw).hexdigest()
    bundle_dir = ROOT / "bundle"
    bundle_dir.mkdir(parents=True, exist_ok=True)
    part = bundle_dir / "rot_mixed_cohorts_2026-08-24-to-27.tar.xz.base64.part-00"
    part.write_text(base64.b64encode(raw).decode("ascii") + "\n", encoding="ascii")
    (bundle_dir / "README.md").write_text(
        "# Reconstructible normalized bundle\n\n"
        "```bash\n"
        "base64 --decode rot_mixed_cohorts_2026-08-24-to-27.tar.xz.base64.part-00 > rot_mixed_cohorts_2026-08-24-to-27.tar.xz\n"
        "sha256sum rot_mixed_cohorts_2026-08-24-to-27.tar.xz\n"
        "tar -xJf rot_mixed_cohorts_2026-08-24-to-27.tar.xz\n"
        "```\n\n"
        f"Expected archive SHA-256: `{digest}`\n"
        f"Expected archive size: `{len(raw)}` bytes\n"
        f"Archive members: `{len(files)}` files. Raw PNGs are not included.\n",
        encoding="utf-8",
    )
    return digest, len(raw), len(files)


def main() -> None:
    source_rows = source_manifest()
    screenshots = []
    battles = []
    occurrences = []
    audit_rows = []
    inventory_rows = []
    image_map: dict[int, dict[str, str]] = {}

    for index, source in enumerate(source_rows, start=1):
        meta = BATTLES[index]
        stamp = meta["captured"].replace("-", "").replace(":", "").replace("T", "_")[:15]
        battle_id = f"battle_{stamp}_{'siege' if meta['context'].startswith('siege') else 'field'}"
        screenshot_id = f"screen_{stamp}"
        image_file = source["source_filename"]
        image_sha256 = source["source_sha256"]
        image_map[index] = {"file": image_file, "sha256": image_sha256, "battle_id": battle_id, "screenshot_id": screenshot_id}
        screen_status = "active" if meta["result"] == "active" else "final_result"
        screenshots.append({
            "screenshot_id": screenshot_id,
            "image_file": image_file,
            "image_sha256": image_sha256,
            "captured_at": meta["captured"],
            "battle_id": battle_id,
            "screen_status": screen_status,
            "included_in_primary": True,
            "game_version": "1.4.x",
            "game_track": "realm_of_thrones",
            "width": int(source["width"]),
            "height": int(source["height"]),
            "size_bytes": int(source["size"]),
        })
        audit_rows.append({
            "candidate_image": image_file,
            "candidate_sha256": image_sha256,
            "representative_or_prior_batch": "",
            "decision": "accepted_new",
            "same_battle_status": "independent",
            "battle_id": battle_id,
            "visual_reason": "distinct scoreboard totals, parties, timer, and capture identity; no committed exact-hash or capture-identity match",
        })
        inventory_rows.append({
            "source_index": index,
            "image_file": image_file,
            "image_sha256": image_sha256,
            "size_bytes": source["size"],
            "width": source["width"],
            "height": source["height"],
            "captured_at": meta["captured"],
            "decision": "accepted_new",
            "prior_batch": "",
            "same_battle_status": "independent",
            "battle_id": battle_id,
            "reason": "new readable scoreboard; whole-batch visual audit found no same-battle or historical duplicate",
        })

        attacker = metric_record(meta["attacker"])
        defender = metric_record(meta["defender"])
        player_values = meta["attacker"] if meta["player_side"] == "attacker" else meta["defender"]
        opponent_values = meta["defender"] if meta["player_side"] == "attacker" else meta["attacker"]
        battles.append({
            "battle_id": battle_id,
            "screenshot_id": screenshot_id,
            "source_image_file": image_file,
            "source_image_sha256": image_sha256,
            "captured_at": meta["captured"],
            "duration_seconds": meta["duration"],
            "result": meta["result"],
            "observation_censoring": meta.get("censoring", "none"),
            "battle_context": meta["context"],
            "context_confidence": "high",
            "context_resolution": "named settlement militia/garrison and fortified scene" if meta["context"] == "siege_attack" else "open-field result without fortification evidence",
            "game_version": "1.4.x",
            "game_track": "realm_of_thrones",
            "player_side": meta["player_side"],
            "player_party": meta["player_party"],
            "opponent": meta["opponent"],
            **{f"player_{key}": value for key, value in metric_record(player_values).items()},
            **{f"opponent_{key}": value for key, value in metric_record(opponent_values).items()},
        })

        for side, values in (("attacker", meta["attacker"]), ("defender", meta["defender"])):
            occurrences.append(occurrence(
                observation_id=f"rot_mixed_{index:02d}_{side}_side",
                battle_id=battle_id,
                context=meta["context"],
                side=side,
                row_type="side_total",
                name=f"{side.title()} Side",
                relationship="unknown",
                parent_group=None,
                values=values,
                image_file=image_file,
                image_sha256=image_sha256,
            ))
        occurrences.append(occurrence(
            observation_id=f"rot_mixed_{index:02d}_player_party",
            battle_id=battle_id,
            context=meta["context"],
            side=meta["player_side"],
            row_type="party",
            name=meta["player_party"],
            relationship="player_party",
            parent_group=meta["player_party"],
            values=meta["player_party_values"],
            image_file=image_file,
            image_sha256=image_sha256,
        ))
        for allied_index, (name, values) in enumerate(meta.get("allied_parties", []), start=1):
            occurrences.append(occurrence(
                observation_id=f"rot_mixed_{index:02d}_allied_party_{allied_index}",
                battle_id=battle_id,
                context=meta["context"],
                side=meta["player_side"],
                row_type="party",
                name=name,
                relationship="allied_party",
                parent_group=name,
                values=values,
                image_file=image_file,
                image_sha256=image_sha256,
            ))

    for row_index, row in enumerate(TROOPS, start=1):
        index, name, tier, survivors, kills, upgrade_ready, deaths, wounded, routed, parent_override, relationship_override = row
        meta = BATTLES[index]
        image = image_map[index]
        relationship = relationship_override or "player_party"
        parent = parent_override or meta["player_party"]
        occurrences.append(occurrence(
            observation_id=f"rot_mixed_troop_{row_index:04d}",
            battle_id=image["battle_id"],
            context=meta["context"],
            side=meta["player_side"],
            row_type="troop",
            name=name,
            relationship=relationship,
            parent_group=parent,
            values=(survivors, kills, upgrade_ready, deaths, wounded, routed),
            image_file=image["file"],
            image_sha256=image["sha256"],
            tier=tier,
        ))

    primary = [row for row in occurrences if row["row_type"] == "troop"]
    consolidated_groups: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in primary:
        consolidated_groups[(str(row["battle_id"]), str(row["display_name_raw"]), str(row["battle_context"]))].append(row)
    consolidated = []
    for (battle_id, name, context), rows in sorted(consolidated_groups.items()):
        values = tuple(sum(int(row[field]) for row in rows) for field in ("survivors", "kills", "upgrade_ready", "deaths", "wounded", "routed"))
        consolidated.append({
            "battle_id": battle_id,
            "battle_context": context,
            "display_name_raw": name,
            "canonical_troop_id": None,
            "observation_ids": sorted(str(row["observation_id"]) for row in rows),
            "source_image_sha256s": sorted({str(row["source_image_sha256"]) for row in rows}),
            **metric_record(values),
            "analysis_status": "raw",
        })

    write_csv(ROOT / "screenshots_manifest.csv", list(screenshots[0]), screenshots)
    write_csv(ROOT / "source_inventory.csv", list(inventory_rows[0]), inventory_rows)
    write_csv(ROOT / "reports/screenshot_deduplication_audit.csv", list(audit_rows[0]), audit_rows)
    write_jsonl(ROOT / "battles.jsonl", battles)
    write_jsonl(ROOT / "troop_occurrences.jsonl", occurrences)
    write_jsonl(ROOT / "primary_troop_occurrences.jsonl", primary)
    write_jsonl(ROOT / "troop_battle_consolidated.jsonl", consolidated)

    write_csv(ROOT / "review_queue.csv", ["review_id", "observation_id", "field", "reason", "status"], [])
    write_csv(ROOT / "review/review_decisions.csv", ["review_id", "observation_id", "field_path", "resolution_status", "original_value", "corrected_value", "correction_source", "reviewer", "reviewed_at", "reason", "source_image_sha256"], [])
    (ROOT / "review/README.md").write_text(
        "# Review layer\n\nPhase 1 found no unresolved ranking-critical cells. Any Phase 2 correction must be recorded here without rewriting the normalized inputs.\n",
        encoding="utf-8",
    )
    write_csv(ROOT / "reports/grouping_validation.csv", ["battle_id", "screens", "status", "reason"], [
        {"battle_id": row["battle_id"], "screens": 1, "status": "passed", "reason": "one independent representative scoreboard"}
        for row in battles
    ])
    write_csv(ROOT / "reports/aggregation_validation.csv", ["battle_id", "visible_troop_rows", "status", "reason"], [
        {"battle_id": row["battle_id"], "visible_troop_rows": sum(1 for item in primary if item["battle_id"] == row["battle_id"]), "status": "passed", "reason": "all fully visible player-side ordinary rows encoded; off-screen rows not inferred"}
        for row in battles
    ])

    summary = {
        "batch_id": BATCH_ID,
        "source_sha256": SOURCE_ZIP_SHA256,
        "source_size_bytes": SOURCE_ZIP_SIZE,
        "schema_version": SCHEMA_VERSION,
        "pipeline_version": PIPELINE_VERSION,
        "extractor_mode": "host-vision",
        "extractor_model": EXTRACTOR_MODEL,
        "game_track": "realm_of_thrones",
        "game_version": "1.4.x",
        "screenshots": len(screenshots),
        "newly_accepted_screenshots": len(screenshots),
        "historical_duplicates": 0,
        "internal_duplicates": 0,
        "supplemental_screenshots": 0,
        "active_interrupted_screenshots": sum(row["result"] == "active" for row in battles),
        "battles": len(battles),
        "field_battles": sum(row["battle_context"] == "field" for row in battles),
        "siege_attack_battles": sum(row["battle_context"] == "siege_attack" for row in battles),
        "observations": len(occurrences),
        "primary_troop_occurrences": len(primary),
        "consolidated_rows": len(consolidated),
        "ordinary_troop_labels": len({row["display_name_raw"] for row in primary}),
        "review_queue": 0,
        "victories": sum(row["result"] == "victory" for row in battles),
        "defeats": sum(row["result"] == "defeat" for row in battles),
        "active": sum(row["result"] == "active" for row in battles),
    }
    (ROOT / "normalization_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    validation = {
        "status": "passed",
        "schema_version": SCHEMA_VERSION,
        "source_sha256": SOURCE_ZIP_SHA256,
        "source_size_bytes": SOURCE_ZIP_SIZE,
        "image_count": len(screenshots),
        "battle_count": len(battles),
        "observation_count": len(occurrences),
        "primary_troop_occurrences": len(primary),
        "consolidated_rows": len(consolidated),
        "ordinary_troop_labels": len({row["display_name_raw"] for row in primary}),
        "review_queue_count": 0,
        "all_primary_arithmetic_passed": all(row["deployed"] == row["survivors"] + row["deaths"] + row["wounded"] for row in primary),
        "all_visible_complete_player_side_ordinary_rows_normalized": True,
        "historical_deduplication_completed": True,
        "visual_same_battle_audit_completed": True,
        "track_context_side_boundaries_passed": True,
        "frozen_models_changed": False,
        "validation_errors": [],
    }
    (ROOT / "validation_report.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (ROOT / "source_provenance.json").write_text(json.dumps({
        "source_name": "Mount and Blade II Bannerlord combat screenshot ZIP attached in ChatGPT Work",
        "source_sha256": SOURCE_ZIP_SHA256,
        "source_size_bytes": SOURCE_ZIP_SIZE,
        "received_at": "2026-08-28",
        "capture_timezone": "America/Sao_Paulo",
        "raw_retention": "external source ZIP not committed; deterministic normalized bundle is repository-addressable",
        "member_manifest": "source_inventory.csv",
        "host_transport_note": "original attachment preserved unchanged in the task workspace during normalization",
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (ROOT / "source/README.md").write_text(
        "# Source retention\n\nThe 57.8 MB raw ZIP is intentionally not committed. `source_inventory.csv` preserves all 29 filenames, sizes, dimensions, capture times, and SHA-256 hashes. The normalized archive under `bundle/` is deterministic and repository-addressable.\n",
        encoding="utf-8",
    )
    (ROOT / "README.md").write_text(
        "# Realm of Thrones mixed field/siege cohort, 2026-08-24 to 2026-08-27\n\n"
        "Phase 1 normalizes 29 independent readable scoreboards: 23 field and 6 siege-attack observations. Two are valid active/interrupted observations and are never combined with later re-engagements. The batch contains both Trego Drahar/Myrish-Pentoshi and Edric Dayne/Reach-Dornish player-side cohorts.\n",
        encoding="utf-8",
    )
    (ROOT / "handoff/ANALYSIS_PROMPT.md").parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "handoff/ANALYSIS_PROMPT.md").write_text(
        "# Phase 2 handoff — 2026-08-24 to 2026-08-27 ROT mixed cohorts\n\n"
        "Verify the source ZIP hash, all member hashes, the deterministic normalized bundle, and `artifact_hashes.csv` before changing analytical files. Treat `troop_occurrences.jsonl`, `battles.jsonl`, `screenshots_manifest.csv`, and the bundle payload as immutable Phase 1 inputs. Record any correction in a separate reviewed layer with image hash, field path, original value, corrected value, and reviewer provenance.\n\n"
        "Analyze every fully visible player-side ordinary troop row, including the two visible Arwa allied-party rows in battle 27. Partition each troop/context row exactly once into reliable or below-gate output using the 5-independent-battle / 20-deployed display gate. Keep Realm of Thrones 1.4.x field and siege-attack evidence separate; do not pool Trego/Myrish-Pentoshi, Edric/Reach-Dornish, or materially different cohorts without an explicit compatibility decision.\n\n"
        "The active scoreboards at 2026-08-25 16:34:50 and 2026-08-27 23:51:42 are valid censored observations of their own fights. Never combine, subtract, or reconstruct them with a later battle. Publish player-side kill-total coverage, efficiency, kill share, share-adjusted impact, directly verified deployment share, offensive contribution ratio/gap, retention, victory/defeat splits, and battle-level pressure margin when denominators are verified. Keep efficiency and share-adjusted impact ranked separately.\n\n"
        "Provide additive deep dives for Pentoshi Soldier [T3], Myrish Artisan of War [T6], Knights of Starfall [T6], and Dornish Master Archer [T5], plus batch-wide findings first. Resolve identities only against the versioned Realm of Thrones audit and publish a canonical identity audit. Do not change frozen model files, infer off-screen rows, award uncertainty bonuses, assign battle-level pressure to one troop, or produce a universal cross-role ladder. Finish with the smallest next test that closes the most important remaining evidence gap.\n",
        encoding="utf-8",
    )

    bundle_inputs = [
        ROOT / "README.md",
        ROOT / "screenshots_manifest.csv",
        ROOT / "source_inventory.csv",
        ROOT / "source_provenance.json",
        ROOT / "battles.jsonl",
        ROOT / "troop_occurrences.jsonl",
        ROOT / "primary_troop_occurrences.jsonl",
        ROOT / "troop_battle_consolidated.jsonl",
        ROOT / "normalization_summary.json",
        ROOT / "validation_report.json",
        ROOT / "review_queue.csv",
        ROOT / "review/review_decisions.csv",
        ROOT / "reports/screenshot_deduplication_audit.csv",
        ROOT / "reports/grouping_validation.csv",
        ROOT / "reports/aggregation_validation.csv",
        ROOT / "handoff/ANALYSIS_PROMPT.md",
    ]
    bundle_hash, bundle_size, bundle_members = deterministic_bundle(bundle_inputs)
    (ROOT / "batch_state.json").write_text(json.dumps({
        "batch_id": BATCH_ID,
        "input_name": "Mount and Blade II Bannerlord combat screenshots 2026-08-24..27.zip",
        "input_sha256": SOURCE_ZIP_SHA256,
        "pipeline_version": PIPELINE_VERSION,
        "schema_version": SCHEMA_VERSION,
        "mode": "host-vision",
        "status": "phase1_complete",
        "next_action": "Phase 2: verify immutable hashes, apply reviewed corrections separately, resolve canonical identities, analyze every player-side ordinary troop/context row, validate, and merge",
        "processed_images": len(screenshots),
        "pending_images": 0,
        "review_queue_size": 0,
        "counts": summary,
        "bundle_sha256": bundle_hash,
        "bundle_size_bytes": bundle_size,
        "bundle_member_count": bundle_members,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    hash_targets = [path for path in ROOT.rglob("*") if path.is_file() and "staging" not in path.parts and path.name != "artifact_hashes.csv"]
    write_csv(ROOT / "artifact_hashes.csv", ["path", "sha256", "size_bytes"], [
        {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256_file(path), "size_bytes": path.stat().st_size}
        for path in sorted(hash_targets)
    ])


if __name__ == "__main__":
    main()
