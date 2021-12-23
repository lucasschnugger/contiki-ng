import os, time, shutil


def run_test(cooja, dir, test, seed):
    # run test simulation with seed
    command = f"java -jar {cooja} -nogui={dir}{test} -random-seed={seed}"
    os.system(command)


def remove_command_in_test(dir, test):
    file = f"{dir}{test}"
    from xml.etree import cElementTree as ET
    root = ET.parse(file)
    for element in root.iter():
        for subelement in element:
            if subelement.tag == "commands":
                element.remove(subelement)
    root.write(file)


def update_firmware_in_test(dir, test, firmware):
    file = f"{dir}{test}"
    from xml.etree import cElementTree as ET
    root = ET.parse(file)
    for element in root.iter():
        for subelement in element:
            if subelement.tag == "firmware":
                subelement.text = f"[CONTIKI_DIR]/examples/6tisch/simple-node/{firmware}"
    root.write(file)


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

seeds = [123456, 123458, 123459]
seeds.sort()
firmwares = ["node.z1", "node-classic.z1"]
tests = [f for f in os.listdir(tests_dir) if os.path.isfile(f"{tests_dir}{f}")]
tests.sort()

os.chdir(run_dir)  # change working directory to run_dir

for test in tests:  # run each test from tests_dir
    shutil.copy(f"{tests_dir}{test}", f"{run_dir}{test}")  # copy test to run_dir

    for seed in seeds:  # run test with each seed

        for firmware in firmwares:  # run test with every firmware
            remove_command_in_test(run_dir, test)  # remove commands in simulation test file
            update_firmware_in_test(run_dir, test, firmware)  # change firmware in file
            print(f"\n\n ########### Now running test '{test}' with firmware '{firmware}' and seed '{seed}' ##############\n")
            run_test(cooja_jar, run_dir, test, seed)  # run simulation with seed
            os.rename(f"{run_dir}COOJA.testlog", f"{log_dir}{test.split('.')[0]}_{firmware.split('.')[0]}_{seed}.testlog")  # move simulation result log
            time.sleep(1)

    os.remove(f"{run_dir}{test}")  # delete test from run_dir
