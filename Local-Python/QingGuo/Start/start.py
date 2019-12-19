import os
import threading
import path
class Thread1(threading.Thread):
    def __init__(self):
        super(Thread1,self).__init__()
    def run(self):
        os.system(path.StartServer)
class Thread2(threading.Thread):
    def __init__(self):
        super(Thread2,self).__init__()
    def run(self):
        os.system(path.StartImageai)
class Thread3(threading.Thread):
    def __init__(self):
        super(Thread3,self).__init__()
    def run(self):
        os.system(path.StartCNN)
Thread1().start()
Thread2().start()
#Thread3().start()
