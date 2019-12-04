#Device Controller-Monitor
import tkinter as tk
import datetime
import os
from tkinter import messagebox
from tkinter import Label
import json
import serial
import time
import struct
import binascii

packets = [0x16,0x00,0x00,0x01]

# Set up tkinter instance
class SampleApp(tk.Tk):
    # Initialize
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Pacemaker DCM')
        self._frame = None
        self.switch_frame(Welcome)

    # Changes windows
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

# Login window
class Welcome(tk.Frame):
    # Initialize
    def __init__(self, master):
        tk.master = master
        tk.Frame.__init__(self, master)
        tk.Frame()

        # Login labels and text boxes
        tk.Label(self, text="Pacemaker DCM\n").grid(row=0, columnspan=2)
        tk.Label(self, text="Username:").grid(row=2)
        tk.Label(self, text="Password:").grid(row=3)
        inUsr = tk.Entry(self)
        inPass = tk.Entry(self, show = "*")
        inUsr.grid(row=2, column=1, padx=5)
        inPass.grid(row=3, column=1, padx=5)

        # Login button redirects to login() function
        tk.Button(self, text="Login", command=lambda: self.login(inUsr, inPass)).grid(row=4, columnspan=2)
        
        # Register button refirects to new register window
        tk.Label(self, text="\nDon't have an account?").grid(row=6, columnspan=2)
        tk.Button(self, text="Register", command=lambda: master.switch_frame(Register)).grid(row=7, columnspan=2, pady=5)

    #
    def login(self, inUsr, inPass):
        # Checks accounts in "accounts.txt"
        with open("accounts.txt", "r") as file:
            content = file.readlines()
        
        index = [x for x in range(0, len(content), 2) if inUsr.get() == content[x].strip('\n')]
        if index:
            if inPass.get() == content[index[0]+1].strip('\n'):
                # Store current user
                open ("user.txt", "w").close
                with open("user.txt", "a+") as file:
                    file.write(inUsr.get())
                # Switch window to main interface window
                tk.master.switch_frame(Main)
            else:
                tk.Label(self, text="          Error: The password is incorrect.          ").grid(row=8, columnspan=2, pady=5)
        else:
            tk.Label(self, text="          Error: The username does not exist.          ").grid(row=8, columnspan=2, pady=5)

# Register window
class Register(tk.Frame):
    # Initialize
    def __init__(self, master):
        tk.master = master
        tk.Frame.__init__(self, master)

        # Register labels and text boxes
        tk.Label(self, text="Pacemaker DCM\n").grid(row=0, columnspan=2)
        tk.Label(self, text="Register for a new account:").grid(columnspan=2)
        tk.Label(self, text="Username:").grid(row=2)
        tk.Label(self, text="Password:").grid(row=3)
        tk.Label(self, text="Confirm password:").grid(row=4)
        regUsr = tk.Entry(self)
        regPass = tk.Entry(self, show = "*")
        regPass2 = tk.Entry(self, show = "*")
        regUsr.grid(row=2, column=1, padx=5)
        regPass.grid(row=3, column=1, padx=5)
        regPass2.grid(row=4, column=1, padx=5)

        # Register button refirects register() function
        tk.Button(self, text="Register", command=lambda: self.register(regUsr, regPass, regPass2)).grid(row=5, column=0, pady=5)
        # Return button refirects to previous welcome window
        tk.Button(self, text="Return", command=lambda: master.switch_frame(Welcome)).grid(row=5, column=1, pady=5)

    def register(self, regUsr, regPass, regPass2):
        # Checks user name and password
        if len(regUsr.get()) < 3: 
            tk.Label(self, text="Error: Username must be 3+ characters.").grid(row=6, columnspan=2)
        elif len(regPass.get()) < 6:
            tk.Label(self, text="Error: Password must be 6+ characters.").grid(row=6, columnspan=2)
        elif regPass.get() != regPass2.get():
            tk.Label(self, text="          Error: The passwords do not match.          ").grid(row=6, columnspan=2)
        else:
            with open("accounts.txt", "r") as file:
                content = file.readlines()
            # Checks number of accounts, max 10 users + 10 password = 20 lines
            if (len(content) >= 20):
                tk.Label(self, text="          Error: Max amount of users reached.          ").grid(row=6, columnspan=2)
            else:
                index = [x for x in range(0, len(content), 2) if regUsr.get() == content[x].strip('\n')]
                if index:
                    tk.Label(self, text="          Error: Username already taken.          ").grid(row=6, columnspan=2)
                else:
                    tk.Label(self, text="          Account created succesfully.          ").grid(row=6, columnspan=2)
                    # Create settings file for new user
                    newUser = {'LRL': 30, 'URL': 50, 'APW': 0.1, 'VPW': 0.1, 'APAR':0.5, 'VPAR':0.5, 'ARP':150, 'VRP':150, 'FAD':150, 'MSR':120, 'AT':4, 'RAT':30, 'RF':8, 'RCT':5}
                    filename = regUsr.get() + '.json'
                    with open (filename, "w") as file:
                        json.dump(newUser, file)
                    # Add new user to accounts list
                    with open("accounts.txt", "a+") as file:
                        file.write(regUsr.get() + "\n")
                        file.write(regPass.get() + "\n")

        regUsr.delete(0, len(regUsr.get()))
        regPass.delete(0, len(regPass.get()))
        regPass2.delete(0, len(regPass2.get()))

