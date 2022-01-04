import os, time, shutil, random, re
from xml.etree import cElementTree as ET


def run_test(cooja, dir, test, seed):
    # run test simulation with seed
    command = f"java -jar {cooja} -nogui={dir}{test} -random-seed={seed}"
    os.system(command)


def remove_command_in_test(dir, test):
    file = f"{dir}{test}"
    root = ET.parse(file)
    for element in root.iter():
        for subelement in element:
            if subelement.tag == "commands":
                element.remove(subelement)
    root.write(file)


def update_firmware_in_test(dir, test, firmware_network, firmware_joining):
    file = f"{dir}{test}"
    root = ET.parse(file)
    for element in root.iter():
        if element.tag == "motetype":
            motetype = ""
            for subelement in element:
                if subelement.tag == "identifier":
                    motetype = subelement.text
            for subelement in element:
                if subelement.tag == "firmware":
                    firmware = firmware_joining if motetype == "z1-joining-node" else firmware_network
                    subelement.text = f"[CONTIKI_DIR]/examples/6tisch/simple-node/{firmware}"
    root.write(file)


def add_scriptrunner_in_test(dir, test):
    file = f"{dir}{test}"
    scriptrunner = ""
    if test.startswith("join-"):
        scriptrunner = open(f"{scripts_dir}join.js").read()
    elif test.startswith("create-"):
        scriptrunner = open(f"{scripts_dir}create.js").read()
    root = ET.parse(file)
    for element in root.iter():
        if element.tag == "simconf":
            plugin = ET.Element("plugin")
            plugin.text = "org.contikios.cooja.plugins.ScriptRunner"
            conf = ET.Element("plugin_config")
            script = ET.Element("script")
            script.text = scriptrunner
            active = ET.Element("active")
            active.text = "true"
            conf.append(script)
            conf.append(active)
            plugin.append(conf)
            element.append(plugin)
    root.write(file)


def add_mobility_in_test(dir, test):
    file = f"{dir}{test}"
    root = ET.parse(file)
    for element in root.iter():
        if element.tag == "simconf":
            plugin = ET.Element("plugin")
            plugin.text = "Mobility"
            conf = ET.Element("plugin_config")
            positions = ET.Element("positions")
            positions.set("EXPORT", "copy")
            positions.text = f"[CONTIKI_DIR]/examples/6tisch/simple-node/simulations/positions/{test.replace('.csc', '.dat')}"
            conf.append(positions)
            plugin.append(conf)
            element.append(plugin)
    root.write(file)


def check_if_test_successful(test_output_file_path):
    f = open(test_output_file_path, "r")
    test_output = f.read()
    if("TEST FAILED" in test_output):
        print("##### Test failed: 'TEST FAILED' found  #####")
        return False
    if("TEST OK" not in test_output):
        print("##### Test failed: 'TEST OK' not found  #####")
        return False
    if("Network created with " not in test_output):
        print("##### Test failed: network not established  #####")
        return False

    # network_established_time = float(test_output.split("Network established time: ")[1].split(". First")[0])
    # first_eb_time = float(test_output.split("First EB time: ")[1].split(". Join")[0])
    # join_time = float(test_output.split("Join time:")[1].split(". Parents")[0])
    # parents_considered = int(test_output.split("Parents considered: ")[1].split(".\n")[0])
    #
    # if join_time >= network_established_time: #if joining EB joins before network is completely established
    #     print("##### Test failed: Joining node finishes network #####")
    #     return False

    return True


def add_testlog_parameters_csv(seed, test, firmware, test_output_file_path):
    test_params = test.split(".")[0].split("-")
    nodes = test_params[2]
    topology = test_params[1]
    firmware_params = firmware.split(".")[0].split("-")
    tsch_version = firmware_params[1]
    channels = re.sub("[^0-9]", "", firmware_params[2])
    assoc_timeout = re.sub("[^0-9]", "", firmware_params[3])
    csv_result = [seed, nodes, channels, topology, tsch_version, assoc_timeout]
    csv_result_str = ",".join([str(elem) for elem in csv_result])
    file = open(test_output_file_path, "r")
    new_file_content = ""
    for line in file:
        if "," in line:
            new_file_content += f"{csv_result_str},{line}"
        else:
            new_file_content += line
    file.close()
    file = open(test_output_file_path, "w")
    file.write(new_file_content)
    file.close()


