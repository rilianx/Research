#!/bin/bash
For ($i=1; $i -le 40; $i++) {./feg 5 ../Instancias/CVS/3-3/data3-3-$i.dat 0 --FERG 1 > tmp.txt; get-content tmp.txt -Tail 1 }


