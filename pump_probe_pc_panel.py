from PyQt5.Qt import QWidget, QApplication, QThread, pyqtSignal, QFileDialog, QMutex
from PyQt5 import QtWidgets
from PyQt5.QtGui import QKeySequence
from ui_pump_probe_pc import Ui_Pump_and_Probe
import time
import numpy as np
import pyqtgraph as pg



'''Backend thread for LIA'''
class BackendThreadLIA(QThread):
    snap_signal = pyqtSignal()
    lia_overload_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.lia_thread_flg = True

    def run(self):
        while self.lia_thread_flg:
            self.snap_signal.emit()
            self.lia_overload_signal.emit()
            # self.get_y.emit()
            # self.get_z.emit()
            # self.update_graph.emit()
            time.sleep(0.5)


'''Backend thread for Delay line'''
class BackendThreadDL(QThread):
    delay_real_pos_signal = pyqtSignal()
    delay_on_target_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.dl_thread_flg = True

    def run(self):
        while self.dl_thread_flg:
            self.delay_real_pos_signal.emit()
            self.delay_on_target_signal.emit()
            time.sleep(0.5)


class Window(QWidget, Ui_Pump_and_Probe):
    '''close signal for software'''
    close_signal = pyqtSignal()
    '''define lock in amplifer API signals'''
    input_type_signal = pyqtSignal(int)
    input_coupling_signal = pyqtSignal(int)
    input_gr_signal = pyqtSignal(int)
    lia_tau_signal = pyqtSignal(int)
    lia_sens_signal = pyqtSignal(int)
    lia_reserve_signal = pyqtSignal(int)
    lia_filter_signal = pyqtSignal(int)
    lia_ext_type_signal = pyqtSignal(int)
    lia_slope_signal = pyqtSignal(int)
    lia_sync_signal = pyqtSignal(int)
    lia_auto_phase_signal = pyqtSignal()
    lia_auto_gain_signal = pyqtSignal()
    lia_auto_reserve_signal = pyqtSignal()
    lia_external_signal = pyqtSignal()
    lia_internal_signal = pyqtSignal()
    lia_freq_signal = pyqtSignal(float)
    lia_amp_signal = pyqtSignal(float)

    '''define PI delay line API signals'''
    delay_ref_signal = pyqtSignal()
    delay_TP_signal = pyqtSignal(float)
    delay_vel_signal = pyqtSignal(float)
    delay_goleft_signal = pyqtSignal()
    delay_goright_signal = pyqtSignal()
    delay_halt_signal = pyqtSignal()
    delay_set_zero_signal = pyqtSignal(float)
    delay_start_pos_signal = pyqtSignal(float)
    delay_end_pos_signal = pyqtSignal(float)
    delay_step_size_signal = pyqtSignal(float)

    '''define horiba API signals'''
    horiba_connect_signal = pyqtSignal()
    horiba_disconnect_signal = pyqtSignal()
    horiba_set_wl_signal = pyqtSignal(float)
    horiba_set_horiba_from_signal = pyqtSignal(float)
    horiba_set_horiba_to_signal = pyqtSignal(float)
    horiba_set_acqtime_signal = pyqtSignal(float)
    horiba_set_acc_signal = pyqtSignal(int)
    horiba_set_rtd_signal = pyqtSignal(float)
    horiba_set_slit_signal = pyqtSignal(float)
    horiba_single_acq_signal = pyqtSignal()
    horiba_multi_acq_signal = pyqtSignal()


    '''define acquistion related signal'''
    pump_pc_start_signal = pyqtSignal()
    # pump_pc_stop_signal = pyqtSignal()
    # pump_pc_save_signal = pyqtSignal()



    def __init__(self):
        super().__init__()
        self.setupUi(self)

        '''Lock in amplifer widgets setting'''
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

        self.coupling = {
                        0: 'AC',
                        1: 'DC'
                        }

        self.input_mode = {
                            0: 'A',
                            1: 'A - B',
                            2: 'I (1 MΩ)',
                            3: 'I (100 MΩ)'
                            }

        self.ground = {
                        0: 'Float',
                        1: 'Ground'
                        }

        self.dict_reserve = {
                            0: 'High Reserve',
                            1: 'Normal',
                            2: 'Low Noise'
                            }

        self.dict_Filter = {
                            0: 'No Filters',
                            1: 'Line Notch',
                            2: '2xLine Notch',
                            3: 'Both Notch'
        }

        self.dict_ext_type = {
                            0: 'Sine', 1: 'TTL Rising', 2: 'TTL Falling'
        }

        self.dict_filter_slope = {
                                    '6dB/oct': 0,
                                    '12dB/oct': 1,
                                    '18dB/oct': 2,
                                    '24dB/oct': 3
        }

        self.dict_sync = {
            'Off': 0, 'Below 200Hz': 1
        }

        self.spb_input_signal.get_dict(self.input_mode)
        self.spb_acdc.get_dict(self.coupling)
        self.spb_ground.get_dict(self.ground)
        self.spb_tc.get_dict(self.tau_set)
        self.spb_sens.get_dict(self.sens_set)
        self.spb_reserve.get_dict(self.dict_reserve)
        self.spb_filter.get_dict(self.dict_Filter)
        self.spb_signal_type.get_dict(self.dict_ext_type)

        self.comb_slope.addItems(('6dB/oct', '12dB/oct', '18dB/oct', '24dB/oct'))
        self.comb_sync.addItems(('Off', 'Below 200Hz'))
        # self.comb_slope.addItem('6dB/oct')
        # self.comb_slope.addItem('12dB/oct')
        # self.comb_slope.addItem('18dB/oct')
        # self.comb_slope.addItem('24dB/oct')


        '''initialise lia display widget'''
        self.lia_dis_x = True
        self.lia_dis_y = False
        self.lia_dis_r = False
        self.lia_dis_ps = False

        '''initialise lia sub thread'''
        self.backendlia = BackendThreadLIA()
        self.initbackendlia()

        '''initialise delay line sub thread'''
        self.backenddl = BackendThreadDL()
        self.initbackenddl()
        print('break point PI sub thread')


        '''PI delay stage widgets and variable setting'''
        self.step_mm = None
        self.delay_zero_position = 0
        self.delay_start_pos_value = None
        self.delay_end_pos_value = None
        self.delay_step_size_value = None
        self.delay_scan_point = None
        self.delay_scan_array = list()
        self.delay_scan_array_save = list()
        self.ppc_1D_y_data = list()

        '''horiba widgets and variable setting'''
        self.horiba_from = 0
        self.horiba_to = 0
        self.horiba_acqtime = 0.5
        self.horiba_acc = 1
        self.horiba_rtd_time = 0.5
        self.horiba_slit = 500
        self.ccd_single_wl = list()
        self.ccd_single_intensity = list()

        '''data acquisition variable'''
        self.single_ppc_continue = True

        '''graphic view section'''
        self.p1 = self.graphic_widget1.plot()
        self.p1.setPen((200, 200, 100))
        self.graphic_widget1.setLabel('left', 'Amplitude', units='V')
        self.graphic_widget1.setLabel('bottom', 'Delay Time', units='ps')

        # self.progb1.setValue(30)
        self.p2 = self.graphic_widget2.plot()
        self.p2.setPen((200, 200, 100))
        self.graphic_widget2.setLabel('left', 'Intensity', units='a.u.')
        self.graphic_widget2.setLabel('bottom', 'Wavelength', units='nm')

    '''slot function of LIA in Ui_form'''
    def lia_in_sig_change(self):
        key = self.spb_input_signal.value()
        print(key)
        self.input_type_signal.emit(key)

    def lia_in_couple_change(self):
        key = self.spb_acdc.value()
        print(key)
        self.input_coupling_signal.emit(key)

    def lia_ground_change(self):
        key = self.spb_ground.value()
        print(key)
        self.input_gr_signal.emit(key)

    def lia_tc_change(self):
        key = self.spb_tc.value()
        print(key)
        self.lia_tau_signal.emit(key)

    def lia_sens_change(self):
        key = self.spb_sens.value()
        print(key)
        self.lia_sens_signal.emit(key)

    def lia_reserve_change(self):
        key = self.spb_reserve.value()
        print(key)
        self.lia_reserve_signal.emit(key)

    def lia_filter_change(self):
        key = self.spb_filter.value()
        print(key)
        self.lia_filter_signal.emit(key)

    def lia_ext_type_change(self):
        key = self.spb_signal_type.value()
        print(key)
        self.lia_ext_type_signal.emit(key)

    def lia_slope_change(self):
        key = self.comb_slope.currentText()
        command = self.dict_filter_slope[key]
        print(command)
        self.lia_slope_signal.emit(command)

    def lia_sync_change(self):
        key = self.comb_sync.currentText()
        command = self.dict_sync[key]
        print(command)
        self.lia_sync_signal.emit(command)

    def lia_auto_phase(self):
        self.lia_auto_phase_signal.emit()

    def lia_auto_gain(self):
        self.lia_auto_gain_signal.emit()

    def lia_auto_reserve(self):
        self.lia_auto_reserve_signal.emit()

    def lia_external(self):
        self.lbl_ref.setText('External')
        self.lia_external_signal.emit()

    def lia_internal(self):
        self.lbl_ref.setText('Internal')
        self.lia_internal_signal.emit()

    def lia_freq_change(self):
        fre = float(self.ledit_fre.text())
        self.lia_freq_signal.emit(fre)

    def lia_amp_change(self):
        amp = float(self.ledit_amp.text())
        self.lia_amp_signal.emit(amp)

    def lia_x_select(self):
        if self.lia_dis_x:
            self.lia_dis_x = True
            self.lia_dis_y = False
            self.lia_dis_r = False
            self.lia_dis_ps = False
        else:
            self.lia_dis_x = True
            self.lia_dis_y = False
            self.lia_dis_r = False
            self.lia_dis_ps = False

    def lia_y_select(self):
        if self.lia_dis_y:
            self.lia_dis_x = False
            self.lia_dis_y = True
            self.lia_dis_r = False
            self.lia_dis_ps = False
        else:
            self.lia_dis_x = False
            self.lia_dis_y = True
            self.lia_dis_r = False
            self.lia_dis_ps = False

    def lia_r_select(self):
        if self.lia_dis_r:
            self.lia_dis_x = False
            self.lia_dis_y = False
            self.lia_dis_r = True
            self.lia_dis_ps = False
        else:
            self.lia_dis_x = False
            self.lia_dis_y = False
            self.lia_dis_r = True
            self.lia_dis_ps = False

    def lia_ps_select(self):
        if self.lia_dis_ps:
            self.lia_dis_x = False
            self.lia_dis_y = False
            self.lia_dis_r = False
            self.lia_dis_ps = True
        else:
            self.lia_dis_x = False
            self.lia_dis_y = False
            self.lia_dis_r = False
            self.lia_dis_ps = True

    '''slot function of Delay stage in Ui_form'''
    def delay_ref_clicked(self):
        self.delay_ref_signal.emit()

    def delay_TP_change(self):
        value = float(self.ledit_PI_TP.text())
        self.delay_TP_signal.emit(value)

    def delay_SS_change(self):
        self.step_mm = float(self.ledit_PI_SS.text())

    def delay_vel_change(self):
        value = float(self.ledit_PI_vel.text())
        self.delay_vel_signal.emit(value)

    def delay_go_left(self):
        self.delay_goleft_signal.emit()

    def delay_go_right(self):
        self.delay_goright_signal.emit()

    def delay_halt(self):
        self.delay_halt_signal.emit()

    def delay_set_zero_change(self):
        value = float(self.ledit_PI_zero.text())
        self.delay_set_zero_signal.emit(value)

    def delay_start_pos(self):
        value = float(self.ledit_PI_sp.text())
        self.delay_start_pos_signal.emit(value)

    def delay_end_pos(self):
        value = float(self.ledit_PI_ep.text())
        self.delay_end_pos_signal.emit(value)

    def delay_step_size(self):
        value = float(self.ledit_PI_ssp.text())
        self.delay_step_size_signal.emit(value)

    '''slot function of horiba in Ui_form'''
    def horiba_connect(self):
        self.horiba_connect_signal.emit()

    def horiba_disconnect(self):
        self.horiba_disconnect_signal.emit()

    def set_horiba_wl(self):
        value = float(self.ledit_specto_center.text())
        self.horiba_set_wl_signal.emit(value)

    def set_horiba_from(self):
        value_from = float(self.ledit_spec_from.text())
        self.horiba_set_horiba_from_signal.emit(value_from)

    def set_horiba_to(self):
        value_to = float(self.ledit_spec_to.text())
        self.horiba_set_horiba_to_signal.emit(value_to)

    def set_horiba_actime(self):
        value = float(self.ledit_acq_time.text())
        self.horiba_set_acqtime_signal.emit(value)

    def set_horiba_acc(self):
        value = int(self.ledit_spec_acc.text())
        self.horiba_set_acc_signal.emit(value)

    def set_horiba_rta_t(self):
        value = float(self.ledit_rtd_time.text())
        self.horiba_set_rtd_signal.emit(value)

    def set_horiba_slit(self):
        value = float(self.ledit_specto_slit.text())
        self.horiba_set_slit_signal.emit(value)

    def enable_horiba_range(self, status):
        self.ledit_spec_from.setEnabled(status)
        self.ledit_spec_to.setEnabled(status)

    def ccd_single_acq(self):
        self.ccd_single_wl = []
        self.ccd_single_intensity = []
        self.horiba_single_acq_signal.emit()

    def ccd_cont_acq(self):                     # use for multiwindow scan with range
        self.ccd_single_wl = []
        self.ccd_single_intensity = []
        self.horiba_multi_acq_signal.emit()

    def ccd_spec_stop(self):
        pass

    def ccd_spec_save(self):
        """'C:/Users/Cambridge-OSD/Desktop/Users'""" # the lab desktop data storage file
        saved_file_path = QFileDialog.getSaveFileName(self, 'Save data', 'C:/Users/Cambridge-OSD/Desktop/Users/',
                                                      'All(*.*);;text file(*.txt);;csv file(*.csv)', 'text file(*.txt)')
        ccd_data = np.column_stack((self.ccd_single_wl, self.ccd_single_intensity))
        if saved_file_path[0] == '':
            # print('empty')
            pass
        else:
            with open(saved_file_path[0], "w") as file:
                for line in ccd_data:
                    v1, v2 = line
                    file.write('{0},  {1}\n'.format(v1, v2))
                file.close()


    '''backend function for lia'''
    def initbackendlia(self):
        self.backendlia.start()

    '''beckend function for delay line'''
    def initbackenddl(self):
        self.backenddl.start()


    """Data acquisition section"""
    '''1D pump probe photocurrent'''
    def pump_pc_start(self):
        # self.delay_scan_array = []
        # self.ppc_1D_y_data = []
        self.single_ppc_continue = True
        self.pump_pc_start_signal.emit()

    def pump_pc_stop(self):
        self.single_ppc_continue = False
        # self.pump_pc_stop_signal.emit()

    def pump_pc_save(self):
        """'C:/Users/Cambridge-OSD/Desktop/Users'""" # the lab desktop data storage file
        saved_file_path = QFileDialog.getSaveFileName(self, 'Save data', 'C:/Users/Cambridge-OSD/Desktop/Users/',
                                                      'All(*.*);;text file(*.txt);;csv file(*.csv)', 'text file(*.txt)')
        ppc_1D_data = np.column_stack((self.delay_scan_array_save, self.ppc_1D_y_data))
        if saved_file_path[0] == '':
            # print('empty')
            pass
        else:
            with open(saved_file_path[0], "w") as file:
                for line in ppc_1D_data:
                    v1, v2 = line
                    file.write('{0},  {1}\n'.format(v1, v2))
                file.close()



    def closeEvent(self, event):
        self.close_signal.emit()
        print('Program closed')
        print('event: {0}'.format(event))
        event.accept()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    my_window = Window()
    my_window.show()
    sys.exit(app.exec_())

"""TODO data visualization and progress bar"""