from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
import manifest

class GUI:

    def __init__(self, master):
        self.master = master
        self.master.geometry("1080x720")
        self.master.update()
        self.operation = ""
        self.frames = [] # store all pages of gui to display

        self.selectOperation()
        self.menuBar()

    def menuBar(self):
        self.userMenu = Menubutton(self.master, text="User")
        self.userMenu.menu = Menu(self.userMenu, tearoff=False)
        self.userMenu["menu"] = self.userMenu.menu
        self.userMenu.menu.add_command(label="Sign In", command=self.signIn)
        self.logMenu = Menubutton(self.master, text = "Event Log")
        self.logMenu.menu = Menu(self.logMenu, tearoff=False)
        self.logMenu["menu"] = self.logMenu.menu
        self.logMenu.menu.add_command(label="Add Comment to Log", command=self.addLogComment)
        self.logMenu.menu.add_command(label="View Log", command=self.viewLog)

        # self.userMenu.place(x=self.master.winfo_width() - self.userMenu.winfo_reqwidth(), y=0)
        # self.logMenu.place(x=0, y=0)
        self.master.bind("<Configure>", lambda event: self.placeMenuBar())

    def placeMenuBar(self):
        self.userMenu.place(x=self.master.winfo_width() - self.userMenu.winfo_reqwidth(), y=0)
        self.logMenu.place(x=0, y=0)

    def signIn(self):
        #TODO: [LOG] implicit sign out
        #prevUser = self.currUser
        self.currUser = simpledialog.askstring(title="User Sign In", prompt="Please enter your name")
        self.userMenu.configure(text=self.currUser)
        #TODO: [LOG] sign in

        self.placeMenuBar()

    def addLogComment(self):
        comment = simpledialog.askstring(title="Log Comment", prompt="Please enter log comment")
        # TODO: [LOG] add comment to log file

    def viewLog(self):
        #TODO: retrieve log file
        pass


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
                                          font=("Arial", 30, "bold"))
        self.manifest_upload_button = Button(self.manifest_upload,
                                             text = "Load Manifest File",
                                             command=self.select_manifest_file,
                                             width=30,
                                             height=20,
                                             font=("Arial", 16, "bold"),
                                             relief="flat",
                                             borderwidth=0,
                                             background="blue")

        # Bug: place causes menubar to disappear, likely still in lower layer
        # menu bar displays correctly if use .pack() rather than .place()
        # self.manifest_upload_text.place(relx=0.5, rely=0.1, anchor="center")
        # self.manifest_upload_button.place(relx=0.5, rely=0.5, anchor="center")
        # self.manifest_upload.place(relwidth=1, relheight=1)
        self.manifest_upload_text.pack()
        self.manifest_upload_button.pack()
        self.manifest_upload.pack()
        # self.placeMenuBar()
        manifest_file = self.select_manifest_file()
        if manifest_file is not None:
            self.manifest = manifest.Manifest(manifest_file.name)
