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

# Strings for file naming convention:
IS    = 'GrIS'  # Ice Sheet name
GROUP = 'NORCE'

outputfolder = './Models'
#outputfolder = './proc' # if regridding is needed

model = IS + '_' + GROUP + '_' + MODEL

start_date = datetime.date(1850, 1, 1)

fileField   = 'output.nc'


# ISMIP7 Field names defined on the thickness grid
ST_list = ['lithk', 'base', 'orog', 'topg', 'litemptop', 'litempmean', 'litempbotgr', 'litempbotfl', 'sftgif', 'sftgrf', 'sftflf'] 
FL_list = ['hfgeoubed']
# Reduced set for scalar recomp
#ST_list = ['lithk', 'orog', 'topg', 'sftgif', 'sftgrf', 'sftflf'] 
#FL_list = []

fieldoutList = ST_list + FL_list

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
            print( 'Reading variable output')    
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
    
                thkout             = cismfilefield.variables['thk'][:,:,:]                # ice thickness (m)
                usurfout           = cismfilefield.variables['usurf'][:,:,:]              # upper surface elevation (m)
                lsurfout           = cismfilefield.variables['lsurf'][:,:,:]              # lower surface elevation (m)
                topgout            = cismfilefield.variables['topg'][:,:,:]               # bed elevation (m)
                bheatflxout        = -cismfilefield.variables['bheatflx'][:,:,:]          # geothermal heat flux (m)
    
                artmout            = cismfilefield.variables['artm'][:,:,:]               # annual mean air temperature (deg C)
                #btempout           = cismfilefield.variables['btemp'][:,:,:]                # basal ice temperature (C)
                #ice_maskout        = cismfilefield.variables['ice_mask'][:,:,:]             # land ice area fraction (1)
                f_groundout        = cismfilefield.variables['grounded_mask'][:,:,:]      # grounded ice sheet area fraction (1)
                f_floatout        = cismfilefield.variables['floating_mask'][:,:,:]       # grounded ice sheet area fraction (1)
    
                tempout           = cismfilefield.variables['tempstag'][:,:,:,:]           # ice temperature (C)
    
            except:
                sys.exit('Error: The output file' + cismfilefield + ' is missing needed variable(s).')
    
    
            # Corresponding CISM fields to assimilate to experiment output field naming
            #f_ground      = f_groundout[:,:,:]*ice_maskout[:,:,:]      # grounded ice sheet area fraction
            #f_float       = (1-f_groundout[:,:,:])*ice_maskout[:,:,:]  # floating ice sheet area fraction
            f_ground      = f_groundout[:,:,:] # grounded ice sheet area fraction
            f_float       = f_floatout[:,:,:] # floating ice sheet area fraction
            f_ice = f_ground[:,:,:] + f_float[:,:,:] # ice sheet area fraction

            btempout          = tempout[:,1,:,:]
            ttempout          = tempout[:,0,:,:]
            mtempout          = np.mean(tempout[:,:,:,:], axis=1) # vertical average 
            
        
            btemp_gr          = btempout[:,:,:]*f_ground[:,:,:]  # basal temperature beneath grounded ice sheet
            btemp_fl          = btempout[:,:,:]*f_float[:,:,:]   # basal temperature beneath floating ice shelf
        
                
            #############################
            # Hgrid variable outputs #
            #############################
    
            # Variables to be written.
            outField = fieldoutList
    
            for field in outField:
    
                print('creating output file for field ',field)
    
                # Create the field output file.
                outfilenamevar = outputfoldervar + '/' + field  + '_' + model + '_' + exp + '.nc'
        
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
                
    
                if field in ST_list:
    
                    time    = ncid.createVariable('time', 'f4', ('time'))
                    time.units         = "days since 1850-01-01" 
                    time.calendar      = "standard" 
                    time.axis          = "T" 
                    time.long_name     = "time" 
                    time.standard_name = "time" 
                    days_end = [(datetime.date(round(yr),1,1)-start_date).days for yr in timeS]
                    time[:] = days_end
    
                    
                    if field in ['lithk']: 
                        lithk = ncid.createVariable(field, 'f4', ('time','y','x'))
                        lithk.units         = 'm'
                        lithk.long_name     = 'ice thickness'
                        lithk.standard_name = 'land_ice_thickness'
                        lithk[:,:,:] = thkout[:,:,:]        
        
                    if field in ['orog']: 
                        orog = ncid.createVariable(field, 'f4', ('time','y','x'))
                        orog.units         = 'm'
                        orog.long_name     = 'surface elevation'
                        orog.standard_name = 'surface_altitude'
                        orog[:,:,:] = usurfout[:,:,:]         
    
                    if field in ['base']: 
                        base = ncid.createVariable(field, 'f4', ('time','y','x'))
                        base.units         = 'm'
                        base.long_name     = 'base elevation'
                        base.standard_name = 'base_altitude'
                        base[:,:,:] = lsurfout[:,:,:]         
    
                    if field in ['topg']: 
                        topg = ncid.createVariable(field, 'f4', ('time','y','x'))
                        topg.units         = 'm'
                        topg.long_name     = 'bedrock elevation'
                        topg.standard_name = 'bedrock_altitude'
                        topg[:,:,:] = topgout[:,:,:]      
    
                    if field in ['litemptop']: 
                        litemptop = ncid.createVariable(field, 'f4', ('time','y','x'))
                        litemptop.units         = 'K'
                        litemptop.long_name     = 'surface temperature'
                        litemptop.standard_name = 'temperature_at_top_of_ice_sheet_model'
                        #litemptop[:,:,:] = artmout[:,:,:]+273.15      
                        litemptop[:,:,:] = ttempout[:,:,:]+273.15      
    
                    if field in ['litempmean']: 
                        litemptop = ncid.createVariable(field, 'f4', ('time','y','x'))
                        litemptop.units         = 'K'
                        litemptop.long_name     = 'vertically averaged ice temperature'
                        #litemptop.standard_name = 'mean_ice_sheet_temperature'
                        litemptop[:,:,:] = mtempout[:,:,:]+273.15
                        
                    if field in ['litempbotgr']: 
                        litempbotgr = ncid.createVariable(field, 'f4', ('time','y','x'))
                        litempbotgr.units         = 'K'
                        litempbotgr.long_name     = 'basal temperature beneath grounded ice sheet'
                        litempbotgr.standard_name = 'temperature_at_base_of_ice_sheet_model'
                        litempbotgr[:,:,:] = btemp_gr[:,:,:]+273.15
    
                    if field in ['litempbotfl']:
                        litempbotfl = ncid.createVariable(field, 'f4', ('time','y','x'))
                        litempbotfl.units         = 'K'
                        litempbotfl.long_name     = 'basal temperature beneath floating ice shelf'
                        litempbotfl.standard_name = 'temperature_at_base_of_ice_sheet_model'
                        litempbotfl[:,:,:] = btemp_fl[:,:,:]+273.15     
    
                    if field in ['sftgif']:
                        sftgif = ncid.createVariable(field, 'f4', ('time','y','x'))
                        sftgif.units         = '1'
                        sftgif.long_name     = 'land ice area fraction'
                        sftgif.standard_name = 'land_ice_area_fraction'
                        sftgif[:,:,:] = f_ice[:,:,:]      
    
                    if field in ['sftgrf']:
                        sftgrf = ncid.createVariable(field, 'f4', ('time','y','x'))
                        sftgrf.units         = '1'
                        sftgrf.long_name     = 'grounded ice sheet area fraction'
                        sftgrf.standard_name = 'grounded_ice_sheet_area_fraction'
                        sftgrf[:,:,:] = f_ground[:,:,:]      
    
                    if field in ['sftflf']:
                        sftflf = ncid.createVariable(field, 'f4', ('time','y','x'))
                        sftflf.units         = '1'
                        sftflf.long_name     = 'floating ice sheet area fraction'
                        sftflf.standard_name = 'floating_ice_shelf_area_fraction'
                        sftflf[:,:,:] = f_float[:,:,:]      
    
    
    
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
        
                    if field in ['hfgeoubed']: 
                        hfgeoubed = ncid.createVariable(field, 'f4', ('time','y','x'))
                        hfgeoubed.units         = 'W m-2'
                        hfgeoubed.long_name     = 'geothermal heat flux'
                        hfgeoubed.standard_name = 'upward_geothermal_heat_flux_in_land_ice'
                        hfgeoubed[:,:,:] = bheatflxout[:,:,:]         
                
                print( 'Created field output file', outfilenamevar)
    
                ncid.close()

    print( 'Done with writing output files for ',tier)


# Close the log file
file_object.close()
    
# Done writing the output files
print( 'Done with writing the output files')
