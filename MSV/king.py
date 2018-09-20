#authors: liaoherui@mail.dlut.edu.cn
import re 
import os
import sys

conf={}
pwd=os.getcwd()


f=open('config.txt','r')
while True:
	line=f.readline()
	if re.search('^#',line) or re.search('^\n',line) or re.search('^ ',line) :continue
	if not line :break	
	line=line.strip()
	line=re.sub('#.*','',line)
#	if re.search('^info'):
		

	ele=re.split('=',line)	
	i=0
	for e in ele:
		e=e.strip()	
		ele[i]=e
		i+=1
	if ele[1]:
		conf[ele[0]]=ele[1]
#print conf['info']
#exit()
if re.search(' ',conf['info']):
	conf['info']=re.sub(' ','_',conf['info'])

if 'stat' not in  conf:
	print 'You must input the [stat] parameters of the config.txt!Please finish and run again!'
	exit()

'''----------stat 0----------'''
if conf['stat']=='0' or conf['stat']=='all':
	if 'phenotype' not in conf:
		print 'You must input the [phenotype] parameters of the config.txt!Please finish and run again!'
		exit()
	elif conf['phenotype'].strip()=='':
		print 'You must input the [phenotype] parameters of the config.txt!Please finish and run again!'
		exit()
	if 'ptype' not in conf:
                print 'You must input the [ptype] parameters of the config.txt!Please finish and run again!'
                exit()
        elif conf['ptype'].strip()=='':
                print 'You must input the [ptype] parameters of the config.txt!Please finish and run again!'
                exit()
#	print 'Stat phenotype of all sample  is starting......'
	os.chdir(pwd+'/bin/0.stat_phenotype')
	os.system('python2.7 stat_All.py -p '+conf['phenotype']+' -t '+conf['ptype']+' -i '+conf['info'])
	os.chdir(pwd+'/Result/0.stat_phenotype')
	if os.path.exists('Report_All.xls'):
		print '1.1_Congratulations! Stat phenotype of all sample is done!'
	if not (os.path.exists('Report_by_'+conf['ptype'])):
		os.makedirs('Report_by_'+conf['ptype'],0755)
	os.chdir(pwd+'/bin/0.stat_phenotype')
	os.system('python2.7 stat_by_country.py -t '+conf['ptype'])
	os.chdir(pwd+'/Result/0.stat_phenotype/Report_by_'+conf['ptype'])
	if os.listdir('./'):
		print '1.2_Great!Stat phenotype of different '+conf['ptype']+' is done,too!'

'''---------stat 1---------'''
if conf['stat']=='1' or conf['stat']=='all':
	
	if 'level' not in conf or 'your_gene_list' not in conf:
		print 'You are required to give the [level] or [your_gene_list] parameters!Please check and run again!'
		exit()
	elif conf['level'].strip()=='' or conf['your_gene_list'].strip()=='':
		print 'You are required to give the [level] or [your_gene_list] parameters!Please check and run again!'
                exit()	
	os.chdir(pwd+'/bin/1.start_stat')
	os.system('python2.7  filter.py -e '+conf['level']+' -l '+conf['your_gene_list'])
	os.system('python2.7 convert.py')
	#os.chdir(pwd+'/Result/1.start_stat')

	#if os.path.exists('convert.R'):
		#os.system('/home/chenjy/software/Anaconda2/bin/Rscript  convert.R')
		

'''----------stat 2----------'''
if conf['stat']=='2' or conf['stat']=='all':
	#get mean of an individual has more than one sample,now,this step is automatic
	if not conf['out_y_dir']=='' and not conf['phenotype']=='' and conf['level2']=='ge':
		os.chdir(pwd+'/bin/2.data_visual')
		os.system('python2.7  get_mean.py -t '+conf['out_y_dir']+' -p '+conf['phenotype'])
		print 'Removing one individual with many samples  is done!'	
	if not conf['level2']=='':
		os.chdir(pwd+'/bin/2.data_visual')
		os.system('python2.7 map_visual.py -e '+conf['level2']+' -p '+conf['phenotype_dir']+' -o '+conf['out_y_dir']+' -g '+conf['out_y_g']+' -l '+conf['out_y_p']+' -s '+conf['out_y_s']+' -t '+conf['ptype']) #step1 get the aim porfile
		#exit()
		os.system('python2.7 remove_zero_of_columns.py -e '+conf['level2']) #step2 remove 0 columns
		os.system('python2.7 to_NA_r0.py -e '+conf['level2'])	#step3 0.1->NA
		os.system('python2.7 static_0.py -e '+conf['level2'])	#step4 stat for bar_plot
		os.system('python2.7 bar_plot.py -e '+conf['level2']+' -t '+conf['ptype'])	#this step  converts step4 data to bar_plot data
		os.system('python2.7 remove_zero_of_lines.py  -e '+conf['level2']) #step5 remove 0 lines
		os.system('python2.7 num_log10.py -e '+conf['level2'])  #this step converts step5 data to box_plot data
		os.system('python2.7 plot.py -e '+conf['level2']+' -t '+conf['ptype'])   #plot
		os.chdir(pwd+'/Result/2.data_visual')
		if os.path.exists('plot.R'):
	                os.system('/home/liaoherui/anaconda2/bin/Rscript  plot.R')
		
	else:
		print 'The level2 parameter may  be wrong,please check it and run again!'
	
