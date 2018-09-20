import re
import os
import sys
import getopt
'''-----Get Option----'''
opts,args=getopt.getopt(sys.argv[1:],"he:t:")
level=''
ptype=''
for opt,arg in opts:
        if opt=='-h':
                print 'eg: python '+os.path.basename(sys.argv[0])+' -e [level] -t [ptype]'
        if opt=='-e':
                level=arg
	if opt=='-t':
		ptype=arg
if level=='ge':
        path='../../Result/2.data_visual/Gene/step4'
if level=='ta':
        path_g='../../Result/2.data_visual/Taxo/genus/step4'
	path_p='../../Result/2.data_visual/Taxo/phylum/step4'
	path_s='../../Result/2.data_visual/Taxo/species/step4'
	path_ta=[]
	path_ta.append(path_g)
	path_ta.append(path_p)
	path_ta.append(path_s)

if level=='ko':
        path='../../Result/2.data_visual/KO/step4'


'''----Make Output dir-----'''
outdir='../../Result/2.data_visual'
end_dir=''

if level=='ge':
        end_dir=outdir+'/Gene/Barplot_Data'
        if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)
if level=='ta':
        end_dir1=outdir+'/Taxo/genus/Barplot_Data'
	end_dir2=outdir+'/Taxo/phylum/Barplot_Data'
	end_dir3=outdir+'/Taxo/species/Barplot_Data'
        if not (os.path.exists(end_dir1)):
                os.makedirs(end_dir1,0755)
	if not (os.path.exists(end_dir2)):
                os.makedirs(end_dir2,0755)
	if not (os.path.exists(end_dir3)):
                os.makedirs(end_dir3,0755)
	
if level=='ko':
        end_dir=outdir+'/KO/Barplot_Data'
        if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)

if level=='ge' or level=='ko':
	for filename in os.listdir(path):
		f=open(path+'/'+filename,'r')
		o=open(end_dir+'/'+filename,'w+')
		s0=[]
		st=[]
		sn=[]
		while True:
			line=f.readline()
			line=line.strip()
			area=line.split('\t')
			area=area[1:]
			if True:break
		while True:
			line=f.readline()
			if not line:break
			line=line.strip()
			num=line.split('\t')	
			
			
			for n in num:
				if re.search('^ID',n) or re.search('^KO',n):continue
				n=re.split('\,',n)
				s0.append(n[0])
				st.append(n[1])
				sn.append(int(n[1])-int(n[0]))
		o.write(ptype+'\tSample numbers(value=0)\tSample numbers(value!=0)\n')
		count=0
		for a in area:
			o.write(a)
			o.write('\t'+str(s0[count])+'\t'+str(sn[count])+'\n')
			count+=1
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
	                s0=[]
	                st=[]
	                sn=[]
	                while True:
	                        line=f.readline()
	                        line=line.strip()
	                        area=line.split('\t')
	                        area=area[1:]
	                        if True:break
	                while True:
	                        line=f.readline()
	                        if not line:break
	                        line=line.strip()
	                        num=line.split('\t')
				
				for n in num:
                                	if re.search('[A-Za-z]',n):continue
	                                n=re.split('\,',n)
        	                        s0.append(n[0])
	                	        st.append(n[1])					
					sn.append(int(n[1])-int(n[0]))
                    	        #sn.append(int(n[1])-int(n[0]))
			o.write(ptype+'\tSample numbers(value=0)\tSample numbers(value!=0)\n')
        	        count=0
               		for a in area:
                       		o.write(a)
	                        o.write('\t'+str(s0[count])+'\t'+str(sn[count])+'\n')
                       		count+=1