def add_testlog_firmwares(firmware_network, firmware_joining, test_output_file_path):
    file = open(test_output_file_path, "r")
    content = file.read()
    file.close()
    new_file_content = f"z1-network-node firmware: {firmware_network}\n" + f"z1-joining-node firmware: {firmware_joining}\n" + content
    file = open(test_output_file_path, "w")
    file.write(new_file_content)
    file.close()


if os.path.isdir("/home/user/"):
    cooja_jar = "/home/user/contiki-ng/tools/cooja/dist/cooja.jar"
    run_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/"
    sim_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/simulations/"
    tests_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/simulations/tests/"
    scripts_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/simulations/scriptrunners/"
    pos_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/simulations/positions/"
    log_dir = "/home/user/contiki-ng/examples/6tisch/simple-node/simulations/logs/"
if not os.path.isdir(tests_dir):
    os.mkdir(tests_dir)
if not os.path.isdir(scripts_dir):
    os.mkdir(scripts_dir)
if not os.path.isdir(pos_dir):
    os.mkdir(pos_dir)
if not os.path.isdir(log_dir):
    os.mkdir(log_dir)

# seeds = [15557,65890,237601,268521,537634,571714,881378,928542,963159,978437]
seeds = random.sample(range(0,999999), 15) # 15 random seeds
seeds.sort()
firmwares = [
    {"joining": "node-custom-4c-16s.z1", "network": "node-network-4c.z1"},
    {"joining": "node-custom-8c-16s.z1", "network": "node-network-8c.z1"},
    {"joining": "node-custom-12c-16s.z1", "network": "node-network-12c.z1"},
    {"joining": "node-custom-16c-16s.z1", "network": "node-network-16c.z1"},
    {"joining": "node-classic-4c-16s.z1", "network": "node-network-4c.z1"},
    {"joining": "node-classic-8c-16s.z1", "network": "node-network-8c.z1"},
    {"joining": "node-classic-12c-16s.z1", "network": "node-network-12c.z1"},
    {"joining": "node-classic-16c-16s.z1", "network": "node-network-16c.z1"}
]
tests = [f for f in os.listdir(tests_dir) if os.path.isfile(f"{tests_dir}{f}")]
tests.sort()

print("")
print(f"Running tests {tests}.")
print(f"Running tests on firmwares {firmwares}.")
print(f"Running tests on seeds {seeds}.")

os.chdir(run_dir)  # change working directory to run_dir

for test in tests:  # run each test from tests_dir

    for seed in seeds:  # run test with each seed

        for firmware in firmwares:  # run test with every firmware
            shutil.copy(f"{tests_dir}{test}", f"{run_dir}{test}")  # copy test to run_dir
            remove_command_in_test(run_dir, test)  # remove commands in simulation test file
            update_firmware_in_test(run_dir, test, firmware["network"], firmware["joining"])  # change firmware in file
            add_mobility_in_test(run_dir, test)  # add mobility file to test
            add_scriptrunner_in_test(run_dir, test)  # add scriptrunner to test for extraction of data and controlling test
            print(f"\n\n ########### Now running test '{test}' with firmware '{firmware}' and seed '{seed}' ##############\n")
            run_test(cooja_jar, run_dir, test, seed)  # run simulation with seed
            local_seed = seed
            while not check_if_test_successful(f"{run_dir}COOJA.testlog"):  # evaluate if test is OK
                local_seed = random.randint(0,999999)
                run_test(cooja_jar, run_dir, test, local_seed)
            add_testlog_parameters_csv(local_seed, test, firmware["joining"], f"{run_dir}COOJA.testlog")  # add test parameters to csv line in file
            add_testlog_firmwares(firmware["network"], firmware["joining"], f"{run_dir}COOJA.testlog")  # add node firmwares used to top of file
            os.rename(f"{run_dir}COOJA.testlog", f"{log_dir}{test.split('.')[0]}_{firmware['joining'].split('.')[0]}_{local_seed}.testlog")  # move simulation result log
            os.remove(f"{run_dir}{test}")  # delete test from run_dir
            time.sleep(1)
