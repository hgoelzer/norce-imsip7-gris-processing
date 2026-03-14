#!/bin/bash
# Rename a batch of files

# A. Find existing exps

# Heiko
#amodel=CISM16-MAR39-p50
#amodel=CISM08-MAR39-p50
#amodel=CISM04-MAR39-p50
#amodel=CISM02-MAR39-p50

# Charlotte
#amodel=CISM04-MAR312-p25
#amodel=CISM04-MAR312-p50
#amodel=CISM04-MAR312-p75
#amodel=CISM08-MAR312-p25
#amodel=CISM08-MAR312-p50
#amodel=CISM08-MAR312-p75
#amodel=CISM16-MAR312-p25
#amodel=CISM16-MAR312-p50
#amodel=CISM16-MAR312-p75

#exps=`ls Models/NORCE/${amodel}/`
#
#for exp in $exps; do
#    echo "## Trying " $exp
#    ./name_remapping_norce_func.sh $amodel $exp
#done


# B. Specify individuals
#amodel=CISM04-MAR39-p50
#./name_remapping_norce_func.sh $amodel greenland_04km_v04_m07_r01_f26_o25
#./name_remapping_norce_func.sh $amodel greenland_04km_v04_m07_r01_f26_o75

#amodel=CISM08-MAR39-p50
#./name_remapping_norce_func.sh $amodel greenland_08km_v04_m11_r02_f85_o50
#./name_remapping_norce_func.sh $amodel greenland_08km_v04_m09_r01_f85_o25
#./name_remapping_norce_func.sh $amodel greenland_08km_v04_m07_r02_f85_o05
#./name_remapping_norce_func.sh $amodel greenland_08km_v04_m08_r02_f85_o05

#amodel=CISM16-MAR39-p50
#./name_remapping_norce_func.sh $amodel hist
#./name_remapping_norce_func.sh $amodel greenland_04km_v04_m01_r01_f26_o05
#./name_remapping_norce_func.sh $amodel greenland_04km_v04_m01_r01_f26_o25

#./name_remapping_norce_func.sh CISM04-MAR312-p25 greenland_04km_v01_ctrl_proj
#./name_remapping_norce_func.sh CISM04-MAR312-p50 greenland_04km_v01_ctrl_proj
#./name_remapping_norce_func.sh CISM04-MAR312-p75 greenland_04km_v01_ctrl_proj
#./name_remapping_norce_func.sh CISM08-MAR312-p25 greenland_08km_v01_ctrl_proj
#./name_remapping_norce_func.sh CISM08-MAR312-p50 greenland_08km_v01_ctrl_proj
#./name_remapping_norce_func.sh CISM08-MAR312-p75 greenland_08km_v01_ctrl_proj
#./name_remapping_norce_func.sh CISM16-MAR312-p25 greenland_16km_v01_ctrl_proj
#./name_remapping_norce_func.sh CISM16-MAR312-p50 greenland_16km_v01_ctrl_proj
#./name_remapping_norce_func.sh CISM16-MAR312-p75 greenland_16km_v01_ctrl_proj


## long repeat runs to 2300
#amodel=CISM16-MAR39-p50
#exps=`ls Models/NORCE/${amodel}/ | grep greenland`
#
#echo $exps
#for exp in $exps; do
#    echo "## Trying " $exp
#    ./name_remapping_norce_func_r2300.sh  $amodel $exp
#done
##./name_remapping_norce_func_r2300.sh CISM16-MAR39-p50 greenland_16km_v04_ctrl_proj



## consistent kappa 39
##amodel=CISM04c-MAR39-p50
##amodel=CISM04c-MAR39-p25
##amodel=CISM04c-MAR39-p75
##amodel=CISM04c-MAR39-p05
##amodel=CISM04c-MAR39-p95
#
##amodel=CISM08c-MAR39-p50
##amodel=CISM08c-MAR39-p25
##amodel=CISM08c-MAR39-p75
##amodel=CISM08c-MAR39-p05
##amodel=CISM08c-MAR39-p95
#
##amodel=CISM16tc-MAR39-p50
##amodel=CISM16tc-MAR39-p25
##amodel=CISM16tc-MAR39-p75
##amodel=CISM16tc-MAR39-p05
#amodel=CISM16tc-MAR39-p95
#
#
##exps=`ls Models/NORCE/${amodel}/ | grep -e greenland`
##exps=`ls Models/NORCE/${amodel}/ | grep hist`
#exps=`ls Models/NORCE/${amodel}/ | grep -e greenland -e hist`
#
#echo $exps
#for exp in $exps; do
#    echo "## Trying " $exp
#    ./name_remapping_norce_func_con.sh  $amodel $exp
#done

