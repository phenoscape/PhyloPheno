#!/usr/bin/env python

from peyotl.api import APIWrapper


infi = open("VTO_taxa_without_ncbiids.txt")


ofi = open('alltaxa_VTO_mapping.txt','w')
ofi.write("{},{},{}\n".format('VTO','taxname','ottid'))

mmfi = open('multi_matched','w')
mmfi.write("{},{}\n".format('VTO','taxname'))

unfi = open('unmatched','w')
unfi.write("{},{}\n".format('VTO','taxname'))

wrap = APIWrapper()
tm = wrap.taxomachine

for lin in infi:
    lii=lin.split("\t")
    taxname=lii[0]
    VTO=lii[1]
    tnrs = tm.TNRS(taxname, "Animals")
    if len(tnrs[u'results']) == 0:
        unfi.write("{},{}\n".format(VTO, taxname))
    if len(tnrs[u'results']) == 1:
        ott_id = tnrs[u'results'][0][u'matches'][0][u'taxon'][u'ott_id']
        ofi.write("{},{},{}\n".format(VTO,taxname,ott_id))
    if len(tnrs[u'results']) > 1:
        mmfi.write("{},{}\n".format(VTO, taxname))


ofi.close()
mmfi.close()
unfi.close()




