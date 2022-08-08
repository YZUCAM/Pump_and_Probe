# -*- coding: utf-8 -*-

"""
PI C633 Mecury controller for PI linear delay stage function library

Dr. Yi Zhu, July 2022, University of Cambridge

This package provides basic setup function using GCS Command (probably)

The command need to be terminated by \n.

version 1.0
"""

import pyvisa
import logging
import time

LOGGER = logging.getLogger(__file__)


class C633:

    def __init__(self, addr):                   # addr of C633 in Photonic bay 2 is: ASRL5::INSTR
        if addr:
            LOGGER.info('Connecting %s.', addr)
            rm = pyvisa.ResourceManager()
            self._connection = rm.open_resource(addr, timeout=5000, chunk_size=24*1024*1024)
            self._connection.baud_rate = 38400
        else:
            LOGGER.info('C633 connection failed!')
            self._connection = None

    '''Low level communication method for SR830'''
    def write_instr(self, command):  # command is string format
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

    def disconnect(self):
        """
        disconnect instrument
        """
        if self._connection:
            self._connection.close()
        else:
            LOGGER.info("Instrument connection issue, can not disconnect properly")

    def identify(self):
        if self._connection:
            response = self.query_instr('*IDN?\n')
            print(response)
            return response
        else:
            print('C633 connection error.')
            return 'C633 connection error.'

    '''high level functions'''
    def get_position(self):
        res = self.query_instr('POS? 1\n')
        res = res[2:]
        return res

    def move_abs(self, value):
        '''the stage range for m414-32S is 0 to 300 mm'''
        self.write_instr('MOV 1 %f\n' % value)

    def mov_relative(self, value):
        '''the minimum step is 0.2 um 0.0002 mm'''
        self.write_instr('MVR 1 %f\n' % value)

    def reboot(self):
        self.write_instr('RBT\n')

    def halt(self):
        self.write_instr('HLT 1\n')

    def go_home(self):
        self.write_instr('GOH 1\n')

    def get_acc(self):
        res = self.query_instr('ACC? 1\n')
        res = res[2:]
        return res

    def set_acc(self, value):
        '''stage step acceleration range from 0 to 10'''
        self.write_instr('ACC 1 %f\n' % value)

    def get_deceleration(self):
        res = self.query_instr('DEC? 1\n')
        res = res[2:]
        return res

    def set_deceleration(self, value):
        '''stage step deceleration range from 0 to 10'''
        self.write_instr('DEC 1 %f\n' % value)

    def chk_on_target(self):
        res = self.query_instr('ONT? 1\n')
        res = res[2:].strip()
        if res == '1':
            return True
        else:
            return False

    def get_velo(self):
        res = self.query_instr('VEL? 1\n')
        res = res[2:]
        return res

    def set_velo(self, value):
        '''stage step velocity range from 0 to 3, minimum 0.0003'''
        self.write_instr('VEL 1 %f\n' % value)

    def ref_to_switch(self):
        self.write_instr('FRF 1\n')

    def ref_to_pos(self):
        self.write_instr('FPL 1\n')

    def ref_to_neg(self):
        self.write_instr('FNL 1\n')

    def chk_ref(self):
        res = self.query_instr('FRF? 1\n')
        res = res[2:].strip()
        if res == '1':
            return True
        else:
            return False
