solpy
-------
Solpy is a python library to model solar system power performance similar to PVWatts or NREL's System Advisor Model(SAM).  I initially started writing this while working in Bangladesh as fairly crude calculator to go from a fisheye panorama to a csv of vectors for shading calculations, however there were several pieces that were added to make it a bit more useful for both analyis and design.  
Daniel Thomas did work adding the Tang evacuated glass tube model. Pyephem was added for solar positioning.  There is also a simple module for reading TMY3 data. This tool is rudimentary, but functional.  

This is primarily a research and analysis tool and there is no guarantee on the calculations.

Features
--------
-Liu & Jordan diffuse irradiance model  
-Perez et al. diffuse irradiance model  
-Sandia Inverter model  
-NEC voltage drop caculations  

Files
-----
-enphase.py - Enphase API wrapper  
-epw.py - EPW weather data  
-expedite.py - calculate information needed for the expedited permit process  
-fisheye.py - fisheye image to shading vectors  
-forecast.py - forecast.io API wrapper  
-noaa.py - NOAA weather data API wrapper  
-pv.py - system performance prediction  
-pvcli - cli interface to pv modeling--
-tmy3.py - read tmy3 data  
-vd.py - voltage drop  

Usage
-----
PV systems are descibed with json. For example:

    {"system_name":"System Name",
        "zipcode":"17601",
        "tilt":34,
        "azimuth":180,
        "phase":1,
        "voltage":240,
        "array":[
            {"inverter":"SMA America: SB6000US 240V",
            "panel":"Mage Solar : Powertec Plus 250-6 MNCS",
            "series":14,
            "parallel":2}
            ]
        }

If that json was in a file called template.json, the command to model it would be;

pvcli -f template.json

Ipython
-------
This is the sort of project that lends itself nicely to ipython.  Since discovering that project I've tried to make things flow naturally in that enviroment. I really like the inline graphics of the qtconsole.

$ipython qtconsole --colors=Linux --pylab=inline

![example](http://char1es.net/ipython_pv_example.png)
