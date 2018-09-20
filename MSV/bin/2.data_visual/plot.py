import os
import re
import sys
import getopt

#this function is used to group country to finish the  R script
def Group(array):
        c=0
        string=''
        length=len(array)
        last_e=length-1 
        if length==2:
                string='c(\"'+array[0]+'\",\"'+array[1]+'\"),'
                string=string[:-1]
        else:
                for i in range(0,last_e):
                        for l in range(i+1,last_e+1):
                                string+='c(\"'+array[i]+'\",\"'+array[l]+'\"),'
                string=string[:-1]
        return string


'''------Get Option--------'''
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
        path_box='../../Result/2.data_visual/Gene/Boxplot_Data'
	path_bar='../../Result/2.data_visual/Gene/Barplot_Data'
if level=='ta':
        path_box_g='../../Result/2.data_visual/Taxo/genus/Boxplot_Data'
	path_bar_g='../../Result/2.data_visual/Taxo/genus/Barplot_Data'
	path_box_p='../../Result/2.data_visual/Taxo/phylum/Boxplot_Data'
        path_bar_p='../../Result/2.data_visual/Taxo/phylum/Barplot_Data'
	path_box_s='../../Result/2.data_visual/Taxo/species/Boxplot_Data'
        path_bar_s='../../Result/2.data_visual/Taxo/species/Barplot_Data'
	path_box_ta=[]
	path_bar_ta=[]
	path_box_ta.append(path_box_g)	
	path_box_ta.append(path_box_p)
	path_box_ta.append(path_box_s)
	path_bar_ta.append(path_bar_g)
	path_bar_ta.append(path_bar_p)
	path_bar_ta.append(path_bar_s)
if level=='ko':
        path_box='../../Result/2.data_visual/KO/Boxplot_Data'
	path_bar='../../Result/2.data_visual/KO/Barplot_Data'

'''----Make Output dir-----'''
outdir='../../Result/2.data_visual'
end_dir=''

if level=='ge':
        end_dir=outdir+'/Gene/img'
        if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)
if level=='ta':
        end_dir1=outdir+'/Taxo/genus/img'
	end_dir2=outdir+'/Taxo/phylum/img'
	end_dir3=outdir+'/Taxo/species/img'
        if not (os.path.exists(end_dir1)):
                os.makedirs(end_dir1,0755)
	if not (os.path.exists(end_dir2)):
                os.makedirs(end_dir2,0755)
	if not (os.path.exists(end_dir3)):
                os.makedirs(end_dir3,0755)
	
if level=='ko':
        end_dir=outdir+'/KO/img'
        if not (os.path.exists(end_dir)):
                os.makedirs(end_dir,0755)
pwd=os.getcwd()
o=open(outdir+'/plot.R','w+')
if level=='ge' or level=='ko':
	for filename in os.listdir(path_box):
		os.chdir(pwd)
		f=open(path_box+'/'+filename,'r')
		country=[]
		s=''
		while True:
			line=f.readline()
			line=line.strip()
			ele=line.split('\t')
			if True:break
		country=ele[1:]
		pre=re.split('final',filename)
		prefix=pre[0]
		ID=prefix[:-1]
		bar_name=prefix+'final_report.xls'
		if not len(country)==1:
			s=Group(country)
			if s=='':
				print filename+' is not right!'
				continue
		
		o.write('library(ggplot2)\nlibrary(reshape2)\nlibrary(ggsignif)\n')
		o.write('pdf(\"Gene/img/'+ID+'.pdf\",family=\"GB1\")\n')
		o.write('profile_text <- read.table(\"'+path_box+'/'+filename+'\", header=T, row.names=1, quote=\"\",sep=\"\\t\", check.names=F)\n')
		o.write('data_m <- melt(profile_text)\n')
		o.write('p <- ggplot(data_m, aes(x=variable, y=value),color=variable)+geom_boxplot(aes(fill=factor(variable)))+theme(axis.text.x=element_text(angle=50,hjust=0.5, vjust=0.5))\n')
		o.write('p<-p+xlab(\"'+ptype+'\")+ylab(\"Relative    Abundance(log10)\")+ggtitle(\"GeneID:'+ID+'\")+guides(fill=guide_legend(title="Country"))\n')
		if len(country)==1:
			o.write('p+stat_summary(fun.y=\"mean\", geom=\"point\", shape=23, size=3, fill=\"white\")\n\n')	
		else:
				
			o.write('p+stat_summary(fun.y=\"mean\", geom=\"point\", shape=23, size=3, fill=\"white\")+geom_signif(comparisons = list('+s+'), test = wilcox.test, step_increase = 0.2)\n\n')	
		o.write('library(ggthemes)\n')
		o.write('data<-read.table(\"'+path_bar+'/'+bar_name+'\", header=T, quote=\"\",sep=\"\\t\", check.names=F)\n')
		o.write('mydata<-melt(data,id.vars=\"'+ptype+'\",variable.name=\"Data_type\",value.name=\"Sample_Numbers\")\n')
		o.write('q<-ggplot(mydata,aes('+ptype+',Sample_Numbers,fill=Data_type))+geom_bar(stat=\"identity\",position=\"dodge\")+theme_wsj()+scale_fill_wsj(\"rgby\", \"\")+theme(axis.ticks.length=unit(0.5,\'cm\'))+guides(fill=guide_legend(title=NULL))+ggtitle(\"The Gene_ID:'+ID+'\")+theme(axis.title = element_blank())+geom_text(aes(label = Sample_Numbers),  colour = \"black\", position = position_dodge(.9), size = 5)\n')
		o.write('q\n')
		o.write('dev.off()\n\n\n')

