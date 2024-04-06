import customtkinter



class LiveClockFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.liveMasterClock = customtkinter.CTkLabel(self, text="00:00:00", font=("Helvetica", 20))
        self.liveMasterClock.grid(row=0, column=1, rowspan=2 )


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Midi Time Code Sync")
        self.minsize(400, 180)
        self.geometry("1280x720")

        self.grid_columnconfigure(5, weight=1)
        self.grid_rowconfigure(4, weight=1)
        


        ## ガイド
        self.label00 = customtkinter.CTkLabel(self, text="( 0 0 )", font=("Helvetica", 20)).grid(row=0, column=0, padx=10, pady=(10, 0))
        self.label01 = customtkinter.CTkLabel(self, text="( 0 1 )", font=("Helvetica", 20)).grid(row=0, column=1, padx=10, pady=(10, 0))
        self.label02 = customtkinter.CTkLabel(self, text="( 0 2 )", font=("Helvetica", 20)).grid(row=0, column=2, padx=10, pady=(10, 0))
        self.label03 = customtkinter.CTkLabel(self, text="( 0 3 )", font=("Helvetica", 20)).grid(row=0, column=3, padx=10, pady=(10, 0))

        self.label10 = customtkinter.CTkLabel(self, text="( 1 0 )", font=("Helvetica", 20)).grid(row=1, column=0, padx=10, pady=(10, 0))
        self.label11 = customtkinter.CTkLabel(self, text="( 1 1 )", font=("Helvetica", 20)).grid(row=1, column=1, padx=10, pady=(10, 0))
        self.label12 = customtkinter.CTkLabel(self, text="( 1 2 )", font=("Helvetica", 20)).grid(row=1, column=2, padx=10, pady=(10, 0))
        self.label13 = customtkinter.CTkLabel(self, text="( 1 3 )", font=("Helvetica", 20)).grid(row=1, column=3, padx=10, pady=(10, 0))

        self.label20 = customtkinter.CTkLabel(self, text="( 2 0 )", font=("Helvetica", 20)).grid(row=2, column=0, padx=10, pady=(10, 0))
        self.label21 = customtkinter.CTkLabel(self, text="( 2 1 )", font=("Helvetica", 20)).grid(row=2, column=1, padx=10, pady=(10, 0))
        self.label22 = customtkinter.CTkLabel(self, text="( 2 2 )", font=("Helvetica", 20)).grid(row=2, column=2, padx=10, pady=(10, 0))
        self.label23 = customtkinter.CTkLabel(self, text="( 2 3 )", font=("Helvetica", 20)).grid(row=2, column=3, padx=10, pady=(10, 0))

        self.label30 = customtkinter.CTkLabel(self, text="( 3 0 )", font=("Helvetica", 20)).grid(row=3, column=0, padx=10, pady=(10, 0))
        self.label31 = customtkinter.CTkLabel(self, text="( 3 1 )", font=("Helvetica", 20)).grid(row=3, column=1, padx=10, pady=(10, 0))
        self.label32 = customtkinter.CTkLabel(self, text="( 3 2 )", font=("Helvetica", 20)).grid(row=3, column=2, padx=10, pady=(10, 0))
        self.label33 = customtkinter.CTkLabel(self, text="( 3 3 )", font=("Helvetica", 20)).grid(row=3, column=3, padx=10, pady=(10, 0))
        # ------------------------------

        # Que List


        # Live Clock

        self.live_clock_frame = LiveClockFrame(self)
        self.live_clock_frame.grid(row=0, column=1, columnspan=2, rowspan=2, padx=10, pady=10, sticky="nsw")


    def button_callback(self):
        print("button pressed")

app = App()
app.attributes("-topmost", True)
app.mainloop()

app.mainloop()

