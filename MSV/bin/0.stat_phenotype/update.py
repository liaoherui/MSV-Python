import os 
import re

f=open('Result.xls','r')
o=open('Result_new.xls','w+') #Rename this file to  Result.xls,then update is done

#hash for updating
ca={'ERP009131':'Canada'}			#No Country info,now update
twins={'ERP010700':'United Kindoms(twins)'}	#No Country info,now update
sweden={'ERP002469':'Sweden'}  #some from other countries ,but live in Sweden for a long time,so seem as Sweden
#ERP005989:some is baby _B,_4M_12M, for these samples,country info set as Denmark(baby)
area={}
disease={}
while True:
	count=1
	line=f.readline()
	line=line.strip()
	if not line:break
	ele=line.split('\t')
	es=[]
	for e in ele:
		e=e.strip()
		es.append(e)
	if es[3] in ca:
		es[22]=ca[es[3]]
	elif es[3] in twins:
		es[22]=twins[es[3]]
	elif es[3] in sweden:
		es[22]=sweden[es[3]]
	elif re.search('_12M',es[1]) or re.search('_4M',es[1]) or re.search('_B',es[1]):
		es[22]='Denmark(baby)'	
	for c in es:
		if count==1:
			o.write(c)
			count+=1
			continue
		o.write('\t'+c)
	o.write('\n')	
		
		
