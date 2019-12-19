import socket
from threading import Thread
import urllib
import keras
from imageai.Detection import ObjectDetection
import os
from imageai.Prediction.Custom import CustomImagePrediction
import tensorflow as tf
def getLocalIP():
    ip = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 0))
        ip = s.getsockname()[0]
    except:
        name = socket.gethostname()
        ip = socket.gethostbyname(name)
    if ip.startswith("127."):
        cmd = '''/sbin/ifconfig | grep "inet " | cut -d: -f2 | awk '{print $1}' | grep -v "^127."'''
        a = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        a.wait()
        out = a.communicate()
        ip = out[0].strip().split("\n")  # 所有的列表
        if len(ip) == 1 and ip[0] == "" or len(ip) == 0:
            return False
        ip = "".join(ip)
    return ip
#ServerIP = "172.19.71.150"
#ServerIP = "localhost"
#ServerIP ="192.168.1.103"
#ServerIP = "192.168.43.241"
ServerIP = getLocalIP()
print(ServerIP)

UnoADDRESS = (ServerIP, 8088)
RaspADDRESS = (ServerIP, 8089)
g_socket_server_uno = None
g_conn_pool_uno = []
g_socket_server_rasp = None
g_conn_pool_rasp = []
Info=[]
Res=[]

def SaveRecord(result,source):
    url = "http://localhost:8000/SaveRecord/"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}
    formData = {
        'result': result,
        'source':source,
    }
    data = urllib.parse.urlencode(formData).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=header)
    return urllib.request.urlopen(request).read().decode("utf-8")


###翻译列表 列表中的'':''表示无法识别
Translate={'person':'人',  'bicycle':'自行车',  'car':'汽车',  'motorcycle':'摩托车',  'airplane':'飞机',  'bus':'公共汽车', 'train':'火车',
           'truck':'卡车',  'boat':'船', 'traffic light':'红绿灯',  'fire hydrant':'消防栓',  'stop sign':'停车标志',  'parking meter':'停车计时器',
           'bench':'长凳',  'bird':'鸟',  'cat':'猫',  'dog':'狗',  'horse':'马',  'sheep':'羊',  'cow':'牛',  'elephant':'大象',
           'bear':'熊', 'zebra':'斑马', 'giraffe':'长颈鹿',  'backpack':'背包',  'umbrella':'雨伞', 'handbag':'手提包', 'tie':'领带',
           'suitcase':'手提箱',  'frisbee':'飞盘',  'skis':'滑雪板', 'snowboard':'滑雪板',  'sports ball':'运动球',  'kite':'风筝',
           'baseball bat':'棒球棒',  'baseball glove':'棒球手套',  'skateboard':'滑板', 'surfboard':'冲浪板',  'tennis racket':'网球拍',
           'bottle':'瓶子', 'wine glass':'酒杯',  'cup':'杯子', 'fork':'叉', 'knife':'刀', 'spoon':'勺子',  'bowl':'碗',
           'banana':'香蕉',  'apple':'苹果', 'sandwich':'三明治', 'orange':'橘子', 'broccoli':'西兰花', 'carrot':'胡萝卜', 'hot dog':'热狗',
           'pizza':'披萨',  'donut':'甜甜圈', 'cake':'蛋糕', 'chair':'椅子','couch':'沙发', 'potted plant':'盆栽植物', 'bed':'床',
           'dining table':'餐桌',  'toilet':'厕所', 'tv':'电视', 'laptop':'笔记本电脑', 'mouse':'鼠标', 'remote':'遥控器', 'keyboard':'键盘',
           'cell phone':'手机', 'microwave':'微波炉', 'oven':'烤箱', 'toaster':'烤面包机', 'sink':'水池', 'refrigerator':'冰箱',
           'book':'书', 'clock':'时钟', 'vase':'花瓶',  'scissors':'剪刀', 'teddy bear':'泰迪熊',  'hair drier':'吹风机',
           'toothbrush':'牙刷','':''}



def init_uno(ADDRESS):
    global Info
    global Res
    global g_socket_server_uno
    g_socket_server_uno = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    g_socket_server_uno.bind(ADDRESS)
    g_socket_server_uno.listen(5)
    print("UNO服务端已启动，等待客户端连接...")
