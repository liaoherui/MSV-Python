#author: liaoherui@mail.dlut.edu.cn

import re
import os
import sys
import getopt

'''--------Get Option--------'''
opts,args=getopt.getopt(sys.argv[1:],"hp:o:e:g:l:s:t:")
phenotype=''
out_y='../../Result/1.start_stat/Gene/Out_y'
level=''
ptype=''

for opt,arg in opts:
	if opt=='-h':
		print 'eg: python '+os.path.basename(sys.argv[0])+' -e [level] -p [phenotype_dir] -o [out_y_dir]'
	elif opt=='-p' and not arg=='':
		phenotype=arg
	elif opt=='-o' and not arg=='':
		out_y=arg
	elif opt =='-e' and not arg=='':
		level=arg
	elif opt =='-g' and not arg=='':
		out_g=arg
	elif opt=='-l' and not arg=='':
		out_p=arg
	elif opt=='-s' and not arg=='':
		out_s=arg
	elif opt=='-t' and not arg=='':
		ptype=arg
		

'''------Make Output dir------'''
outdir='../../Result/2.data_visual'
end_dir=''
if level=='ge':
	end_dir=outdir+'/Gene/step1'
	if not (os.path.exists(end_dir)):
		os.makedirs(end_dir,0755)
if level=='ta':
	end_dir1=outdir+'/Taxo/genus/step1'
	end_dir2=outdir+'/Taxo/phylum/step1'
	end_dir3=outdir+'/Taxo/species/step1'
	if not (os.path.exists(end_dir1)):
		os.makedirs(end_dir1,0755)
	if not (os.path.exists(end_dir2)):
                os.makedirs(end_dir2,0755)
	if not (os.path.exists(end_dir3)):
                os.makedirs(end_dir3,0755)

if level=='ko':
	end_dir=outdir+'/KO/step1'
	if not (os.path.exists(end_dir)):
		os.makedirs(end_dir,0755)



#Initial area_hash -> key 1:Individuals ID | value: phenotype

print 'Initial area_hash......'
area_hash={}
path=phenotype
for filename in os.listdir(path):
	f1=open(path+'/'+filename,'r')
	while True:
		line=f1.readline()
		line=line.strip()
		if not line:break
		if re.search('^Individuals_ID',line):
			ele=line.split('\t')		
			index=ele.index(ptype)	
			#print index
			#exit()
		ele=line.split('\t')
		if ele[0] not in area_hash:
			area_hash[ele[0]]=ele[index].strip()
		if ele[4] not in area_hash:
			area_hash[ele[4]]=ele[index].strip()
		if ele[1] not in area_hash:
			area_hash[ele[1]]=ele[index].strip()
	#if True:break	
#print area_has	
#h
print 'area_hash is done!'	
	

#Initial three_hash -> key 1:IGC Gene Info | key 2:Area |key 3:Individuals ID |value: abundance value
print 'Initial three_hash......'
if level=='ge' or level=='ko':
	path=out_y
	three_hash={}
if level=='ta':
	path_g=out_g
	path_p=out_p
	path_s=out_s
	path_ta=[]
	path_ta.append(path_g)
	path_ta.append(path_p)
	path_ta.append(path_s)	
	three_hash_g={}
	three_hash_p={}
	three_hash_s={}
count=1



def addthreedimdict(thedict, key_a, key_b,key_c, val):        
                        if key_a in thedict:
				if key_b in thedict[key_a]:
					thedict[key_a][key_b].update({key_c:val})
				else:
					thedict[key_a].update({keyb:{key_c:val}})
                        else:
                                thedict.update({key_a:{key_b: {key_c:val}}})



if level=='ge' or level=='ko':
	for filename in os.listdir(path):
		if re.search('Canada',filename):continue
		print filename+' strats...... '
		count=1
		first_line=[]
		f2=open(path+'/'+filename,'r')
		while True:
			info_count=0
			line=f2.readline()	
			if not line: break		
			line=line.strip()
			ele=line.split('\t')
			if count==1:
				for e in ele:
					first_line.append(e)
					if e not in three_hash:
						three_hash.update({e:{}})	
					else:continue
				count+=1
				continue
			ele[0]=ele[0].strip()
		#ele[4]=ele[4].strip()
		#print ele
			for info in first_line:
				ele[info_count+1]=ele[info_count+1].strip()
				if ele[0] in area_hash: 
					if area_hash[ele[0]] not in three_hash[info]:
						three_hash[info].update({area_hash[ele[0]]:{ele[0]:ele[info_count+1]}})
					else:
						if ele[0] not in three_hash[info][area_hash[ele[0]]]:
							three_hash[info][area_hash[ele[0]]].update({ele[0]:ele[info_count+1]})							
						else:
							three_hash[info][area_hash[ele[0]]][ele[0]]=ele[info_count+1]
					info_count+=1
				else: 
					print 'area_hash can\'t find this key: '+ele[0]
					break
			print  filename+' ends!'
	#if True:break	
		print 'three_hash is done!'

