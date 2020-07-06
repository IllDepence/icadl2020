""" More or less a copy of get_authors_inMAG_subset.py
"""

import sys
from sqlalchemy import create_engine

mag_db_uri = 'postgresql+psycopg2://xxx:YYYYY@localhost:5432/MAG19'
mag_engine = create_engine(mag_db_uri)

with open(sys.argv[1]) as f:
    with open('inMAG_author_IDs.tsv', 'w') as fo:
        for line in f:
            in_lang, uuid, g_mid, d_mid, g_aid, d_aid, bstr = line.split('\t')
            if len(in_lang) > 0 and len(d_mid) > 0 and len(g_mid) > 0:
                    citing_authors = mag_engine.execute((
                        f'select authorid, displayname, normalizedname from authors where authorid in '
                        f'(select authorid from paperauthoraffiliations where paperid = {g_mid});'
                        )).fetchall()
                    cited_authors = mag_engine.execute((
                        f'select authorid, displayname, normalizedname from authors where authorid in '
                        f'(select authorid from paperauthoraffiliations where paperid = {d_mid});'
                        )).fetchall()
                    # ID overlap
                    g_auth_ids = set([ca[0] for ca in citing_authors])
                    d_auth_ids = set([ca[0] for ca in cited_authors])
                    author_overlap = len(g_auth_ids.intersection(d_auth_ids))
                    if author_overlap == 0:
                        # possible name overlap
                        g_auth_tokens = set()
                        d_auth_tokens = set()
                        for ga in citing_authors:
                            g_auth_tokens = g_auth_tokens.union([t for t in ga[2].split(' ') if len(t) > 1 and t[-1] != '.'])
                        for da in cited_authors:
                            d_auth_tokens = d_auth_tokens.union([t for t in da[2].split(' ') if len(t) > 1 and t[-1] != '.'])
                        if len(g_auth_tokens.intersection(d_auth_tokens)) > 0:
                            author_overlap = 'x'
                    # human readable author lists
                    if citing_authors == None:
                        g_auth_list = []
                    else:
                        g_auth_list = [ca[0] for ca in citing_authors]
                    if cited_authors == None:
                        d_auth_list = []
                    else:
                        d_auth_list = [ca[0] for ca in cited_authors]
                    auth_list = g_auth_list + d_auth_list
                    auth_list = list(set(auth_list))
                    for author in auth_list:
                        fo.write(f'{author}\n')
