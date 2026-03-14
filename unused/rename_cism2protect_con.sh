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

    cmip5=("01" "02" "03" "04" "05" "06")
    cmip6=("07" "08" "09" "10" "11" "12" "13" "14" "15")
    # Mapping of RCMS and GCMS
    declare -A GCMnames
    # Heikos runs
    #GCMnames=( ["01"]="MIROC5" ["02"]="NorESM1" ["03"]="HadGEM2-ES" ["04"]="IPSL-CM5-MR" ["05"]="CSIRO-Mk3.6" ["06"]="ACCESS1.3" ["07"]="CNRM-CM6" ["08"]="UKESM1-0-LL-Robin" ["09"]="CESM2-Leo" ["10"]="CNRM-ESM2" ["11"]="MPI-ESM1-2-HR" ["12"]="CESM2-CMIP6" )
    # Charlottes runs
    #GCMnames=( ["01"]="MIROC5" ["02"]="NorESM1" ["03"]="HadGEM2-ES" ["04"]="IPSL-CM5-MR" ["05"]="CSIRO-Mk3.6" ["06"]="ACCESS1.3" ["07"]="CNRM-CM6" ["08"]="UKESM1-0-LL-Robin" ["09"]="CESM2-Leo" ["10"]="CNRM-ESM2" ["11"]="MPI-ESM1-2-HR" ["12"]="IPSL-CM6A-LR" ["13"]="NorESM2" ["14"]="CESM2-CMIP6" ["15"]="UKESM1-0-LL-CMIP6")
    # Same order as Charlotte but With final names
    GCMnames=( ["01"]="MIROC5" ["02"]="NorESM1" ["03"]="HadGEM2-ES" ["04"]="IPSL-CM5-MR" ["05"]="CSIRO-Mk3.6.0" ["06"]="ACCESS1.3" ["07"]="CNRM-CM6-1" ["08"]="UKESM1-0-LL-Robin" ["09"]="CESM2-Leo" ["10"]="CNRM-ESM2-1" ["11"]="MPI-ESM1-2-HR" ["12"]="IPSL-CM6A-LR" ["13"]="NorESM2-MM" ["14"]="CESM2" ["15"]="UKESM1-0-LL")
    declare -A SCENnames
    if [[ " ${cmip5[*]} " =~ " ${agcmnum} " ]]; then
	SCENnames=( ["85"]="rcp85" ["26"]="rcp26" )
    fi
    if [[ " ${cmip6[*]} " =~ " ${agcmnum} " ]]; then
	SCENnames=( ["85"]="ssp585" ["45"]="ssp245" ["26"]="ssp126" )
    fi
    # check we have a results
    if [ "${#SCENnames[@]}" -eq 0 ]; then
	echo 'Error'
	exit 0
    fi
    declare -A RCMnames 
    RCMnames=( ["01"]="MARv3.9" ["02"]="MARv3.12" ["03"]="RACMO2.3p2" )
    declare -A OSENSnames
    OSENSnames=( ["50"]="p50" ["75"]="p75" ["25"]="p25" ["05"]="p05" ["95"]="p95" )
    #OSENSnames=( ["50"]="p50" ["75"]="p25" ["25"]="p75" ["05"]="p05" ["95"]="p95" )

    ##### parameters
    AGCM="${GCMnames[$agcmnum]}"
    ASCEN="${SCENnames[$ascenum]}"
    ARCM="${RCMnames[$arcmnum]}"
    AOSENS="${OSENSnames[$aosensnum]}"

    ### protect name
    #CNRM-CM6_ssp585_MARv3.12_high
    echo ${AGCM}_${ASCEN}_${ARCM}_${AOSENS}

fi
