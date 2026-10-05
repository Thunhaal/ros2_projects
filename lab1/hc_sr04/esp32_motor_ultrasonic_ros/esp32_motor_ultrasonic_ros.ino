#define TRIG 5
#define ECHO 18

#define RPWM 25
#define LPWM 26
#define REN 27
#define LEN 14

void setup() {

  Serial.begin(115200);

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(REN, OUTPUT);
  pinMode(LEN, OUTPUT);

  digitalWrite(REN, HIGH);
  digitalWrite(LEN, HIGH);

  analogWrite(RPWM, 0);
  analogWrite(LPWM, 0);
}

void loop() {

  // Trigger ultrasonic sensor
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG, LOW);

  long duration = pulseIn(ECHO, HIGH);

  float distance = duration * 0.0343 / 2.0;

  // Ignore invalid readings
  if (distance <= 0 || distance > 300) {
    return;
  }

  int speed;

  // Gradual speed control
  if (distance <= 10) {

    speed = 0;

  }
  else if (distance >= 50) {

    speed = 255;

  }
  else {

    speed = map((int)distance, 10, 50, 60, 255);

  }

  // Drive motor
  analogWrite(RPWM, speed);
  analogWrite(LPWM, 0);
  
  Serial.println(distance);

  delay(100);
}
