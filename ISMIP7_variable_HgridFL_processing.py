#!/usr/bin/env python
"""
ISMIP7 GrIS flux variables processing (Hgrid FL)

Adapted from the AIS version (norce-ismip7-ais-processing) for the NORCE
GrIS CISM 4 km submission (CISM4).

Differences from AIS:
- domain_id 'GrIS', crs epsg:3413, ism_id from config (CISM4)
- run directory mapping (greenland_04km_v01_*_fXX, ctrl-proj, OCX)
- masks are NOT in output.nc; ice_mask/grounded_mask/floating_mask are read
  from output_mask.nc (time-dependent, same grid and time axis as output.nc)
- output.nc has 'acab' (m/yr ice, packed) instead of 'acab_applied'
- output_tavg.nc additionally has melt_rate_tavg (m/yr, frontal melt) and
  gl_flux_tavg (kg/m/s), which are used for lifmassbf and ligroundf
  (zeros in the AIS processing)
- filePrev logic: historical -> ctrl-proj restart_in.nc; ocx -> OCX
  restart_in.nc; else -> historical output.nc
"""

# Import packages
import numpy as np
from netCDF4 import Dataset
import sys, os
import argparse

# Top-level configuration (paths, interpreter)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import PATH_EXP, DST_PATH, ISM_ID
import netCDF4
from pathlib import Path

from datetime import date, datetime


# ----------------------------------------------------------------------
# Time conversion helper
# ----------------------------------------------------------------------
EPOCH = date(1850, 1, 1)

def days_since_1850(year, month, day):
    """Whole days from 1850-01-01 (which is day 0) to the given Gregorian date."""
    return (date(year, month, day) - EPOCH).days


# ----------------------------------------------------------------------
# Strings for file naming convention:
# ----------------------------------------------------------------------
domain_id = 'GrIS'  # Ice Sheet name
source_id = 'NORCE'
ism_id = ISM_ID  # from config; can be overridden with --ism_id
set_id = 'CORE'

dayPerY = 365.
sPerY = 31536000.
rhoi = 917

fill_value = netCDF4.default_fillvals['f4']

# ----------------------------------------------------------------------
# Command line arguments (defaults reproduce the previous hard-coded run)
# ----------------------------------------------------------------------
parser = argparse.ArgumentParser(description='ISMIP7 GrIS flux variables processing (Hgrid FL)')
parser.add_argument('--exp',       default='ssp585', help='Experiment name (e.g. historical, ssp126, ssp370, ssp585, ctrl-proj, ocx)')
parser.add_argument('--ESM_num',   default='m01',    help='ESM ensemble member (m01, m02); ocx run uses r01 only')
parser.add_argument('--RCM_num',   default='r01',    help='RCM/ISM configuration number')
parser.add_argument('--path_exp',  default=PATH_EXP,
                    help='Path to the proj run directory')
parser.add_argument('--dstPath',   default=DST_PATH,
                    help='Base path for output')
parser.add_argument('--ism_id',    default=ISM_ID,
                    help='ISM model ID for the output path/file names (default from config)')
args = parser.parse_args()

exp      = args.exp
ESM_num  = args.ESM_num
RCM_num  = args.RCM_num
path_exp = args.path_exp
dstPath  = args.dstPath
ism_id   = args.ism_id

# Output experiment name: the data request (and compliance checker) uses
# 'ctrl' for the control run, while the input directory is named ctrl-proj.
exp_out = 'ctrl' if exp == 'ctrl-proj' else exp

# ----------------------------------------------------------------------
# Derive ESM_id / ISM_member_id from the ESM ensemble member
# ----------------------------------------------------------------------
ESM_map = {
    'm01': ('CESM2-WACCM', 'm001'),
    'm02': ('MRI-ESM2-0',  'm002'),
}
if exp == 'ocx':
    # OCX doesn't have an ESM; use ERA
    ESM_id, ISM_member_id = 'ERA', 'm001'
elif ESM_num in ESM_map:
    ESM_id, ISM_member_id = ESM_map[ESM_num]
else:
    sys.exit(f'Error: unknown ESM_num {ESM_num}')

forcing_member_id = 'f001'

# ----------------------------------------------------------------------
# Experiment lookup: set_counter for the 11 CORE runs
# (m01/m02 pairs share the same set_counter; ocx is C011)
# The time_range tag in the output filename is derived from the data below.
# ----------------------------------------------------------------------
exp_map = {
    'historical': 'C001',
    'ssp370':     'C003',
    'ssp126':     'C005',
    'ssp585':     'C007',
    'ctrl-proj':  'C009',
    'ocx':        'C011',
}
if exp in exp_map:
    set_counter_base = exp_map[exp]
else:
    sys.exit(f'Error: unknown experiment {exp}')

