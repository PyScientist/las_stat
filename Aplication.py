# -*- coding: Windows-1251 -*-
import os, sys
from stat import *
from string import *
from las_stat import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """Main function"""
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.connect(self.run_button, SIGNAL('clicked()'), self.run_program)
        self.connect(self.proccess_folder_button, SIGNAL('clicked()'), self.set_to_proccess)
        self.connect(self.results_folder_button, SIGNAL('clicked()'), self.set_results)

    def run_program(self):
        """Run program function"""
        folder_name = ((unicode(self.proccess_folder_text.text()).encode('utf-8')).decode('utf-8'))
        result_folder_name = ((unicode(self.results_folder_text.text()).encode('utf-8')).decode('utf-8'))
        report_file = result_folder_name+'report_file.txt'
        results_file  = result_folder_name+'results_file.txt'
        print ('Путь к папке с данными для обработки', folder_name)
        print ('Путь к файлу отчета о наличии файлов', report_file)
        print ('Путь к файлу результатов статистики', results_file)
        #folder_name = 'C:/Python26/1/Work'
        #report_file = 'C:/Python26/1/Results/good_riddance'
        #results_file = 'C:/Python26/1/Results/good_results.txt'
        index_main(folder_name, report_file, results_file)
        
    def set_to_proccess(self):
        """Set folder with target las files"""
        folder_to_proccess = QFileDialog.getExistingDirectory(self,'Set folder to proccess','c:\\Python26\\1\\Work')
        self.proccess_folder_text.setText(folder_to_proccess)
    def set_results(self):
        """Set folder for Results"""
        result_folder = QFileDialog.getExistingDirectory(self,'Set folder to Results','c:\\Python26\\1\\Results')
        self.results_folder_text.setText(result_folder)

app = QApplication(sys.argv)
main = MainWindow()
main.show()
app.exec_()