# Main interface window
class Main(tk.Frame):
    # Initialize
    def __init__(self, master):
        tk.master = master
        tk.Frame.__init__(self, master)
        self.row_control = 1
        self.mode_int = -1
        
        # Controls
        tk.Label(self, text="Controls").grid(row=self.row_control, columnspan=4)
        f1 = tk.Frame(self)
        f1.grid(row=self.row_control+1, sticky="nsew")
        tk.Label(f1, text="                                                  ").grid(row=self.row_control+1)
        tk.Button(f1, text="Send All", command=lambda: self.send()).grid(row=self.row_control+1, column=1)
        tk.Button(f1, text="  Close  ", command=lambda: self.close()).grid(row=self.row_control+1, column=2)
        tk.Label(self, text="").grid(row=self.row_control+2, columnspan=4)

        # Initialize row_mode for easier formatting
        self.row_mode = self.row_control+3
        # Start of programmable parameters
        tk.Label(self, text="Programmable Parameters").grid(row=self.row_mode, columnspan=3)
        tk.Label(self, text="Parameters").grid(row=self.row_mode+1)
        tk.Label(self, text="Value").grid(row=self.row_mode+1, column=1)

        # Bradycardia Operation Mode
        tk.Label(self, text="Bradycardia Operation Mode").grid(row=self.row_mode+2)
        self.bom = tk.StringVar(self)
        self.current_bom = tk.StringVar(self)
        self.bom.set("Off") # default value
        self.current_bom.set("Off")
        tk.OptionMenu(self, self.bom, "Off", "AOO", "VOO", "AAI", "VVI", "DOO", "AOOR", "VOOR", "AAIR", "VVIR", "DOOR").grid(row=self.row_mode+2, column=1)

        # Initialize row_prog for easier formatting
        self.row_prog = self.row_mode+3
        # Lower Rate Limit
        tk.Label(self, text="Lower Rate Limit (bpm)").grid(row=self.row_prog)
        self.lrl = tk.Entry(self)
        self.lrl.grid(row=self.row_prog, column=1)
        self.lrl_b = tk.Button(self, text="Save", command=lambda: self.set_lrl(self.lrl), state=tk.DISABLED)
        self.lrl_b.grid(row=self.row_prog, column=2)

        # Upper Rate Limit
        tk.Label(self, text="Upper Rate Limit (bpm)").grid(row=self.row_prog+1)
        self.url = tk.Entry(self)
        self.url.grid(row=self.row_prog+1, column=1)
        self.url_b = tk.Button(self, text="Save", command=lambda: self.set_url(self.url), state=tk.DISABLED)
        self.url_b.grid(row=self.row_prog+1, column=2)
        
        # Atrial Pulse Width
        tk.Label(self, text="Atrial Pulse Width (ms)").grid(row=self.row_prog+2)
        self.apw = tk.Entry(self)
        self.apw.grid(row=self.row_prog+2, column=1)
        self.apw_b = tk.Button(self, text="Save", command=lambda: self.set_apw(self.apw), state=tk.DISABLED)
        self.apw_b.grid(row=self.row_prog+2, column=2)
            
        # Ventricular Pulse Width
        tk.Label(self, text="Ventricular Pulse Width (ms)").grid(row=self.row_prog+3)
        self.vpw = tk.Entry(self)
        self.vpw.grid(row=self.row_prog+3, column=1)
        self.vpw_b = tk.Button(self, text="Save", command=lambda: self.set_vpw(self.vpw), state=tk.DISABLED)
        self.vpw_b.grid(row=self.row_prog+3, column=2)

        # Atrial Pulse Amplitude Regulated
        tk.Label(self, text="Atrial Pulse Amplitude Regulated (V)").grid(row=self.row_prog+4)
        self.apar = tk.Entry(self)
        self.apar.grid(row=self.row_prog+4, column=1)
        self.apar_b = tk.Button(self, text="Save", command=lambda: self.set_apar(self.apar), state=tk.DISABLED)
        self.apar_b.grid(row=self.row_prog+4, column=2)

        # Ventricular Pulse Amplitude Regulated
        tk.Label(self, text="Ventricular Pulse Amplitude Regulated (V)").grid(row=self.row_prog+5)
        self.vpar = tk.Entry(self)
        self.vpar.grid(row=self.row_prog+5, column=1)
        self.vpar_b = tk.Button(self, text="Save", command=lambda: self.set_vpar(self.vpar), state=tk.DISABLED)
        self.vpar_b.grid(row=self.row_prog+5, column=2)

        # Atrial Refractory Period
        tk.Label(self, text="Atrial Refractory Period (ms)").grid(row=self.row_prog+6)
        self.arp = tk.Entry(self)
        self.arp.grid(row=self.row_prog+6, column=1)
        self.arp_b = tk.Button(self, text="Save", command=lambda: self.set_arp(self.arp), state=tk.DISABLED)
        self.arp_b.grid(row=self.row_prog+6, column=2)

        # Ventricular Refractory Period
        tk.Label(self, text="Ventricular Refractory Period (ms)").grid(row=self.row_prog+7)
        self.vrp = tk.Entry(self)
        self.vrp.grid(row=self.row_prog+7, column=1)
        self.vrp_b = tk.Button(self, text="Save", command=lambda: self.set_vrp(self.vrp), state=tk.DISABLED)
        self.vrp_b.grid(row=self.row_prog+7, column=2)

        # Fixed AV Delay
        tk.Label(self, text="Fixed AV Delay (ms)").grid(row=self.row_prog+8)
        self.fad = tk.Entry(self)
        self.fad.grid(row=self.row_prog+8, column=1)
        self.fad_b = tk.Button(self, text="Save", command=lambda: self.set_fad(self.fad), state=tk.DISABLED)
        self.fad_b.grid(row=self.row_prog+8, column=2)

        # Maximum Sensor Rate
        tk.Label(self, text="Maximum Sensor Rate (bpm)").grid(row=self.row_prog+9)
        self.msr = tk.Entry(self)
        self.msr.grid(row=self.row_prog+9, column=1)
        self.msr_b = tk.Button(self, text="Save", command=lambda: self.set_msr(self.msr), state=tk.DISABLED)
        self.msr_b.grid(row=self.row_prog+9, column=2)

        # Activity Threshold
        tk.Label(self, text="Activity Threshold (1 (Lowest) - 7 (Highest))").grid(row=self.row_prog+10)
        self.at = tk.Entry(self)
        self.at.grid(row=self.row_prog+10, column=1)
        self.at_b = tk.Button(self, text="Save", command=lambda: self.set_at(self.at), state=tk.DISABLED)
        self.at_b.grid(row=self.row_prog+10, column=2)

        # Reaction Time
        tk.Label(self, text="Reaction Time (sec)").grid(row=self.row_prog+11)
        self.rat = tk.Entry(self)
        self.rat.grid(row=self.row_prog+11, column=1)
        self.rat_b = tk.Button(self, text="Save", command=lambda: self.set_rat(self.rat), state=tk.DISABLED)
        self.rat_b.grid(row=self.row_prog+11, column=2)

        # Response Factor
        tk.Label(self, text="Response Factor").grid(row=self.row_prog+12)
        self.rf = tk.Entry(self)
        self.rf.grid(row=self.row_prog+12, column=1)
        self.rf_b = tk.Button(self, text="Save", command=lambda: self.set_rf(self.rf), state=tk.DISABLED)
        self.rf_b.grid(row=self.row_prog+12, column=2)

        # Recovery Time
        tk.Label(self, text="Recovery Time (min)").grid(row=self.row_prog+13)
        self.rct = tk.Entry(self)
        self.rct.grid(row=self.row_prog+13, column=1)
        self.rct_b = tk.Button(self, text="Save", command=lambda: self.set_rct(self.rct), state=tk.DISABLED)
        self.rct_b.grid(row=self.row_prog+13, column=2)
        tk.Label(self, text="").grid(row=self.row_prog+14)

        # Mode Update
        self.update_mode()

    # Close the window and exit program 
    def close(self):
        exit()

    # Check if the mode has been updated every 100ms
    def update_mode(self):
        if self.bom.get() != self.current_bom.get():
            self.set_mode(self.bom)
        self.mode_job = self.after(100, self.update_mode)

    # Send current profile to the hardware
    def send(self):
        with open('user.txt', 'r') as file:
            curruser = file.read()
        filepath = curruser + '.json'
        with open (filepath) as f:
            usersettings = json.load(f)
        # Pack bytes in the following order:
        # |  1  |  2  |  3  |  4  |
        # | xFF | x00 | xff | MODE|
        # | LRL | URL | APW | VPW |
        # | APAR| VPAR|    ARP    |
        # |    VRP    |    FAD    |
        # | MSR |  AT | RAT |  RF |
        # | RCT |

        if self.mode_int >= 0:
            packet = bytearray([255,
                                0,
                                255,
                                self.mode_int,
                                usersettings['LRL'], 
                                usersettings['URL'], 
                                int(usersettings['APW'] * 10), 
                                int(usersettings['VPW'] * 10), 
                                int(usersettings['APAR']/7 * 100), 
                                int(usersettings['VPAR']/7 * 100), 
                                usersettings['ARP']%256, 
                                int(usersettings['ARP']/256), 
                                usersettings['VRP']%256, 
                                int(usersettings['VRP']/256), 
                                usersettings['FAD']%256, 
                                int(usersettings['FAD']/256), 
                                usersettings['MSR'], 
                                usersettings['AT'],
                                usersettings['RAT'], 
                                usersettings['RF'], 
                                (usersettings['RCT']*60)%256,
                                int((usersettings['RCT']*60)/256)])
            print("[",end =" ")
            for x in packet:
                print(hex(x),end=" ")
            print("]")
                # print (x)print(binascii.hexlify(packet))
            counter = 0

            ser_found = True
            while ser_found:
                print(counter,"/dev/ttyACM"+str(counter),ser_found)
                if counter > 256:
                    messagebox.showinfo("Error", "Please ensure that the connection is established")
                    ser_found = False
                try:
                    ser = serial.Serial(port = "/dev/ttyACM"+str(counter), baudrate = 115200)
                    ser.flush()
                    ser.write(packet)
                    ser.close()
                    ser_found = False
                    tk.Label(self, text= "                  Data transmitted to Pacemaker successfully                  ").grid(row=self.row_prog+15,columnspan=4)
                except:
                    counter+=1
        else:
            messagebox.showinfo("Error", "Please ensure a mode is currently selected")

            #                 # print (x)print(binascii.hexlify(packet))
            # ser = serial.Serial(port = "/dev/ttyACM0", baudrate = 115200)
            # ser.flush()
            # ser.write(packet)
            # ser.close()
        
