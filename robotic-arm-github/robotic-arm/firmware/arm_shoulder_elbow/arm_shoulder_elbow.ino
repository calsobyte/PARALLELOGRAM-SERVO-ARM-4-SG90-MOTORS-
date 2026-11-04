/*
  Shoulder + elbow control for the parallelogram arm  (v2: steadier).
  Joystick position -> servo angle (direct mapping).

  Joystick 1, X axis -> SHOULDER servo
      raw 1023 (stick left)  -> 45 degrees  (furthest front)
      raw 0    (stick right) -> 120 degrees (furthest back)

  Joystick 2, Y axis -> ELBOW servo
      raw 0    (stick up)    -> 40 degrees  (furthest up)
      raw 1023 (stick down)  -> 140 degrees (furthest down)

  Anti-shake: the readings are smoothed, values close to the stick's
  resting position count as exactly "centre" (so the spring bounce is
  ignored), and tiny angle changes are ignored.
*/

#include <Servo.h>

// ---------- Pins (same as the wiring table in the guide) ----------
const uint8_t SHOULDER_PIN = 5;
const uint8_t ELBOW_PIN    = 6;
const uint8_t JOY1_X_PIN   = A0;   // Joystick 1, VRx
const uint8_t JOY2_Y_PIN   = A3;   // Joystick 2, VRy

// ---------- Servo limits (degrees) ----------
const float SHOULDER_FRONT = 45;   // furthest front
const float SHOULDER_BACK  = 120;  // furthest back
const float ELBOW_UP       = 40;   // furthest up
const float ELBOW_DOWN     = 140;  // furthest down

// ---------- Joystick calibration ----------
// Set DEBUG to true and read the real end and resting values of each stick.
const int J1X_MIN = 0, J1X_MAX = 1023, J1X_CENTER = 512;
const int J2Y_MIN = 0, J2Y_MAX = 1023, J2Y_CENTER = 512;

// ---------- Anti-shake tuning ----------
const int   CENTER_DEADZONE = 40;     // stick values this close to centre = exactly centre (0 = off)
const float SMOOTHING       = 0.15;   // 0..1: lower = smoother but slower to respond
const float ANGLE_DEADBAND  = 1.5;    // ignore target changes smaller than this (degrees)

// ---------- Motion feel ----------
const float MAX_SPEED = 120.0;        // maximum servo speed, degrees per second
const unsigned long LOOP_MS = 20;     // update every 20 ms
const bool DEBUG = false;             // true = print readings and angles

Servo shoulder, elbow;
float filtX, filtY;                   // smoothed joystick values
float heldS, heldE;                   // held target angles
float shoulderNow, elbowNow;          // current (slew-limited) angles
int shoulderLast, elbowLast;          // last angles sent to the servos
unsigned long lastUpdate = 0, lastPrint = 0;

// Average 8 readings to reduce jitter.
int readAvg(uint8_t pin) {
  long sum = 0;
  for (uint8_t i = 0; i < 8; i++) sum += analogRead(pin);
  return sum / 8;
}

// Map x from [inMin, inMax] to [outMin, outMax], clamped, works in either direction.
float mapF(float x, float inMin, float inMax, float outMin, float outMax) {
  x = constrain(x, inMin, inMax);
  return outMin + (x - inMin) * (outMax - outMin) / (inMax - inMin);
}

// Treat values near the centre as exactly centre, and stretch the rest
// so the stick still reaches both ends of its range.
float withDeadzone(float raw, float minV, float center, float maxV) {
  float dz = CENTER_DEADZONE;
  if (fabs(raw - center) <= dz) return center;
  if (raw < center) return mapF(raw, minV, center - dz, minV, center);
  return mapF(raw, center + dz, maxV, center, maxV);
}

