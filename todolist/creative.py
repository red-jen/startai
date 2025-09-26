import tkinter as tk
from tkinter import messagebox, ttk
from core import add_todo, get_all_todos, update_todo_status, delete_todo, update_task_details

# --- Color palette ---
BG_COLOR = "#f7f7fa"
ACCENT = "#4f8cff"
SUCCESS = "#43b581"
WARNING = "#ffb347"
ERROR = "#e74c3c"
TEXT = "#222"
FONT = ("Segoe UI", 12)
TITLE_FONT = ("Segoe UI", 20, "bold")
BADGE_COLORS = {"pending": WARNING, "in_progress": ACCENT, "completed": SUCCESS}

root = tk.Tk()
root.title("Creative To-Do List")
root.geometry("700x600")
root.configure(bg=BG_COLOR)
root.minsize(500, 400)

# --- Top Title ---
title_label = tk.Label(root, text="My To-Do List", font=TITLE_FONT, bg=BG_COLOR, fg=ACCENT)
title_label.pack(pady=(20, 10))

# --- Add Task Frame ---
add_frame = tk.Frame(root, bg=BG_COLOR)
add_frame.pack(pady=10, padx=20, fill="x")

tk.Label(add_frame, text="Title", font=FONT, bg=BG_COLOR, fg=TEXT).grid(row=0, column=0, sticky="w")
title_entry = tk.Entry(add_frame, font=FONT, width=25)
title_entry.grid(row=1, column=0, padx=(0, 10), pady=5)

tk.Label(add_frame, text="Description", font=FONT, bg=BG_COLOR, fg=TEXT).grid(row=0, column=1, sticky="w")
desc_entry = tk.Entry(add_frame, font=FONT, width=30)
desc_entry.grid(row=1, column=1, padx=(0, 10), pady=5)

tk.Label(add_frame, text="Status", font=FONT, bg=BG_COLOR, fg=TEXT).grid(row=0, column=2, sticky="w")
status_options = ["pending", "in_progress", "completed"]
status_var = tk.StringVar(value=status_options[0])
status_menu = ttk.Combobox(add_frame, textvariable=status_var, values=status_options, state="readonly", font=FONT, width=12)
status_menu.grid(row=1, column=2, padx=(0, 10), pady=5)

tk.Label(add_frame, text="Priority", font=FONT, bg=BG_COLOR, fg=TEXT).grid(row=0, column=3, sticky="w")
priority_options = ["P1", "P2", "P3"]
priority_values = {"P1": 0, "P2": 1, "P3": 2}
priority_var = tk.StringVar(value=priority_options[0])
priority_menu = ttk.Combobox(add_frame, textvariable=priority_var, values=priority_options, state="readonly", font=FONT, width=6)
priority_menu.grid(row=1, column=3, padx=(0, 10), pady=5)

def clear_inputs():
    title_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    status_var.set(status_options[0])
    priority_var.set(priority_options[0])

def add_task():
    title = title_entry.get().strip()
    desc = desc_entry.get().strip()
    status = status_var.get()
    priority_label = priority_var.get()
    priority = priority_values[priority_label]
    if not title:
        messagebox.showwarning("Input Error", "Title cannot be empty!")
        return
    try:
        add_todo(title, desc, status, priority)
        clear_inputs()
        refresh_tasks()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add task: {e}")

add_btn = tk.Button(add_frame, text="Add Task", font=FONT, bg=ACCENT, fg="white", activebackground=SUCCESS, command=add_task)
add_btn.grid(row=1, column=4, padx=(0, 5), pady=5)

# --- Task List Frame (Scrollable) ---
list_frame = tk.Frame(root, bg=BG_COLOR)
list_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

canvas = tk.Canvas(list_frame, bg=BG_COLOR, highlightthickness=0)
scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
task_container = tk.Frame(canvas, bg=BG_COLOR)

task_container.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=task_container, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# --- Task Card Rendering ---
edit_state = {"id": None}  # Track which task is being edited

def refresh_tasks():
    for widget in task_container.winfo_children():
        widget.destroy()
    tasks = get_all_todos()
    if not tasks:
        tk.Label(task_container, text="No tasks yet!", font=FONT, bg=BG_COLOR, fg="#888").pack(pady=30)
        return
    for task in tasks:
        render_task_card(task)

