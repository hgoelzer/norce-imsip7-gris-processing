# ISMIP7 processing

# Setup run in setup_params.py!

import subprocess

# python processing to extract variables
exec(open('ISMIP7_scalar_process.py').read())
exec(open('ISMIP7_variables_process.py').read())
exec(open('ISMIP7_tavg_variables_process.py').read())
exec(open('ISMIP7_g0_variables_process.py').read())


# cdo interpolation
p = subprocess.run("./meta_regrid_exp.sh")
