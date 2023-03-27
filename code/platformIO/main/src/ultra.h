#include <Arduino.h>
#define ultrasonico 12

long microsecondsToCentimeters(long microseconds) {
  return microseconds / 29 / 2;
}
int ultra() {
  
  pinMode(ultrasonico, OUTPUT);
  digitalWrite(ultrasonico, LOW);
  delayMicroseconds(2);
  digitalWrite(ultrasonico, HIGH);
  delayMicroseconds(5);
  digitalWrite(ultrasonico, LOW);
  pinMode(ultrasonico, INPUT);
  
  long duration = pulseIn(ultrasonico, HIGH);

  long cm = microsecondsToCentimeters(duration);
  delay(100);

  return cm;
}

