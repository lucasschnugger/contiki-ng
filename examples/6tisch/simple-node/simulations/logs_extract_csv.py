import os

if os.path.isdir("/home/user/"):
    log_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/simulations/logs/"
    output_file_join = "/home/user/join-data.csv"
    output_file_power = "/home/user/power-data.csv"
elif os.path.isdir("/Users/Lucas/"):
    log_dir = "/Users/Lucas/Documents/Projects/contiki-ng-fork/examples/6tisch/simple-node/simulations/logs/"
    output_file_join = "/Users/Lucas/Downloads/join-data.csv"
    output_file_power = "/Users/Lucas/Downloads/power-data.csv"

logs = [f for f in os.listdir(log_dir) if os.path.isfile(f"{log_dir}{f}")]
logs.sort()

csv_lines_join = []
csv_lines_power = []

for log in logs:
    with open(f"{log_dir}{log}", "r") as file:
        for line in file:
            if "," in line:
                if "Join:" in line:
                    csv_lines_join.append(line.replace("Join:", ""))
                elif "Power:" in line:
                    csv_lines_power.append(line.replace("Power:", ""))
                else:
                    csv_lines_join.append(line)

csv_lines_join_str = "".join(csv_lines_join)
csv_lines_power_str = "".join(csv_lines_power)
file = open(output_file_join, "w")
file.write(csv_lines_join_str)
file.close()
file = open(output_file_power, "w")
file.write(csv_lines_power_str)
file.close()
# print(csv_lines_str)
