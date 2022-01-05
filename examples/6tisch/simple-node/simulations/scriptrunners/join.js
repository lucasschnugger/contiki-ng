TIMEOUT(600000, log.log("\nSIMULATION ENDED BY TIMEOUT\n")); // End simulation after 600,000 ms (10 min.)

var motes = sim.getMotes();
var mote_count = motes.length;
var network_size = 1;
var network_established_time;
var first_eb_time;

function us_to_second_string(us){
    var remainder = us;
    var seconds = Math.floor(remainder/(1000*1000));
    remainder = remainder % 1000000;
    var milliseconds = Math.floor(remainder/1000);
    return seconds+"."+milliseconds;
}

while(1){
    // time; time of output message
    // mote; current mote
    // id; id of current mote
    // msg; current output message from mote

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
                log.log(us_to_second_string(network_established_time) +
                        "," + us_to_second_string(first_eb_time) +
                        "," + us_to_second_string(time) +
                        "," + discoveredMotes + "\n");
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
