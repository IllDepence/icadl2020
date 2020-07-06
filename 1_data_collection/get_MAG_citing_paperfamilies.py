import datetime
import json
import requests
import sys
import time

keys_tups = [
    ['FamId', 'fam_id'],
    ['Id', 'mag_id'],
    ['D', 'published'],
    ['BT', 'bibtype'],
    ['BV', 'bibvenue'],
    ['CC', 'citcount'],
    ['DOI', 'doi'],
    ['F', 'fos'],
    ['J', 'journal'],
    ['PB', 'publisher'],
    ['Pt', 'pub_type'],
    ['S', 'sources'],
    ['AA', 'authors'],
    ['RId', 'refs']
    ]
def process_ppr_entity(e):
    ppr = dict()
    for kt in keys_tups:
        ms_key = kt[0]
        new_key = kt[1]
        ppr[new_key] = None
        if ms_key in e:
            ppr[new_key] = e[ms_key]
    return ppr

g_mids = set()
with open(sys.argv[1]) as fi:
    for line in fi:
        in_lang, uuid, g_mid, d_mid, g_aid, d_aid, bstr = line.split('\t')
        # if len(in_lang) > 0:  # used for in-lang-set, not used for control sample
        if len(g_mid) > 0:
            g_mids.add(g_mid)

headers = {'Ocp-Apim-Subscription-Key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'}
base_url = 'https://api.labs.cognitive.microsoft.com/academic/v1.0/evaluate?expr='
attribs = '&attributes=FamId,Id,D,BT,BV,CC,DOI,F.FId,F.FN,J.JId,J.JN,PB,Pt,S,AA.AuId'

disappeard_mids = []
retrieved_pprs = []

for i, mid in enumerate(g_mids):
    url = f'{base_url}Id={mid}{attribs}'
    resp = requests.get(
        url,
        headers=headers,
        timeout=60
        )
    jresp = resp.json()
    if len(jresp['entities']) == 0:
        disappeard_mids.append(mid)
    else:
        ppr = jresp['entities'][0]
        if 'FamId' not in ppr:
            # save this single one
            retrieved_pprs.append(process_ppr_entity(ppr))
        else:
            time.sleep(0.3)
            fam_id = ppr['FamId']
            furl = f'{base_url}FamId={fam_id}{attribs}'
            fresp = requests.get(
                furl,
                headers=headers,
                timeout=60
                )
            jfresp = fresp.json()
            for fppr in jfresp['entities']:
                # save them all
                retrieved_pprs.append(process_ppr_entity(fppr))
    time.sleep(0.3)
    if i%1000 == 1:
        print(i)
        timestamp = str(int(datetime.datetime.timestamp(datetime.datetime.now())))
        fn = f'MAG_citing_families_extended_metadata_{timestamp}.json'
        with open(fn, 'w') as fo:
            fo.write(json.dumps(retrieved_pprs))
        with open(f'disappeard_citing_mids_{timestamp}', 'w') as fo:
            for dm in disappeard_mids:
                fo.write(f'{dm}\n')

with open('control_sample_MAG_citing_families_extended_metadata.json', 'w') as fo:
    fo.write(json.dumps(retrieved_pprs))
with open('control_sample_disappeard_citing_mids', 'w') as fo:
    for dm in disappeard_mids:
        fo.write(f'{dm}\n')
