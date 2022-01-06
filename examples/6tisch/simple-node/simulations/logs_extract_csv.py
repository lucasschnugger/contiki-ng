import os

if os.path.isdir("/home/user/"):
    log_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/simulations/logs/"
    output_file = "/home/user/data.csv"
elif os.path.isdir("/Users/Lucas/"):
    log_dir = "/Users/Lucas/Documents/Projects/contiki-ng-fork/examples/6tisch/simple-node/simulations/logs/"
    output_file = "/Users/Lucas/Downloads/data.csv"

logs = [f for f in os.listdir(log_dir) if os.path.isfile(f"{log_dir}{f}")]
logs.sort()

csv_lines = []

for log in logs:
    with open(f"{log_dir}{log}", "r") as file:
        for line in file:
            if "," in line:
                csv_lines.append(line)

csv_lines_str = "".join(csv_lines)
file = open(output_file, "w")
file.write(csv_lines_str)
file.close()
# print(csv_lines_str)
