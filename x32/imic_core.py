# -*- coding: utf-8 -*-
"""
Created on August 26 09:35:13 2016

@author: Maxime P.

From the iMic SDK 0.2.19 lib & documentation
Till Photonics Gmbh, now FEI Inc.
see corresponding pdf for other functions

"""
import os
import ctypes

def close_imic(lib_imic, handle1):
    
    errorcode = lib_imic.IMIC_Close (handle1)
    
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)
    

def open_lib_imic(path_computer):
    
    #os.chdir('%s/Essais/microscope/gui control motor+imic' % self.path_computer)
    
    import _imicinitmp
    
    path00 = '%s/Packages' % path_computer
    
    # ******* open lib ************************************************************
    
    if (os.name != 'nt'):
        raise Exception("Your operating system is not supported. " \
                    "Imic API only works on Windows.")  
    lib_imic = None
    try:
        filename = ctypes.util.find_library("tillimic")
    except:
        filename = None
                
    if (filename is not None):
        lib_imic = ctypes.windll.LoadLibrary(filename)
        print('Lib iMic loaded by windll and util')
    else:
        filename = "%s/tillimic.dll" % path00
        lib_imic = ctypes.CDLL(filename)
        print('Lib iMic loaded by CDLL')
        if (lib_imic is None):
            filename = "%s/tillimic.dll" % os.path.dirname(sys.argv[0])
            lib_imic = ctypes.windll.LoadLibrary(lib_imic)
            print('Lib iMic loaded by windll')
            if (lib_imic is None):
                raise Exception("Could not find shared library tillimic.dll.")
    
    _imicinitmp.set_ctypes_argtypes_mp(lib_imic) # load function properties
    
    # # print('lib iMic loaded')
    
    return lib_imic
    
    
def open_com_imic(lib_imic, port_imic):    

    
    # ******* open com *********************************************************************
    
    # see your config on windows' device manager
    port_imic = port_imic.encode('utf-8')
    port_imic = ctypes.c_char_p(port_imic)
        
    handle1 = ctypes.c_void_p()
    
    errorcode = lib_imic.IMIC_OpenByRS232(port_imic, ctypes.byref(handle1))
    
    # DO NOT PUT exception on errorcode, it's not equal to 0 if ok !!
    if errorcode == 6:
        raise Exception("wrong handle\n")
    elif errorcode == 10:
        raise Exception("failed to open com port\n")
    # # else:
    # #     print(errorcode)
        
    print('iMic handle : %d' % handle1.value)
    
    return handle1
    
    
def init_imic(lib_imic, handle1):
    
    # ******* (re)init imic *********************************************************************
    
    is_init_imic = ctypes.c_void_p()
    
    try:
        ee = lib_imic.IMIC_IsInit (handle1, ctypes.byref(is_init_imic)) # ctypes.byref
    
    except Exception as e: # error seen by Python
        print("error :" , e)
        try_rld_lib_com = 1
        
    else: # no error seen by Python
        if ee != 0: # perhaps error seen by iMic  
            # # raise Exception("error : %d\n" % ee)
            print("error : %d\n" % ee)
            try_rld_lib_com = 1
        else: # no error
            try_rld_lib_com = 0
    
    if (try_rld_lib_com or not bool(is_init_imic.value)): # if not already initialised
    
    # int32_t IMIC_Init(int32_t handle, uint8_t *ips);
        
        print('Is initing iMic : wait 10sec ... \n')
        
        try:
            ee = lib_imic.IMIC_Init (handle1, None)
        
        except Exception as e: # error seen by Python
            print("error when trying to init iMic:" , e)
            ee = 1 # != 0 so will reload
        
        # if ee != 0: # error seen by Python or iMic
                         
                # errorcode = lib_imic.IMIC_OpenByRS232(port_imic, ctypes.byref(handle1))
                # if errorcode == 6:
                #     raise Exception("wrong handle\n")
                # elif errorcode == 10:
                #     raise Exception("failed to open com port\n")
                # try:
                #     ee = lib_imic.IMIC_Init (handle1, None)
                # except Exception as e: # error seen by Python
                #     print("error when trying to init iMic:" , e)
                #     ee = 1 # != 0 so will reload
                #     # other errors handled after
        
        if ee == 6:
            print("wrong handle\n") # raise Exception
        elif ee == 10:
            print("failed to open com port\n")
        elif ee == 11:
            print("Failed to initialise\n")
        elif ee == 0:   
            print("iMic initiated.\n")
            
    return ee
            
            
def filter_pos_top_get(lib_imic, handle1, posFilt_1_get):    
    
    # filter 1 (filtre du haut)
    
    # # posFilt_1_get = ctypes.c_void_p()
    
    errorcode = lib_imic.IMIC_GetFilterChangerPos (handle1, 0, posFilt_1_get)
    
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)
        
    return posFilt_1_get[0]     


def filter_pos_bottom_get(lib_imic, handle1, posFilt_2_get):
    
    # filter 2
    
    errorcode = lib_imic.IMIC_GetFilterChangerPos (handle1, 1, posFilt_2_get)
    
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)
    
    return posFilt_2_get[0] 

    ## set filters pos
    
def filter_pos_top_set(lib_imic, handle1, posFilt_top):
    
    # # filter 1 (filtre top)
    
    errorcode = lib_imic.IMIC_SetFilterChangerPosAbs (handle1, 0, posFilt_top)
    
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)
        
