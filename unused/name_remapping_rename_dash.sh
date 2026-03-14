#!/bin/bash

norce=/nird/projects/NS8006K/users/heig/MIPS/PROTECT-GrIS/norce-ismip6-gris-processing/Models/NORCE

models=`ls $norce`

for model in $models; do
    echo $model
    
    ## processed
    apath=$norce/$model
    echo $apath
    
    cd ${apath}
    rename "n-ssp" "n_ssp" *
    rename "R-ssp" "R_ssp" *
    rename "2-ssp" "2_ssp" *
    rename "o-ssp" "o_ssp" *
    rename "3-rcp" "3_rcp" *
    rename "1-rcp" "1_rcp" *
    rename "5-rcp" "5_rcp" *
    rename "6-rcp" "6_rcp" *
    rename "M-rcp" "M_rcp" *
    rename "S-rcp" "S_rcp" *
    rename "R-rcp" "R_rcp" *
    rename "6-ssp" "6_ssp" *
    rename "M-ssp" "M_ssp" *
    rename "ctrl_proj" "ctrl-proj" *


    exps=`ls ${apath}`
    for exp in $exps; do
	echo renaming in ${exp}
	cd ${apath}/${exp}
	rename "n-ssp" "n_ssp" *.nc
	rename "R-ssp" "R_ssp" *.nc
	rename "2-ssp" "2_ssp" *.nc
	rename "o-ssp" "o_ssp" *.nc
	rename "1-rcp" "1_rcp" *.nc
	rename "3-rcp" "3_rcp" *.nc
	rename "5-rcp" "5_rcp" *.nc
	rename "6-rcp" "6_rcp" *.nc
	rename "M-rcp" "M_rcp" *.nc
	rename "S-rcp" "S_rcp" *.nc
	rename "R-rcp" "R_rcp" *.nc
	rename "6-ssp" "6_ssp" *.nc
	rename "M-ssp" "M_ssp" *.nc
	rename "ctrl_proj" "ctrl-proj" *


    done

done
