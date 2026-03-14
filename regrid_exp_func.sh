#!/bin/bash
# Regrid GrIS experiment from CISM to ISMIP grid
# Skip non-existing infiles and existing outfiles

set -x
#set -e

enspath=$1
aexp=$2
inres=$3
outpath=$4
amodel=$5
outres=$6


# Set up
mkdir -p ${outpath}/${amodel}/${aexp}

# regrid output
#for avar in lithk orog base topg litemptop litempbotgr litempbotfl sftgif sftgrf sftflf hfgeoubed; do
for avar in lithk orog base topg sftgif sftgrf sftflf; do
    infile=${enspath}/${aexp}/${avar}_GrIS_NORCE_${amodel}_${aexp}.nc
    outfile=${outpath}/${amodel}/${aexp}/${avar}_GrIS_NORCE_${amodel}_${aexp}.nc
    if [ -e $infile ] && [ ! -e $outfile ]; then
	./regrid1_CISM2ISMIP7_ycon.sh ${infile} ${outfile} ${inres} ${outres}
    fi
done

# regrid tavg
for avar in acabf libmassbfgr libmassbffl licalvf lifmassbf ligroundf; do
    infile=${enspath}/${aexp}/${avar}_GrIS_NORCE_${amodel}_${aexp}.nc
    outfile=${outpath}/${amodel}/${aexp}/${avar}_GrIS_NORCE_${amodel}_${aexp}.nc
    if [ -e $infile ] && [ ! -e $outfile ]; then
	./regrid1_CISM2ISMIP7_ycon.sh ${infile} ${outfile} ${inres} ${outres}
    fi
done

# regrid g0
for avar in xvelsurf yvelsurf xvelbase yvelbase xvelmean yvelmean strbasemag; do
    infile=${enspath}/${aexp}/${avar}_GrIS_NORCE_${amodel}_${aexp}.nc
    outfile=${outpath}/${amodel}/${aexp}/${avar}_GrIS_NORCE_${amodel}_${aexp}.nc
    if [ -e $infile ] && [ ! -e $outfile ]; then
	./regrid1_CISMg02ISMIP7_ycon.sh ${infile} ${outfile} ${inres} ${outres}
    fi
done
