//MAIN CODE FOR THE ARM. YOU CAN EDIT THE STARTING ANGLES AND LIMITS AS FITS. I DECIDED TO USE VARIABLES TO MAKE IT EASIER TO ADJUST AND CALLIBRATE)

#include <Servo.h>

Servo shoulderServo;
Servo elbowServo;
Servo gripperServo;
Servo baseServo;

// Servo pins
const int shoulderPin = 5;
const int elbowPin = 6;
const int gripperPin = 9;
const int basePin = 10;

// Joystick pins
const int joy1X = A0; //Shoulder
const int joy1Y = A3; //Elbow
const int joy2X = A2; //Base
const int joy2Y = A1; //Gripper

// Starting angles
float shoulderAngle = 90;
float elbowAngle = 85;
float gripperAngle = 90;
float baseAngle = 90;

// Angle limits
const int ShoulderLeft = 45;
const int ShoulderRight = 120;

const int elbowUp = 40;
const int elbowDown = 130;

const int gripperOpen = 0;
const int gripperClose = 180;

const int baseMin = 0;
const int baseMax = 180;

// Joystick settings
const int center = 512;
const int deadzone = 30;

// Movement speed
const float speed = 60.0;

// -1 adjust to your servo direction
const int shoulderDirection = 1;
const int elbowDirection = -1;
const int gripperDirection = 1;
const int baseDirection = 1;

unsigned long previousTime = 0;

float readJoystick(int pin) {
  int value = analogRead(pin);
  int difference = value - center;

  if (abs(difference) < deadzone) {
    return 0;
  }

  return difference / 512.0;
}

void setup() {
  Serial.begin(9600);

  shoulderServo.attach(shoulderPin);
  elbowServo.attach(elbowPin);
  gripperServo.attach(gripperPin);
  baseServo.attach(basePin);

  shoulderServo.write(shoulderAngle);
  elbowServo.write(elbowAngle);
  gripperServo.write(gripperAngle);
  baseServo.write(baseAngle);

  previousTime = millis();
}

void loop() {
  unsigned long currentTime = millis();
  float dt = (currentTime - previousTime) / 1000.0;
  previousTime = currentTime;

  if (dt > 0.05) {
    dt = 0.05;
  }

  float shoulderInput = readJoystick(joy1X);
  float elbowInput = readJoystick(joy1Y);
  float gripperInput = readJoystick(joy2Y);
  float baseInput = readJoystick(joy2X);

  shoulderAngle += shoulderInput * speed * shoulderDirection * dt;
  elbowAngle += elbowInput * speed * elbowDirection * dt;
  gripperAngle += gripperInput * speed * gripperDirection * dt;
  baseAngle += baseInput * speed * baseDirection * dt;

  shoulderAngle = constrain(shoulderAngle, ShoulderLeft, ShoulderRight);
  elbowAngle = constrain(elbowAngle, elbowUp, elbowDown);
  gripperAngle = constrain(gripperAngle, gripperOpen, gripperClose);
  baseAngle = constrain(baseAngle, baseMin, baseMax);

  shoulderServo.write((int)shoulderAngle);
  elbowServo.write((int)elbowAngle);
  gripperServo.write((int)gripperAngle);
  baseServo.write((int)baseAngle);
}
