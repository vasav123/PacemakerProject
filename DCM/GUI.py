#Device Controller-Monitor
import tkinter as tk
import datetime
import os
from tkinter import messagebox
from tkinter import Label
import json

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(Welcome)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

class Welcome(tk.Frame):
    def __init__(self, master):
        tk.master = master
        tk.Frame.__init__(self, master)
        tk.Frame()

        tk.Label(self, text="Pacemaker DCM\n").grid(row=0, columnspan=2)
        
        tk.Label(self, text="Username:").grid(row=2)
        tk.Label(self, text="Password:").grid(row=3)
        inUsr = tk.Entry(self)
        inPass = tk.Entry(self, show = "*")
        inUsr.grid(row=2, column=1, padx=5)
        inPass.grid(row=3, column=1, padx=5)

        tk.Button(self, text="Login", command=lambda: self.login(inUsr, inPass)).grid(row=4, columnspan=2)
        tk.Label(self, text="\nDon't have an account?").grid(row=6, columnspan=2)
        tk.Button(self, text="Register", command=lambda: master.switch_frame(Register)).grid(row=7, columnspan=2, pady=5)

    def login(self, inUsr, inPass):
        with open("accounts.txt", "r") as file:
            content = file.readlines()
        
        index = [x for x in range(0, len(content), 2) if inUsr.get() == content[x].strip('\n')]
        if index:
            if inPass.get() == content[index[0]+1].strip('\n'):
                #store current user
                open ("user.txt", "w").close
                with open("user.txt", "a+") as file:
                    file.write(inUsr.get())
                tk.master.switch_frame(Main)
            else:
                tk.Label(self, text="          Error: The password is incorrect.          ").grid(row=8, columnspan=2, pady=5)
        else:
            tk.Label(self, text="          Error: The username does not exist.          ").grid(row=8, columnspan=2, pady=5)


# Must include 1, 2 (input buttons), 3, 4, and 7 from section 3.2.2 in Overview
class Main(tk.Frame):
    def __init__(self, master):
        tk.master = master
        tk.Frame.__init__(self, master)
        
        tk.Label(self, text="Programmable Parameters").grid(row=1, columnspan=3)

        tk.Label(self, text="Parameters").grid(row=2)
        tk.Label(self, text="Value").grid(row=2, column=1)
        tk.Label(self, text="Lower").grid(row=2, column=2)

        # Bradycardia Operation Mode ===================================================================================
        tk.Label(self, text="Bradycardia Operation Mode").grid(row=3)
        bom = tk.StringVar(self)
        bom.set("Off") # default value
        tk.OptionMenu(self, bom, "Off", "AOO", "VOO", "AAI", "VVI").grid(row=3, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_mode(bom)).grid(row=3, column=2)

