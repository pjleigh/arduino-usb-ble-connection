// reads in value from A0, converts 0-1023 value from ADC to 0-255, sends 1 byte int over serial

// Variables
const int readPin = A0;
float outputvalue = 0.0;
const int baudrate = 9600; // Serial communication rate

void setup() {
  Serial.begin(baudrate);
  pinMode(readPin, INPUT);
}

void loop() {
  int readvalue = analogRead(readPin);
  outputvalue = map(readvalue, 0, 1023, 0, 255);

  Serial.write((int)outputvalue);
}
