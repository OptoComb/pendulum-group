#include<Servo.h>

Servo servo;

void setup() {
  // put your setup code here, to run once:
  uint8_t CONTROL_PIN = 10; // Servo.h の仕様で、9 pin か 10 pin のみ
  servo.attach(CONTROL_PIN);
  pinMode(CONTROL_PIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  servo.write(0); // degree
  delay(1000); // ミリ秒
  servo.write(90); // degree
  delay(1000); // ミリ秒
  exit(0);
}
