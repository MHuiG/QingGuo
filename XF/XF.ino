#include "esp8266.h"
#include "ld3320.h"

VoiceRecognition Voice;                         //声明一个语音识别对象
#define Led 8                                   //定义LED控制引脚

void setup() {
  // put your setup code here, to run once:
  pinMode(Led, OUTPUT);                       //初始化LED引脚为输出模式
  digitalWrite(Led, LOW);                     //LED引脚低电平

  Voice.init();                               //初始化VoiceRecognition模块
  Voice.addCommand("kai deng", 0);            //添加指令,参数（指令内容,指令标签（可重复））
  Voice.addCommand("guan deng", 1);           //添加指令,参数（指令内容,指令标签（可重复））
  Voice.addCommand("ni hao", 2);
  Voice.addCommand("zhe shi shen me", 3);
  Voice.start();//开始识别

  wifi_init();
  serial_wifi.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  wifi_get();
  //serial_send();
  switch (Voice.read())                         //判断识别
  {
    case 0:                                     //若是指令“kai deng”
      digitalWrite(Led, HIGH);                //点亮LED
      //Serial.print("LED ON");
      break;
    case 1:                                     //若是指令“guan deng”
      digitalWrite(Led, LOW); //熄灭LED
      //Serial.print("LED OFF");
      break;
    case 2:
      digitalWrite(Led, HIGH);
      serial_wifi.println("hello");
      break;
    case 3:
      digitalWrite(Led, HIGH);
      serial_wifi.println("what");
      break;
    default:
      break;
  }


}

void wifi_send(char *message)
{
  serial_wifi.listen();
  serial_wifi.println(message);
  _delay_ms(1000);
}