#################################################################################################################################

        # Lower Rate Limit =============================================================================================
        tk.Label(self, text="Lower Rate Limit (bpm)").grid(row=4)
        self.lrl = tk.Entry(self)
        self.lrl.grid(row=4, column=1)
        self.lrl_b = tk.Button(self, text="Set", command=lambda: self.set_lrl(self.lrl, 1))

        # Upper Rate Limit =============================================================================================
        tk.Label(self, text="Upper Rate Limit (bpm)").grid(row=5)
        self.url = tk.Entry(self)
        self.url.grid(row=5, column=1)
        self.url_b = tk.Button(self, text="Set", command=lambda: self.set_url(self.url, 2))

        # Atrial Pulse Width ===========================================================================================
        tk.Label(self, text="Atrial Pulse Width (ms)").grid(row=6)
        self.apw = tk.Entry(self)
        self.apw.grid(row=6, column=1)
        self.apw_b = tk.Button(self, text="Set", command=lambda: self.set_apw(self.apw, 3))
        #.grid(row=6, column=2)

        # Ventricular Pulse Width ======================================================================================
        tk.Label(self, text="Ventricular Pulse Width (ms)").grid(row=7)
        self.vpw = tk.Entry(self)
        self.vpw.grid(row=7, column=1)
        self.vpw_b = tk.Button(self, text="Set", command=lambda: self.set_vpw(self.vpw, 4))
        #.grid(row=7, column=2)

        # Atrial Pulse Amplitude Regulated =============================================================================
        tk.Label(self, text="Atrial Pulse Amplitude Regulated (V)").grid(row=8)
        self.apar = tk.Entry(self)
        self.apar.grid(row=8, column=1)
        self.apar_b = tk.Button(self, text="Set", command=lambda: self.set_apar(self.apar, 5))
        #.grid(row=8, column=2)

        # Ventricular Pulse Amplitude Regulated =======================================================================
        tk.Label(self, text="Ventricular Pulse Amplitude Regulated (V)").grid(row=9)
        self.vpar = tk.Entry(self)
        self.vpar.grid(row=9, column=1)
        self.vpar_b = tk.Button(self, text="Set", command=lambda: self.set_vpar(self.vpar, 6))
        #.grid(row=9, column=2)

        # Atrial Refractory Period ======================================================================================
        tk.Label(self, text="Atrial Refractory Period (ms)").grid(row=10)
        self.arp = tk.Entry(self)
        self.arp.grid(row=10, column=1)
        self.arp_b = tk.Button(self, text="Set", command=lambda: self.set_arp(self.arp, 7))
        #.grid(row=10, column=2)

        # Ventricular Refractory Period ============================================================================
        tk.Label(self, text="Ventricular Refractory Period (ms)").grid(row=11)
        self.vrp = tk.Entry(self)
        self.vrp.grid(row=11, column=1)
        self.vrp_b = tk.Button(self, text="Set", command=lambda: self.set_vrp(self.vrp, 7))
        #.grid(row=10, column=2)

        tk.Label(self, text="").grid(row=12)
        tk.Label(self, text="Measured Parameters").grid(row=13, columnspan=3)
        
        tk.Label(self, text="Parameter").grid(row=14)
        tk.Label(self, text="Value").grid(row=14, column=1)
        tk.Label(self, text="Lower").grid(row=14, column=2)

        # P Wave =======================================================================================================
        tk.Label(self, text="P Wave (mV)").grid(row=15)
        pwave = tk.Entry(self)
        pwave.grid(row=15, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(pwave, 8)).grid(row=15, column=2)

        # R Wave =======================================================================================================
        tk.Label(self, text="R Wave (mV)").grid(row=16)
        rwave = tk.Entry(self)
        rwave.grid(row=16, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(rwave, 9)).grid(row=16, column=2)

        # PPM ==========================================================================================================
        tk.Label(self, text="PPM").grid(row=17)
        ppm = tk.Entry(self)
        ppm.grid(row=17, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(ppm, 10)).grid(row=17, column=2)

        # Battery Status Level =========================================================================================
        tk.Label(self, text="Battery Status Level").grid(row=18)
        bsl = tk.StringVar(self)
        bsl.set("AOO") # default value
        tk.OptionMenu(self, bsl, "BOL").grid(row=18, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(bsl, 11)).grid(row=18, column=2)

        # Controls =====================================================================================================
        tk.Label(self, text="").grid(row=1, column=3)
        tk.Label(self, text="Controls").grid(row=1, column=4, columnspan=4)
        tk.Button(self, text="Start", command=lambda: self.update_label()).grid(row=2, column=4)
        tk.Button(self, text="Stop", command=lambda: self.stop()).grid(row=2, column=5)
        tk.Button(self, text="Reset", command=lambda: self.stop()).grid(row=2, column=6)
        tk.Button(self, text="Close", command=lambda: self.close()).grid(row=2, column=7)

#################################################################################################################################
        #tk.Label(self, text="Monitor").grid(row=4, column=4, columnspan=4)
        #tk.Label(self, text="Status").grid(row=5, column=4)
        #tk.Label(self, text="Upper Rate Limit").grid(row=6, column=4)
