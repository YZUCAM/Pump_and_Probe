import time

from pump_probe_pc_panel import *
from SR830 import SR830
from C633 import C633
from Horiba_DNFActiveX import *
import sys
import numpy as np
import threading
from PyQt5.Qt import QThread, QMutex, pyqtSignal
import pyqtgraph as pg
from random import random

'''set Qmutex locker'''
# mutex_lia_read = QMutex()
# mutex_lia_chk = QMutex()
# mutex_dl_chk = QMutex()
# mutex_dl_getpos = QMutex()
mutex = QMutex()

'''initialise main function variables'''
lia_tau = {
    0: 10e-6,  # "10 us",
    1: 30e-6,  # "30 us",
    2: 100e-6,  # "100 us",
    3: 300e-6,  # "300 us",
    4: 1e-3,  # "1 ms",
    5: 3e-3,  # "3 ms",
    6: 10e-3,  # "10 ms",
    7: 30e-3,  # "30 ms",
    8: 100e-3,  # "100 ms",
    9: 300e-3,  # "300 ms",
    10: 1,  # "1 s",
    11: 3,  # "3 s",
    12: 10,  # "10 s",
    13: 30,  # "30 s",
    14: 100,  # "100 s",
    15: 300,  # "300 s",
    16: 1000,  # "1 ks",
    17: 3000,  # "3 ks",
    18: 10000,  # "10 ks",
    19: 30000}  # "30 ks"

'''initialise ccd single spectrum variable'''
wl_single_spectrum = list()
intensity_single_spectrum = list()



# global stop_1D_ppc_thread
# stop_1D_ppc_thread = False
'''Threading for horiba temperature reading'''
class BackendThreadhorriba(QThread):
    horiba_read_temperature_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.horiba_thread_flg = True

    def run(self):
        while self.horiba_thread_flg:
            self.horiba_read_temperature_signal.emit()
            time.sleep(0.5)


'''initialise functions for initial parameter check'''
def delayline_chk_ref(c633, main_window):
    ref_flg = c633.chk_ref()
    style_normal = 'color: rgb(255, 255, 255);'
    style_alarm = 'color: rgb(255, 255, 255); background-color: rgb(255, 0, 0);'
    # print('break point delay ref checking function inside')
    if ref_flg:
        main_window.lbl_PI_ref.setText('Referenced')
        main_window.lbl_PI_ref.setStyleSheet(style_normal)
    else:
        main_window.lbl_PI_ref.setText('Unreferenced')
        main_window.lbl_PI_ref.setStyleSheet(style_alarm)

'''acquisition function'''
def transform_ps_mm(nparray, zero_pos):
    '''do not try to modify main_window.delay_scan_array or its assigned variable, otherwise there will be an error'''
    x_list = list()
    # print(x_list)
    # print(zero_pos)
    for i in range(len(nparray)):
        # print('*'*10)
        print('££££££££££££££££££££££')
        print(nparray)
        print('££££££££££££££££££££££')
        x_list.append(round(((nparray[i] * 299702547000 / 1e12/2) + zero_pos), 4))  # the optical path = 2 * real movement
        # print(x_list)
        # print('*' * 10)
    # print(nparray)
    print('-------')
    print(nparray)
    return x_list

