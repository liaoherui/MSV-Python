import os
import re


fa=open('/mnt/lustre/user/chenjy/GeneAbundance_IGC/Project_7000/liaoherui/MSV/profile/Other_profile/annotation.summary','r')
anno_s={}
while True:
	line=fa.readline()
	if not line:break	
	if re.match('^ID',line):continue
	ele=line.split('\t')
	if not ele[5]=='Unknown':
		anno_s[ele[1]]=ele[5]


fd=open('/mnt/lustre/user/chenjy/GeneAbundance_IGC/Project_7000/liaoherui/2.start_stat/Drug_IGC.xls','r')
drug_IGC={}
while True:
	line=fd.readline()
	if not line:break
	if re.match('^ID',line):continue
	ele=line.split('\t')
	if ele[2] not in drug_IGC.keys():
		drug_IGC[ele[2]]=ele[2]


for key in drug_IGC:
	if key in anno_s:
		print anno_s[key]
	else:
		continue
