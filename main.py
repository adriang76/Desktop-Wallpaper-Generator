import sys
import os
import typing
import openai
import urllib.request
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QTextEdit, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


class Thread(QThread):
    download_complete = pyqtSignal(str)

    def __init__(self, url, filename):
        QThread.__init__(self)
        self.url = url
        self.filename = filename

    def run(self):
        try:
            image_path, _ = urllib.request.urlretrieve(self.url, self.filename)
            self.download_complete.emit(image_path)
        except Exception as e:
            print(f"API Failed: {e}")
            self.download_complete.emit('')


class ImageWindow(QWidget):
    def __init__(self):
        super(ImageWindow, self).__init__()
        self.initUI()
        self.setGeometry(600, 550, 896, 512)
        self.setWindowTitle("Image display")

    def initUI(self):
        self.imageLabel = QLabel(self)
        self.imageLabel.resize(896, 512)

    def display_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size()))
        self.show()


class MYwindow(QWidget):
    def __init__(self):
        super(MYwindow, self).__init__()
        self.initUI()
        self.setGeometry(600, 550, 1000, 600)
        self.setWindowTitle("Desk Image Generator")
        self.i = 1
        self.filename = "deskimg1.jpg"

    def initUI(self):
        self.genimage = QPushButton("Generate Images", self)
        self.input_box = QTextEdit("Desribe the backgorund you want", self)

        self.Text = QLabel("Generate A Desktop Background", self)
        self.reset = QPushButton("Reset", self)
        self.pop_up_error = QMessageBox(self)
        self.pop_up_error.setWindowTitle("error")
        self.pop_up_error.setText("Put A Description")

        font = QFont("Helvetica", 20)
        self.Text.setFont(font)
        self.imageWindow = ImageWindow()
        # inout box size
        self.input_box.resize(750, 40)
        # button sizes
        button_size = (300, 40)
        self.genimage.resize(*button_size)

        self.reset.resize(*button_size)
        # button events
        self.button_events()
       # positions
        self.Text.move(315, 100)
        self.input_box.move(125, 300)
        self.genimage.move(200, 450)

        self.reset.move(500, 450)

        self.setStyleSheet("""
        QTextEdit {
                color: #CFCFCF;
                font-family: Arial;
                font-size: 12px;
                border: 2px solid #817F7F;
                border-radius: 5px;
                padding: 5px;
            }
        QWidget{
                background-color: #272626; 
                color: #BCBCBC;           
        }
        QPushButton {
                background-color: #1C1D1D; 
                color: #CFCFCF; 
                border: 2px solid #CFCFCF; 
                padding: 5px 10px; 
            }
                           
        QPushButton:hover {
                background-color: #CFCFCF; /* Lighter background color for buttons on hover */
                color: #313333; 
            }
        
        
        """)

    def button_events(self):
        self.reset.clicked.connect(self.reset_app)
        self.genimage.clicked.connect(self.gen_image_clicked)

    def saved_images(self):
        pass

    def gen_image_clicked(self):
        default_text = "Desribe the backgorund you want"
        user_input = self.input_box.toPlainText()

        if user_input.strip() == "" or user_input.strip() == default_text:
            self.pop_up_error.exec_()
            self.input_box.clear()
        else:
            try:
                response = openai.images.generate(
                    model="dall-e-3",
                    prompt=user_input,
                    size="1792x1024",
                    quality="standard",
                    n=1,
                )
                image_url = response.data[0].url
                self.image_urls.append(image_url)
                self.download_and_show_image(image_url)
            except Exception as e:
                print(f"An error occurred: {e}")

    def download_and_show_image(self, image_url):

        self.i = self.i + 1
        self.filename = f"deskimg{self.i}.jpg"
        self.thread = Thread(image_url, self.filename)
        self.thread.download_complete.connect(self.imageWindow.display_image)
        self.thread.start()

    def reset_app(self):

        self.input_box.clear()


def window():
    app = QApplication(sys.argv)
    win = MYwindow()

    win.show()
    sys.exit(app.exec())


window()
