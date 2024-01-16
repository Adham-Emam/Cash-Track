import sys
import json


class CashTrack:
    """
    A class representing a simple cash tracking system.

    Attributes:
    - data (dict): A dictionary containing financial data.
    - budget (int): Monthly budget amount.
    """

    def __init__(self):
        """
        Initializes the CashTrack instance by loading data from a JSON file and displaying initial information.

        Returns:
        - str: A welcome message or an error message if the JSON file has an invalid format.
        """
        try:
            with open("data.json") as f:
                self.data = json.load(f)
                self.budget = self.data["budget"]
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in the data file.")

        print("Welcome To CashTrack", end="\n\n")

    def __str__(self):
        """
        Returns a string representation of the available commands and displays financial information.

        Returns:
        - str: A formatted string containing financial information and available commands.
        """
        if self.data["budget"]:
            print(f"Monthly Budget = {self.data['budget']}$")

        if self.data["expense"] or self.data["income"]:
            net_cash_flow = sum(self.data["income"]) - sum(self.data["expense"])
            if net_cash_flow >= 0:
                print(f"Net Cash Flow = {net_cash_flow}$", end="\n\n")
            elif net_cash_flow < 0:
                print(f"Net Cash Loss = {abs(net_cash_flow)}$", end="\n\n")

        return "1 => Expense Tracking\n2 => Income Tracking\n3 => Budgeting\n4 => Reset\n5 => Exit\n"

    @property
    def get_user_input(self):
        """
        Takes user input for commands.

        Returns:
        - str: User input for commands.
        """
        return input("Enter a command number from above: ")

    @property
    def execute_command(self):
        """
        Executes the user-specified command.

        Returns:
        - str: Output message based on the executed command.
        """
        match self.get_user_input:
            case "1":
                return self.handle_category("expense")
            case "2":
                return self.handle_category("income")
            case "3":
                return self.budgeting()
            case "4":
                return self.reset()
            case "5":
                sys.exit()
        raise ValueError("Please type a number from above")

    def handle_category(self, category):
        """
        Handles expense or income tracking based on user input.

        Parameters:
        - category (str): Either 'expense' or 'income'.

        Returns:
        - str: Output message based on the executed tracking command.
        """
        if category not in ["expense", "income"]:
            raise ValueError("Invalid category. Use 'expense' or 'income'.")

        print(
            f"{category.capitalize()} = {sum(self.data[category])}\n1 => Add {category.capitalize()}\n2 => Subtract {category.capitalize()}\n"
        )

        match self.get_user_input:
            case "1":
                add = int(input(f"Added {category.capitalize()}: "))
                if add >= 0:
                    self.data[category].append(add)
                    self.write_to_json()
                    return f"{category.capitalize()}: {sum(self.data[category]):,}$"
                raise ValueError(
                    f"Added {category.capitalize()} can't be a negative number"
                )

            case "2":
                subtract = int(input(f"Subtracted {category.capitalize()}: "))
                self.data[category].append(int(f"-{subtract}"))
                if sum(self.data[category]) >= 0:
                    self.write_to_json()
                    return f"{category.capitalize()}: {sum(self.data[category]):,}$"
                raise ValueError(f"{category.capitalize()} can't be a negative number")

        raise ValueError("Please type a number from above")

    def write_to_json(self):
        """
        Writes the financial data to the JSON file.
        """
        with open("data.json", "w") as f:
            json.dump(self.data, f)

    def budgeting(self):
        """
        Manages budgeting options based on user input.

        Returns:
        - str: Output message based on the executed budgeting command.
        """
        print("1 => Set Annual Budget\n2 => Set Monthly Budget\n")

        match self.get_user_input:
            case "1":
                budget = int(input("Set your annual budget: ")) / 12
                if budget > 0:
                    self.data["budget"] = int(budget)
                    self.write_to_json()
                    return f"{self.data['budget']:,} monthly target"
                raise ValueError("Annual budget must be a positive value.")
            case "2":
                budget = int(input("Set your annual budget: "))
                if budget > 0:
                    self.data["budget"] = budget
                    self.write_to_json()
                    return f"{self.data['budget']:,} monthly target"
                raise ValueError("Monthly budget must be a positive value.")

        raise ValueError("Please type a number from above")

    def reset(self):
        """
        Resets the financial data, including expenses, income, and budget.

        Returns:
        - str: A message indicating the successful reset operation.
        """
        self.data["expense"].clear()
        self.data["income"].clear()
        self.data["budget"] = 0
        self.write_to_json()
        return "Data Reset Successful"


def main():
    """
    Main function to create a CashTrack instance, display initial information, and execute user commands.
    """
    cash = CashTrack()
    while True:
        print(cash)
        result = cash.execute_command
        print(result)


if __name__ == "__main__":
    main()