def accept_client_uno():
    while True:
        client, _ = g_socket_server_uno.accept()
        g_conn_pool_uno.append(client)
        thread = Thread(target=message_handle_uno, args=(client,))
        thread.setDaemon(True)
        thread.start()
def message_handle_uno(client):
    global Res
    print("uno客户端连接成功")
    print(g_conn_pool_uno)
    try:
        while True:
            while True:
                s = client.recv(1024)
                s = str(s,encoding="gbk").strip()
                if s != "":
                    print("来自Socket的消息:"+s)
                    if(s == "hello") | (s == "what"):
                        break
            if s == "hello":
                try:
                    client.send(bytes("你好,我是小黑",encoding="gbk"))
                except Exception as e:
                    print(e)
            if s == "what":
                Info.append("what")
                print(Info)
                Flag=True
                while True:
                    if "SendOK" in Info:
                        Info.remove("SendOK")
                        print(Info)
                        break
                    if "Error" in Info:
                        Flag=False
                        Info.remove("Error")
                        print(Info)
                        break
                if Flag:
                    Info.append("Check")
                    print(Info)
                    while True:
                        if "CheckOK" in Info:
                            Info.remove("CheckOK")
                            print(Info)
                            break
                    ret_str=Res[0]
                    Res=[]
                    if ret_str != "":
                        try:
                            client.send(bytes("这是"+ret_str,encoding="gbk"))
                        except Exception as e:
                            print(e)
                            client.close()
                            print("uno客户端关闭")
                            g_conn_pool_uno.remove(client)
                            print(g_conn_pool_uno)
                    else:
                        try:
                            client.send(bytes("我不知道",encoding="gbk"))
                        except Exception as e:
                            print(e)
                            client.close()
                            print("uno客户端关闭")
                            g_conn_pool_uno.remove(client)
                            print(g_conn_pool_uno)
                else:
                    try:
                        client.send(bytes("我没听清楚请再说一遍",encoding="gbk"))
                    except Exception as e:
                        print(e)
                        client.close()
                        print("uno客户端关闭")
                        g_conn_pool_uno.remove(client)
                        print(g_conn_pool_uno)
    except Exception as e:
        print(e)
        client.close()
        print("uno客户端关闭")
        g_conn_pool_uno.remove(client)
        print(g_conn_pool_uno)


def init_rasp(ADDRESS):
    global Info
    global Res
    global g_socket_server_rasp
    g_socket_server_rasp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    g_socket_server_rasp.bind(ADDRESS)
    g_socket_server_rasp.listen(5)
    print("RASP服务端已启动，等待客户端连接...")
def accept_client_rasp():
    while True:
        client, _ = g_socket_server_rasp.accept()
        g_conn_pool_rasp.append(client)
        thread = Thread(target=message_handle_rasp, args=(client,))
        thread.setDaemon(True)
        thread.start()
def message_handle_rasp(client):
    print("rasp客户端连接成功")
    print(g_conn_pool_rasp)
    while True:
        if "what" in Info:
            client.send(bytes("Send",encoding="utf-8"))
            print("Send")
            Info.remove("what")
            print(Info)
            break
    try:
        size = client.recv(1024)
        print(size)
        size_str = str(size,encoding="utf-8")
        print(size_str)
        file_size = int(size_str)
        print(file_size)
        has_size = 0
        f = open("rasp.jpg","wb")
        while True:
            if file_size == has_size:
                break
            date = client.recv(1024)
            f.write(date)
            has_size += len(date)
        f.close()
        Info.append("SendOK")
        print(Info)
        client.close()
        print("rasp客户端关闭")
        g_conn_pool_rasp.remove(client)
        print(g_conn_pool_rasp)
    except Exception as e:
        print(e)
        Info.append("Error")
        print(Info)
        client.close()
        print("rasp客户端关闭")
        g_conn_pool_rasp.remove(client)
        print(g_conn_pool_rasp)
