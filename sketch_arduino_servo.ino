#include<Servo.h>

Servo servo9;
Servo servo10;

void setup() {
  Serial.begin(9600);
  Serial.println("Hello, Arduino World!");
  // uint8_t CONTROL_PIN = 10; // Servo.h の仕様で、9 pin か 10 pin のみ
  servo9.attach(9);
  servo10.attach(10);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
}

void loop() {
  char key;

  // 30° だけ倒す（向かい合うので逆向き）
  servo9.write(120);
  servo10.write(60); // degree in [0, 180]
  delay(1000); // safe margin
  // Serial.println("in the loop...");

  // 'e' が入力されたら元に戻して終了する
  if (Serial.available()) {
    key = Serial.read();
    Serial.write(key);
    if (key == 'e') {
      servo9.write(90); // offset value
      servo10.write(90);
      delay(1000); // safe margin
      exit(0); // exit program
    }
  }
}
