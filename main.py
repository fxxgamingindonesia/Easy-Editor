from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout, QFileDialog
import os
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPixmap 

from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import SHARPEN

app = QApplication([])
window = QWidget()
window.setWindowTitle('Easy Editor')
window.resize(700, 500)

lb_image = QLabel('Image')
btn_left = QPushButton('Left')
btn_right = QPushButton('Right')
btn_mirror = QPushButton('Mirror')
btn_sharpness  = QPushButton('Sharpness')
btn_BW = QPushButton('B&W')
btn_folder = QPushButton('Folder')
list_files = QListWidget()

main_layout = QHBoxLayout()
layout_left = QVBoxLayout()
layout_right = QVBoxLayout()
layout_btn = QHBoxLayout()

layout_btn.addWidget(btn_left)
layout_btn.addWidget(btn_right)
layout_btn.addWidget(btn_mirror)
layout_btn.addWidget(btn_sharpness)
layout_btn.addWidget(btn_BW)

layout_left.addWidget(btn_folder)
layout_left.addWidget(list_files)

layout_right.addWidget(lb_image)
layout_right.addLayout(layout_btn)

main_layout.addLayout(layout_left, stretch= 1)
main_layout.addLayout(layout_right, stretch= 4)
window.setLayout(main_layout)

workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenamesList():
    extensions = ['.jpg', '.jpeg,', '.png', '.gif', '.bpm' ]
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)

    list_files.clear()
    for filename in filenames:
        list_files.addItem(filename)

class ImageProcessor():
    def __init__ (self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)

        self.image.save(fullname)
    
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir , self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir , self.filename)
        self.showImage(image_path)

    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir , self.filename)
        self.showImage(image_path)

    def do_sharpness(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir , self.filename)
        self.showImage(image_path)

    def do_BW(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir , self.filename)
        self.showImage(image_path)

workimage = ImageProcessor() 
def showChosenImage():
    if list_files.currentRow() >= 0:
        filename = list_files.currentItem().text()
        workimage.loadImage(workdir, filename)
        workimage.showImage(os.path.join(workdir, workimage.filename))










list_files.currentRowChanged.connect(showChosenImage)
btn_folder.clicked.connect(showFilenamesList)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_mirror.clicked.connect(workimage.do_mirror)
btn_sharpness.clicked.connect(workimage.do_sharpness)
btn_BW.clicked.connect(workimage.do_BW)
window.show()
app.exec_()