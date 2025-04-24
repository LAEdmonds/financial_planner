import customtkinter

class FinancialPlannerApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")

        # Configure grid layout
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        # Entry widget
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter your income for this month")
        self.entry.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Button widget
        self.button = customtkinter.CTkButton(self, text="Click Me", command=self.button_func)
        self.button.grid(row=0, column=1, padx=20, pady=20, sticky="e")

        # Textbox widget (initially not displayed, will be added on button click)
        self.textbox = customtkinter.CTkTextbox(self, width=400, corner_radius=0)

    def button_func(self):
        text = self.entry.get()
        self.textbox.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")  # Use grid to place textbox
        self.textbox.insert("0.0", text)