#!/usr/bin/env python
"""
Top-level configuration for the ISMIP7 NORCE GrIS processing scripts.

All processing scripts (ISMIP7_scalar_processing.py,
ISMIP7_variable_HgridST_processing.py, ISMIP7_variable_HgridFL_processing.py,
ISMIP7_variable_VelogridST_processing.py) and the wrapper (run_all_CORE.py)
import their defaults from this file. Edit the values here to change them
for all scripts at once; individual scripts can still override them on the
command line (--path_exp, --dstPath).
"""

import os

# ----------------------------------------------------------------------
# Python interpreter used by the wrapper to run the processing scripts
# (must have netCDF4, numpy and scipy installed)
# ----------------------------------------------------------------------
PYTHON = '/nird/datapeak/NS11016K/miniforge3_26/envs/nc/bin/python'

# ----------------------------------------------------------------------
# Path to the CISM model output (proj run directory, READONLY)
# GrIS 4 km submission (CISM 2.0.5, old driver)
# ----------------------------------------------------------------------
PATH_EXP = '/nird/datapeak/NS5011K/users/mali/CISM/GrIS/cism_storage/ismip7_gris_04km_old_driver/GrIS_04km_v01_geo01_ghf01_smb01_otf01_pow/proj'

# ----------------------------------------------------------------------
# Base path for the ISMIP7 output data
# ----------------------------------------------------------------------
DST_PATH = '/nird/datalake/NS11016K/users/heig/ISMIP7/data_processing'

# ----------------------------------------------------------------------
# ISM model ID used in the output directory tree and file names
# ({DST_PATH}/GrIS/NORCE/{ISM_ID}/CORE/{C001..C011}/).
# ----------------------------------------------------------------------
ISM_ID = 'CISM4'

# Directory containing this config file (repo root)
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