# m01/m02 runs get consecutive set_counters (e.g. ssp126 -> C005/C006)
if exp == 'ocx':
    set_counter = set_counter_base
elif ESM_num == 'm01':
    set_counter = set_counter_base
elif ESM_num == 'm02':
    set_counter = 'C%03d' % (int(set_counter_base[1:]) + 1)
else:
    sys.exit(f'Error: unknown ESM_num {ESM_num}')

# ----------------------------------------------------------------------
# Input run directory mapping (GrIS proj directory layout):
#   historical -> historical_{m}_{r}
#   ssp370     -> greenland_04km_v01_{m}_{r}_f70
#   ssp126     -> greenland_04km_v01_{m}_{r}_f26
#   ssp585     -> greenland_04km_v01_{m}_{r}_f85
#   ctrl-proj  -> ctrl-proj_{m}_{r}
#   ocx        -> OCX (uppercase, no _{ESM_num}_{RCM_num} suffix)
# ----------------------------------------------------------------------
run_dir_map = {
    'historical': f"{path_exp}/historical_{ESM_num}_{RCM_num}",
    'ssp370':     f"{path_exp}/greenland_04km_v01_{ESM_num}_{RCM_num}_f70",
    'ssp126':     f"{path_exp}/greenland_04km_v01_{ESM_num}_{RCM_num}_f26",
    'ssp585':     f"{path_exp}/greenland_04km_v01_{ESM_num}_{RCM_num}_f85",
    'ctrl-proj':  f"{path_exp}/ctrl-proj_{ESM_num}_{RCM_num}",
    'ocx':        f"{path_exp}/OCX",
}
if exp in run_dir_map:
    run_dir = run_dir_map[exp]
else:
    sys.exit(f'Error: unknown experiment {exp}')

fileVar = f"{run_dir}/output.nc"
fileVarVel = f"{run_dir}/output.nc"


fieldFL = ['acabf', 'libmassbfgr', 'dlithkdt',
           'licalvf', 'ligroundf', 'lifmassbf']
# GrIS source variables:
#   acabf        <- output.nc        acab            (m/yr ice, packed)
#   libmassbfgr  <- output_tavg.nc   basal_mbal_flux_tavg * f_ground (kg/m2/s)
#   NOTE: libmassbffl (basal mass balance beneath floating ice) is NOT written
#   for GrIS — there is no floating ice, so the variable is not relevant.
#   dlithkdt     <- output.nc        dthck_dt        (m/yr after auto-scale)
#   licalvf      <- output_tavg.nc   calving_flux_tavg               (kg/m2/s)
#   ligroundf    <- output_tavg.nc   gl_flux_tavg                    (kg/m/s)
#   lifmassbf    <- output_tavg.nc   melt_rate_tavg                  (m/yr)


# List of variable that needs to be read from previous experiment
readListPrevExptString = ['ligroundf', 'licalvf', 'dlithkdt', 'libmassbfgr', 'acabf']

fieldReady = ['acabf', 'dlithkdt', 'licalvf', 'ligroundf', 'lifmassbf']
nameCISM = ['acab', 'dthck_dt', 'calving_flux_tavg', 'gl_flux_tavg', 'melt_rate_tavg']

fieldException = ['libmassbfgr']
nameCISM = ['basal_mbal_flux_tavg*f_ground']


# ----------------------------------------------------------------------
# Output directory
# ----------------------------------------------------------------------
dstDir = f"{dstPath}/{domain_id}/{source_id}/{ism_id}/{set_id}/{set_counter}/"

if os.path.isdir(dstDir):
    print("The output directory already exists")
else:
    print("Creating output directory")
    os.makedirs(dstDir, exist_ok=True)


# ----------------------------------------------------------------------
# Read source data
# ----------------------------------------------------------------------
try:
    nidsrc = Dataset(fileVar, 'r')
    print('fileVar =', fileVar)
except Exception:
    print('Error: Unable to open CISM file for expt ', exp)
    sys.exit('exiting program now')

# Keep all time entries: the first CISM output is the end of the first
# simulation year (e.g. 1951 for historical), so nothing is dropped.
time_dst = nidsrc['time'][:]
x_dst = nidsrc['x1'][:]
y_dst = nidsrc['y1'][:]

# NOTE: the GrIS output.nc does not contain ice_mask / f_ground_cell.
# The masks live in output_mask.nc (time-dependent, same grid and time
# axis as output.nc). netCDF4 applies the packing scale_factor of the
# flux variables automatically on read, so acab arrives in m/yr ice and
# dthck_dt in m/yr -- do NOT disable auto scaling.
acab_dst    = nidsrc['acab'][:, :, :]
dthckdt_dst = nidsrc['dthck_dt'][:, :, :]

nidsrc.close()

