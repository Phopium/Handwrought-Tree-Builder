letter = "b"
first = '{"id": "'
second = '", "name": "Blank", "description": "Blank", "position": ['
third = '], "connections": []},'
x = 0
y = 0

for i in range(30):
    print(f"{first}{letter}{i}{second}{x},{y}{third}")
    y += 1
    if y == 5:
        y = 0
        x += 1
