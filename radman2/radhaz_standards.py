#!/usr/bin/env python3
#
#   RADHAZ Exposure Limit Conversions
#

import logging
import numpy as np

class FCC96326(object):
    """
    Definition and conversions for the FCC 96-326 RADHAZ standard

    Note that we refer to the standards 'controlled' limits as 'Occupational', and
    the 'uncontrolled' limits as 'General Public'.

    Reference: https://transition.fcc.gov/Bureaus/Engineering_Technology/Orders/1996/fcc96326.pdf
    """

    def __init__(self, occupational=True):


        if occupational:
            self.name = "FCC 96-326 Controlled Environments (Occupational)"
            self.init_tables_occupational()
        else:
            self.name = "FCC 96-326 Uncontrolled Environments (General Public)"
            self.init_tables_general_public()

    
    def init_tables_occupational(self):
        """
        Generate the E and H-field limits for the FCC 96-326 'Controlled Environment'
        in 1 kHz resolution.
        (We refer to this as 'occupational')
        """

        self.frequency_mhz = np.array([])
        self.efield = np.array([])
        self.hfield = np.array([])

        # 0.003 - 0.1 MHz. E = 614 V/m, H = 163 A/m
        _freq = np.arange(0.003, 0.1, 0.01)
        _efield = np.ones(len(_freq)) * 614
        _hfield = np.ones(len(_freq)) * 163

        self.frequency_mhz = np.append(self.frequency_mhz, _freq)
        self.efield = np.append(self.efield, _efield)
        self.hfield = np.append(self.hfield, _hfield)

        # 0.1 - 3.0 MHz. E = 614 V/m, H = 16.3/f A/m
        _freq = np.arange(0.1, 3.0, 0.01)
        _efield = np.ones(len(_freq)) * 614
        _hfield = 16.3 / _freq

        self.frequency_mhz = np.append(self.frequency_mhz, _freq)
        self.efield = np.append(self.efield, _efield)
        self.hfield = np.append(self.hfield, _hfield)

        # 3.0-30 MHz. E = 1842/f V/m, H = 16.3/f A/m
        _freq = np.arange(3.0, 30.0, 0.01)
        _efield = 1842.0 / _freq
        _hfield = 16.3 / _freq

        self.frequency_mhz = np.append(self.frequency_mhz, _freq)
        self.efield = np.append(self.efield, _efield)
        self.hfield = np.append(self.hfield, _hfield)

        # 30-100 MHz. E = 61.4 V/m, H = 16.3/f A/m
        _freq = np.arange(30.0, 100.0, 0.01)
        _efield = np.ones(len(_freq)) * 61.4
        _hfield = 16.3 / _freq

        self.frequency_mhz = np.append(self.frequency_mhz, _freq)
        self.efield = np.append(self.efield, _efield)
        self.hfield = np.append(self.hfield, _hfield)

        # 100-300 MHz E = 61.4 V/m, H = 0.163 A/m
        _freq = np.arange(100.0, 300.0, 0.01)
        _efield = np.ones(len(_freq)) * 61.4
        _hfield = np.ones(len(_freq)) * 0.163

        self.frequency_mhz = np.append(self.frequency_mhz, _freq)
        self.efield = np.append(self.efield, _efield)
        self.hfield = np.append(self.hfield, _hfield)

        # 300-3000 MHz. S = f/300 W/m^2, E = sqrt(S*377), H = sqrt(S/377) (plane-wave approximation)
        _freq = np.arange(300.0, 3000.0, 0.01)
        _s = _freq / 300 # W / m^2
        _efield = np.sqrt(_s*377.0)
        _hfield = np.sqrt(_s/377.0)

        self.frequency_mhz = np.append(self.frequency_mhz, _freq)
        self.efield = np.append(self.efield, _efield)
        self.hfield = np.append(self.hfield, _hfield)

        # # 3000-300000 MHz. S = 10 W/m^2, E = sqrt(S*377), H = sqrt(S/377)
        # _freq = np.arange(3000.0, 300000.0, 0.01)
        # _s = np.ones(len(_freq)) * 10 # W / m^2
        # _efield = np.sqrt(_s*377.0)
        # _hfield = np.sqrt(_s/377.0)

        # self.frequency_mhz = np.append(self.frequency_mhz, _freq)
        # self.efield = np.append(self.efield, _efield)
        # self.hfield = np.append(self.hfield, _hfield)
        
    
    def init_tables_general_public(self):
        """
        Generate the E and H-field limits for the FCC 96-326 'Uncontrolled Environment'
        in 1 kHz resolution.
        (We refer to this as 'general public')

        TODO
        """

        self.frequency_mhz = np.array([])
        self.efield = np.array([])
        self.hfield = np.array([])


    def efield_limit(self, frequency_mhz):
        idx = (np.abs(self.frequency_mhz - frequency_mhz)).argmin()

        if np.abs(self.frequency_mhz[idx] - frequency_mhz) > 1.0:
            logging.warning(f"WARNING - Frequency {frequency_mhz:.3f} MHz is far from nearest match in table ({self.frequency_mhz[idx]} MHz.)")

        return self.efield[idx]


    def hfield_limit(self, frequency_mhz):
        idx = (np.abs(self.frequency_mhz - frequency_mhz)).argmin()
        if np.abs(self.frequency_mhz[idx] - frequency_mhz) > 1.0:
            logging.warning(f"WARNING - Frequency {frequency_mhz:.3f} MHz is far from nearest match in table ({self.frequency_mhz[idx]} MHz.)")

        return self.hfield[idx]
    

    def percentage_to_efield(self, percentage, frequency_mhz):

        if percentage == 0.0:
            return 0.0

        _percentage_db = 10*np.log10(percentage/100.0)

        return 10 **( _percentage_db / 20.0 ) * self.efield_limit(frequency_mhz)


    def percentage_to_hfield(self, percentage, frequency_mhz):
        if percentage == 0.0:
            return 0.0

        _percentage_db = 10*np.log10(percentage/100.0)

        return 10**( _percentage_db / 20.0 ) * self.hfield_limit(frequency_mhz)


    def efield_to_percentage(self, value, frequency_mhz):
        return 0.0

    def hfield_to_percentage(self, value, frequency_mhz):
        return 0.0



def choose_standard(standard_name):

    if "FCC 96-326 / Occupational" in standard_name:
        return FCC96326(occupational=True)
    else:
        return None


if __name__ == "__main__":

    standard = choose_standard("FCC 96-326 / Occupational")

    freq = 100.0

    for percent in range(0,200):
        print(f"100 MHz, {percent}% - E: {standard.percentage_to_efield(percent, freq):0.3f} V/m, H: {standard.percentage_to_hfield(percent, freq):0.3f} A/m,")


    # for freq in range(0,1000):
    #     print(f"{freq} MHz - E: {standard.efield_limit(freq):.2f} V/m, H: {standard.hfield_limit(freq):.3f} A/m")