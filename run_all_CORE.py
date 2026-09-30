#!/usr/bin/env python
"""
Wrapper script: run all 4 ISMIP7 NORCE GrIS processing scripts for the
11 CORE experiments in the proj run directory.

Experiments (set_counter):
    historical m01 -> C001   (1950-2014)
    historical m02 -> C002   (1950-2014)
    ssp370     m01 -> C003   (2015-2100)
    ssp370     m02 -> C004   (2015-2100)
    ssp126     m01 -> C005   (2015-2300)
    ssp126     m02 -> C006   (2015-2300)
    ssp585     m01 -> C007   (2015-2300)
    ssp585     m02 -> C008   (2015-2300)
    ctrl       m01 -> C009   (2015-2300)
    ctrl       m02 -> C010   (2015-2300)
    ocx        r01 -> C011   (1960-2025)
The time_range tag in the output filenames is derived from the actual time
axis of the model output, so it adjusts automatically when a run is
extended.
Usage:
    python run_all_CORE.py                 # run everything
    python run_all_CORE.py --exp ssp126    # run only one experiment (all members)
    python run_all_CORE.py --exp C003      # run one CORE case by counter id
    python run_all_CORE.py --exp C003 C004 # run several cases
    python run_all_CORE.py --dryrun        # only print what would be run
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime

# Top-level configuration (paths)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import PATH_EXP

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

SCRIPTS = [
    'ISMIP7_scalar_processing.py',
    'ISMIP7_variable_HgridST_processing.py',
    'ISMIP7_variable_HgridFL_processing.py',
    'ISMIP7_variable_VelogridST_processing.py',
]

# (exp, ESM_num, RCM_num) for the 11 CORE runs.
# The ocx run has no ESM member; it is identified by RCM_num only.
RUNS = [
    ('historical', 'm01', 'r01'),
    ('historical', 'm02', 'r02'),
    ('ssp370',     'm01', 'r01'),
    ('ssp370',     'm02', 'r02'),
    ('ssp126',     'm01', 'r01'),
    ('ssp126',     'm02', 'r02'),
    ('ssp585',     'm01', 'r01'),
    ('ssp585',     'm02', 'r02'),
    ('ctrl',       'm01', 'r01'),
    ('ctrl',       'm02', 'r02'),
    ('ocx',        None,  'r01'),
]

# Python interpreter used to run the processing scripts: the same one that
# runs this wrapper (sys.executable), so activate a conda env with netCDF4,
# numpy and scipy before calling `python run_all_CORE.py` (see README.md).

path_exp = PATH_EXP


def run_dir(exp, ESM_num, RCM_num):
    """Input run directory for a given experiment (GrIS proj layout)."""
    if exp == 'ocx':
        return f"{path_exp}/OCX"
    if exp == 'historical':
        return f"{path_exp}/historical_{ESM_num}_{RCM_num}"
    if exp == 'ctrl':
        return f"{path_exp}/ctrl-proj_{ESM_num}_{RCM_num}"
    if exp == 'ssp370':
        return f"{path_exp}/greenland_04km_v01_{ESM_num}_{RCM_num}_f70"
    if exp == 'ssp126':
        return f"{path_exp}/greenland_04km_v01_{ESM_num}_{RCM_num}_f26"
    if exp == 'ssp585':
        return f"{path_exp}/greenland_04km_v01_{ESM_num}_{RCM_num}_f85"
    sys.exit(f'Error: unknown experiment {exp}')


def runs_for_exp(exp):
    """Return the RUNS entries matching an experiment name or a counter id.

    Accepts an experiment name (historical, ssp370, ssp126, ssp585,
    ctrl, ocx) or a CORE counter id (C001..C011, case-insensitive).
    The RUNS order matches the CORE.csv counters (C001 = first entry).
    """
    key = exp.lower()
    if key.startswith('c') and key[1:].isdigit():
        idx = int(key[1:]) - 1
        if 0 <= idx < len(RUNS):
            return [RUNS[idx]]
        sys.exit(f'Error: unknown counter {exp} (valid: C001..C011)')
    runs = [r for r in RUNS if r[0] == exp]
    if not runs:
        sys.exit(f'Error: unknown experiment {exp} '
                 '(valid: historical, ssp370, ssp126, ssp585, ctrl, ocx, '
                 'or C001..C011)')
    return runs


def main():
    parser = argparse.ArgumentParser(description='Run ISMIP7 NORCE GrIS processing for all CORE experiments')
    parser.add_argument('--exp', nargs='+', default=None, metavar='EXP',
                        help='Only run these experiments: experiment names '
                             '(historical, ssp370, ssp126, ssp585, ctrl, ocx) '
                             'and/or counter ids (C001..C011). Default: all 11 runs')
    parser.add_argument('--dryrun', action='store_true',
                        help='Only print what would be run, without executing')
    args = parser.parse_args()

    runs = RUNS
    if args.exp is not None:
        runs = []
        for exp in args.exp:
            runs.extend(runs_for_exp(exp))

    results = []

    for exp, ESM_num, RCM_num in runs:
        rdir = run_dir(exp, ESM_num, RCM_num)
        label = f"{exp}_{ESM_num or 'ocx'}_{RCM_num}"

        if not os.path.isdir(rdir):
            print(f"\n===== {label}: input directory missing, skipping =====")
            print(f"    {rdir}")
            results.append((label, 'SKIPPED (no input dir)'))
            continue

        if not os.path.isfile(f"{rdir}/output.nc"):
            print(f"\n===== {label}: output.nc missing, skipping =====")
            print(f"    {rdir}")
            results.append((label, 'SKIPPED (no output.nc)'))
            continue

        print(f"\n===== {label} =====")
        print(f"    {rdir}")

        status = 'OK'
        for script in SCRIPTS:
            cmd = [sys.executable, os.path.join(SCRIPT_DIR, script),
                   '--exp', exp, '--ESM_num', ESM_num or 'm01', '--RCM_num', RCM_num]
            if args.dryrun:
                print('    [dryrun]', ' '.join(cmd))
                continue

            print(f"    running {script} ...")
            proc = subprocess.run(cmd)
            if proc.returncode != 0:
                print(f"    ERROR: {script} failed with return code {proc.returncode}")
                status = f'FAILED ({script})'
                break

        if not args.dryrun:
            results.append((label, status))

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    if not args.dryrun:
        print('\n===== Summary =====')
        for label, status in results:
            print(f"  {label:20s}  {status}")
        n_fail = sum(1 for _, s in results if s.startswith('FAILED'))
        print(f"\nFinished at {datetime.now():%Y-%m-%d %H:%M:%S}: "
              f"{len(results)} runs, {n_fail} failed")


if __name__ == '__main__':
    main()
