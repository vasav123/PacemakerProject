import tkinter as tk

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
                master.switch_frame(Main)
            else:
                tk.Label(self, text="          Error: The password is incorrect.          ").grid(row=8, columnspan=2, pady=5)
        else:
            tk.Label(self, text="          Error: The username does not exist.          ").grid(row=8, columnspan=2, pady=5)


class Main(tk.Frame):
    def __init__(self, master):
        tk.master = master
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Main", font=('Helvetica', 18)).grid(row=0)
        tk.Button(self, text="Go back to start page", command=lambda: master.switch_frame(Welcome)).grid(row=1)

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
