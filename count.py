import csv
fails = 0
with open("output.txt") as f:
    reader = csv.reader(f)
    for row in reader:
        for item in row:
            if item == "Case":
                fails += 1
print(fails)