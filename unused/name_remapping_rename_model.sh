#!/bin/bash

norce=/nird/projects/NS8006K/users/heig/MIPS/PROTECT-GrIS/norce-ismip6-gris-processing/Models/NORCE

# Also change below!
model=CISM08c-MAR312-p25
model_new=CISM08-MAR312-p25
    
## processed
#apath=$norce/$model_new
apath=$norce/$model
echo $apath

cd ${apath}

exps=`ls ${apath}`
for exp in $exps; do
    echo renaming in ${exp}
    cd ${apath}/${exp}
    rename "CISM08c-" "CISM08-" *.nc    
done

# rename model
cd $norce
mv $model $model_new
