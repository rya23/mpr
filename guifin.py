import tkinter as tk
from tkinter import messagebox


class Job:
    def __init__(self, id, time, deadline, holding, penalty):
        self.id = id
        self.time = time
        self.deadline = deadline
        self.holding = holding
        self.penalty = penalty


class AnnealingTkinter:
    def __init__(self):
        self.arr = []
        self.initialize_gui()

    def initialize_gui(self):
        self.root = tk.Tk()
        self.root.title("Job Scheduling with Annealing")

        self.create_job_input_fields()

        self.output_area = tk.Text(self.root, height=15, width=80)
        self.output_area.pack(padx=5, pady=5)

        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        self.solve_button.pack(pady=5)

    def create_job_input_fields(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=5, pady=5)

        tk.Label(input_frame, text="Time:").pack(side=tk.LEFT)
        self.time_field = tk.Entry(input_frame)
        self.time_field.pack(side=tk.LEFT)

        tk.Label(input_frame, text="Deadline:").pack(side=tk.LEFT)
        self.deadline_field = tk.Entry(input_frame)
        self.deadline_field.pack(side=tk.LEFT)

        tk.Label(input_frame, text="Holding Cost:").pack(side=tk.LEFT)
        self.holding_field = tk.Entry(input_frame)
        self.holding_field.pack(side=tk.LEFT)

        tk.Label(input_frame, text="Penalty:").pack(side=tk.LEFT)
        self.penalty_field = tk.Entry(input_frame)
        self.penalty_field.pack(side=tk.LEFT)

        self.add_button = tk.Button(input_frame, text="Add Job", command=self.add_job)
        self.add_button.pack(side=tk.LEFT, padx=5)

    def add_job(self):
        try:
            time = int(self.time_field.get())
            deadline = int(self.deadline_field.get())
            holding = int(self.holding_field.get())
            penalty = int(self.penalty_field.get())

            self.arr.append(Job(len(self.arr) + 1, time, deadline, holding, penalty))
            self.output_area.insert(tk.END, f"Job added: {len(self.arr)}\n")

            self.time_field.delete(0, tk.END)
            self.deadline_field.delete(0, tk.END)
            self.holding_field.delete(0, tk.END)
            self.penalty_field.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid integers.")

    def solve(self):
        n = len(self.arr)
        neighbour = list(range(n))
        min_cost = self.solve_cost(neighbour)

        t = min_cost / 2
        c = 0.9
        minimum = neighbour.copy()

        while t > 1:
            self.neighbour(neighbour, t)
            temp_cost = self.solve_cost(neighbour)
            t *= c
            if temp_cost < min_cost:
                min_cost = temp_cost
                minimum = neighbour.copy()

        self.output_area.insert(tk.END, f"Optimal job sequence:\n")
        for i in minimum:
            job = self.arr[i]
            self.output_area.insert(
                tk.END,
                f"Job ID: {job.id}\tTime: {job.time}\tDeadline: {job.deadline}\tHolding Cost: {job.holding}\tPenalty: {job.penalty}\n",
            )
        self.output_area.insert(
            tk.END, f"Total Cost required: {self.solve_cost(minimum)}\n"
        )

    def solve_cost(self, seq):
        pen = 0
        hold = 0
        ptime = 0
        for i in seq:
            ptime += self.arr[i].time
            if self.arr[i].deadline > ptime:
                temp = self.arr[i].deadline - ptime
                hold += temp * self.arr[i].holding
            else:
                temp = ptime - self.arr[i].deadline
                pen += temp * self.arr[i].penalty
        return hold + pen

    def swap(self, arr, i, j):
        arr[i], arr[j] = arr[j], arr[i]

    def neighbour(self, neighbour, t):
        import random

        n = len(neighbour)
        for i in range(n - 1):
            prob = (i + 1) * (1 / (n - 1))
            b = neighbour[:]
            if prob > random.random():
                self.swap(neighbour, i, i + 1)
                z = abs(self.solve_cost(neighbour) - self.solve_cost(b)) / t
                if self.solve_cost(b) > self.solve_cost(neighbour):
                    break
                elif random.random() < pow(2.71828, -z):
                    break
                else:
                    neighbour[:] = b[:]

    def run(self):
        self.root.mainloop()

    app = AnnealingTkinter()
    app.run()
