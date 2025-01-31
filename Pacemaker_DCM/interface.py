import tkinter
from tkinter import *
from parameters import Parameter
from tkinter import ttk
import tkinter.messagebox
import user_processing
import serial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.animation import FuncAnimation
import egram
from collections import deque

import UART
#ser = serial.Serial("COM6",115200,timeout=1)


class PacemakerGUI:

    #Constructor
    def __init__(self):
        #Setting up the root and size and background of canvas
        self.root = Tk()
        self.screen = "HOME"
        self.root.geometry("800x750")
        self.root.title("Pacemaker DCM")
        self.root.config(background="Light Blue")
        mainframe = ttk.Frame(self.root, padding="100 100")
        self.parameterdict = {}
        self.submit_pressed = 0
        mainframe.pack(pady=100)
        self.unitppm = Parameter.LRL.getUnit()
        self.unitV = Parameter.AA.getUnit()
        self.unitms = Parameter.APW.getUnit()
        self.units = Parameter.REAC.getUnit()
        self.unitmin = Parameter.REC.getUnit()
        self.unitx = ""
        
        if(str(UART.get_serial_ports_info()) != ""):
            uart = str(UART.get_serial_ports_info())
            self.status = f"connected: {uart}"
        else:
            self.status = "no device connected"

        #Widgets of the welcome screen
        status_label = ttk.Label(mainframe, text=self.status, font=('Times New Roman', 14))
        welcome_label = ttk.Label(mainframe, text="Pacemaker DCM", font=('Times New Roman', 20))
        welcome_label.pack(pady = 30)
        login_button = ttk.Button(mainframe, text = "Log-In", command= lambda: self.loginScreen(mainframe))
        login_button.pack(pady=20)
        register_button = ttk.Button(mainframe, text = "Register", command= lambda: self.registerScreen(mainframe))
        register_button.pack(pady=20)
        quit_button = ttk.Button(mainframe, text="Quit", command=quit)
        quit_button.pack(pady=20)
        status_label.pack(pady=5)
        
        #To show the window
        self.root.mainloop()

    #Login Screen function
    def loginScreen(self, mainframe):

        #Clears the frame of its current contents
        self.clearFrame(mainframe)

        #Widgets for login screen
        login_label = ttk.Label(mainframe, text="Log-In", font=('Times New Roman', 20))
        login_label.grid(column=0,row=0, columnspan=2)
        username_label = ttk.Label(mainframe, text="Username: ", font=('Times New Roman', 14))
        username_label.grid(column=0,row=1, sticky='E')
        password_label = ttk.Label(mainframe, text="Password: ", font=('Times New Roman', 14))
        password_label.grid(column=0,row=2, sticky='E')
        self.username_entry = ttk.Entry(mainframe, width=30)
        self.username_entry.grid(column=1,row=1, pady=40, sticky=(S, W))
        self.password_entry = ttk.Entry(mainframe, width=30,show='*')
        self.password_entry.grid(column=1,row=2, sticky=(N, W))
        self.root.bind('<Return>',lambda event: self.login(mainframe))
        login_button = ttk.Button(mainframe, text="Login", command= lambda: self.login(mainframe))
        login_button.grid(row=3, pady=70, column=1, sticky='E')
        back_button = ttk.Button(mainframe, text="Back",command= lambda: self.welcomeScreen(mainframe))
        back_button.grid(row=3, column=0)
        #To make the frame wider with grid manangement
        space_filler = ttk.Label(mainframe, text = "                                                                                            ")
        space_filler.grid(column=0,columnspan=2, row=4)
        self.screen = "LOGIN"
    #Registration screen function
    def registerScreen(self, mainframe):
        #Clears the frame of its current contents
        self.clearFrame(mainframe)

        #Widgets for registration screen
        login_label = ttk.Label(mainframe, text="Register", font=('Times New Roman', 20))
        login_label.grid(column=0,row=0, columnspan=2)
        username_label = ttk.Label(mainframe, text="Username: ", font=('Times New Roman', 14))
        username_label.grid(column=0,row=1, sticky='E')
        password_label = ttk.Label(mainframe, text="Password: ", font=('Times New Roman', 14))
        password_label.grid(column=0,row=2, sticky='E')
        self.username_entry = ttk.Entry(mainframe, width=30)
        self.username_entry.grid(column=1,row=1, pady=40, sticky=(S, W))
        self.password_entry = ttk.Entry(mainframe, width=30,show='*')
        self.password_entry.grid(column=1,row=2, sticky=(N, W))
        login_button = ttk.Button(mainframe, text="Register", command= lambda: self.register())
        login_button.grid(row=3, pady=70, column=1, sticky='E')
        back_button = ttk.Button(mainframe, text="Back",command= lambda: self.welcomeScreen(mainframe))
        # self.root.bind('<Return>',lambda event: self.register(mainframe))
        back_button.grid(row=3, column=0)
        space_filler = ttk.Label(mainframe, text = "                                                                                            ")
        space_filler.grid(column=0,columnspan=2, row=4)

    #Welcome screen function
    def welcomeScreen(self, mainframe):
        #Clears the frame of its current contents
        self.clearFrame(mainframe)

        #Widgets for welcome screen
        status_label = ttk.Label(mainframe, text=self.status, font=('Times New Roman', 14))
        welcome_label = ttk.Label(mainframe, text="Pacemaker DCM", font=('Times New Roman', 20))
        welcome_label.pack(pady = 30)
        login_button = ttk.Button(mainframe, text = "Log-In", command= lambda: self.loginScreen(mainframe))
        login_button.pack(pady=20)
        register_button = ttk.Button(mainframe, text = "Register", command= lambda: self.registerScreen(mainframe))
        register_button.pack(pady=20)
        quit_button = ttk.Button(mainframe, text="Quit", command=quit)
        quit_button.pack(pady=20)
        status_label.pack(pady=5)

        self.screen = "HOME"
    #When the login button is pressed
    def login(self, mainframe):
        message = user_processing.LoginCheck(self.username_entry.get(),self.password_entry.get())
        # tkinter.messagebox.showinfo(title="Login", message=message)
        if(message == "Login successful"):
            self.userScreen(mainframe, self.username_entry.get())
        else:
            tkinter.messagebox.showinfo(title="Login", message=message)


    def userScreen(self, mainframe, username):
        self.clearFrame(mainframe)
        # print(username)
        username_label = ttk.Label(mainframe, text=username + "\n\n", font=('Times New Roman', 20))
        status_label = ttk.Label(mainframe, text=self.status, font=('Times New Roman', 14))
        AOO_button = ttk.Button(mainframe, text="AOO", command=lambda:self.stateScreen(mainframe,"AOO", username))
        VOO_button = ttk.Button(mainframe, text="VOO", command=lambda:self.stateScreen(mainframe,"VOO", username))
        VVI_button = ttk.Button(mainframe, text="VVI", command=lambda:self.stateScreen(mainframe,"VVI", username))
        AAI_button = ttk.Button(mainframe, text = "AAI", command=lambda:self.stateScreen(mainframe,"AAI", username))
        AOOR_button = ttk.Button(mainframe, text = "AOOR", command=lambda:self.stateScreen(mainframe,"AOOR", username))
        VOOR_button = ttk.Button(mainframe, text = "VOOR", command=lambda:self.stateScreen(mainframe,"VOOR", username))
        VVIR_button = ttk.Button(mainframe, text = "VVIR", command=lambda:self.stateScreen(mainframe,"VVIR", username))
        AAIR_button = ttk.Button(mainframe, text = "AAIR", command=lambda:self.stateScreen(mainframe,"AAIR", username))
        egram_button = ttk.Button(mainframe, text="Egram", command=lambda:self.egramScreen(mainframe))
        button_space = ttk.Label(mainframe, text="            ")
        logout_button = ttk.Button(mainframe, text="Log-out", command= lambda: self.welcomeScreen(mainframe))
        quit_button = ttk.Button(mainframe, text = "Quit", command=quit)
        username_label.grid(column=0,row=0,columnspan=3)
        button_space.grid(column=1, row=1, rowspan=3)
        AOO_button.grid(column=0,row=1, sticky=W)
        AAI_button.grid(column=2,row=1, pady=15, sticky= E)
        VOO_button.grid(column=0,row=2, sticky=W)
        VVI_button.grid(column=2,row=2, pady= 15, sticky=E)
        AOOR_button.grid(column=0, row=3, pady=15, sticky=W)
        AAIR_button.grid(column=2, row=3, sticky=E)
        VOOR_button.grid(column=0, row=4, pady = 15, sticky=W)
        VVIR_button.grid(column=2, row=4, sticky=E)
        quit_button.grid(column=2,row=6, pady=15, sticky=E)
        status_label.grid(column=0, row=7, columnspan=3)  
        egram_button.grid(column=1, row=5)
        logout_button.grid(column=0, row=6)

    def stateScreen(self, mainframe, state_name, username):
        user_processing.updatePacing(username,state_name)
        self.clearFrame(mainframe)
        state_label = ttk.Label(mainframe, text=state_name + "\n", font=('Times New Roman', 20))
        submit_button = ttk.Button(mainframe,text="Submit",command=lambda: self.SubmitPressed(username))

        #creating all the slider and labels using variables from parameter file and user 
        #LRL Slider
        LRL_label = ttk.Label(mainframe, text="Lower Rate Limit: ", font=('Times New Roman', 14))
        self.LRL_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"LRL")) + self.unitppm), font=('Times New Roman', 14))
        self.LRL_slider = ttk.Scale(mainframe, from_=50, to=175, command=lambda val: self.updateSliderValue(username, "LRL", val,"ppm"))
        self.LRL_slider.set(user_processing.getParameter(username,"LRL"))

        # URL Slider
        URL_label = ttk.Label(mainframe, text="Upper Rate Limit: ", font=('Times New Roman', 14))
        self.URL_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"URL")) + self.unitppm), font=('Times New Roman', 14))
        self.URL_slider = ttk.Scale(mainframe, from_=50, to=175, command=lambda val: self.updateSliderValue(username, "URL", val,"ppm"))
        self.URL_slider.set(user_processing.getParameter(username,"URL"))

        # AA Slider
        AA_label = ttk.Label(mainframe, text="Atrial Amplitude: ", font=('Times New Roman', 14))
        self.AA_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"AA")) + self.unitV), font=('Times New Roman', 14))
        self.AA_slider = ttk.Scale(mainframe, from_=0.5, to=5, command=lambda val: self.updateSliderValue(username, "AA", val,"V"))
        self.AA_slider.set(user_processing.getParameter(username,"AA"))

        # APW Slider
        APW_label = ttk.Label(mainframe, text="Atrial Pulse Width: ", font=('Times New Roman', 14))
        self.APW_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"APW")) + self.unitms), font=('Times New Roman', 14))
        self.APW_slider = ttk.Scale(mainframe, from_=1, to=30, command=lambda val: self.updateSliderValue(username, "APW", val,"ms"))
        self.APW_slider.set(user_processing.getParameter(username,"APW"))

        # AS Slider
        AS_label = ttk.Label(mainframe, text="Atrial Sensitivity: ", font=('Times New Roman', 14))
        self.AS_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"AS")) + self.unitV), font=('Times New Roman', 14))
        self.AS_slider = ttk.Scale(mainframe, from_=0, to=5, command=lambda val: self.updateSliderValue(username, "AS", val,"V"))
        self.AS_slider.set(user_processing.getParameter(username,"AS"))

        # ARP Slider
        ARP_label = ttk.Label(mainframe, text="Atrial Refractory Period: ", font=('Times New Roman', 14))
        self.ARP_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"ARP")) + self.unitms), font=('Times New Roman', 14))
        self.ARP_slider = ttk.Scale(mainframe, from_=150, to=500, command=lambda val: self.updateSliderValue(username, "ARP", val,"ms"))
        self.ARP_slider.set(user_processing.getParameter(username,"ARP"))

        # VA Slider
        VA_label = ttk.Label(mainframe, text="Ventricular Amplitude: ", font=('Times New Roman', 14))
        self.VA_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"VA")) + self.unitV), font=('Times New Roman', 14))
        self.VA_slider = ttk.Scale(mainframe, from_=0.5, to=5, command=lambda val: self.updateSliderValue(username, "VA", val,"V"))
        self.VA_slider.set(user_processing.getParameter(username,"VA"))

        # VPW Slider
        VPW_label = ttk.Label(mainframe, text="Ventricular Pulse Width: ", font=('Times New Roman', 14))
        self.VPW_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"VPW")) + self.unitms), font=('Times New Roman', 14))
        self.VPW_slider = ttk.Scale(mainframe, from_=1, to=30, command=lambda val: self.updateSliderValue(username, "VPW", val,"ms"))
        self.VPW_slider.set(user_processing.getParameter(username,"VPW"))
        
        # VRP Slider
        VRP_label = ttk.Label(mainframe, text="Ventricular Refractory Period: ", font=('Times New Roman', 14))
        self.VRP_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"VRP")) + self.unitms), font=('Times New Roman', 14))
        self.VRP_slider = ttk.Scale(mainframe, from_=150, to=500, command=lambda val: self.updateSliderValue(username, "VRP", val,"ms"))
        self.VRP_slider.set(user_processing.getParameter(username,"VRP"))

        # VS Slider
        VS_label = ttk.Label(mainframe, text="Ventricular Sensitivity: ", font=('Times New Roman', 14))
        self.VS_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"VS")) + self.unitV), font=('Times New Roman', 14))
        self.VS_slider = ttk.Scale(mainframe, from_=0, to=5, command=lambda val: self.updateSliderValue(username, "VS", val,"V"))
        self.VS_slider.set(user_processing.getParameter(username,"VS"))

        # HRL Slider
        # HRL_label = ttk.Label(mainframe, text="Hysterisis Rate Limit: ", font=('Times New Roman', 14))
        # self.HRL_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"HRL")) + self.unitV), font=('Times New Roman', 14))
        # self.HRL_slider = ttk.Scale(mainframe, from_=0, to=5, command=lambda val: self.updateSliderValue(username, "HRL", val,""))
        # self.HRL_slider.set(user_processing.getParameter(username,"HRL"))

        # HINT Slider
        HINT_label = ttk.Label(mainframe, text="Hysterisis Interval: ", font=('Times New Roman', 14))
        self.HINT_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"HINT")) + self.unitppm), font=('Times New Roman', 14))
        self.HINT_slider = ttk.Scale(mainframe, from_=50, to=175, command=lambda val: self.updateSliderValue(username, "HINT", val,"ppm"))
        self.HINT_slider.set(user_processing.getParameter(username,"HINT"))

        # AT Slider
        AT_label = ttk.Label(mainframe, text="Activity Threshold: ", font=('Times New Roman', 14))
        self.AT_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"AT"))), font=('Times New Roman', 14))
        self.AT_slider = ttk.Scale(mainframe, from_=5, to=35, command=lambda val: self.updateSliderValue(username, "AT", val,"x"))
        self.AT_slider.set(user_processing.getParameter(username,"AT"))

        # REAC Slider
        REAC_label = ttk.Label(mainframe, text="Reaction Time: ", font=('Times New Roman', 14))
        self.REAC_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"REAC")) + self.units), font=('Times New Roman', 14))
        self.REAC_slider = ttk.Scale(mainframe, from_=10, to=50, command=lambda val: self.updateSliderValue(username, "REAC", val,"s"))
        self.REAC_slider.set(user_processing.getParameter(username,"REAC"))

        # RES Slider
        RES_label = ttk.Label(mainframe, text="Response Factor: ", font=('Times New Roman', 14))
        self.RES_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"RES"))), font=('Times New Roman', 14))
        self.RES_slider = ttk.Scale(mainframe, from_=1, to=16, command=lambda val: self.updateSliderValue(username, "RES", val,"x"))
        self.RES_slider.set(user_processing.getParameter(username,"RES"))

        # REC Slider
        REC_label = ttk.Label(mainframe, text="Recovery Time: ", font=('Times New Roman', 14))
        self.REC_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"REC")) + self.unitmin), font=('Times New Roman', 14))
        self.REC_slider = ttk.Scale(mainframe, from_=2, to=16, command=lambda val: self.updateSliderValue(username, "REC", val,"min"))
        self.REC_slider.set(user_processing.getParameter(username,"REC"))

        # MSR Slider
        MSR_label = ttk.Label(mainframe, text="Maximum Sensor Rate: ", font=('Times New Roman', 14))
        self.MSR_val = ttk.Label(mainframe, text=(str(user_processing.getParameter(username,"MSR")) + self.unitppm), font=('Times New Roman', 14))
        self.MSR_slider = ttk.Scale(mainframe, from_=50, to=175, command=lambda val: self.updateSliderValue(username, "MSR", val,"ppm"))
        self.MSR_slider.set(user_processing.getParameter(username,"MSR"))
        quit_button = ttk.Button(mainframe, text = "Back", command=lambda: self.userScreen(mainframe, username))

        #placing all the sliders and labels
        state_label.grid(column=0, row=0, columnspan=3, pady=5)
        if (state_name == "AOO" or state_name == "AAI" or state_name == "AOOR" or state_name == "AAIR"):
            LRL_label.grid(row=1, column=0)
            self.LRL_val.grid(row=1, column=1)
            self.LRL_slider.grid(row=1, column=2)

            URL_label.grid(row=2, column=0)
            self.URL_val.grid(row=2, column=1)
            self.URL_slider.grid(row=2, column=2)

            AA_label.grid(row=3, column=0)
            self.AA_val.grid(row=3, column=1)
            self.AA_slider.grid(row=3, column=2)

            APW_label.grid(row=4, column=0)
            self.APW_val.grid(row=4, column=1)
            self.APW_slider.grid(row=4, column=2)

            ARP_label.grid(row=5, column=0)
            self.ARP_val.grid(row=5, column=1)
            self.ARP_slider.grid(row=5, column=2)

            AS_label.grid(row=6, column=0)
            self.AS_val.grid(row=6, column=1)
            self.AS_slider.grid(row=6, column=2)

            HINT_label.grid(row=7, column=0)
            self.HINT_val.grid(row=7, column=1)
            self.HINT_slider.grid(row=7, column=2)

            submit_button.grid(column=2,row=9,sticky=E)
            quit_button.grid(column=1, row=9, sticky=E, pady=10)

            
            if (state_name == "AOOR" or  state_name == "AAIR"):

                LRL_label.grid(row=1, column=0)
                self.LRL_val.grid(row=1, column=1)
                self.LRL_slider.grid(row=1, column=2)

                URL_label.grid(row=2, column=0)
                self.URL_val.grid(row=2, column=1)
                self.URL_slider.grid(row=2, column=2)

                AA_label.grid(row=3, column=0)
                self.AA_val.grid(row=3, column=1)
                self.AA_slider.grid(row=3, column=2)

                APW_label.grid(row=4, column=0)
                self.APW_val.grid(row=4, column=1)
                self.APW_slider.grid(row=4, column=2)

                ARP_label.grid(row=5, column=0)
                self.ARP_val.grid(row=5, column=1)
                self.ARP_slider.grid(row=5, column=2)

                AS_label.grid(row=6, column=0)
                self.AS_val.grid(row=6, column=1)
                self.AS_slider.grid(row=6, column=2)

                HINT_label.grid(row=7, column=0)
                self.HINT_val.grid(row=7, column=1)
                self.HINT_slider.grid(row=7, column=2)

                AT_label.grid(row=8, column=0)
                self.AT_val.grid(row=8, column=1)
                self.AT_slider.grid(row=8, column=2)

                REAC_label.grid(row=9, column=0)
                self.REAC_val.grid(row=9, column=1)
                self.REAC_slider.grid(row=9, column=2)

                RES_label.grid(row=10, column=0)
                self.RES_val.grid(row=10, column=1)
                self.RES_slider.grid(row=10, column=2)

                REC_label.grid(row=11, column=0)
                self.REC_val.grid(row=11, column=1)
                self.REC_slider.grid(row=11, column=2)

                MSR_label.grid(row=12, column=0)
                self.MSR_val.grid(row=12, column=1)
                self.MSR_slider.grid(row=12, column=2)

                submit_button.grid(column=2,row=13,sticky=E)
                quit_button.grid(column=1, row=13, sticky=E, pady=10)
        
        else:

            LRL_label.grid(row=1, column=0)
            self.LRL_val.grid(row=1, column=1)
            self.LRL_slider.grid(row=1, column=2)

            URL_label.grid(row=2, column=0)
            self.URL_val.grid(row=2, column=1)
            self.URL_slider.grid(row=2, column=2)

            
            VA_label.grid(row=3, column=0)
            self.VA_val.grid(row=3, column=1)
            self.VA_slider.grid(row=3, column=2)

            VPW_label.grid(row=4, column=0)
            self.VPW_val.grid(row=4, column=1)
            self.VPW_slider.grid(row=4, column=2)

            VRP_label.grid(row=5, column=0)
            self.VRP_val.grid(row=5, column=1)
            self.VRP_slider.grid(row=5, column=2)

            VS_label.grid(row=6, column=0)
            self.VS_val.grid(row=6, column=1)
            self.VS_slider.grid(row=6, column=2)

            HINT_label.grid(row=7, column=0)
            self.HINT_val.grid(row=7, column=1)
            self.HINT_slider.grid(row=7, column=2)

            submit_button.grid(column=2,row=9,sticky=E)
            quit_button.grid(column=1, row=9, sticky=E, pady=10)

            if (state_name == "VOOR" or state_name == "VVIR"):
                LRL_label.grid(row=1, column=0)
                self.LRL_val.grid(row=1, column=1)
                self.LRL_slider.grid(row=1, column=2)

                URL_label.grid(row=2, column=0)
                self.URL_val.grid(row=2, column=1)
                self.URL_slider.grid(row=2, column=2)

                
                VA_label.grid(row=3, column=0)
                self.VA_val.grid(row=3, column=1)
                self.VA_slider.grid(row=3, column=2)

                VPW_label.grid(row=4, column=0)
                self.VPW_val.grid(row=4, column=1)
                self.VPW_slider.grid(row=4, column=2)

                VRP_label.grid(row=5, column=0)
                self.VRP_val.grid(row=5, column=1)
                self.VRP_slider.grid(row=5, column=2)

                VS_label.grid(row=6, column=0)
                self.VS_val.grid(row=6, column=1)
                self.VS_slider.grid(row=6, column=2)

                HINT_label.grid(row=7, column=0)
                self.HINT_val.grid(row=7, column=1)
                self.HINT_slider.grid(row=7, column=2)

                AT_label.grid(row=8, column=0)
                self.AT_val.grid(row=8, column=1)
                self.AT_slider.grid(row=8, column=2)

                REAC_label.grid(row=9, column=0)
                self.REAC_val.grid(row=9, column=1)
                self.REAC_slider.grid(row=9, column=2)

                REC_label.grid(row=11, column=0)
                self.REC_val.grid(row=11, column=1)
                self.REC_slider.grid(row=11, column=2)

                MSR_label.grid(row=12, column=0)
                self.MSR_val.grid(row=12, column=1)
                self.MSR_slider.grid(row=12, column=2)
                submit_button.grid(column=2,row=13,sticky=E)
                quit_button.grid(column=1, row=13, sticky=E, pady=10)

    
    def SubmitPressed(self,username):
        self.submit_pressed = 1
        self.updateSliderValue(username,"none",0,"none")
        self.parameterdict = {}
    def UpdateLabel(self,val,key,unit):
        param_name = f"{key}_val"
        unit_name = f"unit{unit}"
        if hasattr(self,param_name):
            if(hasattr(self,unit_name)):
                unit = str(getattr(self,unit_name))
                attribute = getattr(self,param_name)
                if(unit == "ppm"):
                    roundval = round(val)
                    attribute['text'] = str(roundval) + unit
                elif(unit == "ms"):
                    roundval = round(val)
                    attribute['text'] = str(roundval) + unit
                elif(unit == "s"):
                    roundval = round(val)
                    attribute['text'] = str(roundval) + unit
                elif(unit == "min"):
                    roundval = round(val) 
                    attribute['text'] = str(roundval) + unit
                elif(unit == ""):
                    roundval = round(val)
                    attribute['text'] = str(roundval)
                else:
                    roundval = round(val,1)
                    attribute['text'] = str(roundval) + unit
        else:
            print(f"Parameter '{param_name}' does not exist")

    def egramScreen(self, mainframe):
        root = tkinter.Tk()
        root.title("Scrolling Egram Data")
       
        fig, ax = plt.subplots()
        canvas = FigureCanvasTkAgg(fig, master=root)
        
        x_data = deque(maxlen=50) 
        y_data = deque(maxlen=50)

        def plot():
 
            if x_data:
                last_x = x_data[-1]
            else:
                last_x = 0
            x_data.append(last_x + 1) 
            y_data.append(np.random.randint(0, 10)) 

            ax.clear()
            ax.scatter(x_data, y_data, c="blue", label="Data Points")
            ax.plot(x_data, y_data, linestyle="--", color="gray") 
            ax.set_xlim(max(0, last_x - 40), last_x + 10) 
            ax.set_ylim(0, 10)  
            ax.set_title("Egram Data")
            ax.set_xlabel("Time")
            ax.set_ylabel("Value")
            ax.legend()

            canvas.draw()

                
            root.after(200, plot)

        canvas.get_tk_widget().pack()

  
        plot()


        root.mainloop()
        


    def updateSliderValue(self,username:str,key:str,value:int,unit):
        param_actions = {
            "LRL": lambda: self.updateParameter(Parameter.LRL, round(self.parameterdict["LRL"]), self.LRL_val,username),
            "URL": lambda: self.updateParameter(Parameter.URL, round(self.parameterdict["URL"]), self.URL_val,username),
            "AA": lambda: self.updateParameter(Parameter.AA, round(self.parameterdict["AA"],1), self.AA_val,username),
            "APW": lambda: self.updateParameter(Parameter.APW, round(self.parameterdict["APW"]), self.APW_val,username),
            "ARP": lambda: self.updateParameter(Parameter.ARP, round(self.parameterdict["ARP"]), self.ARP_val,username),
            "AS": lambda: self.updateParameter(Parameter.AS, round(self.parameterdict["AS"],1), self.AS_val,username),
            "AT": lambda: self.updateParameter(Parameter.AT, round(self.parameterdict["AT"]), self.AT_val,username),
            "VA": lambda: self.updateParameter(Parameter.VA, round(self.parameterdict["VA"],1), self.VA_val,username),
            "VPW": lambda: self.updateParameter(Parameter.VPW, round(self.parameterdict["VPW"]), self.VPW_val,username),
            "VRP": lambda: self.updateParameter(Parameter.VRP, round(self.parameterdict["VRP"]), self.VRP_val,username),
            "VS": lambda: self.updateParameter(Parameter.VS, round(self.parameterdict["VS"],1), self.VS_val,username),
            "HINT": lambda: self.updateParameter(Parameter.HINT, round(self.parameterdict["HINT"]), self.HINT_val,username),
            "REAC": lambda: self.updateParameter(Parameter.REAC, round(self.parameterdict["REAC"]), self.REAC_val,username),
            "RES": lambda: self.updateParameter(Parameter.RES, round(self.parameterdict["RES"]), self.RES_val,username),
            "REC": lambda: self.updateParameter(Parameter.REC, round(self.parameterdict["REC"]), self.REC_val,username),
            "MSR": lambda: self.updateParameter(Parameter.MSR, round(self.parameterdict["MSR"]), self.MSR_val,username),

        }
        self.UpdateLabel(float(value),key,unit)
        if (self.submit_pressed):
            #dictionary for all different parameters, rounds the slider value for readability
            keylist = [key for key in self.parameterdict]
            for key in range(len((keylist))):
                action = param_actions.get(keylist[key])
                if action:
                    action()  #calls the update parameter if the parameter exists
                else:
                    print(f"Unknown parameter: {key}")
           
            self.submit_pressed = 0
            keylist = []
        else: 
            
            value = float(value)
            self.parameterdict[key] = value
            
       

        

    #updates the parameter on the screen and in the json file 
    def updateParameter(self, parameter:Parameter, value, label,username):
        user_processing.updateParameter(username, parameter.getName(),float(value)) #calling the json file update for the user
        label.config(text=str(value) + parameter.getUnit())#updating the label for the parameter
        


    
    #When the register button is pressed
    def register(self):
        
        message = user_processing.RegisterCheck(self.username_entry.get(),self.password_entry.get())
        tkinter.messagebox.showinfo(title="Login", message=message)
           

    
    def clearFrame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        
PacemakerGUI()
