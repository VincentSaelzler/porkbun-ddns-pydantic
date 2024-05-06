import os
from datetime import datetime

now = datetime.now().isoformat()
aye = os.environ['A']
bee = os.environ['B']

line = f"{now}-{aye}-{bee}"
print(line)

with open("t.txt", "a") as file:
    file.write(line)
    file.write("\n")
