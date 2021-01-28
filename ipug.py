from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
import json
import urllib.request
import webbrowser

def get_json_data_from_http(url):
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
    except Exception as e:
        print(f"Impossible de lire le contenu json : {url}\n{e}")
    else:
        return data

def get_json_data_local(json_path):  
    with open(json_path, "r") as data:
        try:
            list_data = json.load(data)
        except Exception as e:
            print(f"Impossible d'ouvrir le fichier {json_path} \n{e}")
            return False
        else:
            return list_data

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.fname = ""
        self.setWindowTitle("GENEPIX Geolocalisation")
        self.setGeometry(300,300, 800,600)
        self.main_layout = QVBoxLayout()
        self.lbl_logo = QLabel(self)
        pixmap = QPixmap('img/genepix_localizer.png')
        self.lbl_logo.setPixmap(pixmap)
        self.setStyleSheet("background-color: #222; color: #fff; font-weight: bold;")
        self.ip_address = QLineEdit("")
        self.ip_address.setPlaceholderText("addresse IP ...")
        self.ip_address.setStyleSheet("background-color: #e8e8e8; color: #222; padding: 15px; border-radius: 3px;")
        self.btn_search = QPushButton("Geolocaliser")
        self.btn_search.setStyleSheet("background-color: #ff074b; padding: 15px; border-radius: 3px;")
        self.btn_search.clicked.connect(self.geoloc)
        self.main_layout.addWidget(self.lbl_logo)
        self.main_layout.addWidget(self.ip_address)
        self.main_layout.addWidget(self.btn_search)
        self.setLayout(self.main_layout)

    def geoloc(self):
        apikey_jsonfile = "apikey.json"
        api_key = get_json_data_local(apikey_jsonfile)['key']
        ip_to_dox = self.ip_address.text()        
        if ip_to_dox == "":
            print("Merci de rentrer une adresse IP")
            return

        json_file = f"http://api.ipstack.com/{ip_to_dox}?access_key={api_key}&format=1"
        json_data = get_json_data_from_http(json_file)

        if "latitude" not in json_data.keys() or "longitude" not in json_data.keys():
            print(f"Impossible de récupérer les infos de cette IP : {ip_to_dox}")
            return
        latitude, longitude = json_data['latitude'], json_data['longitude']
    
        try:
            webbrowser.open(f"http://maps.google.com/?q={latitude},{longitude}")
        except Exception as e:
            print(f"Error while trying to open webbrowser")
            return


myApp = QApplication(sys.argv)
window = Window()
window.show() 
myApp.exec_()
sys.exit(0)