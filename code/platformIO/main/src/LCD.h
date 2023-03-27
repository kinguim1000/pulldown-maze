#include <Arduino.h>
#include "SSD1306Ascii.h"
#include "SSD1306AsciiWire.h"

SSD1306AsciiWire oled;
void LCD(byte x, byte y, float num){
  char msg[80];
    sprintf(msg, "%s", (String(num,2)));
    oled.setCursor (x, y); 
    oled.print(msg);
}
void LCDs(byte x, byte y, String num){
  char msgs[80];
    sprintf(msgs, "%s", num);
    oled.setCursor (x, y); 
    oled.print(msgs);
}