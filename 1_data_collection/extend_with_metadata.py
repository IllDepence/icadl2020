""" Extend in_lang.tsv with arXiv metadata

    $ python3 extend_with_metadata.py in_lang_cleaned.tsv in_lang_cleaned_metadata.json
"""

import json
import re
import sys

tsv = sys.argv[1]
md_json = sys.argv[2]

with open(md_json) as f:
    md = json.load(f)
print('metadata loaded')

md_dict = {}
vers_patt = re.compile(r'v\d+$')
ws_patt = re.compile(r'\s+')
for ppr in md:
    url = ppr['id']  # e.g. "http://arxiv.org/abs/1103.2678v1"
    raw_id = url.split('/abs/')[-1]
    aid = vers_patt.sub('', raw_id).replace('/', '')
    category = ppr['arxiv_primary_category']['term']
    if ppr['journal_reference']:
        journal_ref = ws_patt.sub(' ', ppr['journal_reference'])
    else:
        journal_ref = ''
    published = ppr['published']
    md_dict[aid] = {
        'published': published,
        'category': category,
        'journal_ref': journal_ref
        }
print('metadata extracted')

with open(tsv) as fi:
    with open('in_lang_cleaned_extended.tsv', 'w') as fo:
        for line in fi:
            lang, bstr, aid, uuid = line.split('\t')
            uuid = uuid.strip()
            new_meta = md_dict[aid]
            new_line = '\t'.join([
                uuid,
                lang,
                aid,
                new_meta['published'],
                new_meta['category'],
                new_meta['journal_ref'],
                bstr
                ])
            fo.write(f'{new_line}\n')
