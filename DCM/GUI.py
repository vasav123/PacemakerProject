#Device Controller-Monitor
import tkinter as tk
import datetime

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
        inPass = tk.Entry(self)
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
        bom.set("AOO") # default value
        tk.OptionMenu(self, bom, "AOO", "VOO", "AAI", "VVI").grid(row=3, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(bom, 0)).grid(row=3, column=2)

        # Lower Rate Limit =============================================================================================
        tk.Label(self, text="Lower Rate Limit").grid(row=4)
        lrl = tk.Entry(self)
        lrl.grid(row=4, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(lrl, 1)).grid(row=4, column=2)

        # Upper Rate Limit =============================================================================================
        tk.Label(self, text="Upper Rate Limit").grid(row=5)
        url = tk.Entry(self)
        url.grid(row=5, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(url, 2)).grid(row=5, column=2)

        # Atrial Pulse Width ===========================================================================================
        tk.Label(self, text="Atrial Pulse Width").grid(row=6)
        apw = tk.Entry(self)
        apw.grid(row=6, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(apw, 3)).grid(row=6, column=2)

        # Ventricular Pulse Width ======================================================================================
        tk.Label(self, text="Ventricular Pulse Width").grid(row=7)
        vpw = tk.Entry(self)
        vpw.grid(row=7, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(bom, 4)).grid(row=7, column=2)

        # Atrial Pulse Amplotude Regulated =============================================================================
        tk.Label(self, text="Atrial Pulse Amplotude Regulated").grid(row=8)
        apar = tk.Entry(self)
        apar.grid(row=8, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(apar, 5)).grid(row=8, column=2)

        # Ventricular Pulse Ampliotude Regulated =======================================================================
        tk.Label(self, text="Bradycardia Operation Mode").grid(row=9)
        vpar = tk.Entry(self)
        vpar.grid(row=9, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(vpar, 6)).grid(row=9, column=2)

        # Fixed AV Delay ===============================================================================================
        tk.Label(self, text="Fixed AV Delay").grid(row=10)
        fad = tk.Entry(self)
        fad.grid(row=10, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(fad, 7)).grid(row=10, column=2)

        tk.Label(self, text="").grid(row=11)
        tk.Label(self, text="Measured Parameters").grid(row=12, columnspan=3)
        
        tk.Label(self, text="Parameter").grid(row=13)
        tk.Label(self, text="Value").grid(row=13, column=1)
        tk.Label(self, text="Lower").grid(row=13, column=2)

        # P Wave =======================================================================================================
        tk.Label(self, text="P Wave").grid(row=14)
        pwave = tk.Entry(self)
        pwave.grid(row=14, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(pwave, 8)).grid(row=14, column=2)

        # R Wave =======================================================================================================
        tk.Label(self, text="R Wave").grid(row=15)
        rwave = tk.Entry(self)
        rwave.grid(row=15, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(rwave, 9)).grid(row=15, column=2)

        # PPM ==========================================================================================================
        tk.Label(self, text="PPM").grid(row=16)
        ppm = tk.Entry(self)
        ppm.grid(row=16, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(ppm, 10)).grid(row=16, column=2)

        # Battery Status Level =========================================================================================
        tk.Label(self, text="Battery Status Level").grid(row=17)
        bsl = tk.StringVar(self)
        bsl.set("AOO") # default value
        tk.OptionMenu(self, bsl, "BOL").grid(row=17, column=1)
        tk.Button(self, text="Set", command=lambda: self.set_variable(bsl, 11)).grid(row=17, column=2)

        # Controls =====================================================================================================
        tk.Label(self, text="").grid(row=1, column=3)
        tk.Label(self, text="Controls").grid(row=1, column=4, columnspan=4)
        tk.Button(self, text="Start", command=lambda: self.update_label()).grid(row=2, column=4)
        tk.Button(self, text="Stop", command=lambda: self.stop()).grid(row=2, column=5)
        tk.Button(self, text="Reset", command=lambda: self.stop()).grid(row=2, column=6)
        tk.Button(self, text="Close", command=lambda: self.close()).grid(row=2, column=7)

        #tk.Label(self, text="Monitor").grid(row=4, column=4, columnspan=4)
        #tk.Label(self, text="Status").grid(row=5, column=4)
        #tk.Label(self, text="Upper Rate Limit").grid(row=6, column=4)


    def close(self):
        exit()

    def stop(self):
        if self._job is not None:
            self.after_cancel(self._job)
            self._job = None

    def set_variable(self, value, port):
        if value.get():
            print("Sent " + value.get() + " to port " + str(port) + ".")

    def update_label(self):
        currentTime = datetime.datetime.now()
        tk.Label(self, text=currentTime).grid(row=0)
        self._job = self.after(1000, self.update_label)

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
        regPass = tk.Entry(self)
        regPass2 = tk.Entry(self)
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
        
            index = [x for x in range(0, len(content), 2) if regUsr.get() == content[x].strip('\n')]
            if index:
                tk.Label(self, text="          Error: Username already taken.          ").grid(row=6, columnspan=2)

            else:
                tk.Label(self, text="          Account created succesfully.          ").grid(row=6, columnspan=2)
                with open("accounts.txt", "a+") as file:
                    file.write(regUsr.get() + "\n")
                    file.write(regPass.get() + "\n")

        regUsr.delete(0, len(regUsr.get()))
        regPass.delete(0, len(regPass.get()))
        regPass2.delete(0, len(regPass2.get()))


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()