import customtkinter as ctk
from PIL import Image
from configuration import configuration, configurations

class duplicateWarningWindow(ctk.CTkToplevel):
    def __init__(self, newConfigName):
        super().__init__()
        self.title("Live Serial Reader - Duplicate Configuration Names")
        self.geometry("435x200")
        self.resizable(False, False)
        self.lift()
        
        self.iconbitmap("Resources/serial_port_icon_blue.ico")

        self.grid_columnconfigure(0, weight=1)

        error_icon = Image.open('Resources/error_icon.png')
        self.error_image = ctk.CTkImage(light_image=error_icon, size=(47, 47))

        self.error_frame = ctk.CTkFrame(self, width=100, height=37)
        self.error_frame.grid(row=0, column=0, padx=10, pady=5)

        self.error_image_label = ctk.CTkLabel(self.error_frame, text="", image=self.error_image)
        self.error_image_label.grid(row=0, column=0, padx=5, pady=10)

        error_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")
        error_message_font = ctk.CTkFont(family="Helvetica", size=12)

        self.error_text = ctk.CTkLabel(self.error_frame, text="ERROR!", font=error_font)
        self.error_text.grid(row=0, column=1, padx=5)

        self.error_message = ctk.CTkLabel(self, text=f"The configuration enetered already exists:\n\n\"{newConfigName}\"", font=error_message_font)
        self.error_message.grid(row=1, column=0, pady=5, padx=10)

        self.button = ctk.CTkButton(self, text="Cancel", command=self.cancelNewConfig)
        self.button.grid(row=2, column=0, pady=5, padx=20)

    def cancelNewConfig(self):
        self.destroy()

class serial_error_window1(ctk.CTkToplevel):
    def __init__(self, serial_num):
        super().__init__()
        self.title("Live Serial Reader - Duplicate Serial Variable")
        self.geometry("435x200")
        self.resizable(False, False)
        self.lift()
        self.iconbitmap("Resources/serial_port_icon_blue.ico")
        self.grid_columnconfigure(0, weight=1)

        error_icon = Image.open('Resources/error_icon.png')
        self.error_image = ctk.CTkImage(light_image=error_icon, size=(47, 47))

        self.error_frame = ctk.CTkFrame(self, width=100, height=37)
        self.error_frame.grid(row=0, column=0, padx=10, pady=5)

        self.error_image_label = ctk.CTkLabel(self.error_frame, text="", image=self.error_image)
        self.error_image_label.grid(row=0, column=0, padx=5, pady=10)

        error_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")
        error_message_font = ctk.CTkFont(family="Helvetica", size=12)

        self.error_text = ctk.CTkLabel(self.error_frame, text="ERROR!", font=error_font)
        self.error_text.grid(row=0, column=1, padx=5)

        self.error_message = ctk.CTkLabel(self, text=f"The serial number enetered already exists or is invalid:\n\n\"{serial_num}\"", font=error_message_font)
        self.error_message.grid(row=1, column=0, pady=5, padx=10)

        self.button = ctk.CTkButton(self, text="Cancel", command=self.cancelNewSerial1)
        self.button.grid(row=2, column=0, pady=5, padx=20)

    def cancelNewSerial1(self):
        self.destroy()

class serial_error_window2(ctk.CTkToplevel):
    def __init__(self, serial_name):
        super().__init__()
        self.title("Live Serial Reader - Duplicate Serial Name")
        self.geometry("435x200")
        self.resizable(False, False)
        self.lift()
        self.iconbitmap("Resources/serial_port_icon_blue.ico")
        self.grid_columnconfigure(0, weight=1)

        error_icon = Image.open('Resources/error_icon.png')
        self.error_image = ctk.CTkImage(light_image=error_icon, size=(47, 47))

        self.error_frame = ctk.CTkFrame(self, width=100, height=37)
        self.error_frame.grid(row=0, column=0, padx=10, pady=5)

        self.error_image_label = ctk.CTkLabel(self.error_frame, text="", image=self.error_image)
        self.error_image_label.grid(row=0, column=0, padx=5, pady=10)

        error_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")
        error_message_font = ctk.CTkFont(family="Helvetica", size=12)

        self.error_text = ctk.CTkLabel(self.error_frame, text="ERROR!", font=error_font)
        self.error_text.grid(row=0, column=1, padx=5)

        self.error_message = ctk.CTkLabel(self, text=f"The serial name enetered already exists:\n\n\"{serial_name}\"", font=error_message_font)
        self.error_message.grid(row=1, column=0, pady=5, padx=10)

        self.button = ctk.CTkButton(self, text="Cancel", command=self.cancelNewSerial2)
        self.button.grid(row=2, column=0, pady=5, padx=20)

    def cancelNewSerial2(self):
        self.destroy()

