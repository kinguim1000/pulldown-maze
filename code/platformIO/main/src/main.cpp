#include <Arduino.h>
#include "include.h"
using namespace Sensores;
// IRTherm therm1; // Create an IRTherm object to interact with throughout
// IRTherm therm2;
// IRTherm therm3;
// IRTherm therm4;

SensorDeTemperatura Sensor1(0x5C);
#define I2C_ADDRESS 0x3C

// Define proper RST_PIN if required.
#define RST_PIN -1

// SSD1306AsciiWire oled;

void setup() 
{
  Serial.begin(115200); // Initialize Serial to log output
  Wire.begin(); //Joing I2C bus

#if RST_PIN >= 0
  oled.begin(&Adafruit128x64, I2C_ADDRESS, RST_PIN);
#else // RST_PIN >= 0
  oled.begin(&Adafruit128x64, I2C_ADDRESS);
#endif // RST_PIN >= 0

  oled.setFont(System5x7);
  oled.clear();
  oled.print("Hello world!");
//   therm1.begin(0x5A);// Initialize thermal IR sensor
// therm2.begin(0x5B);
// therm3.begin(0x5C);
// therm4.begin(0x5D);

  Serial.println("Qwiic IR Thermometer did acknowledge.");
  
  // therm1.setUnit(TEMP_K); // Set the library's units to Farenheit
  // therm2.setUnit(TEMP_K); // Set the library's units to Farenheit
  // therm3.setUnit(TEMP_K); // Set the library's units to Farenheit
  // therm4.setUnit(TEMP_K); // Set the library's units to Farenheit
  
  // Alternatively, TEMP_F can be replaced with TEMP_C for Celsius or
  // TEMP_K for Kelvin.
  // LED pin as output
}

void loop() 
{
    
  // Call therm.read() to read object and ambient temperatures from the sensor.
  // if (therm1.read() && therm2.read() && therm3.read() && therm4.read()) // On success, read() will return 1, on fail 0.
  // {
    
     Serial.print(Sensor1);
     Serial.println("K");
     Serial.println();
  // // }
  // delay(1000);

}






// 0X3C+SA0 - 0x3C or 0x3D

//---------------------
//------------
/*
#include <Wire.h>

#include "LCD.h"



//------------------------------------------------------------------------------
void setup() {
  Wire.begin();
  Wire.setClock(400000L);


  oled.begin(&Adafruit128x64,0x3C);


  oled.setFont(Adafruit5x7);

  uint32_t m = micros();
  
}
//------------------------------------------------------------------------------
int b;
char buffer[40];
void loop() {
  
  b = 'a';
  sprintf(buffer,"%s",b);
  // LCD(0,0,buffer);

  oled.println("a");
}








*/
