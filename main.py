import os
import tkinter as tk
from tkinter import messagebox
from plyer import notification

TASK_FILE = "tasks.txt"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


class WeeklyTodoApp:  # Manages the GUI, tasks, and notifications
    def __init__(self, root):
        self.root = root
        self.root.title("Weekly To-Do List")
        self.root.geometry("770x300")
        self.root.configure(bg="#252426")

        self.frames = {}  # Stores frames for each weekday
        self.task_lists = {}  # Stores a listbox for each weekday

        # Create a grid layout for weekdays
        for idx, day in enumerate(DAYS):
            frame = tk.Frame(root, bg="#252426", padx=5, pady=5)
            frame.grid(row=0, column=idx, sticky="nsew")
            self.frames[day] = frame

            label = tk.Label(frame, text=day, font=("Arial", 12, "bold"), bg="#252426", fg="white")
            label.pack()

            task_list = tk.Listbox(frame, font=("Arial", 10), bg="#909090", fg="black", selectbackground="#808080",
                                   height=10)
            task_list.pack(expand=True, fill="both")
            self.task_lists[day] = task_list

        # Entry field and dropdown menu to select the day
        self.entry = tk.Entry(root, font=("Arial", 12), bg="#909090", fg="black", insertbackground="black")
        self.entry.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

        self.day_var = tk.StringVar(value="Monday")
        self.day_dropdown = tk.OptionMenu(root, self.day_var, *DAYS)
        self.day_dropdown.grid(row=1, column=3, columnspan=2, sticky="ew", padx=10, pady=5)

        # Buttons for add, complete, and delete
        btn_frame = tk.Frame(root, bg="#252426")
        btn_frame.grid(row=2, column=0, columnspan=5, pady=5)

        self.add_btn = tk.Button(btn_frame, text="Add Task", command=self.add_task, bg="#27AE60", fg="white", width=10)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.complete_btn = tk.Button(btn_frame, text="Complete Task", command=self.complete_task, bg="#F39C12",
                                      fg="white", width=12)
        self.complete_btn.grid(row=0, column=1, padx=5)

        self.delete_btn = tk.Button(btn_frame, text="Delete Task", command=self.delete_task, bg="#C0392B", fg="white",
                                    width=10)
        self.delete_btn.grid(row=0, column=2, padx=5)

        self.load_tasks()
        self.notify_pending_tasks()

    def load_tasks(self):
        """Loads tasks from file and assigns them to the correct weekday"""
        if os.path.exists(TASK_FILE):
            with open(TASK_FILE, "r") as file:
                for line in file:
                    try:
                        day, task = line.strip().split("|", 1)
                        if day in DAYS:
                            self.task_lists[day].insert(tk.END, task)
                    except ValueError:
                        continue  # Skip invalid lines

    def save_tasks(self):
        """Saves tasks to the tasks.txt file with assigned days"""
        with open(TASK_FILE, "w") as file:
            for day in DAYS:
                tasks = self.task_lists[day].get(0, tk.END)
                for task in tasks:
                    file.write(f"{day}|{task}\n")

    def add_task(self):
        """Adds a task to the selected weekday"""
        task = self.entry.get().strip()
        day = self.day_var.get()
        if task:
            self.task_lists[day].insert(tk.END, "[ ] " + task)
            self.entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty.")

    def complete_task(self):
        """Marks a selected task as complete for the chosen weekday"""
        day = self.day_var.get()
        try:
            selected = self.task_lists[day].curselection()[0]
            task_text = self.task_lists[day].get(selected)
            if "[ ]" in task_text:
                self.task_lists[day].delete(selected)
                self.task_lists[day].insert(selected, task_text.replace("[ ]", "[✔]"))
                self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to mark as complete.")

    def delete_task(self):
        """Deletes a selected task from the chosen weekday"""
        day = self.day_var.get()
        try:
            selected = self.task_lists[day].curselection()[0]
            self.task_lists[day].delete(selected)
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to delete.")

    def notify_pending_tasks(self):
        """Sends a notification for pending tasks from all weekdays"""
        pending_tasks = []
        for day in DAYS:
            tasks = self.task_lists[day].get(0, tk.END)
            pending_tasks += [f"{day}: {task}" for task in tasks if "[ ]" in task]

        if pending_tasks:
            notification.notify(
                title="Pending Tasks Reminder",
                message="\n".join(pending_tasks[:3]),  # Show up to 3 tasks
                timeout=10
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = WeeklyTodoApp(root)
    root.mainloop()
