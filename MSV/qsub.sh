qsub -cwd  -V -q alpha.q -l h_vmem=15G -pe smp 4 run.sh
