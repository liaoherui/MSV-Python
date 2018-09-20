import os
import re
import sys
import getopt
from  numpy import *
'''----------Get Option------------'''
opts,args=getopt.getopt(sys.argv[1:],"ht:p:")
t_file=''  #the out_y dir of  setp1
p_file=''  #the phenotype of all

for opt,arg in opts:
	if opt=='-h':
		print 'eg: python '+os.path.basename(sys.argv[0])+' -t [trouble profile] -p [pp_profile]'
	elif opt=='-t':
		t_file=arg
	elif opt=='-p':
		p_file=arg



'''--------Start-------'''


#hash_1: key->sampleName | value->value matrix
hash_1={}

f=open(t_file,'r')
while True:
	line=f.readline()
	if not line:break
	#if not re.search('^P',line):continue
	if re.search('^\t',line):continue
	line=line.strip()
	ele=line.split('\t')
	samp=ele[0]
	ele=ele[1:]
	num=[]
	for e in ele:
		num.append(float(e))
	value=mat(num)
	hash_1[samp]=value
	

#hash_2: key1->Individual ID|  key2->Sample Name |value->value matrix
hash_2={}
f2=open(p_file,'r')
while True:
	line=f2.readline()
	if not line:break
	line=line.strip()
	if re.search('^Individuals',line):continue
	ele=line.split('\t')
	if ele[0] not in hash_2:
		if ele[1] in hash_1:
			hash_2.update({ele[0]:{ele[1]:hash_1[ele[1]]}})
		else:
			print ele[1]+'  is not in ERP009131_result_y.xls!'
	else:
		if ele[1] in hash_1:
			hash_2[ele[0]].update({ele[1]:hash_1[ele[1]]})
		else:
			print ele[1]+'  is not in ERP009131_result_y.xls!'
		
#out
#o=open('ERP009131_result_y_new.xls','w+')
fl=''
f3=open(t_file,'r')
while True:
	line=f3.readline()
	fl=line
	if True:break
o=open(t_file,'w+')
o.write(fl)
#mean=[]
#mean=mat(mean)

for key1 in hash_2:
	mean=[]
	mean=mat(mean)
	count=0
	for key2 in hash_2[key1]:
		if any(mean):
			mean+=hash_2[key1][key2]
		else:
			mean=hash_2[key1][key2]
		count+=1
	mean=mean/float(count)
	mean=array(mean)
	o.write(key1)
	for i in mean[0]:
		o.write('\t'+str(i))
	o.write('\n')	
		

	
	
	
			
		




