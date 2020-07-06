""" $ python3 get_arxiv_metadata.py in_lang_cleaned_ids
"""

import arxiv
import json
import re
import sys
import time

# https://stackoverflow.com/a/312464
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

aids = []
with open(sys.argv[1]) as fi:
    for line in fi:
        aid = line.strip()
        m = re.search('\d', aid)
        if m and m.start() > 0:
            aid = '{}/{}'.format(aid[:m.start()], aid[m.start():])
        aids.append(aid)

chunks = list(chunks(aids, 100))
n_chunks = len(chunks)
papers = []
for i, chunk in enumerate(chunks):
    pprs = []
    print(f'{i}/{n_chunks}')
    pprs = arxiv.query(id_list=chunk)
    papers.extend(pprs)
    time.sleep(2)
with open('in_lang_cleaned_metadata.json', 'w') as fo:
    fo.write(json.dumps(papers))
