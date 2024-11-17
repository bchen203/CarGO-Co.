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

        self.operation_select = Frame(self.master, height=720, width=1080)

        # prompt user for operation select
        self.operation_select_text = Label(self.operation_select,
                                           text="Please select type of operation to perform",
                                           font=("Arial", 30, "bold"))

        # buttons to select type of operation
        # will automatically prompt user for file upload
        # create frames that serve as borders for buttons
        self.button_border1 = Frame(self.operation_select,
                                   highlightbackground="black",
                                   background="black",
                                   bd=4)
        self.button_border2 = Frame(self.operation_select,
                                           highlightbackground="black",
                                           background="black",
                                           bd=4)

        self.load_offload_button = Button(self.button_border1,
                                          command=self.select_load_offload,
                                          text="Load/Offload Containers",
                                          font=("Arial", 16, "bold"),
                                          relief="flat",
                                          overrelief="flat",
                                          borderwidth=0,
                                          activebackground="#00ff14")

        self.balance_button = Button(self.button_border2,
                                     command=self.select_balance,
                                     text="Balance Containers",
                                     font=("Arial", 16, "bold"),
                                     relief="flat",
                                     borderwidth=0,
                                     activebackground="#00ff14")

        # center buttons/text based on size of window
        self.operation_select_text.place(relx=0.5, rely=0.1, anchor="center")
        self.button_border1.place(relx=0.05, rely=0.2, relheight=0.6, relwidth=0.4)
        self.load_offload_button.place(relheight=1, relwidth=1)

        self.button_border2.place(relx=0.55, rely=0.2, relheight=0.6, relwidth=0.4)
        self.balance_button.place(relheight=1, relwidth=1)

        self.operation_select.place(relheight=1, relwidth=1)


    def select_load_offload(self):
        self.operation = "load"
        self.loadManifest()

    def select_balance(self):
        self.operation = "balance"
        self.loadManifest()

    def select_manifest_file(self):
        # limit file select to only txt files
        manifest_file = filedialog.askopenfile(mode="r", filetypes=[("Text Files", "*.txt")])
        return manifest_file


    def loadManifest(self):
        self.operation_select.place_forget()
        self.manifest_upload = Frame(self.master)
        self.manifest_upload_text = Label(self.manifest_upload,
                                          text = "Please select manifest file",
                                          font=("Arial", 16, "bold"))
        self.manifest_upload_button = Button(self.manifest_upload,
                                             text = "Load Manifest File",
                                             command=self.select_manifest_file,
                                             width=30,
                                             height=20,
                                             font=("Arial", 16, "bold"),
                                             relief="flat",
                                             borderwidth=0,
                                             background="blue")

        self.manifest_upload_text.pack()
        self.manifest_upload_button.pack()
        self.manifest_upload.pack()
        manifest_file = self.select_manifest_file()
        if manifest_file is not None:
            self.manifest = manifest.Manifest(manifest_file.name)