// Joystick 1 X: 0 -> 120 (back), 1023 -> 45 (front)
float shoulderTarget(float rawX) {
  float x = withDeadzone(rawX, J1X_MIN, J1X_CENTER, J1X_MAX);
  return mapF(x, J1X_MIN, J1X_MAX, SHOULDER_BACK, SHOULDER_FRONT);
}

// Joystick 2 Y: 0 -> 40 (up), 1023 -> 120 (down)
float elbowTarget(float rawY) {
  float y = withDeadzone(rawY, J2Y_MIN, J2Y_CENTER, J2Y_MAX);
  return mapF(y, J2Y_MIN, J2Y_MAX, ELBOW_UP, ELBOW_DOWN);
}

// Keep the old target unless the new one differs enough (always reach the ends).
float holdTarget(float held, float fresh, float lo, float hi) {
  if (fabs(fresh - held) >= ANGLE_DEADBAND) return fresh;
  if (fresh <= lo + 0.5 || fresh >= hi - 0.5) return fresh;
  return held;
}

// Move 'now' toward 'target' by at most maxStep degrees.
float approach(float now, float target, float maxStep) {
  float diff = target - now;
  if (diff > maxStep)  diff = maxStep;
  if (diff < -maxStep) diff = -maxStep;
  return now + diff;
}

void setup() {
  if (DEBUG) Serial.begin(9600);

  // Start from wherever the sticks are, so the servos don't jump on power-up.
  filtX = readAvg(JOY1_X_PIN);
  filtY = readAvg(JOY2_Y_PIN);
  heldS = shoulderNow = shoulderTarget(filtX);
  heldE = elbowNow    = elbowTarget(filtY);
  shoulderLast = (int)(shoulderNow + 0.5);
  elbowLast    = (int)(elbowNow + 0.5);

  shoulder.write(shoulderLast);           // set the target before attaching
  shoulder.attach(SHOULDER_PIN);
  delay(300);                             // stagger start-up current
  elbow.write(elbowLast);
  elbow.attach(ELBOW_PIN);
  delay(300);

  lastUpdate = millis();
}

void loop() {
  unsigned long now = millis();
  if (now - lastUpdate < LOOP_MS) return;
  float dt = (now - lastUpdate) / 1000.0;
  lastUpdate = now;

  int rawX = readAvg(JOY1_X_PIN);
  int rawY = readAvg(JOY2_Y_PIN);

  // Smooth the stick readings.
  filtX += SMOOTHING * (rawX - filtX);
  filtY += SMOOTHING * (rawY - filtY);

  // Turn them into held target angles.
  heldS = holdTarget(heldS, shoulderTarget(filtX), SHOULDER_FRONT, SHOULDER_BACK);
  heldE = holdTarget(heldE, elbowTarget(filtY),    ELBOW_UP,       ELBOW_DOWN);

  // Move toward the targets with a speed limit.
  float maxStep = MAX_SPEED * dt;
  shoulderNow = approach(shoulderNow, heldS, maxStep);
  elbowNow    = approach(elbowNow,    heldE, maxStep);

  // Never send an angle outside the calibrated range.
  int s = constrain((int)(shoulderNow + 0.5), (int)SHOULDER_FRONT, (int)SHOULDER_BACK);
  int e = constrain((int)(elbowNow + 0.5),    (int)ELBOW_UP,       (int)ELBOW_DOWN);

  if (s != shoulderLast) { shoulder.write(s); shoulderLast = s; }
  if (e != elbowLast)    { elbow.write(e);    elbowLast = e; }

  if (DEBUG && now - lastPrint > 200) {
    lastPrint = now;
    Serial.print(F("J1 X raw: ")); Serial.print(rawX);
    Serial.print(F(" smooth: ")); Serial.print((int)filtX);
    Serial.print(F(" -> shoulder: ")); Serial.print(s);
    Serial.print(F("   J2 Y raw: ")); Serial.print(rawY);
    Serial.print(F(" smooth: ")); Serial.print((int)filtY);
    Serial.print(F(" -> elbow: ")); Serial.println(e);
  }
}
