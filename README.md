# norce-ismip7-gris-processing
CISM GrIS postprocessing for ISMIP7 type projections

## renaming ISMIP7 conventions
### python env
conda activate nc (on nird!)

### scalar processing
ISMIP7_scalar_process.py

### fields
ISMIP7_variables_process.py \
ISMIP7_tavg_variables_process.py \
ISMIP7_g0_variables_process.py


### regrid invividual variables
regrid_exp.sh

### All in one regridding
meta_regrid_exp.sh \
&nbsp; calls regrid_exp_func.sh \
&nbsp;&nbsp;  calls regrid1_CISMg02ISMIP7_ycon.sh, regrid1_CISM2ISMIP7_ycon.sh


## All in one processing
### Set it up in
setup_params.py
### run
python meta_ISMIP7_process.py


## File renaming
meta_name_remapping_norce.sh \
&nbsp;  name_remapping_norce_func.sh \
&nbsp;  name_remapping_norce_func_ext.sh \
&nbsp;  name_remapping_norce_func_r2300.sh \
&nbsp;&nbsp;    rename_cism2protect.sh


### Final submission in 
Models/

### temporary output after extraction, before regridding
proc/


## Utilities
add_ISMIP7_GrIS_coords.sh
att_process.sh
ncatt.sh
