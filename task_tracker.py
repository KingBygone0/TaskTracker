import sqlite3
import argparse
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for colored text
init(autoreset=True)

# Database setup
DB_FILE = "tasks.db"

def create_table():
    """Creates a tasks table if it doesn't exist."""
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

def add_task(description, due_date):
    """Adds a task with a due date to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description, due_date) VALUES (?, ?)", (description, due_date))
    conn.commit()
    conn.close()
    print(Fore.GREEN + f"✅ Task added: {description} (Due: {due_date})")

def list_tasks():
    """Lists all tasks."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, description, due_date, completed FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    if not tasks:
        print(Fore.YELLOW + "📌 No tasks available.")
    else:
        for task in tasks:
            task_id, description, due_date, completed = task
            status = Fore.GREEN + "✓" if completed else Fore.RED + "✗"
            print(f"{task_id}. {description} (Due: {due_date}) [{status}{Style.RESET_ALL}]")

def complete_task(task_id):
    """Marks a task as completed."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(Fore.CYAN + f"✅ Task {task_id} marked as complete!")

def delete_task(task_id):
    """Deletes a task from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print(Fore.MAGENTA + f"🗑️ Deleted task {task_id}")

# Set up the CLI parser
parser = argparse.ArgumentParser(description="Task Tracker with SQLite")
parser.add_argument("action", choices=["add", "list", "complete", "delete"], help="Action to perform")
parser.add_argument("--desc", type=str, help="Task description (for 'add')")
parser.add_argument("--due", type=str, help="Due date in YYYY-MM-DD format (for 'add')")
parser.add_argument("--id", type=int, help="Task ID (for 'complete' or 'delete')")

args = parser.parse_args()

# Ensure the database and table exist
create_table()

# Execute the appropriate function
if args.action == "add" and args.desc and args.due:
    add_task(args.desc, args.due)
elif args.action == "list":
    list_tasks()
elif args.action == "complete" and args.id:
    complete_task(args.id)
elif args.action == "delete" and args.id:
    delete_task(args.id)
else:
    print(Fore.RED + "⚠️ Invalid command. Use '--help' for details.")

