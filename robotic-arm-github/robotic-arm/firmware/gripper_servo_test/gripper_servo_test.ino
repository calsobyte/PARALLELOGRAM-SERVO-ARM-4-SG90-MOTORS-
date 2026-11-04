/*
  Gripper servo test: find the open and closed angles.
  Wire the gripper servo signal to D9, power the servo from the external 5 V supply
  (common ground with the Arduino). Open the Serial Monitor at 9600 baud, type an
  angle (0-180) and press Enter. Note the angle where the jaws just close on the foam
  pads (closed) and the angle where the jaw is fully open. Never go past either.
*/
#include <Servo.h>

Servo grip;

void setup() {
  Serial.begin(9600);
  grip.write(90);
  grip.attach(9);
  Serial.println(F("Type an angle (0-180) and press Enter."));
}

void loop() {
  if (Serial.available()) {
    int a = Serial.parseInt();
    if (a >= 0 && a <= 180) {
      grip.write(a);
      Serial.print(F("Angle: ")); Serial.println(a);
    }
    while (Serial.available()) Serial.read();   // clear the line ending
  }
}
