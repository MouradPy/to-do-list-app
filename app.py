# app.py

def display_todos(todos):
    print("\nTo-Do List:")
    for i, todo in enumerate(todos, 1):
        print(f"{i}. {todo}")

def main():
    todos = []

    while True:
        print("\nOptions:")
        print("1. Add a To-Do")
        print("2. View To-Dos")
        print("3. Exit")

        choice = input("Choose an option (1-3): ")

        if choice == '1':
            todo = input("Enter a new to-do: ")
            todos.append(todo)
            print(f'"{todo}" has been added to your to-do list.')
        elif choice == '2':
            display_todos(todos)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