if level=='ta':
	for path_box in path_box_ta:
		for filename in os.listdir(path_box):	
			os.chdir(pwd)
	                f=open(path_box+'/'+filename,'r')
	                country=[]
	                s=''
	                while True:
	                        line=f.readline()
	                        line=line.strip()
	                        ele=line.split('\t')
	                        if True:break
	                country=ele[1:]
	                pre=re.split('final',filename)
	                prefix=pre[0]
	                prefix=prefix[:-1]
	   
	                bar_name=prefix+'_final_report.xls'
	                if not len(country)==1:
        	                s=Group(country)
	                        if s=='':
	                                print filename+' is not right!'
	                                continue
			
			o.write('library(ggplot2)\nlibrary(reshape2)\nlibrary(ggsignif)\n')
			if re.search('genus',path_box):
		                o.write('pdf(\"Taxo/genus/img/'+prefix+'.pdf\",family=\"GB1\")\n')
			if re.search('phylum',path_box):
				o.write('pdf(\"Taxo/phylum/img/'+prefix+'.pdf\",family=\"GB1\")\n')
			if re.search('species',path_box):
				o.write('pdf(\"Taxo/species/img/'+prefix+'.pdf\",family=\"GB1\")\n')
	                o.write('profile_text <- read.table(\"'+path_box+'/'+filename+'\", header=T, row.names=1, quote=\"\",sep=\"\\t\", check.names=F)\n')
	                o.write('data_m <- melt(profile_text)\n')
	                o.write('p <- ggplot(data_m, aes(x=variable, y=value),color=variable)+geom_boxplot(aes(fill=factor(variable)))+theme(axis.text.x=element_text(angle=50,hjust=0.5, vjust=0.5))\n')
			if re.search('genus',path_box):
		                o.write('p<-p+xlab(\"'+ptype+'\")+ylab(\"Relative    Abundance(log10)\")+ggtitle(\"Taxo(genus):'+prefix+'\")+guides(fill=guide_legend(title="'+ptype+'"))\n')
			if re.search('phylum',path_box):
                                o.write('p<-p+xlab(\"'+ptype+'\")+ylab(\"Relative    Abundance(log10)\")+ggtitle(\"Taxo(phylum):'+prefix+'\")+guides(fill=guide_legend(title="'+ptype+'"))\n')
			if re.search('species',path_box):
                                o.write('p<-p+xlab(\"'+ptype+'\")+ylab(\"Relative    Abundance(log10)\")+ggtitle(\"Taxo(species):'+prefix+'\")+guides(fill=guide_legend(title="'+ptype+'"))\n')

			if len(country)==1:
                        	o.write('p+stat_summary(fun.y=\"mean\", geom=\"point\", shape=23, size=3, fill=\"white\")\n\n')
                	else:
	                        o.write('p+stat_summary(fun.y=\"mean\", geom=\"point\", shape=23, size=3, fill=\"white\")+geom_signif(comparisons = list('+s+'), test = wilcox.test, step_increase = 0.2)\n\n')
	                o.write('library(ggthemes)\n')
			if re.search('genus',path_box):
	        	        o.write('data<-read.table(\"'+path_bar_g+'/'+bar_name+'\", header=T, quote=\"\",sep=\"\\t\", check.names=F)\n')
			if re.search('phylum',path_box):
                                o.write('data<-read.table(\"'+path_bar_p+'/'+bar_name+'\", header=T, quote=\"\",sep=\"\\t\", check.names=F)\n')
			if re.search('species',path_box):
                                o.write('data<-read.table(\"'+path_bar_s+'/'+bar_name+'\", header=T, quote=\"\",sep=\"\\t\", check.names=F)\n')
                	o.write('mydata<-melt(data,id.vars=\"Areas\",variable.name=\"Data_type\",value.name=\"Sample_Numbers\")\n')
	                o.write('q<-ggplot(mydata,aes('+ptype+',Sample_Numbers,fill=Data_type))+geom_bar(stat=\"identity\",position=\"dodge\")+theme_wsj()+scale_fill_wsj(\"rgby\", \"\")+theme(axis.ticks.length=unit(0.5,\'cm\'))+guides(fill=guide_legend(title=NULL))+ggtitle(\"The Taxo:'+prefix+'\")+theme(axis.title = element_blank())+geom_text(aes(label = Sample_Numbers),  colour = \"black\", position = position_dodge(.9), size = 5)\n')
        	        o.write('q\n')
               		o.write('dev.off()\n\n\n')
