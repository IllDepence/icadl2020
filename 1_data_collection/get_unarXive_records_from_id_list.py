""" Extract db entries
"""

import re
import sys
from sqlalchemy import create_engine

if len(sys.argv) != 4:
    print('Usage: python3 [...].py path/to/id_list path/to/in_lang_tsv path/to/refs.db')
    sys.exit()
id_file = sys.argv[1]
tsv_file = sys.argv[2]
db_path = sys.argv[3]

ids = list()
with open(id_file) as f:
    ids = [l.strip() for l in f.readlines()]

in_lang_dict = dict()
with open(tsv_file) as f:
    for line in f:
        lang, text, aid, uuid = line.strip().split('\t')
        in_lang_dict[uuid] = lang

db_uri = 'sqlite:///{}'.format(db_path)
db_engine = create_engine(db_uri)

results = db_engine.execute('select uuid, citing_mag_id, cited_mag_id, citing_arxiv_id, cited_arxiv_id, bibitem_string from bibitem;')

with open('XXX_docs_all_bibitems.tsv', 'w') as f:
    for i, row in enumerate(results):
        if i%10000 == 0:
            print(i)
        aid = row[3]
        if aid in ids:
            uuid = row[0]
            if uuid in in_lang_dict:
                in_lang = in_lang_dict[uuid]
            else:
                in_lang = ''
            row = ['' if v is None else v for v in row]
            line = '\t'.join(row)
            f.write(f'{in_lang}\t{line}\n')
