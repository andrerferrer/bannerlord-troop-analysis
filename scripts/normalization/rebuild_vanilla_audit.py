from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from pathlib import Path

import pandas as pd


SKILL_COLUMNS = [
    "OneHanded",
    "TwoHanded",
    "Polearm",
    "Bow",
    "Crossbow",
    "Throwing",
    "Riding",
    "Athletics",
]


def strip_ns(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def clean_ref(value):
    if value is None:
        return None
    return (
        str(value)
        .replace("Item.", "")
        .replace("NPCCharacter.", "")
        .replace("Culture.", "")
        .replace("Monster.", "")
        .replace("BodyProperty.", "")
    )


def clean_name(value):
    if value is None:
        return None
    return re.sub(r"\{=.*?\}", "", str(value))


def num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_troops(raw_xml_root: Path):
    spnpc = raw_xml_root / "SandboxCore" / "ModuleData" / "spnpccharacters.xml"
    if not spnpc.exists():
        matches = list(raw_xml_root.rglob("spnpccharacters.xml"))
        if not matches:
            raise FileNotFoundError("Could not find spnpccharacters.xml")
        spnpc = matches[0]

    tree = ET.parse(spnpc)
    rx = tree.getroot()

    troop_rows = []
    edge_rows = []
    equipment_rows = []

    for npc in rx.iter():
        if strip_ns(npc.tag) != "NPCCharacter":
            continue

        attrs = dict(npc.attrib)
        troop_id = attrs.get("id")
        if not troop_id:
            continue

        row = {
            "troop_id": troop_id,
            "name_raw": attrs.get("name"),
            "name": clean_name(attrs.get("name")),
            "level": num(attrs.get("level")),
            "occupation": attrs.get("occupation"),
            "culture": clean_ref(attrs.get("culture")),
            "default_group": attrs.get("default_group"),
            "is_basic_troop": attrs.get("is_basic_troop"),
            "is_hero": attrs.get("is_hero"),
            "is_template": attrs.get("is_template"),
        }

        skills = {}
        upgrade_targets = []

        for child in npc:
            tag = strip_ns(child.tag)

            if tag == "skills":
                for skill in child:
                    if strip_ns(skill.tag) == "skill":
                        sid = skill.attrib.get("id")
                        if sid:
                            skills[sid] = num(skill.attrib.get("value"))

            elif tag == "upgrade_targets":
                for up in child:
                    if strip_ns(up.tag) == "upgrade_target":
                        target = clean_ref(up.attrib.get("id"))
                        if target:
                            upgrade_targets.append(target)
                            edge_rows.append({
                                "source_troop_id": troop_id,
                                "target_troop_id": target,
                            })

            elif tag == "Equipments":
                common_equipment = []
                rosters = []

                for elem in child:
                    elem_tag = strip_ns(elem.tag)

                    if elem_tag == "equipment":
                        common_equipment.append({
                            "slot": elem.attrib.get("slot"),
                            "item_id": clean_ref(elem.attrib.get("id")),
                            "equipment_source": "common",
                        })

                    elif elem_tag == "EquipmentRoster":
                        roster_equipment = []
                        for eq in elem:
                            if strip_ns(eq.tag) == "equipment":
                                roster_equipment.append({
                                    "slot": eq.attrib.get("slot"),
                                    "item_id": clean_ref(eq.attrib.get("id")),
                                    "equipment_source": "roster",
                                })
                        if roster_equipment:
                            rosters.append(roster_equipment)

                if not rosters and common_equipment:
                    rosters = [[]]

                for roster_index, roster_equipment in enumerate(rosters):
                    for eq in roster_equipment + common_equipment:
                        equipment_rows.append({
                            "troop_id": troop_id,
                            "roster_index": roster_index,
                            "slot": eq["slot"],
                            "item_id": eq["item_id"],
                            "equipment_source": eq["equipment_source"],
                        })

        for skill_name in SKILL_COLUMNS:
            row[skill_name] = skills.get(skill_name)

        row["upgrade_targets"] = "|".join(upgrade_targets)
        row["has_upgrade_targets"] = bool(upgrade_targets)
        row["is_soldier"] = row["occupation"] == "Soldier"

        troop_rows.append(row)

    troops = pd.DataFrame(troop_rows)
    edges = pd.DataFrame(edge_rows).drop_duplicates()
    equipment = pd.DataFrame(equipment_rows).drop_duplicates()

    return troops, edges, equipment


def derive_tree_tiers(troops: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    soldier_ids = set(troops.loc[troops["is_soldier"], "troop_id"])
    edges_soldier = edges[
        edges["source_troop_id"].isin(soldier_ids)
        & edges["target_troop_id"].isin(soldier_ids)
    ].copy()

    incoming = defaultdict(set)
    outgoing = defaultdict(set)

    for _, row in edges_soldier.iterrows():
        src = row["source_troop_id"]
        tgt = row["target_troop_id"]
        outgoing[src].add(tgt)
        incoming[tgt].add(src)

    roots = sorted([
        troop_id
        for troop_id in soldier_ids
        if len(incoming[troop_id]) == 0 and len(outgoing[troop_id]) > 0
    ])

    tier_rows = []
    visited_best = {}
    queue = deque()

    for root_id in roots:
        queue.append((root_id, root_id, 1, [root_id]))

    while queue:
        troop_id, root_id, depth, path = queue.popleft()
        key = (troop_id, root_id)

        if key in visited_best and visited_best[key] <= depth:
            continue

        visited_best[key] = depth

        tier_rows.append({
            "troop_id": troop_id,
            "tree_root_id": root_id,
            "tree_tier": depth,
            "upgrade_path": "|".join(path),
        })

        for next_id in sorted(outgoing.get(troop_id, [])):
            if next_id in path:
                continue
            queue.append((next_id, root_id, depth + 1, path + [next_id]))

    if tier_rows:
        tree_tiers = (
            pd.DataFrame(tier_rows)
            .sort_values(["troop_id", "tree_tier", "tree_root_id"])
            .drop_duplicates("troop_id", keep="first")
            .copy()
        )
    else:
        tree_tiers = pd.DataFrame(
            columns=["troop_id", "tree_root_id", "tree_tier", "upgrade_path"]
        )

    unreached = sorted(soldier_ids - set(tree_tiers["troop_id"]))
    if unreached:
        extra = pd.DataFrame([{
            "troop_id": troop_id,
            "tree_root_id": None,
            "tree_tier": None,
            "upgrade_path": None,
        } for troop_id in unreached])
        tree_tiers = pd.concat([tree_tiers, extra], ignore_index=True)

    def line_status(row):
        if pd.isna(row["tree_tier"]):
            return "special_or_unlinked"
        root = str(row["tree_root_id"] or "")
        if "youth" in root or "noble" in root:
            return "noble_line"
        return "main_or_minor_line"

    tree_tiers["line_status"] = tree_tiers.apply(line_status, axis=1)

    return tree_tiers.merge(
        troops[[
            "troop_id",
            "name",
            "level",
            "occupation",
            "culture",
            "default_group",
            "has_upgrade_targets",
        ]],
        on="troop_id",
        how="left",
    )


def parse_direct_items(raw_xml_root: Path) -> pd.DataFrame:
    rows = []

    for xml_path in raw_xml_root.rglob("*.xml"):
        rel = str(xml_path.relative_to(raw_xml_root)).replace("\\", "/")

        if any(x in rel for x in ["Languages/", "/GUI/", "/Atmospheres/"]):
            continue

        if not (
            "/ModuleData/items/" in rel
            or rel.endswith("story_mode_items.xml")
            or rel.endswith("mpitems.xml")
        ):
            continue

        try:
            tree = ET.parse(xml_path)
        except ET.ParseError:
            continue

        for item in tree.getroot().iter():
            if strip_ns(item.tag) != "Item":
                continue

            attrs = dict(item.attrib)
            item_id = attrs.get("id")

            if not item_id:
                continue

            row = {
                "item_id": item_id,
                "name": clean_name(attrs.get("name")),
                "item_kind": "Item",
                "type": attrs.get("Type"),
                "subtype": attrs.get("subtype"),
                "culture": clean_ref(attrs.get("culture")),
                "weight": num(attrs.get("weight")),
                "value": num(attrs.get("value")),
                "source_xml": rel,
                "weapon_class": None,
                "stack_amount": None,
                "speed_rating": None,
                "missile_speed": None,
                "accuracy": None,
                "weapon_length": None,
                "swing_damage": None,
                "swing_damage_type": None,
                "thrust_damage": None,
                "thrust_damage_type": None,
                "hit_points": None,
                "shield_armor": None,
                "head_armor": None,
                "body_armor": None,
                "arm_armor": None,
                "leg_armor": None,
                "horse_speed": None,
                "horse_maneuver": None,
                "horse_charge_damage": None,
                "horse_extra_health": None,
            }

            for child in item:
                if strip_ns(child.tag) != "ItemComponent":
                    continue

                for comp in child:
                    ctag = strip_ns(comp.tag)
                    cattrs = dict(comp.attrib)

                    if ctag == "Weapon":
                        row["weapon_class"] = cattrs.get("weapon_class")
                        row["stack_amount"] = num(cattrs.get("stack_amount"))
                        row["speed_rating"] = num(cattrs.get("speed_rating"))
                        row["missile_speed"] = num(cattrs.get("missile_speed"))
                        row["accuracy"] = num(cattrs.get("accuracy"))
                        row["weapon_length"] = num(cattrs.get("weapon_length"))
                        row["swing_damage"] = num(cattrs.get("swing_damage"))
                        row["swing_damage_type"] = cattrs.get("swing_damage_type")
                        row["thrust_damage"] = num(cattrs.get("thrust_damage"))
                        row["thrust_damage_type"] = cattrs.get("thrust_damage_type")
                        row["hit_points"] = num(cattrs.get("hit_points"))
                        row["shield_armor"] = num(cattrs.get("body_armor"))

                    elif ctag == "Armor":
                        row["head_armor"] = num(cattrs.get("head_armor"))
                        row["body_armor"] = num(cattrs.get("body_armor"))
                        row["arm_armor"] = num(cattrs.get("arm_armor"))
                        row["leg_armor"] = num(cattrs.get("leg_armor"))

                    elif ctag == "Horse":
                        row["horse_speed"] = num(cattrs.get("speed"))
                        row["horse_maneuver"] = num(cattrs.get("maneuver"))
                        row["horse_charge_damage"] = num(cattrs.get("charge_damage"))
                        row["horse_extra_health"] = num(cattrs.get("extra_health"))

            rows.append(row)

    return pd.DataFrame(rows)


def parse_crafted_items(raw_xml_root: Path) -> pd.DataFrame:
    rows = []

    for xml_path in raw_xml_root.rglob("*.xml"):
        rel = str(xml_path.relative_to(raw_xml_root)).replace("\\", "/")

        if any(x in rel for x in ["Languages/", "/GUI/", "/Atmospheres/"]):
            continue

        if not ("/ModuleData/items/" in rel or rel.endswith("mpitems.xml")):
            continue

        try:
            tree = ET.parse(xml_path)
        except ET.ParseError:
            continue

        for crafted in tree.getroot().iter():
            if strip_ns(crafted.tag) != "CraftedItem":
                continue

            attrs = dict(crafted.attrib)
            item_id = attrs.get("id")

            if not item_id:
                continue

            piece_ids = []

            for child in crafted:
                if strip_ns(child.tag) == "Pieces":
                    for piece in child:
                        if strip_ns(piece.tag) == "Piece":
                            pid = piece.attrib.get("id")
                            if pid:
                                piece_ids.append(pid)

            rows.append({
                "item_id": item_id,
                "name": clean_name(attrs.get("name")),
                "item_kind": "CraftedItem",
                "type": "CraftedWeapon",
                "crafting_template": attrs.get("crafting_template"),
                "culture": clean_ref(attrs.get("culture")),
                "modifier_group": attrs.get("modifier_group"),
                "source_xml": rel,
                "piece_ids": "|".join(piece_ids),
                "crafted_stats_reconstructed": False,
                "score_usage_status": "audit_only_no_aggressive_htk",
            })

    return pd.DataFrame(rows)


def build_audit_join(
    troops: pd.DataFrame,
    tree_tiers: pd.DataFrame,
    equipment: pd.DataFrame,
    direct_items: pd.DataFrame,
    crafted_items: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    direct_lookup = (
        direct_items
        .sort_values(["item_id", "source_xml"])
        .drop_duplicates("item_id", keep="first")
        .set_index("item_id")
        .to_dict("index")
    )

    crafted_lookup = (
        crafted_items
        .sort_values(["item_id", "source_xml"])
        .drop_duplicates("item_id", keep="first")
        .set_index("item_id")
        .to_dict("index")
    )

    rows = []

    for _, eq in equipment.iterrows():
        item_id = eq["item_id"]
        direct = direct_lookup.get(item_id)
        crafted = crafted_lookup.get(item_id)

        row = {
            **eq.to_dict(),
            "item_found": bool(direct or crafted),
            "item_kind": None,
            "type": None,
            "item_name": None,
            "crafting_template": None,
            "crafted_stats_reconstructed": None,
            "score_usage_status": None,
        }

        stat_cols = [
            "weapon_class",
            "stack_amount",
            "speed_rating",
            "missile_speed",
            "accuracy",
            "weapon_length",
            "swing_damage",
            "swing_damage_type",
            "thrust_damage",
            "thrust_damage_type",
            "hit_points",
            "shield_armor",
            "head_armor",
            "body_armor",
            "arm_armor",
            "leg_armor",
            "horse_speed",
            "horse_maneuver",
            "horse_charge_damage",
            "horse_extra_health",
        ]

        for col in stat_cols:
            row[col] = None

        if direct:
            row["item_kind"] = "Item"
            row["type"] = direct.get("type")
            row["item_name"] = direct.get("name")
            row["score_usage_status"] = "direct_stats_available"
            for col in stat_cols:
                row[col] = direct.get(col)

        elif crafted:
            row["item_kind"] = "CraftedItem"
            row["type"] = "CraftedWeapon"
            row["item_name"] = crafted.get("name")
            row["crafting_template"] = crafted.get("crafting_template")
            row["crafted_stats_reconstructed"] = False
            row["score_usage_status"] = "audit_only_no_aggressive_htk"

        rows.append(row)

    audit = pd.DataFrame(rows)

    audit = audit.merge(
        troops[[
            "troop_id",
            "name",
            "level",
            "occupation",
            "culture",
            "default_group",
            *SKILL_COLUMNS,
        ]].rename(columns={"name": "troop_name"}),
        on="troop_id",
        how="left",
    )

    audit = audit.merge(
        tree_tiers[["troop_id", "tree_root_id", "tree_tier", "line_status"]],
        on="troop_id",
        how="left",
    )

    roster_rows = []

    for (troop_id, roster_index), group in audit.groupby(["troop_id", "roster_index"], dropna=False):
        first = group.iloc[0]
        weapons = group[group["slot"].astype(str).str.startswith("Item", na=False)]
        armor = group[group["slot"].isin(["Head", "Body", "Gloves", "Leg", "Cape"])]
        horse = group[group["slot"].eq("Horse")]
        harness = group[group["slot"].eq("HorseHarness")]

        crafted_templates = sorted(set(weapons["crafting_template"].dropna().tolist()))

        roster_rows.append({
            "troop_id": troop_id,
            "troop_name": first["troop_name"],
            "level": first["level"],
            "tree_tier": first["tree_tier"],
            "line_status": first["line_status"],
            "culture": first["culture"],
            "default_group": first["default_group"],
            "roster_index": roster_index,
            "items": "|".join(group["item_id"].dropna().tolist()),
            "weapon_items": "|".join(weapons["item_id"].dropna().tolist()),
            "direct_weapon_items": "|".join(weapons.loc[weapons["item_kind"].eq("Item"), "item_id"].dropna().tolist()),
            "crafted_weapon_items": "|".join(weapons.loc[weapons["item_kind"].eq("CraftedItem"), "item_id"].dropna().tolist()),
            "crafted_templates": "|".join(crafted_templates),
            "has_bow": bool((weapons["type"] == "Bow").any()),
            "has_crossbow": bool((weapons["type"] == "Crossbow").any()),
            "has_arrows": bool((weapons["type"] == "Arrows").any()),
            "has_bolts": bool((weapons["type"] == "Bolts").any()),
            "has_shield": bool((weapons["type"] == "Shield").any()),
            "has_horse": bool(len(horse)),
            "has_horse_harness": bool(len(harness)),
            "has_throwing": any(("Javelin" in t or "Throwing" in t) for t in crafted_templates) or bool((weapons["type"] == "Thrown").any()),
            "armor_total": (
                armor["head_armor"].fillna(0).sum()
                + armor["body_armor"].fillna(0).sum()
                + armor["arm_armor"].fillna(0).sum()
                + armor["leg_armor"].fillna(0).sum()
            ),
            "shield_hp_max": weapons.loc[weapons["type"].eq("Shield"), "hit_points"].fillna(0).max() if bool((weapons["type"] == "Shield").any()) else 0,
            "horse_speed_max": horse["horse_speed"].fillna(0).max() if len(horse) else 0,
            "horse_charge_max": horse["horse_charge_damage"].fillna(0).max() if len(horse) else 0,
            "horse_harness_armor_max": harness["body_armor"].fillna(0).max() if len(harness) else 0,
            "crafted_weapon_stat_status": "not_reconstructed",
            "unknown_item_count": int((~group["item_found"]).sum()),
        })

    return audit, pd.DataFrame(roster_rows)


def build_sanity_table(roster_summary: pd.DataFrame) -> pd.DataFrame:
    sanity_ids = [
        "battanian_fian_champion",
        "khuzait_khans_guard",
        "imperial_legionary",
        "vlandian_sergeant",
        "vlandian_sharpshooter",
        "imperial_elite_cataphract",
        "vlandian_banner_knight",
        "druzhinnik_champion",
        "aserai_vanguard_faris",
        "khuzait_darkhan",
    ]

    rows = []

    for troop_id in sanity_ids:
        sub = roster_summary[roster_summary["troop_id"] == troop_id].copy()

        if sub.empty:
            rows.append({
                "troop_id": troop_id,
                "found": False,
                "parser_verdict": "missing",
            })
            continue

        first = sub.iloc[0]

        direct_weapons = sorted(set("|".join(sub["direct_weapon_items"].fillna("")).split("|")) - {""})
        crafted_weapons = sorted(set("|".join(sub["crafted_weapon_items"].fillna("")).split("|")) - {""})
        crafted_templates = sorted(set("|".join(sub["crafted_templates"].fillna("")).split("|")) - {""})

        has_bow = bool(sub["has_bow"].max())
        has_crossbow = bool(sub["has_crossbow"].max())
        has_shield = bool(sub["has_shield"].max())
        has_horse = bool(sub["has_horse"].max())
        has_throwing = bool(sub["has_throwing"].max())

        verdicts = []
        name = str(first["troop_name"])

        if "Fian" in name and not has_bow:
            verdicts.append("problem: expected bow")
        if "Khan" in name and not (has_horse and has_bow):
            verdicts.append("problem: expected horse+bow")
        if "Sharpshooter" in name and not has_crossbow:
            verdicts.append("problem: expected crossbow")
        if ("Cataphract" in name or "Banner Knight" in name or "Faris" in name) and not has_horse:
            verdicts.append("problem: expected horse")

        if not verdicts:
            verdicts.append("parser looks plausible")

        rows.append({
            "troop_id": troop_id,
            "found": True,
            "troop_name": first["troop_name"],
            "level": first["level"],
            "tree_tier": first["tree_tier"],
            "line_status": first["line_status"],
            "culture": first["culture"],
            "default_group": first["default_group"],
            "roster_count": len(sub),
            "has_bow": has_bow,
            "has_crossbow": has_crossbow,
            "has_shield": has_shield,
            "has_horse": has_horse,
            "has_throwing": has_throwing,
            "armor_total_avg": round(float(sub["armor_total"].mean()), 2),
            "shield_hp_max": round(float(sub["shield_hp_max"].max()), 2),
            "horse_speed_max": round(float(sub["horse_speed_max"].max()), 2),
            "horse_harness_armor_max": round(float(sub["horse_harness_armor_max"].max()), 2),
            "direct_weapon_items": "|".join(direct_weapons),
            "crafted_weapon_items": "|".join(crafted_weapons),
            "crafted_templates": "|".join(crafted_templates),
            "parser_verdict": "; ".join(verdicts),
        })

    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-xml-root", type=Path, default=Path("data/vanilla/raw_xml"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/vanilla/audit"))
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    troops, edges, equipment = parse_troops(args.raw_xml_root)
    tree_tiers = derive_tree_tiers(troops, edges)
    direct_items = parse_direct_items(args.raw_xml_root)
    crafted_items = parse_crafted_items(args.raw_xml_root)
    audit, roster_summary = build_audit_join(
        troops=troops,
        tree_tiers=tree_tiers,
        equipment=equipment,
        direct_items=direct_items,
        crafted_items=crafted_items,
    )
    sanity = build_sanity_table(roster_summary)

    troops.to_csv(args.output_dir / "vanilla_troops.csv", index=False)
    edges.to_csv(args.output_dir / "vanilla_upgrade_edges.csv", index=False)
    tree_tiers.to_csv(args.output_dir / "vanilla_tree_tiers.csv", index=False)
    equipment.to_csv(args.output_dir / "vanilla_equipment_rosters.csv", index=False)
    direct_items.to_csv(args.output_dir / "vanilla_items_direct.csv", index=False)
    crafted_items.to_csv(args.output_dir / "vanilla_items_crafted.csv", index=False)
    audit.to_csv(args.output_dir / "vanilla_troop_equipment_audit.csv", index=False)
    roster_summary.to_csv(args.output_dir / "vanilla_roster_audit_summary.csv", index=False)
    sanity.to_csv(args.output_dir / "vanilla_sanity_check_table.csv", index=False)

    print("Audit rebuild complete.")
    print(f"troops={len(troops)}")
    print(f"upgrade_edges={len(edges)}")
    print(f"equipment_rows={len(equipment)}")
    print(f"direct_items={len(direct_items)}")
    print(f"crafted_items={len(crafted_items)}")
    print(f"audit_rows={len(audit)}")
    print(f"sanity_rows={len(sanity)}")


if __name__ == "__main__":
    main()
