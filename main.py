import os
import tkinter as tk
from tkinter import messagebox
from plyer import notification

TASK_FILE = "tasks.txt"

class TodoApp: # Manages the GUI, tasks, and notifications from the OS
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("300x400")
        self.root.configure(bg="#252426")

        self.task_list = tk.Listbox(root, font=("Arial", 12), bg="#909090", fg="black", selectbackground="#808080")
        self.task_list.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(root, font=("Arial", 12), bg="#909090", fg="black", insertbackground="black")
        self.entry.pack(pady=5, padx=10, fill=tk.X)

        btn_frame = tk.Frame(root, bg="#252426")
        btn_frame.pack(pady=5)

        self.add_btn = tk.Button(btn_frame, text="Add", command=self.add_task, bg="#27AE60", fg="white", width=8)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.complete_btn = tk.Button(btn_frame, text="Complete", command=self.complete_task, bg="#F39C12", fg="white", width=8)
        self.complete_btn.grid(row=0, column=1, padx=5)

        self.delete_btn = tk.Button(btn_frame, text="Delete", command=self.delete_task, bg="#C0392B", fg="white", width=8)
        self.delete_btn.grid(row=0, column=2, padx=5)

        self.load_tasks()
        self.notify_pending_tasks()

    def load_tasks(self):
        """Loads tasks from file, display in the box"""
        if os.path.exists(TASK_FILE):
            with open(TASK_FILE, "r") as file:
                tasks = file.readlines()
                for task in tasks:
                    self.task_list.insert(tk.END, task.strip())

    def save_tasks(self):
        """Saves tasks to file"""
        tasks = self.task_list.get(0, tk.END)
        with open(TASK_FILE, "w") as file:
            for task in tasks:
                file.write(task + "\n")

    def add_task(self):
        """Adds a new task"""
        task = self.entry.get().strip()
        if task:
            self.task_list.insert(tk.END, "[ ] " + task)
            self.entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty.")

    def complete_task(self):
        """Marks a task as complete"""
        try:
            selected = self.task_list.curselection()[0]
            task_text = self.task_list.get(selected)
            if "[ ]" in task_text:
                self.task_list.delete(selected)
                self.task_list.insert(selected, task_text.replace("[ ]", "[✔]"))
                self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to mark as complete.")

    def delete_task(self):
        """Deletes a selected task"""
        try:
            selected = self.task_list.curselection()[0]
            self.task_list.delete(selected)
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to delete.")

    def notify_pending_tasks(self):
        """Sends a notification for pending tasks"""
        tasks = self.task_list.get(0, tk.END)
        pending = [task for task in tasks if "[ ]" in task]
        if pending:
            notification.notify(
                title="Pending Tasks Reminder",
                message="\n".join(pending[:3]),  # Show up to 3 tasks
                timeout=10
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
