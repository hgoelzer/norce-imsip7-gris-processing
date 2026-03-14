#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This script reads CISM output from a GrIS experiment, and creates a netCDF file following ISMIP7 conventions

# authors: Gunter Leguy (gunterl@ucar.edu) 
# adapted for NORCE Heiko Goelzer (heig@norceresearch.no)


import os, sys
import numpy as np
from netCDF4 import Dataset
from netCDF4 import default_fillvals
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

# Strings for file naming convention:
IS    = 'GrIS'  # Ice Sheet name
GROUP = 'NORCE'

#outputfolder = './Models'
outputfolder = './proc'

model = IS + '_' + GROUP + '_' + MODEL

start_date = datetime.date(1850, 1, 1)
sPerY = 31556926.
fillf4 = default_fillvals['f4']

fileField   = 'output_g0.nc'


# ISMIP7 Field names defined on the velocity grid
fieldoutList = ['xvelsurf', 'yvelsurf', 'xvelbase', 'yvelbase', 'xvelmean', 'yvelmean', 'strbasemag']
# Reduced set for scalar recomp
#fieldoutList = ['xvelmean', 'yvelmean']

stopOnErrors = False
file_object = open('output.log', 'a')
file_object.write('\n' + datetime.datetime.now().ctime() + '\n')

