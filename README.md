# RadioReference2PCR1000
    Convert the frequency database csv file from the radioreference.com site to the Icom PCR1000 MCH file
    Author William Main - mainmeister@gmail.com

    Notes:
        The name of the MCH file will have the same base name as the csv file.
            aid_7768.csv --> aid_7768.mch
            metro_22.csv --> metro_22.mch
            
            *if the number of channels or frequencies exceed the limits of a single MCH file then 
            multiple MCH files will be created ie file1.mch, file2.mch, ...., fileX.mch

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
