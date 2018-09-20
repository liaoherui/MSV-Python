import os

if os.path.exists('../../Result/1.start_stat/convert.R'):
	os.chdir('../../Result/1.start_stat')
	os.system('Rscript convert.R')


