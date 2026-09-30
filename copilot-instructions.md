# Copilot Instructions — NORCE ISMIP7 GrIS Processing

Project: post-processing of NORCE CISM GrIS (Greenland) runs into
ISMIP7-compliant NetCDF output (11 CORE experiments), validated with the
ISM_SimulationChecker (`isschecker`). This repo mirrors
`norce-ismip7-ais-processing/` — keep the two consistent where possible.

## Layout

- 4 processing scripts (module-level, no `main()`; argparse with defaults imported from `config.py`):
  - `ISMIP7_scalar_processing.py` — scalar time series (10 variables) from `scalars.nc`
  - `ISMIP7_variable_HgridST_processing.py` — state variables on x1/y1 grid (lithk, orog, base, topg, sftgif/sftgrf/sftflf)
  - `ISMIP7_variable_HgridFL_processing.py` — flux variables on x1/y1 grid (acabf, libmassbfgr, libmassbffl, dlithkdt, licalvf, lifmassbf, ligroundf; libmassbffl is all zeros — required variable, no floating ice in GrIS)
  - `ISMIP7_variable_VelogridST_processing.py` — velocity variables interpolated from x0/y0 to x1/y1 (xvelmean, yvelmean, strbasemag)
- `run_all_CORE.py` — wrapper over all 4 scripts for all 11 runs (`--exp`, `--dryrun` flags)
- `config.py` — central config (paths, interpreter, `ISM_ID`). **Edit this, not the scripts**, to change paths.
- `CORE.csv` — experiment table: counter_id, experiment_id (lowercase: `ctrl`, not `ctrl-proj`), start/end year, ESM_id
- `verify_base_topg.py` — offline replication of the isschecker base/topg/orog consistency tests
- Output: `../GrIS/NORCE/CISM4/CORE/{C001..C011}/` — 27 files per case; `ism_id` comes from `ISM_ID` in `config.py` (CLI override: `--ism_id`)

## Environments & commands

- Processing python: `/nird/datapeak/NS11016K/miniforge3_26/envs/nc/bin/python` (netCDF4, numpy, scipy)
- Compliance checker: isschecker 0.5.1 in env `/nird/datapeak/NS11016K/miniforge3_26/envs/isschecker` (python 3.14)
- Run everything: `/nird/datapeak/NS11016K/miniforge3_26/envs/nc/bin/python run_all_CORE.py --exp <exp>` (exp = input dir name, e.g. `ctrl-proj`)
- Long batch runs: execute in background and check the summary table at the end.

## Input data

- Input (READONLY): `/nird/datapeak/NS5011K/users/mali/CISM/GrIS/cism_storage/ismip7_gris_04km_old_driver/GrIS_04km_v01_geo01_ghf01_smb01_otf01_pow/proj`
- Per run dir: `output.nc` (state, packed), `output_mask.nc` (ice_mask, grounded_mask, floating_mask, calving_front_mask, melt_front_mask — time-dependent), `output_tavg.nc` (sfc/basal_mbal_flux_tavg, calving_flux_tavg, gl_flux_tavg, melt_rate_tavg, dthck_dt_tavg), `output_g0.nc` (uvel_mean, vvel_mean, btract on x0/y0), `scalars.nc`, `restart_in.nc` (in ctrl-proj and OCX)
- 11 runs: historical_{m01_r01,m02_r02}, greenland_04km_v01_{m01_r01,m02_r02}_{f26,f70,f85}, ctrl-proj_{m01_r01,m02_r02}, OCX
  - f26 = ssp126, f70 = ssp370 (to 2100), f85 = ssp585; f34 (ssp534-over) exists but is NOT in CORE
- ESM mapping: m01=CESM2-WACCM, m02=MRI-ESM2-0; ocx has no ESM → ESM_id='ERA', ISM_member_id='m001'
- Experiment → counter: historical→C001/C002 (1950-2014), ssp370→C003/C004 (2015-2100), ssp126→C005/C006 (2015-2300), ssp585→C007/C008 (2015-2300), ctrl-proj→C009/C010 (2015-2300), ocx→C011 (1960-2025). m02 gets base counter +1 (`C%03d`).
- HgridFL filePrev logic: historical → ctrl-proj restart_in.nc; ocx → OCX restart_in.nc (no historical predecessor); else → historical output.nc

