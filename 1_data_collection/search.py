""" Search for "in (<Language)" in unarXive
    "bibitems" (reference section entries)

    $ python3 search.py unarXive/papers/refs.db
"""

import re
import sys
from sqlalchemy import create_engine

if len(sys.argv) != 2:
    print('Usage: python3 search.py path/to/refs.db')
    sys.exit()
db_path = sys.argv[1]

lang_patt = re.compile(r'\(\s*in\s+[a-zA-Z][a-z]+\s*\)')

db_uri = 'sqlite:///{}'.format(db_path)
db_engine = create_engine(db_uri)

results = db_engine.execute('select bibitem_string, citing_arxiv_id, uuid from bibitem;')

with open('in_lang.tsv', 'w') as f:
    for i, row in enumerate(results):
        if i%10000 == 0:
            print(i)
        if lang_patt.search(row[0]):
            line = '\t'.join(row)
            f.write(f'{line}\n')
