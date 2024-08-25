class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    # Methods
    def deposit(self, amount, description = ''):
        self.ledger.append({'amount': amount, 'description': description})
    
    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {category.name}')
            category.deposit(amount, f'Transfer from {self.name}')
            return True
        return False

    def check_funds(self, amount):
        if self.get_balance() < amount:
            return False
        return True
    
    def __str__(self):
        title = '{:*^30}'.format(self.name) + '\n'
        formatted_entries = ''
        total = 'Total: {:.2f}'.format(self.get_balance())

        for item in self.ledger:
            formatted_entries += f"{item['description'][:23]:23}{item['amount']:>7.2f}\n"

        return title + formatted_entries + total


# Creates a bar chart that displays the percentage spent in each category
def create_spend_chart(categories):
    chart = 'Percentage spent by category\n'
    # Calculate total spent and percentage spent for each category
    total_spent = sum(-item['amount'] for category in categories for item in category.ledger if item['amount'] < 0)
    category_spent = [(category.name, sum(-item['amount'] for item in category.ledger if item['amount'] < 0)) for category in categories]
    category_averages = [(name, int((spent/total_spent) * 100)) for name, spent in category_spent]

    # Create the chart
    for i in range(100, -10, -10):
        chart += f"{i:>3}| "
        for name, percent in category_averages:
            chart += f"o  " if percent >= i else "   "
        chart += "\n"
    chart += "    -" + "---" * len(categories) + "\n"

    # Add category names vertically
    for i in range(max(len(category.name) for category in categories)):
        chart += "     "
        for category in categories:
            chart += (category.name[i] + "  ") if i < len(category.name) else "   "
        chart += "\n"
    
    return chart.rstrip("\n")