import time
import json
import serial
import multiprocessing as mlt
from collections import Counter
from serial.tools import list_ports
from resource_manager import COMMUNICATION, CURRENT_CONFIG
from configuration import configuration
from plots import plot
from lines import line
from data_manager import update_metadata, is_csv_empty
from date_and_time import get_trial_date

class run_plots:
    def __init__(self):
        self.plot_cycle_termination_event = mlt.Event()

    def start_gui_plot_processes(self):
        # plot_cycle_termination_event = mlt.Event()
        gui_plot_cycle_process = mlt.Process(target=self.gui_plot_cycle, args=(self.plot_cycle_termination_event, ))
        gui_plot_cycle_process.start()
        # if self.plot_cycle_termination_event.is_set():
        #     gui_plot_cycle_process.join()
        # return

    def gui_plot_cycle(self, termination_event):
        # Creates objects related to port validation and access which are mutable within the memory space of the process
        self.port_objs = list_ports.comports()
        self.port_names = [port.device for port in self.port_objs]
        self.serial_com = serial.Serial()
        # print("Plot cycle process has been entered!")
        # Creates a communication dictionary from communication.json
        communication_dict = read_communication_file()
        # communication_dict['valid_port'] = False
        while True:
            # Checks if the module currently designated to write in communication.json is the backend_module
            time.sleep(0.001)
            if (
                communication_dict['designated_author'] == 'backend'
                and communication_dict['gui'] == 'waiting'
                and communication_dict['backend'] == 'requested'
                ):
                communication_dict['gui'] = 'requested' # Updating communication dict to request the gui module to run one of its methods
                communication_dict['update_config_to_json'] = True # Updating communication dict to tell the gui module which method is being requested
                communication_dict['designated_author'] = 'gui' # Changing the designated author before writing the new communication dict to communication.json to prevent two modules writing into it at once
                communication_dict['backend'] = 'waiting'
                # Dictionary of which keys must have what value in communication.json in order to unpause once the request has been completed by the gui module
                unpause_dict = {
                    'update_gui_plots': True,
                    'update_config_to_json': False,
                    'gui': 'waiting',
                    'backend': 'requested',
                    'designated_author': 'backend'
                }
                write_and_wait_function(unpause_dict, communication_dict, f"Backend has requested gui to update config.json and is waiting! - Running status = {communication_dict['running']}") # Waits for the gui module to confirm that it has completed the requested task before continuing the backend process
                config = config_from_json()
                communication_dict = read_communication_file()
                if communication_dict['exit_gui']:
                    break
            else:
                communication_dict['skip_to_beginning'] = True
                config = None

            if not communication_dict['skip_to_beginning'] and isinstance(config, configuration):
                self.update_gui_plots(communication_dict, config)

            if (
                not communication_dict['skip_to_beginning']
                and not communication_dict['validate_port_settings']
                and communication_dict['generate_gui_plots']
                and communication_dict['gui'] == 'requested'
                and communication_dict['backend'] == 'waiting'
                and communication_dict['designated_author'] == 'gui'
            ):
                unpause_dict = {
                    'validate_port_settings': True,
                    'generate_gui_plots': False,
                    'gui': 'waiting',
                    'backend': 'requested',
                    'designated_author': 'backend'
                }
                write_and_wait_function(unpause_dict, communication_dict, f"Process has requested and is waiting for gui to generate plots! - Running status = {communication_dict['running']}")
                communication_dict = read_communication_file()
                if communication_dict['exit_gui']:
                    break

            if (
                communication_dict['running']
                and not communication_dict['valid_port']
                and not communication_dict['skip_to_beginning']
                and communication_dict['validate_port_settings']
                and communication_dict['gui'] == 'waiting'
                and communication_dict['backend'] == 'requested'
                and communication_dict['designated_author'] == 'backend'
                and not communication_dict['error_triggered']
            ):
                self.validate_port_settings(communication_dict, config)

            if (
                communication_dict['running']
                and not communication_dict['skip_to_beginning']
                and communication_dict['obtain_serial_data']
                and communication_dict['gui'] == 'waiting'
                and communication_dict['backend'] == 'requested'
                and communication_dict['designated_author'] == 'backend'
                and communication_dict['valid_port']
            ):
                self.obtain_serial_data(communication_dict)
            
            if (
                communication_dict['running']
                and not communication_dict['skip_to_beginning']
                and communication_dict['plot_serial_data']
                and communication_dict['gui'] == 'requested'
                and communication_dict['backend'] == 'waiting'
                and communication_dict['designated_author'] == 'gui'
                and communication_dict['serial_values']
            ):
                unpause_dict = {
                    'plot_serial_data': False,
                    'gui': 'waiting',
                    'backend': 'requested',
                    'designated_author': 'backend'
                }
                write_and_wait_function(unpause_dict, communication_dict, f"Process has requested and is waiting for the gui to plot the serial data! - Running status = {communication_dict['running']}")
                communication_dict = read_communication_file()
                if communication_dict['exit_gui']:
                    break

            if communication_dict['exit_gui']:
                break
            else:
                communication_dict['serial_values'] = []
                communication_dict['update_gui_plots'] = False
                communication_dict['generate_gui_plots'] = False
                communication_dict['validate_port_settings'] = False
                communication_dict['obtain_serial_data'] = False
                communication_dict['plot_serial_data'] = False
                communication_dict['update_config_to_json'] = False
                communication_dict['skip_to_beginning'] = False
                communication_dict['gui'] = 'waiting'
                communication_dict['backend'] = 'requested'
                communication_dict['designated_author'] = 'backend'
            write_communication_file(communication_dict)
        # print(f"Process has been broken out of!")
        # print(f"Exit GUI? - {communication_dict['exit_gui']}")
        reset_config_json()
        return termination_event.set()

    def update_gui_plots(self, communication_dict: dict, config: configuration):
        # print(f"Process has begun updating gui plots! - Running status = {communication_dict['running']}")
        plot_dict = deserialize_plot_dict(communication_dict['plot_dict'])
        plots = config.plots
        matching_plots = False
        dict_plot_objs = [plot_key for plot_key in plot_dict]
        matching_plots = Counter(dict_plot_objs) == Counter(plots)
        if matching_plots:
            matching_plots = all(next((True for plot_key, ax_line_list in plot_dict.items() if plot_key == plot_obj and Counter(ax_line_list) == Counter(plot_obj.lines)), False) for plot_obj in plots)
        if not matching_plots:
            # print(f"The config plots and dict plots do not match! - Running status = {communication_dict['running']}")
            communication_dict['gui'] = 'requested'
            communication_dict['generate_gui_plots'] = True
            communication_dict['update_gui_plots'] = False
            communication_dict['designated_author'] = 'gui'
            communication_dict['backend'] = 'waiting'
            return
        elif plots and matching_plots and communication_dict['running'] and communication_dict['valid_port']:
            # print(f"The GUI plots do not need to be generated and the process is ready to obtain serial data! - Running status = {communication_dict['running']}")
            communication_dict['update_gui_plots'] = False
            communication_dict['validate_port_settings'] = False
            communication_dict['obtain_serial_data'] = True
            return
        elif not plots:
            # print(f"The config has no plots!")
            communication_dict['skip_to_beginning'] = True
            communication_dict['update_gui_plots'] = False
            return
        elif matching_plots and communication_dict['running'] and not communication_dict['valid_port']:
            # print(f"The GUI plots do not need to be generated but the process is not ready to obtain serial data! - Running status = {communication_dict['running']}")
            communication_dict['update_gui_plots'] = False
            communication_dict['validate_port_settings'] = True
            return
        else:
            # print(f"The GUI plots do not need to be generated! - Running status = {communication_dict['running']}")
            communication_dict['update_gui_plots'] = False
            communication_dict['skip_to_beginning'] = True
            return

    def validate_port_settings(self, communication_dict: dict, config: configuration):
        # print(f"Process has begun validating port settings! - Running status = {communication_dict['running']}")
        com_port = f"COM{config.com_port}"
        baud_rate = int(config.baud_rate)
        valid_port = communication_dict['valid_port']
        if not isinstance(self.serial_com, serial.Serial):
            self.serial_com = serial.Serial()
        if isinstance(self.serial_com, serial.Serial):
            if not com_port in self.port_names:
                error_message = f"The port {com_port} does not exist!"
                error_title = "COM Port Not Found"
                error_function(error_message, error_title, com_port=com_port)
                communication_dict['valid_port'] = False
                communication_dict['skip_to_beginning'] = True
                communication_dict['validate_port_settings'] = False
                communication_dict['error_triggered'] = True
                return
            if self.serial_com.port != com_port or self.serial_com.baudrate != baud_rate:
                valid_port = False
                try:
                    self.serial_com = serial.Serial(com_port, baud_rate)
                    # print(f"Process has created the serial com! - Running status = {communication_dict['running']}")
                except:
                    # print(f"Process failed to create serial com! - Running status = {communication_dict['running']}")
                    error_message = f"Either the port {com_port} is unavaliable or the baud rate {baud_rate} is incorrect!"
                    error_title = "Unavailable COM Port or Incorrect Baud Rate"
                    error_function(error_message, error_title, com_port=com_port, baud_rate=baud_rate)
                    communication_dict['valid_port'] = False
                    communication_dict['skip_to_beginning'] = True
                    communication_dict['validate_port_settings'] = False
                    communication_dict['error_triggered'] = True
                    return
            if not valid_port:
                self.serial_com.setDTR(False)
                time.sleep(0.01)
                self.serial_com.flushInput()
                self.serial_com.setDTR(True)
            communication_dict['valid_port'] = True
            communication_dict['obtain_serial_data'] = True
            communication_dict['validate_port_settings'] = False
            # print(f"Process has validated port settings! - Running status = {communication_dict['running']}")
            return
        else:
            error_message = "Mismatched serial class!"
            error_title = "Mismatched Serial Class"
            error_function(error_message, error_title)
            communication_dict['valid_port'] = False 
            communication_dict['skip_to_beginning'] = True
            communication_dict['validate_port_settings'] = False
            communication_dict['error_triggered'] = True
            return

    def obtain_serial_data(self, communication_dict: dict):
        # print(f"Process has begun to obtain serial data! - Running status = {communication_dict['running']}")
        csv_recording = communication_dict['csv_recording']
        print(f"NEW TRIAL 2 - {communication_dict['new_trial']}")
        if is_csv_empty():
            trial_date = get_trial_date()
            update_metadata(trial_date, csv_recording, communication_dict)
        else:
            trial_date = None
        try:
            serial_bytes = self.serial_com.readline()
            decoded_bytes = serial_bytes.decode("utf-8").strip('\r\n')
            serial_values = decoded_bytes.split(',')
            update_metadata(serial_values, csv_recording, communication_dict)
            communication_dict['serial_values'] = serial_values
            communication_dict['gui'] = 'requested'
            communication_dict['plot_serial_data'] = True
            communication_dict['backend'] = 'waiting'
            communication_dict['obtain_serial_data'] = False
            communication_dict['designated_author'] = 'gui'
            # print(f"Process has successfully obtained serial values! - Running status = {communication_dict['running']}")
            return
        except:
            communication_dict['skip_to_beginning'] = True
            communication_dict['obtain_serial_data'] = False
            # print(f"Process failed to get serial values! - Running status = {communication_dict['running']}")
            return