## Critical domain rules (do not violate)

1. **Masks come from `output_mask.nc`, never from `output.nc`** — the GrIS output.nc has no `ice_mask`/`f_ground_cell`. It has `f_flotation`, which is the flotation FUNCTION (can be very negative), NOT a fraction — never use it as a mask.
2. **No floating ice in GrIS** — `floating_mask` is all zero (marine_margin=1). `libmassbffl` is a REQUIRED variable → write it as all zeros; sftflf/iareafl/tendlibmassbffl are zero/fill.
3. **Packed data**: output.nc variables carry `scale_factor` (thk/topg/lsurf/usurf ×2000, acab ×5, dthck_dt ×1/31536000; output_g0 uvel/vvel ×500, btract ×17854200). netCDF4 auto-applies scaling on read (default) → values arrive in real units. NEVER call `set_auto_scale(False)` for these.
4. **Masking per data request**: variables defined only where ice exists (libmassbfgr, xvelmean, yvelmean, strbasemag) → `np.where(mask>0, val, netCDF4.default_fillvals['f4'])`. But **dlithkdt, lifmassbf and libmassbffl permit NO missing values** → write 0 where there is no ice (libmassbffl is all zeros anyway).
5. **`exp_out` mapping**: checker requires lowercase `ctrl`; input dir is `ctrl-proj` → `exp_out = 'ctrl' if exp == 'ctrl-proj' else exp` in all 4 scripts (filenames use `exp_out`). OCX → `ocx`.
6. **Time conventions**: ST variables → Jan 1 of year+1; FL variables → Jul 1 of year; `time_range` tag derived from data (`time_dst[t]-1`). CISM year t covers nominal year t−1.
7. **CF bounds naming**: the time bounds variable MUST be named `time_bnds` (matching `time:bounds = "time_bnds"`), not `time_bounds`.
8. **Unit conversions**:
   - acabf ← `acab` (m/yr ice) × rhoi / sPerY
   - dlithkdt ← `dthck_dt` (m/yr after auto-scale) / sPerY → m/s, 0-filled
   - lifmassbf ← `melt_rate_tavg` (m/yr, frontal melt) × rhoi / sPerY, 0-filled
   - licalvf ← `calving_flux_tavg` (kg/m2/s, negative) with positive-clamp `np.where(calving>0, 0, calving)`
   - ligroundf ← `gl_flux_tavg` (kg/m/s — per METRE of grounding line, not per m2; written as-is, flagged)
   - xvelmean/yvelmean ← uvel_mean/vvel_mean (m/yr after auto-scale) / sPerY → m/s (same as AIS)
   - tendligroundf ← `total_gl_flux` (kg/s); tendlifmassbf ← zeros (no total_latmelt_flux); tendlibmassbfgr ← total_bmb_flux (all basal melt grounded); tendlibmassbffl ← zeros
9. **base/topg cosmetic fix** (in `ISMIP7_variable_HgridST_processing.py`, applied before writing base/orog): where sftgrf==1 and |lsurf−topg|>0.009 → base=topg; where sftflf==1 and lsurf−topg<=0.011 → base=topg+0.1 m; same delta added to orog (keeps orog = base + lithk). The floating case never triggers for GrIS but is kept for consistency. Mask test uses MASK_TOL=1e-6, not ==1.0.
10. **netCDF4 auto-masking pitfall**: `v == fv` never matches on auto-masked reads. To verify fill placement use `nid.set_auto_mask(False)` + `np.isclose(v, fv, rtol=1e-5)`.

## Compliance checker notes

- The user reruns the checker themselves — do not run it unprompted.
- Expected known issues (mirroring AIS): (a) C011 ocx: 'ERA' naming errors — expected for reanalysis forcing; (b) warning "lithk > 0 where sftgif is 0" — thin margin ice below the mask threshold, warning-only.
- The local test-only patch for ocx in `.../envs/isschecker/lib/python3.14/site-packages/isschecker/data/experiments_ismip7.csv` (see AIS repo instructions) applies here too; lost on isschecker update.
