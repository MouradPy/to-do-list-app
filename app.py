tasks = []  # Initialize an empty list to store tasks

from datetime import datetime, timedelta  # Import necessary classes for date and time handling
import re  # Import regular expressions for future validation or parsing needs

# Function to add a new task
def add_task():
    task = input("Enter a task: ")  # Prompt user for task description
    
    # Validate the due date and ensure it's not in the past
    while True:
        due_date = input("Enter the due date (YYYY-MM-DD): ")  # Ask for due date
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")  # Convert string to date object
            if due_date_obj < datetime.now():  # Check if the due date is in the past
                print("Due date cannot be in the past. Please enter a valid future date.")
            else:
                break  # Exit loop if due date is valid
        except ValueError:  # Handle invalid date format
            print("Invalid date format. Please enter in YYYY-MM-DD format.")
    
    # Task priority selection
    while True:
        priority = input("Set task priority (Low, Medium, High): ").capitalize()  # Ask for priority
        if priority in ["Low", "Medium", "High"]:  # Validate priority
            break  # Exit loop if priority is valid
        else:
            print("Invalid priority. Please enter 'Low', 'Medium', or 'High'.")
    
    # Append the new task to the tasks list
    tasks.append({"task": task, "completed": False, "due_date": due_date, "priority": priority})
    print(f"'{task}' with a due date of {due_date} and priority '{priority}' has been added.")

# Function to view tasks sorted by either due date or priority
def view_tasks(sort_by="due_date"):
    if not tasks:  # Check if tasks list is empty
        print("No tasks available.")
        return  # Exit the function if no tasks exist

    # Sort tasks based on the specified criteria
    if sort_by == "due_date":
        tasks_sorted = sorted(tasks, key=lambda x: datetime.strptime(x["due_date"], "%Y-%m-%d"))
    elif sort_by == "priority":
        priority_order = {"High": 1, "Medium": 2, "Low": 3}  # Define priority order
        tasks_sorted = sorted(tasks, key=lambda x: priority_order[x["priority"]])

    # Display sorted tasks with status and due date information
    for index, task in enumerate(tasks_sorted, 1):
        status = "Completed" if task["completed"] else "Pending"  # Determine task status
        due_date_obj = datetime.strptime(task["due_date"], "%Y-%m-%d")  # Convert due date string to date object
        
        # Check for overdue tasks and display appropriate message
        if not task["completed"] and due_date_obj < datetime.now():
            print(f"{index}. {task['task']} - {status} (Due: {task['due_date']}, OVERDUE!) - Priority: {task['priority']}")
        else:
            print(f"{index}. {task['task']} - {status} (Due: {task['due_date']}) - Priority: {task['priority']}")

# Function to check for tasks due soon and notify the user
def check_due_tasks():
    now = datetime.now()  # Get the current date and time
    for task in tasks:  # Iterate through all tasks
        due_date_obj = datetime.strptime(task["due_date"], "%Y-%m-%d")  # Convert due date string to date object
        # Notify for tasks due within the next 24 hours
        if not task["completed"] and due_date_obj <= now + timedelta(days=1):
            print(f"Reminder: The task '{task['task']}' is due on {task['due_date']}.")

# Function to filter tasks by priority level
def filter_tasks_by_priority():
    priority_filter = input("Show tasks with priority (Low, Medium, High): ").capitalize()  # Ask for priority filter
    filtered_tasks = [task for task in tasks if task["priority"] == priority_filter]  # Filter tasks by priority
    
    if not filtered_tasks:  # Check if any tasks match the filter
        print(f"No tasks with priority '{priority_filter}' found.")
    else:
        # Display filtered tasks with status and due date
        for index, task in enumerate(filtered_tasks, 1):
            status = "Completed" if task["completed"] else "Pending"
            print(f"{index}. {task['task']} - {status} (Due: {task['due_date']}) - Priority: {task['priority']}")

# Function to filter tasks based on completion status
def filter_tasks_by_status():
    status_filter = input("Show (1) Completed or (2) Pending tasks? ")  # Ask user for status filter
    # Filter tasks based on completion status
    filtered_tasks = [task for task in tasks if (task["completed"] and status_filter == "1") or (not task["completed"] and status_filter == "2")]
    
    if not filtered_tasks:  # Check if any tasks match the selected status
        print("No tasks match the selected status.")
    else:
        # Display filtered tasks
        for index, task in enumerate(filtered_tasks, 1):
            print(f"{index}. {task['task']} (Due: {task['due_date']}) - Priority: {task['priority']}")

