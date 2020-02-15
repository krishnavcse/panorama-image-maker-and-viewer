from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QImage,QPalette, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel, QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy)
import subprocess
import webbrowser
import sys
import os
import cv2
import crop_i       # importing crop_i.py to provide crop image function
import main         # importing main.py to perform image stiching operation

class ImageViewer(QMainWindow):   #Class Name ImageViewer
    def __init__(self):      #__init__ method
        super(ImageViewer, self).__init__()
        self.scaleFactor = 0.0

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("PANORAMA")
        self.resize(500, 400)

    def new(self): #new() method for selecting the .text file which consist of ordered images list with focal length
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath()) #dialog box to select file
        if fileName: #fileName is the path of the file
            main.newPanorama(fileName) # main.py is the file and newPanorama() is method of it, fileName is passed for stitching
            cwd = os.getcwd() #get current directory and perform manipulation to display the stiched image after completion
            data = cwd.split("\\")
            data.pop()
            source_d = '\\'.join(data)
            source_d = source_d + '\stitch' + '\cropped.jpg'
            image = QImage(source_d)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer" , "Cannot load %s." % source_d)
                return
            crop_i.f_path = source_d
            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.cropAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def open(self): # open() method to open any image from any folder
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        if fileName:
            #print(fileName)
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return
            crop_i.f_path = fileName
            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.cropAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def exit(self): #exit() method to quit the GUI and Program
        exit(0)

    def save(self): #save() method to save the image to any folder
        if crop_i.f_path:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
            img = cv2.imread(crop_i.f_path)
            cv2.imwrite(fileName, img)
        else:
            print("No File to Save")

    def crop(self): # crop() method to crop the image by pressing c and r if selection not proper
        crop_i.path_image(crop_i.f_path) # crop_i.py file and path_image() to crop the image

    def zoomIn(self): # zoomIn() method to zoomin
        self.scaleImage(1.25)

    def zoomOut(self):# zoomOut() method to zoomout
        self.scaleImage(0.8)

    def normalSize(self): #normalSize() method to display the image with 100% size
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def panoramaView(self): # panoramaView() method to view the panorama image in webpage view through browser
        cwd = os.getcwd()
        data = cwd.split("\\")
        data.pop()
        source_d = '\\'.join(data)
        source_d = source_d + '\Panorama_Viewer'
        url = source_d + '\PanoramaViewer.html' #webpage link where the Panorama image could be viewed
        #print(url)
        if sys.platform == 'darwin':  # in case of OS X
            subprocess.Popen(['open', url]) #opens up browser
        else:
            webbrowser.open_new_tab(url) # opens a new tab in browser

    def fitToWindow(self): #fitToWindow() for complete view of the image in window by filling complete size of window
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self): # about() method consist information about the project. I have written sample information.
        #You can edit the information and write as per your need
        QMessageBox.about(self, "About Image Viewer",
                "<p>The <b>Panorama Project</b> example shows how to combine "
                "QLabel and QScrollArea to display an image. QLabel is "
                "typically used for displaying text, but it can also display "
                "an image. QScrollArea provides a scrolling view around "
                "another widget. If the child widget exceeds the size of the "
                "frame, QScrollArea automatically provides scroll bars.</p>"
                "<p>The example demonstrates how QLabel's ability to scale "
                "its contents (QLabel.scaledContents), and QScrollArea's "
                "ability to automatically resize its contents "
                "(QScrollArea.widgetResizable), can be used to implement "
                "zooming and scaling features.</p>")

    def createActions(self): # createAction() method to provide action to the earlier methods
        self.newAct = QAction("&New...", self, shortcut="Ctrl+N",
                               triggered=self.new)

        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.cropAct = QAction("&Crop...", self, shortcut="Ctrl+C",
                enabled=False, triggered=self.crop)

        self.saveAct = QAction("&Save...", self, shortcut="Ctrl+S",
                triggered=self.save)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.exit)

        self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++",
                enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-",
                enabled=False, triggered=self.zoomOut)

        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+E",
                enabled=False, triggered=self.normalSize)

        self.panoramaAct = QAction("&Panorama Viewer", self, shortcut="Ctrl+P",
                                   triggered=self.panoramaView)

        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False,
                checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)

        self.aboutAct = QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                triggered=QApplication.instance().aboutQt)

    def createMenus(self): #createMenus() to create menu for the GUI
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.cropAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addAction(self.panoramaAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self): #updateActions() method to update the action
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor): # scaleImage() method to scale the image
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor): #adjustScrollBar() to keep track of scroll bar
        scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * scrollBar.pageStep()/2)))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    imageViewer = ImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())