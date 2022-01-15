TIMEOUT(600000, log.log("\nSIMULATION ENDED BY TIMEOUT\n")); // End simulation after 600,000 ms (10 min.)

var motes = sim.getMotes();
var mote_count = motes.length;
var network_size = 1;
var disassociated = false;
var reassociated = false;
var reassociate_time;
var parents_considered = 0;


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


while(1) {
    // time; time of output message
    // mote; current mote
    // id; id of current mote
    // msg; current output message from mote

    // if test failed due to various reasons --> stop test
    if (msg.contains("left network") && parseInt(msg.split("node ")[1].split(" as left network")[0]) !== mote_count){
        log.log("Test failed because a static mote crashed and was marked as left network.\n");
        log.testFailed();
    }

    //If join phase
    if(us_to_seconds(time) < 3*60){
        //Ensure all nodes joined network
        if (msg.contains("SIM:")) {
            if (msg.contains("disassociated")) { // if mote disassociated
                network_size--;
                log.log(us_to_second_string(time) + ": Mote " + id + " disassociated.\n");
            } else if (msg.contains("associated")) { // if mote associated
                network_size++;
                log.log(us_to_second_string(time) + ": Mote " + id + " associated.\n");
            }
        }
    }
    //if leave phase
    else if(us_to_seconds(time) < (3+2.5)*60){
        //If all nodes not on network, abort
        if (network_size !== mote_count){
            log.log("Test failed because all motes had not joined the network after 3 minutes.\n");
            log.testFailed();
        }
        if (msg.contains("SIM: Mote="+mote_count+" disassociated")){
            disassociated = true;
            log.log(us_to_second_string(time) + ": Mobile Mote " + id + " disassociated.\n");
        }
    }
    //If rejoin phase
    else{
        if(!disassociated){
            log.log("Test failed because mobile mote had not disassociated after 5.5 minutes.\n");
            log.testFailed();
        }
        if(msg.contains("SIM: Mote="+mote_count+" associated")){
            log.log(us_to_second_string(time) + ": Mobile Mote " + id + " reassociated.\n");
            reassociate_time = time;
            reassociated = true;
        }
        if (msg.contains("discovered motes") && msg.contains("SIM: Mote="+mote_count)) { // if mote re-associated, how many motes were discovered
            var msgTrimmed = msg.split("SIM:")[1];
            var reg = new RegExp(".*(\\d).*(\\d).*");
            var matches = reg.exec(msgTrimmed);
            var moteId = parseInt(matches[1]);
            var discoveredMotes = parseInt(matches[2]);
            parents_considered = discoveredMotes;
        }
        if (reassociated && parents_considered > 0){
            log.log("Test summary:\n" +
                "Mobile node reassociated to the network at: " + us_to_second_string(reassociate_time) + "\n" +
                "Mobile node at reassociate considered parents: " + parents_considered + "\n"
            );
            log.log("Rejoin:" +
                us_to_second_string(reassociate_time) +
                "," + parents_considered +
                "\n");
            log.testOK();
        }
    }

    YIELD(); // wait for next mote output message
}

log.testOK();