# [ 0xff 0x0 0xff 0x3 0x1e 0x3c 0x1 0x1 0x64 0x64 0x96 0x0 0x96 0x0 0x2c 0x1 0xaf 0x1 0xa 0x1 0x1e ]
    # Set Mode        


    def set_mode(self, value):
        mode = value.get()
        self.mode_int = -1
        self.current_bom.set(mode)
        
        # Disable all buttons
        self.lrl_b.configure(state=tk.DISABLED)
        self.url_b.configure(state=tk.DISABLED)
        self.apw_b.configure(state=tk.DISABLED)
        self.apar_b.configure(state=tk.DISABLED)
        self.vpw_b.configure(state=tk.DISABLED)
        self.vpar_b.configure(state=tk.DISABLED)
        self.arp_b.configure(state=tk.DISABLED)
        self.vrp_b.configure(state=tk.DISABLED)
        self.fad_b.configure(state=tk.DISABLED)
        self.msr_b.configure(state=tk.DISABLED)
        self.at_b.configure(state=tk.DISABLED)
        self.rat_b.configure(state=tk.DISABLED)
        self.rf_b.configure(state=tk.DISABLED)
        self.rct_b.configure(state=tk.DISABLED)
        
        # Clear all entry fields
        self.lrl.delete(0,'end')
        self.url.delete(0,'end')
        self.apw.delete(0,'end')
        self.vpw.delete(0,'end')
        self.apar.delete(0,'end')
        self.vpar.delete(0,'end')
        self.arp.delete(0,'end')
        self.vrp.delete(0,'end')
        self.fad.delete(0,'end')
        self.msr.delete(0,'end')
        self.at.delete(0,'end')
        self.rat.delete(0,'end')
        self.rf.delete(0,'end')
        self.rct.delete(0,'end')
        
        #Get User settings values
        with open('user.txt', 'r') as file:
            curruser = file.read()
        filepath = curruser + '.json'
        with open (filepath) as f:
            usersettings = json.load(f)
        LRLval = usersettings['LRL']
        URLval = usersettings['URL']
        APWval = usersettings['APW']
        VPWval = usersettings['VPW']
        APARval = usersettings['APAR']
        VPARval = usersettings['VPAR']
        ARPval = usersettings['ARP']
        VRPval = usersettings['VRP']
        FADval = usersettings['FAD']
        MSRval = usersettings['MSR']
        ATval = usersettings['AT']
        RATval = usersettings['RAT']
        RFval = usersettings['RF']
        RCTval = usersettings['RCT']
        
        # Success message for mode selection
        tk.Label(self, text= "                  " + mode + " mode selected successfully                  ").grid(row=self.row_prog+15,columnspan=4)
        tk.Label(self, text= " ").grid(row=self.row_prog+16,columnspan=4)

        if "AOO" in mode:
            # Set mode and enable buttons
            self.mode_int = 0
            self.lrl_b.config(state=tk.NORMAL)
            self.url_b.config(state=tk.NORMAL)
            self.apw_b.config(state=tk.NORMAL)
            self.apar_b.config(state=tk.NORMAL)
            # Default values to be inserted
            self.lrl.insert(0, LRLval)
            self.url.insert(0, URLval)
            self.apw.insert(0, APWval)
            self.apar.insert(0, APARval)
        if "VOO" in mode:
            # Set mode and enable buttons
            self.mode_int = 1
            self.lrl_b.config(state=tk.NORMAL)
            self.url_b.config(state=tk.NORMAL)
            self.vpw_b.config(state=tk.NORMAL)
            self.vpar_b.config(state=tk.NORMAL)
            # Default values to be inserted
            self.lrl.insert(0, LRLval)
            self.url.insert(0, URLval)
            self.vpw.insert(0, VPWval)
            self.vpar.insert(0, VPARval)
        if "AAI" in mode:
            # Set mode and enable buttons
            self.mode_int = 2
            self.lrl_b.config(state=tk.NORMAL)
            self.url_b.config(state=tk.NORMAL)
            self.apw_b.config(state=tk.NORMAL)
            self.apar_b.config(state=tk.NORMAL)
            self.arp_b.config(state=tk.NORMAL)
            # Default values to be inserted
            self.lrl.insert(0, LRLval)
            self.url.insert(0, URLval)
            self.apw.insert(0, APWval)
            self.apar.insert(0, APARval)
            self.arp.insert(0, ARPval)
        if "VVI" in mode:
            # Set mode and enable buttons
            self.mode_int = 3
            self.lrl_b.config(state=tk.NORMAL)
            self.url_b.config(state=tk.NORMAL)
            self.vpw_b.config(state=tk.NORMAL)
            self.vpar_b.config(state=tk.NORMAL)
            self.vrp_b.config(state=tk.NORMAL)
            # Default values to be inserted
            self.lrl.insert(0, LRLval)
            self.url.insert(0, URLval)
            self.vpw.insert(0, VPWval)
            self.vpar.insert(0, VPARval)
            self.vrp.insert(0, VRPval)
        if "DOO" in mode:
            # Set mode and enable buttons
            self.mode_int = 4
            self.lrl_b.config(state=tk.NORMAL)
            self.url_b.config(state=tk.NORMAL)
            self.apw_b.config(state=tk.NORMAL)
            self.apar_b.config(state=tk.NORMAL)
            self.vpw_b.config(state=tk.NORMAL)
            self.vpar_b.config(state=tk.NORMAL)
            self.fad_b.config(state=tk.NORMAL)
            # Default values to be inserted
            self.lrl.insert(0, LRLval)
            self.url.insert(0, URLval)
            self.apw.insert(0, APWval)
            self.apar.insert(0, APARval)
            self.vpw.insert(0, VPWval)
            self.vpar.insert(0, VPARval)
            self.fad.insert(0, FADval)
        if "R" in mode:
            # Set mode and enable buttons
            self.mode_int += 5
            self.msr_b.configure(state=tk.NORMAL)
            self.at_b.configure(state=tk.NORMAL)
            self.rat_b.configure(state=tk.NORMAL)
            self.rf_b.configure(state=tk.NORMAL)
            self.rct_b.configure(state=tk.NORMAL)
            # Default values to be inserted
            self.msr.insert(0, MSRval)
            self.at.insert(0, ATval)
            self.rat.insert(0, RATval)
            self.rf.insert(0, RFval)
            self.rct.insert(0, RCTval)

        print (mode)
        return mode

    # Save parameter to json
    def set_json(self, value, name):
        with open('user.txt', 'r') as file:
            curruser = file.read()
        filepath = curruser + '.json'
        with open (filepath) as f:
            usersettings = json.load(f)
        usersettings[name] = value
        with open (filepath, "w") as file:
            json.dump(usersettings, file)

    # Functions below checks if each parameter meets its unique boundaries and displays unique messages depending on fail/pass.
    # The function then passes on to set_json which puts the value in the json file
    def set_lrl(self, value):
        if (value.get().isdigit()) and (int(value.get())>=30 and int(value.get())<=175):
            with open('user.txt', 'r') as file:
                curruser = file.read()
            filepath = curruser + '.json'
            with open (filepath) as f:
                usersettings = json.load(f)
            if(usersettings['URL']>int(value.get())):
                tk.Label(self, text= "                    Lower Rate Limit saved to " + value.get() + "bpm                    ").grid(row=self.row_prog+15,columnspan=4)
                self.set_json(int(value.get()), 'LRL')
            else:
                messagebox.showinfo("Error", "Please ensure your Lower Rate Limit is less than your Upper Rate Limit")
        else:
            messagebox.showinfo("Error", "Please choose an integer value between 30bpm - 175bpm")

    def set_url(self, value):
        if (value.get().isdigit()) and (int(value.get())>=50 and int(value.get())<=175):
            with open('user.txt', 'r') as file:
                curruser = file.read()
            filepath = curruser + '.json'
            with open (filepath) as f:
                usersettings = json.load(f)
            if (usersettings['LRL']<int(value.get())):
                tk.Label(self, text= "                    Upper Rate Limit saved to " + value.get() + "bpm                    ").grid(row=self.row_prog+15,columnspan=4)
                self.set_json(int(value.get()), 'URL')
            else:
                messagebox.showinfo("Error", "Please ensure your Upper Rate Limit is greater than your Lower Rate Limit")
        else:
            messagebox.showinfo("Error", "Please choose an integer value between 50bpm - 175bpm")

    def set_apw(self, value):
        try:
            checknum = float(value.get())
            if (checknum>=0.1 and checknum<=1.9):
                tk.Label(self, text= "                    Atrial Pulse Width saved to " + value.get() + "ms                    ").grid(row=self.row_prog+15,columnspan=4)
                self.set_json(checknum, 'APW')
            else:
                messagebox.showinfo("Error", "Please choose a value between 0.1ms - 1.9ms")
        except ValueError:
            messagebox.showinfo("Error", "Please choose a value between 0.1ms - 1.9ms")
    
    def set_vpw(self, value):
        try:
            checknum = float(value.get())
            if (checknum>=0.1 and checknum<=1.9):
                tk.Label(self, text= "                    Ventricular Pulse Width saved to " + value.get() + "ms                    ").grid(row=self.row_prog+15,columnspan=4)
                self.set_json(checknum, 'VPW')
            else:
                messagebox.showinfo("Error", "Please choose a value between 0.1ms - 1.9ms")
        except ValueError:
            messagebox.showinfo("Error", "Please choose a value between 0.1ms - 1.9ms")

    def set_apar(self, value):
        try:
            checknum = float(value.get())
            if (checknum>=0.5 and checknum<=3.2) or (checknum>=3.5 and checknum<=7):
                tk.Label(self, text= "                    Atrial Pulse Amplitude Regulated saved to " + value.get() + "V                    ").grid(row=self.row_prog+15,columnspan=4)
                self.set_json(checknum, 'APAR')
            else:
                messagebox.showinfo("Error", "Please choose a value between 0.5V - 3.2V or 3.5V - 7.0V")
        except ValueError:
            messagebox.showinfo("Error", "Please choose a value between 0.5V - 3.2V or 3.5V - 7.0V")

    def set_vpar(self, value):
        try:
            checknum = float(value.get())
            if (checknum>=0.5 and checknum<=3.2) or (checknum>=3.5 and checknum<=7):
                tk.Label(self, text= "                    Ventricular Pulse Amplitude Regulated saved to " + value.get() + "V                    ").grid(row=self.row_prog+15,columnspan=4)
                self.set_json(checknum, 'VPAR')
            else:
                messagebox.showinfo("Error", "Please choose a value between 0.5V - 3.2V or 3.5V - 7.0V")
        except ValueError:
            messagebox.showinfo("Error", "Please choose a value between 0.5V - 3.2V or 3.5V - 7.0V")

    def set_arp(self, value):
        if (value.get().isdigit()) and (int(value.get())>=150 and int(value.get())<=500):
            tk.Label(self, text= "                    Atrial Refractory Period saved to " + value.get() + "ms                    ").grid(row=self.row_prog+15,columnspan=4)
            self.set_json(int(value.get()), 'ARP')
        else:
            messagebox.showinfo("Error", "Please choose an integer value between 150ms - 500ms")

    def set_vrp(self, value):
        if (value.get().isdigit()) and (int(value.get())>=150 and int(value.get())<=500):
            tk.Label(self, text= "                    Ventricular Refractory Period saved to " + value.get() + "ms                    ").grid(row=self.row_prog+15,columnspan=4)
            self.set_json(int(value.get()), 'VRP')
        else:
            messagebox.showinfo("Error", "Please choose an integer value between 150ms - 500ms")

    def set_fad(self, value):
        if (value.get().isdigit()) and (int(value.get())>=70 and int(value.get())<=300):
            tk.Label(self, text= "                    Fixed VA Delay saved to " + value.get() + "ms                    ").grid(row=self.row_prog+15,columnspan=4)
            self.set_json(int(value.get()), 'FAD')
        else:
            messagebox.showinfo("Error", "Please choose an integer value between 70ms - 300ms")

    def set_msr(self, value):
        if (value.get().isdigit()) and (int(value.get())>=50 and int(value.get())<=175):
            tk.Label(self, text= "                    Ventricular Refractory Period saved to " + value.get() + "bpm                    ").grid(row=self.row_prog+15,columnspan=4)
            self.set_json(int(value.get()), 'MSR')
        else:
            messagebox.showinfo("Error", "Please choose an integer value between 50bpm - 175bpm")

    def set_at(self, value):
        if (value.get().isdigit()) and (int(value.get())>=1 and int(value.get())<=7):
            tk.Label(self, text= "                    Activity Threshold saved to " + value.get() + "                    ").grid(row=self.row_prog+15,columnspan=4)
            self.set_json(int(value.get()), 'AT')
        else:
            messagebox.showinfo("Error", "Please choose an integer value between 1 - 7")

    def set_rat(self, value):
        if (value.get().isdigit()) and (int(value.get())>=10 and int(value.get())<=50):
            tk.Label(self, text= "                    Reaction Time saved to " + value.get() + "sec                    ").grid(row=self.row_prog+15,columnspan=4)
            self.set_json(int(value.get()), 'RAT')
        else:
            messagebox.showinfo("Error", "Please choose an integer value between 10sec - 50sec")

    def set_rf(self, value):
        if (value.get().isdigit()) and (int(value.get())>=1 and int(value.get())<=16):
            tk.Label(self, text= "                    Response Factor saved to " + value.get() + "                    ").grid(row=self.row_prog+15,columnspan=4)
            self.set_json(int(value.get()), 'RF')
        else:
            messagebox.showinfo("Error", "Please choose an integer value between 1 - 16")

    def set_rct(self, value):
        if (value.get().isdigit()) and (int(value.get())>=2 and int(value.get())<=16):
            tk.Label(self, text= "                    Recovery Time saved to " + value.get() + "min                    ").grid(row=self.row_prog+15,columnspan=4)
            self.set_json(int(value.get()), 'RCT')
        else:
            messagebox.showinfo("Error", "Please choose an integer value between 2min - 16min")

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
