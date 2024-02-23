import random
import math

# random.seed(42)


class Job:
    def __init__(self, id, time, deadline, holding, penalty):
        self.id = id
        self.time = time
        self.deadline = deadline
        self.holding = holding
        self.penalty = penalty

    def __str__(self):
        return f"ID: {self.id:2d}\tTime: {self.time:2d}\tHolding: {self.holding:2d}\tDeadline: {self.deadline:2d}\tPenalty: {self.penalty:2d}"


class SolveJob(Job):
    def __init__(self, id, time, deadline, holding, penalty):
        super().__init__(id, time, deadline, holding, penalty)

    def solve(arr, seq):
        pen = 0
        hold = 0
        ptime = 0
        for i in range(len(arr)):
            ptime = ptime + arr[seq[i]].time
            if arr[seq[i]].deadline > ptime:
                temp = arr[seq[i]].deadline - ptime
                hold = hold + (temp * arr[seq[i]].holding)
            else:
                temp = ptime - arr[seq[i]].deadline
                pen = pen + (temp * arr[seq[i]].penalty)
        return hold + pen

    # to swap diffrent combinations

    def neighbor(neighbour, arr, t):
        rand = random.random()
        n = len(arr)
        for i in range(n - 1):
            prob = (i + 1) * (1 / (n - 1))
            b = neighbour.copy()
            if prob > rand:
                neighbour[i + 1], neighbour[i] = neighbour[i], neighbour[i + 1]
                z = abs(SolveJob.solve(arr, neighbour) - SolveJob.solve(arr, b)) / t
                if SolveJob.solve(arr, b) > SolveJob.solve(arr, neighbour):
                    # print(f"Accepted : {SolveJob.solve(arr, neighbour)}")
                    break
                elif random.random() < math.exp(-z):  # check for down grading
                    # print(f"Accepted : {SolveJob.solve(arr, neighbour)}")
                    break
                else:
                    # print(f"\tRejected : {SolveJob.solve(arr, neighbour)}")
                    neighbour = b.copy()


def main():
    print("Hello")
    arr = []
    n = 0
    print("1. Manual Input  \t 2. Automatic input")
    no = int(input())
    if no == 1:
        print("Enter number of Jobs to Schedule : ")
        n = int(input())
        for i in range(1, n + 1):
            time = int(input(f"Enter Time for Job {i}: "))
            deadline = int(input(f"Enter Deadline for Job {i}: "))
            holding = int(input(f"Enter Holding cost for Job {i}: "))
            penalty = int(input(f"Enter Penalty for Job {i}: "))
            arr.append(SolveJob(i, time, deadline, holding, penalty))
    else:
        arr.append(SolveJob(1, 10, 15, 3, 10))
        arr.append(SolveJob(2, 8, 20, 2, 22))
        arr.append(SolveJob(3, 6, 10, 5, 10))
        arr.append(SolveJob(4, 7, 30, 4, 8))
    n = len(arr)
    neighbour = list(range(n))
    min_cost = SolveJob.solve(arr, neighbour)
    print(f"Current cost: {min_cost}")
    t = 1000
    c = 0.9
    result = neighbour.copy()

    while t > 1.0:
        SolveJob.neighbor(neighbour, arr, t)
        temp = SolveJob.solve(arr, neighbour)
        t *= c
        if temp < min_cost:
            min_cost = temp
            result = neighbour.copy()
    for i in range(n):
        print(arr[result[i]])

    print(f"Total Cost required: {SolveJob.solve(arr, result)}")


main()
