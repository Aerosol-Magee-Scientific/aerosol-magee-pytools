# Copyright (c) 2026 Aerosol d.o.o.
# Licensed under the Aerosol Magee Scientific Software License
# (see LICENSE file for details)


# default MAC values
SIGMA = {340: 20.1,
         370: 18.47,
         400: 17.09,
         430: 15.90,
         470: 14.54,
         520: 13.14,
         525: 13.02,
         565: 12.73,
         590: 11.58,
         630: 10.84,
         660: 10.35,
         700: 9.77,
         880: 7.77,
         950: 7.19}

# default source apportionment parameters
ALPHA_FF = 1.0
ALPHA_BB = 2.0
ALPHA_BC = 1.0

# ACTRIS harmonization factor
H_STAR = 1.76

WAVELENGTHS_COMMON = [370, 470, 520, 590, 880, 950]


class Aethalometer:
    LIST_TYPES = ['AE33', 'AE36s', 'AE36']
    ATN_MAX = 120
    ATN_F1 = 10
    ATN_F2 = 30

class AE33(Aethalometer):
    WAVELENGTHS = [370, 470, 520, 590, 660, 880, 950]

class AE36s(Aethalometer):
    WAVELENGTHS_P01 = [340, 370, 400, 470, 520, 590, 660, 880, 950]
    WAVELENGTHS = [340, 370, 400, 470, 520, 590, 630, 880, 950]

class AE36(Aethalometer):
    WAVELENGTHS = [370, 470, 520, 590, 630, 880, 950]