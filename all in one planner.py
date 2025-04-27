# financial_planner_updated_v2.py

import customtkinter
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Financial Linked List Classes ---

class FinancialNode:
    def __init__(self, income, class_year, over_21, risk_level, sim_length):
        now = datetime.now()
        self.time = now.strftime("%Y-%m-%d")
        self.income = income
        self.class_year = class_year
        self.over_21 = over_21
        self.risk_level = risk_level
        self.sim_length = sim_length
        self.saving = None
        self.spending = None
        self.invest = None
        self.next = None
        
class FinancialLinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def _compare_dates(self, date1, date2):
        dt1 = datetime.strptime(date1, "%Y-%m-%d")
        dt2 = datetime.strptime(date2, "%Y-%m-%d")
        return dt1 > dt2

    def add(self, income, class_year, over_21, risk_level, sim_length):
        new_node = FinancialNode(income, class_year, over_21, risk_level, sim_length)
        if self.is_empty() or self._compare_dates(self.head.time, new_node.time):
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and not self._compare_dates(current.next.time, new_node.time):
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def display(self):
        records = ""
        current = self.head
        while current:
            record = (f"Date: {current.time}\n"
                      f"  Income: {current.income}\n"
                      f"  Class Year: {current.class_year}\n"
                      f"  Over 21: {current.over_21}\n"
                      f"  Risk Level: {current.risk_level}\n"
                      f"  Simulation Length: {current.sim_length} months\n"
                      "------------------------------\n")
            records += record
            current = current.next
        return records

# --- GUI App Class ---

class FinancialPlannerApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x700")
        self.title("Financial Planner")

        self.planner = FinancialLinkedList()

        # Configure grid
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        # Widgets
        self.income_entry = customtkinter.CTkEntry(self, placeholder_text="Enter your cadet paycheck")
        self.income_entry.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.class_year_option = customtkinter.CTkOptionMenu(self, values=["1/c", "2/c", "3/c", "4/c"])
        self.class_year_option.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.class_year_option.set("Select Class Year")

        self.over21_option = customtkinter.CTkOptionMenu(self, values=["Yes", "No"])
        self.over21_option.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.over21_option.set("Over 21?")

        self.risk_level_option = customtkinter.CTkOptionMenu(self, values=["Saver", "Balancer", "Gambler"], command=self.update_risk_info)
        self.risk_level_option.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.risk_level_option.set("Select Risk Level")

        # Label to display risk level allocation
        self.risk_info_label = customtkinter.CTkLabel(self, text="", width=400, height=100)
        self.risk_info_label.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # Ensure risk_info_label grid row has weight
        self.grid_rowconfigure(4, weight=1)

        self.sim_length_entry = customtkinter.CTkEntry(self, placeholder_text="Simulation length (months)")
        self.sim_length_entry.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.submit_button = customtkinter.CTkButton(self, text="Submit", command=self.submit_data)
        self.submit_button.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        self.textbox = customtkinter.CTkTextbox(self, width=600, height=400)
        self.textbox.grid(row=0, column=1, rowspan=6, padx=20, pady=10, sticky="nsew")

        #Pie Chart
        self.figure = Figure(figsize=(4,2.5), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=7, column=0, columnspan=2, sticky="nsew")

    def update_risk_info(self, risk_level):
        """Update the label with risk level allocation information."""
        if risk_level == "Saver":
            self.risk_info_label.configure(text="Saver: Spend 10%, Save 20%, Invest 70%")
        elif risk_level == "Balancer":
            self.risk_info_label.configure(text="Balancer: Spend 30%, Save 30%, Invest 40%")
        elif risk_level == "Gambler":
            self.risk_info_label.configure(text="Gambler: Spend 50%, Save 10%, Invest 40%")
        else:
            self.risk_info_label.configure(text="")

    def submit_data(self):
        try:
            income = float(self.income_entry.get())  # Bi-weekly paycheck
            class_year = self.class_year_option.get()
            over_21 = self.over21_option.get()
            risk_level = self.risk_level_option.get()
            sim_length = int(self.sim_length_entry.get())  # In months
    
            if "Select" in class_year or "Over" in over_21 or "Select" in risk_level:
                self.textbox.insert("0.0", "Please complete all selections.\n")
                return
    
            # Define risk allocations
            if risk_level == "Saver":
                spend_percentage, save_percentage, invest_percentage = 0.10, 0.20, 0.70
            elif risk_level == "Balancer":
                spend_percentage, save_percentage, invest_percentage = 0.30, 0.30, 0.40
            elif risk_level == "Gambler":
                spend_percentage, save_percentage, invest_percentage = 0.50, 0.10, 0.40
            else:
                self.textbox.insert("0.0", "Invalid risk level selection.\n")
                return
    
            # Calculate amounts spent, saved, and invested per paycheck (bi-weekly)
            spend_amount = income * spend_percentage
            save_amount = income * save_percentage
            invest_amount = income * invest_percentage

            # S&P 500 annual return rate
            annual_return_rate = 0.07
            monthly_return_rate = annual_return_rate / 12  # Approx 0.005833 per month
    
            # Total pay periods (bi-weekly pay, so 2 per month)
            num_pay_periods = sim_length * 2
    
            # Total amounts (before investment growth)
            total_spent = spend_amount * num_pay_periods
            total_saved = save_amount * num_pay_periods
            total_invested = invest_amount * num_pay_periods
    
            # Investment growth calculation:
            # Bi-weekly contributions grow with monthly compounding
            total_investment_value = 0
            for i in range(num_pay_periods):
                # Find how many months are left after this contribution
                months_remaining = sim_length - (i // 2)
                if months_remaining > 0:
                    total_investment_value += invest_amount * ((1 + monthly_return_rate) ** months_remaining)
                else:
                    total_investment_value += invest_amount  # No more time to grow
            roi = (total_investment_value - total_invested) / total_invested * 100
            # Add the data to the planner
            self.planner.add(income, class_year, over_21, risk_level, sim_length)
    
            # Display breakdown
            result_text = (
                f"Risk Level: {risk_level}\n"
                f"Total Simulation Length: {sim_length} months\n"
                f"Total Pay Periods (bi-weekly): {num_pay_periods}\n\n"
                f"Money Breakdown per Paycheck:\n"
                f"  Spend: ${spend_amount:.2f}\n"
                f"  Save:  ${save_amount:.2f}\n"
                f"  Invest: ${invest_amount:.2f}\n\n"
                f"Total for Simulation:\n"
                f"  Total Spent: ${total_spent:.2f}\n"
                f"  Total Saved: ${total_saved:.2f}\n"
                f"  Total Invested (Before Growth): ${total_invested:.2f}\n\n"
                f"Investment Growth (S&P 500 Return Applied):\n"
                f"  Total Investment Value: ${total_investment_value:.2f}\n"
                f"  ROI: {roi:.2f}%"          
            )
    
            self.textbox.insert("0.0", result_text)
            # Pie Chart
            sizes  = [spend_amount, save_amount, invest_amount]
            labels = ['Spend', 'Save', 'Invest']

            self.ax.clear()
            self.ax.pie(sizes,
                        labels=labels,
                        autopct='%1.1f%%',
                        startangle=90)
            self.ax.set_title("Allocation per Paycheck")
            self.ax.axis('equal')           # make it a circle
            self.canvas.draw()

# then your scenario comparison or clearing inputs…

            # Clear inputs
            self.income_entry.delete(0, "end")
            self.sim_length_entry.delete(0, "end")
            self.class_year_option.set("Select Class Year")
            self.over21_option.set("Over 21?")
            self.risk_level_option.set("Select Risk Level")
    
        except ValueError:
            self.textbox.insert("0.0", "Please enter valid numeric values.\n")


    def update_textbox(self):
        self.textbox.delete("0.0", "end")
        records = self.planner.display()
        self.textbox.insert("0.0", records)


# --- FinancialNode and FinancialLinkedList class code remains the same ---

# --- Main Launcher ---

if __name__ == "__main__":
    app = FinancialPlannerApp()
    app.mainloop()