def process_is_finished():
    return True

def write_and_wait_function(unpause_dict: dict, communication_dict: dict, my_message: str = None):
    communication_keys = [key for key in communication_dict]
    write_communication_file(communication_dict)
    # print(my_message)
    while True:
        test_communication_dict = read_communication_file()
        if all(key in test_communication_dict for key in communication_keys):
            comparison_dict = {key: test_communication_dict[key] for key in unpause_dict if key in test_communication_dict}
            if all(unpause_dict[key] == comparison_dict[key] for key in unpause_dict):
                break
            elif test_communication_dict['exit_gui']:
                break
        time.sleep(0.001)
    # print(f"Process has finished waiting for gui! - Running status = {communication_dict['running']}")
    return

def config_from_json():
    try:
        with open(CURRENT_CONFIG, "r") as file:
            config = json.load(file)
            return configuration.from_dict(config)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    
def write_communication_file(backend_to_gui_dict: dict):
    with open(COMMUNICATION, "w") as file:
        json.dump(backend_to_gui_dict, file, indent=4)
        return

def read_communication_file():
    try:
        with open(COMMUNICATION, "r") as file:
            gui_to_backend_dict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        gui_to_backend_dict = {}
    return gui_to_backend_dict

def error_function(error_message :str, error_title: str, **kwargs):
    from warning_window import alternate_error_window
    error_win = alternate_error_window(error_message, error_title, **kwargs)
    error_win.mainloop()

def deserialize_plot_dict(plot_dict_serialized: list):
    plot_dict = {}
    if not plot_dict_serialized:
        return plot_dict
    try:
        for item in plot_dict_serialized:
            new_key = plot.plot_from_dict(item[0])
            new_value = []
            for line_obj in item[1]:
                new_value.append(line.line_from_dict(line_obj))
            plot_dict[new_key] = new_value
    except:
        return TypeError
    return plot_dict

def reset_config_json():
    with open(CURRENT_CONFIG, "w") as file:
        json.dump({}, file, indent=4)
    return