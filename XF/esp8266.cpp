#include "esp8266.h"
void wifi_init()
{
  serial_wifi.listen();
  serial_wifi.begin(9600);
  _delay_ms(2);
  /*serial_wifi.println("AT+RST");
    serial_wifi.println("AT");
    _delay_ms(3000);
    serial_wifi.println("AT+CWMODE=1");
    _delay_ms(3000);
    serial_wifi.println("AT+CWJAP=\"QingGuo\",\"12345678\"");
    _delay_ms(3000);*/
  serial_wifi.println("AT+CIPMUX=0");
  _delay_ms(1000);
  //serial_wifi.println("AT+CIPSTART=\"TCP\",\"192.168.1.100\",8086");//local-java
  //  serial_wifi.println("AT+CIPSTART=\"TCP\",\"101.132.98.221\",8088"); //cloud
  serial_wifi.println("AT+CIPSTART=\"TCP\",\"192.168.1.103\",8088"); //local-python
  //    serial_wifi.println("AT+CIPSTART=\"TCP\",\"192.168.43.241\",8088"); //local-python WLan
  //  serial_wifi.println("AT+CIPSTART=\"TCP\",\"192.168.43.240\",8088"); //local-python WLan pi
  _delay_ms(1000);
  serial_wifi.println("AT+CIPMODE=1");
  _delay_ms(1000);
  serial_wifi.println("AT+CIPSEND");
  _delay_ms(1000);
  //serial_wifi.println("init_end");
  //_delay_ms(1000);
}
/*void wifi_send(char *message)
  {
  serial_wifi.listen();
  serial_wifi.print(message);
  }*/
void wifi_get()
{
  serial_wifi.listen();
  String comdata = "";
  while (serial_wifi.available() > 0)
  {
    comdata += char(serial_wifi.read());
    delay(2);
  }

  if (comdata.length() > 0)
  {
    char *send_message = comdata.c_str();
    //serial_wifi.println(send_message);
    XFS_FrameInfo(send_message);
    //omdata = "";
  }
}
