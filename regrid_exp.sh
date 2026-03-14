#!/bin/bash
# Regrid AIS experiment from CISM to ISMIP6 grid

#set -x
set -e

amodel='CISM3-MAR364-ERA-t1'
inres='08'
outres='08' # match to target 2d output, typically higher than model res

inpath=/projects/NS8085K/users/heig/MIPS/ISMIP6-AIS-2300/norce-ismip6-ais-processing/proc/NORCE/${amodel}

outpath=/projects/NS8085K/users/heig/MIPS/ISMIP6-AIS-2300/norce-ismip6-ais-processing/Models/NORCE

aexp=ctrlAE 


# Set up
mkdir -p ${outpath}/${amodel}/${aexp}_${outres}

## regrid output
#for avar in lithk orog base topg litemptop litempbotgr litempbotfl sftgif sftgrf sftflf hfgeoubed; do
#    infile=${inpath}/${aexp}/${avar}_AIS_NORCE_${amodel}_${aexp}.nc
#    outfile=${outpath}/${amodel}/${aexp}_${outres}/${avar}_AIS_NORCE_${amodel}_${aexp}.nc
#    ./regrid1_CISM2ISMIP6_ycon.sh ${infile} ${outfile} ${inres} ${outres}
#done

# regrid tavg
#for avar in acabf libmassbfgr libmassbffl licalvf lifmassbf ligroundf; do
for avar in licalvf; do
    infile=${inpath}/${aexp}/${avar}_AIS_NORCE_${amodel}_${aexp}.nc
    outfile=${outpath}/${amodel}/${aexp}_${outres}/${avar}_AIS_NORCE_${amodel}_${aexp}.nc
    ./regrid1_CISM2ISMIP6_ycon.sh ${infile} ${outfile} ${inres} ${outres}
done

## regrid g0
#for avar in xvelsurf yvelsurf xvelbase yvelbase xvelmean yvelmean strbasemag; do
#    infile=${inpath}/${aexp}/${avar}_AIS_NORCE_${amodel}_${aexp}.nc
#    outfile=${outpath}/${amodel}/${aexp}_${outres}/${avar}_AIS_NORCE_${amodel}_${aexp}.nc
#    ./regrid1_CISMg02ISMIP6_ycon.sh ${infile} ${outfile} ${inres} ${outres}
#done
