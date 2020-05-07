#!/bin/bash
#$ -S /bin/bash
#$ -P general
#$ -jc dma.A
#$ -pe impi_fillup 16
#$ -l h_vmem=300g
#$ -l h_rt=1:00:00
#$ -N chemkinpro190
#$ -cwd
. /etc/profile.d/modules.sh
module load ansys/19.0
source chemkinpro_setup.ksh
chem -i mech.inp -o mech.out -d thermo.dat
tran -i transport.dat > tran.out
CKReactorFreelyPropagatingFlame< input.inp > solution.out

GetSolution
CKSolnTranspose