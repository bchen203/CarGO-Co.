from tkinter import *
from tkinter import filedialog
import manifest

class GUI:

    def __init__(self, master):
        self.master = master
        self.master.geometry("1080x720")
        self.operation = ""
        self.frames = [] # store all pages of gui to display

        self.selectOperation()


    def selectOperation(self):

        self.operation_select = Frame(self.master)

        # prompt user for operation select
        self.operation_select_text = Label(self.operation_select,
                                           text="Please select type of operation to perform",
                                           font=("Arial", 30, "bold"))

        # buttons to select type of operation
        # will automatically prompt user for file upload
        self.load_offload_button = Button(self.operation_select,
                                          command=self.select_load_offload,
                                          text="Load/Offload Containers",
                                          height=2,
                                          width=30)

        self.balance_button = Button(self.operation_select,
                                     command=self.select_balance,
                                     text="Balance Containers",
                                     height=2,
                                     width=30)

        self.operation_select_text.pack()
        self.load_offload_button.pack()
        self.balance_button.pack()
        self.operation_select.pack()

    def select_load_offload(self):
        self.operation = "load"
        self.loadManifest()

    def select_balance(self):
        self.operation = "balance"
        self.loadManifest()

    def select_manifest_file(self):

        pass


    def loadManifest(self):
        self.operation_select.pack_forget()
        self.manifest_upload = Frame(window)
        self.manifest_upload_text = Label(self.manifest_upload, text = "Please select manifest file")
        self.manifest_upload_button = Button(self.manifest_upload,
                                             text = "Load Manifest File",
                                             width=30,
                                             height=2)

        self.manifest_upload_text.pack()
        self.manifest_upload_button.pack()
        self.manifest_upload.pack()
        manifest_file = filedialog.askopenfile(mode="r",filetypes=[("Text Files", "*.txt")])
        print(manifest_file)
        if manifest_file is not None:
            self.manifest = manifest.Manifest(manifest_file.name)
        self.manifest.displayManifest()







window = Tk()
GUI(window)
window.mainloop()