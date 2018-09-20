import re
import os

for filename in os.listdir('../../Result/1.start_stat/Gene'):
	if  re.search('Out_y',filename):
		continue
	name=re.split('\.',filename)
	name=name[0]+'_y.xls'
	f=open('../../Result/1.start_stat/Gene/'+filename,'r')
	sample=[]
	sample_gene={}
	while True:
		line=f.readline()
		line=line.strip()
		#if not line:break	
		ele=line.split('\t')
		for e in ele:
			sample.append(e)
		if True:break
		
	for e in sample:
		if e not in sample_gene:
			sample_gene[e]={}
		else:
			print 'This sample: '+e+" one sample -> two sample? wrong!"
	gene=[]
	while True:
		line=f.readline()
		line=line.strip()
		if not line:break
		ele=line.split('\t')
		count=1
		gene.append(ele[0])
		for s in sample:
			if ele[0] not in sample_gene[s]:
				sample_gene[s][ele[0]]=ele[count]
			count+=1
	#print gene
	#print sample
	#exit()
	o=open('../../Result/1.start_stat/Gene/Out_y/'+name,'w+')
	gs='\t'.join(gene)
	o.write('\t'+gs+'\n')
	for key1 in sample:
		o.write(key1)
		for g in gene:
			o.write('\t'+sample_gene[key1][g])
		o.write('\n')

		
	
