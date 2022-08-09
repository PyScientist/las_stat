# -*- coding: cp1251 -*-
import os, sys
from stat import *
from string import *

def filtr_uniq(spisok):
    'получение уникального списка'
    spisok_uniq =[]
    for x in xrange(0,len(spisok)):
        if spisok_uniq.count(spisok[x])<1:
            spisok_uniq.append(spisok[x])
    return spisok_uniq

def spiski(folder_name):
    'получение списков папок, ласов, и других файлов не ласов'
    #Инициализация списков
    spisok_folders = []
    spisok_files = []
    spisok_unknown = []
    spisok_all =[]
    #Задание глубины просмотра папок
    subfolders = 4
    #Задание в список объектов из папки на вход
    spisok_object = os.listdir(folder_name)
    
    #Формирование начальных списков папок файлов и т.д.
    for x in  xrange(0,len(spisok_object)):
        mode = os.stat(folder_name+'/'+spisok_object[x])[ST_MODE]
        if S_ISDIR(mode):
            spisok_folders.append(folder_name+'/'+spisok_object[x])
        elif S_ISREG(mode):
            spisok_files.append(folder_name+'/'+spisok_object[x])
        else:
            spisok_unknown.append(folder_name+'/'+spisok_object[x])
            
    #Дополнение списков файлами и папками из вложенных папок до уровня глубины просмотра
    p=0
    while p < subfolders :
        #Цикл перебора папок в списке папок для извлечения информации о файлах и папках
        for x in xrange(0,len(spisok_folders)):
            folder_name = spisok_folders[x]
            spisok_object = os.listdir(folder_name)
            
            #Цикл опознания объекта
            for y in  xrange(0,len(spisok_object)):
                mode = os.stat(folder_name+'/'+spisok_object[y])[ST_MODE]   
                #добавление папок
                if S_ISDIR(mode):
                    spisok_folders.append(folder_name+'/'+spisok_object[y])
                #добавление файлов
                elif S_ISREG(mode):
                    spisok_files.append(folder_name+'/'+spisok_object[y])
                #добавление неопознанных объектов
                else:
                    spisok_unknown.append(folder_name+'/'+spisok_object[y])
        p = p+1

    #Извлечение уникальных значений для путей к файлам
    spisok_uniq_files = filtr_uniq(spisok_files)
    #Извлечение уникальных значений для путей к папкам
    spisok_uniq_folders = filtr_uniq(spisok_folders)
    #Извлечение уникальных значений для путей к неопознаным объектам
    spisok_uniq_unknown = filtr_uniq(spisok_unknown)
    #Формирование выходного списка (списков файлов папок и неопознаных обектов)
    spisok_all.append(spisok_uniq_files)
    spisok_all.append(spisok_uniq_folders)
    spisok_all.append(spisok_uniq_unknown)
      
    return spisok_all

def create_las_file_lists(spisok_all):
    'создание списков файлов лас  версий 1.2, 2.0 и нераспознанных файлов'
    #Получение списка файлов для определения версии лас
    spisok_uniq_files = spisok_all[0]
    
    #Инициализация выходных списков
    las_12_version_list = []
    las_20_version_list = []
    not_recognized_list = []
    spisok_files_all = []
    
    
    for x in xrange(0,len(spisok_uniq_files)):
        #Чтение одного из файлов
        read_las = open(spisok_uniq_files[x], "rb")
        spisok_strings_in_file = read_las.readlines()
        read_las.close

        #Инициализация переменных и списков
        version_information_position = vers = 'novalue'
        version_line = []
        wrap_line = []

        #Поиск начала раздела с данными о версии и свертки
        for y in xrange(0, len(spisok_strings_in_file)):
            if spisok_strings_in_file[y].startswith('~V') == 1 :
                version_information_position = y
        #получение строк с разверткой и версией las из считанного файла при условии что блок версии ~version information найден
        if version_information_position  <> 'novalue':          
            for y in xrange (version_information_position, len(spisok_strings_in_file)):
                if ((strip(spisok_strings_in_file[y]).startswith('VERS') == 1)or (strip(spisok_strings_in_file[y]).startswith('Vers') == 1)):
                    version_line = spisok_strings_in_file[y]
                if (strip(spisok_strings_in_file[y]).startswith('WRAP') == 1) :
                    wrap_line = spisok_strings_in_file[y]   
                if spisok_strings_in_file[y+1].startswith('~') == 1 :
                    break
        #получение значения версии файла при условии что строка версии не равна пустой строке
        if version_line <> []:
            version_line_lenght=len(version_line)
            mesto_pervoi_tochki=str(version_line).find('.')
            mesto_dvoetochiya=str(version_line).find(':')
            vers = strip(str(version_line)[mesto_pervoi_tochki+1:mesto_dvoetochiya])
        #Запись пути к файлу в список для версии 1.2
        if ((vers == '1.20') or (vers == '1.2')) : las_12_version_list.append(spisok_uniq_files[x])
        #Запись пути к файлу в список для версии 2.0
        elif ((vers == '2.00') or (vers == '2.0') or (vers == '2')):las_20_version_list.append(spisok_uniq_files[x])
        #Запись пути к файлу в список для неопознаных файлов
        else: not_recognized_list.append(spisok_uniq_files[x])
        
    #Формирование выходного списка (списков файлов лас 1.2 2.0 и неопознаных файлов)
    spisok_files_all.append(las_12_version_list)
    spisok_files_all.append(las_20_version_list)
    spisok_files_all.append(not_recognized_list)
        
    return spisok_files_all

