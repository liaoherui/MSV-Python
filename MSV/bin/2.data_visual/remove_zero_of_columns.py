import pandas as pd
import re
import os
import sys
import getopt
import numpy as np
import math
'''----------Get Option--------'''
opts,args=getopt.getopt(sys.argv[1:],"he:")
level=''
for opt,arg in opts:
	if opt=='-h':
		print 'eg: python '+os.path.basename(sys.argv[0])+' -e [level]'
	if opt=='-e':
		level=arg

if level=='ge':
	path='../../Result/2.data_visual/Gene/step1'
if level=='ta':
	path_g='../../Result/2.data_visual/Taxo/genus/step1'
	path_p='../../Result/2.data_visual/Taxo/phylum/step1'
	path_s='../../Result/2.data_visual/Taxo/species/step1'
	path_ta=[]
	path_ta.append(path_g)
	path_ta.append(path_p)
	path_ta.append(path_s)
if level=='ko':
	path='../../Result/2.data_visual/KO/step1'
#f=pd.read_table('ID_71_visual.xls',sep='\t')
'''--------Make Output dir-------'''
outdir='../../Result/2.data_visual'
end_dir=''
if level=='ge':
	end_dir=outdir+'/Gene/step2'
	if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)
if level=='ta':
	end_dir1=outdir+'/Taxo/genus/step2'
	end_dir2=outdir+'/Taxo/phylum/step2'
	end_dir3=outdir+'/Taxo/species/step2'
	if not (os.path.exists(end_dir1)):
                os.makedirs(end_dir1,0755)
	if not (os.path.exists(end_dir2)):
                os.makedirs(end_dir2,0755)
	if not (os.path.exists(end_dir3)):
                os.makedirs(end_dir3,0755)

if level=='ko':
	end_dir=outdir+'/KO/step2'
	if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)

'''--------Start-------'''
if level=='ge' or level=='ko':
	for filename in os.listdir(path):
		f=pd.read_table(path+'/'+filename,sep='\t')
		f2=open(path+'/'+filename,'r')
		arr=re.split('\.',filename)
		prefix=arr[0]
		while True: 
			line=f2.readline().strip()
			ele=line.split('\t')
			ele=ele[1:]
			if True: break
		for area in ele:
			count=0
			real_count=0
			for i in f[area]:
				real_count+=1
				if i!=0.0 and i!=0.1:
					count+=1
			if count==0:
				del f[area]	
		if level=='ge':
			prefix=re.sub('\|','_',prefix)
		f.to_csv(end_dir+'/'+prefix+'_final.xls',index=False,sep='\t')
if level=='ta':
	for path in path_ta:
		for filename in os.listdir(path):
                	f=pd.read_table(path+'/'+filename,sep='\t')
	                f2=open(path+'/'+filename,'r')
        	        arr=re.split('\.',filename)
	                prefix=arr[0]
        	        while True:
                	        line=f2.readline().strip()
	                        ele=line.split('\t')
	                        ele=ele[1:]
	                        if True: break
	                for area in ele:
	                        count=0
	                        real_count=0
	                        for i in f[area]:
	                                real_count+=1
	                                if i!=0.0 and i!=0.1:
	                                        count+=1
	                        if count==0:
	                                del f[area] 
			if re.search('genus',path):
		                f.to_csv(end_dir1+'/'+prefix+'_final.xls',index=False,sep='\t')
			if re.search('phylum',path):
				f.to_csv(end_dir2+'/'+prefix+'_final.xls',index=False,sep='\t')
			if re.search('species',path):
                                f.to_csv(end_dir3+'/'+prefix+'_final.xls',index=False,sep='\t')
