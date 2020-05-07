#!/bin/sh

if [ -z "$CHEMKIN_BIN" ]; then
  module load ansys/19.0
  source chemkinpro_setup.ksh
fi

chem -i ../chem.inp -d ../therm.dat -o ./chem.out
aurora < aurora.inp > aurora.out
python ./outIDT.py
echo

