#ifndef ESP8266_H
#define ESP8266_H
#include <SoftwareSerial.h>
#include "Arduino.h"
#include "XFS5152.h"

const int rxPin_wifi = 5;
const int txPin_wifi = 3;
const SoftwareSerial serial_wifi(rxPin_wifi, txPin_wifi);

void wifi_init();
//void wifi_send(char *message);
void wifi_get();

#endif
