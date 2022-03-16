#include <SPI.h>
#include <ESP_AVRISP.h>
#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>

const char* host = "esp-avrisp";
const char* ssid = "...........";
const char* pass = "...........";
const uint16_t port = 3000;
const uint8_t reset_pin = 5;

ESP_AVRISP avrprog(port, reset_pin);

void setup() {
    // Serial.begin(9600);
    // Serial.println("");
    // Serial.println("Arduino AVR-ISP over TCP");
    avrprog.setReset(false); // let the AVR run

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, pass);
    while (WiFi.waitForConnectResult() != WL_CONNECTED);

    MDNS.begin(host);
    MDNS.addService("avrisp", "tcp", port);

    IPAddress local_ip = WiFi.localIP();
    // Serial.print("IP address: ");
    // Serial.println(local_ip);
    // Serial.println("Use your avrdude:");
    // Serial.print("avrdude -c arduino -p <device> -P net:");
    // Serial.print(local_ip);
    // Serial.print(":");
    // Serial.print(port);
    // Serial.println(" -t # or -U ...");

    // listen for avrdudes
    avrprog.begin();
    ArduinoOTA.begin();
}

void loop() {
    ArduinoOTA.handle();
    static AVRISPState_t last_state = AVRISP_STATE_IDLE;
    AVRISPState_t new_state = avrprog.update();
    if (last_state != new_state) {
        switch (new_state) {
            case AVRISP_STATE_IDLE: {
                // Serial.printf("[AVRISP] now idle\r\n");
                // Use the SPI bus for other purposes
                break;
            }
            case AVRISP_STATE_PENDING: {
                // Serial.printf("[AVRISP] connection pending\r\n");
                // Clean up your other purposes and prepare for programming mode
                break;
            }
            case AVRISP_STATE_ACTIVE: {
                // Serial.printf("[AVRISP] programming mode\r\n");
                // Stand by for completion
                break;
            }
        }
        last_state = new_state;
    }
    // Serve the client
    if (last_state != AVRISP_STATE_IDLE) {
        avrprog.serve();
    }
}
