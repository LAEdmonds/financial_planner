from datetime import datetime
"""
This part of the code is the algorithms part using linked lists
"""
class FinancialNode:
    def __init__(self, income):
        now = datetime.now()
        self.time = now.strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
        self.income = income
        self.saving = None
        self.spending = None
        self.invest = None
        self.next = None

    # Getters
    def get_time(self):
        return self.time

    def get_income(self):
        return self.income

    def get_saving(self):
        return self.saving

    def get_spending(self):
        return self.spending

    def get_invest(self):
        return self.invest

    # Setters
    def set_income(self, income):
        self.income = income

    def set_saving(self, saving):
        self.saving = saving

    def set_spending(self, spending):
        self.spending = spending

    def set_invest(self, invest):
        self.invest = invest


class FinancialLinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def _compare_dates(self, date1, date2):
        """Return True if date1 is after date2"""
        dt1 = datetime.strptime(date1, "%Y-%m-%d")
        dt2 = datetime.strptime(date2, "%Y-%m-%d")
        return dt1 > dt2

    def add(self, income):
        new_node = FinancialNode(income)
        if self.is_empty() or self._compare_dates(self.head.get_time(), new_node.get_time()):
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next and not self._compare_dates(current.next.get_time(), new_node.get_time()):
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def search(self, year, month):
        """Searches for the first node in the given year and month"""
        target_prefix = f"{year}-{month:02d}"
        current = self.head
        while current:
            if current.get_time().startswith(target_prefix):
                return current
            current = current.next
        return None

    def size(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def display(self):
        current = self.head
        while current:
            print(f"Date:     {current.get_time()}")
            print(f"  Income:   {current.get_income()}")
            print(f"  Saving:   {current.get_saving()}")
            print(f"  Spending: {current.get_spending()}")
            print(f"  Invest:   {current.get_invest()}")
            print("-" * 30)
            current = current.next


# Example usage
if __name__ == "__main__":
    planner = FinancialLinkedList()

    # Adding nodes
    planner.add(4000)
    planner.add(5000)

    # Editing a specific month's data
    now = datetime.now()
    node = planner.search(now.year, now.month)
    if node:
        node.set_saving(800)
        node.set_spending(2200)
        node.set_invest(1000)

    # Displaying records
    print("Financial Records:")
    planner.display()
    print("Total Records:", planner.size())
