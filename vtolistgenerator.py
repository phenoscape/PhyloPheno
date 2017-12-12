__author__ = 'pasanfernando'
## the scripts builds VTO network and gives a list of all the families in it
# 7/14/16: the script was updated to generate a list of all taxa that are descendents of teleostei (including teleostei)
import re
import networkx as nx
import matplotlib.pyplot as plt
import os

# u = raw_input('Enter vto data file: ')

p = open('vto.owl', 'r')
out = open('vtoallfamilies.txt', 'wb+')

G = nx.DiGraph()
name = {}
namer ={}
taxarank ={}

# The dictiorary to store VTO id as the key and NCBI id as the value
vtncbi = {}
# building the vto network
for line in p:
    # print line
    if '<!-- http://purl.obolibrary.org/obo/' in line:
        result = re.search('<!-- http://purl.obolibrary.org/obo/(.*)-->', line)
        x = result.group(1)
        x1 = x.strip()
        # print x1
        if G.has_node(x1) == False:
            G.add_node(x1)

    if '<rdfs:label rdf:datatype="http://www.w3.org/2001/XMLSchema#string">' in line:
        name1 = re.search('<rdfs:label rdf:datatype="http://www.w3.org/2001/XMLSchema#string">(.*)</rdfs:label>', line)
        n = name1.group(1)
        # print n
        name[n] = x1
        namer[x1] = n
    #
    if '<rdfs:subClassOf rdf:resource="http://purl.obolibrary.org/obo/' in line:
        s = re.search('<rdfs:subClassOf rdf:resource="http://purl.obolibrary.org/obo/(.*)"/>', line)
        k = s.group(1)

        G.add_edge(k, x1)

    if '<vto:has_rank rdf:resource="http://purl.obolibrary.org/obo' in line:
        name1 = re.search('<vto:has_rank rdf:resource="http://purl.obolibrary.org/obo/TAXRANK_(.*)"/>', line)
        rank = name1.group(1)
        # print n
        taxarank[n]= rank

    if '<oboInOwl:hasDbXref rdf:datatype="http://www.w3.org/2001/XMLSchema#string">NCBITaxon:' in line:
        s = re.search('<oboInOwl:hasDbXref rdf:datatype="http://www.w3.org/2001/XMLSchema#string">NCBITaxon:(.*)<',
                      line)
        nc = s.group(1)
        ## there are synonyms for some taxa and they have ncbi id's as well so only the first ocurrance is stored
        if n not in vtncbi:
            vtncbi[x1] = nc

#print vtncbi


#generating a list of nodes for the network
nd = nx.nodes(G)
# print nd

# for ln in nd:
#     print namer[ln]
#print taxarank

print name['Siluriformes']
##extracting all the descendents for teleostei
td =list(nx.descendants(G,name['Siluriformes']))
print 'total taxa in vto',len(td)
print 'Number of taxa with ncbi ids:',len(vtncbi)

########################## open tree data file processing########################################################################

otncbi ={}
otncbir={}
oid ={}

# opening the taxonomy file downloaded from opentree; this contains references to NCBI ids
d = open('taxonomy.tsv', 'r')


for line in d:
    a = line.split('|')

    # extracting open tree id and name
    otid = a[0].strip()
    otname = a[2].strip()
    otname = otname.replace('_', ' ')

    #storing all ids: name as the key and open tree id as the value
    oid[otname]=otid

    # extracting the NCBI ids, by stripping unwanted segments
    a1 = a[4].strip()

    if 'ncbi:' in a1:
        if ',' in a1:
            b = a1.split(',')
            for i in b:
                if 'ncbi' in i:
                    x = i

        else:
            x = a1
        #print '     ',x
        x=x.strip('ncbi:')

        # storing ncbi ids: name as key ncbi ID as value
        otncbi[otname]=x
        #reversed assignment: key is ncbi id , value is name
        otncbir[x]=otname

out1 = open('vtoalltaxa.txt', 'wb+')
out1.write('vto_name\tvto_id\tncbi_id\tOT_name\tOt_ID\n')

# list for taxa with ncbi ids
taxawithncbi =[]

# list for taxa with ncbi ids
taxawithoutncbi =[]

#open tree taxa without ncbi ids
ottaxawithoutncbi=[]


## prints teleostei in the output, change this according to interested taxa
#out1.write('Teleostei\n')
for i in td:
    #print i
    x = namer[i]
    x1 = x.strip()
    # if the vto has an ncbi id
    if i in vtncbi:
        taxawithncbi.append(i)
        ncbiid = vtncbi[i]
        if ncbiid in otncbir:
            otname1 = otncbir[ncbiid]
            out1.write('%s\t%s\t%s\t%s\t%s\n'%(x1,i,ncbiid,otname1,oid[otname1]))

        else:
            ottaxawithoutncbi.append(x1)
            out1.write('%s\t%s\t%s\tNA\tNA\n' % (x1, i, vtncbi[i]))


    else:
        out1.write('%s\t%s\tNA\tNA\tNA\n' % (x1, i))

        taxawithoutncbi.append(x1)
out1.close()

print 'Number of taxa with NCBI ids:',len(taxawithncbi)
print 'Number of taxa withou NCBI ids:',len(taxawithoutncbi)
print 'Number of OT taxa without maching NCBI ids:',len(ottaxawithoutncbi)
print ottaxawithoutncbi

# file to save VTO taxa without NCBI ids
wncbi = open('VTO_taxa_without_ncbiids.txt','wb+')
wncbi.write('VTO_name\tVTO_id\n')

for i in taxawithoutncbi:
    wncbi.write('%s\t%s\n' % (i, name[i]))

wncbi.write('\n')
wncbi.write('The VTO taxa that has NCBI ids but are not found in OPenTree data file\n')
wncbi.write('VTO_name\tVTO_id\tncbi_id\n')
for i in ottaxawithoutncbi:
    print i
    wncbi.write('%s\t%s\t%s\n' % (i, name[i], vtncbi[name[i]]))

wncbi.close()



