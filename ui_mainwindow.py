# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwindow.ui'
#
# Created: Tue Mar 16 18:53:54 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(724, 246)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 40, 641, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.proccess_folder_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.proccess_folder_button.setObjectName("proccess_folder_button")
        self.horizontalLayout.addWidget(self.proccess_folder_button)
        self.proccess_folder_text = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.proccess_folder_text.setObjectName("proccess_folder_text")
        self.horizontalLayout.addWidget(self.proccess_folder_text)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.results_folder_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.results_folder_button.setObjectName("results_folder_button")
        self.horizontalLayout_2.addWidget(self.results_folder_button)
        self.results_folder_text = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.results_folder_text.setObjectName("results_folder_text")
        self.horizontalLayout_2.addWidget(self.results_folder_text)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.run_button = QtGui.QPushButton(self.verticalLayoutWidget)
        self.run_button.setObjectName("run_button")
        self.verticalLayout.addWidget(self.run_button)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(140, 180, 511, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.proccess_folder_button.setText(QtGui.QApplication.translate("MainWindow", "Set folder to proccess", None, QtGui.QApplication.UnicodeUTF8))
        self.results_folder_button.setText(QtGui.QApplication.translate("MainWindow", "Set Results folder", None, QtGui.QApplication.UnicodeUTF8))
        self.run_button.setText(QtGui.QApplication.translate("MainWindow", "RUN", None, QtGui.QApplication.UnicodeUTF8))

