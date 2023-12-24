import customtkinter

class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

class LiveClockFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.liveMasterClock = customtkinter.CTkLabel(self, text="00:00:00", font=("Helvetica", 20))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Midi Time Code Sync")
        self.minsize(400, 180)
        self.geometry("400x180")
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        #self.checkbox_frame = MyCheckboxFrame(self)
        #self.checkbox_frame.grid(row=0, column=0, padx=0, pady=(10, 0), sticky="nsw")


        #self.live_clock_frame = LiveClockFrame(self)
        #self.live_clock_frame.grid(row=0, column=0, padx=10, pady=(10, 0))
        #self.live_clock_frame2 = LiveClockFrame(self)
        #self.live_clock_frame.grid(row=1, column=0, padx=10, pady=(10, 0))
        #self.live_clock_frame2 = LiveClockFrame(self)
        #self.live_clock_frame.grid(row=2, column=0, padx=10, pady=(10, 0))
        #self.live_clock_frame3 = LiveClockFrame(self)
        #self.live_clock_frame3.grid(row=3, column=0, padx=10, pady=(10, 0))
        #self.live_clock_frame4 = LiveClockFrame(self)
        #self.live_clock_frame4.grid(row=0, column=4, padx=10, pady=(10, 0))


        self.label1 = customtkinter.CTkLabel(self, text="my label", font=("Helvetica", 20))
        self.label1 = customtkinter.CTkLabel(self, text="my label", font=("Helvetica", 20))

    def button_callback(self):
        print("button pressed")

app = App()
app.attributes("-topmost", True)
app.mainloop()

app.mainloop()

