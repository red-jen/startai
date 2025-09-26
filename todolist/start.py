import tkinter as tk
from tkinter import messagebox
from core import add_todo, get_all_todos, update_todo_status, delete_todo, update_task_details

root = tk.Tk()
root.title('To Do List - Kanban Style')
root.geometry("1200x600")

# Global variable to track selected task ID
selected_task_id = None

def add_task():
    title = title_entry.get().strip()
    description = description_entry.get().strip()
    status = selected_status.get()
    priority_label = selected_priority.get()
    priority = priority_values[priority_label]
    
    if not title:
        messagebox.showwarning("Warning", "Task title cannot be empty!")
        return

    try:
        add_todo(title, description, status, priority)
        title_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        selected_priority.set(priority_options[0])
        selected_status.set(status_options[0])
        load_tasks()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add task: {str(e)}")

def load_tasks():
    # Clear all listboxes
    todo_listbox.delete(0, tk.END)
    progress_listbox.delete(0, tk.END)
    done_listbox.delete(0, tk.END)
    
    tasks = get_all_todos()  
    
    # Sort by priority (0=P1, 1=P2, 2=P3)
    tasks_sorted = sorted(tasks, key=lambda x: x[4])  
    
    for task in tasks_sorted:
        task_id, name, description, status, priority = task
        priority_label = [k for k, v in priority_values.items() if v == priority][0] if priority in priority_values.values() else f"P{priority+1}"
        display_text = f"{name} - {description} [{priority_label}]"
        
        # Distribute tasks to appropriate columns
        if status == 'pending':
            todo_listbox.insert(tk.END, display_text)
        elif status == 'in_progress':
            progress_listbox.insert(tk.END, display_text)
        elif status == 'done':
            done_listbox.insert(tk.END, display_text)

def select_task():
    global selected_task_id
    try:
        # Check which listbox has a selection
        selected_index = None
        selected_listbox = None
        
        if todo_listbox.curselection():
            selected_index = todo_listbox.curselection()[0]
            selected_listbox = 'pending'
        elif progress_listbox.curselection():
            selected_index = progress_listbox.curselection()[0]
            selected_listbox = 'in_progress'
        elif done_listbox.curselection():
            selected_index = done_listbox.curselection()[0]
            selected_listbox = 'done'
        
        if selected_index is None:
            messagebox.showwarning("Warning", "Please select a task to update!")
            return
            
        # Get tasks filtered by status and sorted by priority
        tasks = get_all_todos()
        tasks_sorted = sorted(tasks, key=lambda x: x[4])  # Sort by priority
        filtered_tasks = [task for task in tasks_sorted if task[3] == selected_listbox]
        
        if selected_index >= len(filtered_tasks):
            messagebox.showwarning("Warning", "Invalid task selection!")
            return
            
        selected_task = filtered_tasks[selected_index]

        # Extract task details
        selected_task_id, name, description, status, priority = selected_task

        # Populate the entry fields with the selected task's data
        title_entry.delete(0, tk.END)
        title_entry.insert(0, name)
        description_entry.delete(0, tk.END)
        description_entry.insert(0, description)
        selected_status.set(status)
        priority_label = [k for k, v in priority_values.items() if v == priority][0] if priority in priority_values.values() else priority_options[0]
        selected_priority.set(priority_label)
        
        messagebox.showinfo("Task Selected", f"Selected task: {name}")
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to update!")

def update_task():
    global selected_task_id
    if selected_task_id is None:
        messagebox.showwarning("Warning", "No task selected for updating")
        return
    title = title_entry.get().strip()
    description = description_entry.get().strip()
    status = selected_status.get()
    priority_label = selected_priority.get()
    priority = priority_values[priority_label]
    
    if not title:
        messagebox.showwarning("Warning", "Task title cannot be empty")
        return
    try:
        # Update task details (name, description, priority)
        update_task_details(selected_task_id, title, description, priority)
        # Update task status
        update_todo_status(selected_task_id, status)
        
        # Clear the input fields
        title_entry.delete(0, tk.END)
        description_entry.delete(0, tk.END)
        selected_status.set(status_options[0])
        selected_priority.set(priority_options[0])
        selected_task_id = None  # Reset the selected task ID
        load_tasks()
        messagebox.showinfo("Success", "Task updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update task: {str(e)}")

