import socket
import predict
CNNServerIP = "172.19.71.150"  # localhost
CNNServerPoint = 8087
cnn_model = predict.CnnModel()
print("LoadCNNMould OK")
while True:
    try:
        """
        CNNSocketServer
        """
        s = socket.socket()
        s.bind((CNNServerIP, CNNServerPoint))
        s.listen(5)
        c, addr = s.accept()
        while True:
            while True:
                ss = c.recv(1024)
                #Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
                ss = str(ss,encoding="utf-8").strip()
                if ss != "":
                    #print("来自Socket的消息:"+ss)
                    break
            if ss=='end':
                break
            test_demo=[ss]
            res=[]
            for i in test_demo:
                res.append(cnn_model.predict(i))
                #print(cnn_model.predict(i))
            try:
                c.send(bytes(res[0],encoding="utf-8"))
            except Exception as e:
                print(e)
    except Exception as ex:
            print(ex)