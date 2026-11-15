#!/usr/bin/env python3
"""Keep a date-stamped publication metadata snapshot from Europe PMC.

No model inference: this script never changes a protein's evidence classification.
Exact gene-symbol text matches are potential leads, not verified gene-specific papers.
"""
import argparse
import datetime as dt
import json
import pathlib
import time
from urllib.parse import urlencode
from urllib.request import Request,urlopen

ROOT=pathlib.Path(__file__).resolve().parents[1]
ENDPOINT='https://www.ebi.ac.uk/europepmc/webservices/rest/search'

def parse_item(record,gene,old,now):
    ident=(record.get('source') or 'MED')+':'+str(record.get('id') or record.get('pmid') or record.get('doi') or '')
    if not ident.split(':')[1]:return None
    link=('https://pubmed.ncbi.nlm.nih.gov/'+str(record['pmid'])+'/' if record.get('pmid')
          else 'https://doi.org/'+str(record['doi']) if record.get('doi')
          else 'https://europepmc.org/article/'+ident.replace(':','/',1))
    return {
      'key':ident, 'gene':gene,'title':record.get('title','Untitled'),
      'year':record.get('pubYear'),'date':record.get('firstPublicationDate',''),
      'journal':record.get('journalTitle',''), 'source':record.get('source',''),
      'pmid':record.get('pmid',''),'doi':record.get('doi',''),
      'url':link,
      'first_seen':old.get('first_seen',now)
    }

def fetch_gene(gene,count=8):
    # Symbol only: aliases can be entered in a reviewed query in targets.json.
    query='TITLE_ABS:"'+gene+'" sort_date:y'
    params=urlencode({'query':query,'resultType':'lite','pageSize':count,'format':'json'})
    request=Request(ENDPOINT+'?'+params,headers={'User-Agent':'TransporterAtlas/2.0 (public academic research)'} )
    with urlopen(request,timeout=22) as response:
        data=json.load(response)
    return data.get('resultList',{}).get('result',[]),data.get('hitCount',0)

def update(fetch=fetch_gene,now=None,sleep=0.1):
    now=now or dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    targets=json.loads((ROOT/'data/targets.json').read_text())['targets']
    path=ROOT/'data/literature.json'
    old=json.loads(path.read_text())
    old_by={(p.get('gene'),p.get('key')):p for p in old.get('papers',[])}
    per=old.get('per_target',{})
    new=[]; errors=[];checked=0
    for t in targets:
        g=t['gene']
        try:
            results,total=fetch(g)
            current=[]
            for p in results:
                key=(p.get('source') or 'MED')+':'+str(p.get('id') or p.get('pmid') or p.get('doi') or '')
                item=parse_item(p,g,old_by.get((g,key),{}),now[:10])
                if item: current.append(item)
            per[g]={'last_checked':now[:10],'hit_count':total,'items_indexed':len(current)}
            new.extend(current);checked+=1
        except Exception as e:
            errors.append({'gene':g,'error':str(e)[:200]})
            # On partial failure preserve the last successful results for that gene.
            new.extend([p for p in old.get('papers',[]) if p.get('gene')==g])
        time.sleep(sleep)
    if checked==0:raise RuntimeError('All literature lookups failed; preserving existing snapshot')
    # Stable dedupe across gene-symbol fetches.
    out={**old,'last_full_run':now if not errors else old.get('last_full_run'),
         'last_attempted_run':now,'per_target':per,'sync_failures':errors,
         'papers':sorted(new,key=lambda p:(p.get('gene',''),p.get('date') or '',p.get('title','')),reverse=True)}
    path.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'Checked {checked}/{len(targets)} targets; {len(out["papers"])} matched records; {len(errors)} failures')
    if errors:print('Partially updated: some sources could not be fetched',errors[:3])
    return out

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--no-sleep',action='store_true');args=a.parse_args()
    update(sleep=0 if args.no_sleep else 0.1)