'''use pyqt5 Qthread instead of python built-in threading for data acquistion'''
class BackendThread1Dppc(QThread):
    update_1Dppc_graph_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.main_window = None
        self.c633 = None
        self.abs_mm_list = None
        self.sr830 = None
        print('initial BackendThread1Dppc')
        self.y_lia_list = list()
        self.x_lia_list = list()
        self.progress = 0

    def transfer_args(self, main_window, c633, sr830, abs_mm_list):
        self.main_window = main_window
        self.c633 = c633
        self.abs_mm_list = abs_mm_list
        self.sr830 = sr830

    def run(self):
        print('enter thread run function')
        tc = lia_tau[int(self.main_window.spb_tc.value())] * 6      #fix scan interval time
        self.y_lia_list = list()
        self.x_lia_list = list()
        self.progress = 0
        total_point = self.main_window.delay_scan_point
        self.c633.move_abs(self.abs_mm_list[0])
        time.sleep(2)
        for i in range(total_point):
            # self.c633.move_abs(self.abs_mm_list[i])
            # time.sleep(0.1)
            self.progress = round(((i + 1) / total_point) * 100)
            if self.main_window.single_ppc_continue:
                print('mutex_dl_chk lock start')
                # mutex_dl_chk.lock()                               #dead lock here       no locker in main
                mutex.lock()
                PI_ont_flg = self.main_window.chk_PI_ont.checkState()
                # mutex_dl_chk.unlock()
                mutex.unlock()
                while not PI_ont_flg:
                    time.sleep(0.6)
                    # mutex_dl_chk.lock()  # dead lock here
                    mutex.lock()
                    PI_ont_flg = self.main_window.chk_PI_ont.checkState()
                    # PI_ont_flg = c633.chk_on_target()
                    # mutex_dl_chk.unlock()
                    mutex.unlock()
                # mutex_dl_chk.unlock()
                print('mutex_dl_chk lock stop')
                if tc < 0.5:
                    time.sleep(0.5)
                else:
                    time.sleep(tc)                      # if tc is too small, need add more delay
                print('mutex_lia_read lock start')
                # mutex_lia_read.lock()
                mutex.lock()
                # self.sr830._connection.clear()
                """use get_X method acquire data"""
                # self.sr830._connection.flush(1)
                # time.sleep(0.05)
                # if self.main_window.lia_dis_x:
                #     self.y_lia_list.append(float(self.sr830.get_X()))
                # elif self.main_window.lia_dis_y:
                #     self.y_lia_list.append(float(self.sr830.get_Y()))
                # elif self.main_window.lia_dis_r:
                #     self.y_lia_list.append(float(self.sr830.get_R()))
                # elif self.main_window.lia_dis_ps:
                #     self.y_lia_list.append(float(self.sr830.get_Theta()))
                """use access snap method acquire data"""
                self.y_lia_list.append(float(self.main_window.lia_dis_1.text()))
                """test if crashdown comes from sr830"""
                # y_lia_list.append(float(random()))
                # y_lia_list.append(float(self.sr830.get_X()))
                # mutex_lia_read.unlock()
                mutex.unlock()
                if i < total_point - 1:
                    self.c633.move_abs(self.abs_mm_list[i+1])

                print('mutex_lia_read lock stop')
                self.x_lia_list.append(0 - self.main_window.delay_scan_array[i])
                # print(x_lia_list)
                self.update_1Dppc_graph_signal.emit()
                # self.main_window.p1.setData(y=y_lia_list, x=x_lia_list, pen='y')
                # self.main_window.progb1.setValue(progress)
                # time.sleep(0.1)
            else:
                break
            self.main_window.ppc_1D_y_data = self.y_lia_list
            # print(y_lia_list)
            print('below display delay array after once measurement')
            # print(self.main_window.delay_scan_array)
            print('-----------------------------')
            print('delay_scan_point')
            # print(self.main_window.delay_scan_point)
            print('--------------------------------')

