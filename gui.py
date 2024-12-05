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
        self.currUser = "User"
        self.frames = [] # store all pages of gui to display

        self.selectOperation()

    def menuBar(self):
        self.userMenu = Menubutton(self.master, text=self.currUser, bd=0)
        self.userMenu.menu = Menu(self.userMenu, tearoff=False)
        self.userMenu["menu"] = self.userMenu.menu
        self.userMenu.menu.add_command(label="Sign In", command=self.signIn)
        self.userMenu.menu.add_command(label="Sign Out", command=self.signOut)
        self.logMenu = Menubutton(self.master, text = "Event Log", bd=0)
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

    def signOut(self):
        #TODO: [Log] shutdown port & program for annual maintainence
        self.master.destroy()

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
        # draw menubar over operation selection screen
        self.menuBar()


    def select_load_offload(self):
        self.operation = "load"
        self.loadManifest()

    def select_balance(self):
        self.operation = "balance"
        self.loadManifest()

    def select_manifest_file(self):
        # limit file select to only txt files
        self.manifest_file = filedialog.askopenfile(mode="r", filetypes=[("Text Files", "*.txt")])

        if self.manifest_file is not None:
            self.manifest = manifest.Manifest(self.manifest_file.name)
            # redisplay manifest_upload with button for next screen
            self.manifest_upload.place_forget()
            self.userMenu.place_forget()
            self.logMenu.place_forget()
            if self.operation == "load":  # button to move to container select screen
                self.calculate_button_border.place(relx=0.975, rely=0.975, relheight=0.1, relwidth=0.15, anchor="se")
                self.container_select_button.place(relheight=1, relwidth=1)
                self.manifest_upload.place(relwidth=1, relheight=1)

            else:  # button to calculate solution for balance operation
                self.calculate_button_border.place(relx=0.975, rely=0.975, relheight=0.1, relwidth=0.15, anchor="se")
                self.calculate_button.place(relheight=1, relwidth=1)
                self.manifest_upload.place(relwidth=1, relheight=1)


            # display selected file with full path
            self.manifest_file_text = Label(self.manifest_upload,
                                            font=[("Arial", 16)])
            self.manifest_file_text.configure(text=self.manifest_file.name, background="red")
            self.manifest_file_text.place(relx=0.5, rely=0.8, anchor="center", relwidth = 1, relheight=0.1)
            self.menuBar()

    def calculateSolution(self):
        if self.manifest is None:
            # TODO: error popup
            pass
        else:
            self.manifest_upload.place_forget()
            if self.operation == "load":
                #TODO: load/offload select screen
                pass
            else: # balance solution
                # calculate solution without additional input
                pass

    def containerSelect(self):
        self.manifest_upload.place_forget()
        self.load_list = {}
        self.offload_list = {}


        self.container_select = Frame(self.master)

        self.manifest_display = Frame(self.container_select)
        self.manifest_label = Label(self.container_select,
                                    text="Select Containers to Load/Offload",
                                    font=("Arial", 30, "bold"))
        self.grid = self.manifest.copyManifest()

        for r in range(8):
            for c in range(12):
                if self.grid[r][c].description != "NAN" and self.grid[r][c].description != "UNUSED":
                    self.offload_list[f"{self.grid[r][c].description}"] = 0

        # buttons for selecting containers for offload
        self.container_buttons = [[None for r in range(12)] for c in range(8)]
        self.configureGridDisplay(self.manifest_display, self.grid)


        for r in range(8):
            for c in range(12):
                # configure container selection toggle and hover for complete container info
                if self.container_buttons[r][c].cget("text") != "NAN" and self.container_buttons[r][c].cget("text") != "UNUSED":
                    self.container_buttons[r][c].configure(activebackground="#00ff14", command=lambda x=c, y=r: self.toggle_container(x, y))
                    self.container_buttons[r][c].bind("<Enter>", lambda event, x=r, y=c: self.displayContainerInfo(event, x, y))
                    self.container_buttons[r][c].bind("<Leave>", lambda event, x=r, y=c: self.removeContainerInfo(event, x, y))

        for r in range(7, -1, -1):
            for c in range(12):
                self.container_buttons[r][c].place(relwidth=1, relheight=1)
                self.container_button_frames[r][c].place(relx=c*(1/12), rely=(7-r)*(1/8), relwidth=(1/12), relheight=(1/8))

        self.manifest_display.place(relx=0.975, rely=0.5, relwidth=0.75, relheight=0.75, anchor="e")
        self.manifest_label.place(relx=0.5, rely=0.075, anchor="center")
        self.container_select.place(relwidth=1, relheight=1)
        self.menuBar()

    # create frames/buttons to display manifest grid
    def configureGridDisplay(self, parentFrame, grid):
        self.container_button_frames = [[Frame(parentFrame, highlightbackground="black", background="black", bd=2) for r in range(12)] for c in range(8)]
        # configure buttons to match current state of grid
        for r in range(8):
            for c in range(12):
                temp = Button(self.container_button_frames[r][c], border=0, relief="flat", font=("Arial", 10, "bold"))
                temp.configure(text=grid[r][c].description[0:14])  # only display first 15 characters of container descriptions
                # configure NAN locations
                if grid[r][c].description == "NAN":
                    temp.configure(background="#3A3A3A",
                                   foreground="white",
                                   activebackground="#3A3A3A",
                                   activeforeground="white")
                # configure actual containers
                elif grid[r][c].description != "UNUSED":
                    temp.configure(background="red", activebackground="red")
                self.container_buttons[r][c] = temp

    def toggle_container(self, x, y):
        description = self.grid[y][x].description
        curr_offload = self.offload_list.get(description)
        if self.container_buttons[y][x].cget("bg") == "red":
            self.container_buttons[y][x].configure(background="#00ff14", activebackground="red")
            self.offload_list.update({description: curr_offload + 1}) # increase selected offload by 1

        else:
            self.container_buttons[y][x].configure(background="red", activebackground="#00ff14")
            self.offload_list.update({description: curr_offload - 1}) # decrease selected offload by 1


    def displayContainerInfo(self, event, x, y):
        self.container_info_border = Frame(self.container_select, bd=4, background="black")
        self.container_info = Frame(self.container_info_border)
        self.container_info_title = Label(self.container_info, text="Container Information", font=("Arial", 14, "bold"))
        self.container_info_description = Label(self.container_info,
                                                text=self.grid[x][y].description,
                                                font=("Arial", 12, "bold"),
                                                wraplength=200)
        self.container_info_weight = Label(self.container_info,
                                           text=f"{self.grid[x][y].weight} kg",
                                           font=("Arial", 12, "bold"),
                                           justify="left")
        # self.container_info_description.configure(text= Weight: {self.grid[x][y].weight} kg", justify="left", wraplength=60)

        self.container_info_title.pack()
        self.container_info_description.pack()
        self.container_info_weight.pack()
        self.container_info.place(relwidth=1, relheight=1)
        self.container_info_border.place(relx=0.02, rely=0.65, relwidth=0.2, relheight=0.2)
    def removeContainerInfo(self, event, x, y):
        self.container_info_border.place_forget()




    def loadManifest(self):
        # deload operation selection screen
        self.operation_select.place_forget()
        self.userMenu.place_forget()
        self.logMenu.place_forget()

        # configure manifest upload screen
        self.manifest_upload = Frame(self.master)
        self.manifest_upload_text = Label(self.manifest_upload,
                                          text = "Please select manifest file",
                                          font=("Arial", 30, "bold"))

        self.manifest_upload_button_border = Frame(self.manifest_upload,
                                                   highlightbackground="black",
                                                   background="black",
                                                   bd=4)
        self.manifest_upload_button = Button(self.manifest_upload_button_border,
                                             text = "Load Manifest File",
                                             command=self.select_manifest_file,
                                             # width=30,
                                             # height=20,
                                             font=("Arial", 16, "bold"),
                                             relief="flat",
                                             borderwidth=0,
                                             activebackground="#00ff14")
        self.calculate_button_border = Frame(self.manifest_upload,
                                             highlightbackground="black",
                                             background="black",
                                             bd=2)
        self.calculate_button = Button(self.calculate_button_border,
                                       text="Calculate Move Sequence",
                                       font=("Arial", 10, "bold"),
                                       wraplength=150,
                                       relief="flat",
                                       activebackground="#00ff14",
                                       borderwidth=0,
                                       command=self.calculateSolution)
        self.container_select_button = Button(self.calculate_button_border,
                                              text="Select Containers",
                                              font=("Arial", 10, "bold"),
                                              wraplength=150,
                                              relief="flat",
                                              activebackground="#00ff14",
                                              borderwidth=0,
                                              command=self.containerSelect)

        self.manifest_upload_text.place(relx=0.5, rely=0.1, anchor="center")
        self.manifest_upload_button_border.place(relx=0.5, rely=0.5, relwidth = 0.5, relheight=0.5, anchor="center")
        self.manifest_upload_button.place(relheight=1, relwidth=1)

        self.manifest_upload.place(relwidth=1, relheight=1)


        # redraw menubar over manifest_upload screen
        self.menuBar()
        self.select_manifest_file()
