import random
import time

starttime = time.time()


class Job:
    def __init__(self, id, time, deadline, holding, penalty):
        self.id = id
        self.time = time
        self.deadline = deadline
        self.holding = holding
        self.penalty = penalty

    def __str__(self):
        return f"ID: {self.id:2d}\tTime: {self.time:2d}\tHolding: {self.holding:2d}\tDeadline: {self.deadline:2d}\tPenalty: {self.penalty:2d}"


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


def mutate(temp1, temp2):
    length = len(temp1)
    one = 0
    two = 0
    for i in range(2):
        one = random.randint(0, length - 1)
        while True:
            two = random.randint(0, length - 1)
            if one != two:
                break
        if i == 0:
            temp1[two], temp1[one] = temp1[one], temp1[two]
        else:
            temp2[two], temp2[one] = temp2[one], temp2[two]
    return temp1, temp2


def genetic(arr, l2):
    column = len(l2[0])
    row = len(l2)
    best = l2[0][1:]
    randomIndex = random.randint(1, row - 1)
    randomValue = l2[randomIndex][1:]
    crossoverPoint = random.randint(1, column - 3)

    temp1 = best[:crossoverPoint]
    temp2 = randomValue[:crossoverPoint]
    new1 = [item for item in randomValue if item not in temp1]
    new2 = [item for item in best if item not in temp2]
    temp1 = temp1 + new1
    temp2 = temp2 + new2

    if random.random() > 0.5:
        temp1, temp2 = mutate(temp1, temp2)
    temp1.insert(0, solve(arr, temp1))
    temp2.insert(0, solve(arr, temp2))

    if temp1 not in l2:
        l2.append(temp1)
    if temp2 not in l2:
        l2.append(temp2)
    l2 = sorted(l2)
    reduceby = len(l2) - row
    if reduceby == 0:
        return l2
    return l2[:-reduceby]




def execute(arr):
    l2 = []
    l1 = list(range(0, len(arr)))
    # l1 = [0, 1, 2, 3, 4]
    for i in range(len(l1)):
        random.shuffle(l1)
        l3 = list(l1)
        l3.insert(0, solve(arr, l3))
        l2.append(l3)
    l2 = sorted(l2)
    for i in range(40000):
        l2 = genetic(arr, l2)
        # print("Best Solution is ", l2[0][0])

    seq = l2[0][1:]
    # for i in range(len(seq)):
    #     print(arr[seq[i]])
    # print(f"Timetaken = {time.time()-starttime} seconds")
    return seq
    

def main():
    print("Hello")
    arr = []
    arr.append(Job(1, 10, 15, 3, 10))
    arr.append(Job(2, 8, 20, 2, 22))
    arr.append(Job(3, 6, 10, 5, 10))
    arr.append(Job(4, 7, 30, 4, 8))
    arr.append(Job(5, 4, 12, 6, 15))
    random.seed(42)
    l2 = []
    l1 = list(range(0, len(arr)))
    print(solve(arr, l1))
    # l1 = [0, 1, 2, 3, 4]
    for i in range(len(l1)):
        random.shuffle(l1)
        l3 = list(l1)
        l3.insert(0, solve(arr, l3))
        l2.append(l3)
    l2 = sorted(l2)
    for i in range(40000):
        l2 = genetic(arr, l2)
        # print("Best Solution is ", l2[0][0])

    print("Best Solution is ", l2[0][0])
    seq = l2[0][1:]
    for i in range(len(seq)):
        print(arr[seq[i]])
    print(f"Timetaken = {time.time()-starttime} seconds")


if __name__ == "__main__":
    main()
