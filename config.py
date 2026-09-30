#!/usr/bin/env python
"""
Top-level configuration for the ISMIP7 NORCE GrIS processing scripts.

All processing scripts (ISMIP7_scalar_processing.py,
ISMIP7_variable_HgridST_processing.py, ISMIP7_variable_HgridFL_processing.py,
ISMIP7_variable_VelogridST_processing.py) and the wrapper (run_all_CORE.py)
import their defaults from this file. Edit the values here to change them
for all scripts at once; individual scripts can still override them on the
command line (--path_exp, --dstPath).

The scripts require a python environment with netCDF4, numpy and scipy
installed (see README.md for how to create one); run them with that
environment's `python`.
"""

import os

# ----------------------------------------------------------------------
# Path to the CISM model output (proj run directory, READONLY)
# ----------------------------------------------------------------------
PATH_EXP = '/nird/datapeak/NS5011K/users/mali/CISM/GrIS/cism_storage/ismip7_gris_04km_old_driver/GrIS_04km_v01_geo01_ghf01_smb01_otf01_pow/proj'

# ----------------------------------------------------------------------
# Base path for the ISMIP7 output data
# ----------------------------------------------------------------------
DST_PATH = '/nird/datapeak/NS5011K/users/heig/ISMIP7'

# ----------------------------------------------------------------------
# Strings for the output directory tree and file names
# ({DST_PATH}/{DOMAIN_ID}/{SOURCE_ID}/{ISM_ID}/{SET_ID}/{C001..C011}/).
# DOMAIN_ID and SOURCE_ID are also written as global attributes
# (`domain`/`group`) in the output NetCDF files.
# ----------------------------------------------------------------------
DOMAIN_ID = 'GrIS'    # Ice sheet
SOURCE_ID = 'NORCE'   # Modelling group (also global attribute `group`)
SET_ID = 'CORE'       # Experiment set

# ----------------------------------------------------------------------
# ISM model ID used in the output directory tree and file names
# ({DST_PATH}/GrIS/NORCE/{ISM_ID}/CORE/{C001..C011}/).
# Also written as the global attribute `model` in the output NetCDF files.
# ----------------------------------------------------------------------
ISM_ID = 'CISM'

# ----------------------------------------------------------------------
# Contact information written as global attributes (`contact_name`,
# `contact_email`) in the output NetCDF files.
# ----------------------------------------------------------------------
CONTACT_NAME = 'Maria Paz Lira, Heiko Goelzer'
CONTACT_EMAIL = 'mali@norceresearch.no, heig@norceresearch.no'

# Directory containing this config file (repo root)
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
