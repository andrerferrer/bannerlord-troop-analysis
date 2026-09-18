"""Adversarial/production gates for weapon-first audit; no battle simulation."""
from __future__ import annotations
import copy
import csv
import hashlib
import io
import json
import unittest
from pathlib import Path
from scripts.analysis.weapon_first_audit import (BASE, FOCUS, QUEUE, Source, canonical_json,
    compare_pair, eligible_pair, family, generate, number, operator_queue, unique_index)

ROOT = Path(__file__).resolve().parents[1]


def pair(**changes):
    row = {'damage': 100, 'attack_speed': 90, 'attack_usage': 'swing',
           'damage_type': 'Cut', 'weapon_class': 'TwoHandedSword', 'context': 'field',
           'mount_state': 'mounted', 'track': 'realm_of_thrones', 'profile': 'same-source-profile',
           'source_reference': 'verified_fixture', 'evidence_grade': 'direct_usage_verified',
           'usage_verified': True, 'context_usable': True}
    row.update(changes)
    return row


class PrimaryInputTests(unittest.TestCase):
    def test_no_invalid_or_nonfinite_numbers(self):
        for value in (None, '', ' ', True, False, 'garbage', 'nan', float('nan'), 'inf', '-inf', -1):
            with self.subTest(value=value):
                self.assertIsNone(number(value))

    def test_explicit_zero_is_not_missing_but_not_a_positive_pair(self):
        self.assertEqual(number('0'), 0)
        self.assertFalse(eligible_pair(pair(damage=0)))
        self.assertFalse(eligible_pair(pair(attack_speed=0)))

    def test_no_skill_or_generic_rating_fallback(self):
        self.assertFalse(eligible_pair(pair(attack_speed=None, speed_rating=100, TwoHanded=1000)))
        self.assertFalse(eligible_pair(pair(damage=None, template='TwoHandedSword', melee_proxy=100)))

    def test_rejects_unknown_mount_and_context_even_when_both_equal(self):
        self.assertFalse(eligible_pair(pair(mount_state='unknown')))
        self.assertFalse(eligible_pair(pair(context='unknown')))

    def test_requires_usage_and_mount_usability_verification(self):
        self.assertFalse(eligible_pair(pair(usage_verified=False)))
        self.assertFalse(eligible_pair(pair(context_usable=False)))

    def test_no_unvalidated_source_grade(self):
        for grade in ('low_confidence_family_prior', 'crafted_unvalidated', 'proxy', None):
            self.assertFalse(eligible_pair(pair(evidence_grade=grade)))

    def test_requires_usage_and_provenance(self):
        for key in ('source_reference', 'profile', 'context', 'mount_state', 'weapon_class', 'damage_type'):
            self.assertFalse(eligible_pair(pair(**{key: ''})))
        self.assertFalse(eligible_pair(pair(attack_usage='best-of-swing-and-thrust')))

    def test_throwing_axes_not_silent_melee(self):
        for template in ('ThrowingAxe', 'ROT_ThrowingAxe', 'ThrowingKnife', 'Javelin'):
            self.assertEqual(family({'item_found': 'True', 'item_kind': 'CraftedItem', 'crafting_template': template}), 'thrown')

    def test_pike_and_dagger_not_same_unknown_proxy(self):
        for template in ('Pike', 'Dagger', 'TwoHandedMace'):
            self.assertEqual(family({'item_found': 'True', 'item_kind': 'CraftedItem', 'crafting_template': template}), 'melee')

    def test_missing_item_and_unknown_template_retained(self):
        self.assertEqual(family({'item_found': 'False'}), 'unresolved_item')
        self.assertEqual(family({'item_found': 'True', 'item_kind': 'CraftedItem', 'crafting_template': 'ImaginaryAxe'}), 'unresolved_template')

    def test_shield_not_offensive_melee(self):
        self.assertEqual(family({'item_found': 'True', 'item_kind': 'Item', 'type': 'Shield'}), 'non_melee')


class ComparatorTests(unittest.TestCase):
    def test_strict_two_dimension_dominance(self):
        self.assertEqual(compare_pair(pair(damage=120, attack_speed=95), pair()), 'a_dominates_on_damage_and_speed')
        self.assertEqual(compare_pair(pair(), pair(damage=120, attack_speed=95)), 'b_dominates_on_damage_and_speed')

    def test_one_equal_dimension_can_dominate(self):
        self.assertEqual(compare_pair(pair(damage=120), pair()), 'a_dominates_on_damage_and_speed')

    def test_tradeoff_has_no_invented_weight(self):
        self.assertEqual(compare_pair(pair(damage=120, attack_speed=70), pair()), 'tradeoff_no_total_order')

    def test_skills_last_do_not_change_pair_result(self):
        self.assertEqual(compare_pair(pair(TwoHanded=1), pair(TwoHanded=10000)), 'equal')

    def test_no_cross_profile_context_mount_class_type_or_mode_pooling(self):
        for key in ('track', 'profile', 'context', 'mount_state', 'weapon_class', 'damage_type', 'attack_usage'):
            self.assertEqual(compare_pair(pair(**{key: 'other'}), pair()), 'incomparable')

    def test_unknown_pair_does_not_lose_or_win(self):
        self.assertEqual(compare_pair(pair(damage=None), pair()), 'incomparable')

    def test_comparator_symmetry_and_no_overflow_products(self):
        for d in (1, 90, 100, 150, 1e308):
            for s in (1, 90, 100, 150, 1e308):
                a = compare_pair(pair(damage=d, attack_speed=s), pair())
                b = compare_pair(pair(), pair(damage=d, attack_speed=s))
                self.assertEqual({'a_dominates_on_damage_and_speed': 'b_dominates_on_damage_and_speed', 'b_dominates_on_damage_and_speed': 'a_dominates_on_damage_and_speed'}.get(a, a), b)

    def test_unique_identity_gate(self):
        with self.assertRaises(ValueError):
            unique_index([{'id': 'a'}, {'id': 'a'}], 'id')


class ProductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs = generate(ROOT)
        cls.summary = json.loads(cls.outputs['summary.json'])
        cls.original_queue = json.loads(Source(ROOT).read(QUEUE))

    def test_complete_pinned_population_covered(self):
        self.assertEqual(self.summary['raw_soldiers'], 1232)
        self.assertEqual(self.summary['selected_troops'], 865)
        rows = list(csv.DictReader(io.StringIO(self.outputs['troop_coverage.csv'].decode())))
        self.assertEqual(len(rows), 865)
        self.assertEqual(len({r['troop_id'] for r in rows}), 865)

    def test_no_melee_template_or_skill_rank_created(self):
        self.assertEqual(self.summary['complete_usage_pairs'], 0)
        self.assertFalse(self.summary['rank_generated'])
        self.assertFalse(self.summary['skill_used_for_priority'])
        self.assertEqual(len(self.outputs['verified_usage_pairs.csv'].decode().splitlines()), 1)

    def test_families_reconcile_and_ambiguity_not_hidden(self):
        self.assertEqual(sum(self.summary['families'].values()), self.summary['weapon_slot_rows'])
        self.assertEqual(sum(self.summary['evidence_grades'].values()), self.summary['melee_or_unresolved_slot_rows'])
        self.assertEqual(self.summary['evidence_grades']['ambiguous_slot'], 2)
        self.assertEqual(self.summary['families']['unresolved_item'], 5)

    def test_yiti_actual_full_loadout_not_sword_only(self):
        rows = [r for r in json.loads(self.outputs['focus_loadouts.json']) if r['troop_id'] == 'yiti_samurai']
        self.assertEqual([r['item_id'] for r in rows], ['yiti_sword', 'yiti_qinglongji', 'empire_throwingknife_t5', 'empire_throwingknife_t5'])
        self.assertEqual(len({r['slot'] for r in rows}), 4)
        self.assertTrue(all(r['mount_state'] == 'mounted' for r in rows))
        self.assertTrue(all(r['stack_amount'] is None for r in rows))
        self.assertTrue(all(r['swing_damage'] is None and r['thrust_damage'] is None for r in rows))

    def test_all_comparison_focus_units_retained(self):
        self.assertEqual({r['troop_id'] for r in json.loads(self.outputs['focus_loadouts.json'])}, set(FOCUS))

    def test_every_legacy_sensitivity_row_rejected(self):
        rows = json.loads(self.outputs['legacy_rejected_profiles.json'])
        self.assertEqual(len(rows), 20)
        self.assertTrue(all(r['admitted_to_current_comparison'] is False for r in rows))
        self.assertEqual(json.loads(self.outputs['repository_evidence_search.json'])['v44_exact_profile_template_data_rows'], 0)

    def test_artifact_hashes_verify(self):
        hashes = json.loads(self.outputs['artifact_hashes.json'])
        self.assertEqual(set(hashes), set(self.outputs) - {'artifact_hashes.json'})
        self.assertTrue(all(hashlib.sha256(self.outputs[k]).hexdigest() == v for k, v in hashes.items()))

    def test_byte_identical_regeneration(self):
        self.assertEqual(self.outputs, generate(ROOT))

    def test_explicit_override_preserves_other_queue_states(self):
        old = self.original_queue
        original_bytes = canonical_json(old)
        new = operator_queue(old)
        self.assertEqual(canonical_json(old), original_bytes)
        self.assertEqual(new['active_test']['troop_id'], 'yiti_samurai')
        self.assertEqual(new['active_test']['weapon_evidence_status'], 'damage_and_usage_speed_pending')
        for field in ('closed', 'verification_holds', 'ordered_queue', 'authority', 'update_contract'):
            self.assertEqual(new[field], old[field])
        self.assertEqual(new['parked'], [r for r in old['parked'] if r['troop_id'] != 'yiti_samurai'])

    def test_conflicting_operator_snapshot_refused(self):
        for field, value in (('active_test', {'troop_id': 'other'}), ('ordered_queue', [{'troop_id': 'other'}]), ('track', 'vanilla')):
            changed = copy.deepcopy(self.original_queue)
            changed[field] = value
            with self.assertRaises(ValueError):
                operator_queue(changed)

    def test_closed_or_held_target_cannot_be_silently_reopened(self):
        for field in ('closed', 'verification_holds'):
            changed = copy.deepcopy(self.original_queue)
            changed[field].append({'troop_id': 'yiti_samurai'})
            with self.assertRaises(ValueError):
                operator_queue(changed)

    def test_no_zero_filled_missing_inputs(self):
        rows = list(csv.DictReader(io.StringIO(self.outputs['melee_weapon_audit.csv'].decode())))
        self.assertTrue(all(r['swing_damage'] == '' and r['thrust_damage'] == '' for r in rows))

    def test_scope_is_not_live_game_compatibility_claim(self):
        self.assertEqual(self.summary['live_installation_equivalence'], 'unverified')
        self.assertIn('v1.4.7', self.summary['game_version_from_package'])

if __name__ == '__main__':
    unittest.main()
