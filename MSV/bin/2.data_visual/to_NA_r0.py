import re
import os
import sys
import getopt

'''-------Get Option------'''
opts,args=getopt.getopt(sys.argv[1:],"he:")
level=''
for opt,arg in opts:
	if opt=='-h':
		print 'eg: python '+os.path.basename(sys.argv[0])+' -e [level]'
	if opt=='-e':
		level=arg 
if level=='ge':
	path='../../Result/2.data_visual/Gene/step2'
if level=='ta':
        path_g='../../Result/2.data_visual/Taxo/genus/step2'
	path_p='../../Result/2.data_visual/Taxo/phylum/step2'
	path_s='../../Result/2.data_visual/Taxo/species/step2'
	path_ta=[]
	path_ta.append(path_g)
	path_ta.append(path_p)
	path_ta.append(path_s)
if level=='ko':
        path='../../Result/2.data_visual/KO/step2'

'''---------Make Output dir---------'''
outdir='../../Result/2.data_visual'
end_dir=''
if level=='ge':
        end_dir=outdir+'/Gene/step3'
        if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)
if level=='ta':
        end_dir1=outdir+'/Taxo/genus/step3'
	end_dir2=outdir+'/Taxo/phylum/step3'
	end_dir3=outdir+'/Taxo/species/step3'
        if not (os.path.exists(end_dir1)):
                os.makedirs(end_dir1,0755)
	if not (os.path.exists(end_dir2)):
                os.makedirs(end_dir2,0755)	
	if not (os.path.exists(end_dir3)):
                os.makedirs(end_dir3,0755)
if level=='ko':
        end_dir=outdir+'/KO/step3'
        if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)

if level=='ge' or level=='ko':
	for filename in os.listdir(path):
		f=open(path+'/'+filename,'r')
		o=open(end_dir+'/'+filename,'w+')
		while True:
			line=f.readline()	
			if not line:break
			line=line.strip()
			ele=line.split('\t')
			new_line=''
			count=1
			for e in ele:
				if count==1:
					new_line+=str(e)
					count+=1
					continue
				if e==0.1 or e=='0.1':
					new_line+='\tNA'
				elif e==0.0 or e=='0.0':
					new_line+='\t0'	
				else:
					new_line+='\t'+str(e)
			new_line+='\n'
			o.write(new_line)

if level=='ta':
	for path in path_ta:
		for filename in os.listdir(path):
	                f=open(path+'/'+filename,'r')
			if re.search('genus',path):
	        	        o=open(end_dir1+'/'+filename,'w+')
			if re.search('phylum',path):
				o=open(end_dir2+'/'+filename,'w+')
			if re.search('species',path):
                                o=open(end_dir3+'/'+filename,'w+')
	                while True:
	                        line=f.readline()
	                        if not line:break
	                        line=line.strip()
	                        ele=line.split('\t')
	                        new_line=''
	                        count=1
	                        for e in ele:
	                                if count==1:
	                                        new_line+=str(e)
	                                        count+=1
	                                        continue
	                                if e==0.1 or e=='0.1':
	                                        new_line+='\tNA'
	                                elif e==0.0 or e=='0.0':
	                                        new_line+='\t0'
	                                else:
	                                        new_line+='\t'+str(e)
	                        new_line+='\n'
	                        o.write(new_line)
	
