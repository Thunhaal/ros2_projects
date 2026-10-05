#define RPWM 25
#define LPWM 26
#define REN 27
#define LEN 14

String cmd = "";

void setup() {

  Serial.begin(115200);

  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(REN, OUTPUT);
  pinMode(LEN, OUTPUT);

  digitalWrite(REN, HIGH);
  digitalWrite(LEN, HIGH);

  analogWrite(RPWM, 0);
  analogWrite(LPWM, 0);

  Serial.println("Motor Ready");
}

void loop() {

  if (Serial.available()) {

    cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "forward") {

      analogWrite(RPWM, 200);
      analogWrite(LPWM, 0);
      Serial.println("Forward");

    }
    else if (cmd == "backward") {

      analogWrite(RPWM, 0);
      analogWrite(LPWM, 200);
      Serial.println("Backward");

    }
    else if (cmd == "stop") {

      analogWrite(RPWM, 0);
      analogWrite(LPWM, 0);
      Serial.println("Stopped");

    }

  }

}
