# -*- coding: cp1251 -*-
import os, sys
from stat import *
from string import *

def filtr_uniq(spisok):
    '��������� ����������� ������'
    spisok_uniq =[]
    for x in xrange(0,len(spisok)):
        if spisok_uniq.count(spisok[x])<1:
            spisok_uniq.append(spisok[x])
    return spisok_uniq

def spiski(folder_name):
    '��������� ������� �����, �����, � ������ ������ �� �����'
    #������������� �������
    spisok_folders = []
    spisok_files = []
    spisok_unknown = []
    spisok_all =[]
    #������� ������� ��������� �����
    subfolders = 4
    #������� � ������ �������� �� ����� �� ����
    spisok_object = os.listdir(folder_name)
    
    #������������ ��������� ������� ����� ������ � �.�.
    for x in  xrange(0,len(spisok_object)):
        mode = os.stat(folder_name+'/'+spisok_object[x])[ST_MODE]
        if S_ISDIR(mode):
            spisok_folders.append(folder_name+'/'+spisok_object[x])
        elif S_ISREG(mode):
            spisok_files.append(folder_name+'/'+spisok_object[x])
        else:
            spisok_unknown.append(folder_name+'/'+spisok_object[x])
            
    #���������� ������� ������� � ������� �� ��������� ����� �� ������ ������� ���������
    p=0
    while p < subfolders :
        #���� �������� ����� � ������ ����� ��� ���������� ���������� � ������ � ������
        for x in xrange(0,len(spisok_folders)):
            folder_name = spisok_folders[x]
            spisok_object = os.listdir(folder_name)
            
            #���� ��������� �������
            for y in  xrange(0,len(spisok_object)):
                mode = os.stat(folder_name+'/'+spisok_object[y])[ST_MODE]   
                #���������� �����
                if S_ISDIR(mode):
                    spisok_folders.append(folder_name+'/'+spisok_object[y])
                #���������� ������
                elif S_ISREG(mode):
                    spisok_files.append(folder_name+'/'+spisok_object[y])
                #���������� ������������ ��������
                else:
                    spisok_unknown.append(folder_name+'/'+spisok_object[y])
        p = p+1

    #���������� ���������� �������� ��� ����� � ������
    spisok_uniq_files = filtr_uniq(spisok_files)
    #���������� ���������� �������� ��� ����� � ������
    spisok_uniq_folders = filtr_uniq(spisok_folders)
    #���������� ���������� �������� ��� ����� � ����������� ��������
    spisok_uniq_unknown = filtr_uniq(spisok_unknown)
    #������������ ��������� ������ (������� ������ ����� � ����������� �������)
    spisok_all.append(spisok_uniq_files)
    spisok_all.append(spisok_uniq_folders)
    spisok_all.append(spisok_uniq_unknown)
      
    return spisok_all

def create_las_file_lists(spisok_all):
    '�������� ������� ������ ���  ������ 1.2, 2.0 � �������������� ������'
    #��������� ������ ������ ��� ����������� ������ ���
    spisok_uniq_files = spisok_all[0]
    
    #������������� �������� �������
    las_12_version_list = []
    las_20_version_list = []
    not_recognized_list = []
    spisok_files_all = []
    
    
    for x in xrange(0,len(spisok_uniq_files)):
        #������ ������ �� ������
        read_las = open(spisok_uniq_files[x], "rb")
        spisok_strings_in_file = read_las.readlines()
        read_las.close

        #������������� ���������� � �������
        version_information_position = vers = 'novalue'
        version_line = []
        wrap_line = []

        #����� ������ ������� � ������� � ������ � �������
        for y in xrange(0, len(spisok_strings_in_file)):
            if spisok_strings_in_file[y].startswith('~V') == 1 :
                version_information_position = y
        #��������� ����� � ���������� � ������� las �� ���������� ����� ��� ������� ��� ���� ������ ~version information ������
        if version_information_position  <> 'novalue':          
            for y in xrange (version_information_position, len(spisok_strings_in_file)):
                if ((strip(spisok_strings_in_file[y]).startswith('VERS') == 1)or (strip(spisok_strings_in_file[y]).startswith('Vers') == 1)):
                    version_line = spisok_strings_in_file[y]
                if (strip(spisok_strings_in_file[y]).startswith('WRAP') == 1) :
                    wrap_line = spisok_strings_in_file[y]   
                if spisok_strings_in_file[y+1].startswith('~') == 1 :
                    break
        #��������� �������� ������ ����� ��� ������� ��� ������ ������ �� ����� ������ ������
        if version_line <> []:
            version_line_lenght=len(version_line)
            mesto_pervoi_tochki=str(version_line).find('.')
            mesto_dvoetochiya=str(version_line).find(':')
            vers = strip(str(version_line)[mesto_pervoi_tochki+1:mesto_dvoetochiya])
        #������ ���� � ����� � ������ ��� ������ 1.2
        if ((vers == '1.20') or (vers == '1.2')) : las_12_version_list.append(spisok_uniq_files[x])
        #������ ���� � ����� � ������ ��� ������ 2.0
        elif ((vers == '2.00') or (vers == '2.0') or (vers == '2')):las_20_version_list.append(spisok_uniq_files[x])
        #������ ���� � ����� � ������ ��� ����������� ������
        else: not_recognized_list.append(spisok_uniq_files[x])
        
    #������������ ��������� ������ (������� ������ ��� 1.2 2.0 � ����������� ������)
    spisok_files_all.append(las_12_version_list)
    spisok_files_all.append(las_20_version_list)
    spisok_files_all.append(not_recognized_list)
        
    return spisok_files_all

