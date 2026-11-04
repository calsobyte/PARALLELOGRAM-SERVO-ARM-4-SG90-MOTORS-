/*
  U can use this to find the grippers max angle. I decided to just let it open and close to the max since I manually callibrated the servo for the 0 to be pararell to the static part of the gripper)
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
