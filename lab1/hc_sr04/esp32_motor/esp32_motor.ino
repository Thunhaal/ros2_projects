#define RPWM 25
#define LPWM 26
#define REN 27
#define LEN 14

void setup() {
  Serial.begin(115200);

  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(REN, OUTPUT);
  pinMode(LEN, OUTPUT);

  digitalWrite(REN, HIGH);
  digitalWrite(LEN, HIGH);
}

void loop() {

  Serial.println("Forward");
  analogWrite(RPWM, 200);
  analogWrite(LPWM, 0);
  delay(5000);

  Serial.println("Stop");
  analogWrite(RPWM, 0);
  analogWrite(LPWM, 0);
  delay(2000);

  Serial.println("Backward");
  analogWrite(RPWM, 0);
  analogWrite(LPWM, 200);
  delay(5000);

  Serial.println("Stop");
  analogWrite(RPWM, 0);
  analogWrite(LPWM, 0);
  delay(2000);
}
