#!/usr/bin/env python3
"""Apply compact P1 review decisions to a P0-reviewed troop JSONL."""
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path
FIELDS=("survivors","kills","upgrade_ready","deaths","wounded","routed")
def optint(v:str|None)->int|None:return None if v in (None,"") else int(v)
def fingerprint(row:dict[str,object])->str:
    payload=[row.get("analysis_status"),*[row.get(f) for f in FIELDS]]
    return hashlib.sha256(json.dumps(payload,separators=(",",":")).encode()).hexdigest()
def main()->None:
    p=argparse.ArgumentParser();p.add_argument("input",type=Path);p.add_argument("decisions",type=Path);p.add_argument("output",type=Path);a=p.parse_args()
    with a.decisions.open(encoding="utf-8",newline="") as h: decisions={r["observation_id"]:r for r in csv.DictReader(h)}
    seen=set();counts={"corrected":0,"confirmed":0,"excluded":0};output=[]
    with a.input.open(encoding="utf-8") as h:
      for line_no,line in enumerate(h,1):
        if not line.strip():continue
        try:row=json.loads(line)
        except json.JSONDecodeError as e:raise ValueError(f"Invalid JSON on {a.input}:{line_no}: {e}") from e
        oid=str(row.get("observation_id"));d=decisions.get(oid)
        if d:
          seen.add(oid);status=d["review_status"];counts[status]+=1
          actual=fingerprint(row)
          if actual!=d["source_fingerprint_sha256"]:raise ValueError(f"{oid}: source fingerprint mismatch {actual}")
          before={f:row.get(f) for f in FIELDS}
          if status=="excluded":
            row.update(analysis_status="excluded",exclusion_reason=d["exclusion_reason"],needs_review=False,review_status="excluded")
          elif status in {"corrected","confirmed"}:
            for f in FIELDS:
              v=optint(d[f"reviewed_{f}"])
              if v is not None:row[f]=v
            row["deployed"]=int(row["survivors"])+int(row["deaths"])+int(row["wounded"])
            row["kills_per_deployed"]=round(int(row["kills"])/int(row["deployed"]),6) if row["deployed"] else None
            row["routed_rate"]=round(int(row["routed"])/int(row["deployed"]),6) if row["deployed"] else None
            extraction=row.setdefault("field_extraction",{})
            for f in FIELDS:extraction.setdefault(f,{}).update(confidence=1.0,source="manual_visual_review",uncertain=False,reviewed_value=row[f])
            row.update(needs_review=False,review_status="reviewed")
          else:raise ValueError(f"{oid}: unsupported status {status}")
          row.setdefault("review_history",[]).append({"reviewed_at":"2026-07-26","reviewer":"OpenAI GPT-5.6 Thinking with user-authorized repository workflow","review_source":"manual_visual_review_exact_hash_source_screenshot","review_status":status,"changed_fields":[x for x in d["changed_fields"].split(";") if x],"before":before,"after":{f:row.get(f) for f in FIELDS}})
        output.append(row)
    missing=set(decisions)-seen
    if missing:raise ValueError(f"Decisions not found: {sorted(missing)}")
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open("w",encoding="utf-8") as h:
      for row in output:h.write(json.dumps(row,ensure_ascii=False,sort_keys=True)+"\n")
    print(json.dumps({"input_rows":len(output),"decisions_applied":len(seen),"counts":counts,"remaining_needs_review":sum(bool(r.get("needs_review")) for r in output)},indent=2))
if __name__=="__main__":main()
