#author: liaoherui@mail.dlut.edu.cn
import os
import re
import sys
import getopt
import time

'''------Get Option----------'''
opts,args=getopt.getopt(sys.argv[1:],"hl:e:")
gene_list=''
level=''

for opt,arg in opts:
	if opt =="-h":
		print 'eg: python '+os.path.basename(sys.argv[0])+' -e [level]  -l [gene_list]'
	elif opt == "-l":
		gene_list=arg
	elif opt =="-e":
		level=arg	

'''--------product the output dir-------'''
outdir='../../Result/1.start_stat'
#if not (os.path.exists(outdir)):
#	os.makedirs(outdir,0755)
if re.search('g',level) :
	if not (os.path.exists(outdir+'/Gene')):
		os.makedirs(outdir+'/Gene',0755)
if level=='ta' :
	if not (os.path.exists(outdir+'/Taxo/genus')):
		os.makedirs(outdir+'/Taxo/genus',0755)
	if not (os.path.exists(outdir+'/Taxo/phylum')):
                os.makedirs(outdir+'/Taxo/phylum',0755)
	if not (os.path.exists(outdir+'/Taxo/species')):
                os.makedirs(outdir+'/Taxo/species',0755)
if level=='ko' :
	if not (os.path.exists(outdir+'/KO')):
                os.makedirs(outdir+'/KO',0755)


'''-----------Strat----------'''


if True:
	start=time.clock()
	fa=open('../../profile/Other_profile/annotation.summary','r')
	#initial anno hash.	key:IGC_name/value:ID_from_Abundance_profile
	print 'Initializing anno hash starts!'
	anno={}
	anno_g={}
	anno_p={}
	anno_s={}
	anno_ko={}
	while True:
		line=fa.readline()
		if not line:break
		if re.match('^ID',line): continue
		ele=line.split('\t')
		anno[ele[1]]=ele[0]
		if not ele[6]=='Unknown' and level=='ko' :
			anno_ko[ele[1]]=ele[6].strip()
		if not ele[3]=='Unknown'and level=='ta':
			anno_p[ele[1]]=ele[3]
		if not ele[4]=='Unknown' and level=='ta':
			anno_g[ele[1]]=ele[4]
		if not ele[5]=='Unknown' and level=='ta':
			anno_s[ele[1]]=ele[5]
	fa.close()
	end=time.clock()
	
	print 'anno hash is done!'
	print 'Use Time: '+str(end-start)


	start=time.clock()
	print'Initializing drug_IGC hash starts!'
	fd=open(gene_list,'r')
	#initial drug_IGC hash.	key:IGC_name/value:raw_genename/drug(ID from Drug_IGC.xls)
	drug_IGC={}
	while True:
		line=fd.readline()
		if not line :break
		if re.search('^Num',line): continue
		ele=line.split('\t')
		if ele[2] not in drug_IGC.keys():
			drug_IGC[ele[2]]=ele[3]+'|'+ele[1]+'|ID:'+ele[0]
		else:
			drug_IGC[ele[2]]+='--OR--'+ele[3]+'|'+ele[1]+'|ID:'+ele[0]
	fd.close()
	end=time.clock()	
	#print drug_IGC
	#print drug_IGC[anno['5061288']]
	print 'drug_IGC hash is done!'
	print 'Use time: '+str(end-start)
	#print drug_IGC
	
#------level : gene number-------------
	if level=='gn' :
		start=time.clock()
		print 'f_hash of Gene  is running......'
		f_hash={}
		for key in drug_IGC.keys():
                        if key in anno.keys():
                                f_hash[anno[key]]=anno[key]
                        else: continue
                end=time.clock()
                print 'f_hash of Gene  is done'
                print 'Use time: '+str(end-start)
#------level : gene name from IGC---------------
	if level=='gm' :
                start=time.clock()
                print 'f_hash of Gene is running......'
                f_hash={}
                for key in drug_IGC.keys():
                        if key in anno.keys():
                                f_hash[anno[key]]=key
                        else: continue
                end=time.clock()
                print 'f_hash of Gene is done'
                print 'Use time: '+str(end-start)

