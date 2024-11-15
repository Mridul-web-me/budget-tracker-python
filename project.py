import os

Database = "expenses.txt"

#load expenses for a specific user
def load_expenses(username):
    expenses = []
    if os.path.exists(Database):
        with open(Database, "r") as file:
            for line in file:
                data = line.strip().split(":")
                if len(data) == 2 and data[0] == username:
                    expense_data = data[1].split(",")
                    if len(expense_data) == 3:
                        description, amount, category = expense_data
                        expenses.append({
                            "description": description,
                            "amount": float(amount),
                            "category": category
                        })
    return expenses

#save expenses for a specific user
def save_expenses(username, expenses):
    lines = []
    if os.path.exists(Database):
        with open(Database, "r") as file:
            lines = file.readlines()
    
    lines = [line for line in lines if not line.startswith(username + ":")]
    
    # Add updated expenses for the current user
    with open(Database, "w") as file:
        for line in lines:
            file.write(line)
        for expense in expenses:
            file.write(f"{username}:{expense['description']},{expense['amount']},{expense['category']}\n")

#save a new user to the file
def save_user(username):
    if not os.path.exists(Database):
        open(Database, "w").close() 
    with open(Database, "a") as file:
        file.write(f"{username}:\n")

#display the menu
def display_menu():
    print("\n==== Budget Tracker Menu ====")
    print("1. Add an Expense")
    print("2. View Expenses")
    print("3. Delete an Expense")
    print("4. View Total Expenses")
    print("5. Logout")
    print("=============================")

#add a new expense
def add_expense(expenses):
    description = input("Enter expense description: ")
    try:
        amount = float(input("Enter expense amount: "))
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return
    category = input("Enter expense category: ")
    expenses.append({
        "description": description,
        "amount": amount,
        "category": category
    })
    print("Expense added successfully!")


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded.")
        return
    print("\n==== Your Expenses ====")
    for idx, expense in enumerate(expenses, start=1):
        print(f"{idx}. {expense['description']} - ${expense['amount']} ({expense['category']})")

# delete an expense
def delete_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return
    try:
        idx = int(input("Enter the expense number to delete: "))
        if 1 <= idx <= len(expenses):
            removed = expenses.pop(idx - 1)
            print(f"Deleted expense: {removed['description']} - ${removed['amount']} ({removed['category']})")
        else:
            print("Invalid expense number.")
    except ValueError:
        print("Please enter a valid number.")

#view total expenses
def view_total_expenses(expenses):
    total = sum(expense['amount'] for expense in expenses)
    print(f"\nTotal Expenses: ${total:.2f}")

#user registration
def register_user(users):
    username = input("Enter a new username: ")
    if username in users:
        print("Username already exists. Try another one.")
    else:
        users.append(username)
        save_user(username)
        print("User registered successfully!")
    return username

def login_user(users):
    username = input("Enter your username: ")
    username = username.capitalize()
    if username in users:
        print(f"Welcome back, {username}!")
        return username
    else:
        print("User not found. Please register first.")
        return None


def load_users():
    users = set()
    if os.path.exists(Database):
        with open(Database, "r") as file:
            for line in file:
                data = line.strip().split(":")
                if len(data) > 0:
                    username = data[0]
                    users.add(username)
    return list(users)

#Run the Budget Tracker
def main():
    users = load_users()
    current_user = None

    while True:
        if not current_user:
            print("\n==== Welcome to Budget Tracker ====")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            option = input("Select an option (1-3): ")

            if option == '1':
                current_user = login_user(users)
            elif option == '2':
                current_user = register_user(users)
            elif option == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
        else:
            expenses = load_expenses(current_user)
            display_menu()
            choice = input("Select an option (1-5): ")

            if choice == '1':
                add_expense(expenses)
                save_expenses(current_user, expenses)
            elif choice == '2':
                view_expenses(expenses)
            elif choice == '3':
                delete_expense(expenses)
                save_expenses(current_user, expenses)
            elif choice == '4':
                view_total_expenses(expenses)
            elif choice == '5':
                save_expenses(current_user, expenses)
                print("Expenses saved. Logging out...")
                current_user = None
            else:
                print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