# Function to mark a task as complete
def mark_task_complete():
    view_tasks()  # Display current tasks
    try:
        task_num = int(input("Enter the task number to mark as complete: "))  # Prompt for task number
        if 1 <= task_num <= len(tasks):  # Validate task number
            tasks[task_num - 1]["completed"] = True  # Mark the specified task as complete
            print(f"Task {task_num} marked as complete.")
        else:
            print("Invalid task number.")  # Handle invalid input
    except ValueError:  # Handle non-integer input
        print("Please enter a valid number.")

# Function to delete a task
def delete_task():
    view_tasks()  # Display current tasks
    try:
        task_num = int(input("Enter the task number to delete: "))  # Prompt for task number
        if 1 <= task_num <= len(tasks):  # Validate task number
            removed_task = tasks.pop(task_num - 1)  # Remove the specified task
            print(f"Task '{removed_task['task']}' deleted.")
        else:
            print("Invalid task number.")  # Handle invalid input
    except ValueError:  # Handle non-integer input
        print("Please enter a valid number.")

# Function to edit an existing task
def edit_task():
    view_tasks()  # Display current tasks
    try:
        task_num = int(input("Enter the task number to edit: "))  # Prompt for task number
        if 1 <= task_num <= len(tasks):  # Validate task number
            new_task = input("Enter the new task description: ")  # Prompt for new task description
            tasks[task_num - 1]["task"] = new_task  # Update the task description
            
            # Prompt for new due date
            new_due_date = input("Enter the new due date (YYYY-MM-DD) or press Enter to keep the current one: ")
            if new_due_date:  # If a new date is provided
                try:
                    new_due_date_obj = datetime.strptime(new_due_date, "%Y-%m-%d")  # Convert to date object
                    if new_due_date_obj >= datetime.now():  # Check if the new date is valid
                        tasks[task_num - 1]["due_date"] = new_due_date  # Update due date
                        print(f"Task {task_num} due date updated to '{new_due_date}'.")
                    else:
                        print("Due date cannot be in the past. Keeping the current due date.")  # Handle invalid date
                except ValueError:  # Handle invalid date format
                    print("Invalid date format. Keeping the current due date.")
                    
            # Prompt for new priority
            new_priority = input("Enter the new priority (Low, Medium, High) or press Enter to keep the current one: ").capitalize()
            if new_priority in ["Low", "Medium", "High"]:  # Validate priority
                tasks[task_num - 1]["priority"] = new_priority  # Update priority
                print(f"Task {task_num} priority updated to '{new_priority}'.")
            print(f"Task {task_num} updated to '{new_task}'.")
        else:
            print("Invalid task number.")  # Handle invalid input
    except ValueError:  # Handle non-integer input
        print("Please enter a valid number.")

# Function to save tasks to a text file
def save_tasks_to_file():
    with open("tasks.txt", "w") as f:  # Open file in write mode
        for task in tasks:  # Iterate through all tasks
            f.write(f"{task['task']},{task['completed']},{task['due_date']},{task['priority']}\n")  # Write task details to file
    print("Tasks saved to file.")

# Function to load tasks from a text file
def load_tasks_from_file():
    try:
        with open("tasks.txt", "r") as f:  # Open file in read mode
            for line in f:
                values = line.strip().split(",")
                
                # Handle cases where older tasks don't have the priority field
                if len(values) == 3:  # Task, Completed, Due Date
                    task, completed, due_date = values
                    priority = "Medium"  # Default priority for tasks without it
                elif len(values) == 4:  # Task, Completed, Due Date, Priority
                    task, completed, due_date, priority = values
                
                tasks.append({"task": task, "completed": completed == "True", "due_date": due_date, "priority": priority})
    except FileNotFoundError:
        print("No saved tasks found.")

def main():
    load_tasks_from_file()
    check_due_tasks()  # Check for due tasks when starting the app
    while True:
        print("\n1. Add Task\n2. View Tasks (Sorted by Due Date)\n3. View Tasks (Sorted by Priority)\n4. View Tasks by Status\n5. View Tasks by Priority\n6. Mark Task as Complete\n7. Edit Task\n8. Delete Task\n9. Save and Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks("due_date")
        elif choice == "3":
            view_tasks("priority")
        elif choice == "4":
            filter_tasks_by_status()
        elif choice == "5":
            filter_tasks_by_priority()
        elif choice == "6":
            mark_task_complete()
        elif choice == "7":
            edit_task()
        elif choice == "8":
            delete_task()
        elif choice == "9":
            save_tasks_to_file()
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
# After loading tasks in the main function
print("Current tasks:")
view_tasks()  # This will show all tasks with their current priorities
