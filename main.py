"""
    Convert the frequency database csv file from the radioreference.com site to the Icom PCR1000 MCH file

    Notes:
        The name of the MCH file will have the same base name as the csv file.
            aid_7768.csv --> aid_7768.mch
            metro_22.csv --> metro_22.mch

        Exit codes:
            1 - CSV input file selection cancelled
            2 - file names verification failed (user clicked no)

    Author William Main - mainmeister@gmail.com
"""

import csv              # read radioreference csv file
import configparser     # write PCR1000 MCH file
from easygui import *   #quasi-cli-gui app
import os

csv_filename = 'metro_22.csv'
mch_filename = 'metro_22.mch'

tf=fileopenbox("Frequency Database File", "Select Frequency Database File")
if tf == None:
    exit(1)
else:
    csv_filename = tf

basename, ext = os.path.splitext(csv_filename)
mch_filename = basename + '.mch'

if not ynbox("CSV: %s\nMCH: %s" % (csv_filename, mch_filename), "Are these files correct?"):
    exit(2)
mchdict = configparser.ConfigParser(delimiters=('='))
mchdict.add_section('REV')
mchdict.set('REV', 'ID', '1.0.0')
mchdict.set('REV', 'APP', 'IC-PCR1000  Revision 2.2')

with open(mch_filename, mode='w') as mchfile:
    mchdict.write(mchfile, space_around_delimiters = False)

banks = {}
with open(csv_filename) as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for transmitter in csv_reader:
        #print(transmitter)
        bankname = transmitter['Agency/Category']
        description = transmitter['Description']
        pltone = transmitter['PL Tone']
        frequency = transmitter['Frequency Output']
        mode = transmitter['Mode']
        if mode == 'FM':
            filter = '15k'
            step = '250KHz'
        elif mode == 'FMW':
            filter = '230k'
            step = '250KHz'
        elif mode == 'AM' or mode == 'LSB' or mode == 'USB' or mode == 'CW':
            filter = '3k'
            step = '25KHz'
        else:
            if float(frequency) > 30:
                filter = '15k'
                step = '250KHz'
            else:
                filter = '3k'
                step = '25KHz'
        #print('bankname: %s, description: %s, pltone: %s, frequency: %s, mode: %s, filter: %s, step: %s' % (bankname, description, pltone, frequency, mode, filter, step))
        print(mode)