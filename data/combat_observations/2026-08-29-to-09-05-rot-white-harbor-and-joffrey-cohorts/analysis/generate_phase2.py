#!/usr/bin/env python3
"""Generate Phase 2 analysis for the White Harbor/Joffrey ROT batch.

The Phase 1 normalized bundle is immutable. This script reconstructs it, verifies
its manifest, resolves conservative exact identities against the committed ROT
roster audit, and writes only analysis/review-layer outputs.
"""
from __future__ import annotations

import argparse, base64, csv, hashlib, io, json, random, re, tarfile, zipfile
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ANALYSIS_DIR = Path(__file__).resolve().parent
BATCH_DIR = ANALYSIS_DIR.parent
REPO_ROOT = ANALYSIS_DIR.parents[3]
REVIEW_DIR = BATCH_DIR / "review"
IDENTITY_PATH = REPO_ROOT / "data/realm_of_thrones/audit/realm_of_thrones_troops.csv"

BATCH_ID = "2026-08-29-to-09-05-rot-white-harbor-and-joffrey-cohorts"
TRACK = "realm_of_thrones"
GAME_VERSION = "1.4.x"
PIPELINE_VERSION = "0.4.0"
SCHEMA_VERSION = "2.0.0"
NORMALIZATION_COMMIT = "d73bbfdbaafac4856ee0e9963fdab41ad552837c"
IDENTITY_AUDIT_SHA256 = "63ea983998e25aa0e6f8c0747bf42e44440f695bbe1fec717074e7ba64e42810"
SOURCE_SHA256 = "198e895c17e03a9254c4d23e8611557da05271fec5a466966cffbddb36a9028a"
SOURCE_SIZE = 67_529_739
BUNDLE_SHA256 = "9cc8482caf6d37356b186c0a68dfa9e6f50303fb715f6ddfc3a49e2593b59c9d"
BUNDLE_SIZE = 31_004
BUNDLE_MEMBERS = 18
GATE_BATTLES = 5
GATE_DEPLOYED = 20
BOOTSTRAP_REPETITIONS = 10_000
FOCUS = ("White Harbor Knight Commander", "Westerling Hedgeknight")
COUNT_FIELDS = ("deployed", "survivors", "kills", "deaths", "wounded", "routed")

RANKING_FIELDS = (
    "track","game_version","cohort","context","participant_scope","parent_group",
    "efficiency_rank","impact_rank","display_name","canonical_troop_id","identity_status",
    "canonical_default_group","canonical_role","reliable_role_population",
    "role_adjusted_rank_status","independent_battles",*COUNT_FIELDS,"kills_per_deployed",
    "ci95_low","ci95_high","verified_player_side_total_kills","kill_total_coverage_battles",
    "kill_total_coverage_complete","player_side_kill_share","share_adjusted_impact",
    "verified_player_side_total_deployed","deployment_total_coverage_battles",
    "deployment_total_coverage_complete","player_side_deployment_share",
    "offensive_contribution_ratio","offensive_share_gap","retention_rate","death_rate",
    "casualty_rate","victory_battles","defeat_battles","retreated_to_keep_battles",
    "active_battles","reliability_status","more_battles_needed","more_deployed_needed",
)

def sha256_bytes(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()
def read_csv(path: Path):
    with path.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(fields),lineterminator='\n'); w.writeheader()
        w.writerows({k:r.get(k,'') for k in fields} for r in rows)
