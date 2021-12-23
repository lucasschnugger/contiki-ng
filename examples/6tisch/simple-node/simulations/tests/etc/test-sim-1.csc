<?xml version="1.0" encoding="UTF-8"?>
<simconf>
  <project EXPORT="discard">[APPS_DIR]/mrm</project>
  <project EXPORT="discard">[APPS_DIR]/mspsim</project>
  <project EXPORT="discard">[APPS_DIR]/avrora</project>
  <project EXPORT="discard">[APPS_DIR]/serial_socket</project>
  <project EXPORT="discard">[APPS_DIR]/powertracker</project>
  <project EXPORT="discard">[APPS_DIR]/mobility</project>
  <simulation>
    <title>My simulation</title>
    <randomseed>123456</randomseed>
    <motedelay_us>1000000</motedelay_us>
    <radiomedium>
      org.contikios.cooja.radiomediums.UDGM
      <transmitting_range>50.0</transmitting_range>
      <interference_range>100.0</interference_range>
      <success_ratio_tx>1.0</success_ratio_tx>
      <success_ratio_rx>1.0</success_ratio_rx>
    </radiomedium>
    <events>
      <logoutput>40000</logoutput>
    </events>
    <motetype>
      org.contikios.cooja.mspmote.Z1MoteType
      <identifier>z11</identifier>
      <description>Z1 Mote Type #z11</description>
      <source EXPORT="discard">[CONTIKI_DIR]/examples/6tisch/simple-node/node.c</source>
      <commands EXPORT="discard">make node.z1 TARGET=z1</commands>
      <firmware EXPORT="copy">[CONTIKI_DIR]/examples/6tisch/simple-node/node.z1</firmware>
      <moteinterface>org.contikios.cooja.interfaces.Position</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.RimeAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.IPAddress</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.Mote2MoteRelations</moteinterface>
      <moteinterface>org.contikios.cooja.interfaces.MoteAttributes</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspClock</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspMoteID</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspButton</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.Msp802154Radio</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspDefaultSerial</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspLED</moteinterface>
      <moteinterface>org.contikios.cooja.mspmote.interfaces.MspDebugOutput</moteinterface>
    </motetype>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>34.26142233346383</x>
        <y>66.272930556713</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>1</id>
      </interface_config>
      <motetype_identifier>z11</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>58.93401687219831</x>
        <y>38.10025352659975</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>2</id>
      </interface_config>
      <motetype_identifier>z11</motetype_identifier>
    </mote>
    <mote>
      <breakpoints />
      <interface_config>
        org.contikios.cooja.interfaces.Position
        <x>72.38168421270848</x>
        <y>70.68055152068492</y>
        <z>0.0</z>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspClock
        <deviation>1.0</deviation>
      </interface_config>
      <interface_config>
        org.contikios.cooja.mspmote.interfaces.MspMoteID
        <id>3</id>
      </interface_config>
      <motetype_identifier>z11</motetype_identifier>
    </mote>
  </simulation>
  <plugin>
    org.contikios.cooja.plugins.SimControl
    <width>280</width>
    <z>2</z>
    <height>160</height>
    <location_x>400</location_x>
    <location_y>0</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.Visualizer
    <plugin_config>
      <moterelations>true</moterelations>
      <skin>org.contikios.cooja.plugins.skins.IDVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.GridVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.TrafficVisualizerSkin</skin>
      <skin>org.contikios.cooja.plugins.skins.UDGMVisualizerSkin</skin>
      <viewport>2.9371408695788768 0.0 0.0 2.9371408695788768 32.18134591145051 13.902849892633501</viewport>
    </plugin_config>
    <width>400</width>
    <z>1</z>
    <height>400</height>
    <location_x>1</location_x>
    <location_y>1</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.LogListener
    <plugin_config>
      <filter />
      <formatted_time />
      <coloring />
    </plugin_config>
    <width>1258</width>
    <z>3</z>
    <height>773</height>
    <location_x>5</location_x>
    <location_y>406</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.TimeLine
    <plugin_config>
      <mote>0</mote>
      <mote>1</mote>
      <mote>2</mote>
      <showRadioRXTX />
      <showRadioHW />
      <showLEDs />
      <zoomfactor>500.0</zoomfactor>
    </plugin_config>
    <width>1263</width>
    <z>5</z>
    <height>166</height>
    <location_x>0</location_x>
    <location_y>1182</location_y>
  </plugin>
  <plugin>
    org.contikios.cooja.plugins.Notes
    <plugin_config>
      <notes>Enter notes here</notes>
      <decorations>true</decorations>
    </plugin_config>
    <width>583</width>
    <z>4</z>
    <height>160</height>
    <location_x>680</location_x>
    <location_y>0</location_y>
  </plugin>
  <plugin>
    Mobility
    <plugin_config>
      <positions EXPORT="copy">[CONTIKI_DIR]/examples/6tisch/simple-node/position-in.dat</positions>
    </plugin_config>
    <width>500</width>
    <z>0</z>
    <height>200</height>
    <location_x>733</location_x>
    <location_y>175</location_y>
  </plugin>
  <plugin>
		org.contikios.cooja.plugins.ScriptRunner
		<plugin_config>
			<script>
				TIMEOUT(600000, log.log("\nSIMULATION ENDED BY TIMEOUT\n")); /* End simulation after 600,000 ms (10 min.)*/

        var motes = sim.getMotes();
        var mote_count = motes.length;
        var network_size = 0;
        var network_established_time;
        var first_eb_time;
        while(1){
            // time; time of output message
            // mote; current mote
            // id; id of current mote
            // msg; current output message from mote

            // if output message contains results from simulation
            if (msg.contains("SIM:")){
                if (msg.contains("disassociated")){ // if mote disassociated
                    network_size--;
                }else if(msg.contains("associated")){ // if mote associated
                    network_size++;
                    if (network_size == mote_count-1){ // if all but one mote associated
                        network_established_time = time;
                        log.log(time + ": " + " Network created with " + network_size + " motes.\n");
                    }
                }

                if (msg.contains("discovered motes")){ // if a mote associated, how many motes were discovered
                    var msgTrimmed = msg.split("SIM:")[1];
                    var reg = new RegExp(".*(\\d).*(\\d).*");
                    var matches = reg.exec(msgTrimmed);
                    var moteId = parseInt(matches[1]);
                    var discoveredMotes = parseInt(matches[2]);
                    log.log(time + ": Mote " + moteId + " discovered " + discoveredMotes + " motes before associating.\n");
                    if(moteId == mote_count){ //Always highest ID mote joining last
                        log.log("Network established time: "+network_established_time+
                            ". First EB time: "+first_eb_time+
                            ". Join time: " + time +
                            ". Parents considered: " + discoveredMotes +".\n"
                        );
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
                        log.log(time + ": " + "Mote " + moteId + " found first EB from mote " + ebSrcMoteId + ".\n");
                        if(moteId == mote_count){
                            first_eb_time = time;
                        }
                    }
                }
            }
            YIELD(); // wait for next mote output message
        }

        log.testOK();
			</script>
			<active>true</active>
		</plugin_config>
	</plugin>
</simconf>