def print_files_stat_in_file(report_file, spisok_all,spisok_files_all):
    '������ ������� �����, ������, ����������� �������� � �������� ����, � ����� ������ las 1.2 2.0 � ����������� ������'
    #���������� �������
    spisok_uniq_files = spisok_all[0]
    spisok_uniq_folders = spisok_all[1]
    spisok_uniq_unknown = spisok_all[2]
    las_12_version_list = spisok_files_all[0]
    las_20_version_list = spisok_files_all[1]
    not_recognized_list = spisok_files_all[2]

    #�������� ����� ��� ������ 
    report = open(report_file, 'w')

    #������ � ���� ����������� ����� � �� ���� ��� EMPTY � ������ ���� ��������� ����� ���    
    report.write('FOLDERS:'+str(len(spisok_uniq_folders))+'\n')
    if len(spisok_uniq_folders) == 0 : report.write('--EMPTY--'+'\n')
    else :
        for x in xrange (0,len(spisok_uniq_folders)):
            report.write(spisok_uniq_folders[x].encode('cp', 'replace')+'\n')    
    #������ � ���� ����������� ������ � �� ���� ��� EMPTY � ������ ���� ������ ���   
    report.write('FILES:'+str(len(spisok_uniq_files))+'\n')
    if len(spisok_uniq_files) == 0 : report.write('--EMPTY--'+'\n')
    else :
        for x in xrange (0,len(spisok_uniq_files)):
            print spisok_uniq_files[x]
            report.write(spisok_uniq_files[x].encode('utf-8', 'replace')+'\n')
    #������ � ���� ����������� ��� ������ 1.2 � �� ���� ��� EMPTY � ������ ���� ������ ���
    report.write('Las_files 1.20:'+str(len(las_12_version_list))+'\n')
    if len(las_12_version_list) == 0 : report.write('--EMPTY--'+'\n')
    else :
        for x in xrange (0,len(las_12_version_list)):
            report.write(unicode(las_12_version_list[x]).encode('utf-8', 'replace')+'\n')
    #������ � ���� ����������� ��� ������ 2.0 � �� ���� ��� EMPTY � ������ ���� ������ ���       
    report.write('Las_files 2.00:'+str(len(las_20_version_list))+'\n')
    if len(las_20_version_list) == 0 : report.write('--EMPTY--'+'\n')
    else :
        for x in xrange (0,len(las_20_version_list)):
            report.write(las_20_version_list[x].encode('utf-8', 'replace')+"\n")
    #������ � ���� ����������� �������������� ������ � �� ���� ��� EMPTY � ������ ���� ������ ���       
    report.write('Not recognized files:'+str(len(not_recognized_list))+'\n')
    if len(not_recognized_list) == 0 : report.write('--EMPTY--'+'\n')
    else :
        for x in xrange (0,len(not_recognized_list)):
            report.write(not_recognized_list[x].encode('utf-8', 'replace')+'\n')  
    #������ � ���� ����������� �������������� �������� � �� ���� ��� EMPTY � ������ ���� �������� ���      
    report.write('UNKNOWN:'+str(len(spisok_uniq_unknown))+'\n')
    if len(spisok_uniq_unknown) == 0 : report.write('--EMPTY--'+'\n')
    else :
        for x in xrange (0,len(spisok_uniq_unknown)):
            report.write(spisok_uniq_unknown[x].encode('utf-8', 'replace'), '\n')
                  
    report.close


def spiski_fayla(folder_name, report_file):
    '������� ��� ������������ ������ razbor_files_in_folder'
    spisok_all = spiski(folder_name)
    spisok_files_all = create_las_file_lists(spisok_all)
    print_files_stat_in_file(report_file, spisok_all,spisok_files_all)
    return spisok_files_all


#DATA FOR TEST
report_file = 'C:/Python26/1/Results/good_riddance'
folder_name = 'C:/Python26/1/Work�'
spiski_fayla(folder_name, report_file)

    