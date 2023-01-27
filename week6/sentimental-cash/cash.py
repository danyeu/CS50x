from cs50 import get_float

while True:
    cash = get_float("Change owed: ")
    if cash >= 0:
        break

counter = 0
intcash = int(100 * cash)
for coins in [25, 10, 5, 1]:
    while intcash >= coins:
        counter += 1
        intcash += -coins

print(counter)