from __future__ import annotations
import base64, csv, hashlib, io, json, tarfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / 'data/combat_observations/2026-09-15-to-16-rot-qartheen-enthroned-guardian'
ARCHIVE_TEXT = BATCH / 'bundle/qartheen_enthroned_guardian_phase1.tar.xz.base64'
EXPECTED_SOURCES = {'ChatGPT 15_09_2026 16_34_46.png': '95efffabe6383d536e0b344010a77277b9bd10c98bff90bb1ebd7c00404c2404', 'Mount and Blade II Bannerlord - Singleplayer PID_ 24144 -  Win64_Shipping_Client Msvc14 Managed C__Program Files (x86)_Steam_steamapps_common_Mount & Blade II Bannerlord_bin_Modules_ 15_09_2026 16_37_02.png': 'aa2e27bcb60a4e3a2131c2b7f90a5281940ac0f9426857afbac8306719366853', 'Mount and Blade II Bannerlord - Singleplayer PID_ 24144 -  Win64_Shipping_Client Msvc14 Managed C__Program Files (x86)_Steam_steamapps_common_Mount & Blade II Bannerlord_bin_Modules_ 15_09_2026 16_39_50.png': '1f36bf7ab9299961de7824ab372733bacd160b1dc39cbe310599f014146aa14e', 'Mount and Blade II Bannerlord - Singleplayer PID_ 24144 -  Win64_Shipping_Client Msvc14 Managed C__Program Files (x86)_Steam_steamapps_common_Mount & Blade II Bannerlord_bin_Modules_ 15_09_2026 16_43_27.png': 'd0f5222d1e1d52144aded15f32bfeebac4118cdda0bf4c6d2ac191535349940f', 'Screenshot 16_09_2026 16_04_22.png': 'd422642f40d465a09c06379febfebff2ae1f439ed2928730e2d56ad2b0478e39', 'Mount and Blade II Bannerlord - Singleplayer PID_ 13216 -  Win64_Shipping_Client Msvc14 Managed C__Program Files (x86)_Steam_steamapps_common_Mount & Blade II Bannerlord_bin_Modules_ 16_09_2026 16_24_56.png': 'd4530c1c1384f0ee05623e97265858fa0007e3eb0ef7ef0af6724ea7d4746fa9', 'Mount and Blade II Bannerlord - Singleplayer PID_ 13216 -  Win64_Shipping_Client Msvc14 Managed C__Program Files (x86)_Steam_steamapps_common_Mount & Blade II Bannerlord_bin_Modules_ 16_09_2026 16_27_11.png': 'c220ed7557ed19bd14899cf8e902068043fea5c7686b6a447a81c58f75e343fb', 'Mount and Blade II Bannerlord - Singleplayer PID_ 13216 -  Win64_Shipping_Client Msvc14 Managed C__Program Files (x86)_Steam_steamapps_common_Mount & Blade II Bannerlord_bin_Modules_ 16_09_2026 16_32_18.png': '4fa9797ff6ea4d8fdcff7643afeddcd6dc73297ceb26e02202e921d761918f89', 'Mount and Blade II Bannerlord - Singleplayer PID_ 13216 -  Win64_Shipping_Client Msvc14 Managed C__Program Files (x86)_Steam_steamapps_common_Mount & Blade II Bannerlord_bin_Modules_ 16_09_2026 16_38_41.png': '47a608df0c009ad3c707761332bd8ee0302599c8f5cb60ecd8eea68107012ac9', 'Mount and Blade II Bannerlord - Singleplayer PID_ 13216 -  Win64_Shipping_Client Msvc14 Managed C__Program Files (x86)_Steam_steamapps_common_Mount & Blade II Bannerlord_bin_Modules_ 16_09_2026 18_45_27.png': 'e6db64e597b9098e2006451a5369ba1acc147e6ff3215d50bce16042623a319a'}
EXPECTED_MEMBERS = ['README.md', 'screenshots_manifest.csv', 'source_manifest.json', 'source_inventory.csv', 'normalization_summary.json', 'normalized/events.jsonl', 'normalized/party_summaries.jsonl', 'normalized/player_rows/index.json', 'normalized/player_rows/b01.jsonl', 'normalized/player_rows/b02.jsonl', 'normalized/player_rows/b03.jsonl', 'normalized/player_rows/b04.jsonl', 'normalized/player_rows/b05.jsonl', 'normalized/player_rows/b06.jsonl', 'normalized/player_rows/b07.jsonl', 'normalized/player_rows/b08.jsonl', 'normalized/player_rows/b09.jsonl', 'normalized/player_rows/b10.jsonl', 'reports/screenshot_deduplication_audit.csv', 'reports/unresolved_rows.csv', 'integrity_report.json', 'handoff/ANALYSIS_PROMPT.md', 'handoff/ANALYSIS_TASK_V1.json', 'reviewed/review_resolutions.csv']

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

class Phase1Tests(unittest.TestCase):
    def test_bundle_manifest_and_normalized_contract(self):
        archive = base64.b64decode(b"".join(ARCHIVE_TEXT.read_bytes().split()), validate=True)
        self.assertEqual(sha(archive), '7f75db2d12038c24a57a12f2bdb1f37b2220f873b34ea7247121aa7c5b9b4ced')
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as handle:
            members = {m.name: handle.extractfile(m).read() for m in handle.getmembers() if m.isfile()}
        self.assertEqual(sorted(members), sorted(EXPECTED_MEMBERS))
        declared = {line.split(maxsplit=1)[1]: line.split(maxsplit=1)[0] for line in (BATCH / "bundle/qartheen_enthroned_guardian_phase1.members.sha256").read_text().splitlines()}
        self.assertEqual(declared, {name: sha(data) for name, data in members.items()})
        with (BATCH / "screenshots_manifest.csv").open(newline="", encoding="utf-8") as handle:
            screenshots = list(csv.DictReader(handle))
        self.assertEqual(len(screenshots), 10)
        self.assertEqual(len({r["battle_id"] for r in screenshots}), 10)
        self.assertEqual({r["screen_status"] for r in screenshots}, {"final_result"})
        self.assertEqual({r["game_track"] for r in screenshots}, {"realm_of_thrones"})
        self.assertEqual({r["game_version"] for r in screenshots}, {"1.4.x"})
        self.assertEqual({r["image_file"]: r["image_sha256"] for r in screenshots}, EXPECTED_SOURCES)
        rows = [json.loads(line) for name, data in sorted(members.items()) if name.startswith("normalized/player_rows/b") for line in data.splitlines()]
        self.assertEqual(sum(r["row_type"] == "ordinary_troop" for r in rows), 79)
        self.assertEqual(sum(r["row_type"] == "character" for r in rows), 74)
        self.assertEqual(sum(r["visibility_status"] == "partial" for r in rows), 2)
        report = json.loads(members["integrity_report.json"])
        self.assertTrue(all(v is True or isinstance(v, int) for v in report["checks"].values()))

if __name__ == "__main__": unittest.main()
