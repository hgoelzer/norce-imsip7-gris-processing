# NORCE ISMIP7 GrIS Processing

Post-processing of the NORCE CISM GrIS (Greenland) runs into ISMIP7-compliant
NetCDF output (11 CORE experiments), validated with the ISM_SimulationChecker
(`isschecker`).

This repo is the Greenland (GrIS) counterpart of `norce-ismip7-ais-processing/`
and follows the same structure, naming conventions and directory layout.

## Environment setup

The processing scripts need a python environment with **netCDF4**, **numpy**
and **scipy** (no matplotlib). Any conda installation works, e.g.:

```bash
conda create -n ismip7 -c conda-forge python=3.11 netcdf4 numpy scipy
conda activate ismip7
```

All commands below assume this environment is activated, so that plain
`python` resolves to it. The compliance checker (`isschecker`) uses its own
separate environment and is not affected.

## Model / input

- Model: CISM 2.0.5 (old driver), 4 km grid, `ism_id = CISM4`
- Input (READONLY):
  `/nird/datapeak/NS5011K/users/mali/CISM/GrIS/cism_storage/ismip7_gris_04km_old_driver/GrIS_04km_v01_geo01_ghf01_smb01_otf01_pow/proj`
- Run directories:
  - `historical_{m01_r01,m02_r02}` (1950–2014)
  - `greenland_04km_v01_{m01_r01,m02_r02}_{f26,f70,f85}`
    (f26 = ssp126, f70 = ssp370 [to 2100], f85 = ssp585; 2015–2300 except f70)
  - `ctrl-proj_{m01_r01,m02_r02}` (2015–2300)
  - `OCX` (1960–2025)
  - `greenland_04km_v01_*_f34` (ssp534-over) exists but is NOT part of CORE
- ESM mapping: m01 = CESM2-WACCM, m02 = MRI-ESM2-0; OCX has no ESM → `ERA`
- Grid: 421×721 @ 4 km (x1/y1 thickness grid; x0/y0 velocity grid), crs epsg:3413

## CORE experiment mapping

| counter | experiment | input dir | years |
|---------|-----------|-----------|-------|
| C001 | historical | historical_m01_r01 | 1950–2014 |
| C002 | historical | historical_m02_r02 | 1950–2014 |
| C003 | ssp370 | greenland_04km_v01_m01_r01_f70 | 2015–2100 |
| C004 | ssp370 | greenland_04km_v01_m02_r02_f70 | 2015–2100 |
| C005 | ssp126 | greenland_04km_v01_m01_r01_f26 | 2015–2300 |
| C006 | ssp126 | greenland_04km_v01_m02_r02_f26 | 2015–2300 |
| C007 | ssp585 | greenland_04km_v01_m01_r01_f85 | 2015–2300 |
| C008 | ssp585 | greenland_04km_v01_m02_r02_f85 | 2015–2300 |
| C009 | ctrl | ctrl-proj_m01_r01 | 2015–2300 |
| C010 | ctrl | ctrl-proj_m02_r02 | 2015–2300 |
| C011 | ocx | OCX | 1960–2025 |

## Layout

- 4 processing scripts (module-level, no `main()`; argparse with defaults
  imported from `config.py`):
  - `ISMIP7_scalar_processing.py` — scalar time series (10 variables) from `scalars.nc`
  - `ISMIP7_variable_HgridST_processing.py` — state variables on x1/y1 grid
    (lithk, orog, base, topg, sftgif/sftgrf/sftflf)
  - `ISMIP7_variable_HgridFL_processing.py` — flux variables on x1/y1 grid
    (acabf, libmassbfgr, libmassbffl, dlithkdt, licalvf, lifmassbf, ligroundf;
    libmassbffl is all zeros — required variable, but GrIS has no floating ice)
  - `ISMIP7_variable_VelogridST_processing.py` — velocity variables interpolated
    from x0/y0 to x1/y1 (xvelmean, yvelmean, strbasemag)
- `run_all_CORE.py` — wrapper over all 4 scripts for all 11 runs (`--exp`, `--dryrun`)
- `config.py` — central config (paths, interpreter, `ISM_ID`). **Edit this, not
  the scripts**, to change paths.
- `CORE.csv` — experiment table: counter_id, experiment_id (lowercase: `ctrl`,
  not `ctrl-proj`), start/end year, ESM_id
- `verify_base_topg.py` — offline replication of the isschecker base/topg/orog
  consistency tests
- Output: `../GrIS/NORCE/CISM4/CORE/{C001..C011}/` — 27 files per case

## Usage

```bash
# all 11 runs
python run_all_CORE.py

# one experiment (both members)
python run_all_CORE.py --exp historical

# dry run
python run_all_CORE.py --dryrun

# offline consistency verification
python verify_base_topg.py
```

## GrIS-specific differences from the AIS processing

1. **Masks live in `output_mask.nc`** — the GrIS `output.nc` has no
   `ice_mask`/`f_ground_cell` (it has `f_flotation`, which is the flotation
   function, NOT a fraction — never use it). `output_mask.nc` contains
   time-dependent (time, y1, x1) masks: `ice_mask`, `grounded_mask`,
   `floating_mask`, `calving_front_mask`, `melt_front_mask`.
2. **No floating ice** — `floating_mask` is all zero (marine_margin=1 removes
   floating ice), so `libmassbffl` is written as **all zeros** (required
   variable); `sftflf`/`iareafl`/`tendlibmassbffl` are zero/fill.
3. **Packed variables** — output.nc variables carry `scale_factor` (thk/topg/
   lsurf/usurf ×2000, acab ×5, dthck_dt ×1/31536000); netCDF4 applies the
   scaling automatically on read. Never use `set_auto_scale(False)`.
4. **More fluxes available than AIS** — `output_tavg.nc` has `melt_rate_tavg`
   (frontal melt, m/yr → lifmassbf) and `gl_flux_tavg` (kg/m/s → ligroundf);
   `scalars.nc` has `total_gl_flux` (→ tendligroundf). `total_bmlt_float` and
   `total_latmelt_flux` are not available (tendlifmassbf = 0; all basal melt
   is under grounded ice).
5. **Velocity units** — `uvel_mean`/`vvel_mean` in `output_g0.nc` are
   meter/year (scale_factor 500), same as AIS (scale_factor 31536000) →
   `/sPerY` conversion to m/s applies as in AIS.
6. **crs** is `epsg:3413` (north polar stereographic, Greenland), not 3031.
