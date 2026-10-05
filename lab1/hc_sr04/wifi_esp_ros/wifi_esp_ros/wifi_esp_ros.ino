const int RPWM = 25;
const int LPWM = 26;

const int PWM_FREQ = 1000;
const int PWM_CHANNEL_R = 0;
const int PWM_CHANNEL_L = 1;
const int PWM_RESOLUTION = 8;

void setup()
{
  Serial.begin(115200);

  ledcSetup(PWM_CHANNEL_R, PWM_FREQ, PWM_RESOLUTION);
  ledcSetup(PWM_CHANNEL_L, PWM_FREQ, PWM_RESOLUTION);

  ledcAttachPin(RPWM, PWM_CHANNEL_R);
  ledcAttachPin(LPWM, PWM_CHANNEL_L);

  ledcWrite(PWM_CHANNEL_R, 0);
  ledcWrite(PWM_CHANNEL_L, 0);

  Serial.println("ESP32 Ready");
}

void loop()
{
  if (Serial.available())
  {
    String data = Serial.readStringUntil('\n');
    data.trim();

    int speed = data.toInt();

    if (speed < 0) speed = 0;
    if (speed > 100) speed = 100;

    int pwm = map(speed, 0, 100, 0, 255);

    // Forward
    ledcWrite(PWM_CHANNEL_R, pwm);
    ledcWrite(PWM_CHANNEL_L, 0);

    Serial.print("Speed = ");
    Serial.print(speed);
    Serial.print("%  PWM = ");
    Serial.println(pwm);
  }
}
