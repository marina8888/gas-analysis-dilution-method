#!/bin/sh

if [ -z "$CHEMKIN_BIN" ]; then
  module load ansys/19.0
  source chemkinpro_setup.ksh
fi

chem -i ../chem.inp -d ../therm.dat -o ./chem.out
tran -i ../tran.dat > tran.out
premix < premix.inp > premix.out
python ./outSummary.py
echo

