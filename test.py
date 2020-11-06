from random import random

print("Hello world")

num_experts = 15
exeprt_fail_chance = 0.40
num_right_experts = 0

for i in range(10000):
    num_right = 0
    for j in range(num_experts):
        if random() > exeprt_fail_chance:
            num_right += 1
    if num_right > num_experts//2:
        num_right_experts += 1

print(num_right_experts/10000.0)