if __name__ == '__main__':
    init_uno(UnoADDRESS)
    threadUno = Thread(target=accept_client_uno)
    threadUno.setDaemon(True)
    threadUno.start()
    init_rasp(RaspADDRESS)
    threadRasp = Thread(target=accept_client_rasp)
    threadRasp.setDaemon(True)
    threadRasp.start()
    while True:
        try:
            """
            清空会话
            第二次预测时不可缺少的操作
            如果缺少这一行代码会在AIThread线程的下一次开启预测时报错
            """
            ####销毁当前的TF图并创建一个新图。有助于避免旧模型/图层混乱 防止keras框架反复调用模型出错 第二次预测时,model底层tensorflow的session中还有数据
            keras.backend.clear_session()
            #通过编写此Config原型并传递给tf.session（）来允许GPU内存增长
            # config = tf.ConfigProto()
            # config.gpu_options.allow_growth = True
            # tf.Session(config=config)
            """
            载入目标检测模型
            """
            #获得当前python文件的文件夹的路径
            execution_path = os.getcwd()
            #创建ObjectDetection类的新实例
            detector = ObjectDetection()
            #将模型类型设置为RetinaNet
            detector.setModelTypeAsRetinaNet()
            #将模型路径设置为RetinaNet模型文件所在文件夹的路径
            detector.setModelPath(os.path.join(execution_path, "./ImageModel/resnet50_coco_best_v2.0.1.h5"))
            #载入模型 可用的检测速度是 "normal"(default), "fast", "faster" , "fastest" and "flash" flash不靠谱
            #detector.loadModel(detection_speed="fastest")
            detector.loadModel()

            #"""
            #加载自定义图像预测模型 (图像预测模型不知道自己不知道) DeepMind 发表论文表示深度生成模型真的不知道它们到底不知道什么。
            #"""
            #prediction = CustomImagePrediction()
            #prediction.setModelTypeAsResNet()
            #prediction.setModelPath(os.path.join(execution_path, "./ImageModel/0.h5"))
            #prediction.setJsonPath(os.path.join(execution_path, "./ImageModel/model_class.json"))
            #prediction.loadModel(num_objects=7)  # 载入模型并设置需要预测的对象数

            print("LoadModel OK")
            """
            Check
            """
            while True:
                try:
                    while True:
                        if "Check" in Info:
                            Info.remove("Check")
                            print(Info)
                            break
                    try:    
                        """
                        目标检测
                        """
                        # 调用了detectObjectsFromImage()函数并传入input_image参数和output_image_path参数来指定输入文件和输出文件的路径。
                        # 然后该函数返回一个字典数组，每个字典包含图像中检测到的对象信息，字典中的对象信息有name（对象类名）和 percentage_probability（概率）
                        detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, "./rasp.jpg"),
                                                                     output_image_path=os.path.join(execution_path,
                                                                                                    "./Identified.jpg"))
                        result = ""
                        maxNum = 0
                        for eachObject in detections:
                            print(eachObject["name"] + ":" + str(eachObject["percentage_probability"]))
                            if eachObject["percentage_probability"] > maxNum and eachObject['name'] != "person" and  eachObject['name'] != 'chair' and eachObject['name'] !='dining table':
                                maxNum = eachObject["percentage_probability"]
                                source = eachObject['name']
                                result = Translate[source]
                                break;
                       
                        print("--------------------------------------------------------------")
                        #"""
                        #自定义图像预测
                        #"""
                        #if maxNum < 60:
                        #    maxN = 0
                        #    predictions, probabilities = prediction.predictImage(os.path.join(execution_path, "./rasp.jpg"))
                        #    for eachPrediction, eachProbability in zip(predictions, probabilities):
                        #        print(eachPrediction + " : " + eachProbability)
                        #        if float(eachProbability) > maxN:
                        #            maxN = float(eachProbability)
                        #            sourceN = eachPrediction
                        #            resultN = Translate[sourceN]
                        #    if maxN > 90:
                        #        result = resultN
                        #        source = sourceN
                        #    else:
                        #        result = result
                        #print("--------------------------------------------------------------")
                        print(result)
                        # source="football"
                        # result="足球"
                        #c.send(bytes("这是"+result,encoding="utf-8"))
                        Res.append(result)
                        Info.append("CheckOK")
                        print(Info)
                        """
                        保存result至数据库
                        """
                        try:
                            rec = SaveRecord(result,source)
                            print(rec)
                        except Exception as e:
                            print(e)
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
        except Exception as ex:
                print(ex)


