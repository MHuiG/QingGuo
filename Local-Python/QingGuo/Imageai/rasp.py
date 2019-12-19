import os
import socket
import cv2
import time
#ServerIP = "101.132.96.221"
ServerIP = "192.168.1.103"
ServerPoint = 8089
while True:
    try:
        cap = cv2.VideoCapture(0)
        obj = socket.socket()
        obj.connect((ServerIP,ServerPoint))
        while True:
            ret_bytes = obj.recv(1024)
            ret_str = str(ret_bytes,encoding="utf-8").strip()
            if ret_str == "Send":
                break
        ret, frame = cap.read()
        cv2.imwrite("photo.jpg", frame)
        f = open("photo.jpg", 'rb')
        file_size = os.stat("photo.jpg").st_size
        print(file_size)
        obj.send(bytes(str(file_size),encoding="utf-8"))
        print(bytes(str(file_size),encoding="utf-8"))
        time.sleep(1) #缓冲时间
        has_sent = 0
        while has_sent != file_size:
            data = f.read(1024)
            obj.sendall(data)
            has_sent = has_sent + len(data)
        f.close()
        print("OK")
        obj.close()
        cap.release()
    except Exception as e:
        print(e)
        obj.close()
        cap.release()