def render_task_card(task):
    task_id, name, desc, status, priority = task
    card = tk.Frame(task_container, bg="white", bd=2, relief="groove")
    card.pack(fill="x", pady=8, padx=5)

    # Status badge and priority
    badge_frame = tk.Frame(card, bg="white")
    badge_frame.pack(side="left", padx=10, pady=10)
    
    badge = tk.Label(badge_frame, text=status.replace("_", " ").title(), font=("Segoe UI", 10, "bold"),
                     bg=BADGE_COLORS.get(status, ACCENT), fg="white", padx=10, pady=2)
    badge.pack()
    
    priority_label = [k for k, v in priority_values.items() if v == priority][0] if priority in priority_values.values() else f"P{priority+1}"
    priority_badge = tk.Label(badge_frame, text=priority_label, font=("Segoe UI", 8, "bold"),
                             bg="#666", fg="white", padx=5, pady=1)
    priority_badge.pack(pady=(2, 0))

    # Task info (editable if in edit mode)
    if edit_state["id"] == task_id:
        name_var = tk.StringVar(value=name)
        desc_var = tk.StringVar(value=desc)
        status_edit_var = tk.StringVar(value=status)
        priority_label = [k for k, v in priority_values.items() if v == priority][0] if priority in priority_values.values() else priority_options[0]
        priority_edit_var = tk.StringVar(value=priority_label)
        name_entry = tk.Entry(card, textvariable=name_var, font=FONT, width=15)
        name_entry.pack(side="left", padx=2)
        desc_entry = tk.Entry(card, textvariable=desc_var, font=FONT, width=18)
        desc_entry.pack(side="left", padx=2)
        status_menu = ttk.Combobox(card, textvariable=status_edit_var, values=status_options, state="readonly", font=FONT, width=8)
        status_menu.pack(side="left", padx=2)
        priority_menu_edit = ttk.Combobox(card, textvariable=priority_edit_var, values=priority_options, state="readonly", font=FONT, width=5)
        priority_menu_edit.pack(side="left", padx=2)
        def save_edit():
            try:
                priority_val = priority_values[priority_edit_var.get()]
                update_task_details(task_id, name_var.get().strip(), desc_var.get().strip(), priority_val)
                update_todo_status(task_id, status_edit_var.get())
                edit_state["id"] = None
                refresh_tasks()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update task: {e}")
        tk.Button(card, text="Save", font=FONT, bg=SUCCESS, fg="white", command=save_edit).pack(side="left", padx=2)
        tk.Button(card, text="Cancel", font=FONT, bg=ERROR, fg="white", command=lambda: cancel_edit()).pack(side="left", padx=2)
    else:
        # Display info
        info = tk.Frame(card, bg="white")
        info.pack(side="left", fill="x", expand=True)
        tk.Label(info, text=name, font=("Segoe UI", 13, "bold"), bg="white", fg=TEXT, anchor="w").pack(anchor="w")
        tk.Label(info, text=desc, font=("Segoe UI", 11), bg="white", fg="#555", anchor="w").pack(anchor="w")

        # Action buttons
        btns = tk.Frame(card, bg="white")
        btns.pack(side="right", padx=10)
        tk.Button(btns, text="Edit", font=("Segoe UI", 10), bg=ACCENT, fg="white", width=7,
                  command=lambda: start_edit(task_id)).pack(side="left", padx=2)
        tk.Button(btns, text="Delete", font=("Segoe UI", 10), bg=ERROR, fg="white", width=7,
                  command=lambda: delete_task_confirm(task_id)).pack(side="left", padx=2)
        # Status cycle button
        def cycle_status():
            idx = status_options.index(status)
            new_status = status_options[(idx + 1) % len(status_options)]
            try:
                update_todo_status(task_id, new_status)
                refresh_tasks()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update status: {e}")
        tk.Button(btns, text="Next Status", font=("Segoe UI", 10), bg=SUCCESS, fg="white", width=10,
                  command=cycle_status).pack(side="left", padx=2)

def start_edit(task_id):
    edit_state["id"] = task_id
    refresh_tasks()

def cancel_edit():
    edit_state["id"] = None
    refresh_tasks()

def delete_task_confirm(task_id):
    if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
        try:
            delete_todo(task_id)
            refresh_tasks()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete task: {e}")

# --- Initial load ---
refresh_tasks()

root.mainloop()
