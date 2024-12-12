from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
from copy import deepcopy
import manifest
import LogHandler
import calculate
import balance_operator
import json
import os

class GUI:

    def __init__(self, master):
        self.master = master
        self.master.geometry("1080x720")
        self.master.update()
        self.operation = ""
        self.currUser = None
        self.frames = [] # store all pages of gui to display
        self.save_state = {}

        try:
            if os.path.isfile("./save_state.json"):
                with open("save_state.json", "r") as save_state:
                    save_state_string = save_state.read()
                    self.save_state = json.loads(save_state_string)

            else: # first time opening program
                self.selectOperation()
                self.signIn()
        except "Error":
            print("An error has occured")



    def menuBar(self):
        self.userMenu = Menubutton(self.master, text=self.currUser, bd=0)
        self.userMenu.menu = Menu(self.userMenu, tearoff=False)
        self.userMenu["menu"] = self.userMenu.menu
        self.userMenu.menu.add_command(label="Sign In", command=self.signIn)
        self.userMenu.menu.add_command(label="Shut Down", command=self.shutDown)
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
        currUser = simpledialog.askstring(title="User Sign In", prompt="Please enter your name to sign in")

        while((currUser is None and self.currUser is None) or (currUser is not None and (currUser.strip() == ""))):
            if(currUser is None and self.currUser is None):
                messagebox.showerror("Error", "Please enter your name to sign in")
            else:
                messagebox.showerror("Error", f"\"{currUser}\" is an invalid name")
            currUser = simpledialog.askstring(title="User Sign In", prompt="Please enter your name to sign in")
        if currUser is not None:
            self.updateJSON({"currUser": currUser})
            self.currUser = currUser
            self.userMenu.configure(text=self.currUser)
            #TODO: [LOG] sign in
            LogHandler.logOperatorSignIn(self.currUser)


        self.placeMenuBar()

    def shutDown(self):
        #TODO: [Log] shutdown port & program for annual maintainence
        confirmShutDown = messagebox.askquestion("Shut Down", "Are you sure you want to shut down for the year?", icon="warning")
        if confirmShutDown == "yes":
            LogHandler.logEndOfYearShutdown()
            self.master.destroy()

    def addLogComment(self):
        comment = simpledialog.askstring(title="Log Comment", prompt="Please enter a log comment")
        while(comment is not None and (comment.strip() == "")):
            messagebox.showerror("Error", f"\"{comment}\" is an invalid log comment")
            comment = simpledialog.askstring(title="Log Comment", prompt="Please enter a log comment")
        if comment is not None:
            # TODO: [LOG] add comment to log file
            LogHandler.logOperatorComment(comment)

    def viewLog(self):
        #TODO: retrieve log file
        # NOTE: might need to change directory to read log from desktop
        logConents = LogHandler.getLogContents()

        self.logWindow = Toplevel()
        self.logWindow.grab_set() # ensure that other windows cannot be modified while this one is open
        self.logWindow.geometry("1500x900")
        self.logWindow.title("View Log")
        self.log_listbox = Listbox(self.logWindow,
                          activestyle="none")
        self.log_text = Label(self.logWindow,
                                           text=LogHandler.generateFileName(),
                                           font=("Arial", 20, "bold"))
        self.log_scrollbar = Scrollbar(self.log_listbox,
                                       command=self.log_listbox.yview)
        self.log_listbox.config(yscrollcommand = self.log_scrollbar.set)

        for line in logConents.splitlines():
            self.log_listbox.insert(END, line)
        self.log_listbox.see(END)

        self.log_text.place(relx=0.5, rely=0.03, anchor="center")
        self.log_scrollbar.pack(side = RIGHT, fill = BOTH)
        self.log_listbox.place(relx=0.5, rely=0.5, relheight=0.9, relwidth=0.9, anchor="center")
        self.logWindow.mainloop()


    def selectOperation(self):
        self.updateJSON({"currScreen": "selectOperation"})

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
                                          activebackground="#DBDBDB")

        self.balance_button = Button(self.button_border2,
                                     command=self.select_balance,
                                     text="Balance Containers",
                                     font=("Arial", 16, "bold"),
                                     relief="flat",
                                     borderwidth=0,
                                     activebackground="#DBDBDB")

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
            self.updateJSON({"manifest_file": self.manifest_file.name})

            array, containerID = self.manifest.copyManifest()
            self.calc = calculate.Calculate(array, containerID)
            # redisplay manifest_upload with button for next screen
            self.manifest_upload.place_forget()
            self.userMenu.place_forget()
            self.logMenu.place_forget()
            if self.operation == "load": # button to move to container select screen
                self.calculate_button_border.place(relx=0.975, rely=0.975, relheight=0.1, relwidth=0.15, anchor="se")
                self.container_select_button.place(relheight=1, relwidth=1)
                self.manifest_upload.place(relwidth=1, relheight=1)
                self.menuBar()



            else: # button to calculate solution for balance operation
                self.calculate_button_border.place(relx=0.975, rely=0.975, relheight=0.1, relwidth=0.15, anchor="se")
                self.calculate_button.place(relheight=1, relwidth=1)
                self.manifest_upload.place(relwidth=1, relheight=1)
                self.menuBar()
            # display selected file with full path
            self.manifest_file_text = Label(self.manifest_upload,
                                            font=[("Arial", 16)])
            self.manifest_file_text.configure(text=self.manifest_file.name[self.manifest_file.name.rfind('/')+1:],
                                              font=("Arial", 16, "bold"))
            self.manifest_file_text.place(relx=0.5, rely=0.8, anchor="center",
                                          relwidth = 1,
                                          relheight=0.1)
    def calculateSolution(self):
        self.updateJSON({"currScreen": "calculateSolution", "currInstruction": 0})
        self.instructionList = []
        self.currInstruction = 0
        if self.manifest is None:
            # TODO: error popup
            messagebox.showerror("Error", f"No manifest file found")
        else:
            if self.operation == "load":
                #TODO: load/offload select screen
                self.container_select.place_forget()
            else: # balance solution
                # calculate solution without additional input
                balancer = balance_operator.BalanceOperator(self.calc, self.manifest)
                self.instructionList = balancer.perform_balance_operation(self.calc.ship_bay_array)
                self.save_state.update({"currScreen": "displayInstructions", "instructionList": [instruction.__dict__ for instruction in self.instructionList]})
                #for instruction in self.InstructionList:
                #    instruction.print()
                self.manifest_upload.place_forget()
            
            
            preGridList = []
            postGridList = []

            for i in range(len(self.instructionList)):
                preGridList.append(deepcopy(self.calc.ship_bay_array))
                self.calc.performInstruction(self.instructionList[i])
                postGridList.append(deepcopy(self.calc.ship_bay_array))
                self.frames.append(self.renderInstructionFrame(preGridList[i], postGridList[i], self.instructionList[i]))
            self.getNextInstruction()
            self.menuBar()
            #TESTING renderInstructionFrame below
            # postManifest_file = "SampleManifests/customManifest.txt"
            # postManifest = manifest.Manifest(postManifest_file)
            # post = postManifest.copyManifest()[0]
            # self.renderInstructionFrame(self.calc.ship_bay_array, post, None)

    def renderInstructionFrame(self, preGrid, postGrid, currInstruction):
        instruction_frame = Frame(self.master)

        pre_manifest_display = Frame(instruction_frame)
        post_manifest_display = Frame(instruction_frame)
        instruction_label = Label(instruction_frame,
                                    text="Instructions",
                                    font=("Arial", 30, "bold"))
        # TODO: dynamically update based on current move number (default/move=0 -> "Overview", move>0 -> "Move move/moveTotal")
        instruction_step = Label(instruction_frame,
                                    text="Overview",
                                    font=("Arial", 15, "bold"))
        instruction_top_divider = Canvas(instruction_frame, background="black")
        instruction_description = Label(instruction_frame,
                                    text=f"There are 21 moves to complete.\nThis will take an estimated 52 minutes to complete.\n{len(self.frames)}",
                                    font=("Arial", 15))
        instruction_step_divider = Canvas(instruction_frame, background="black")
        instruction_vertical_divider = Canvas(instruction_frame, background="black")
        instruction_bottom_divider = Canvas(instruction_frame, background="black")
        instruction_move_eta = Label(instruction_frame,
                                    text="ETA: 0 minutes",
                                    font=("Arial", 20, "bold"))

        instruction_next_button_border = Frame(instruction_frame,
                                             highlightbackground="black",
                                             background="black",
                                             bd=3)
        instruction_next_button = Button(instruction_next_button_border,
                                       background="#00ff14",
                                       text="Next >",
                                       font=("Arial", 15, "bold"),
                                       wraplength=150,
                                       relief="flat",
                                       activebackground="#00CD14",
                                       borderwidth=0,
                                       command=self.getNextInstruction)

        # Don't need offload_list for rendering instructions
        # for r in range(8):
        #     for c in range(12):
        #         if self.preGrid[r][c].description != "NAN" and self.preGrid[r][c].description != "UNUSED":
        #             self.offload_list[f"{self.preGrid[r][c].description}"] = 0

        # buttons for selecting containers for offload
        #self.container_buttons = [[None for r in range(12)] for c in range(8)]
        self.configureGridDisplay(pre_manifest_display, preGrid)

        # disable clicking and hover functionality for container_buttons
        # TODO: check if this errors out if starting from balance containers
        for r in range(8):
            for c in range(12):
                # configure container selection toggle and hover for complete container info
                if self.container_buttons[r][c].cget("text") != "NAN" and self.container_buttons[r][c].cget("text") != "UNUSED":
                    self.container_buttons[r][c].configure(activebackground="#BCBCBC")
                    self.container_buttons[r][c].unbind("<Enter>")
                    self.container_buttons[r][c].unbind("<Leave>")

        # NOTE: to highlight a specific container
        #   self.container_buttons[r][c].configure(background=color, activebackground=color)

        for r in range(7, -1, -1):
            for c in range(12):
                self.container_buttons[r][c].place(relwidth=1, relheight=1)
                self.container_button_frames[r][c].place(relx=c*(1/12), rely=(7-r)*(1/8), relwidth=(1/12), relheight=(1/8))
        pre_manifest_display.place(relx=0.075, rely=0.58, relwidth=0.40, relheight=0.40, anchor="w")
        
        self.configureGridDisplay(post_manifest_display, postGrid)
        for r in range(7, -1, -1):
            for c in range(12):
                self.container_buttons[r][c].place(relwidth=1, relheight=1)
                self.container_button_frames[r][c].place(relx=c*(1/12), rely=(7-r)*(1/8), relwidth=(1/12), relheight=(1/8))
        post_manifest_display.place(relx=0.925, rely=0.58, relwidth=0.40, relheight=0.40, anchor="e")
        
        instruction_label.place(relx=0.5, rely=0.075, anchor="center")
        instruction_step.place(relx=0.5, rely=0.12, anchor="center")
        instruction_top_divider.place(relx=0.5, rely=0.15, relwidth=1.1, relheight=0.008, anchor="center")
        instruction_description.place(relx=0.5, rely=0.25, anchor="center")
        instruction_step_divider.place(relx=0.5, rely=0.35, relwidth=1.1, relheight=0.008, anchor="center")
        instruction_vertical_divider.place(relx=0.5, rely=0.58, relwidth=0.0052, relheight=0.455, anchor="center")
        instruction_bottom_divider.place(relx=0.5, rely=0.81, relwidth=1.1, relheight=0.008, anchor="center")
        instruction_move_eta.place(relx=0.5, rely=0.90, anchor="center")

        instruction_next_button_border.place(relx=0.885, rely=0.90, relheight=0.06, relwidth=0.08, anchor="center")
        instruction_next_button.place(relheight=1, relwidth=1)
        #instruction_frame.place(relwidth=1, relheight=1)
        return instruction_frame
        #self.menuBar()

    def getNextInstruction(self):
        if(self.currInstruction == len(self.frames)):
            messagebox.showinfo("Info", "Operation complete. Please send the outbound manifest to the ship captain")
            self.frames[self.currInstruction-1].place_forget()
            self.frames = []
            self.initializeJSON()
            self.selectOperation()
        else:
            if(self.currInstruction != 0):
                self.frames[self.currInstruction-1].place_forget()
            instruction_frame = self.frames[self.currInstruction]
            instruction_frame.place(relwidth=1, relheight=1)
            #self.menuBar()
            self.currInstruction += 1
            self.updateJSON({"currInstruction": self.currInstruction})

    def containerSelect(self):
        self.updateJSON({"currScreen": "containerSelect"})
        self.manifest_upload.place_forget()
        self.load_list = {}
        self.offload_list = {}
        self.offload_positions = [] # only use for recovering from save state


        self.container_select = Frame(self.master)

        self.manifest_display = Frame(self.container_select)
        self.manifest_label = Label(self.container_select,
                                    text="Select Containers to Load/Offload",
                                    font=("Arial", 30, "bold"))
        self.grid = self.manifest.copyManifest()[0]

        for r in range(8):
            for c in range(12):
                if self.grid[r][c].description != "NAN" and self.grid[r][c].description != "UNUSED":
                    self.offload_list[f"{self.grid[r][c].description}"] = 0
        self.updateJSON({"offload_list": self.offload_list})

        # buttons for selecting containers for offload
        self.configureGridDisplay(self.manifest_display, self.grid)


        for r in range(8):
            for c in range(12):
                # configure container selection toggle and hover for complete container info
                if self.container_buttons[r][c].cget("text") != "NAN" and self.container_buttons[r][c].cget("text") != "UNUSED":
                    self.container_buttons[r][c].configure(activebackground="red", command=lambda x=c, y=r: self.toggle_container(x, y))
                    self.container_buttons[r][c].bind("<Enter>", lambda event, x=r, y=c: self.displayContainerInfo(x, y))
                    self.container_buttons[r][c].bind("<Leave>", lambda event: self.removeContainerInfo())

        for r in range(7, -1, -1):
            for c in range(12):
                self.container_buttons[r][c].place(relwidth=1, relheight=1)
                self.container_button_frames[r][c].place(relx=c*(1/12), rely=(7-r)*(1/8), relwidth=(1/12), relheight=(1/8))

        self.manifest_display.place(relx=0.975, rely=0.5, relwidth=0.75, relheight=0.75, anchor="e")
        self.manifest_label.place(relx=0.5, rely=0.075, anchor="center")
        self.renderLoadOffloadButtons()
        self.container_select.place(relwidth=1, relheight=1)
        self.menuBar()

    # create frames/buttons to display manifest grid
    def configureGridDisplay(self, parentFrame, grid):
        self.container_buttons = [[None for r in range(12)] for c in range(8)]
        self.container_button_frames = [[Frame(parentFrame, highlightbackground="black", background="black", bd=2) for r in range(12)] for c in range(8)]
        # configure buttons to match current state of grid
        for r in range(8):
            for c in range(12):
                temp = Button(self.container_button_frames[r][c], border=0, relief="flat", font=("Arial", 8, "bold"))
                temp.configure(text=grid[r][c].description[0:14])  # only display first 15 characters of container descriptions
                # configure NAN locations
                if grid[r][c].description == "NAN":
                    temp.configure(background="#3A3A3A",
                                   foreground="white",
                                   activebackground="#3A3A3A",
                                   activeforeground="white")
                # configure actual containers
                elif grid[r][c].description != "UNUSED":
                    temp.configure(background="#BCBCBC", activebackground="#BCBCBC")
                self.container_buttons[r][c] = temp

    def toggle_container(self, x, y):
        description = self.grid[y][x].description
        curr_offload = self.offload_list.get(description)
        if self.container_buttons[y][x].cget("bg") == "#BCBCBC":
            self.container_buttons[y][x].configure(background="red", activebackground="#BCBCBC")
            self.offload_list.update({description: curr_offload + 1}) # increase selected offload by 1
            self.offload_positions.append((y, x))
        else:
            self.container_buttons[y][x].configure(background="#BCBCBC", activebackground="red")
            self.offload_list.update({description: curr_offload - 1}) # decrease selected offload by 1
            self.offload_positions.remove((y, x))
        self.updateJSON({"offload_list": self.offload_list, "offload_positions": self.offload_positions})
        self.updatePendingOffloads()


    def displayContainerInfo(self, x, y):
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
    
    def removeContainerInfo(self):
        self.container_info_border.place_forget()

    def renderLoadOffloadButtons(self):
        # helper function to define and place the buttons that will be used during load/offload operations
        self.load_container_button_border = Frame(self.container_select,
                                                   highlightbackground="black",
                                                   background="black",
                                                   bd=4)
        self.load_container_button = Button(self.load_container_button_border,
                                             background="#00ff14",
                                             text = "+\nLoad",
                                             command=self.loadContainerPrompt,
                                             font=("Arial", 16, "bold"),
                                             relief="flat",
                                             borderwidth=0,
                                             activebackground="#00CD14")

        self.pending_loads_button_border = Frame(self.container_select,
                                                   highlightbackground="black",
                                                   background="black",
                                                   bd=4)
        self.pending_loads_button = Button(self.pending_loads_button_border,
                                             text = "0 pending loads",
                                             command=self.displayPendingLoadsList,
                                             font=("Arial", 14, "bold"),
                                             relief="flat",
                                             borderwidth=0,
                                             activebackground="#DBDBDB")

        self.pending_offloads_button_border = Frame(self.container_select,
                                                   highlightbackground="black",
                                                   background="black",
                                                   bd=4)
        self.pending_offloads_button = Button(self.pending_offloads_button_border,
                                             text = "0 pending offloads",
                                             command=self.displayPendingOffloadsList,
                                             font=("Arial", 14, "bold"),
                                             relief="flat",
                                             borderwidth=0,
                                             activebackground="#DBDBDB")
        self.loadOffload_calculate_button_border = Frame(self.container_select,
                                             highlightbackground="black",
                                             background="black",
                                             bd=2)
        self.loadOffload_calculate_button = Button(self.loadOffload_calculate_button_border,
                                       background="#00ff14",
                                       text="Calculate Move Sequence",
                                       font=("Arial", 10, "bold"),
                                       wraplength=150,
                                       relief="flat",
                                       activebackground="#00CD14",
                                       borderwidth=0,
                                       command=self.calculateSolution)

        self.load_container_button_border.place(relx=0.1, rely=0.2, relheight=0.1, relwidth=0.1, anchor="nw")
        self.load_container_button.place(relheight=1, relwidth=1)
        self.pending_loads_button_border.place(relx=0.02, rely=0.32, relheight=0.05, relwidth=0.18, anchor="nw")
        self.pending_loads_button.place(relheight=1, relwidth=1)
        self.pending_offloads_button_border.place(relx=0.02, rely=0.39, relheight=0.05, relwidth=0.18, anchor="nw")
        self.pending_offloads_button.place(relheight=1, relwidth=1)
        self.loadOffload_calculate_button_border.place(relx=0.975, rely=0.975, relheight=0.1, relwidth=0.15, anchor="se")
        self.loadOffload_calculate_button.place(relheight=1, relwidth=1)

    def updatePendingLoads(self):
        pendingLoadsNum = sum(self.load_list.values())
        pendingLoadsText = "0 pending loads"

        if(pendingLoadsNum == 1):
            pendingLoadsText = f"{pendingLoadsNum} pending load"
        else:
            pendingLoadsText = f"{pendingLoadsNum} pending loads"

        self.pending_loads_button.config(text = pendingLoadsText)

    def updatePendingOffloads(self):
        pendingOffloadsNum = sum(self.offload_list.values())
        pendingOffloadsText = "0 pending offloads"

        if(pendingOffloadsNum == 1):
            pendingOffloadsText = f"{pendingOffloadsNum} pending offload"
        else:
            pendingOffloadsText = f"{pendingOffloadsNum} pending offloads"

        self.pending_offloads_button.config(text = pendingOffloadsText)

    def loadContainerPrompt(self):
        loadContainerDescription = simpledialog.askstring(title="Load Container", prompt="Please enter a description for the container")
        while(loadContainerDescription is not None and (loadContainerDescription.strip() == "" or loadContainerDescription.strip().upper() == "UNUSED" or loadContainerDescription.strip().upper() == "NAN")):
            messagebox.showerror("Error", f"\"{loadContainerDescription}\" is an invalid container description")
            loadContainerDescription = simpledialog.askstring(title="Load Container", prompt="Please enter a description for the container")
        if loadContainerDescription is not None:
            if loadContainerDescription in self.load_list:
                curr_load_dupe = self.load_list.get(loadContainerDescription)
                self.load_list.update({loadContainerDescription: curr_load_dupe + 1}) # increase selected load by 1
            else:
                self.load_list[f"{loadContainerDescription}"] = 1

            self.updateJSON({"load_list": self.load_list})
            self.updatePendingLoads()
            print(self.load_list)

    def displayPendingLoadsList(self):
        self.pendingLoadsWindow = Toplevel()
        self.pendingLoadsWindow.grab_set() # ensure that other windows cannot be modified while this one is open
        self.pendingLoadsWindow.geometry("200x300")
        self.pendingLoadsWindow.title("Pending Loads")
        self.pending_loads_listbox = Listbox(self.pendingLoadsWindow,
                          activestyle="dotbox",
                          selectmode="multiple",
                          selectbackground="red")
        for containerDescription in self.load_list:
            for dupes in range(self.load_list.get(containerDescription)):
                self.pending_loads_listbox.insert(END, containerDescription)

        self.pending_loads_delete_button_border = Frame(self.pendingLoadsWindow,
                                                   highlightbackground="black",
                                                   background="black",
                                                   bd=2)
        self.pending_loads_delete_button = Button(self.pending_loads_delete_button_border,
                                             background="red",
                                             text = "Delete",
                                             command=self.deletePendingLoads,
                                             font=("Arial", 12, "bold"),
                                             relief="flat",
                                             borderwidth=0,
                                             activebackground="#C90000")
        self.pending_loads_scrollbar = Scrollbar(self.pending_loads_listbox,
                                       command=self.pending_loads_listbox.yview)
        self.pending_loads_listbox.config(yscrollcommand = self.pending_loads_scrollbar.set)

        self.pending_loads_scrollbar.pack(side = RIGHT, fill = BOTH)
        self.pending_loads_listbox.place(relx=0.5, rely=0.05, relheight=0.8, relwidth=0.6, anchor="n")
        self.pending_loads_delete_button_border.place(relx=0.5, rely=0.95, relheight=0.095, relwidth=0.3, anchor="s")
        self.pending_loads_delete_button.place(relheight=1, relwidth=1)
        self.pendingLoadsWindow.mainloop()

    def displayPendingOffloadsList(self):
        self.pendingOffloadsWindow = Toplevel()
        self.pendingOffloadsWindow.grab_set() # ensure that other windows cannot be modified while this one is open
        self.pendingOffloadsWindow.geometry("200x300")
        self.pendingOffloadsWindow.title("Pending Offloads")
        self.pending_offloads_listbox = Listbox(self.pendingOffloadsWindow,
                          activestyle="none")
        for containerDescription in self.offload_list:
            for dupes in range(self.offload_list.get(containerDescription)):
                self.pending_offloads_listbox.insert(END, containerDescription)
        self.pending_offloads_scrollbar = Scrollbar(self.pending_offloads_listbox,
                                       command=self.pending_offloads_listbox.yview)
        self.pending_offloads_listbox.config(yscrollcommand = self.pending_offloads_scrollbar.set)

        self.pending_offloads_scrollbar.pack(side = RIGHT, fill = BOTH)
        self.pending_offloads_listbox.place(relx=0.5, rely=0.05, relheight=0.8, relwidth=0.6, anchor="n")
        self.pendingOffloadsWindow.mainloop()

    def deletePendingLoads(self):
        #print(self.pending_loads_listbox.curselection())
        for delIndex in sorted(self.pending_loads_listbox.curselection(), reverse=TRUE):
            #print(f"deleteing index {delIndex}")
            container2DeleteDescription = self.pending_loads_listbox.get(delIndex)
            #print(container2DeleteDescription)
            # remove container description from listbox
            self.pending_loads_listbox.delete(delIndex)
            # decrement the number of dupes of the container description from dict. if there are no more dupes, remove the container description entirely
            if container2DeleteDescription in self.load_list:
                curr_load_dupe = self.load_list.get(container2DeleteDescription)
                if(curr_load_dupe - 1 == 0):
                    del self.load_list[container2DeleteDescription]
                else:
                    self.load_list.update({container2DeleteDescription: curr_load_dupe - 1}) # increase selected load by 1
        self.updateJSON({"load_list": self.load_list})
        self.updatePendingLoads()

    #def displayPendingOffloadsList(self):



    def loadManifest(self):
        self.updateJSON({"operation": self.operation, "currScreen": "loadManifest"})
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
                                             activebackground="#DBDBDB")
        self.calculate_button_border = Frame(self.manifest_upload,
                                             highlightbackground="black",
                                             background="black",
                                             bd=2)
        self.calculate_button = Button(self.calculate_button_border,
                                       background="#00ff14",
                                       text="Calculate Move Sequence",
                                       font=("Arial", 10, "bold"),
                                       wraplength=150,
                                       relief="flat",
                                       activebackground="#00CD14",
                                       borderwidth=0,
                                       command=self.calculateSolution)
        self.container_select_button = Button(self.calculate_button_border,
                                              text="Select Containers",
                                              font=("Arial", 10, "bold"),
                                              wraplength=150,
                                              relief="flat",
                                              activebackground="#DBDBDB",
                                              borderwidth=0,
                                              command=self.containerSelect)

        self.manifest_upload_text.place(relx=0.5, rely=0.1, anchor="center")
        self.manifest_upload_button_border.place(relx=0.5, rely=0.5, relwidth = 0.5, relheight=0.5, anchor="center")
        self.manifest_upload_button.place(relheight=1, relwidth=1)

        self.manifest_upload.place(relwidth=1, relheight=1)


        # redraw menubar over manifest_upload screen
        self.menuBar()
        self.select_manifest_file()

    def updateJSON(self, dict):
        self.save_state.update(dict)
        with open("save_state.json", "w") as file:
            file.write(json.dumps(self.save_state, indent=4))
            file.close()

    def initializeJSON(self):
        self.save_state = {"currUser": self.currUser}
        with open("save_state.json", "w") as file:
            file.write(json.dumps(self.save_state, indent=4))
            file.close()