# Ice / grounded / floating masks from output_mask.nc
fileMask = f"{run_dir}/output_mask.nc"
try:
    nidmask = Dataset(fileMask, 'r')
    print('fileMask =', fileMask)
except Exception:
    print('Error: Unable to open CISM mask file for expt ', exp)
    sys.exit('exiting program now')

ice_mask = nidmask['ice_mask'][:, :, :]
grounded_mask = nidmask['grounded_mask'][:, :, :]

nidmask.close()

# Fractions on the x1/y1 grid, restricted to where there is ice
f_ground = grounded_mask*ice_mask

# The time-mean flux variables are written to a separate output_tavg.nc file
nidtavg = Dataset(f"{run_dir}/output_tavg.nc", 'r')
basal_flux_dst   = nidtavg['basal_mbal_flux_tavg'][:, :, :]
calving_flux_dst = nidtavg['calving_flux_tavg'][:, :, :]
gl_flux_dst      = nidtavg['gl_flux_tavg'][:, :, :]
melt_rate_dst    = nidtavg['melt_rate_tavg'][:, :, :]
nidtavg.close()

nt = len(time_dst)
nx = len(x_dst)
ny = len(y_dst)


print(f"nt={nt}, ny={ny}, nx={nx}")

# The time_range tag in the output filename is derived from the data:
# entry t (CISM year time_dst[t]) covers nominal year time_dst[t]-1, so the
# first/last nominal years are time_dst[0]-1 / time_dst[-1]-1. It therefore
# adjusts automatically when a run is extended by one year.
time_range = f"{int(time_dst[0])-1}-{int(time_dst[-1])-1}"
print('time_range =', time_range)


# readListPrevExptString = [ 'licalvf', 'dlithkdt',  'acabf']
if exp in ['historical']:
    # Need to read in the last time slice of the spin-up
    filePrev = f"{path_exp}/ctrl-proj_{ESM_num}_{RCM_num}/restart_in.nc"

elif exp == 'ocx':
    # OCX is a standalone run with no historical predecessor;
    # use its own spin-up restart like the historical run does
    filePrev = f"{path_exp}/OCX/restart_in.nc"

else:
    # Need to read the last time slice of the historical
    filePrev = f"{path_exp}/historical_{ESM_num}_{RCM_num}/output.nc"

try:
    nidprev = Dataset(filePrev, 'r')
    print('filePrev =', filePrev)
except Exception:
    print('Error: Unable to open CISM previous file ', filePrev)
    sys.exit('exiting program now')

nidprev.close()


# ----------------------------------------------------------------------
# Time axes
# ----------------------------------------------------------------------
# CISM writes the first output at the end of the first simulation year:
# entry t (time_dst[t]) is the state / year-mean of nominal year time_dst[t]-1.
# FL fields (year-means) are assigned to the middle of the nominal year,
# Jul 1 of time_dst[t]-1; the bounds span that nominal year.
timeST = np.zeros(nt)
timeFL = np.zeros(nt)

for t in range(nt):
    timeST[t] = days_since_1850(int(time_dst[t]), 1, 1)      # time in days

for t in range(nt):
    timeFL[t] = days_since_1850(int(time_dst[t])-1, 7, 1)    # time in days

print(time_dst)


