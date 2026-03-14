#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script reads CISM output from a GrIS experiment, and creates a netCDF file following ISMIP7 conventions

# authors: Gunter Leguy (gunterl@ucar.edu) 
# adapted for NORCE Heiko Goelzer (heig@norceresearch.no)


import os, sys
import numpy as np
from netCDF4 import Dataset
import datetime

#########################################
# Defining paths, fields, and constants #
#########################################

#### 16 km
#path_to_experiment='/projects/NS8006K/users/heig/CISM/GrIS/gris_16km/e16_MAR39_classic_t0/e16_ens_MAR39_Rmed'
#MODEL='CISM16-MAR39-p50'
#inres='16'
#outres='08' # match to target 2d output, typically higher than model res

# Source setup instead
exec(open('setup_params.py').read())

# Experiment list

Tiers = ['Tier1']
#Tiers = ['Tier1','Tier2','Tier3','Tier4']

# Now sourced from setup_params.py. Override manually here
#tier1_ID = ['hist']

# Scalar output file used in experiment 
fileScalar  = 'scalars.nc'

# Strings for file naming convention:
IS    = 'GrIS'  # Ice Sheet name
GROUP = 'NORCE'

outputfolder = './Models/'

# State and flux variables
ST_var = ['lim','limnsw','iareagr','iareafl']
FL_var = ['tendacabf','tendlicalvf','tendlibmassbf','tendligroundf']

modeltag = IS + '_' + GROUP + '_' + MODEL

sPerY = 31536000.
dayPerY = 365.

start_date = datetime.date(1850, 1, 1)

stopOnErrors = False
file_object = open('scalar.log', 'a')
file_object.write('\n' + datetime.datetime.now().ctime() + '\n')

####################################
# Looping throught the experiments #
####################################


