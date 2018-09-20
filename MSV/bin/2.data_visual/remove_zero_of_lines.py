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
        end_dir=outdir+'/Gene/step5'
        if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)
if level=='ta':
        end_dir1=outdir+'/Taxo/genus/step5'
	end_dir2=outdir+'/Taxo/phylum/step5'
	end_dir3=outdir+'/Taxo/species/step5'
        if not (os.path.exists(end_dir1)):
                os.makedirs(end_dir1,0755)
	if not (os.path.exists(end_dir2)):
                os.makedirs(end_dir2,0755)
	if not (os.path.exists(end_dir3)):
                os.makedirs(end_dir3,0755)
if level=='ko':
        end_dir=outdir+'/KO/step5'
        if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)

if level=='ko' or level=='ge':
	for filename in os.listdir(path):
		sample_count=0
		if not re.search('final',filename):continue
		f=open(path+'/'+filename,'r')
		new=re.split('\.',filename)
		prefix=new[0]
		o=open(end_dir+'/'+prefix+'_visual.xls','w+')
		print filename+' starts removing...'
		while True:
			count=0
			line=f.readline()
			if not line:break
			if sample_count==0:
				o.write(line)
				sample_count+=1
				continue
			eles=line.split('\t')
			for ele in eles:
				ele=ele.strip()
				if ele =='0' or ele=='NA':
					count+=1
			if count==(len(eles)-1):continue
			else:
				o.write(line)
		
		print filename+' ends !'	
if level=='ta':
	for path in path_ta:
		for filename in os.listdir(path):
	                sample_count=0
	                if not re.search('final',filename):continue
	                f=open(path+'/'+filename,'r')
	                new=re.split('\.',filename)
	                prefix=new[0]
			if re.search('genus',path):
		                o=open(end_dir1+'/'+prefix+'_visual.xls','w+')
			if re.search('phylum',path):
				o=open(end_dir2+'/'+prefix+'_visual.xls','w+')
			if re.search('species',path):
				o=open(end_dir3+'/'+prefix+'_visual.xls','w+')
	                print filename+' starts removing...'		
			while True:
	                        count=0
	                        line=f.readline()
	                        if not line:break
	                        if sample_count==0:
	                                o.write(line)
	                                sample_count+=1
	                                continue
	                        eles=line.split('\t')
	                        for ele in eles:
	                                ele=ele.strip()
	                                if ele =='0' or ele=='NA':
	                                        count+=1
	                        if count==(len(eles)-1):continue
	                        else:
        	                        o.write(line)
	                print filename+' ends !'
		