if level=='ta':
	for path in path_ta:
		for filename in os.listdir(path):
			print filename+' strats...... '
                	count=1
			first_line=[]
			f2=open(path+'/'+filename,'r')
	                while True:
        	                info_count=0
                	        line=f2.readline()
                        	if not line: break
                       		line=line.strip()
	                        ele=line.split('\t')
        	                if count==1:
	                	        for e in ele:
        	                	        first_line.append(e)
						if re.search('genus',path):
		        	                        if e not in three_hash_g:
	        	        	                        three_hash_g.update({e:{}})
							else:continue
						if re.search('phylum',path):
                                                	if e not in three_hash_p:
                                                        	three_hash_p.update({e:{}})
							else:continue
						if re.search('species',path):
							if e not in three_hash_s:
                	                                        three_hash_s.update({e:{}})
							else:continue
	                	           
	                       		count+=1
		                        continue
	        	        ele[0]=ele[0].strip()
				for info in first_line:
                        		ele[info_count+1]=ele[info_count+1].strip()
	                        	if ele[0] in area_hash:
						if re.search('genus',path):
	        	        	                if area_hash[ele[0]] not in three_hash_g[info]:
        	        		                        three_hash_g[info].update({area_hash[ele[0]]:{ele[0]:ele[info_count+1]}})
                	        		        else:
                        		        	        if ele[0] not in three_hash_g[info][area_hash[ele[0]]]:
                               		 	        		three_hash_g[info][area_hash[ele[0]]].update({ele[0]:ele[info_count+1]})               
                                       				else:
	                                               		 	three_hash_g[info][area_hash[ele[0]]][ele[0]]=ele[info_count+1]
			                                info_count+=1
						if re.search('phylum',path):
							if area_hash[ele[0]] not in three_hash_p[info]:
                       		         	                three_hash_p[info].update({area_hash[ele[0]]:{ele[0]:ele[info_count+1]}})
                                	        	else:
                                        	        	if ele[0] not in three_hash_p[info][area_hash[ele[0]]]:
                                                	        	three_hash_p[info][area_hash[ele[0]]].update({ele[0]:ele[info_count+1]})     
	                                               		else:
        	                                               		three_hash_p[info][area_hash[ele[0]]][ele[0]]=ele[info_count+1]
	                	                        info_count+=1
						if re.search('species',path):
							if area_hash[ele[0]] not in three_hash_s[info]:
								three_hash_s[info].update({area_hash[ele[0]]:{ele[0]:ele[info_count+1]}})
	                        	                else:
        	                        	                if ele[0] not in three_hash_s[info][area_hash[ele[0]]]:
                	                        	                three_hash_s[info][area_hash[ele[0]]].update({ele[0]:ele[info_count+1]})     
	                        	                        else:
        	                        	                        three_hash_s[info][area_hash[ele[0]]][ele[0]]=ele[info_count+1]
                	                        	info_count+=1
	                	        else:
        	                	        print 'area_hash can\'t find this key: '+ele[0]
                	                	break

       			print  filename+' ends!'
	print 'three_hash of taxo is done!'
