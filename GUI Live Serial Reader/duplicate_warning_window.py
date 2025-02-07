import customtkinter as ctk
from PIL import Image
from configuration import configuration, configurations


class duplicateWarningWindow(ctk.CTk):
    def __init__(self, newConfigName):
        super().__init__()
        self.title("Live Serial Reader - Duplicate Configuration Names")
        self.geometry("700x450")
        self.resizable(True, True)

        error_icon = Image.open("C:\Users\mdspenc1\Desktop\GUI Live Serial Reader\Resources\error_icon.ico")
        self.image = ctk.CTkImage(light_image=error_icon, size=(32, 32))

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, padx=20, pady=30)

        self.label_image = ctk.CTkLabel(self.frame, image=self.image)
        self.label_image.grid(row=0, column=0, padx=10)

        self.label_message = ctk.CTkLabel(self.frame, text=f"ERROR! The name {newConfigName} is already used by another configuration. \nDelete the pre-existing configuration or rename the new one.")
        self.label_message.grid(row=0, column=1, padx=10)

        #self.button1 = ctk.CTkButton(text="Delete Existing Configuration", command=lambda: self.deleteConfiguration(duplicateConfig.configuration_name))
        #self.button1.grid(row=1, pady=10, padx=20)

        #self.button2 = ctk.CTkButton(text="Rename New Configuration", command=lambda: self.renameConfiguration(newConfig))
        #self.button2.grid(row=2, pady=10, padx=20)

        self.button3 = ctk.CTkButton(text="Cancel", command=self.cancelNewConfig)
        self.button3.grid(row=1, pady=10, padx=20)

    def cancelNewConfig(self):
        open_menu_window()
        self.destroy

def open_menu_window():
    from menu_window import menuWindow
    menu_win = menuWindow()
    menu_win.mainloop()