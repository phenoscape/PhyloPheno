#!/usr/bin/env python

#script to rewrite VTO_to_OTT.csv to rdf

#Demo text from Jim Balhoff
'''<http://purl.obolibrary.org/obo/VTO_0000001> <http://www.geneontology.org/formats/oboInOwl#hasDbXref> <http://opentree.org/12345> .
_:1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Axiom> .
_:1 <http://www.w3.org/2002/07/owl#annotatedSource> <http://purl.obolibrary.org/obo/VTO_0000001> .
_:1 <http://www.w3.org/2002/07/owl#annotatedProperty> <http://www.geneontology.org/formats/oboInOwl#hasDbXref> .
_:1 <http://www.w3.org/2002/07/owl#annotatedTarget> <http://opentree.org12234> .
_:1 <http://purl.org/dc/terms/description> "exact label match" .'''

rdfout = open("VTO_to_OTT.rdf","w")

ncbi = "matched based on VTO ncbi ID to OpenTreeTaxonomy OTTv3"
exact = "exact string match of VTO name to OpenTreeTaxonomy OTTV3 name or synonyms"
fuzzy = "fuzzy match of VTO name to OpenTreeTaxonomy OTTV3 name or synonyms"

string_stub = '''<http://purl.obolibrary.org/obo/{vtoid}> <http://www.geneontology.org/formats/oboInOwl#hasDbXref> <https://tree.opentreeoflife.org/taxonomy/browse?id={ottid}> .
_:{i} <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Axiom> .
_:{i} <http://www.w3.org/2002/07/owl#annotatedSource> <http://purl.obolibrary.org/obo/{vtoid}> .
_:{i} <http://www.w3.org/2002/07/owl#annotatedProperty> <http://www.geneontology.org/formats/oboInOwl#hasDbXref> .
_:{i} <http://www.w3.org/2002/07/owl#annotatedTarget> https://tree.opentreeoflife.org/taxonomy/browse?id={ottid}> .
_:{i} <http://purl.org/dc/terms/description> "{match_type}" .\n'''


infi = open('VTO_to_OTT.csv','r') #Output the map from VTO to ott_id

infi.readline()

i = 0
for lin in infi:
    lii=lin.strip().split("\t")
    if lii[4]=='NA':
        pass
    else:
    	i+=1
        VTO = lii[1]
        OTT = lii[4]
        if lii[2] == 'NA':
        	match_type = exact
        else:
        	assert(int(lii[2]))
        	match_type = ncbi
        rdfout.write(string_stub.format(vtoid=VTO,ottid=OTT,match_type=match_type,i=i))

