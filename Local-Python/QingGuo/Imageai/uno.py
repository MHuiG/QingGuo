import socket
ServerIP = "192.168.1.103"
#ServerIP = "192.168.1.121"
while True:
    #ServerIP = "101.132.96.221"
    ServerPoint = 8088

    obj = socket.socket()
    obj.connect((ServerIP,ServerPoint))

    while True:
        while True:
            s = input(">>>")
            if (s == "1") | (s == "0"):
                break
        if s == "1":
            obj.sendall(bytes("hello\n",encoding="gbk"))

        if s == "0":
            obj.sendall(bytes("what\n",encoding="gbk"))
        ret_bytes = obj.recv(1024)
        ret_str = str(ret_bytes,encoding="gbk")
        if ret_str != "":
            print(ret_str)

