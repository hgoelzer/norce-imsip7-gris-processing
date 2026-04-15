#!/bin/bash
# Rename back to protect conventions

#exp=greenland_16km_v01_m06_r02_f85_o25
exp=$1

# special case ctrl
if [[ "$exp" == *"ctrl_proj"* ]]; then
    # return standard name
    echo ctrl_proj
elif [[ "$exp" == *"hist"* ]]; then
    # return standard name
    echo historical
else
    # standard exp name
    OLDIFS=$IFS
    IFS=_
    set -- $exp
    #echo ${exp}
    agcmnum=${4:1}
    arcmnum=${5:1}
    ascenum=${6:1}
    aosensnum=${7:1}
    IFS=$OLDIFS

    #echo $agcmnum $arcmnum $ascenum $aosensnum

    #arcmnum=02
    #agcmnum=12
    #ascenum=85
    #aosensnum=25

    # Mapping of RCMS and GCMS
    # hybrid 
    declare -A GCMnames
    GCMnames=( ["CESM2"]="01" ["CNRM-CM6-1"]="02" ["CNRM-ESM2-1"]="03" ["IPSL-CM6A-LR"]="04" ["MPI-ESM1-2-HR"]="05" ["NorESM2-MM"]="06" ["UKESM1-0-LL"]="07" ["CESM2-WACCM"]="08" )
    declare -A SCENnames
    SCENnames=( ["ssp585"]="85" ["ssp245"]="45" ["ssp126"]="26" ["rcp85"]="85" ["rcp26"]="26" )
    # check we have a results
    if [ "${#SCENnames[@]}" -eq 0 ]; then
	echo 'Error'
	exit 0
    fi
    declare -A RCMnames 
    RCMnames=( ["MARv3.12"]="01" ["RACMO2.3p2"]="02" )
    declare -A OSENSnames
    OSENSnames=( ["med"]="50" ["high"]="25" ["low"]="75" ["p05"]="05" ["p95"]="95" ["ooo"]="00" )
    
    ##### parameters
    AGCM="${GCMnames[$agcmnum]}"
    ASCEN="${SCENnames[$ascenum]}"
    ARCM="${RCMnames[$arcmnum]}"
    AOSENS="${OSENSnames[$aosensnum]}"

    ### protect name
    #CNRM-CM6_ssp585_MARv3.12_high
    echo ${AGCM}_${ASCEN}_${ARCM}_${AOSENS}

fi
