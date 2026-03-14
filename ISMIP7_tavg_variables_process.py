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
#outres='05' # match to target 2d output, typically higher than model res

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

fileField   = 'output_tavg.nc'
fileMask   = 'output.nc'


# ISMIP6 Field names defined on the thickness grid
FL_list = ['acabf', 'libmassbfgr','libmassbffl','licalvf','lifmassbf', 'ligroundf']
# Reduced set for scalar recomp
#FL_list = ['acabf']

fieldoutList = FL_list

stopOnErrors = False
file_object = open('output.log', 'a')
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
        sys.exit('This tier is not supported by ISMIP6 protocole.')
        
        
    for exp in expID:

        ok = True
        print( 'Creating the ISMIP6 file for experiment', exp)

        outputfoldervar = outputfolder + '/' + GROUP + '/' + MODEL + '/' + exp + '/'  
    
        # Create a subdirectory named for the output files.
        try:
            os.makedirs(outputfoldervar)
            print( 'Created subdirectory ', outputfoldervar)
        except:
            print( 'Subdirectory', outputfoldervar, 'already exists')
    
    
        # Defining the file to access
        field_file = path_to_experiment + '/' + exp + '/' + fileField
        
        print( 'Attempting to read CISM file', field_file)

        try:
            cismfilefield  = Dataset(field_file,'r')
        except:
            print( 'Error: Unable to open file for expt ',exp)
            ok = False 
            if stopOnErrors:
                sys.exit('exiting program now')
            else:
                file_object.write('Missing output.nc ' + exp + '\n')

        if ok:
            print( 'Reading variables')    
            # Reading the fields.
            try:
                nx = len(cismfilefield.dimensions['x1'])
                ny = len(cismfilefield.dimensions['y1'])
    
                timeS = cismfilefield.variables['time'][:]     
                nt = len(timeS)
                print('the time dimension is nt=',nt)
                if nt>287.:
                    sys.exit('Something wrong with the time dimension, check your file.')            
                
                x1out   = cismfilefield.variables['x1'][:] 
                y1out   = cismfilefield.variables['y1'][:] 
    
                sfc_mbal_fluxout   = cismfilefield.variables['sfc_mbal_flux_tavg'][:,:,:]   # surface mass balance flux (kg.m^-2.s^-1)
                basal_mbal_fluxout = cismfilefield.variables['basal_mbal_flux_tavg'][:,:,:] # basal mass balance flux (kg.m^-2.s^-1)
                calving_fluxout    = cismfilefield.variables['calving_flux_tavg'][:,:,:]    # calving flux (kg.m^-1.s^-1)
                gl_fluxout         = cismfilefield.variables['gl_flux_tavg'][:,:,:]         # calving flux (kg.m^-1.s^-1)
    
    
            except:
                sys.exit('Error: The output file' + cismfilefield + ' is missing needed variable(s).')
    
    
            # Defining the file to access
            mask_file = path_to_experiment + '/' + exp + '/' + fileMask
            
            print( 'Attempting to read CISM file', field_file)
    
            try:
                cismfilemask  = Dataset(mask_file,'r')
            except:
                print( 'Error: Unable to open file for expt ',exp)
                ok = False 
                if stopOnErrors:
                    sys.exit('exiting program now')
                else:
                    file_object.write('Missing output.nc ' + exp + '\n')
    
            if ok:
                print( 'Reading variables')    
                # Reading the fields.
                try:
                    nx = len(cismfilemask.dimensions['x1'])
                    ny = len(cismfilemask.dimensions['y1'])
        
                    timeS = cismfilemask.variables['time'][:]     
                    nt = len(timeS)
                    print('the time dimension is nt=',nt)
                    if nt>287.:
                        sys.exit('Something wrong with the time dimension, check your file.')            
                    
        #            dthck_dtout = np.zeros((nt+1,ny,nx))
        #            dthck_dtout[0,:,:] = dhdt_hist[:,:]
                    
                    
                    x1out   = cismfilemask.variables['x1'][:] 
                    y1out   = cismfilemask.variables['y1'][:] 
                    
                    f_groundout       = cismfilemask.variables['grounded_mask'][:,:,:]       # grounded ice sheet area fraction (1)
                    f_floatout        = cismfilemask.variables['floating_mask'][:,:,:]       # grounded ice sheet area fraction (1)
                
                except:
                    sys.exit('Error: The output file' + cismfilemask + ' is missing needed variable(s).')
        
                    
                # Corresponding CISM fields to assimilate to experiment output field naming
                f_ground      = f_groundout[:,:,:] # grounded ice sheet area fraction
                f_float       = f_floatout[:,:,:] # floating ice sheet area fraction
                f_ice = f_ground + f_float # ice sheet area fraction
                
                basal_mbal_flux_gr = basal_mbal_fluxout[:,:,:]*f_ground[:,:,:]   # basal mass balance flux beneath grounded ice
                basal_mbal_flux_fl = basal_mbal_fluxout[:,:,:]*f_float[:,:,:]    # basal mass balance flux beneath floating ice
                    
                #############################
                # Hgrid variable outputs #
                #############################
            
                # Variables to be written.
                outField = fieldoutList
        
                for field in outField:
        
                    print('creating output file for field ',field)
        
                    # Create the field output file.
                    outfilenamevar = outputfoldervar + field  + '_' + model + '_' + exp + '.nc'
            
                    # Removing the output file if it already exists.
                    if os.path.isfile(outfilenamevar):
                        print( 'yup')
                        os.remove(outfilenamevar)
        
                    ncid = Dataset(outfilenamevar, 'w')
                    ncid.createDimension('time', None)
                    ncid.createDimension('x', nx)
                    ncid.createDimension('y', ny)
        
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
        
                    if field in FL_list:
        
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
                        time_bounds.units         = "days since 1850-01-01" 
                        time_bounds.calendar      = "standard" 
                        days_start = [(datetime.date(round(yr-1),1,1)-start_date).days for yr in timeS]
                        days_end = [(datetime.date(round(yr),1,1)-start_date).days for yr in timeS]
                        time_bounds[:,0] = days_start
                        time_bounds[:,1] = days_end
        
        
                        if field in ['acabf']: 
                            acabf = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
                            acabf.units         = 'kg m-2 s-1'
                            acabf.long_name     = 'surface mass balance flux'
                            acabf.standard_name = 'land_ice_surface_specific_mass_balance_flux'
                            sfc_mbal_fluxout[f_ice<1] = fillf4   # mask to missing value 
                            acabf[:,:,:] = sfc_mbal_fluxout
        
                        if field in ['libmassbfgr']: 
                            libmassbfgr = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
                            libmassbfgr.units         = 'kg m-2 s-1'
                            libmassbfgr.long_name     = 'basal mass balance flux beneath grounded ice'
                            libmassbfgr.standard_name = 'land_ice_basal_specific_mass_balance_flux'
                            basal_mbal_flux_gr[f_ground<1] = fillf4   # mask to missing value 
                            libmassbfgr[:,:,:] = basal_mbal_flux_gr[:,:,:]        
        
                        if field in ['libmassbffl']: 
                            libmassbffl = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
                            libmassbffl.units         = 'kg m-2 s-1'
                            libmassbffl.long_name     = 'basal mass balance flux beneath floating ice'
                            libmassbffl.standard_name = 'land_ice_basal_specific_mass_balance_flux'
                            basal_mbal_flux_fl[f_float<1] = fillf4   # mask to missing value 
                            libmassbffl[:,:,:] = basal_mbal_flux_fl[:,:,:]        
        
        #                if field in ['dlithkdt']: 
        #                    dlithkdt = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
        #                    dlithkdt.units         = 'm s-1'
        #                    dlithkdt.long_name     = 'ice thickness imbalance'
        #                    dlithkdt.standard_name = 'tendency_of_land_ice_thickness'
        #                    dlithkdt[:,:,:] = (dthck_dtout[1:,:,:] + dthck_dtout[0:-1,:,:])/2.
                    
                        if field in ['licalvf']: 
                            licalvf = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
                            licalvf.units         = 'kg m-2 s-1'
                            licalvf.long_name     = 'calving flux'
                            licalvf.standard_name = 'land_ice_specific_mass_flux_due_to_calving'
                            calving_fluxout[:,:,:] = -calving_fluxout[:,:,:] # sign convention
                            calving_fluxout[f_ice<1] = fillf4   # mask to missing value 
                            licalvf[:,:,:] = calving_fluxout
                    
        #                if field in ['lifmassbf']: 
        #                    lifmassbf = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
        #                    lifmassbf.units         = 'kg m-2 s-1'
        #                    lifmassbf.long_name     = 'ice front melt and calving flux'
        #                    lifmassbf.standard_name = 'land_ice_specific_mass_flux_due_to_calving_and_ice_front_melting'
        #                    lifmassbf[:,:,:] = -calving_fluxout[:,:,:]+meltflux...
        
                        if field in ['ligroundf']: 
                            ligroundf = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
                            ligroundf.units         = 'kg m-2 s-1'
                            ligroundf.long_name     = 'grounding line flux'
                            ligroundf.standard_name = 'land_ice_specific_mass_flux_at_grounding_line'
                            gl_fluxout[:,:,:][f_ice<1] = fillf4   # mask to missing value 
                            ligroundf[:,:,:] = gl_fluxout[:,:,:]
        
        #                if field in ['hfgeoubed']: 
        #                    hfgeoubed = ncid.createVariable(field, 'f4', ('time','y','x'), fill_value=fillf4)
        #                    hfgeoubed.units         = 'W m-2'
        #                    hfgeoubed.long_name     = 'geothermal heat flux'
        #                    hfgeoubed.standard_name = 'upward_geothermal_heat_flux_in_land_ice'
        #                    hfgeoubed[:,:,:] = bheatflxout[:,:,:]         
            
                    
                    print( 'Created field output file', outfilenamevar)
        
        
            
                    ncid.close()
    

    print( 'Done with writing output files for ',tier)


# Close the log file
file_object.close()
    
# Done writing the output files
print( 'Done with writing the output files')
