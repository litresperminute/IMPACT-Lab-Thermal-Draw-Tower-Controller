import time
import serial
import threading
from serial.tools import list_ports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class run_plots:
    def __init__(self, ctk_window):
        self.ctk_window = ctk_window
        self.config = ctk_window.current_config
        #self.running = ctk_window.running

        figs = []
        axes =[]
        matplot_lines = []

        self.serial_reading_thread(figs, axes, matplot_lines)
        self.plot_number = len(self.config.plots)

    def serial_reading_thread(self, figs, axes, matplot_lines):
        if not self.ctk_window.running:
            return

        # Generate figures and their axes
        for plot_obj in self.config.plots:
            fig, ax = plt.subplots()

            ax_lines = []

            if len(plot_obj.lines) != 0:
                for line_obj in plot_obj.lines:
                    ax_line, = ax.plot(line_obj.x_serial.data_array, line_obj.y_serial.data_array, label=line_obj.label, color=line_obj.color)
                    ax_lines.append([ax_line, line_obj.x_serial.variable_number, line_obj.y_serial.variable_number])
                ax.legend(loc=plot_obj.legend_position)

            ax.set_title(plot_obj.plot_title)
            ax.set_xlabel(plot_obj.x_label)
            ax.set_ylabel(plot_obj.y_label)
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
            ax.grid()

            figs.append([fig, plot_obj.plot_position])
            axes.append(ax)
            matplot_lines.append(ax_lines)
        
        thread = threading.Thread(target=self.serial_reading_loop, args=(figs, axes, matplot_lines), daemon=True)
        thread.start()

    def serial_reading_loop(self, figs, axes, matplot_lines):
        com_port = f"COM{self.config.com_port}"
        baud_rate = self.config.baud_rate
        serial_variables = self.config.serial_variables
        lines = self.config.lines
        plots = self.config.plots
        ports = list_ports.comports()
        port_names = [port.device for port in ports]

        if com_port not in port_names:
            error_message = "Port {com_port} does not exist."
            error_title = "COM Port Not Found"
            open_missing_com_warning(error_message, error_title, com_port)
            self.ctk_window.running = False
            return

        try:
            serial_com = serial.Serial(com_port, baud_rate)
        except:
            error_message = "Either the port {com_port} is unavaliable or the baud rate {baud_rate} is incorrect."
            error_title = "Unavailable COM Port or Incorrect Baud Rate"
            open_serial_com_warning(error_message, error_title, com_port, baud_rate)
            self.ctk_window.running = False
            return

        serial_com.setDTR(False)
        time.sleep(5)
        serial_com.flushInput()
        serial_com.setDTR(True)

        while True:
            if not self.ctk_window.running:
                break
            try:
                serial_bytes = serial_com.readline()
                print("Line has been read", flush=True)
                decoded_bytes = serial_bytes.decode("utf-8").strip('\r\n')
                print("decoding successful")
                values = decoded_bytes.split(",")
                v = 0
                for v in range(len(values)):
                    serial_objs = [serial_var for serial_var in serial_variables if serial_var.variable_number == v]
                    print("matching serial variables found")
                    for serial_obj in serial_objs:
                        serial_obj.data_array.append(float(values[v].strip()))
                        print("serial variables have had their data arrays updated")
                        #print(serial_obj.data_array)
                print("serial data arrays have been updates")
                for ax_lines in matplot_lines:
                    print("for ax lines in matplot lines")
                    for ax_line in ax_lines:
                        print("for ax line in ax lines")
                        for serial_obj in serial_variables:
                            if ax_line[1] == serial_obj.variable_number:
                                print("matplot line updated x array")
                                x_array = serial_obj.data_array
                            elif ax_line[2] == serial_obj.variable_number:
                                y_array = serial_obj.data_array
                                print("matplot line updated y array")
                        ax_line[0].set_data(x_array, y_array)
                
                for ax in axes:
                    ax.relim()
                    ax.autoscale()

                for fig in figs:
                    def draw_canvas():
                        canvas = FigureCanvasTkAgg(fig[0], self.ctk_window)
                        canvas.draw()
                        fig[0].tight_layout()
                        canvas_widget = canvas.get_tk_widget()
                        fig[0].subplots_adjust(right=0.75, bottom=0.25, top=0.85)
                        canvas_widget.grid(row=fig[1][0], column=fig[1][1], sticky="nsew")
                        self.ctk_window.grid_rowconfigure(fig[1][0], weight=1)
                        self.ctk_window.grid_columnconfigure(fig[1][1], weight=1)
                    self.ctk_window.after(0, draw_canvas)
                
            except:
                continue

def open_missing_com_warning(error_message, error_title, com_port):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, com_port=com_port)
    error_win.mainloop()

def open_serial_com_warning(error_message, error_title, com_port, baud_rate):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, com_port=com_port, baud_rate=baud_rate)
    error_win.mainloop()

def open_bad_serial_warning(error_message, error_title, time_elapsed):
    from warning_window import error_window
    error_win = error_window(error_message, error_title, time_elapsed=time_elapsed)
    error_win.mainloop()