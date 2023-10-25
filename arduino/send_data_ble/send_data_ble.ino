#include <ArduinoBLE.h>

BLEService simpleService("180D");  // BLE Service
BLEIntCharacteristic simpleCharacteristic("2A37",  // UUID for Simple Characteristic
                                          BLERead | BLENotify);  // properties

// reads in value from A0, sends 10 bit over bluetooth

// Variables
const int analogPin = A0; // Analog pin to read
int sensorValue = 0.0;

void setup() {
  if (!BLE.begin()) {
    while (1);
  }

  BLE.setLocalName("NanoRP2040");  // Set name for connection
  BLE.setAdvertisedService(simpleService);  // Advertise our service
  simpleService.addCharacteristic(simpleCharacteristic);
  BLE.addService(simpleService);  // Add service
  simpleCharacteristic.writeValue(sensorValue);  // Set initial value for characteristic

  BLE.advertise();  // Start advertising
}

void loop() {
  BLEDevice central = BLE.central();  // Wait for a BLE central

  if (central) {
    while (central.connected()) {
      sensorValue = analogRead(analogPin);
      simpleCharacteristic.writeValue(sensorValue);
    }
  }}
