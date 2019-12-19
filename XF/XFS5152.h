#ifndef XFS5152_H
#define XFS5152_H

#include "Arduino.h"
#include <SoftwareSerial.h>
#include <string.h>

const int rxPin_xfs = 7;
const int txPin_xfs = 6;
const int rxPin_433 = 5;
const int txPin_433 = 3;
const SoftwareSerial serial_XFS(rxPin_xfs, txPin_xfs);
const SoftwareSerial serial_433(rxPin_433, txPin_433);

const char XFS_StopCom[] = {0xFD, 0X00, 0X01, 0X02}; //停止合成
const char XFS_SuspendCom[] = {0XFD, 0X00, 0X01, 0X03}; //暂停合成
const char XFS_RecoverCom[] = {0XFD, 0X00, 0X01, 0X04}; //恢复合成
const char XFS_ChackCom[] = {0XFD, 0X00, 0X01, 0X21}; //状态查询
const char XFS_PowerDownCom[] = {0XFD, 0X00, 0X01, 0X88}; //进入POWER DOWN 状态命令

void XFS_FrameInfo(char *HZdata);
void YS_XFS_Set(char *Info_data);

void serial_send();

#endif
