"""
    Convert the frequency database csv file from the radioreference.com site to the Icom PCR1000 MCH file
    Author William Main - mainmeister@gmail.com

    Notes:
        The name of the MCH file will have the same base name as the csv file.
            aid_7768.csv --> aid_7768.mch
            metro_22.csv --> metro_22.mch

        Exit codes:
            1 - CSV input file selection cancelled
            2 - file names verification failed (user clicked no)

        MCH file format
            Header
                [REV]
                ID=1.0.0
                APP=IC-PCR1000  Revision 2.2

            for each memory bank (00 - 19)
            [BANK##]
            BANKNAME=THIS IS THE NAME OF THE BANK
            ACTIVECH=##
            ##=NAME,REMARK,FREQUENCY,MODE,FILTER,ATT,TS,SEL,SKIP,T-SQL
            where
                ## = 00 - 49
                NAME = is a name of the channel ie Toronto Ambulance
                REMARK = any remark about the contents ie Simplex for person to person only
                FREQUENCY = the frequency in MHz ie 124.75
                MODE = one of AM, FM, WFM, CW, USB, LSB
                FILTER = band pass filter one of
                    MODE = AM, CW, USB, LSB
                        3k, 6k
                     MODE = FM
                        6k, 15k, 50k
                    MODE = WFM
                        50k, 230k
                ATT = ON or OFF, this is the signal attenuator
                TS = ##KHz, this is the tuning step
                SEL = ON or OFF, this is whether the channel is selected
                    see set function, Memory SCAN tab
                SKIP = ON or OFF, this is whether or not to skip this channel
                    see set function, Memory SCAN tab
                T-SQL = the tone squelch frequency
                    one of OFF,
"""

import csv              # read radioreference csv file
import configparser     # write PCR1000 MCH file
from easygui import *   #quasi-cli-gui app
import os
import math

def maxchannelnumber(channels):
    maxchannel = -1
    for channel in channels:
        if str(channel).isdigit():
            channelint = int(channel)
            if channelint > maxchannel:
                maxchannel = channelint
    return maxchannel + 1

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
mchdict.optionxform = lambda option: option
mchdict.add_section('REV')
mchdict.set('REV', 'ID', '1.0.0')
mchdict.set('REV', 'APP', 'IC-PCR1000  Revision 2.2')
mchdict.set('REV', 'SOURCE', csv_filename)

#with open(mch_filename, mode='w') as mchfile:
#    mchdict.write(mchfile, space_around_delimiters = False)

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
                mode = 'FM'
                filter = '15k'
                step = '250KHz'
            else:
                mode = 'AM'
                filter = '3k'
                step = '25KHz'
        print('bankname: %s, description: %s, pltone: %s, frequency: %s, mode: %s, filter: %s, step: %s' % (bankname, description, pltone, frequency, mode, filter, step))
        banknumber = None
        for section in mchdict.sections():
            if section != 'REV':
                if bankname == mchdict.get(section, 'BANKNAME'):
                    banknumber = section
                    break
        if banknumber is None:
            banknumber = 'BANK%02d' % (len(mchdict.sections()) - 1)
            mchdict.add_section(banknumber)
            mchdict.set(banknumber, 'BANKNAME', bankname)
        mchdict.set(banknumber,"%02d" % maxchannelnumber(mchdict.options(banknumber)),description)
with open(mch_filename, mode='w') as mchfile:
    mchdict.write(mchfile, space_around_delimiters = False)
