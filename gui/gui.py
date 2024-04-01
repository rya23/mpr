import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import geneticgui
import random
import math


class Job:
    def __init__(self, id, time, deadline, holding, penalty):
        self.id = id
        self.time = time
        self.deadline = deadline
        self.holding = holding
        self.penalty = penalty

    def __str__(self):
        return f"ID: {self.id:2d}\tTime: {self.time:2d}\tHolding: {self.holding:2d}\tDeadline: {self.deadline:2d}\tPenalty: {self.penalty:2d}\n"


class AnnealingGUI:
    def __init__(self, master):
        self.arr = []
        self.master = master
        self.master.title("Job Scheduling with Annealing")

        self.create_job_input_fields()

        self.output_area = tk.Text(master, wrap=tk.WORD)
        self.output_area.pack(fill=tk.BOTH, expand=True)
        solve_button = tk.Button(master, text="Solve", command=self.solve)
        solve_button.pack(side=tk.BOTTOM)

    def create_job_input_fields(self):
        input_frame = ttk.Frame(self.master)
        input_frame.pack(side=tk.TOP)

        ttk.Label(input_frame, text="Time:").grid(row=0, column=0, padx=5, pady=5)
        self.time_field = ttk.Entry(input_frame)
        self.time_field.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Deadline:").grid(row=1, column=0, padx=5, pady=5)
        self.deadline_field = ttk.Entry(input_frame)
        self.deadline_field.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Holding Cost:").grid(
            row=2, column=0, padx=5, pady=5
        )
        self.holding_field = ttk.Entry(input_frame)
        self.holding_field.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Penalty:").grid(row=3, column=0, padx=5, pady=5)
        self.penalty_field = ttk.Entry(input_frame)
        self.penalty_field.grid(row=3, column=1, padx=5, pady=5)

        add_button = ttk.Button(input_frame, text="Add Job", command=self.add_job)
        add_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        clear_button = ttk.Button(input_frame, text="Clear", command=self.clear_input)
        clear_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def clear_input(self):
        self.time_field.delete(0, tk.END)
        self.deadline_field.delete(0, tk.END)
        self.holding_field.delete(0, tk.END)
        self.penalty_field.delete(0, tk.END)
        self.arr = []
        self.output_area.delete("1.0", tk.END)

    def add_job(self):
        try:
            time = int(self.time_field.get())
            deadline = int(self.deadline_field.get())
            holding = int(self.holding_field.get())
            penalty = int(self.penalty_field.get())

            if (
                time < 0
                or deadline <= 0
                or holding < 0
                or penalty <= 0
                or time > deadline
            ):
                messagebox.showerror("Error", "Invalid input. Please enter valid data.")
            else:
                self.arr.append(
                    Job(len(self.arr) + 1, time, deadline, holding, penalty)
                )
                self.output_area.insert(
                    tk.END, "Job added: " + str(len(self.arr)) + "\n"
                )
                self.time_field.delete(0, tk.END)
                self.deadline_field.delete(0, tk.END)
                self.holding_field.delete(0, tk.END)
                self.penalty_field.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid data.")

    def solve(self):
        n = len(self.arr)
        neighbour = list(range(n))
        min_cost = geneticgui.solve(self.arr, neighbour)
        l1 = geneticgui.execute(self.arr)
        self.output_area.insert(tk.END, "Current cost: " + str(min_cost) + "\n")

        self.output_area.insert(tk.END, "Optimal job sequence:\n")
        for i in l1:
            job = l1[i]
            self.output_area.insert(
                tk.END,
                str(self.arr[job]),
            )
        # self.output_area.insert(
        #     tk.END, "Total Cost required: " + str(self._solve(self.arr, minimum)) + "\n"
        # )


def main():
    root = tk.Tk()
    app = AnnealingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