#print three_hash
#exit()
#write out the 'xls' file to visualize abundance data to show the distribution of the drug gene
if level=='ge' or level=='ko':
	for key1 in three_hash:
		ID=''
		filename=''
		array=[]
		class_name=''
		if re.search('--OR--',key1):
			nums=re.split('--OR--',key1)
			for num in nums:
				num=num.strip()
				Info=re.split('\|',num)
				ID=Info[2].strip()
				#class_name=Info[1]
				filename+=ID+'_'
		else:
			key1=key1.strip()
			if level=='ge':
				Info2=re.split('\|',key1)
				ID=Info2[2].strip()
				filename+=ID+'_'
		filename=filename[:-1]
		filename=re.sub(':','_',filename)
		tem=re.split('_',filename)
		if len(tem)>30:
			t=[]
			for i in range(0,30):
				t.append(tem[i])
			filename='_'.join(t)	
			filename+='_ID_more'
				
		#filename=class_name
		#filename=re.sub('/','_',filename)
		if level=='ko':
			filename=key1
		print filename+'.xls is  making......'
		o2=open(end_dir+'/'+filename+'.xls','w+')
		#start writing
		o2.write('Sample_Name')
		for key2 in three_hash[key1]:
			o2.write('\t'+key2)
			array.append(key2)
		o2.write('\n')	
		for key2 in three_hash[key1]:
			for key3 in three_hash[key1][key2]:
				o2.write(key3)
				for arr in array:
					if arr in three_hash[key1]:
						if key3 in three_hash[key1][arr]:
							value=float(three_hash[key1][arr][key3])
							if not value==0:
								o2.write('\t'+three_hash[key1][arr][key3])
							else:
								o2.write('\t0')
						else:
							o2.write('\t0.1')  #consider NA->0.1,this is for the next step
				o2.write('\n')
		print filename+' is done now !'

if level=='ta':
	for key1 in three_hash_g:
		filename=''
                array=[]
		filename=key1
		filename=re.sub('/','_',filename)
		print filename+'.xls is  making......'
		o2_g=open(end_dir1+'/'+filename+'.xls','w+')		
		o2_g.write('Sample_Name')
                for key2 in three_hash_g[key1]:
                        o2_g.write('\t'+key2)
                        array.append(key2)
                o2_g.write('\n')
                for key2 in three_hash_g[key1]:
                        for key3 in three_hash_g[key1][key2]:
                                o2_g.write(key3)
                                for arr in array:
                                        if arr in three_hash_g[key1]:
                                                if key3 in three_hash_g[key1][arr]:
							value=float(three_hash_g[key1][arr][key3])
                                                        if not value==0:
                                                                o2_g.write('\t'+three_hash_g[key1][arr][key3])
                                                        else:
                                                                o2_g.write('\t0')
                                                else:
                                                        o2_g.write('\t0.1')  #consider NA->0.1,this is for the next step
                                o2_g.write('\n')	
		print filename+' is done!'
	for key1 in three_hash_p:
                filename=''
                array=[]
                filename=key1
                filename=re.sub('/','_',filename)
                print filename+'.xls is  making......'
                o2_p=open(end_dir2+'/'+filename+'.xls','w+')
                o2_p.write('Sample_Name')
                for key2 in three_hash_p[key1]:
                        o2_p.write('\t'+key2)
                        array.append(key2)
                o2_p.write('\n')
                for key2 in three_hash_p[key1]:
                        for key3 in three_hash_p[key1][key2]:
                                o2_p.write(key3)
                                for arr in array:
                                        if arr in three_hash_p[key1]:
                                                if key3 in three_hash_p[key1][arr]:
							value=float(three_hash_p[key1][arr][key3])
                                                        if not value==0 :
                                                                o2_p.write('\t'+three_hash_p[key1][arr][key3])
                                                        else:
                                                                o2_p.write('\t0')
                                                else:
                                                        o2_p.write('\t0.1')  #consider NA->0.1,this is for the next step
                                o2_p.write('\n')
		print filename+'is done!'
	for key1 in three_hash_s:
                filename=''
                array=[]
                filename=key1
                filename=re.sub('/','_',filename)
		filename=re.sub('\s','-',filename)
		filename=re.sub('\.','-',filename)
                print filename+'.xls is  making......'
                o2_s=open(end_dir3+'/'+filename+'.xls','w+')
                o2_s.write('Sample_Name')
                for key2 in three_hash_s[key1]:
                        o2_s.write('\t'+key2)
                        array.append(key2)
                o2_s.write('\n')
                for key2 in three_hash_s[key1]:
                        for key3 in three_hash_s[key1][key2]:
                                o2_s.write(key3)
                                for arr in array:
                                        if arr in three_hash_s[key1]:
                                                if key3 in three_hash_s[key1][arr]:
							value=float(three_hash_s[key1][arr][key3])
                                                        if not value==0:
                                                                o2_s.write('\t'+three_hash_s[key1][arr][key3])
                                                        else:
                                                                o2_s.write('\t0')
                                                else:
                                                        o2_s.write('\t0.1')  #consider NA->0.1,this is for the next step
                                o2_s.write('\n')
		print filename+'is done!'
