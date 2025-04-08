import time
import serial
from serial.tools import list_ports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class run_plots:
    def __init__(self, ctk_window):
        self.ctk_window = ctk_window
        self.config = ctk_window.current_config
        self.running = ctk_window.running
        self.update_loop()

    def update_loop(self):
        if not self.running:
            return

        com_name = f"COM{self.config.com_port}"
        baud_value = self.config.baud_rate
        serial_variables = self.config.serial_variables
        lines = self.config.lines
        plots = self.config.plots
        figures = self.ctk_window.fig_objects
        axes = self.ctk_window.ax_objects
        canvases = self.ctk_window.canvas_objects
        time_elapsed = 0
        ports = list_ports.comports()

        if com_name not in ports:
            error_message = "COM port {com_name} does not exist."
            error_title = "COM Port Not Found"
            open_missing_com_warning()
            return

        try:
            serial_com = serial.Serial(com_name, baud_value)
        except:
            error_message = "Either the port {com_name} is unavaliable or the baud rate {baud_value} is incorrect."
            error_title = "Unavailable COM Port or Incorrect Baud Rate"
            open_serial_com_warning(error_message, error_title, com_name, baud_value)
            return

        # Reset arduino
        serial_com.setDTR(False)
        time.sleep(1)
        serial_com.flushInput()
        serial_com.setDTR(True)

        # Loop through data
        time_start = time.time()
        while True:
            try:
                # Read the serial ine
                s_bytes = serial_com.readline()
                decoded_bytes = s_bytes.decode("utf-8").strip('\r\n')

                # Parse the decoded line
                values = decoded_bytes.split(",")

                # Append data values to their respective serial variable data arrays
                v = 0
                for v in range(len(values)):
                    try:
                        serial_var = [serial_obj for serial_obj in serial_variables if serial_obj.variable_number == v][0]
                    except IndexError:
                        serial_var = None
                    
                    serial_var.data_array.append(float(values[v]))

                # Update data arrays for line objects
                for line_obj in lines:
                    x_serial = line_obj.x_serial
                    y_serial = line_obj.y_serial
                    if len(x_serial.data_array) == len(y_serial.data_array):
                        line_obj.set_data(x_serial.data_array, y_serial.data_array)
                
                # #Update axis limits and figures
                # for plot_obj in plots:
                #     ax = axes.get(plot_obj.plot_title)
                #     ax.relim()
                #     ax.autoscale()

                #     canvas = canvases.get(plot_obj.plot_title)
                #     canvas.draw()
                #     canvas.

                # for ax in axes:
                #     ax.relim()
                #     ax.autoscale()
                
                # # Update figures
                # for fig in figures:
                #     canvas = 
                #     canvas.draw()
                #     canvas.flush_events()
                
            except:
                # Error for bad data
                error_message = "Bad serial data has been detected at time t={time_elapsed}s."
                error_title = "Bad Serial Data"
                open_bad_serial_warning(error_message, error_title, time_elapsed)
                #print("MEOW")
                break

            # Check elapsed time
            time_current = time.time()
            time_elapsed = time_current - time_start
        return

def open_missing_com_warning(error_message, error_title, com_name):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, com_name=com_name)
    error_win.mainloop()

def open_serial_com_warning(error_message, error_title, com_name, baud_value):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, com_name=com_name, baud_value=baud_value)
    error_win.mainloop()

def open_bad_serial_warning(error_message, error_title, time_elapsed):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, time_elapsed=time_elapsed)
    error_win.mainloop()