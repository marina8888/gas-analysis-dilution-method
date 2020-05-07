#!/bin/bash
#$ -S /bin/bash
#$ -P general
#$ -jc dma.A
#$ -pe impi_fillup 16
#$ -l h_vmem=300g
#$ -l h_rt=2:00:00
#$
python ./Main5-forLinux.py
echo