#################################################################################################################################

    def close(self):
        exit()

    def stop(self):
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None

    def set_mode(self, value):
        mode = value.get()
        self.lrl_b.grid_forget()
        self.url_b.grid_forget()
        self.apw_b.grid_forget()
        self.apar_b.grid_forget()
        self.vpw_b.grid_forget()
        self.vpar_b.grid_forget()
        self.arp_b.grid_forget()
        self.vrp_b.grid_forget()
        #Clear all entry fields
        self.lrl.delete(0,'end')
        self.url.delete(0,'end')
        self.apw.delete(0,'end')
        self.vpw.delete(0,'end')
        self.apar.delete(0,'end')
        self.vpar.delete(0,'end')
        self.arp.delete(0,'end')
        self.vrp.delete(0,'end')
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
        
        #Success message for mode selection
        tk.Label(self, text= mode + " mode selected successfully").grid(row=6, column=4, rowspan=2,columnspan=4)

        if (mode == "AOO"):
            #Parameters that will show
            self.lrl_b.grid(row=4, column=2)
            self.url_b.grid(row=5, column=2)
            self.apw_b.grid(row=6, column=2)
            self.apar_b.grid(row=8, column=2)
            #Clear all entry fields
            self.lrl.delete(0,'end')
            self.url.delete(0,'end')
            self.apw.delete(0,'end')
            self.vpw.delete(0,'end')
            self.apar.delete(0,'end')
            self.vpar.delete(0,'end')
            self.arp.delete(0,'end')
            self.vrp.delete(0,'end')
            #Default values to be inserted
            self.lrl.insert(0, LRLval)
            self.url.insert(0, URLval)
            self.apw.insert(0, APWval)
            self.apar.insert(0, APARval)
        if (mode == "VOO"):
            self.lrl_b.grid(row=4, column=2)
            self.url_b.grid(row=5, column=2)
            self.vpw_b.grid(row=7, column=2)
            self.vpar_b.grid(row=9, column=2)
            #Clear all entry fields
            self.lrl.delete(0,'end')
            self.url.delete(0,'end')
            self.apw.delete(0,'end')
            self.vpw.delete(0,'end')
            self.apar.delete(0,'end')
            self.vpar.delete(0,'end')
            self.arp.delete(0,'end')
            self.vrp.delete(0,'end')
            #Default values to be inserted
            self.lrl.insert(0, LRLval)
            self.url.insert(0, URLval)
            self.vpw.insert(0, VPWval)
            self.vpar.insert(0, VPARval)
        if (mode == 'AAI'):
            self.lrl_b.grid(row=4, column=2)
            self.url_b.grid(row=5, column=2)
            self.apw_b.grid(row=6, column=2)
            self.apar_b.grid(row=8, column=2)
            self.arp_b.grid(row=10, column=2)
            #Clear all entry fields
            self.lrl.delete(0,'end')
            self.url.delete(0,'end')
            self.apw.delete(0,'end')
            self.vpw.delete(0,'end')
            self.apar.delete(0,'end')
            self.vpar.delete(0,'end')
            self.arp.delete(0,'end')
            self.vrp.delete(0,'end')
            #Default values to be inserted
            self.lrl.insert(0, LRLval)
            self.url.insert(0, URLval)
            self.apw.insert(0, APWval)
            self.apar.insert(0, APARval)
            self.arp.insert(0, ARPval)
        if (mode == "VVI"):
            self.lrl_b.grid(row=4, column=2)
            self.url_b.grid(row=5, column=2)
            self.vpw_b.grid(row=7, column=2)
            self.vpar_b.grid(row=9, column=2)
            self.vrp_b.grid(row=11, column=2)
            #Clear all entry fields
            self.lrl.delete(0,'end')
            self.url.delete(0,'end')
            self.apw.delete(0,'end')
            self.vpw.delete(0,'end')
            self.apar.delete(0,'end')
            self.vpar.delete(0,'end')
            self.arp.delete(0,'end')
            self.vrp.delete(0,'end')
            #Default values to be inserted
            self.lrl.insert(0, LRLval)
            self.url.insert(0, URLval)
            self.vpw.insert(0, VPWval)
            self.vpar.insert(0, VPARval)
            self.vrp.insert(0, VRPval)
        print (mode)
        return mode
    
    def set_variable(self, value, port):
        if value.get():
            print("Sent " + value.get() + " to port " + str(port) + ".")

    def set_lrl(self, value, port):
        with open('user.txt', 'r') as file:
            curruser = file.read()
        filepath = curruser + '.json'
        with open (filepath) as f:
            usersettings = json.load(f)
        if (value.get().isdigit()) and (int(value.get())>=30 and int(value.get())<=175):
            if(usersettings['URL']>int(value.get())):
                print("Sent " + value.get() + " to port " + str(port) + ".")
                #Update json file value
                usersettings['LRL'] = int(value.get())
                with open (filepath, "w") as file:
                    json.dump(usersettings, file)
            else:
                messagebox.showinfo("Error", "Please ensure your Lower Rate Limit is less than your Upper Rate Limit")
        else:
            messagebox.showinfo("Error", "Please choose a value between 30bpm - 175bpm")

    def set_url(self, value, port):
        with open('user.txt', 'r') as file:
            curruser = file.read()
        filepath = curruser + '.json'
        with open (filepath) as f:
            usersettings = json.load(f)
        if (value.get().isdigit()) and (int(value.get())>=50 and int(value.get())<=175):
            if (usersettings['LRL']<int(value.get())):
                print("Sent " + value.get() + " to port " + str(port) + ".")
                #Update json file value
                usersettings['URL'] = int(value.get())
                with open (filepath, "w") as file:
                    json.dump(usersettings, file)
            else:
                messagebox.showinfo("Error", "Please ensure your Upper Rate Limit is greater than your Lower Rate Limit")
        else:
            messagebox.showinfo("Error", "Please choose a value between 50bpm - 175bpm")

    def set_apw(self, value, port):
        try:
            checknum = float(value.get())
            if (checknum>=0.1 and checknum<=1.9):
                print("Sent " + value.get() + " to port " + str(port) + ".")
                #Update json file value
                with open('user.txt', 'r') as file:
                    curruser = file.read()
                filepath = curruser + '.json'
                with open (filepath) as f:
                    usersettings = json.load(f)
                usersettings['APW'] = float(value.get())
                with open (filepath, "w") as file:
                    json.dump(usersettings, file)
            else:
                messagebox.showinfo("Error", "Please choose a value between 0.1ms - 1.9ms")
        except ValueError:
            messagebox.showinfo("Error", "Please choose a value between 0.1ms - 1.9ms")
    
    def set_vpw(self, value, port):
        try:
            checknum = float(value.get())
            if (checknum>=0.1 and checknum<=1.9):
                print("Sent " + value.get() + " to port " + str(port) + ".")
                #Update json file value
                with open('user.txt', 'r') as file:
                    curruser = file.read()
                filepath = curruser + '.json'
                with open (filepath) as f:
                    usersettings = json.load(f)
                usersettings['VPW'] = float(value.get())
                with open (filepath, "w") as file:
                    json.dump(usersettings, file)
            else:
                messagebox.showinfo("Error", "Please choose a value between 0.1ms - 1.9ms")
        except ValueError:
            messagebox.showinfo("Error", "Please choose a value between 0.1ms - 1.9ms")

    def set_apar(self, value, port):
        try:
            checknum = float(value.get())
            if (checknum>=0.5 and checknum<=3.2) or (checknum>=3.5 and checknum<=7):
                print("Sent " + value.get() + " to port " + str(port) + ".")
                #Update json file value
                with open('user.txt', 'r') as file:
                    curruser = file.read()
                filepath = curruser + '.json'
                with open (filepath) as f:
                    usersettings = json.load(f)
                usersettings['APAR'] = float(value.get())
                with open (filepath, "w") as file:
                    json.dump(usersettings, file)
            else:
                messagebox.showinfo("Error", "Please choose a value between 0.5V - 3.2V or 3.5V - 7.0V")
        except ValueError:
            messagebox.showinfo("Error", "Please choose a value between 0.5V - 3.2V or 3.5V - 7.0V")

    def set_vpar(self, value, port):
        try:
            checknum = float(value.get())
            if (checknum>=0.5 and checknum<=3.2) or (checknum>=3.5 and checknum<=7):
                print("Sent " + value.get() + " to port " + str(port) + ".")
                #Update json file value
                with open('user.txt', 'r') as file:
                    curruser = file.read()
                filepath = curruser + '.json'
                with open (filepath) as f:
                    usersettings = json.load(f)
                usersettings['VPAR'] = float(value.get())
                with open (filepath, "w") as file:
                    json.dump(usersettings, file)
            else:
                messagebox.showinfo("Error", "Please choose a value between 0.5V - 3.2V or 3.5V - 7.0V")
        except ValueError:
            messagebox.showinfo("Error", "Please choose a value between 0.5V - 3.2V or 3.5V - 7.0V")

    def set_arp(self, value, port):
        if (value.get().isdigit()) and (int(value.get())>=150 and int(value.get())<=500):
            print("Sent " + value.get() + " to port " + str(port) + ".")
            #Update json file value
            with open('user.txt', 'r') as file:
                curruser = file.read()
            filepath = curruser + '.json'
            with open (filepath) as f:
                usersettings = json.load(f)
            usersettings['ARP'] = int(value.get())
            with open (filepath, "w") as file:
                json.dump(usersettings, file)
        else:
            messagebox.showinfo("Error", "Please choose a value between 150ms - 500ms")

    def set_vrp(self, value, port):
        if (value.get().isdigit()) and (int(value.get())>=150 and int(value.get())<=500):
            print("Sent " + value.get() + " to port " + str(port) + ".")
            #Update json file value
            with open('user.txt', 'r') as file:
                curruser = file.read()
            filepath = curruser + '.json'
            with open (filepath) as f:
                usersettings = json.load(f)
            usersettings['VRP'] = int(value.get())
            with open (filepath, "w") as file:
                json.dump(usersettings, file)
        else:
            messagebox.showinfo("Error", "Please choose a value between 150ms - 500ms")

    def update_label(self):
        currentTime = datetime.datetime.now()
        tk.Label(self, text=currentTime).grid(row=0)
        self._job = self.after(1000, self.update_label)

