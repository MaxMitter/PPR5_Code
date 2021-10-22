# -*- coding: utf-8 -*-

doors = [False] * 100    

for i in range(100):
    for j in range(100):
        if (i + 1) % (j + 1) == 0:
            doors[i] = not doors[i]

#print(doors)

n = 1
while n <= 100:
    #print("Door Nr." + str(n) + " is " + str(doors[n - 1]))
    print(f"Door Nr. {n} is {doors[n - 1]}")
    n += 1

opened = 0
closed = 0

for i in doors:
    if i:
        opened += 1
    else:
        closed += 1

print("opened: " + str(opened))
print("closed: " + str(closed))

efficientDoors = [False] * 100

for x in range(100):
    for y in range(x, 100, x + 1):
        efficientDoors[y] = not efficientDoors[y]
    print(f"Doors {x + 1} open? {efficientDoors[x]}")
    
for door in range(100):
    if (door + 1) ** 0.5 % 1 == 0:
        doors[door] = True
    print(f"Doors {door + 1} open? {doors[door]}")