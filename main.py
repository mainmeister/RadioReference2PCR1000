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
from easygui import *   # quasi-cli-gui app
import os               # mostly for the path object

class MCH():
    def __init__(self, basename):
        self.banks = []
        self.basename = basename

    def __repr__(self):
        banknames = ""
        [banknames.join(bank.bankname + '') for bank in self.banks]
        return banknames

    def save(self):
        basex = 0



class Bank():
    def __init__(self, bankname):
        self.channels = []
        self.bankname = bankname

    def __repr__(self):
        return self.bankname

class Channel():
    def __init__(self, description, remark, frequency, mode, pltone):
        self.description = description
        self.remark = remark
        self.frequency = frequency
        self.mode = mode
        self.pltone = pltone
        if self.pltone == '':
            self.pltone = 'OFF'
        else:
            self.pltone = str(self.pltone).split(' ')[0]
            if not self.pltone.isnumeric() or self.pltone.strip() == '':
                self.pltone = 'OFF'
        if self.mode == 'FM':
            self.filter = '15k'
            self.step = '250KHz'
        elif self.mode == 'FMW':
            self.filter = '230k'
            self.step = '250KHz'
        elif self.mode == 'AM' or self.mode == 'LSB' or self.mode == 'USB' or self.mode == 'CW':
            self.filter = '3k'
            self.step = '25KHz'
        else:
            if self.float(frequency) > 30:
                self.mode = 'FM'
                self.filter = '15k'
                self.step = '250KHz'
            else:
                self.mode = 'AM'
                self.filter = '3k'
                self.step = '25KHz'

"""
    returns the maximum number in a list of channels
"""
def maxchannelnumber(channels):
    maxchannel = -1
    for channel in channels:
        if str(channel).isdigit():
            channelint = int(channel)
            if channelint > maxchannel:
                maxchannel = channelint
    return maxchannel + 1

"""
"""
def getbank(bankname):
    pass

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

"""
create a new config (MCH) file and initialize with the obligatory 'REV' section
"""
mchdict = configparser.ConfigParser(delimiters=('='))   # use only the '=' and not ':' character as the name/value separator
mchdict.optionxform = lambda option: option             # do not force to lower case
mchdict.add_section('REV')                              # the obligatory 'REV' section
mchdict.set('REV', 'ID', '1.0.0')
mchdict.set('REV', 'APP', 'IC-PCR1000  Revision 2.2')
mchdict.set('REV', 'SOURCE', csv_filename)

"""
Read one line (channel) from the CSV file at a time and add to the config (MCH) file
"""

with open(csv_filename) as csvfile:
    csv_reader = csv.DictReader(csvfile)
    """
    parse the CSV line into a bank/channel
    
    CSV field           MCH value
    ---------           ----------
    Agency/Category     BANKNAME
    Description         channel description
    Tag                 channel remark
    PL Tone             channel pltone
    Frequency Output    channel frequency
    Mode                channel mode
    
    notes: filter and step are determined by the mode. If mode is not supplied in the CSV the it is determined by the frequency.
    
    MODE            Filter/Step
    ----            -----------
    FM              15K/250KHz
    FMW             230K/250KHz
    AM/LSB/USB/CW   3K/25KHz
    
    FREQUENCY RANGE     MODE
    ---------------     ----
    30MHz - MAX         FM
    < 20MHz             AM
    
    To Do: add AM mode for air frequencies
    """
    for transmitter in csv_reader:
        bankname = transmitter['Agency/Category']
        description = transmitter['Description']
        remark = transmitter['Tag']
        pltone = transmitter['PL Tone']
        if pltone == '':
            pltone = 'OFF'
        else:
            pltone = str(pltone).split(' ')[0]
            if not pltone.isnumeric() or pltone.strip() == '':
                pltone = 'OFF'
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
        banknumber = None
        """
        look for an existing bank number for the current bank name
        """
        for section in mchdict.sections():
            if section != 'REV':
                if bankname == mchdict.get(section, 'BANKNAME'):
                    banknumber = section
                    break
        """
        if there is no existing bank for the current name then create a new bank
        """
        if banknumber is None:
            banknumber = 'BANK%02d' % (len(mchdict.sections()) - 1) # not counting the [REV] section (sections -1) and starting at bank00
            mchdict.add_section(banknumber)
            mchdict.set(banknumber, 'BANKNAME', bankname)
        """
        create the channel data
        description, remark, frequency, mode, filter, att, step, sel, skip, pltone
        not: att, sel and skip are arbitrarily set to OFF
        """
        channeldata = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (description, remark, frequency, mode, filter, 'OFF', step, 'OFF', 'OFF', pltone)
        mchdict.set(banknumber,"%02d" % maxchannelnumber(mchdict.options(banknumber)), channeldata)
with open(mch_filename, mode='w') as mchfile:
    mchdict.write(mchfile, space_around_delimiters = False)