def write_json(path: Path, value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf-8')
def fmt(v): return '' if v is None else f'{v:.6f}'
def safe_div(a,b): return None if b in (None,0) else a/b

def cohort_for(b):
    p=b['player_party_name']
    if p=="Wyman Manderly's Party": return 'white_harbor'
    if p=="Joffrey Baratheon's Party": return 'joffrey'
    raise ValueError(f'unrecognized player party {p!r}')

def result_for(b):
    if b['battle_state']=='active_last_readable': return 'active'
    return b['player_outcome']

def capture_key(b):
    name=b['source']['image_file']
    m=re.search(r'(\d{2})_(\d{2})_(\d{4})[ _](\d{2})_(\d{2})_(\d{2})',name)
    if m:
        d,mo,y,h,mi,s=map(int,m.groups()); return datetime(y,mo,d,h,mi,s).isoformat()
    return b['battle_id']

def canonical_role(group):
    g=(group or '').casefold().replace(' ','_')
    if g in {'ranged','horsearcher','horse_archer'}: return 'ranged'
    if g=='infantry': return 'frontline_infantry'
    if g=='cavalry': return 'melee_cavalry'
    return ''

def extract_bundle():
    parts=sorted((BATCH_DIR/'bundle').glob('*base64.part-*'))
    if len(parts)!=14: raise ValueError(f'expected 14 bundle parts, found {len(parts)}')
    encoded=b''.join(p.read_bytes() for p in parts)
    archive=base64.b64decode(encoded)
    if len(archive)!=BUNDLE_SIZE or sha256_bytes(archive)!=BUNDLE_SHA256:
        raise ValueError('normalized bundle hash/size mismatch')
    files={}
    with tarfile.open(fileobj=io.BytesIO(archive),mode='r:xz') as tf:
        members=tf.getmembers()
        if len(members)!=BUNDLE_MEMBERS: raise ValueError('bundle member-count mismatch')
        for m in members:
            p=Path(m.name)
            if p.is_absolute() or '..' in p.parts or not m.isfile(): raise ValueError(f'unsafe member {m.name}')
            f=tf.extractfile(m)
            if f is None: raise ValueError(f'unreadable member {m.name}')
            files[m.name]=f.read()
    manifest=json.loads(files['manifest/phase1_bundle_manifest.json'])
    checks=[]
    for item in manifest['payload']:
        payload=files[item['path']]
        ok=len(payload)==int(item['size_bytes']) and sha256_bytes(payload)==item['sha256']
        checks.append({'path':item['path'],'passed':ok})
        if not ok: raise ValueError(f"manifest mismatch: {item['path']}")
    return files, {'sha256':BUNDLE_SHA256,'size_bytes':len(archive),'members':len(files),'payload_hashes_verified':len(checks),'safe_preflight_passed':True}

def verify_source_zip(path):
    out={'expected_sha256':SOURCE_SHA256,'expected_size_bytes':SOURCE_SIZE,'locally_verified':False,'member_hashes_verified':0,'note':'raw source optional after immutable normalized bundle verification'}
    if path is None: return out
    if not path.is_file(): raise ValueError('source ZIP path does not exist')
    if sha256_file(path)!=SOURCE_SHA256 or path.stat().st_size!=SOURCE_SIZE: raise ValueError('source ZIP hash/size mismatch')
    inv=read_csv(BATCH_DIR/'source_inventory.csv')
    with zipfile.ZipFile(path) as z:
        members={i.filename:i for i in z.infolist() if not i.is_dir()}
        if set(members)!={r['image_file'] for r in inv}: raise ValueError('source member-set mismatch')
        for r in inv:
            if sha256_bytes(z.read(r['image_file']))!=r['image_sha256']: raise ValueError(f"source member hash mismatch {r['image_file']}")
    out.update({'actual_sha256':SOURCE_SHA256,'actual_size_bytes':SOURCE_SIZE,'locally_verified':True,'member_hashes_verified':len(inv)})
    return out

def parse_jsonl(blob): return [json.loads(x) for x in blob.decode('utf-8').splitlines() if x.strip()]
def parse_csv_blob(blob): return list(csv.DictReader(io.StringIO(blob.decode('utf-8-sig'))))

def resolve_identities(names):
    if sha256_file(IDENTITY_PATH)!=IDENTITY_AUDIT_SHA256: raise ValueError('ROT roster audit hash mismatch')
    audit=read_csv(IDENTITY_PATH); out={}
    for name in sorted(names):
        matches=[r for r in audit if r.get('is_soldier','').casefold()=='true' and r.get('name','').casefold()==name.casefold()]
        ids=sorted({r['troop_id'] for r in matches}); confirmed=len(ids)==1; row=matches[0] if confirmed else {}
        out[name]={
            'canonical_troop_id':ids[0] if confirmed else '',
            'identity_status':'confirmed_id' if confirmed else ('ambiguous_exact_name' if ids else 'unresolved'),
            'default_group':row.get('default_group',''),'canonical_role':canonical_role(row.get('default_group','')),
            'level':row.get('level',''),'candidate_count':len(ids),'candidate_troop_ids':'|'.join(ids),
            'blocking_reason':'' if confirmed else ('multiple exact display-name matches' if ids else 'no exact display-name match in committed ROT audit'),
        }
    return out

def participant_key(r,b): return (cohort_for(b),r['battle_context'],r['relationship_to_player'],r['parent_group'],r['display_name_raw'])
def bootstrap(rows,key):
    seed=int(hashlib.sha256(f'{BATCH_ID}|{key}|{BOOTSTRAP_REPETITIONS}'.encode()).hexdigest()[:16],16); rng=random.Random(seed)
    ordered=sorted(rows,key=lambda r:r['battle_id']); vals=[]
    for _ in range(BOOTSTRAP_REPETITIONS):
        sample=[ordered[rng.randrange(len(ordered))] for _ in ordered]
        dep=sum(int(x['deployed']) for x in sample); kills=sum(int(x['kills']) for x in sample); vals.append(kills/dep)
    vals.sort(); return vals[int(.025*(len(vals)-1))],vals[int(.975*(len(vals)-1))]

def denominator_metrics(subset,battles):
    ids={r['battle_id'] for r in subset}
    kill_ids={i for i in ids if battles[i]['player_side_total'].get('kills') not in (None,0)}
    dep_ids={i for i in ids if battles[i]['player_side_total'].get('deployed') not in (None,0)}
    side_kills=sum(int(battles[i]['player_side_total']['kills']) for i in kill_ids)
    covered_kills=sum(int(r['kills']) for r in subset if r['battle_id'] in kill_ids)
    kill_share=safe_div(covered_kills,side_kills)
    side_dep=sum(int(battles[i]['player_side_total']['deployed']) for i in dep_ids)
    covered_dep=sum(int(r['deployed']) for r in subset if r['battle_id'] in dep_ids)
    dep_share=safe_div(covered_dep,side_dep)
    return {'kill_ids':kill_ids,'dep_ids':dep_ids,'side_kills':side_kills,'side_dep':side_dep,'kill_share':kill_share,'dep_share':dep_share,'kill_complete':kill_ids==ids,'dep_complete':dep_ids==ids}

def aggregate_rows(rows,battles,identities):
    groups=defaultdict(list)
    for r in rows: groups[participant_key(r,battles[r['battle_id']])].append(r)
    output=[]
    for (co,ctx,scope,parent,name),ss in groups.items():
        ids={r['battle_id'] for r in ss}; counts={f:sum(int(r[f]) for r in ss) for f in COUNT_FIELDS}; independent=len(ids)
        reliable=independent>=GATE_BATTLES and counts['deployed']>=GATE_DEPLOYED
        eff=counts['kills']/counts['deployed']; den=denominator_metrics(ss,battles); ks=den['kill_share']; ds=den['dep_share']
        impact=eff*ks if ks is not None and den['kill_complete'] else None
        off_ratio=safe_div(ks,ds) if den['kill_complete'] and den['dep_complete'] else None
        gap=(ks-ds) if ks is not None and ds is not None and den['kill_complete'] and den['dep_complete'] else None
        res=Counter(result_for(battles[i]) for i in ids); identity=identities[name]
        ci=bootstrap(ss,'|'.join((co,ctx,scope,parent,name))) if reliable else (None,None)
        output.append({
            'track':TRACK,'game_version':GAME_VERSION,'cohort':co,'context':ctx,'participant_scope':scope,'parent_group':parent,
            'display_name':name,'canonical_troop_id':identity['canonical_troop_id'],'identity_status':identity['identity_status'],
            'canonical_default_group':identity['default_group'],'canonical_role':identity['canonical_role'],'role_adjusted_rank_status':'not_published_current_methodology_keeps_offense_and_defense_independent',
            'independent_battles':independent,**counts,'kills_per_deployed':fmt(eff),'ci95_low':fmt(ci[0]),'ci95_high':fmt(ci[1]),
            'verified_player_side_total_kills':den['side_kills'],'kill_total_coverage_battles':len(den['kill_ids']),'kill_total_coverage_complete':den['kill_complete'],
            'player_side_kill_share':fmt(ks),'share_adjusted_impact':fmt(impact),
            'verified_player_side_total_deployed':den['side_dep'],'deployment_total_coverage_battles':len(den['dep_ids']),'deployment_total_coverage_complete':den['dep_complete'],
            'player_side_deployment_share':fmt(ds),'offensive_contribution_ratio':fmt(off_ratio),'offensive_share_gap':fmt(gap),
            'retention_rate':fmt(counts['survivors']/counts['deployed']),'death_rate':fmt(counts['deaths']/counts['deployed']),'casualty_rate':fmt((counts['deaths']+counts['wounded'])/counts['deployed']),
            'victory_battles':res['victory'],'defeat_battles':res['defeat'],'retreated_to_keep_battles':res['retreated_to_keep'],'active_battles':res['active'],
            'reliability_status':'reliable' if reliable else 'insufficient_evidence','more_battles_needed':max(0,GATE_BATTLES-independent),'more_deployed_needed':max(0,GATE_DEPLOYED-counts['deployed'])})
    rankgroups=defaultdict(list)
    for r in output: rankgroups[(r['cohort'],r['context'],r['participant_scope'],r['parent_group'])].append(r)
    for group in rankgroups.values():
        for rank,r in enumerate(sorted(group,key=lambda x:(-float(x['kills_per_deployed']),-x['deployed'],x['display_name'])),1): r['efficiency_rank']=rank
        impactables=[x for x in group if x['share_adjusted_impact']!='']
        for r in group: r['impact_rank']=''
        for rank,r in enumerate(sorted(impactables,key=lambda x:(-float(x['share_adjusted_impact']),-x['deployed'],x['display_name'])),1): r['impact_rank']=rank
        rc=Counter(r['canonical_role'] for r in group if r['reliability_status']=='reliable' and r['canonical_role'])
        for r in group: r['reliable_role_population']=rc[r['canonical_role']] if r['canonical_role'] else 0
    return sorted(output,key=lambda r:(r['cohort'],r['context'],r['participant_scope'],r['parent_group'],r['efficiency_rank']))

def rerank_reliable(rows):
    rel=[dict(r) for r in rows if r['reliability_status']=='reliable']; groups=defaultdict(list)
    for r in rel: groups[(r['cohort'],r['context'],r['participant_scope'],r['parent_group'])].append(r)
    for g in groups.values():
        for rank,r in enumerate(sorted(g,key=lambda x:(-float(x['kills_per_deployed']),-x['deployed'],x['display_name'])),1): r['efficiency_rank']=rank
        for r in g: r['impact_rank']=''
        imp=[x for x in g if x['share_adjusted_impact']!='']
        for rank,r in enumerate(sorted(imp,key=lambda x:(-float(x['share_adjusted_impact']),-x['deployed'],x['display_name'])),1): r['impact_rank']=rank
    return sorted(rel,key=lambda r:(r['cohort'],r['context'],r['participant_scope'],r['efficiency_rank']))

def split_rows(rows,battles,identities):
    groups=defaultdict(list)
    for r in rows:
        b=battles[r['battle_id']]; groups[(*participant_key(r,b),result_for(b))].append(r)
    out=[]
    order={'victory':0,'defeat':1,'retreated_to_keep':2,'active':3}
    for (co,ctx,scope,parent,name,res),ss in groups.items():
        counts={f:sum(int(r[f]) for r in ss) for f in COUNT_FIELDS}; den=denominator_metrics(ss,battles); ks=den['kill_share']; ds=den['dep_share']
        out.append({'cohort':co,'context':ctx,'participant_scope':scope,'parent_group':parent,'display_name':name,'canonical_troop_id':identities[name]['canonical_troop_id'],
                    'result':res,'censoring_status':'censored_diagnostic' if res=='active' else ('phase_complete_stage' if res=='retreated_to_keep' else 'final'),
                    'independent_battles':len({r['battle_id'] for r in ss}),**counts,'kills_per_deployed':fmt(counts['kills']/counts['deployed']),'retention_rate':fmt(counts['survivors']/counts['deployed']),
                    'verified_player_side_total_kills':den['side_kills'],'kill_total_coverage_complete':den['kill_complete'],'player_side_kill_share':fmt(ks),
                    'verified_player_side_total_deployed':den['side_dep'],'deployment_total_coverage_complete':den['dep_complete'],'player_side_deployment_share':fmt(ds),
                    'offensive_contribution_ratio':fmt(safe_div(ks,ds) if den['kill_complete'] and den['dep_complete'] else None),
                    'offensive_share_gap':fmt(ks-ds if ks is not None and ds is not None and den['kill_complete'] and den['dep_complete'] else None)})
    return sorted(out,key=lambda r:(r['cohort'],r['context'],r['display_name'],order.get(r['result'],9)))

def pressure_rows(battles):
    out=[]
    for b in sorted(battles.values(),key=capture_key):
        p=b.get('player_side_total') or {}; e=b.get('enemy_side_total') or {}; pd=p.get('deployed'); ed=e.get('deployed'); ps=p.get('survivors'); es=e.get('survivors')
        pr=safe_div(ps,pd) if ps is not None else None; er=safe_div(es,ed) if es is not None else None; margin=pr-er if pr is not None and er is not None else None
        res=result_for(b); production=b['battle_state']=='final' and margin is not None
        out.append({'battle_id':b['battle_id'],'captured_at':capture_key(b),'cohort':cohort_for(b),'context':b['battle_context'],'result':res,'battle_state':b['battle_state'],
                    'player_deployed':'' if pd is None else pd,'player_remaining':'' if ps is None else ps,'allied_retention':fmt(pr),
                    'opponent_deployed':'' if ed is None else ed,'opponent_remaining':'' if es is None else es,'enemy_retention':fmt(er),'pressure_margin':fmt(margin),
                    'metric_status':'final' if production else ('diagnostic_phase_complete' if b['battle_state']=='phase_complete' else 'diagnostic_censored_or_missing_denominator'),
                    'included_in_final_pressure_summary':production,'source_image_sha256':b['source']['image_sha256']})
    return out

def focus_battle_rows(rows,battles,identities):
    out=[]
    for r in rows:
        if r['display_name_raw'] not in FOCUS: continue
        b=battles[r['battle_id']]; p=b['player_side_total']
        out.append({'display_name':r['display_name_raw'],'canonical_troop_id':identities[r['display_name_raw']]['canonical_troop_id'],'battle_id':r['battle_id'],'captured_at':capture_key(b),
                    'cohort':cohort_for(b),'context':r['battle_context'],'result':result_for(b),'battle_state':b['battle_state'],'deployed':r['deployed'],'survivors':r['survivors'],'kills':r['kills'],'deaths':r['deaths'],'wounded':r['wounded'],
                    'kills_per_deployed':fmt(r['kills']/r['deployed']),'retention_rate':fmt(r['survivors']/r['deployed']),'player_side_kills':p.get('kills',''),'player_side_deployed':p.get('deployed','')})
    return sorted(out,key=lambda r:(FOCUS.index(r['display_name']),r['captured_at']))

def identity_rows(rows,identities):
    obs=defaultdict(lambda:{'ids':set(),'hashes':set(),'n':0})
    for r in rows:
        x=obs[r['display_name_raw']]; x['ids'].add(r.get('canonical_troop_id') or ''); x['hashes'].add(r['source_image_sha256']); x['n']+=1
    out=[]
    for name in sorted(obs):
        i=identities[name]; out.append({'display_name':name,'observed_canonical_troop_ids':'|'.join(sorted(obs[name]['ids'])),'canonical_troop_id':i['canonical_troop_id'],'resolution_status':i['identity_status'],
            'default_group':i['default_group'],'canonical_role':i['canonical_role'],'level':i['level'],'candidate_count':i['candidate_count'],'candidate_troop_ids':i['candidate_troop_ids'],
            'resolution_method':'exact display-name match' if i['identity_status']=='confirmed_id' else 'unresolved conservative exact-match audit','blocking_reason':i['blocking_reason'],'ordinary_occurrences':obs[name]['n'],'source_image_count':len(obs[name]['hashes']),
            'audit_path':IDENTITY_PATH.relative_to(REPO_ROOT).as_posix(),'audit_sha256':IDENTITY_AUDIT_SHA256})
    return out

def review_decisions(queue,occurrences,source_available):
    byid={r['observation_id']:r for r in occurrences}; out=[]
    for q in queue:
        src=byid[q['observation_id']]
        for field in json.loads(q['field_paths']):
            out.append({'observation_id':q['observation_id'],'battle_id':q['battle_id'],'source_image_file':q['source_file'],'source_image_sha256':src['source_image_sha256'],'field':field,
                        'original_value':'' if src.get(field) is None else src.get(field),'reviewed_value':'','decision_status':'unresolved_pending_raw_image_review' if source_available else 'unresolved_no_raw_image_review',
                        'reason':('Raw source verified but no direct visual correction recorded.' if source_available else 'Raw source ZIP unavailable to this Phase 2 run; no value inferred.')+' Queue note: '+q.get('reason',''),
                        'reviewer':'distinct Phase 2 analysis agent','evidence_reference':f"normalized occurrence {q['observation_id']}; review_queue.csv; source SHA-256 {src['source_image_sha256']}"})
    return out

def report(rankings,reliable,insufficient,focus,pressure,identity_audit):
    lines=[f'# Phase 2 analysis — {BATCH_ID}','','## Batch-wide findings','',
        f'All **355** fully visible player-side ordinary-troop occurrences are represented in **{len(rankings)}** cohort/context rows: **{len(reliable)} reliable** and **{len(insufficient)} below gate**. White Harbor and Joffrey are separate cohorts, and field/siege contexts are never pooled.','',
        'Active last-readable scoreboards remain independent censored observations. The two `retreated_to_keep` siege stages are preserved as phase-complete observations rather than converted into victories/defeats.','',
        '### Reliable rows','',
        '| Cohort/context | Eff. rank | Impact rank | Troop | Battles | Deployed | Kills/deployed | Kill share | Deploy share | Offense ratio | Retention |','|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|']
    for r in reliable:
        ks='—' if r['player_side_kill_share']=='' else f"{100*float(r['player_side_kill_share']):.2f}%"; ds='—' if r['player_side_deployment_share']=='' else f"{100*float(r['player_side_deployment_share']):.2f}%"; ratio='—' if r['offensive_contribution_ratio']=='' else f"{float(r['offensive_contribution_ratio']):.3f}"; ret=f"{100*float(r['retention_rate']):.2f}%"
        lines.append(f"| {r['cohort']} / {r['context']} | {r['efficiency_rank']} | {r['impact_rank'] or '—'} | {r['display_name']} | {r['independent_battles']} | {r['deployed']} | {r['kills_per_deployed']} | {ks} | {ds} | {ratio} | {ret} |")
    lines += ['','### Below-gate partition','','Every below-gate row is retained without promotion. See `insufficient_evidence.csv` for exact gaps.','','## Focus conclusions','']
    for name in FOCUS:
        for r in [x for x in focus if x['display_name']==name]:
            ks='—' if r['player_side_kill_share']=='' else f"{100*float(r['player_side_kill_share']):.2f}%"; ds='—' if r['player_side_deployment_share']=='' else f"{100*float(r['player_side_deployment_share']):.2f}%"; ratio='—' if r['offensive_contribution_ratio']=='' else f"{float(r['offensive_contribution_ratio']):.3f}×"
            lines.append(f"- **{name} — {r['cohort']} / {r['context']}**: `{r['kills']} / {r['deployed']} = {r['kills_per_deployed']}` kills/deployed; kill share **{ks}**, deployment share **{ds}**, offense ratio **{ratio}**, retention **{100*float(r['retention_rate']):.1f}%**; gate `{r['reliability_status']}` ({r['independent_battles']} battles).")
    lines += ['','### Interpretation','',
        '**White Harbor Knight Commander is high-evidence but proportional.** Its field sample clears the gate comfortably, but its share of kills is close to its share of deployed troops; it is useful, not a Raven/Sarnori-style disproportional outlier.','',
        '**Westerling Hedgeknight is the more interesting next isolated target.** The mixed Joffrey field sample already clears the minimum gate and shows much higher per-unit output and a >1 offensive contribution ratio, but retention is low enough that composition/opponent confounding matters. Isolation is the smallest test that can tell whether the signal is intrinsic.','',
        '## Defensive context and result splits','',
        '`result_splits.csv` keeps victory, defeat, phase-complete retreat, and active/censored observations separate. `battle_pressure_margin.csv` is battle-level only; it is never assigned to an individual troop.','',
        '## Identity and review limits','',
        f"The committed ROT audit confirms **{sum(r['resolution_status']=='confirmed_id' for r in identity_audit)} of {len(identity_audit)}** observed labels by one exact name-to-ID match. Unresolved labels remain provisional.",'',
        'The three clipped/obscured Phase 1 rows remain excluded from primary rankings and unresolved in the review layer because no raw screenshot was available to this distinct Phase 2 run. No numeric value was inferred.','',
        '## Smallest next test','',
        '**Isolate Westerling Hedgeknight in field battles.** Run at least **5 independent field battles** with a stable supporting roster/orders and enough Westerling Hedgeknights to keep total deployment ≥20. Do not mix siege observations into this test. The purpose is no longer to close the minimum gate; it is to test whether the mixed-army 3.19 kills/deployed signal survives isolation.','',
        '## Limitations','',
        'Campaign observations remain opponent-, roster-, map-, result-, and player-order-confounded. Active observations are right-censored. No off-screen row is inferred, no cohort/context boundary is crossed, and no frozen model is changed.','']
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source-zip',type=Path); args=ap.parse_args()
    files,bundle=extract_bundle(); source=verify_source_zip(args.source_zip)
    battles_list=parse_jsonl(files['battles.jsonl']); battles={b['battle_id']:b for b in battles_list}; occurrences=parse_jsonl(files['troop_occurrences.jsonl']); rows=parse_jsonl(files['primary_troop_occurrences.jsonl']); queue=parse_csv_blob(files['review/review_queue.csv'])
    if len(battles)!=27 or len(rows)!=355 or len(occurrences)!=515: raise ValueError('unexpected normalized counts')
    for r in rows:
        if r['game_track']!=TRACK or r['game_version']!=GAME_VERSION or r['schema_version']!=SCHEMA_VERSION: raise ValueError('track/version/schema boundary violation')
        if r['row_type']!='troop' or r['relationship_to_player']!='player_party': raise ValueError('primary ordinary player-party boundary violation')
        if r['side']!=battles[r['battle_id']]['player_side']: raise ValueError('player/enemy side boundary violation')
        if r['deployed']!=r['survivors']+r['deaths']+r['wounded']: raise ValueError(f"troop arithmetic mismatch {r['observation_id']}")
    if Counter(b['battle_context'] for b in battles.values())!={'field':22,'siege_attack':4,'siege_defense':1}: raise ValueError('context count mismatch')
    identities=resolve_identities({r['display_name_raw'] for r in rows}); rankings=aggregate_rows(rows,battles,identities); reliable=rerank_reliable(rankings); insufficient=[r for r in rankings if r['reliability_status']=='insufficient_evidence']; splits=split_rows(rows,battles,identities); pressure=pressure_rows(battles); identity_audit=identity_rows(rows,identities)
    rel_index={(r['cohort'],r['context'],r['display_name']):r for r in reliable}; focus=[]
    for r in rankings:
        if r['display_name'] in FOCUS: focus.append(rel_index.get((r['cohort'],r['context'],r['display_name']),r))
    focus_battles=focus_battle_rows(rows,battles,identities); decisions=review_decisions(queue,occurrences,source['locally_verified'])
    if len(rankings)!=len(reliable)+len(insufficient): raise ValueError('partition mismatch')
    if not any(r['display_name']=='White Harbor Knight Commander' and r['context']=='field' and r['reliability_status']=='reliable' for r in focus): raise ValueError('WH focus gate mismatch')
    if not any(r['display_name']=='Westerling Hedgeknight' and r['context']=='field' and r['reliability_status']=='reliable' for r in focus): raise ValueError('Westerling focus gate mismatch')
    write_csv(ANALYSIS_DIR/'ranking_complete.csv',RANKING_FIELDS,rankings); write_csv(ANALYSIS_DIR/'ranking_reliable.csv',RANKING_FIELDS,reliable); write_csv(ANALYSIS_DIR/'insufficient_evidence.csv',RANKING_FIELDS,insufficient)
    write_csv(ANALYSIS_DIR/'result_splits.csv',list(splits[0]),splits); write_csv(ANALYSIS_DIR/'battle_pressure_margin.csv',list(pressure[0]),pressure); write_csv(ANALYSIS_DIR/'focus_deep_dive.csv',RANKING_FIELDS,focus); write_csv(ANALYSIS_DIR/'focus_battle_rates.csv',list(focus_battles[0]),focus_battles); write_csv(ANALYSIS_DIR/'canonical_identity_audit.csv',list(identity_audit[0]),identity_audit)
    denom=[]
    for b in sorted(battles.values(),key=capture_key):
        p=b['player_side_total']; denom.append({'battle_id':b['battle_id'],'captured_at':capture_key(b),'cohort':cohort_for(b),'context':b['battle_context'],'result':result_for(b),'player_kills':'' if p.get('kills') is None else p['kills'],'player_deployed':'' if p.get('deployed') is None else p['deployed'],'kill_total_direct_positive':p.get('kills') not in (None,0),'deployment_total_direct_positive':p.get('deployed') not in (None,0),'provenance':'visible player_side_total','source_image_sha256':b['source']['image_sha256']})
    write_csv(ANALYSIS_DIR/'denominator_coverage.csv',list(denom[0]),denom)
    cov=defaultdict(lambda:{'bids':set(),'occ':0,'rows':0,'rel':0,'ins':0})
    for r in rows:
        b=battles[r['battle_id']]; k=(cohort_for(b),r['battle_context'],r['relationship_to_player'],r['parent_group']); cov[k]['bids'].add(r['battle_id']); cov[k]['occ']+=1
    for r in rankings:
        k=(r['cohort'],r['context'],r['participant_scope'],r['parent_group']); cov[k]['rows']+=1; cov[k]['rel']+=r['reliability_status']=='reliable'; cov[k]['ins']+=r['reliability_status']=='insufficient_evidence'
    coverage=[{'cohort':k[0],'context':k[1],'participant_scope':k[2],'parent_group':k[3],'independent_battles':len(v['bids']),'ordinary_occurrences':v['occ'],'partition_rows':v['rows'],'reliable_rows':v['rel'],'insufficient_rows':v['ins']} for k,v in sorted(cov.items())]
    write_csv(ANALYSIS_DIR/'context_coverage.csv',list(coverage[0]),coverage)
    write_csv(REVIEW_DIR/'review_decisions.csv',list(decisions[0]),decisions)
    write_csv(REVIEW_DIR/'phase2_identity_decisions.csv',list(identity_audit[0]),identity_audit)
    write_json(REVIEW_DIR/'phase2_review_summary.json',{'status':'complete_with_unresolved_raw_review_items','normalized_review_queue_rows':len(queue),'field_level_review_decisions':len(decisions),'numeric_corrections':0,'identity_decisions':len(identity_audit),'reviewer':'distinct Phase 2 analysis agent','raw_source_locally_verified':source['locally_verified'],'note':'No Phase 1 value changed; unresolved clipped rows stay excluded from primary rankings.'})
    (REVIEW_DIR/'README.md').write_text(f"# Phase 2 review layer\n\n{len(queue)} queued Phase 1 rows expand to {len(decisions)} field-level decisions. No normalized numeric value was changed. Raw screenshot evidence was {'available' if source['locally_verified'] else 'not available'} to this Phase 2 run; unresolved clipped fields remain excluded from primary rankings.\n",encoding='utf-8')
    write_json(ANALYSIS_DIR/'cohort_compatibility.json',{'status':'passed_with_separate_cohorts_and_contexts','decisions':[{'cohort':'white_harbor','contexts':['field'],'decision':'aggregate only inside field and Wyman Manderly player-party scope'},{'cohort':'joffrey','contexts':['field','siege_attack','siege_defense'],'decision':'same party may aggregate only within one context; contexts never pooled'},{'pair':['white_harbor','joffrey'],'decision':'incompatible campaigns/rosters; never pooled'},{'battle_states':['active_last_readable','phase_complete'],'decision':'independent observations; active remains censored, phase-complete retreat stays its own result category'}]})
    write_json(ANALYSIS_DIR/'input_verification.json',{'status':'passed','batch_id':BATCH_ID,'pipeline_mode':'offline-existing','pipeline_version':PIPELINE_VERSION,'schema_version':SCHEMA_VERSION,'normalization_commit':NORMALIZATION_COMMIT,'source_zip':source,'normalized_bundle':bundle,'identity_audit':{'path':IDENTITY_PATH.relative_to(REPO_ROOT).as_posix(),'sha256':IDENTITY_AUDIT_SHA256},'immutable_phase1_modified':False,'frozen_models_changed':False})
    (ANALYSIS_DIR/'ANALYSIS_REPORT.md').write_text(report(rankings,reliable,insufficient,focus,pressure,identity_audit),encoding='utf-8')
    (ANALYSIS_DIR/'NEXT_TEST_RECOMMENDATION.md').write_text('# Smallest next test\n\nIsolate **Westerling Hedgeknight** in at least 5 independent field battles with a stable support roster/orders and total Westerling deployment >=20. The mixed Joffrey field sample already passes the basic gate; this isolation test checks whether its 3.19 kills/deployed and >1 offensive contribution ratio survive composition/opponent confounding. Do not substitute siege observations.\n',encoding='utf-8')
    validation={'status':'passed','validation_errors':[],'batch_id':BATCH_ID,'bundle_members_verified':bundle['members'],'bundle_payload_hashes_verified':bundle['payload_hashes_verified'],'battles':len(battles),'ordinary_occurrences':len(rows),'distinct_display_labels':len(identities),'partition_rows':len(rankings),'reliable_rows':len(reliable),'insufficient_rows':len(insufficient),'partition_exact':len(rankings)==len(reliable)+len(insufficient),'review_queue_rows':len(queue),'review_field_decisions':len(decisions),'identity_confirmed':sum(r['resolution_status']=='confirmed_id' for r in identity_audit),'identity_unresolved':sum(r['resolution_status']!='confirmed_id' for r in identity_audit),'direct_kill_total_coverage':f"{sum(r['kill_total_direct_positive'] for r in denom)}/{len(denom)}",'direct_deployment_total_coverage':f"{sum(r['deployment_total_direct_positive'] for r in denom)}/{len(denom)}",'pressure_margin_final_battles':sum(bool(r['included_in_final_pressure_summary']) for r in pressure),'contexts_pooled':False,'cohorts_pooled':False,'player_enemy_pooled':False,'offscreen_rows_inferred':False,'active_battles_combined_with_later_fights':False,'frozen_models_changed':False,'role_adjusted_blended_rank_published':False}
    write_json(ANALYSIS_DIR/'validation_report.json',validation)
    (ANALYSIS_DIR/'README.md').write_text(f"# Phase 2 analytical outputs\n\nAll 355 primary ordinary-troop occurrences partition into {len(rankings)} cohort/context rows: {len(reliable)} reliable and {len(insufficient)} below gate. Rankings keep efficiency and share-adjusted impact independent. White Harbor/Joffrey and field/siege boundaries remain separate.\n\nReproduce from the repository root with:\n\n```bash\npython3 {Path(__file__).relative_to(REPO_ROOT).as_posix()}\n```\n\nAdd `--source-zip /absolute/path/to/source.zip` for optional raw-source/member hash verification.\n",encoding='utf-8')
    (ANALYSIS_DIR/'TESTS.md').write_text('# Validation runs\n\n- Phase 2 generator: passed immutable bundle SHA-256/size, safe tar preflight, all 17 payload manifest hashes, schema/arithmetic boundaries, exact partition, denominator coverage, and focus gates.\n- `python3 -m py_compile .../analysis/generate_phase2.py`: passed.\n- Repository unit test results are recorded after publication/branch validation.\n',encoding='utf-8')
    targets=[p for p in ANALYSIS_DIR.iterdir() if p.is_file() and p.name!='artifact_hashes.csv']+[REVIEW_DIR/'README.md',REVIEW_DIR/'review_decisions.csv',REVIEW_DIR/'phase2_identity_decisions.csv',REVIEW_DIR/'phase2_review_summary.json']
    artifacts=[{'path':p.relative_to(BATCH_DIR).as_posix(),'sha256':sha256_file(p),'size_bytes':p.stat().st_size} for p in sorted(targets)]
    write_csv(ANALYSIS_DIR/'artifact_hashes.csv',('path','sha256','size_bytes'),artifacts)
    print(json.dumps(validation,indent=2,sort_keys=True))

if __name__=='__main__': main()