# # old thread using python builtin threading
# '''thread for acquistion to mitigate freeze screen'''
# def thread_start_acquire_1D_ppc(main_window, c633, abs_mm_list):
#     '''do not try to modify main_window.delay_scan_array or its assigned variable, otherwise there will be an error'''
#     y_lia_list = list()
#     x_lia_list = list()
#     # print(main_window.delay_scan_array)
#     # abs_mm_list = transform_ps_mm(main_window.delay_scan_array, main_window.delay_zero_position)
#     total_point = main_window.delay_scan_point
#     # c633.move_abs(abs_mm_list[0])
#     for i in range(total_point):
#         progress = round(((i+1)/total_point)*100)
#         if main_window.single_ppc_continue:
#             c633.move_abs(abs_mm_list[i])
#             # print('move to place')
#             while not main_window.chk_PI_ont.checkState():
#                 time.sleep(0.3)
#             time.sleep(lia_tau[int(main_window.spb_tc.value())] * 6)
#             y_lia_list.append(float(main_window.lia_dis_1.text()))
#             # if main_window.lia_dis_x:
#             #     y_lia_list.append(sr830.get_X())
#             # elif main_window.lia_dis_y:
#             #     y_lia_list.append(sr830.get_Y())
#             # elif main_window.lia_dis_r:
#             #     y_lia_list.append(sr830.get_R())
#             # elif main_window.lia_dis_ps:
#             #     y_lia_list.append(sr830.get_Theta())
#             # print('read data')
#             print('------------------')
#             print(y_lia_list)
#             x_lia_list.append(main_window.delay_scan_array[i])
#             print(x_lia_list)
#             main_window.p1.setData(y=y_lia_list, x=x_lia_list, pen='y')
#             main_window.progb1.setValue(progress)
#             # print(x_lia_list_temp[i])
#         else:
#             break
#     main_window.ppc_1D_y_data = y_lia_list
#     print(y_lia_list)
#     print('below display delay array after once measurement')
#     print(main_window.delay_scan_array)
#     print('-----------------------------')
#     print('delay_scan_point')
#     print(main_window.delay_scan_point)
#     print('--------------------------------')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    '''initialise main window and instruments'''
    main_window = Window()
    sr830 = SR830('GPIB0::8::INSTR')
    sr830.setSR830()
    c633 = C633('ASRL5::INSTR')
    horiba = None
    backend_horiba = None
    acquire_1D_ppc = BackendThread1Dppc()



    '''initialise SR830 setting in main window'''
    main_window.spb_input_signal.setValue(int(sr830.get_input()))
    main_window.spb_acdc.setValue(int(sr830.get_couple()))
    main_window.spb_ground.setValue(int(sr830.get_ground()))
    main_window.spb_tc.setValue(int(sr830.get_tau()))
    main_window.spb_sens.setValue(int(sr830.get_sens()))
    main_window.spb_reserve.setValue((int(sr830.get_reserve())))
    main_window.spb_filter.setValue((int(sr830.get_filter())))
    main_window.spb_signal_type.setValue((int(sr830.get_refshape())))
    main_window.comb_slope.setCurrentText(sr830.get_slope())
    main_window.comb_sync.setCurrentText(sr830.get_sync())
    main_window.ledit_fre.setText('1000')
    main_window.ledit_amp.setText('1')

    '''initialise PI delay line setting in main window'''
    main_window.ledit_PI_TP.setText(c633.get_position())
    main_window.ledit_PI_SS.setText('10')
    c633.set_velo(1.5)
    main_window.ledit_PI_vel.setText(c633.get_velo())
    main_window.ledit_PI_zero.setText(str(main_window.delay_zero_position))
    main_window.ledit_PI_sp.setText('0')
    main_window.ledit_PI_ep.setText('500')
    main_window.ledit_PI_ssp.setText('10')
    main_window.ledit_PI_point.setText('50')
    main_window.step_mm = float(main_window.ledit_PI_SS.text())
    print('initialsed PI delay stage')

    '''connect close function with close signal for main_window'''
    main_window.close_signal.connect(lambda: close_software())
    '''connect slot function with lia signals from main_window'''
    main_window.input_type_signal.connect(lambda key: set_lia_input_type(key))
    main_window.input_coupling_signal.connect(lambda key: set_lia_in_couple(key))
    main_window.input_gr_signal.connect(lambda key: set_lia_in_gr(key))
    main_window.lia_tau_signal.connect(lambda key: set_lia_tc(key))
    main_window.lia_sens_signal.connect(lambda key: set_lia_sens(key))
    main_window.lia_reserve_signal.connect(lambda key: set_lia_reserve(key))
    main_window.lia_filter_signal.connect(lambda key: set_lia_filter(key))
    main_window.lia_ext_type_signal.connect(lambda key: set_lia_ext_signal_type(key))
    main_window.lia_slope_signal.connect(lambda command: set_lia_slope(command))
    main_window.lia_sync_signal.connect(lambda command: set_lia_sync(command))
    main_window.lia_auto_phase_signal.connect(lambda: lia_auto_phase())
    main_window.lia_auto_gain_signal.connect(lambda: lia_auto_gain())
    main_window.lia_auto_reserve_signal.connect(lambda: lia_auto_reserve())
    main_window.lia_external_signal.connect(lambda: lia_set_ext())
    main_window.lia_internal_signal.connect(lambda: lia_set_int())
    main_window.lia_freq_signal.connect(lambda fre: lia_set_fre(fre))
    main_window.lia_amp_signal.connect(lambda amp: lia_set_amp(amp))

    '''connect slot function with signals for LIA sub thread'''
    main_window.backendlia.snap_signal.connect(lambda: get_lia_snap())
    main_window.backendlia.lia_overload_signal.connect(lambda: check_lia_overload())
    print('start lia thread')

    '''connect slot function with signals for delay line sub thread'''
    main_window.backenddl.delay_real_pos_signal.connect(lambda: get_delay_line_pos())
    main_window.backenddl.delay_on_target_signal.connect(lambda: check_delay_on_target())
    print('break point start PI delay stage thread')

    '''connect slot function with PI delay line signals from main_window'''
    main_window.delay_ref_signal.connect(lambda: set_delay_reference())
    main_window.delay_TP_signal.connect(lambda value: set_delay_target(value))
    main_window.delay_goleft_signal.connect(lambda: delay_go_left())
    main_window.delay_goright_signal.connect(lambda: delay_go_right())
    main_window.delay_halt_signal.connect(lambda: delay_halt())
    main_window.delay_set_zero_signal.connect(lambda value: set_delay_zero(value))
    main_window.delay_start_pos_signal.connect(lambda value: set_delay_start_pos(value))
    main_window.delay_end_pos_signal.connect(lambda value: set_delay_end_pos(value))
    main_window.delay_step_size_signal.connect(lambda value: set_delay_step_size(value))

    '''connect slot function with horiba related signals from main_window'''
    main_window.horiba_connect_signal.connect(lambda: connect_horiba())
    main_window.horiba_disconnect_signal.connect(lambda: disconnect_horiba())
    main_window.horiba_set_wl_signal.connect(lambda value: set_wl(value))
    main_window.horiba_set_horiba_from_signal.connect(lambda value: set_from(value))
    main_window.horiba_set_horiba_to_signal.connect(lambda value: set_to(value))
    main_window.horiba_set_acqtime_signal.connect(lambda value: set_acq_time(value))
    main_window.horiba_set_acc_signal.connect(lambda value: set_acc(value))
    main_window.horiba_set_rtd_signal.connect(lambda value: set_rtd_time(value))
    main_window.horiba_set_slit_signal.connect(lambda value: set_slit(value))


    '''connect slot function with acquistion related signals from main_window'''
    main_window.pump_pc_start_signal.connect(lambda: start_acquire_1D_ppc())
    acquire_1D_ppc.update_1Dppc_graph_signal.connect(lambda: update_1D_ppc_graph())
    main_window.horiba_single_acq_signal.connect(lambda: ccd_single_acq())
    main_window.horiba_multi_acq_signal.connect(lambda: ccd_multi_acq())


    '''initialise C633 delay stage setting in main window'''
    delayline_chk_ref(c633, main_window)
    print('break point delay stage reference checking')




    '''slot functions for LIA'''
    def set_lia_input_type(key):
        sr830.set_input(key)

    def set_lia_in_couple(key):
        sr830.set_couple(key)

    def set_lia_in_gr(key):
        sr830.set_ground(key)

    def set_lia_tc(key):
        sr830.set_tau(key)

    def set_lia_sens(key):
        sr830.set_sens(key)

    def set_lia_reserve(key):
        sr830.set_reserve(key)

    def set_lia_filter(key):
        sr830.set_filter(key)

    def set_lia_ext_signal_type(key):
        sr830.set_refshape(key)

    def set_lia_slope(command):
        sr830.set_slope(command)

    def set_lia_sync(command):
        sr830.set_sync(command)

    def lia_auto_phase():
        sr830.auto_phase()

    def lia_auto_gain():
        sr830.auto_gain()

    def lia_auto_reserve():
        sr830.auto_reserve()

    def lia_set_ext():
        sr830.set_mode(0)

    def lia_set_int():
        sr830.set_mode(1)

    def lia_set_fre(fre):
        sr830.set_freq(fre)

    def lia_set_amp(amp):
        sr830.set_ampl(amp)

    '''lia sub thread functions'''
    def get_lia_snap():
        # sr830._connection.flush(1)
        # time.sleep(0.05)
        lia_x, lia_y, lia_r, lia_ps, lia_f = sr830.get_snap_five(1, 2, 3, 4, 9)
        main_window.lia_dis_2.setText(lia_f)
        # mutex_lia_read.lock()
        mutex.lock()
        if main_window.lia_dis_x:
            main_window.lia_dis_1.setText(lia_x)
        elif main_window.lia_dis_y:
            main_window.lia_dis_1.setText(lia_y)
        elif main_window.lia_dis_r:
            main_window.lia_dis_1.setText(lia_r)
        elif main_window.lia_dis_ps:
            main_window.lia_dis_1.setText(lia_ps)
        # mutex_lia_read.unlock()
        mutex.unlock()
        print('get_lia_snap_sub thread\n -------------------')

    # def get_lia_snap():
    #     lia_y, lia_f = sr830.get_snap_two(2, 9)
    #     main_window.lia_dis_2.setText(lia_f.strip())
    #     # mutex_lia_read.lock()
    #     mutex.lock()
    #     if main_window.lia_dis_x:
    #         lia_x = sr830.get_X()
    #         main_window.lia_dis_1.setText(str(lia_x))
    #     elif main_window.lia_dis_y:
    #         lia_y = sr830.get_Y()
    #         main_window.lia_dis_1.setText(str(lia_y))
    #     elif main_window.lia_dis_r:
    #         lia_r = sr830.get_R()
    #         main_window.lia_dis_1.setText(str(lia_r))
    #     elif main_window.lia_dis_ps:
    #         lia_ps = sr830.get_Theta()
    #         main_window.lia_dis_1.setText(str(lia_ps))
    #     # mutex_lia_read.unlock()
    #     mutex.unlock()
    #     print('get_lia_snap_sub thread\n -------------------')


    def check_lia_overload():
        InOL, TCOL, OutOL = sr830.check_overload()
        style_normal = ''
        style_alarm = 'background-color: rgb(255, 0, 0);'
        # mutex_lia_chk.lock()
        if InOL == '1':
            main_window.lbl_lia_input_ol.setStyleSheet(style_alarm)
        else:
            main_window.lbl_lia_input_ol.setStyleSheet(style_normal)
        if TCOL == '1':
            main_window.lbl_lia_filter_ol.setStyleSheet(style_alarm)
        else:
            main_window.lbl_lia_filter_ol.setStyleSheet(style_normal)
        if OutOL == '1':
            main_window.lbl_lia_output_ol.setStyleSheet(style_normal)
        print('check_lia_overload_sub thread\n -------------------')
        # mutex_lia_chk.unlock()

    '''slot functions for Delay Line'''
    # def delayline_chk_ref():
    #     ref_flg = c633.chk_ref()
    #     style_normal = ''
    #     style_alarm = 'background-color: rgb(255, 0, 0);'
    #     if ref_flg:
    #         main_window.lbl_PI_ref.setText('Referenced')
    #         main_window.lbl_PI_ref.setStyleSheet(style_normal)
    #     else:
    #         main_window.lbl_PI_ref.setText('Unreferenced')
    #         main_window.lbl_PI_ref.setStyleSheet(style_alarm)

    def set_delay_reference():
        c633.ref_to_switch()

    def set_delay_target(value):
        c633.move_abs(value)

    def delay_go_left():
        c633.mov_relative(0 - main_window.step_mm)

    def delay_go_right():
        c633.mov_relative(main_window.step_mm)

    def delay_halt():
        c633.halt()

    def set_delay_zero(value):
        main_window.delay_zero_position = value

    def set_delay_start_pos(value):
        main_window.delay_start_pos_value = value

    def set_delay_end_pos(value):
        main_window.delay_end_pos_value = value

    def set_delay_step_size(value):
        main_window.delay_step_size_value = value
        print('*'*10)
        print(main_window.delay_end_pos_value)
        print(main_window.delay_start_pos_value)
        print(main_window.delay_scan_point)
        '''build 1D scan array'''
        if None != main_window.delay_start_pos_value and None != main_window.delay_end_pos_value:
            '''start construct 1D scan array'''
            main_window.delay_scan_point = int((main_window.delay_end_pos_value - main_window.delay_start_pos_value) /
                                               main_window.delay_step_size_value + 1)
            main_window.delay_scan_array = np.linspace((0 - main_window.delay_start_pos_value), (0 - main_window.delay_end_pos_value),
                                           main_window.delay_scan_point).tolist()
            main_window.delay_scan_array_save = np.linspace(main_window.delay_start_pos_value, main_window.delay_end_pos_value,
                                                            main_window.delay_scan_point).tolist()
            main_window.ledit_PI_point.setText(str(main_window.delay_scan_point))
            print(main_window.delay_scan_array)
        else:
            pass

    '''delay line sub thread functions'''
    def get_delay_line_pos():
        # mutex_dl_getpos.lock()
        value = c633.get_position().strip()
        main_window.ledit_cpm.setText(value)
        main_window.horizontalSlider.setValue(int(float(value) * 1e4))
        value_ps = (((float(value) - main_window.delay_zero_position) / 299702547000) * 1e12)*2  # set unit to ps
        main_window.lbl_PI_cpp.setText(str(0 - value_ps))
        # mutex_dl_getpos.unlock()
        # print('break point get delay line pos')
        print('delay_getpos_sub thread\n -------------------')

    def check_delay_on_target():
        flg = c633.chk_on_target()
        # mutex_dl_chk.lock()
        mutex.lock()
        main_window.chk_PI_ont.setChecked(flg)
        # mutex_dl_chk.unlock()
        mutex.unlock()
        print('delay_on_target_sub thread\n -------------------')
        # print('break point on target set')


    # # old start_acquire_1D_ppc function with python built in threading
    # '''acquistion section (should be in seperate thread)'''
    # def start_acquire_1D_ppc():
    #     print('---initial delay array---')
    #     print(main_window.delay_scan_array)
    #     # main_window.delay_scan_array_temp = main_window.delay_scan_array
    #        #get list element from class 'list'
    #     abs_mm_list = transform_ps_mm(main_window.delay_scan_array, main_window.delay_zero_position)
    #     thread_1D = threading.Thread(target=thread_start_acquire_1D_ppc, args=(main_window, c633, abs_mm_list))
    #     thread_1D.start()

    '''slot function for horiba'''
    def connect_horiba():
        global horiba
        horiba = Horiba()
        """initialise horiba widgets value"""
        # main_window.spb_input_signal.setValue(int(sr830.get_input()))
        main_window.ledit_specto_center.setText(str(horiba.get_wl()))
        main_window.ledit_spec_from.setText(str(main_window.horiba_from))
        main_window.ledit_spec_to.setText(str(main_window.horiba_to))
        main_window.ledit_acq_time.setText(str(main_window.horiba_acqtime))
        main_window.ledit_spec_acc.setText(str(main_window.horiba_acc))
        main_window.ledit_rtd_time.setText(str(main_window.horiba_rtd_time))
        main_window.ledit_specto_slit.setText(str(horiba.get_slit()))
        global backend_horiba
        backend_horiba = BackendThreadhorriba()
        backend_horiba.horiba_read_temperature_signal.connect(lambda: get_ccd_temperature())
        backend_horiba.start()

    def disconnect_horiba():
        backend_horiba.horiba_thread_flg =False
        global horiba
        del horiba
        horiba = None

    def set_wl(value):
        horiba.set_wl(value)

    def set_from(value):
        main_window.horiba_from = value

    def set_to(value):
        main_window.horiba_to = value

    def set_acq_time(value):
        main_window.horiba_acqtime = value

    def set_acc(value):
        main_window.horiba_acc = value

    def set_rtd_time(value):
        main_window.horiba_rtd_time = value

    def set_slit(value):
        main_window.horiba_slit = value

    def get_ccd_temperature():
        main_window.lbl_ccd_T.setText(str(horiba.get_temperature()))

    def ccd_single_acq():
        # update_ccd_single_spectrum_signal = pyqtSignal()
        # update_ccd_single_spectrum_signal.connect(lambda: update_ccd_single_spectrum_graph())
        wl, intensity = horiba.acquire_spectrum(main_window.horiba_acqtime, main_window.horiba_acc)
        wl = wl.tolist()
        intensity = intensity.tolist()
        '''prepare data to be saved'''
        main_window.ccd_single_wl = wl
        main_window.ccd_single_intensity = intensity
        '''update figure plot'''
        update_ccd_single_spectrum_graph()

    def ccd_multi_acq():
        wl, intensity = horiba.acquire_spectrum_stitch(main_window.horiba_from, main_window.horiba_to,
                                                       main_window.horiba_acqtime, main_window.horiba_acc)
        wl = wl.tolist()
        intensity = intensity.tolist()
        '''prepare data to be saved'''
        main_window.ccd_single_wl = wl
        main_window.ccd_single_intensity = intensity
        '''update figure plot'''
        update_ccd_single_spectrum_graph()

    '''acquisition function'''
    def start_acquire_1D_ppc():
        print('---initial delay array---')
        print(main_window.delay_scan_array)
        abs_mm_list = transform_ps_mm(main_window.delay_scan_array, main_window.delay_zero_position)
        acquire_1D_ppc.transfer_args(main_window, c633, sr830, abs_mm_list)
        acquire_1D_ppc.start()


    '''update graph'''
    def update_1D_ppc_graph():
        main_window.p1.setData(y=acquire_1D_ppc.y_lia_list, x=acquire_1D_ppc.x_lia_list, pen='y')
        main_window.progb1.setValue(acquire_1D_ppc.progress)
        # time.sleep(0.1)

    def update_ccd_single_spectrum_graph():
        main_window.p2.setData(y=main_window.ccd_single_intensity, x=main_window.ccd_single_wl, pen='y')

    '''close process function'''
    def close_software():
        global horiba
        print('Unregister device')
        main_window.backendlia.lia_thread_flg = False
        main_window.backenddl.dl_thread_flg = False
        if horiba == None:
            pass
        else:
            backend_horiba.horiba_thread_flg = False
            del horiba
        time.sleep(1)
        sr830.disconnect()
        print('sr830 disconnected')
        c633.disconnect()
        print('PI delay line disconnected')
        # if horiba == None:
        #     pass
        # else:
        #     del horiba

    main_window.show()
    sys.exit(app.exec_())