# Looping throught the experiments:
    
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
        print( 'Creating the ISMIP7 file for experiment', exp)

        outputfoldervar = outputfolder + '/' + GROUP + '/' + MODEL + '/' + exp + '_' + inres
    
        # Create a subdirectory named for the output files.
        try:
            os.makedirs(outputfoldervar)
            print( 'Created subdirectory ', outputfoldervar)
        except:
            print( 'Subdirectory', outputfoldervar, 'already exists')
    
    
        # Defining the file to access
        field_fileG0 = path_to_experiment + '/' + exp + '/' + fileField
        
        print( 'Attempting to read CISM file', field_fileG0)

        try:
            cismfilefieldG0  = Dataset(field_fileG0,'r')
        except:
            print( 'Error: Unable to open file for expt ',exp)
            print( 'with file', field_fileG0)
            ok = False
            if stopOnErrors:
                sys.exit('exiting program now')
            else:
                file_object.write('Missing output_g0.nc ' + exp + '\n')

                
        if ok:
            print( 'Reading variable output')    
    
            # Reading the fields.
            try:
                nx = len(cismfilefieldG0.dimensions['x0'])
                ny = len(cismfilefieldG0.dimensions['y0'])
    
                timeS = cismfilefieldG0.variables['time'][:]
                nt = len(timeS)
                print('the time dimension is nt=',nt)
                if nt>287.:
                    sys.exit('Something wrong with the time dimension, check your file.')
    
                x0out   = cismfilefieldG0.variables['x0'][:] 
                y0out   = cismfilefieldG0.variables['y0'][:]            
                usfcout = cismfilefieldG0.variables['usfc'][:,:,:]      # ice surface x-velocity (m.a^-1)
                vsfcout = cismfilefieldG0.variables['vsfc'][:,:,:]      # ice surface y-velocity (m.a^-1)
                ubasout = cismfilefieldG0.variables['ubas'][:,:,:]      # ice basal x-velocity (m.a^-1)
                vbasout = cismfilefieldG0.variables['vbas'][:,:,:]      # ice basal y-velocity (m.a^-1)
                uvel_meanout = cismfilefieldG0.variables['uvel_mean'][:,:,:] # ice vertical mean x-velocity (m.a^-1)
                vvel_meanout = cismfilefieldG0.variables['vvel_mean'][:,:,:] # ice vertical mean y-velocity (m.a^-1)            
                btractout    = cismfilefieldG0.variables['btract'][:,:,:]    # basal traction magnitude (Pa)
                ice_mask_stagout = cismfilefieldG0.variables['ice_mask_stag'][:,:,:]    # g0 ice mask (1)
    
            except:
                sys.exit('Error: The file' + cismfilefieldG0 + ' is missing needed variable(s).')
    
    
            #############################
            # Velocity variable outputs #
            #############################    
    
            # Variables to be written.
            # Note: the velocity-grid dependent variables are all State Variables
            outField = fieldoutList
    
            field_thick_grid = ['zvelsurf','zvelbase']
                
            for field in outField:
    
                print('creating output file for field ',field)
    
                # Create the field output file.
                outfilenamevar = outputfoldervar + '/' + field  + '_' + model + '_' + exp + '.nc'
        
                # Removing the output file if it already exists.
                if os.path.isfile(outfilenamevar):
                    print( 'there is already a file named ',outfilenamevar)
                    print('removing the file ', outfilenamevar)
                    
                    os.remove(outfilenamevar)
    
                ncid = Dataset(outfilenamevar, 'w')
                ncid.createDimension('time', None)
    
                if field in field_thick_grid:
    
                    ncid.createDimension('x', nx1)
                    ncid.createDimension('y', ny1)
    
                    x           = ncid.createVariable('x','f4',('x',))
                    x.long_name = "x coordinate of projection";
                    x.standard_name = "projection_x_coordinate"
                    x.axis = "X"
                    x.units     = "m"
                    x[:] = x1out[:]
    
                    y           = ncid.createVariable('y','f4',('y',))
                    y.long_name = "y coordinate of projection";
                    y.standard_name = "projection_y_coordinate"
                    y.axis = "Y"
                    y.units     = "m"            
                    y[:] = y1out[:]
    
                else: 
    
                    ncid.createDimension('x', nx)
                    ncid.createDimension('y', ny)
    
                    x           = ncid.createVariable('x','f4',('x',))
                    x.long_name = "x coordinate of projection";
                    x.standard_name = "projection_x_coordinate"
                    x.axis = "X"
                    x.units     = "m"
                    x[:] = x0out[:]
    
                    y           = ncid.createVariable('y','f4',('y',))
                    y.long_name = "y coordinate of projection";
                    y.standard_name = "projection_y_coordinate"
                    y.axis = "Y"
                    y.units     = "m"            
                    y[:] = y0out[:]
    
    
    
                            
                time    = ncid.createVariable('time', 'f4', ('time'))
                days_end = [(datetime.date(round(yr),1,1)-start_date).days for yr in timeS]
                time[:] = days_end
                
                time.units         = "days since 1850-01-01" 
                time.calendar      = "standard" 
                time.axis          = "T" 
                time.long_name     = "time" 
                time.standard_name = "time" 
    
    
                if field in ['xvelsurf']:                    
                    xvelsurf = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
                    xvelsurf.units         = 'm s-1'
                    xvelsurf.long_name     = 'surface velocity in x'
                    xvelsurf.standard_name = 'land_ice_surface_x_velocity'
                    xvelsurf.missing_value = fillf4
                    usfcout = usfcout[:,:,:]/sPerY         # converting from (m.a^-1) to (m.s^-1)
                    usfcout[ice_mask_stagout<1] = fillf4   # mask to missing value 
                    xvelsurf[:,:,:] = usfcout
    
                if field in ['yvelsurf']:                    
                    yvelsurf = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
                    yvelsurf.units         = 'm s-1'
                    yvelsurf.long_name     = 'surface velocity in y'
                    yvelsurf.standard_name = 'land_ice_surface_y_velocity'
                    yvelsurf.missing_value = fillf4
                    vsfcout = vsfcout[:,:,:]/sPerY         # converting from (m.a^-1) to (m.s^-1)
                    vsfcout[ice_mask_stagout<1] = fillf4   # mask to missing value 
                    yvelsurf[:,:,:] = vsfcout
    
                if field in ['xvelbase']:                    
                    xvelbase = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
                    xvelbase.units         = 'm s-1'
                    xvelbase.long_name     = 'basal velocity in x'
                    xvelbase.standard_name = 'land_ice_basal_x_velocity'
                    xvelbase.missing_value = fillf4
                    ubasout = ubasout[:,:,:]/sPerY         # converting from (m.a^-1) to (m.s^-1)
                    ubasout[ice_mask_stagout<1] = fillf4   # mask to missing value 
                    xvelbase[:,:,:] = ubasout
    
                if field in ['yvelbase']:                    
                    yvelbase = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
                    yvelbase.units         = 'm s-1'
                    yvelbase.long_name     = 'basal velocity in y'
                    yvelbase.standard_name = 'land_ice_basal_y_velocity'
                    yvelbase.missing_value = fillf4
                    vbasout = vbasout[:,:,:]/sPerY         # converting from (m.a^-1) to (m.s^-1)
                    vbasout[ice_mask_stagout<1] = fillf4   # mask to missing value 
                    yvelbase[:,:,:] = vbasout
    
                if field in ['xvelmean']:                    
                    xvelmean = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
                    xvelmean.units         = 'm s-1'
                    xvelmean.long_name     = 'mean velocity in x'
                    xvelmean.standard_name = 'land_ice_vertical_mean_x_velocity'
                    xvelmean.missing_value = fillf4
                    uvel_meanout = uvel_meanout[:,:,:]/sPerY         # converting from (m.a^-1) to (m.s^-1)
                    uvel_meanout[ice_mask_stagout<1] = fillf4   # mask to missing value 
                    xvelmean[:,:,:] = uvel_meanout
    
                if field in ['yvelmean']:                    
                    yvelmean = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
                    yvelmean.units         = 'm s-1'
                    yvelmean.long_name     = 'mean velocity in y'
                    yvelmean.standard_name = 'land_ice_vertical_mean_y_velocity'
                    yvelmean.missing_value = fillf4
                    vvel_meanout = vvel_meanout[:,:,:]/sPerY         # converting from (m.a^-1) to (m.s^-1)
                    vvel_meanout[ice_mask_stagout<1] = fillf4   # mask to missing value 
                    yvelmean[:,:,:] = vvel_meanout
    
                if field in ['strbasemag']:                    
                    strbasemag = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
                    strbasemag.units         = 'Pa'
                    strbasemag.long_name     = 'basal drag'
                    strbasemag.standard_name = 'land_ice_basal_drag'
                    strbasemag.missing_value = fillf4
                    btractout[ice_mask_stagout<1] = fillf4   # mask to missing value 
                    strbasemag[:,:,:] = btractout
    
                
                print( 'Created field output file', outfilenamevar)
    
        
                ncid.close()
    

    print( 'Done with writing output files for ',tier)


# Close the log file
file_object.close()
    
# Done writing the output files
print( 'Done with writing the output files')
