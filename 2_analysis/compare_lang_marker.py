""" Compare number of non-English titles and explicit "in (<Language)" markers
"""

import re
import sys

if len(sys.argv) != 4:
    print('Usage: python3 [...].py path/to/some.tsv <lang_code> <lang_marker>')
    sys.exit()
fn = sys.argv[1]
search_code = sys.argv[2]
search_marker = sys.argv[3]

lang_patt = re.compile(r'\(\s*in\s+([a-zA-Z][a-z]+)\s*\)')

num_as_is = 0
num_marker = 0
num_both = 0
with open(fn) as f:
    for line in f:
        lang_code, title, bibitem_string, uuid, cgaid, cdaid, cgmid, cdmid = line.split('\t')
        m = lang_patt.search(bibitem_string)
        if m:
            lang = m.group(1).lower()
            if lang in ['russion',
                         'russsian',
                         'rissian',
                         'russ',
                         'rusian',
                         'russain',
                         'rus',
                         'russan',
                         'russin',
                         'rusia',
                         'russina',
                         'rassian',
                         'russe',
                         'russisan',
                         'ruassian']:
                lang = 'russian'
            elif lang in ['japanase',
                          'japanse',
                          'japaneese',
                          'japanes',
                          'japansese',
                          'japnese']:
                lang = 'japanese'
            elif lang in ['chines',
                          'chinses',
                          'chineses']:
                lang = 'chinese'
            elif lang == 'roumanian':
                lang = 'romanian'
            elif lang == 'hugarian':
                lang = 'hungarian'
            elif lang == 'franch':
                lang = 'french'
            elif lang == 'ukrainain':
                lang = 'ukranian'
            elif lang == 'protuguese':
                lang = 'portuguese'
        else:
            lang = None

        if lang_code == search_code:
            num_as_is += 1
        if lang == search_marker:
            num_marker += 1
        if lang_code == search_code and lang == search_marker:
            num_both += 1

print(f'As is: {num_as_is}')
print(f'Explicit marker: {num_marker}')
print(f'Both: {num_both}')
