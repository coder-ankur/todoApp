import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime
import mysql.connector

# Establish database connection
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ankur12345",
    database="ToDoApp"
)

def add_task():
    task = task_entry.get()
    date = date_picker.get()

    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor()

    # SQL query to insert the task into the tasks table
    query = "INSERT INTO tasks (task_name, task_date) VALUES (%s, %s)"
    values = (task, date)

    try:
        # Execute the query
        cursor.execute(query, values)

        # Commit the changes to the database
        cnx.commit()

        # Clear the entry fields
        task_entry.delete(0, tk.END)
        date_picker.set_date(datetime.date.today())

        # Refresh the task list
        update_task_list()

    except mysql.connector.Error as err:
        print("Error adding task:", err)

    # Close the cursor
    cursor.close()

def delete_task():
    current_selection = task_list.curselection()
    if current_selection:
        task_index = current_selection[0]
        selected_task = task_list.get(task_index)
        task_parts = selected_task.split('. ', 1)[1].split(' - ')  # Split the task name and date
        task_value = task_parts[0].strip()  # Extract the task name
        print("Task value:", task_value)  # Print the task value

        # Create a cursor object to execute SQL queries
        cursor = cnx.cursor()

        # SQL query to delete the selected task from the tasks table by task_name
        query = "DELETE FROM tasks WHERE task_name = %s"
        values = (task_value,)

        try:
            # Execute the query
            cursor.execute(query, values)

            # Check if any row is affected
            rows_affected = cursor.rowcount
            print(f"Rows affected: {rows_affected}")

            # Commit the changes to the database
            cnx.commit()

            # Close the cursor
            cursor.close()

            # Delete the task from the listbox
            task_list.delete(task_index)

            # Update the indices of the remaining tasks
            for index in range(task_index, task_list.size()):
                task_text = task_list.get(index).split('. ', 1)[1]
                task_list.delete(index)
                task_list.insert(index, f"{index+1}. {task_text}")

        except mysql.connector.Error as err:
            print("Error deleting task:", err)

    else:
        print("Error: No task selected.")


def update_task_list():
    # Clear the current task list
    task_list.delete(0, tk.END)

    # Create a cursor object to execute SQL queries
    cursor = cnx.cursor()

    # SQL query to retrieve all tasks from the tasks table
    query = "SELECT task_name, task_date FROM tasks"

    try:
        # Execute the query
        cursor.execute(query)

        # Fetch all rows from the result set
        tasks = cursor.fetchall()

        # Loop through the tasks and insert them into the task list
        for index, task in enumerate(tasks):
            task_name, task_date = task
            task_list.insert(tk.END, f"{index+1}. {task_name} - {task_date}")

    except mysql.connector.Error as err:
        print("Error retrieving tasks:", err)

    # Close the cursor
    cursor.close()

def save_and_quit():
    # Close the database connection
    cnx.close()

    root.quit()

root = tk.Tk()
root.title("To-Do App")
root.geometry("425x700")
root.resizable(False, False)
root.configure(bg='sky blue')
style = ttk.Style()
style.configure("TLabel", font=("Arial", 16, "bold"), foreground="blue")

task_label = ttk.Label(root, text="Enter Your Task:", style="TLabel")
task_label.pack(pady=10)

task_entry = ttk.Entry(root, font=("Arial", 16))
task_entry.pack(pady=10)

date_label = ttk.Label(root, text="Deadline Date:", style="TLabel")
date_label.pack(pady=10)

date_picker = DateEntry(root, font=("Arial", 16), date_pattern="yyyy-mm-dd")
date_picker.pack(pady=10)
date_picker.set_date(datetime.date.today())

style.configure("TButton", font=("Arial", 16, "bold"), foreground="green")

add_button = ttk.Button(root, text="Add", command=add_task, style="TButton")
add_button.pack(pady=10)

task_list = tk.Listbox(root, font=("Arial", 16), height=10)
task_list.pack(pady=10)

delete_button = ttk.Button(root, text="Delete", command=delete_task, style="TButton")
delete_button.pack(pady=10)

quit_button = ttk.Button(root, text="Save & Exit", command=save_and_quit, style="TButton")
quit_button.pack(pady=10)

# Initial refresh of the task list
update_task_list()

root.mainloop()
