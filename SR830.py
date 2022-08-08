# -*- coding: utf-8 -*-

'''
Standford Research SR830 Lock in amplifer function library used to communicate with instrument
Based on heeres code in https://github.com/heeres/qtlab.git
and https://github.com/ari1127/SR830.git

Dr. Yi Zhu, June 2022, University of Cambridge

This package provides basic setup function using SCPI Command

version 1.2
update the new class methods.   20220705
'''


import pyvisa
import logging
import time

LOGGER = logging.getLogger(__file__)

class SR830:

    def __init__(self, addr):                   # addr of SR830 in Photonic bay 2 is: GPIB0::8::INSTR
        if addr:
            LOGGER.info('Connecting %s.', addr)
            rm = pyvisa.ResourceManager()
            self._connection = rm.open_resource(addr, timeout=5000, chunk_size=24*1024*1024)
        else:
            LOGGER.info('SR830 in dry-run mode!')
            self._connection = None

        self.tau_set = {
                            0: "10 us",
                            1: "30 us",
                            2: "100 us",
                            3: "300 us",
                            4: "1 ms",
                            5: "3 ms",
                            6: "10 ms",
                            7: "30 ms",
                            8: "100 ms",
                            9: "300 ms",
                            10: "1 s",
                            11: "3 s",
                            12: "10 s",
                            13: "30 s",
                            14: "100 s",
                            15: "300 s",
                            16: "1 ks",
                            17: "3 ks",
                            18: "10 ks",
                            19: "30 ks"}

        self.sens_set = {
                            0: "2 nV",
                            1: "5 nV",
                            2: "10 nV",
                            3: "20 nV",
                            4: "50 nV",
                            5: "100 nV",
                            6: "200 nV",
                            7: "500 nV",
                            8: "1 uV",
                            9: "2 uV",
                            10: "5 uV",
                            11: "10 uV",
                            12: "20 uV",
                            13: "50 uV",
                            14: "100 uV",
                            15: "200 uV",
                            16: "500 uV",
                            17: "1 mV",
                            18: "2 mV",
                            19: "5 mV",
                            20: "10 mV",
                            21: "20 mV",
                            22: "50 mV",
                            23: "100 mV",
                            24: "200 mV",
                            25: "500 mV",
                            26: "1 V"}

    '''Low level communication method for SR830'''
    def write_instr(self, command):# command is string format
        if self._connection:
            self._connection.write(command)
        else:
             LOGGER.info("WRITE: %s failed, connection issue", command)

    def query_instr(self, command):
        if self._connection:
            response = self._connection.query(command)
            return response
        else:
            LOGGER.info("QUERY: %s failed, connection issue", command)

    def identify(self):
        if self._connection:
            response = self.query_instr('*IDN?')
            print(response)
            return response
        else:
            print('SR830 dry run.')
            return 'SR830 dry run.'

    def reset(self):
        self.write_instr('*RST')

    def disconnect(self):
        """
        disconnect instrument
        """
        if self._connection:
            self._connection.close()
        else:
            LOGGER.info("Instrument connection issue, can not disconnect properly")    

    '''low level settings method'''
    def setSR830(self):
        self.write_instr('*RST')
        self.write_instr('REST')    # Reset the scan. All stored data is lost.
        self.write_instr('OUTX 1')  # Set (Query) the Output Interface to RS232 (0) or GPIB (1).
        self.write_instr('OVRM 1')  # Set (Query) the GPIB Overide Remote state to Off (0) or On (1).

    '''AUTO Section'''
    def auto_phase(self):
        self.write_instr('APHS')


    def auto_gain(self):
        self.write_instr('AGAN')


    def auto_reserve(self):
        self.write_instr('ARSV')


    def auto_offset(self, channel):     #Auto Offset X,Y or R (i=1,2,3).
        self.write_instr('AOFF %i' % channel)

    '''get current settings'''
    def get_tau(self):              # get time constant
        res = self.query_instr('OFLT?')
        print('Time constant is %s' % self.tau_set[int(res.strip())])
        return res

    def get_sens(self):
        res = self.query_instr('SENS?')
        print('Sensitivity is %s' % self.sens_set[int(res.strip())])
        return res

    def get_refsource(self):
        """Reference Source to External (0) or Internal (1)"""
        res = self.query_instr('FMOD?')
        dic = {'0': 'External', '1': 'Internal'}
        print('Reference source is %s' % dic[res.strip()])
        return res

    def get_refshape(self):
        """Set (Query) the External Reference Slope to Sine(0), TTL Rising (1), or TTL Falling (2)"""
        res = self.query_instr('RSLP?')
        dic = {'0': 'Sine', '1': 'TTL Rising', '2': 'TTL Falling'}
        print('Reference shape is %s' % dic[res.strip()])
        return res

    def get_harm(self):
        """get Detection Harmonic. Largest value is 102 kHz."""
        return self.query_instr('HARM?')    # return string of harmonic value

    def get_input(self):
        """signal input type
        The parameter i: A (i=0), A-B (i=1), I (1 MΩ) (i=2) or I (100 MΩ) (i=3).
        """
        return self.query_instr('ISRC?')

    def get_ground(self):
        """signal ground or float, Float (i=0) or Ground (i=1)"""
        return self.query_instr('IGND?')

    def get_couple(self):
        """signal input couple: AC (i=0) or DC (i=1)"""
        return self.query_instr('ICPL?')

    def get_filter(self):
        """queries the input line notch filter status. The parameter i selects Out or no filters (i=0),
        Line notch in (i=1), 2xLine notch in (i=2) or Both notch filters in (i=3)"""
        return self.query_instr('ILIN?')

    def get_reserve(self):
        """High Reserve (i=0), Normal (i=1) or Low Noise (minimum) (i=2)"""
        return self.query_instr('RMOD?')

    def get_slope(self):
        """the low pass filter slope: 6 dB/oct (i=0), 12 dB/oct (i=1), 18 dB/oct (i=2) or 24 dB/oct (i=3)"""
        dic = {'0': '6dB/oct', '1': '12dB/oct', '2': '18dB/oct', '3': '24dB/oct'}
        return dic[self.query_instr('OFSL?').strip()]

    def get_sync(self):
        """the synchronous filter status: Off (i=0) or below 200 Hz (i=1)"""
        dic = {'0': 'Off', '1': 'Below 200Hz'}
        return dic[self.query_instr('SYNC?').strip()]

    def get_disp_rat(self, channel):
        """check channel display: The returned string contains both j and k separated by a comma. For example,
        if the DDEF? 1 command returns "1,0" then the CH1 display is R with no ratio."""
        return self.query_instr('DDEF? %i' % channel)

    def get_exp_off(self, output_type):
        """The parameter i selects X (i=1), Y (i=2) or R (i=3) and is required"""
        return self.query_instr('OEXP? %i' % output_type)

    '''set settings for SR830'''
    def set_freq(self, freq):
        """unit Hz, maximum 102 kHz"""
        self.write_instr('FREQ %f' % freq)

    def set_ampl(self, ampl):
        """unit V: range from 0.004 ≤ x ≤ 5.000"""
        self.write_instr('SLVL %f' % ampl)

    def set_mode(self, mode):
        """internal (i=1) or external (i=0)"""
        self.write_instr('FMOD %i' % mode)

    def set_tau(self, tau):
        self.write_instr('OFLT %i' % tau)

    def set_sens(self, sens):
        self.write_instr('SENS %i' % sens)

    def set_phase(self, phase):
        """The phase may be programmed from -360.00 ≤ x ≤ 729.99 and will be wrapped around at ±180°.
        For example, the PHAS 541.0 command will set the phase to -179.00° (541-360=181=-179)"""
        self.write_instr('PHAS %f' % phase)

    def set_aux(self, output, value):
        """Aux Output (1, 2, 3 or 4), x is the output voltage (real number of Volts)
        and is limited to -10.500 ≤ x ≤ 10.500"""
        self.write_instr('AUXV %(out)i, %(val).3f' % {'out':output,'val':value})

    def set_refsource(self, ref):
        """Reference Source to External (0) or Internal (1)"""
        self.write_instr('FMOD %i' % ref)

    def set_refshape(self, refshape):
        """External Reference Slope to Sine(0), TTL Rising (1), or TTL Falling (2)"""
        self.write_instr('RSLP %i' % refshape)

    def set_disp_rat(self, channel, disp, ratio):                      # .
        """the CH1 or CH2 (i=1,2) display to CH1 (X, R, X Noise, Auxin1, Auxin2) (j=0 to 4)
        CH2 (Y, theta, Y Noise, Auxin3, Auxin4) (j=0 to 4)
        and ratio the display to None, Aux1, Aux2 (k=0,1,2) for CH1
        Aux3, Aux4 (k=0,1,2) for CH1
        """
        self.write_instr('DDEF %(channel)i, %(disp)i, %(ratio)i' % {'channel': channel, 'disp': disp, 'ratio': ratio})

    def set_exp_off(self, output_type, offset, expand):
        """i selects X (i=1), Y (i=2) or R (i=3)
        x is the offset in percent (-105.00 ≤ x ≤ 105.00)
        j selects no expand (j=0), expand by 10 (j=1) or 100 (j=2)"""
        self.write_instr('OEXP %(channel)i, %(offset)f, %(expand)i' % {'channel': output_type, 'offset': offset, 'expand': expand})

    def set_reserve(self, reserve):
        """HighReserve (0), Normal (1), or Low Noise (2)"""
        self.write_instr('RMOD %i' % reserve)

    def set_filter(self, filt):
        """Line Notch Filters to Out (0), Line In (1) , 2xLine In (2), or Both In (3)"""
        self.write_instr('ILIN %i' % filt)

    def set_input(self, inp):
        """the Input Configuration to A (0), A-B (1) , I (1 MΩ) (2) or I (100 MΩ) (3)"""
        self.write_instr('ISRC %i' % inp)

    def set_ground(self, gnd):
        """the Input Shield Grounding to Float (0) or Ground (1)"""
        self.write_instr('IGND %i' % gnd)

    def set_couple(self, coup):
        """AC (0) or DC (1)"""
        self.write_instr('ICPL %i' % coup)

    def set_slope(self, slope):
        """Low Pass Filter Slope to 6 (0), 12 (1), 18 (2) or 24 (3) dB/oct"""
        self.write_instr('OFSL %i' % slope)

    def set_sync(self, sync):
        """Synchronous Filter to Off (0) or On below 200 Hz (1)"""
        self.write_instr('SYNC %i' % sync)

    '''data storage, the data can be stored in internal storage and transfer out later'''
    def get_sample_rate(self):
        """sample rate: 0 62.5 mHz; 1 125 mHz; 2 250 mHz; 3 500 mHz; 4 1 Hz; 5 2 Hz;
        6 4 Hz; 7 8 Hz; 8 16 Hz; 9 32 Hz; 10 64 Hz; 11 128 Hz; 12 256 Hz; 13 512 Hz; 14 Trigger"""
        return self.query_instr('SRAT?')

    def set_sample_rate(self, rate):
        """sample rate: 0 62.5 mHz; 1 125 mHz; 2 250 mHz; 3 500 mHz; 4 1 Hz; 5 2 Hz;
        6 4 Hz; 7 8 Hz; 8 16 Hz; 9 32 Hz; 10 64 Hz; 11 128 Hz; 12 256 Hz; 13 512 Hz; 14 Trigger"""
        self.write_instr('SYNC %i' % rate)

    def get_buffer_mode(self):
        """The parameter i selects 1 Shot (i=0) or Loop (i=1)(default)"""
        return self.query_instr('SEND?')

    def set_buffer_mode(self, mode):
        """The parameter i selects 1 Shot (i=0) or Loop (i=1)(default)"""
        self.write_instr('SYNC %i' % mode)

    def soft_trigger(self):
        """send software trigger"""
        self.write_instr('TRIG')

    def get_trigger_start_mode(self):
        """i=1 selects trigger starts the scan and i=0 turns the trigger start feature off"""
        self.query_instr('TSTR?')

    def set_trigger_start_mode(self, mode):
        """i=1 selects trigger starts the scan and i=0 turns the trigger start feature off"""
        self.write_instr('TSTR %i' % mode)

    def start_data_storage(self):
        """starts or resumes data storage"""
        self.write_instr('STRT')

    def pause_data_storage(self):
        self.write_instr('PAUS')

    def reset_data_buffer(self):
        self.write_instr('REST')

    '''data transfer, the command can transfer stored data but can also transfer real time data'''
    def get_X(self):
        return float(self.query_instr('OUTP? 1'))
    
    def get_Y(self):
        return float(self.query_instr('OUTP? 2'))
    
    def get_R(self):
        return float(self.query_instr('OUTP? 3'))
    
    def get_Theta(self):
        return float(self.query_instr('OUTP? 4'))

    def get_snap_one(self, p1):
        res = self.query_instr(('SNAP ? %(p1)i' % {'p1': p1}))
        return res.strip()

    def get_buffer_points(self):
        """queries the number of points stored in the buffer"""
        return self.query_instr('SPTS ?')

    def get_snap_two(self, p1, p2):
        res = self.query_instr(('SNAP ? %(p1)i, %(p2)i' % {'p1': p1, 'p2': p2}))
        res = res.split(",")
        return res[0], res[1]

    def get_snap_three(self, p1, p2, p3):
        """1 X
            2 Y
            3 R
            4 theta
            5 Aux In 1
            6 Aux In 2
            7 Aux In 3
            8 Aux In 4
            9 Reference Frequency
            10 CH1 display
            11 CH2 display"""
        res = self.query_instr(('SNAP ? %(p1)i, %(p2)i, %(p3)i' % {'p1': p1, 'p2': p2, 'p3': p3}))
        res = res.split(",")
        return res[0], res[1], res[2]

    def get_snap_four(self, p1, p2, p3, p4):
        res = self.query_instr(('SNAP ? %(p1)i, %(p2)i, %(p3)i, %(p4)i' % {'p1': p1, 'p2': p2, 'p3': p3, 'p4': p4}))
        res = res.split(",")
        return res[0], res[1], res[2], res[3]

    def get_snap_five(self, p1, p2, p3, p4, p5):
        res = self.query_instr(('SNAP ? %(p1)i, %(p2)i, %(p3)i, %(p4)i, %(p5)i' % {'p1': p1, 'p2': p2, 'p3': p3,
                                                                                   'p4': p4, 'p5': p5}))
        res = res.split(",")
        return res[0], res[1], res[2], res[3], res[4].strip()


    ''' The other command such as 
    OUTR ? i; SNAP ? i,j {,k,l,m,n}; OAUX? i; TRCA ? i, j, k; TRCB ? i, j, k; TRCL ? i, j, k
    FAST (?) {i} .      Those command is rarely used, will not encapsulate with function in this version.
    '''

    def check_overload(self):
        res = self.query_instr('LIAS?')
        bit = format(int(res), '08b')
        # print(bit)
        # if bit[7] == '1':
        #     print('Input overload')
        # if bit[6] == '1':
        #     print('Time constant filter overload')
        # if bit[5] == '1':
        #     print('Output overload')
        return bit[7], bit[6], bit[5]