# consistent kappa
#amodel=CISM16c-MAR312-p50
#amodel=CISM16c-MAR312-p25
#amodel=CISM16c-MAR312-p75
#amodel=CISM16c-MAR312-p05
#amodel=CISM16c-MAR312-p95
#exps=`ls Models/NORCE/${amodel}/ | grep greenland`

#echo $exps
#for exp in $exps; do
#    echo "## Trying " $exp
#    ./name_remapping_norce_func_charlotte.sh  $amodel $exp
#done



# SDBN1/MARv3.13 ext2300
#amodel=CISM16x-MAR312-p50
#exps=`ls Models/NORCE/${amodel}`
#echo $exps
#for exp in $exps; do
#    echo "## Trying " $exp
#    ./name_remapping_norce_func_charlotte_plus.sh  $amodel $exp
#done
#amodel=CISM16x-MAR312-p25
#exps=`ls Models/NORCE/${amodel}`
#echo $exps
#for exp in $exps; do
#    echo "## Trying " $exp
#    ./name_remapping_norce_func_charlotte_plus.sh  $amodel $exp
#done
#amodel=CISM16x-MAR312-p75
#exps=`ls Models/NORCE/${amodel}`
#echo $exps
#for exp in $exps; do
#    echo "## Trying " $exp
#    ./name_remapping_norce_func_charlotte_plus.sh  $amodel $exp
#done
#amodel=CISM16x-MAR312-p05
#exps=`ls Models/NORCE/${amodel}`
#echo $exps
#for exp in $exps; do
#    echo "## Trying " $exp
#    ./name_remapping_norce_func_charlotte_plus.sh  $amodel $exp
#done
amodel=CISM16x-MAR312-p95
exps=`ls Models/NORCE/${amodel}`
echo $exps
for exp in $exps; do
    echo "## Trying " $exp
    ./name_remapping_norce_func_charlotte_plus.sh  $amodel $exp
done


# Separate extension Charlotte
#./name_remapping_norce_func_charlotte.sh  CISM04e-MAR312-p50 greenland_04km_v01_m12_r02_f85_o50
#./name_remapping_norce_func_charlotte.sh  CISM04e-MAR312-p50 hist
#./name_remapping_norce_func_charlotte_e2200.sh  CISM04e-MAR312-p50 greenland_04km_v01_m12_r02_f85_o50_ext
#./name_remapping_norce_func_charlotte.sh  CISM04e-MAR312-p25 greenland_04km_v01_m12_r02_f85_o25
#./name_remapping_norce_func_charlotte.sh  CISM04e-MAR312-p25 hist
#./name_remapping_norce_func_charlotte_e2200.sh  CISM04e-MAR312-p25 greenland_04km_v01_m12_r02_f85_o25_ext
#./name_remapping_norce_func_charlotte.sh  CISM04e-MAR312-p75 greenland_04km_v01_m12_r02_f85_o75
#./name_remapping_norce_func_charlotte.sh  CISM04e-MAR312-p75 hist
#./name_remapping_norce_func_charlotte_e2200.sh  CISM04e-MAR312-p75 greenland_04km_v01_m12_r02_f85_o75_ext
#./name_remapping_norce_func_charlotte.sh  CISM04e-MAR312-p05 greenland_04km_v01_m12_r02_f85_o05
#./name_remapping_norce_func_charlotte.sh  CISM04e-MAR312-p05 hist
#./name_remapping_norce_func_charlotte_e2200.sh  CISM04e-MAR312-p05 greenland_04km_v01_m12_r02_f85_o05_ext
#./name_remapping_norce_func_charlotte.sh  CISM04e-MAR312-p95 greenland_04km_v01_m12_r02_f85_o95
#./name_remapping_norce_func_charlotte.sh  CISM04e-MAR312-p95 hist
#./name_remapping_norce_func_charlotte_e2200.sh  CISM04e-MAR312-p95 greenland_04km_v01_m12_r02_f85_o95_ext