#------level : gene annotation----------
	#product the f_hash we finally use!  key:ID_from_Abundance_profile/value:raw_genename/drug(ID from Drug_IGC.xls)
	if level=='ga':
		start=time.clock()
		print 'f_hash of Gene is running......'
		f_hash={}
		for key in drug_IGC.keys():
			if key in anno.keys():
				f_hash[anno[key]]=drug_IGC[key]
			else: continue
		end=time.clock()
		print 'f_hash of Gene  is done'
		print 'Use time: '+str(end-start)
	#y=open('Gene_ID.xls','w+')
	#for key in f_hash.keys():
	#	y.write( key+'\t'+f_hash[key]+'\n')
#------level : KO---------------
	if level=='ko':
		start=time.clock()
                print 'f_hash of KO is running......'
                f_hash={}
                for key in drug_IGC.keys():
                        if key in anno_ko.keys():
                                f_hash[anno_ko[key]]=anno_ko[key]
                        else: continue
                end=time.clock()
                print 'f_hash of KO is done'
                print 'Use time: '+str(end-start)			
#------level : Taxo---------------
	if level=='ta':
                start=time.clock()
                print 'f_hash of Taxo  is running......'
                f_hash_g={}
		f_hash_p={}
		f_hash_s={}
                for key in drug_IGC.keys():
                        if key in anno_g.keys():
                                f_hash_g[anno_g[key]]=anno_g[key]
			if key in anno_p.keys():
				f_hash_p[anno_p[key]]=anno_p[key]
			if key in anno_s.keys():
				f_hash_s[anno_s[key]]=anno_s[key]
                end=time.clock()
                print 'f_hash of Taxo is done! '
                print 'Use time: '+str(end-start)
	#print f_hash_s

	# use 'for'  to handle each profile
	ele=[]
	for filename in os.listdir('../../profile/Gene_Abundance'):
		filename=filename.strip()
		s=re.split('_',filename)
		ele.append(str(s[0]))

	r=open('../../Result/1.start_stat/convert.R','w+')
	for each_dir in ele:
	#each_dir='ERP000108'
		if re.search('g',level):
			f=open('../../profile/Gene_Abundance/'+each_dir+'_GeneCatalog_profile.xls','r')
		elif level=='ko':
			f=open('../../profile/KO_Abundance/'+each_dir+'_KO_abundance_profile.xls')
		elif level=='ta':
			fg=open('../../profile/Taxo_Abundance/genus/'+each_dir+'_genus_abundance_profile.xls')
			fp=open('../../profile/Taxo_Abundance/phylum/'+each_dir+'_phylum_abundance_profile.xls')
			fs=open('../../profile/Taxo_Abundance/species/'+each_dir+'_species_abundance_profile.xls')
		if re.search('g',level):
			o=open('../../Result/1.start_stat/Gene/'+each_dir+'_gene_result.xls','w+')
			r.write('tx <- read.table("Gene/'+each_dir+'_gene_result.xls" , header=FALSE,sep="\\t")\nty<-t(tx)\nwrite.table(ty,file="Gene/Out_y/'+each_dir+'_gene_result_y.xls",quote=F,sep="\\t", col.name=F, row.names=F)\n\n')
		if level=='ko':
			o=open('../../Result/1.start_stat/KO/'+each_dir+'_ko_result.xls','w+')
			r.write('tx <- read.table("KO/'+each_dir+'_ko_result.xls" , header=FALSE,sep="\\t")\nty<-t(tx)\nwrite.table(ty,file="KO/Out_y/'+each_dir+'_ko_result_y.xls",quote=F,sep="\\t", col.name=F, row.names=F)\n\n')
		if level=='ta':
			o1=open('../../Result/1.start_stat/Taxo/genus/'+each_dir+'_genus_result.xls','w+')
			o2=open('../../Result/1.start_stat/Taxo/phylum/'+each_dir+'_phylum_result.xls','w+')
			o3=open('../../Result/1.start_stat/Taxo/species/'+each_dir+'_species_result.xls','w+')
                        r.write('tx <- read.table("Taxo/genus/'+each_dir+'_genus_result.xls" , header=FALSE,sep="\\t")\nty<-t(tx)\nwrite.table(ty,file="Taxo/genus/Out_y/'+each_dir+'_genus_result_y.xls",quote=F,sep="\\t", col.name=F, row.names=F)\n')
			r.write('tx <- read.table("Taxo/phylum/'+each_dir+'_phylum_result.xls" , header=FALSE,sep="\\t")\nty<-t(tx)\nwrite.table(ty,file="Taxo/phylum/Out_y/'+each_dir+'_phylum_result_y.xls",quote=F,sep="\\t", col.name=F, row.names=F)\n')
			r.write('tx <- read.table("Taxo/species/'+each_dir+'_species_result.xls" , header=FALSE,sep="\\t")\nty<-t(tx)\nwrite.table(ty,file="Taxo/species/Out_y/'+each_dir+'_species_result_y.xls",quote=F,sep="\\t", col.name=F, row.names=F)\n\n')


		print 'The project: '+each_dir+' starts stating!'
		content='' #the content of line without the first column
		#initial biaotou
		first_line='' #this is biao tou 
		while True:
			if re.search('g',level) or level=='ko':
				line=f.readline()
				first_line=line
			elif level=='ta':
				line1=fg.readline()
				line2=fp.readline()
				line3=fs.readline()
				
			if not level=='ta':
				o.write(first_line)
			else:
				o1.write(line1)
				o2.write(line2)
				o3.write(line3)
			if True: break
		#start stating
		start=time.clock()
		if level=='ko' or re.search('g',level):
			while True:
				line=f.readline()
				if not line :break
				ele=line.split('\t')
				#print ele[0]+' |'
				if ele[0] in f_hash.keys():
				#	print ele[0] +'has been found!'
					e=ele[1:]
					content='\t'.join(e)
					o.write(f_hash[ele[0]]+'\t'+content)
		elif level=='ta':
			while True:
				line1=fg.readline()
				if not line1:break
				ele1=line1.split('\t')
				if ele1[0] in f_hash_g.keys():
					e1=ele1[1:]	
					content='\t'.join(e1)
					o1.write(f_hash_g[ele1[0]]+'\t'+content)
			while True:
				line2=fp.readline()
				if not line2:break
				ele2=line2.split('\t')
				if ele2[0] in f_hash_p.keys():
                               		e2=ele2[1:]
                               		content='\t'.join(e2)
                               		o2.write(f_hash_p[ele2[0]]+'\t'+content)
			while True:
				line3=fs.readline()
				if not line3:break
				ele3=line3.split('\t')	
				if ele3[0] in f_hash_s.keys():
                               		e3=ele3[1:]
                                	content='\t'.join(e3)
                                	o3.write(f_hash_s[ele3[0]]+'\t'+content)
				
		end=time.clock()
		print 'Running the '+ each_dir+'  uses: '+str(end-start)+'(s)'
		print  'The project: '+each_dir+' ends!\n'
	
	if not os.path.exists('../../Result/1.start_stat/Gene/Out_y') and re.search('g',level):
		os.makedirs('../../Result/1.start_stat/Gene/Out_y',0755)
	if not os.path.exists('../../Result/1.start_stat/KO/Out_y') and level=='ko':
                os.makedirs('../../Result/1.start_stat/KO/Out_y',0755)
	if not os.path.exists('../../Result/1.start_stat/Taxo/genus/Out_y') and level=='ta':
                os.makedirs('../../Result/1.start_stat/Taxo/genus/Out_y',0755)
	if not os.path.exists('../../Result/1.start_stat/Taxo/phylum/Out_y') and level=='ta':
                os.makedirs('../../Result/1.start_stat/Taxo/phylum/Out_y',0755)
	if not os.path.exists('../../Result/1.start_stat/Taxo/species/Out_y') and level=='ta':
                os.makedirs('../../Result/1.start_stat/Taxo/species/Out_y',0755)

	print 'Anything is done!'

