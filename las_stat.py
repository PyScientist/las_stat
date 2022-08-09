# -*- coding: cp1251 -*-
import os, sys
from stat import *
from string import *
from razbor_las import  *
from razbor_files_in_folder import *


def help_chto_gde():
    vihodnoy_massiv_vocabulary = {0: '33'}

def write_results_in_file(vihodnoy_massiv, results_file):
    'Печать выходного массива в файл'
    destanation = open(results_file, 'w')
    for f in xrange(0, len(vihodnoy_massiv[0][0])):
        destanation.write(vihodnoy_massiv[0][0][f]+';')       
    for k in xrange(0, len(vihodnoy_massiv[0][2])):
        destanation.write(vihodnoy_massiv[0][2][k]+';')
    destanation.write('\n')
    for r in xrange (0, len(vihodnoy_massiv)):
        for p in xrange(0, len(vihodnoy_massiv[r][3][0])):
            for n in xrange(0, len(vihodnoy_massiv[r][0])):
                destanation.write((vihodnoy_massiv[r][1][n])+';')
            for s in xrange(0, len(vihodnoy_massiv[r][2])):
                destanation.write(str(vihodnoy_massiv[r][3][s][p])+';')
            destanation.write('\n')  
    destanation.close

def massive_itogov(folder_name, report_file):
    'Полученние массива данных для записи по всем файлам'
    las_all = []
    vihodnoy_massiv = []
    #Запись данных о фалах и папках в файл отчета и получение списка ласов на обработку
    spisok_files_all = spiski_fayla(folder_name, report_file)    
    # Получение полного массива данных по всем ласам
    for x in xrange(0,len((spisok_files_all)[0])):
        las_all.append((spisok_files_all)[0][x])
    for x in xrange(0,len((spisok_files_all)[1])):
        las_all.append((spisok_files_all)[1][x])
    for x in xrange(0, len(las_all)):
        vihodnoy_massiv.append(massive_statistiki(las_all[x]))
    return vihodnoy_massiv

def index_main(folder_name, report_file, results_file):
    'функция для запуска функций модуля'
    vihodnoy_massiv = massive_itogov(folder_name, report_file)
    write_results_in_file(vihodnoy_massiv, results_file)

#DATA FOR TEST      
folder_name = './ishoniy'
print(folder_name)
report_file = u'C:/Python26/1/Results/good_riddance'
results_file = u'C:/Python26/1/Results/good_results.txt'
index_main(folder_name, report_file, results_file)