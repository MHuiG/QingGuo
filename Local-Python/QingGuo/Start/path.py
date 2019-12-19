import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Python = "D:/ProgramData/Anaconda3/envs/imageai/python.exe"


ServerPath = os.path.join(BASE_DIR, "manage.py")
ImageaiPath = os.path.join(BASE_DIR, "Imageai/main.py")


StartServer = Python+" "+ServerPath+" runserver 0.0.0.0:8000"
StartImageai = Python+" "+ImageaiPath

