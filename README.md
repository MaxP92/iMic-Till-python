# iMic-Till-python
Python-based implementation of an iMic (Till Photonics) control (unofficial)

--- Needed ---
- ctypes
- msl-loadlib (github.com/MSLNZ/msl-loadlib) if using Python x64
- pyQt (to include in a GUI, but not mandatory)

---- Files -----
- tillimic.dll : the x32 DLL you need to control the instrument
- iMIC-SDK-0.2.19.pdf : the description of the API (official)
- iMICsetup.exe : the iMic soft (official), just for info
- x32 folder : if you are using Python 32 bits
- x64 folder : if you are using Python 64 bits
 
 --------------
 
  -----------------
  Info :  
  The x32 version controls directly the DLL.  
  The x64 uses msl-loadlib to create a client/server interface to control in Python 64bits.  
  Use "open_com" to open the COM port and get an handle. After use "imic_ini" to init the instrument.  
  You can now use the other functions.  
  The code has been extracted from a GUI, and has not been (yet?) adapted to a basic use. But any Python programmer should find what he wants inside it by cherry-picking !
  
  -----------------
 
Consider saying thanks ! --> maxime.pinsard@outlook.com



--------------------------
Copyright to the code is held by the following parties:
Copyright (C) 2017 Maxime Pinsard, INRS-EMT Varennes

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation, version 2.1.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

- Name: iMic-Till-python
- Version: 0.1
- Author: Maxime PINSARD
- Author-email: maxime.pinsard@outlook.com
        
- Platform: Windows
- Classifier: Intended Audience :: Science/Research
- Classifier: License :: OSI Approved :: GNU General Public License v2 (GPLv2)
- Classifier: Programming Language :: Python
- Classifier: Operating System :: Microsoft :: Windows
