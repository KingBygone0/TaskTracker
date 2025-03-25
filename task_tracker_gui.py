import sqlite3
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

# Database setup
DB_FILE = "tasks.db"

def create_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            due_date TEXT,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_task():
    description = task_entry.get()
    due_date = due_date_entry.get()

    if description.strip() == "" or due_date.strip() == "":
        messagebox.showwarning("Warning", "Task and Due Date cannot be empty!")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description, due_date) VALUES (?, ?)", (description, due_date))
    conn.commit()
    conn.close()

    task_entry.delete(0, tk.END)
    due_date_entry.delete(0, tk.END)
    display_tasks()

def display_tasks():
    task_listbox.delete(0, tk.END)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, due_date, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    for task in tasks:
        task_id, description, due_date, completed = task
        status = "✔️" if completed else "❌"
        task_listbox.insert(tk.END, f"{task_id}. {description} (Due: {due_date}) [{status}]")

def complete_task():
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Select a task to complete!")
        return

    task_id = task_listbox.get(selected).split(".")[0]
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    display_tasks()

def delete_task():
    selected = task_listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Select a task to delete!")
        return

    task_id = task_listbox.get(selected).split(".")[0]
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    display_tasks()

# Initialize GUI
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("Task Tracker")
root.geometry("500x400")

# Widgets
task_label = ctk.CTkLabel(root, text="Task Description:")
task_label.pack()
task_entry = ctk.CTkEntry(root, width=300)
task_entry.pack()

due_date_label = ctk.CTkLabel(root, text="Due Date (YYYY-MM-DD):")
due_date_label.pack()
due_date_entry = ctk.CTkEntry(root, width=300)
due_date_entry.pack()

add_button = ctk.CTkButton(root, text="Add Task", command=add_task)
add_button.pack()

task_listbox = tk.Listbox(root, width=60, height=10)
task_listbox.pack()

complete_button = ctk.CTkButton(root, text="Complete Task", command=complete_task)
complete_button.pack()

delete_button = ctk.CTkButton(root, text="Delete Task", command=delete_task)
delete_button.pack()

# Create the database table
create_table()
display_tasks()

# Run the GUI
root.mainloop()

