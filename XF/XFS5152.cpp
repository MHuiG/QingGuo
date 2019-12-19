#include "XFS5152.h"
/***********************************************************
  名    称：  YS-XFS5051 文本合成函数
  功    能：  发送合成文本到XFS5051芯片进行合成播放
  入口参数：  *HZdata:文本指针变量
  出口参数：
  说    明： 本函数只用于文本合成，具备背景音乐选择。默认波特率9600bps。
  调用方法：例： SYN_FrameInfo（“飞音云电子”）；
**********************************************************/
void XFS_FrameInfo(char *HZdata)
{

  char Frame_Info[200]; //定义的文本长度
  unsigned  int  HZ_Length;

  unsigned  int i = 0;
  HZ_Length = strlen(HZdata);      //需要发送文本的长度

  /*****************帧固定配置信息**************************************/
  Frame_Info[0] = 0xFD ;       //构造帧头FD
  Frame_Info[1] = 0x00 ;       //构造数据区长度的高字节
  Frame_Info[2] = HZ_Length + 2;   //构造数据区长度的低字节
  Frame_Info[3] = 0x01 ;       //构造命令字：合成播放命令
  Frame_Info[4] = 0x01;       //文本编码格式：GBK

  /*******************发送帧信息***************************************/
  memcpy(&Frame_Info[5], HZdata, HZ_Length);
  //PrintCom(Frame_Info,5+HZ_Length); //发送帧配置
  serial_XFS.listen();
  serial_XFS.begin(9600);
  _delay_ms(10);
  serial_XFS.write(Frame_Info, 5 + HZ_Length);
}


/***********************************************************
  名    称： void  main(void)
  功    能： 主函数 程序入口
  入口参数： *Info_data:固定的配置信息变量
  出口参数：
  说    明：本函数用于配置，停止合成、暂停合成等设置 ，默认波特率9600bps。
  调用方法：通过调用已经定义的相关数组进行配置。
**********************************************************/
void YS_XFS_Set(char *Info_data)
{
  char Com_Len;
  Com_Len = strlen(Info_data);
  //PrintCom(Info_data,Com_Len);

  serial_XFS.listen();
  serial_XFS.begin(9600);
  _delay_ms(10);
  serial_XFS.print(Info_data);
}

void serial_send()
{
  serial_433.listen();
  serial_433.begin(9600);
  String comdata = "";
  while (serial_433.available() > 0)
  {
    comdata += char(serial_433.read());
    delay(2);
  }

  if (comdata.length() > 0)
  {
    char *send_message = comdata.c_str();
    serial_433.println(send_message);
    XFS_FrameInfo(send_message);
    //omdata = "";
  }
}
