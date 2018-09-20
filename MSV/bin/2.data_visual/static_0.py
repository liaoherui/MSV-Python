import re
import os
import sys
import getopt

'''------Get Option--------'''
opts,args=getopt.getopt(sys.argv[1:],"he:")
level=''
for opt,arg in opts:
	if opt=='-h':
		print 'eg: python '+os.path.basename(sys.argv[0])+' -e [level]'
	if opt=='-e':
		level=arg
if level=='ge':
	path='../../Result/2.data_visual/Gene/step3'
if level=='ta':
	path_g='../../Result/2.data_visual/Taxo/genus/step3'
	path_p='../../Result/2.data_visual/Taxo/phylum/step3'
	path_s='../../Result/2.data_visual/Taxo/species/step3'
	path_ta=[]	
	path_ta.append(path_g)
	path_ta.append(path_p)
	path_ta.append(path_s)
if level=='ko':
        path='../../Result/2.data_visual/KO/step3'

'''----Make Output dir-----'''
outdir='../../Result/2.data_visual'
end_dir=''

if level=='ge':
        end_dir=outdir+'/Gene/step4'
        if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)
if level=='ta':
        end_dir1=outdir+'/Taxo/genus/step4'
	end_dir2=outdir+'/Taxo/phylum/step4'
	end_dir3=outdir+'/Taxo/species/step4'
	
        if not (os.path.exists(end_dir1)):
                os.makedirs(end_dir1,0755)
	if not (os.path.exists(end_dir2)):
                os.makedirs(end_dir2,0755)
	if not (os.path.exists(end_dir3)):
		os.makedirs(end_dir3,0755)
if level=='ko':
        end_dir=outdir+'/KO/step4'
        if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)

'''----------Start-------'''
if level=='ge' or level=='ko':
	for filename in os.listdir(path):
		if re.search('report',filename):continue
		f=open(path+'/'+filename,'r')
		prefix=re.split('\.',filename)
		o=open(end_dir+'/'+prefix[0]+'_report.xls','w+')
		count=0
		biaotou=''
		hash_count={}
		hash_NA={}	
	
		while True:
			line=f.readline()
			if not line:break
			if re.search('^Sample',line):
				biaotou=re.sub('Sample_Name','',line)
				biaotou=biaotou.strip()
				line=line.strip()
				fl=line.split('\t')
				fl=fl[1:]
				for i in fl:
					i=i.strip()
					hash_count[i]=0
					hash_NA[i]=0
				continue	
			line=line.strip()
			ele=line.split('\t')
			ele=ele[1:]
			c=0
			for e in ele:
				e=e.strip()
				if e=='0' or e==0:
					hash_count[fl[c]]+=1
					c+=1
					continue
				if e=='NA':
					hash_NA[fl[c]]+=1
					c+=1
					continue
				else:
					c+=1
					continue
				
			count+=1
		if level=='ge':
			o.write('Gene_ID\t'+biaotou+'\n')
		if level=='ko':
			o.write('KO_ID\t'+biaotou+'\n')
		o.write(prefix[0])
		for l in fl:
			o.write('\t'+str(hash_count[l])+','+str(count-hash_NA[l]))
		o.write('\n')
if level=='ta':
	for path in path_ta:
		for filename in os.listdir(path):
			if re.search('report',filename):continue
	                f=open(path+'/'+filename,'r')
	                prefix=re.split('\.',filename)
			if re.search('genus',path):
		                o=open(end_dir1+'/'+prefix[0]+'_report.xls','w+')
			if re.search('phylum',path):
				o=open(end_dir2+'/'+prefix[0]+'_report.xls','w+')
			if re.search('species',path):
				o=open(end_dir3+'/'+prefix[0]+'_report.xls','w+')
        	        count=0
                	biaotou=''
	                hash_count={}
	                hash_NA={}
			while True:
	                        line=f.readline()
	                        if not line:break
	                        if re.search('^Sample',line):
	                                biaotou=re.sub('Sample_Name','',line)
	                                biaotou=biaotou.strip()
	                                line=line.strip()
	                                fl=line.split('\t')
	                                fl=fl[1:]
	                                for i in fl:
	                                        i=i.strip()
	                                        hash_count[i]=0
        	                                hash_NA[i]=0
	                                continue
	                        line=line.strip()
	                        ele=line.split('\t')
	                        ele=ele[1:]
	                        c=0
				for e in ele:
					e=e.strip()
                                	if e=='0' or e==0:
                                       		hash_count[fl[c]]+=1
	                                        c+=1
	                                        continue
        	                        if e=='NA':
                	                        hash_NA[fl[c]]+=1
                        	                c+=1
                                	        continue
	                                else:
        	                                c+=1
                	                        continue
	
        	                count+=1
			o.write('Taxo_ID\t'+biaotou+'\n')
			pre=re.sub('_final','',prefix[0])
			o.write(pre)
	                for l in fl:
        	                o.write('\t'+str(hash_count[l])+','+str(count-hash_NA[l]))
	                o.write('\n')