def filter_pos_bottom_set(lib_imic, handle1, posFilt_bottom):   
     
    # # filter 2 (bottom)
    
    # # = 1 for mirror of stage path
    
    errorcode = lib_imic.IMIC_SetFilterChangerPosAbs (handle1, 1, posFilt_bottom)
    
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)
        
def obj_choice_set(lib_imic, handle1, obj_choice):
    
    if (obj_choice != 0 and obj_choice != 1):
        obj_choice = 0
        print("obj turret out of range")
        
    # 0 = 20X, 1 = 40X
    errorcode = lib_imic.IMIC_SetObjectiveTurretPosAbs(handle1, obj_choice)
    
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)
    
def obj_choice_get(lib_imic, handle1, choice_obj):

    # # choice_obj = ctypes.c_void_p()
    
    errorcode =  lib_imic.IMIC_GetObjectiveTurretPos (handle1, choice_obj)
    
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)

    return choice_obj[0]
    
def pos_Z_motor_set(lib_imic, handle1, posZ_motor):
    
    # stage Z
    
    # zPosition1 = 20.235 # up to 20.5
    
    # upt to 1 000 000 000
    # init 2576980378
    
    max_Z_motor = 22 # mm
    
    if posZ_motor > max_Z_motor:
        posZ_motor = max_Z_motor
        print('max Z motor is %s' % max_Z_motor)
    elif posZ_motor < 0:
        posZ_motor = 0
        print('min Z motor is 0')
    
    errorcode = lib_imic.IMIC_SetZPosAbs (handle1, 0, posZ_motor)
    
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)

def pos_Z_piezo_set(lib_imic, handle1, posZ_piezo):
    
    # piezo Z
    # max = .25 !!!!
    # upt to 1 000 000 000
    # init 2576980378
    
    if posZ_piezo > 0.25:
        posZ_piezo = 0.25
        print('max Z piezo is 0.25')
    elif posZ_piezo < 0:
        posZ_piezo = 0
        print('min Z piezo is 0')
    
    print('told piezoZ to go to', posZ_piezo)
    
    errorcode = lib_imic.IMIC_SetZPosAbs (handle1, 1, posZ_piezo)
    
    if errorcode != 0:
        if errorcode == 12:
            raise Exception("unknown error")
        raise Exception("error : %d\n" % errorcode)
        
        
def pos_Z_motor_get(lib_imic, handle1, posZ_mtr_got):

    # stage Z
    
    # # posZ_mtr_got = ctypes.c_void_p()
    
    errorcode = lib_imic.IMIC_GetZPos (handle1, 0, posZ_mtr_got)
    
    if errorcode != 0:   
        
        if errorcode == 2:
            raise Exception("missing Z axis\n")
        else:
            raise Exception("error : %d\n" % errorcode)
    
    if posZ_mtr_got[0] == 0:
        print('PosZ is 0')
    else:
        pass
        # # print("Z motor (core)= %.3f" % posZ_mtr_got[0])
    
    return posZ_mtr_got[0] 
    
def pos_Z_piezo_get(lib_imic, handle1, posZ_pz_got):

    # piezo Z
    
    # # posZ_pz_got = ctypes.c_void_p()
    
    errorcode = lib_imic.IMIC_GetZPos (handle1, 1, posZ_pz_got)
    
    if errorcode != 0:   
        if errorcode == 2:
            raise Exception("missing Z axis\n")
        else:
            raise Exception("error : %d\n" % errorcode)
    
    if posZ_pz_got[0] == 0:
        print('PiezoZ is 0')
    else:
        pass
        # # print("Z piezo = %.3f" % posZ_pz_got[0])
    
    return posZ_pz_got[0]
    
## not used functions

def pos_Z_motor_relative_set(handle1):
    
    zPositionRel = 10
    # upt to 1 000 000 000
    # init 2576980378
        # 1316134912
    
    errorcode = self.lib_imic.IMIC_SetZPosRel (handle1, 0, zPositionRel)
    # errorcode = lib.IMIC_SetZPosAbs (handle1, 0, 2576980378)
    
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)
        
def number_filter_get(handle1, nb_filters):

    
    errorcode = self.lib_imic.IMIC_GetNumberOfFilterChangers (handle1, nb_filters)
            
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)
        
    return nb_filters[0]

def pos_XY_get(handle1, xPosition, yPosition): # surely with old PRIOR stage
        
    # int IMIC_GetXYPos (void  handle, double  xPosition, double  yPosition)
    
    # xPosition = ctypes.c_void_p()
    # yPosition  = ctypes.c_void_p()
    # use a pointer to a double (see getZ example)
        
    errorcode = self.lib_imic.IMIC_GetXYPos (handle1, xPosition, yPosition)
    
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)
        
    return xPosition[0], yPosition[0]

def pos_X_set(handle1, xPosition): # surely with old PRIOR stage
        
    errorcode = self.lib_imic.IMIC_SetXPosAbs (handle1, xPosition)
    
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)
        
def pos_Y_set(handle1, yPosition): # surely with old PRIOR stage
        
    errorcode = self.lib_imic.IMIC_SetYPosAbs (handle1, yPosition)
    
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)
        
def nb_Z_axes_get(handle1, znumber_axe):

    # Returns the current number of axes.
    # The indices are 0-based. Thus, the last legal index is number-1.

    # znumber_axes = ctypes.c_void_p()
    
    errorcode = self.lib_imic.IMIC_GetNumberOfZAxes (handle1, znumber_axe)
    
    if errorcode != 0:   
        raise Exception("error : %d\n" % errorcode)
        
    print("Z nb axes = %d" % znumber_axes.value)
    
    return znumber_axe[0]