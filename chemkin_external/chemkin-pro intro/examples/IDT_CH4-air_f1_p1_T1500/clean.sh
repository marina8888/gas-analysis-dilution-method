#!/bin/sh
read -p "Input yes if cleanup is OK: " ans
case $ans in
  yes)
    rm -f -r *.out *.asc *.csv idt_crnt.inp *.zip *.txt *.ckcsv dirp* *.plt
    echo 'Cleanup has been DONE.'
    break
    ;;
  *)
    echo 'Cleanup has been CANCELED.'
    ;;
esac

