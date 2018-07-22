# -*- coding: utf-8 -*-
"""
Created on Sept 12 15:35:13 2016

@author: Maxime PINSARD
"""

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
from modules import param_ini
import ctypes

class Worker_imic(QObject):

    progress_motor_signal = pyqtSignal(int)
    progress_piezo_signal = pyqtSignal(int)
    fltr_top_choice_set = pyqtSignal(int)
    fltr_bottom_choice_set = pyqtSignal(int)
    obj_choice_set = pyqtSignal(int)
    posZ_mtr_str = pyqtSignal(int)
    posZ_piezo_str = pyqtSignal(int)
    imic_was_ini_signal = pyqtSignal(bool)


    def __init__(self, path_computer, queue_disconnections, motorZ_changeDispValue_signal, piezoZ_changeDispValue_signal): 
    
        super(Worker_imic, self).__init__()
        
        self.path_computer = path_computer

        # otherwise it is imported every time a galvo scan is launched ...
        print('Imported imic_core...')
        import imic_core
        import time, numpy
        # otherwise it is imported every time a galvo scan is launched ...
        
        self.imic_core = imic_core
        self.time = time
        self.queue_disconnections = queue_disconnections
        self.motorZ_changeDispValue_signal = motorZ_changeDispValue_signal
        self.piezoZ_changeDispValue_signal = piezoZ_changeDispValue_signal
        
        a = numpy.array([0.0], dtype=numpy.float64)
        self.empty_array_one = a.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
        
        b = numpy.array([0], dtype=numpy.int16)
        self.empty_array_int = b.ctypes.data_as(ctypes.POINTER(ctypes.c_int16))
        
        self.minTime_wait2read_ms = 200 # ms

        
    # def __del__(self):
    #     self.wait()

    @pyqtSlot()
    def open_com(self):
        
        # print("Slot is executed in thread : ", self.thread().currentThreadId())
        
        if (hasattr(self, 'lib_imic') and hasattr(self, 'handle1')):
            
            # self.imic_core.close_imic(self.lib_imic, self.handle1)
            handle_lib = self.lib_imic._handle # obtain the DLL handle
            ctypes.windll.kernel32.FreeLibrary(handle_lib)
            del self.lib_imic, self.handle1
                    
        self.lib_imic = self.imic_core.open_lib_imic(self.path_computer) # open library
        self.handle1 = self.imic_core.open_com_imic(self.lib_imic, param_ini.port_imic) # open COM port
        
    @pyqtSlot()
    def imic_ini(self):
        # is called by init_imic_button
        
        # print("Slot is executed in thread : ", self.thread().currentThreadId())
        
        # # print(self.handle1)
  
        ee = self.imic_core.init_imic(self.lib_imic, self.handle1) 
        
        if ee != 0: # error seen by Python or iMic
            self.imic_was_ini_signal.emit(False)
            return # out the func
       
        # get infos ************************************
        self.posFilt_1_get = self.imic_core.filter_pos_top_get(self.lib_imic, self.handle1, self.empty_array_int)
        self.posFilt_2_get = self.imic_core.filter_pos_bottom_get(self.lib_imic, self.handle1, self.empty_array_int)
        
        self.choice_obj = self.imic_core.obj_choice_get(self.lib_imic, self.handle1, self.empty_array_int)
        
        self.posZ_motor_get = self.imic_core.pos_Z_motor_get(self.lib_imic, self.handle1, self.empty_array_one)
        self.posZ_piezo_get = self.imic_core.pos_Z_piezo_get(self.lib_imic, self.handle1, self.empty_array_one)
        
        # set param ***************************************************
        # self.posFilt_1_get = 0
        # self.posFilt_2_get = 0
        # self.choice_obj = 0
        # self.posZ_motor_get = 0
        # self.posZ_piezo_get = 0
            
        # else:
        #     self.posFilt_1_get = self.posFilt_1_get.value
        #     self.posFilt_2_get = self.posFilt_2_get.value
        #     self.choice_obj = self.choice_obj.value
        #     self.posZ_motor_get.value = self.posZ_motor_get
        #     self.posZ_piezo_get.value = self.posZ_piezo_get
        
        self.fltr_top_choice_set.emit(self.posFilt_1_get)
        
        self.fltr_bottom_choice_set.emit(self.posFilt_2_get) 
        
        self.obj_choice_set.emit(self.choice_obj) 
        
        self.posZ_mtr_str.emit(self.posZ_motor_get)
        
        self.posZ_piezo_str.emit(self.posZ_piezo_get)
        
        self.imic_was_ini_signal.emit(True)
        
    @pyqtSlot(float)
    def change_z_motor_meth(self, posZ_motor):
        
        # print("Slot is executed in thread : ", self.thread().currentThreadId())
        
        max_pos_Z_motor = 22.0
        speed_motorZ_imic = 2 # mm/s
        
        self.posZ_motor_get = self.imic_core.pos_Z_motor_get(self.lib_imic, self.handle1, self.empty_array_one)     
           
        self.posZ_motor = posZ_motor
        self.imic_core.pos_Z_motor_set(self.lib_imic, self.handle1, posZ_motor)
        
        # self.time.sleep(abs(self.posZ_motor_get - posZ_motor)/speed_motorZ_imic + self.minTime_wait2read_ms/1000) # it already sleep
        self.posZ_motor_get = self.imic_core.pos_Z_motor_get(self.lib_imic, self.handle1, self.empty_array_one) # get real pos
        print("Z motor (worker)= %.3f mm" % self.posZ_motor_get)
        
        self.progress_motor_signal.emit(round(self.posZ_motor_get/max_pos_Z_motor*100))
        self.motorZ_changeDispValue_signal.emit(self.posZ_motor_get) # in mm
        
    @pyqtSlot(float)
    def change_z_piezo_meth(self, posZ_piezo):
        
        max_pos_Z_piezo = 0.25
                
        self.posZ_piezo = posZ_piezo
        
        self.imic_core.pos_Z_piezo_set(self.lib_imic, self.handle1, posZ_piezo)
        
        self.posZ_piezo_get = self.imic_core.pos_Z_piezo_get(self.lib_imic, self.handle1, self.empty_array_one) # in mm
        self.posZ_piezo_get = round(self.posZ_piezo_get*1000*100)/100/1000  # in mm
        print("Z piezo (got) = %.4f um" % (self.posZ_piezo_get*1000))
        
        self.progress_piezo_signal.emit(round(self.posZ_motor_get/max_pos_Z_piezo)*100)
        self.piezoZ_changeDispValue_signal.emit(self.posZ_piezo_get) # in mm
        
    @pyqtSlot(int)
    def filter_top_meth(self, posFilt_top):
        
        self.posFilt_top = posFilt_top
        
        self.imic_core.filter_pos_top_set(self.lib_imic, self.handle1, posFilt_top)
        
        self.time.sleep( self.minTime_wait2read_ms/1000)
        
        posFilt_1_got = self.imic_core.filter_pos_top_get(self.lib_imic, self.handle1, self.empty_array_int)
        
        self.fltr_top_choice_set.emit(posFilt_1_got)
        
        
    @pyqtSlot(int)
    def filter_bottom_meth(self, posFilt_bottom):
        
        self.posFilt_bottom = posFilt_bottom
        
        self.imic_core.filter_pos_bottom_set(self.lib_imic, self.handle1, posFilt_bottom)
        
        self.time.sleep( self.minTime_wait2read_ms/1000)
        
        posFilt_2_got = self.imic_core.filter_pos_bottom_get(self.lib_imic, self.handle1, self.empty_array_int)
        self.fltr_bottom_choice_set.emit(posFilt_2_got) 

        
    @pyqtSlot(int)
    def obj_choice_meth(self, obj_choice):
        
        self.obj_choice = obj_choice
        
        self.imic_core.obj_choice_set(self.lib_imic, self.handle1, obj_choice)
        
        self.time.sleep( self.minTime_wait2read_ms/1000)
        
        choice_obj = self.imic_core.obj_choice_get(self.lib_imic, self.handle1, self.empty_array_int)
        
        self.obj_choice_set.emit(choice_obj) 

        
    @pyqtSlot()
    def update_Z_values_meth(self):
        
        self.posZ_motor_get = self.imic_core.pos_Z_motor_get(self.lib_imic, self.handle1, self.empty_array_one)
        self.motorZ_changeDispValue_signal.emit(self.posZ_motor_get) # in mm
        
        self.posZ_piezo_get = self.imic_core.pos_Z_piezo_get(self.lib_imic, self.handle1, self.empty_array_one)
        self.piezoZ_changeDispValue_signal.emit(self.posZ_piezo_get) # in mm
    
    def close_imic_meth(self, the_end):
        # print('In closing Imic !')
        
        if (hasattr(self, 'lib_imic') and hasattr(self, 'handle1')):
            
            self.imic_core.close_imic(self.lib_imic, self.handle1)
            handle_lib = self.lib_imic._handle # obtain the DLL handle
            ctypes.windll.kernel32.FreeLibrary(handle_lib)
            del self.lib_imic, self.handle1
        
        if the_end:
            self.queue_disconnections.put(1) # tell the GUI the iMic is closed : iMic's signature is 1