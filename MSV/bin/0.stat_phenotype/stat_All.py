# -*- coding:utf-8 -*-

#Author: liaoherui@mail.dlut.edu.cn

import re
import os
import sys
import getopt
import time
'''-----------获取参数----------'''
opts,args=getopt.getopt(sys.argv[1:],"hp:t:i:")
phenotype=''
ptype=''
info=''

for opt,arg in opts:
	if opt == "-h":
		print "eg: python "+os.path.basename(sys.argv[0])+" -p [phenotype] -i [info]"
	elif opt == "-p":
		phenotype=arg
	elif opt=="-t":
		ptype=arg
	elif opt=="-i":
		info=arg
		

if re.search('_',info):
	info=re.sub('_',' ',info)

'''---------自动创建输出目录--------'''

#pwd=os.getcwd()


outdir='../../Result/0.stat_phenotype' #输出目录默认为king.py主脚本所在路径自动创建的Result/0.stat_phenotype文件夹
n_dir='../../Result/0.stat_phenotype/File_by_'+ptype
if not (os.path.exists(n_dir)):
	os.makedirs(n_dir,0755)

'''---------------------开始统计-------------------'''

f=open(phenotype,'r')
r_out=open(outdir+'/Report_'+ptype+'.xls','w+')

biao_tou=''
count=0		#表型(比如国家)总数
p_hash={}	#这个哈希键为表型(比如国家)，值为样本数（通过Individuals ID统计的样本数）
p_ID_hash={}	#这是个二维哈希,这个哈希键第一层为表型(比如国家),第二层为Individuals ID，值为该样本所包含的所有行内容
def addtwodimdict(thedict, key_a, key_b, val):        #python没有直接可用的二维字典，所以要自己定义函数实现
                        if key_a in thedict:
                                thedict[key_a].update({key_b: val})
                        else:
                                thedict.update({key_a:{key_b: val}})

content_hash={} #这个哈希键为表型(如国家)，值为其对应行的内容
if re.search(',',info):
	info=re.split(',',info)
else:
	i=info
	info=[]
	info.append(i)
#print info
#exit()
while True:
	line=f.readline()
	if re.match('Individuals_ID',line):
		biao_tou=line
		pt=biao_tou.split('\t')
		num=pt.index(ptype)
		continue
	if not line: break
	line=line.strip()
	eles=line.split('\t')	
	if eles[num] not in info:continue
	eles[num]=re.sub(':','_',eles[num])
	eles[num]=re.sub(';','_',eles[num])
	eles[num]=re.sub('-','_',eles[num])
	eles[num]=re.sub(' ','_',eles[num])
	eles[num]=re.sub('/',r'\\',eles[num])
	#for 
	if eles[num] in p_ID_hash.keys() :
		if eles[0] not in p_ID_hash[eles[num]].keys():
			p_hash[eles[num]]+=1
			p_ID_hash[eles[num]][eles[0]]=line+'\n'
		else:
			p_ID_hash[eles[num]][eles[0]]+=line+'\n'
		#area_hash[eles[22]]+=1
		content_hash[eles[num]]+=line+'\n'
		
	else:
		p_hash[eles[num]]=1
		addtwodimdict(p_ID_hash,eles[num],eles[0],line+'\n')
		content_hash[eles[num]]=line+'\n'
		count+=1
#按国家生成文件
for key in content_hash.keys():
	out=open(outdir+'/File_by_'+ptype+'/'+key+'.xls','w+')
	out.write(biao_tou+content_hash[key])
#生成报告文件

r_out.write('#########Report#######'+'\n')
r_out.write('The total numbers of '+ptype+': '+str(count)+'\n')
r_out.write('The sample number of each '+ptype+': '+'\n')
total_num=0
for key in p_hash.keys():
		r_out.write(key+':	'+str(p_hash[key])+'\n')
		total_num+=p_hash[key]
r_out.write('The total numbers of sample is:	'+str(total_num))
f.close()