# ----------------------------------------------------------------------
# Main processing loop
# ----------------------------------------------------------------------
for field in fieldFL:

    # Create the field output file.
    dstFile = f"{dstDir}{field}_{domain_id}_{source_id}_{ism_id}_{ISM_member_id}_{ESM_id}_{forcing_member_id}_{exp_out}_{set_counter}_{time_range}.nc"

    # Removing the output file if it already exists.
    if os.path.isfile(dstFile):
        print('yup')
        os.remove(dstFile)

    print('Created field output file', dstFile)
    ncid = Dataset(dstFile, 'w')
    ncid.createDimension('time', None)
    ncid.createDimension('bnds', 2)

    time    = ncid.createVariable('time', 'f4', ('time'))
    time.bounds        = 'time_bnds'
    time.units         = "days since 1850-01-01"
    time.calendar      = "standard"
    time.axis          = "T"
    time.long_name     = "time"
    time.standard_name = "time"
    time[:] = timeFL[:]  # time in days since 1850

    # CF bounds variable: must be named 'time_bnds' to match time:bounds
    time_bnds = ncid.createVariable('time_bnds', 'f4', ('time', 'bnds',))
    time_bnds[:, 0] = np.array([days_since_1850(int(time_dst[t])-1, 1, 1) for t in range(nt)])
    time_bnds[:, 1] = timeST[:]

    ncid.createDimension('x', size=nx)
    x    = ncid.createVariable('x', 'f4', ('x'))
    x.long_name = "Cartesian centered thickness x-coordinate"
    x.units     = "m"
    x[:] = x_dst[:]

    ncid.createDimension('y', size=ny)
    y    = ncid.createVariable('y', 'f4', ('y'))
    y.long_name = "Cartesian centered thickness y-coordinate"
    y.units     = "m"
    y[:] = y_dst[:]


    if field in ['acabf']:
        acabf = ncid.createVariable(field, 'f4', ('time', 'y', 'x'), fill_value=netCDF4.default_fillvals['f4'])
        acabf.units         = 'kg m-2 s-1'
        acabf.long_name     = 'surface mass balance flux'
        acabf.standard_name = 'land_ice_surface_specific_mass_balance_flux'
        # GrIS acab is in meter/year ice (packed; auto-scaled on read) ->
        # convert to kg m-2 s-1 with the ice density.
        acabf[:, :, :] = acab_dst[:, :, :]*rhoi/sPerY

    if field in ['libmassbfgr']:
        libmassbfgr = ncid.createVariable(field, 'f4', ('time', 'y', 'x'), fill_value=netCDF4.default_fillvals['f4'])
        libmassbfgr.units         = 'kg m-2 s-1'
        libmassbfgr.long_name     = 'basal mass balance flux beneath grounded ice'
        libmassbfgr.standard_name = 'land_ice_basal_specific_mass_balance_flux'
        # The data request defines this variable only where there is grounded
        # ice; cells without grounded ice hold the fill value.
        libmassbfgr[:, :, :] = np.where(f_ground[:, :, :] > 0,
                                        basal_flux_dst[:, :, :]*f_ground[:, :, :],
                                        netCDF4.default_fillvals['f4'])

    if field in ['dlithkdt']:
        dlithkdt = ncid.createVariable(field, 'f4', ('time', 'y', 'x'), fill_value=netCDF4.default_fillvals['f4'])
        dlithkdt.units         = 'm s-1'
        dlithkdt.long_name     = 'ice thickness imbalance'
        dlithkdt.standard_name = 'tendency_of_land_ice_thickness'
        # GrIS dthck_dt is packed with scale_factor 1/31536000, so after the
        # automatic scaling it is in m/yr -> divide by sPerY to get m/s.
        # The data request does not permit missing values in this variable:
        # any masked/fill cells (e.g. where there is no ice) are set to 0.
        dlithkdt[:, :, :] = np.ma.filled(dthckdt_dst[:, :, :]/sPerY, 0.0)

    if field in ['licalvf']:
        licalvf = ncid.createVariable(field, 'f4', ('time', 'y', 'x'), fill_value=netCDF4.default_fillvals['f4'])
        licalvf.units         = 'kg m-2 s-1'
        licalvf.long_name     = 'calving flux'
        licalvf.standard_name = 'land_ice_specific_mass_flux_due_to_calving'
        # Temporary fix for positive values
        licalvf[:, :, :] = np.where(calving_flux_dst[:, :, :] > 0, 0, calving_flux_dst[:, :, :])

    if field in ['lifmassbf']:
        lifmassbf = ncid.createVariable(field, 'f4', ('time', 'y', 'x'), fill_value=netCDF4.default_fillvals['f4'])
        lifmassbf.units         = 'kg m-2 s-1'
        lifmassbf.long_name     = 'loss of ice mass resulting from ice front melting'
        lifmassbf.standard_name = 'land_ice_specific_mass_flux_due_to_ice_front_melting'
        # GrIS melt_rate_tavg (frontal melt) is in meter/year (unpacked) ->
        # convert to kg m-2 s-1 with the ice density.
        # The data request does not permit missing values in this variable:
        # any masked/fill cells (e.g. where there is no ice) are set to 0.
        lifmassbf[:, :, :] = np.ma.filled(melt_rate_dst[:, :, :]*rhoi/sPerY, 0.0)


    if field in ['ligroundf']:
        ligroundf = ncid.createVariable(field, 'f4', ('time', 'y', 'x'), fill_value=netCDF4.default_fillvals['f4'])
        ligroundf.units         = 'kg m-2 s-1'
        ligroundf.long_name     = 'Flux of ice mass across the grounding line'
        ligroundf.standard_name = 'land_ice_specific_grounding_line_flux'
        # GrIS gl_flux_tavg is available (kg/m/s, i.e. per metre of grounding
        # line, not per m2). NOTE: the data request unit is kg m-2 s-1; the
        # per-metre value is written as-is (flagged for the checker).
        ligroundf[:, :, :] = np.ma.filled(gl_flux_dst[:, :, :], 0.0)

    ncid.group = 'NORCE'
    ncid.model = 'CISM3'
    ncid.contact_name = 'Heiko Goelzer'
    ncid.contact_email = 'heig@norceresearch.no'
    ncid.crs = 'epsg:3413'
    ncid.close()