def delete_task():
    global selected_task_id
    if selected_task_id is None:
        messagebox.showwarning("Warning", "No task selected for deletion")
        return
    
    try:
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
            delete_todo(selected_task_id)
            
            # Clear the input fields
            title_entry.delete(0, tk.END)
            description_entry.delete(0, tk.END)
            selected_status.set(status_options[0])
            selected_priority.set(priority_options[0])
            selected_task_id = None  # Reset the selected task ID
            load_tasks()
            messagebox.showinfo("Success", "Task deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete task: {str(e)}")

# Create the main GUI layout
tk.Label(root, text="To-Do List", font=('Arial', 16, 'bold')).pack(pady=10)

# Input section
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Title: ", font=('Arial', 12)).grid(row=0, column=0, sticky="w", padx=5)
title_entry = tk.Entry(input_frame, width=40, font=('Arial', 12))
title_entry.grid(row=0, column=1, padx=5)

tk.Label(input_frame, text="Description:", font=('Arial', 12)).grid(row=1, column=0, sticky="w", padx=5)
description_entry = tk.Entry(input_frame, width=40, font=('Arial', 12))
description_entry.grid(row=1, column=1, padx=5)

tk.Label(input_frame, text="Priority:", font=('Arial', 12)).grid(row=2, column=0, sticky="w", padx=5)
priority_options = ['P1', 'P2', 'P3']
priority_values = {'P1': 0, 'P2': 1, 'P3': 2}
selected_priority = tk.StringVar()
selected_priority.set(priority_options[0])
priority_entry = tk.OptionMenu(input_frame, selected_priority, *priority_options)
priority_entry.grid(row=2, column=1, padx=5, sticky="w")

tk.Label(input_frame, text="Status:", font=('Arial', 12)).grid(row=3, column=0, sticky="w", padx=5)
status_options = ['pending', 'in_progress', 'done']
selected_status = tk.StringVar()
selected_status.set(status_options[0])
status_entry = tk.OptionMenu(input_frame, selected_status, *status_options)
status_entry.grid(row=3, column=1, padx=5, sticky="w")

tk.Button(input_frame, text="Add Task", bg="green", fg="white", command=add_task).grid(row=4, column=0, columnspan=2, pady=10)

# Create frame for the three lists
lists_frame = tk.Frame(root)
lists_frame.pack(pady=10, fill="both", expand=True)

# Todo column
todo_frame = tk.Frame(lists_frame)
todo_frame.pack(side="left", fill="both", expand=True, padx=5)
tk.Label(todo_frame, text="TO DO", font=('Arial', 14, 'bold'), bg="orange", fg="white").pack(fill="x")
todo_listbox = tk.Listbox(todo_frame, width=30, height=15, font=('Arial', 10))
todo_listbox.pack(fill="both", expand=True)

# Progress column
progress_frame = tk.Frame(lists_frame)
progress_frame.pack(side="left", fill="both", expand=True, padx=5)
tk.Label(progress_frame, text="IN PROGRESS", font=('Arial', 14, 'bold'), bg="blue", fg="white").pack(fill="x")
progress_listbox = tk.Listbox(progress_frame, width=30, height=15, font=('Arial', 10))
progress_listbox.pack(fill="both", expand=True)

# Done column
done_frame = tk.Frame(lists_frame)
done_frame.pack(side="left", fill="both", expand=True, padx=5)
tk.Label(done_frame, text="DONE", font=('Arial', 14, 'bold'), bg="green", fg="white").pack(fill="x")
done_listbox = tk.Listbox(done_frame, width=30, height=15, font=('Arial', 10))
done_listbox.pack(fill="both", expand=True)

# Button frame at the bottom
button_frame = tk.Frame(root)
button_frame.pack(side="bottom", pady=10)

tk.Button(button_frame, text="Select Task", bg="orange", fg="white", command=select_task).pack(side='left', padx=5)
tk.Button(button_frame, text="Update Task", bg="blue", fg="white", command=update_task).pack(side='left', padx=5)
tk.Button(button_frame, text="Delete Task", bg="red", fg="white", command=delete_task).pack(side='left', padx=5)

# Load tasks and run the app
load_tasks()
root.mainloop()