for tier in Tiers:
    if tier in ['Tier1']:
        expID = tier1_ID

    elif tier in ['Tier2']:
        expID = tier2_ID

    elif tier in ['Tier3']:
        expID = tier3_ID

    elif tier in ['Tier4']:
        expID = tier4_ID

    else:
        sys.exit('This tier is not supported by ISMIP7 protocole.')
        
        
    for exp in expID:
        
        ok = True
        # Defining the filed to access
        scalar_file = path_to_experiment + '/' + exp + '/' + fileScalar
        
        outputfolderscal = outputfolder + '/' + GROUP + '/' + MODEL + '/' + exp + '/'  
    
        # Create a subdirectory named for the output files.
        try:
            os.makedirs(outputfolderscal)
            print( 'Created subdirectory ', outputfolderscal)
        except:
            print( 'Subdirectory', outputfolder, 'already exists')
    
    
        print( 'Creating the ISMIP7 scalar files for experiment', exp)
        print( 'Attempting to read CISM file', scalar_file)

        try:
            cismfilescalar = Dataset(scalar_file,'r')            
        except:
            print( 'Error: Unable to open file for expt ',exp)
            ok = False
            if stopOnErrors:
                sys.exit('exiting program now')
            else:
                file_object.write('Missing scalars.nc ' + exp + '\n')
        if ok:
            print( 'Reading scalar output')    
            # READ SCALARS (function of time only).
            try:
                iareafc = cismfilescalar.variables['iareaf'][:]                # area covered by floating ice (m^2)
                iareagc = cismfilescalar.variables['iareag'][:]                # area covered by grounded ice (m^2)
                imassc  = cismfilescalar.variables['imass'][:]                 # total ice mass (kg)
                imafc   = cismfilescalar.variables['imass_above_flotation'][:] # total ice mass above flotation(kg)
                timeS   = cismfilescalar.variables['time'][:]
        
                nt = len(timeS)
        
                print('the time dimension is nt=',nt)
    
                tsmbfc = cismfilescalar.variables['total_smb_flux'][:]     # total surface mass balance flux (kg.s^-1)
                tbmbfc = cismfilescalar.variables['total_bmb_flux'][:]     # total basal mass balance flux (kg.s^-1)
                tcalfc = cismfilescalar.variables['total_calving_flux'][:] # total calving mass balance flux (kg.s^-1)
                tglfc  = cismfilescalar.variables['total_gl_flux'][:]      # total grounding line flux(kg.s^-1)
            except:
                sys.exit('Error: The output file is missing needed scalar(s).')
    
    
                
                        ##################
                        # Scalar outputs #
                        ##################
    
    
            # Varaiables to be written
            outField = ['lim','limnsw','iareagr','iareafl','tendacabf','tendlibmassbf','tendlicalvf','tendligroundf']
    
    
        
            for field in outField:
    
                print('creating output file for field ',field)
    
                # Create the field output file.
                outfilenamescal = outputfolderscal + field  + '_' + modeltag + '_' + exp + '.nc'
        
                # Removing the output file if it already exists.
                if os.path.isfile(outfilenamescal):
                    print( 'yup')
                    os.remove(outfilenamescal)
    
                if field in ST_var:            
                    ncid = Dataset(outfilenamescal, 'w')
                    ncid.createDimension('time', None)
                    time = ncid.createVariable('time', 'f4', ('time'))
                    days_end = [(datetime.date(round(yr),1,1)-start_date).days for yr in timeS]
                    time[:] = days_end
                    
                    time.units         = "days since 1850-01-01" 
                    time.calendar      = "standard" 
                    time.axis          = "T" 
                    time.long_name     = "time" 
                    time.standard_name = "time" 
    
    
                    if field in ['lim']:                    
                        lim = ncid.createVariable(field, 'f4', ('time'))
                        lim.units         = 'kg'
                        lim.long_name     = 'total ice mass'
                        lim.standard_name = 'land_ice_mass'
                        lim[:] = imassc[:]
    
                    if field in ['limnsw']:                    
                        limnsw = ncid.createVariable(field, 'f4', ('time'))
                        limnsw.units         = 'kg'
                        limnsw.long_name     = 'mass above flotation'
                        limnsw.standard_name = 'land_ice_mass_not_displacing_sea_water'
                        limnsw[:] = imafc[:]
    
                    if field in ['iareagr']:  
                        iareagr = ncid.createVariable(field, 'f4', ('time'))
                        iareagr.units         = 'm^2'
                        iareagr.long_name     = 'grounded ice area'
                        iareagr.standard_name = 'grounded_land_ice_area'
                        iareagr[:] = iareagc[:]
    
                    if field in ['iareafl']:
                        iareafl = ncid.createVariable(field, 'f4', ('time'))
                        iareafl.units         = 'm^2'
                        iareafl.long_name     = 'floating ice area'
                        iareafl.standard_name = 'floating_ice_shelf_area'
                        iareafl[:] = iareafc[:]
    
    
                if field in FL_var:            
                    ncid = Dataset(outfilenamescal, 'w')
                    ncid.createDimension('time', None)
                    ncid.createDimension('bnds',2)
    
                    time = ncid.createVariable('time', 'f4', ('time')) 
                    time.bounds        = 'time_bnds'
                    time.units         = "days since 1850-01-01" 
                    time.calendar      = "standard" 
                    time.axis          = "T" 
                    time.long_name     = "time" 
                    time.standard_name = "time"
                    days_mid = [(datetime.date(round(yr-1),7,1)-start_date).days for yr in timeS]
                    time[:] = days_mid
                    time_bounds = ncid.createVariable('time_bounds','f4', ('time','bnds',))
                    days_start = [(datetime.date(round(yr-1),1,1)-start_date).days for yr in timeS]
                    days_end = [(datetime.date(round(yr),1,1)-start_date).days for yr in timeS]
                    time_bounds[:,0] = days_start
                    time_bounds[:,1] = days_end
    
                    if field in ['tendacabf']:
                        tendacabf = ncid.createVariable(field, 'f4', ('time'))
                        tendacabf.units         = 'kg s-1'
                        tendacabf.long_name     = 'total SMB flux'
                        tendacabf.standard_name = 'tendency_of_land_ice_mass_due_to_surface_mass_balance'
                        tendacabf[:] = tsmbfc[:]
    
                    if field in ['tendlibmassbf']:
                        tendlibmassbf = ncid.createVariable(field, 'f4', ('time'))
                        tendlibmassbf.units         = 'kg s-1'
                        tendlibmassbf.long_name     = 'total BMB flux'
                        tendlibmassbf.standard_name = 'tendency_of_land_ice_mass_due_to_basal_mass_balance'
                        tendlibmassbf[:] = tbmbfc[:]
    
                    if field in ['tendlicalvf']:
                        tendlicalvf = ncid.createVariable(field, 'f4', ('time'))
                        tendlicalvf.units         = 'kg s-1'
                        tendlicalvf.long_name     = 'total calving flux'
                        tendlicalvf.standard_name = 'tendency_of_land_ice_mass_due_to_calving'
                        tendlicalvf[:] = -tcalfc[:]
    
                    if field in ['tendligroundf']:
                        tendligroundf = ncid.createVariable(field, 'f4', ('time'))
                        tendligroundf.units         = 'kg s-1'
                        tendligroundf.long_name     = 'total grounding line flux'
                        tendligroundf.standard_name = 'tendency_of_grounded_ice_mass'
                        tendligroundf[:] = -tglfc[:]
                    
                print( 'Created scalar file ', outfilenamescal)
        
                ncid.close()

    print( 'Done with writing output files for ',tier)


# Close the log file
file_object.close()
    
# Done writing the output files
print( 'Done with writing the output files')
