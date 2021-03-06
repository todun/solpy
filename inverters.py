# Copyright (C) 2012 Nathan Charles
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import json
import os
SPATH = os.path.dirname(os.path.abspath(__file__))
class inverter(object):
    """Sandia Model"""
    #Inverter Output = Array STC power * Irradiance * Negative Module Power Tolerance * Soiling * Temperature factor * Wiring efficiency * Inverter efficiency
    #PVWATTS Default
    #Mismatch      0.97 - 0.995
    mismatch = .98
    #Diodes and connections      0.99 - 0.997
    connections = .995
    #DC wiring     0.97 - 0.99
    dc_wiring = .98
    #AC wiring0.98 - 0.993
    ac_wiring = .99
    #Soiling       0.30 - 0.995
    soiling = .95
    #System availability     0.00 - 0.995
    availability = 0.98
    #not included in PVWATTS/SAM
    NMPT = .97
    Tfactor = .98

    def __init__(self, model, array, orientation=[(180,0)]):
        self.array = array
        self.orientation = orientation
        self.properties = None
        inverters = json.loads(open(SPATH + '/si.json').read())
        for i in inverters:
            try:
                if i['inverter']==model:
                    self.properties = i
                    break
            except:
                print "Error on key with data",i
                raise
        if self.properties == None:
            raise Exception("Inverter not found")
        self.ac_voltage = self.properties['ac_voltage']
        self.inverter = self.properties['inverter']
        self.vdcmax = self.properties['vdcmax']
        self.Pdco = self.properties['pdco']
        self.Paco = self.properties['paco']
        self.pnt = self.properties['pnt']
        self.Pso = self.properties['pso']
        self.Vdco = self.properties['vdco']
        self.C0 = self.properties['c0']
        self.C1 = self.properties['c1']
        self.C2 = self.properties['c2']
        self.C3 = self.properties['c3']
        self.idcmax = self.properties['idcmax']
        self.mppt_hi = self.properties['mppt_hi']
        self.mppt_low = self.properties['mppt_low']
        self.make,self.model = self.inverter.split(":",2)
        self.derate = self.mismatch * self.soiling * self.dc_wiring * self.connections \
                * self.availability# * m.Tfactor #* m.NMPT
        #self.derate = self.dc_wiring

    def Pac(self, Insolation, tCell = 25):
        Pdc = self.array.output(Insolation, tCell)
        Vdc = self.array.Vdc()
        A = self.Pdco * (1 + self.C1 * (Vdc - self.Vdco))
        B = self.Pso * (1 + self.C2 * (Vdc - self.Vdco))
        C = self.C0 * (1 + self.C3 * (Vdc - self.Vdco))
        Pac = ((self.Paco / (A - B)) - C*(A - B))*(Pdc- B) + C *(Pdc - B)**2
        #clip at Paco
        return min(float(self.Paco),Pac * self.derate)

    def I(self,Insolation,Vac):
        return self.Pac(Insolation)/Vac

def manufacturers():
    a =  [i['inverter'].split(":")[0] for i in json.loads(open(SPATH + '/si.json').read()) ]
    a.sort()
    b = [i for i in set(a)]
    b.sort()
    return b

def models(manufacturer = None):
    """returns list of available inverter models"""
    if manufacturer ==None:
        return [i['inverter'] for i in json.loads(open(SPATH + '/si.json').read()) ]
    else:
        a = []
        for i in json.loads(open(SPATH + '/si.json').read()):
            if i['inverter'].find(manufacturer) != -1:
                a.append(i['inverter'])
        return a


def insolationToA(ins, peakA):
    """scale current in response to insolation"""
    pass

if __name__=="__main__":
    from modules import *

    p = module('Mage Solar : Powertec Plus 245-6 PL *')
    e = inverter("Enphase Energy: M215-60-SIE-S2x 240V",p)
    s = pvArray(p,14,2)
    s = pvArray(p,14,20*8)
    #si = sb6000us(s)

    print e.Pac(950)
    print e.I(960,240)

