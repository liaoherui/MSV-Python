# -*- coding:utf-8 -*-

#Author: liaoherui@mail.dlut.edu.cn

import re
import os
import sys
import getopt

opts,args=getopt.getopt(sys.argv[1:],"t:")
ptype=''
for opt,arg in opts:
	if opt=="-t":
		ptype=arg


path='../../Result/0.stat_phenotype/File_by_'+ptype

if not os.path.exists('../../Result/0.stat_phenotype/Report_by_'+ptype):
	os.makedirs('../../Result/0.stat_phenotype/Report_by_'+ptype,0755)

#迭代操作目录下的文件，然后迭代生成相应的报告文件
for filename in os.listdir(path):
	if re.match('Report',filename): continue
	if re.search('report',filename): continue
	f=open('../../Result/0.stat_phenotype/File_by_'+ptype+'/'+filename,'r')
	country=re.split('xls',filename)
	country[0]=re.sub('\.','',country[0])
	o=open('../../Result/0.stat_phenotype/Report_by_'+ptype+'/'+country[0]+'_report.xls','w+')
	gender_count=0 #即总样本数
	age_count=0
	gender_hash={}
	age_hash={}
	age_hash['0-4']=0
	age_hash['4-10']=0
	age_hash['10-18']=0
	age_hash['18-50']=0
	age_hash['>50']=0
	age_hash['NA']=0
	def addtwodimdict(thedict, key_a, key_b, val):        #python没有直接可用的二维字典，所以要自己定义函数实现
                        if key_a in thedict:
                                thedict[key_a].update({key_b: val})
                        else:
                                thedict.update({key_a:{key_b: val}})
	gender_ID_hash={}
	age_ID_hash={}
	print country[0]+' starts......'	
	while True:
		line=f.readline().strip()
		if not line: break
		ele=line.split('\t')
		if re.match('Individuals_ID',line):
			continue
		#remove () of age
		if re.search('\(',ele[26]):
			ele[26]=re.sub('\(.*','',ele[26])			
		#print ele[26]
		ele[25]=ele[25].strip()
		ele[26]=ele[26].strip()	
		#About gender
		ele[0]=ele[0].strip()
		if ele[0]=='':
			continue
		if ele[0]  in gender_ID_hash.keys():
				#gender_ID_hash[ele[0]][ele[25]]+=line+'\n'
				#print 'yes'
				continue
		else:
			if ele[25] not in gender_hash.keys():
				gender_hash[ele[25]]=1
			else:
				gender_hash[ele[25]]+=1
			addtwodimdict(gender_ID_hash,ele[0],ele[25],line+'\n')
			gender_count+=1
		#About age
		if ele[0] in age_ID_hash.keys():
			'''
			if ele[26] not in age_ID_hash[ele[0]].keys():
				age_ID_hash[ele[0]][ele[26]]=line+'\n'
				if re.match('NA',ele[26]):
					age_hash['NA']+=1
                        		age_count+=1
                		elif  float(ele[26])<=4:
                        		age_hash['0-4']+=1
                        		age_count+=1
                		elif float(ele[26])>4 and float(ele[26])<=10:
                        		age_hash['4-10']+=1
                       	 		age_count+=1
                		elif float(ele[26])>10 and float(ele[26])<=18:
                        		age_hash['10-18']+=1
                        		age_count+=1
				elif float(ele[26])>18 and float(ele[26])<=50:
					age_hash['18-50']+=1
					age_count+=1
                		else:
                        		age_hash['>50']+=1
                        		age_count+=1
			else:
				#age_ID_hash[ele[26]][ele[0]]+=line+'\n'
				continue
			'''
			continue
		else:
				if re.match('NA',ele[26]):
                                        age_hash['NA']+=1
                                        age_count+=1
                                elif float(ele[26])<=4:
					age_hash['0-4']+=1
                                        age_count+=1
                                elif float(ele[26])>4 and float(ele[26])<=10:
                                        age_hash['4-10']+=1
                                        age_count+=1
                                elif float(ele[26])>10 and float(ele[26])<=18:
                                        age_hash['10-18']+=1
                                        age_count+=1
                                elif float(ele[26])>18 and float(ele[26])<=50:
                                        age_hash['18-50']+=1
                                        age_count+=1
                                else:
                                        age_hash['>50']+=1
                                        age_count+=1
				addtwodimdict(age_ID_hash,ele[0],ele[26],line+'\n')
	
	
	o.write('The total sample numbers of this '+ptype+'  are: '+str(gender_count)+'\n')
	o.write('####About Gender####'+'\n')
	for key in gender_hash.keys():
		o.write(key+' :'+str(gender_hash[key])+'\n')
	o.write('Total numbers of gender: '+str(gender_count)+'\n')
	o.write('#####About Age#####'+'\n')
	for key in age_hash.keys():
		o.write(key+' :'+str(age_hash[key])+'\n')
	o.write('Total numbers of age: '+str(age_count)+'\n')
	print country[0]+' over!'	
	
		
		
	
