import re
import os
import math
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
        path='../../Result/2.data_visual/Gene/step5'
if level=='ta':
        path_g='../../Result/2.data_visual/Taxo/genus/step5'
	path_p='../../Result/2.data_visual/Taxo/phylum/step5'
	path_s='../../Result/2.data_visual/Taxo/species/step5'
	path_ta=[]
	path_ta.append(path_g)
	path_ta.append(path_p)
	path_ta.append(path_s)

if level=='ko':
        path='../../Result/2.data_visual/KO/step5'


'''----Make Output dir-----'''
outdir='../../Result/2.data_visual'
end_dir=''

if level=='ge':
        end_dir=outdir+'/Gene/Boxplot_Data'
        if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)
if level=='ta':
        end_dir1=outdir+'/Taxo/genus/Boxplot_Data'
	end_dir2=outdir+'/Taxo/phylum/Boxplot_Data'
	end_dir3=outdir+'/Taxo/species/Boxplot_Data'
        if not (os.path.exists(end_dir1)):
                os.makedirs(end_dir1,0755)
	if not (os.path.exists(end_dir2)):
                os.makedirs(end_dir2,0755)
	if not (os.path.exists(end_dir3)):
                os.makedirs(end_dir3,0755)
if level=='ko':
        end_dir=outdir+'/KO/Boxplot_Data'
        if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)
if level=='ge' or level=='ko':
	for  filename in os.listdir(path):
		f=open(path+'/'+filename,'r')
		o=open(end_dir+'/'+filename,'w+')
		while True:	
			line=f.readline()
			o.write(line)
			if True:break
		while True:
			count=1
			line=f.readline()
			line=line.strip()
			if not line :break
			ele=line.split('\t')
			for e in ele:
				e=e.strip()
				if count==1:
					o.write(e)
					count+=1
					continue
				if re.search('NA',e) or e=='0' or e==0:
					o.write('\tNA')
					continue
				e=math.log10(float(e))
				o.write('\t'+str(e))
			o.write('\n')
if level=='ta':
	for path in path_ta:
		for  filename in os.listdir(path):
	                f=open(path+'/'+filename,'r')
			if re.search('genus',path):
		                o=open(end_dir1+'/'+filename,'w+')
			if re.search('phylum',path):
				o=open(end_dir2+'/'+filename,'w+')
			if re.search('species',path):
				o=open(end_dir3+'/'+filename,'w+')
	                while True:
	                        line=f.readline()
	                        o.write(line)
	                        if True:break
			while True:
	                        count=1
	                        line=f.readline()
	                        line=line.strip()
	                        if not line :break
	                        ele=line.split('\t')
	                        for e in ele:
	                                e=e.strip()
	                                if count==1:
	                                        o.write(e)
	                                        count+=1
	                                        continue
	                                if re.search('NA',e) or e=='0' or e==0:
	                                        o.write('\tNA')
	                                        continue
	                                e=math.log10(float(e))
	                                o.write('\t'+str(e))
	                        o.write('\n')
