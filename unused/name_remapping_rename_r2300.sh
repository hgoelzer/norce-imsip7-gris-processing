#!/bin/bash

# NORCE
norce=/nird/projects/NS8006K/users/heig/MIPS/PROTECT-GrIS/norce-ismip6-gris-processing/Models/NORCE
# PROTECT archive
#norce=/nird/datalake/NS8085K/PROTECT-GrIS/Results/protect-gris-results-processing/Archive_sc/Data/SC_GIC1_OBS0/NORCE

models=`ls $norce | grep CISM16tc-`

for model in $models; do
    echo $model
    
    ## processed
    apath=$norce/$model
    echo $apath
    
    cd ${apath}
    rename "rcp85_" "rcp85-r2300_" *
    rename "ssp126_" "ssp126-r2300_" *
    rename "ssp245_" "ssp245-r2300_" *
    rename "ssp585_" "ssp585-r2300_" *
    #rename "ctrl-proj" "ctrl-proj-r2300" *
    #rename "_r2300" "" *


    exps=`ls ${apath}`
    for exp in $exps; do
	echo renaming in ${exp}
	cd ${apath}/${exp}
	rename "rcp85_" "rcp85-r2300_" *
	rename "ssp126_" "ssp126-r2300_" *
	rename "ssp245_" "ssp245-r2300_" *
	rename "ssp585_" "ssp585-r2300_" *
	#rename "ctrl_proj" "ctrl-proj-r2300" *

    done

done
