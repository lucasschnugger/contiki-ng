TIMEOUT(600000, log.log("\nSIMULATION ENDED BY TIMEOUT\n")); // End simulation after 600,000 ms (10 min.)

var motes = sim.getMotes();
var mote_count = motes.length;
var network_size = 1;
var network_established_time;
var first_eb_time;


function us_to_seconds(us){
    return Math.floor(us/(1000*1000));
}

function us_to_second_string(us){
    var remainder = us;
    var seconds = Math.floor(remainder/(1000*1000));
    remainder = remainder % 1000000;
    var milliseconds = Math.floor(remainder/1000);
    return seconds+"."+milliseconds;
}

function extract_powertracker_stats(plugin){
    if (plugin != null){
        stats = plugin.radioStatistics();

        var max_id = 0;
        var reg = new RegExp("Z1_(\\d)", "gi");
        stats.match(reg).forEach(function(node) {
            reg = new RegExp("Z1_(\\d)", "i");
            var id = parseInt(reg.exec(node)[1]);
            if (id > max_id){
                max_id = id;
            }
        });
        var node_id = "Z1_" + max_id.toString();

        var joining_node_stats = [];
        stats.split("\n").forEach(function(line) {
            if (line.indexOf(node_id) !== -1){
                joining_node_stats.push(line);
            }
        });

        var csv_stats = [];
        joining_node_stats.forEach(function(line) {
            if (line.indexOf(node_id) !== -1) {
                if (line.indexOf("MONITORED") !== -1) {
                    csv_stats.push(us_to_second_string(parseInt(line.split(" ")[2])));  // add time monitored in seconds
                } else {
                    line_arr = line.split(" ");
                    csv_stats.push(us_to_second_string(parseInt(line_arr[2])));  // add time monitored in seconds
                    csv_stats.push(parseFloat(line_arr[4]));  // add percentage of time spent in mode [ON, TX, RX, INT]
                }
            }
        })

        var csv_stats_str = "";
        csv_stats.forEach(function(stat) {
           csv_stats_str += stat + ",";
        });
        csv_stats_str = csv_stats_str.slice(0,-1);
        log.log("Power:" + csv_stats_str + "\n");
    } else {
        log.log("No PowerTracker plugin.\n");
    }
}

while(1){
    // time; time of output message
    // mote; current mote
    // id; id of current mote
    // msg; current output message from mote

    power_plugin = mote.getSimulation().getCooja().getStartedPlugin("PowerTracker");
    if (power_plugin != null && us_to_seconds(time) < 180){
        power_plugin.reset();
    }

    // if test failed due to various reasons --> stop test
    if (msg.contains("left network")){
        log.testFailed();
    }

    // if output message contains results from simulation
    if (msg.contains("SIM:")){
        if (msg.contains("disassociated")){ // if mote disassociated
            network_size--;
        }else if(msg.contains("associated")){ // if mote associated
            network_size++;
            if (network_size == mote_count-1){ // if all but one mote associated
                network_established_time = time;
                log.log(us_to_second_string(time) + ": " + " Network created with " + network_size + " motes.\n");
            }
        }

        if (msg.contains("discovered motes")){ // if a mote associated, how many motes were discovered
            var msgTrimmed = msg.split("SIM:")[1];
            var reg = new RegExp(".*(\\d).*(\\d).*");
            var matches = reg.exec(msgTrimmed);
            var moteId = parseInt(matches[1]);
            var discoveredMotes = parseInt(matches[2]);
            log.log(us_to_second_string(time) + ": Mote " + moteId + " discovered " + discoveredMotes + " motes before associating.\n");
            if(moteId == mote_count){ //Always highest ID mote joining last
                log.log("Network established time: "+us_to_second_string(network_established_time) +
                    ". First EB time: "+us_to_second_string(first_eb_time)+
                    ". Join time: " + us_to_second_string(time) +
                    ". Parents considered: " + discoveredMotes +".\n"
                );
                log.log("Join:" + us_to_second_string(network_established_time) +
                        "," + us_to_second_string(first_eb_time) +
                        "," + us_to_second_string(time) +
                        "," + discoveredMotes + "\n");
                extract_powertracker_stats(power_plugin);
                log.testOK();
            }
        }

        if (msg.contains("discovered EB")){
            var msgTrimmed = msg.split("SIM:")[1];
            var reg = new RegExp(".*(\\d).*(\\d).*(\\d).*");
            var matches = reg.exec(msgTrimmed);
            var moteId = parseInt(matches[1]);
            var discoveredMotes = parseInt(matches[2]);
            var ebSrcMoteId = parseInt(matches[3]);
            if (discoveredMotes == 1){
                log.log(us_to_second_string(time) + ": " + "Mote " + moteId + " found first EB from mote " + ebSrcMoteId + ".\n");
                if(moteId == mote_count){
                    first_eb_time = time;
                }
            }
        }
    }
    YIELD(); // wait for next mote output message
}

log.testOK();
