#!/bin/bash
# Regrid from GrIS CISM to ISMIP grid
# CDO regridding with weights 

set -e 
set -x

cdo_app=cdo

## Path to GDFs
pingdf=/nird/datapeak/NS5011K/CISM/GrIS/Database7/Grid/CDO_gdfs
poutgdf=/nird/datapeak/NS5011K/Remapping/textGDFs
# path to weights
pwgts=/nird/datapeak/NS5011K/Remapping/Weights

# input/output files
infile=$1
outfile=$2

# resolution
inres=${3}000m
outres=${4}000m

# input/output grid description files
ingdf=gdf_CISM3_g1_GrIS_${inres}.txt 
outgdf=gdf_ISMIP7_GrIS_${outres}.txt

#### All in one 
#$cdo_app -L -remapycon,${outgdfs}/${outgdf} -setmisstoc,0 -setgrid,${ingdfs}/${ingdf} ${infile} ${outfile}

### With weights file
wgts=weights_ycon_c${inres}_e${outres}.nc
# produce remap weights file if needed
if [ ! -e ${pwgts}/${wgts} ]; then
    #$cdo_app -L -genycon,${poutgdf}/${outgdf} -setmisstoc,0 -setgrid,${pingdf}/${ingdf} ${infile} ${pwgts}/${wgts} 2> /dev/null
    $cdo_app -L -genycon,${poutgdf}/${outgdf} -setgrid,${pingdf}/${ingdf} ${infile} ${pwgts}/${wgts} 2> /dev/null
fi
# remap with predefined weights
#$cdo_app -L -remap,${poutgdf}/${outgdf},${pwgts}/${wgts} -setmisstoc,0 -setgrid,${pingdf}/${ingdf} ${infile} ${outfile} 2> /dev/null
$cdo_app -L -remap,${poutgdf}/${outgdf},${pwgts}/${wgts} -setgrid,${pingdf}/${ingdf} ${infile} ${outfile} 2> /dev/null

# remove grid info to save space
ncks -C -O -x -v lat,lon,lat_bnds,lon_bnds ${outfile} ${outfile}

# add xy axis 
#./add_ISMIP7_GrIS_coords.sh ${outfile} $4