def print_files_stat_in_file(report_file, spisok_all,spisok_files_all):
    'Печать списков папок, файлов, неопознаных объектов в выходной файл, а также списки las 1.2 2.0 и неопознаных файлов'
    #присвоение списков
    spisok_uniq_files = spisok_all[0]
    spisok_uniq_folders = spisok_all[1]
    spisok_uniq_unknown = spisok_all[2]
    las_12_version_list = spisok_files_all[0]
    las_20_version_list = spisok_files_all[1]
    not_recognized_list = spisok_files_all[2]

    #Открытие файла для записи 
    report = open(report_file, 'w')

    #Запись в файл колличества папок и их пути или EMPTY в случае если вложенных папок нет    
    report.write('FOLDERS:'+str(len(spisok_uniq_folders))+'\n')
    if len(spisok_uniq_folders) == 0 : report.write('--EMPTY--'+'\n')
    else :
        for x in xrange (0,len(spisok_uniq_folders)):
            report.write(spisok_uniq_folders[x].encode('cp', 'replace')+'\n')    
    #Запись в файл колличества файлов и их пути или EMPTY в случае если файлов нет   
    report.write('FILES:'+str(len(spisok_uniq_files))+'\n')
    if len(spisok_uniq_files) == 0 : report.write('--EMPTY--'+'\n')
    else :
        for x in xrange (0,len(spisok_uniq_files)):
            print spisok_uniq_files[x]
            report.write(spisok_uniq_files[x].encode('utf-8', 'replace')+'\n')
    #Запись в файл колличества лас файлов 1.2 и их пути или EMPTY в случае если файлов нет
    report.write('Las_files 1.20:'+str(len(las_12_version_list))+'\n')
    if len(las_12_version_list) == 0 : report.write('--EMPTY--'+'\n')
    else :
        for x in xrange (0,len(las_12_version_list)):
            report.write(unicode(las_12_version_list[x]).encode('utf-8', 'replace')+'\n')
    #Запись в файл колличества лас файлов 2.0 и их пути или EMPTY в случае если файлов нет       
    report.write('Las_files 2.00:'+str(len(las_20_version_list))+'\n')
    if len(las_20_version_list) == 0 : report.write('--EMPTY--'+'\n')
    else :
        for x in xrange (0,len(las_20_version_list)):
            report.write(las_20_version_list[x].encode('utf-8', 'replace')+"\n")
    #Запись в файл колличества нераспознанных файлов и их пути или EMPTY в случае если файлов нет       
    report.write('Not recognized files:'+str(len(not_recognized_list))+'\n')
    if len(not_recognized_list) == 0 : report.write('--EMPTY--'+'\n')
    else :
        for x in xrange (0,len(not_recognized_list)):
            report.write(not_recognized_list[x].encode('utf-8', 'replace')+'\n')  
    #Запись в файл колличества нераспознанных объектов и их пути или EMPTY в случае если объектов нет      
    report.write('UNKNOWN:'+str(len(spisok_uniq_unknown))+'\n')
    if len(spisok_uniq_unknown) == 0 : report.write('--EMPTY--'+'\n')
    else :
        for x in xrange (0,len(spisok_uniq_unknown)):
            report.write(spisok_uniq_unknown[x].encode('utf-8', 'replace'), '\n')
                  
    report.close


def spiski_fayla(folder_name, report_file):
    'функция для исполненения модуля razbor_files_in_folder'
    spisok_all = spiski(folder_name)
    spisok_files_all = create_las_file_lists(spisok_all)
    print_files_stat_in_file(report_file, spisok_all,spisok_files_all)
    return spisok_files_all


#DATA FOR TEST
report_file = 'C:/Python26/1/Results/good_riddance'
folder_name = 'C:/Python26/1/Workя'
spiski_fayla(folder_name, report_file)

    