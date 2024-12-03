from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import manifest

class GUI:

    def __init__(self, master):
        self.master = master
        self.master.geometry("1080x720")
        self.master.update()
        self.operation = ""
        self.currUser = "User"
        self.frames = [] # store all pages of gui to display

        self.operation = "load"
        self.loadManifest()

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
            self.manifest_file_text.configure(text=self.manifest_file.name, background="red")
            self.manifest_file_text.place(relx=0.5, rely=0.8, anchor="center",
                                          relwidth = 1,
                                          relheight=0.1)
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
        grid = self.manifest.copyManifest()

        for r in range(12):
            for c in range(8):
                if grid[c][r].description != "NAN" and grid[c][r].description != "UNUSED":
                    self.offload_list[f"{grid[c][r].description}"] = 0
                    print(self.offload_list)

        self.containers = [[None for r in range(12)] for c in range(8)]


        for r in range(8):
            for c in range(12):
                temp = Button(self.manifest_display,
                              border=0,
                              relief="flat",
                              font=("Arial", 8))
                temp.configure(text=grid[r][c].description)
                if grid[r][c].description == "NAN":
                    temp.configure(background="black",
                                   foreground="white",
                                   activebackground="black",
                                   activeforeground="white")
                elif grid[r][c].description != "UNUSED":
                    temp.configure(background="red",
                                   activebackground="green",
                                   command=lambda x=c, y=r: self.toggle_container(x, y))
                self.containers[r][c] = temp

        for r in range(7, -1, -1):
            for c in range(12):
                self.containers[r][c].place(relx=c*(1/12), rely=(7-r)*(1/8), relwidth=(1/12), relheight=(1/8))

        self.manifest_display.place(relx=0.975, rely=0.5, relwidth=0.75, relheight=0.75, anchor="e")
        self.manifest_label.place(relx=0.5, rely=0.075, anchor="center")
        self.renderLoadOffloadButtons()
        self.container_select.place(relwidth=1, relheight=1)
        self.menuBar()


    def toggle_container(self, x, y):
        print(f"({x}, {y})")
        description = self.manifest.copyManifest()[y][x].description
        curr_offload = self.offload_list.get(description)
        if self.containers[y][x].cget("bg") == "red":
            self.containers[y][x].configure(background="green", activebackground="red")
            self.offload_list.update({description: curr_offload + 1}) # increase selected offload by 1

        else:
            self.containers[y][x].configure(background="red", activebackground="green")
            self.offload_list.update({description: curr_offload - 1}) # decrease selected offload by 1
        
        self.updatePendingOffloads()
        print(self.offload_list)


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
                                             #command=self.displayPendingOffloadsList,
                                             font=("Arial", 14, "bold"),
                                             relief="flat",
                                             borderwidth=0,
                                             activebackground="#DBDBDB")

        self.load_container_button_border.place(relx=0.1, rely=0.2, relheight=0.1, relwidth=0.1, anchor="nw")
        self.load_container_button.place(relheight=1, relwidth=1)
        self.pending_loads_button_border.place(relx=0.02, rely=0.32, relheight=0.05, relwidth=0.18, anchor="nw")
        self.pending_loads_button.place(relheight=1, relwidth=1)
        self.pending_offloads_button_border.place(relx=0.02, rely=0.39, relheight=0.05, relwidth=0.18, anchor="nw")
        self.pending_offloads_button.place(relheight=1, relwidth=1)

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
        while(loadContainerDescription is not None and (loadContainerDescription.strip() == "" or loadContainerDescription.strip() == "UNUSED" or loadContainerDescription.strip() == "NAN")):
            messagebox.showerror("Error", f"\"{loadContainerDescription}\" is an invalid container description")
            loadContainerDescription = simpledialog.askstring(title="Load Container", prompt="Please enter a description for the container")
        if loadContainerDescription is not None:
            if loadContainerDescription in self.load_list:
                curr_load_dupe = self.load_list.get(loadContainerDescription)
                self.load_list.update({loadContainerDescription: curr_load_dupe + 1}) # increase selected load by 1
            else:
                self.load_list[f"{loadContainerDescription}"] = 1
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

        self.pending_loads_listbox.place(relx=0.5, rely=0.05, relheight=0.8, relwidth=0.6, anchor="n")
        self.pending_loads_delete_button_border.place(relx=0.5, rely=0.95, relheight=0.095, relwidth=0.3, anchor="s")
        self.pending_loads_delete_button.place(relheight=1, relwidth=1)
        self.pendingLoadsWindow.mainloop()

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
        self.updatePendingLoads()

    #def displayPendingOffloadsList(self):



    def loadManifest(self):
        # deload operation selection screen
        #self.operation_select.place_forget()
        #self.userMenu.place_forget()
        #self.logMenu.place_forget()

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










if __name__ == "__main__":

    #import gui
    import tkinter as tk

    window = tk.Tk()
    window.title("CargoCo Ship Optimizer")
    GUI(window)
    window.mainloop()