import random

with open("source.txt", "w") as f:
    a = [str(i) + "\n" for i in range(1, 100)]
    random.shuffle(a)
    f.writelines(a)