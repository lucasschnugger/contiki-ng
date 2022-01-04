import os

if os.path.isdir("/home/user/"):
    log_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/simulations/logs/"
elif os.path.isdir("/Users/Lucas/"):
    log_dir = "/Users/Lucas/Documents/Projects/contiki-ng-fork/examples/6tisch/simple-node/simulations/logs/"

logs = [f for f in os.listdir(log_dir) if os.path.isfile(f"{log_dir}{f}")]

csv_lines = []

for log in logs:
    with open(f"{log_dir}{log}", "r") as file:
        for line in file:
            if "," in line:
                csv_lines.append(line)

csv_lines_str = "".join(csv_lines)
print(csv_lines_str)