class baud_error_window1(ctk.CTkToplevel):
    def __init__(self, baud_value):
        super().__init__()
        self.title("Live Serial Reader - Invalid Baud Rate")
        self.geometry("435x200")
        self.resizable(False, False)
        self.lift()
        self.iconbitmap("Resources/serial_port_icon_blue.ico")
        self.grid_columnconfigure(0, weight=1)

        error_icon = Image.open('Resources/error_icon.png')
        self.error_image = ctk.CTkImage(light_image=error_icon, size=(47, 47))

        self.error_frame = ctk.CTkFrame(self, width=100, height=37)
        self.error_frame.grid(row=0, column=0, padx=10, pady=5)

        self.error_image_label = ctk.CTkLabel(self.error_frame, text="", image=self.error_image)
        self.error_image_label.grid(row=0, column=0, padx=5, pady=10)

        error_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")
        error_message_font = ctk.CTkFont(family="Helvetica", size=12)

        self.error_text = ctk.CTkLabel(self.error_frame, text="ERROR!", font=error_font)
        self.error_text.grid(row=0, column=1, padx=5)

        self.error_message = ctk.CTkLabel(self, text=f"The baud rate {baud_value} is invalid.", font=error_message_font)
        self.error_message.grid(row=1, column=0, pady=5, padx=10)

        self.button = ctk.CTkButton(self, text="Cancel", command=self.cancelNewBaud)
        self.button.grid(row=2, column=0, pady=5, padx=20)

    def cancelNewBaud(self):
        self.destroy()

class com_error_window1(ctk.CTkToplevel):
    def __init__(self, com_value):
        super().__init__()
        self.title("Live Serial Reader - Invalid COM Port")
        self.geometry("435x200")
        self.resizable(False, False)
        self.lift()
        self.iconbitmap("Resources/serial_port_icon_blue.ico")
        self.grid_columnconfigure(0, weight=1)

        error_icon = Image.open('Resources/error_icon.png')
        self.error_image = ctk.CTkImage(light_image=error_icon, size=(47, 47))

        self.error_frame = ctk.CTkFrame(self, width=100, height=37)
        self.error_frame.grid(row=0, column=0, padx=10, pady=5)

        self.error_image_label = ctk.CTkLabel(self.error_frame, text="", image=self.error_image)
        self.error_image_label.grid(row=0, column=0, padx=5, pady=10)

        error_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")
        error_message_font = ctk.CTkFont(family="Helvetica", size=12)

        self.error_text = ctk.CTkLabel(self.error_frame, text="ERROR!", font=error_font)
        self.error_text.grid(row=0, column=1, padx=5)

        self.error_message = ctk.CTkLabel(self, text=f"The COM port {com_value} is invalid.", font=error_message_font)
        self.error_message.grid(row=1, column=0, pady=5, padx=10)

        self.button = ctk.CTkButton(self, text="Cancel", command=self.cancelNewCom)
        self.button.grid(row=2, column=0, pady=5, padx=20)

    def cancelNewCom(self):
        self.destroy()

class csv_error_window1(ctk.CTkToplevel):
    def __init__(self, csv_name):
        super().__init__()
        self.title("Live Serial Reader - CSV File Error")
        self.geometry("435x200")
        self.resizable(False, False)
        self.lift()
        self.iconbitmap("Resources/serial_port_icon_blue.ico")
        self.grid_columnconfigure(0, weight=1)

        error_icon = Image.open('Resources/error_icon.png')
        self.error_image = ctk.CTkImage(light_image=error_icon, size=(47, 47))

        self.error_frame = ctk.CTkFrame(self, width=100, height=37)
        self.error_frame.grid(row=0, column=0, padx=10, pady=5)

        self.error_image_label = ctk.CTkLabel(self.error_frame, text="", image=self.error_image)
        self.error_image_label.grid(row=0, column=0, padx=5, pady=10)

        error_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")
        error_message_font = ctk.CTkFont(family="Helvetica", size=12)

        self.error_text = ctk.CTkLabel(self.error_frame, text="ERROR!", font=error_font)
        self.error_text.grid(row=0, column=1, padx=5)

        self.error_message = ctk.CTkLabel(self, text=f"The CSV file {csv_name} is invalid.", font=error_message_font)
        self.error_message.grid(row=1, column=0, pady=5, padx=10)

        self.button = ctk.CTkButton(self, text="Cancel", command=self.cancelNewCSV)
        self.button.grid(row=2, column=0, pady=5, padx=20)

    def cancelNewCSV(self):
        self.destroy()

class csv_error_window2(ctk.CTkToplevel):
    def __init__(self, csv_name):
        super().__init__()
        self.title("Live Serial Reader - CSV File Error")
        self.geometry("435x200")
        self.resizable(False, False)
        self.lift()
        self.iconbitmap("Resources/serial_port_icon_blue.ico")
        self.grid_columnconfigure(0, weight=1)

        error_icon = Image.open('Resources/error_icon.png')
        self.error_image = ctk.CTkImage(light_image=error_icon, size=(47, 47))

        self.error_frame = ctk.CTkFrame(self, width=100, height=37)
        self.error_frame.grid(row=0, column=0, padx=10, pady=5)

        self.error_image_label = ctk.CTkLabel(self.error_frame, text="", image=self.error_image)
        self.error_image_label.grid(row=0, column=0, padx=5, pady=10)

        error_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")
        error_message_font = ctk.CTkFont(family="Helvetica", size=12)

        self.error_text = ctk.CTkLabel(self.error_frame, text="ERROR!", font=error_font)
        self.error_text.grid(row=0, column=1, padx=5)

        self.error_message = ctk.CTkLabel(self, text=f"The CSV file {csv_name} doesn't exist.", font=error_message_font)
        self.error_message.grid(row=1, column=0, pady=5, padx=10)

        self.button = ctk.CTkButton(self, text="Cancel", command=self.cancelNewCSV)
        self.button.grid(row=2, column=0, pady=5, padx=20)

    def cancelNewCSV(self):
        self.destroy()