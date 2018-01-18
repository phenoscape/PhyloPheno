import json
from peyotl.api import APIWrapper

wrap = APIWrapper()
tm = wrap.taxomachine

unmaps = open('unmatched')

unmatched = {}
for lin in unmaps:
    lii = lin.split(',')
    if len(lii)==2:
        unmatched[lii[0]] = lii[1].strip()


multi_match = open("multi_matches.csv","w")
still_unmatched = open("still_unmatched.csv","w")

fuzzy_match = open("fuzzy_matches.csv","r")
fuzz = fuzzy_match.readlines()
for lin in fuzz:
    lii = lin.split(",")
    if lii[0] in unmatched.keys():
        del unmatched[lii[0]]


fuzzy_match.close()
fuzzy_match = open("fuzzy_matches.csv","a")
for VTO in unmatched.keys():
    taxname = unmatched[VTO]
    tnrs = tm.TNRS(taxname,"Animals",fuzzy_matching=True)
    if len(tnrs[u'results']) == 0:
            still_unmatched.write("{},{}\n".format(VTO, taxname))
    elif len(tnrs[u'results']) == 1:
            ott_id = tnrs[u'results'][0][u'matches'][0][u'taxon'][u'ott_id']
            fuzzy_match.write("{},{},{}\n".format(VTO, taxname,ott_id))
    elif len(tnrs[u'results']) > 1:
            multi_match.write("{},{}\n".format(VTO, taxname))
    else:
            still_unmatched.write("{},{}\n".format(VTO, taxname))


fuzzy_match.close()
multi_match.close()
still_unmatched.close()