#################################################################################################################################

class Register(tk.Frame):
    def __init__(self, master):
        tk.master = master
        tk.Frame.__init__(self, master)
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

        tk.Button(self, text="Register", command=lambda: self.register(regUsr, regPass, regPass2)).grid(row=5, column=0, pady=5)
        tk.Button(self, text="Return", command=lambda: master.switch_frame(Welcome)).grid(row=5, column=1, pady=5)

    def register(self, regUsr, regPass, regPass2):
        if len(regUsr.get()) < 3: 
            tk.Label(self, text="Error: Username must be 3+ characters.").grid(row=6, columnspan=2)
        elif len(regPass.get()) < 6:
            tk.Label(self, text="Error: Password must be 6+ characters.").grid(row=6, columnspan=2)
        elif regPass.get() != regPass2.get():
            tk.Label(self, text="          Error: The passwords do not match.          ").grid(row=6, columnspan=2)
        else:
            with open("accounts.txt", "r") as file:
                content = file.readlines()
        
            if (len(content) >= 20):
                tk.Label(self, text="          Error: Max amount of users reached.          ").grid(row=6, columnspan=2)
            else:
                index = [x for x in range(0, len(content), 2) if regUsr.get() == content[x].strip('\n')]
                if index:
                    tk.Label(self, text="          Error: Username already taken.          ").grid(row=6, columnspan=2)

                else:
                    tk.Label(self, text="          Account created succesfully.          ").grid(row=6, columnspan=2)
                    #Create settings file for new user
                    newUser = {'LRL': 30, 'URL': 50, 'APW': 0.1, 'VPW': 0.1, 'APAR':0.5, 'VPAR':0.5, 'ARP':150, 'VRP':150}
                    filename = regUsr.get() + '.json'
                    with open (filename, "w") as file:
                        json.dump(newUser, file)
                    #Add new user to accounts list
                    with open("accounts.txt", "a+") as file:
                        file.write(regUsr.get() + "\n")
                        file.write(regPass.get() + "\n")

        regUsr.delete(0, len(regUsr.get()))
        regPass.delete(0, len(regPass.get()))
        regPass2.delete(0, len(regPass2.get()))


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
