# -*- coding: cp1251 -*-
import os, sys
from stat import *
from string import *
from operator import truth

def read_file(las_file):
    'Чтение файла и получение списка с строками из файла'
    # read file and return list of strings
    file_to_procces = open(las_file, 'rb')
    strings_in_file = file_to_procces.readlines()
    file_to_procces.close
    return strings_in_file 
    
def search_first_data_block_string(prefix, strings_in_file):
    'Поиск строки начала сектора данных'
    #Получение начальной позиции сектора
    position = 'Novalue'    
    for x in xrange(0, len(strings_in_file)):
        if strings_in_file[x].startswith(prefix) == 1 :
            position = x
            break
    return position

def single_block(position, strings_in_file):
    'Сборка сектора данных данных'
    #Получение сектора без строк коментариев и строк начина.щихся на ~
    data_block = []
    if (position)!='Novalue':
        for x in xrange(position+1, len(strings_in_file)) :
            if strings_in_file[x].startswith("~") == 0:
                if strings_in_file[x].startswith("#") == 0:
                    data_block.append(strip(strings_in_file[x]))
            else:
                break
    return data_block

def combine_data_bloks(las_file):
    'Создание массивов секторов данных'
    #Задание префиксов сеторов в список
    prefix_datablock_list=['~V', '~W', '~C', '~P', '~O', '~A', '~B']
    strings_in_file  = read_file(las_file)
    data_blocks = []
    #Цикл получения секторов данных
    for x in xrange(0, len(prefix_datablock_list)):
        position = search_first_data_block_string(prefix_datablock_list[x], strings_in_file)
        data_block = single_block(position, strings_in_file)
        data_blocks.append(data_block)
    return data_blocks

def version_search(version_information_block):
    'получение версии и развертки фала'
    for v in xrange (0, len(version_information_block)):
        if (version_information_block[v].startswith('VERS') == 1) or (version_information_block[v].startswith('Vers') == 1) :
            version_line = version_information_block[v]
        if version_information_block[v].startswith('WRAP') == 1 :
            wrap_line = version_information_block[v]
    version = poluchenie_dannih_las_20(version_line)
    wrap = poluchenie_dannih_las_20(wrap_line)
    return version, wrap

def line_defination(information_block, prefix):
        'получение строки из сектора данных с указанным префиксом'
        line = 'novalue'
        for y in xrange(0,len(information_block)):
            if information_block[y].startswith(prefix) == 1:
                line = information_block[y]
                return line

def poluchenie_dannih_las_20(line):
    'получение данных из ласа 2.0'
    length_line=len(line)
    mesto_pervoi_tochki=line.find('.')
    stroka_bez_nazvaniya=line[mesto_pervoi_tochki+1:length_line]
    mesto_probela=stroka_bez_nazvaniya.find(' ')
    mesto_dvoetochiya=stroka_bez_nazvaniya.find(':')
    data = strip(stroka_bez_nazvaniya[mesto_probela:mesto_dvoetochiya])      
    return  data

def poluchenie_dannih_las_12(line):
    'получение данных из ласа 1.2'
    lenght_line = len(line)
    mesto_dvoetochiya = line.find(':')
    data = strip(line[mesto_dvoetochiya+1:lenght_line])
    return data

def spisok_metodov(curve_information_block):
    'Получение списка методов ГИС'
    spisok_imen_krivih = []
    for s in xrange(0, len(curve_information_block)):
        imya_krivoy = curve_information_block[s][0:curve_information_block[s].find(".")]
        spisok_imen_krivih.append(strip(imya_krivoy))   
    return spisok_imen_krivih

def spisok_opisaniy(curve_information_block):
    'Получение списка описаний методов ГИС'
    spisok_opisaniy_krivih = []
    for t in xrange(0, len(curve_information_block)):
        opisanie_krivoy = curve_information_block[t][curve_information_block[t].find(":")+1:len(curve_information_block[t])]
        spisok_opisaniy_krivih.append(strip(opisanie_krivoy))       
    return spisok_opisaniy_krivih

def edinici_izmereniya(curve_information_block):
    'Получение списка единиц измерений методов ГИС'
    spisok_ed_izm = []
    for t in xrange(0, len(curve_information_block)):
        edin_izmer = '-'
        lenght = len(curve_information_block[t])
        mesto_pervoy_tochki = curve_information_block[t].find('.')
        line_ot_tochki = curve_information_block[t][mesto_pervoy_tochki:lenght]
        mesto_probela_posle_tochki = line_ot_tochki.find(' ')
        edin_izmer = strip(line_ot_tochki[1:line_ot_tochki.find(' ')])
        spisok_ed_izm.append(strip(edin_izmer))       
    return spisok_ed_izm

def print_las(spisok_metodov_gis, massiv_metodov,las_print_file):
    'Печать ласа в виде таблицы'
    d = open(las_print_file, 'a')
    for v in xrange(0, len(spisok_metodov_gis)):      
        d.write(spisok_metodov_gis[v]+';')
    d.write("\n")    
    for f in xrange (0 ,kolvo_otschetov):        
        for v in xrange(0, len(spisok_metodov_gis)):                                
            d.write(massiv_metodov[f][v]+";")
        d.write("\n")
    d.close
    
def find_null(well_information_block):
    "Поиск кода пустого значения"
    null = '-'
    for v in xrange (0, len(well_information_block)):
            if well_information_block[v].startswith('NULL') == 1 :
                null_line = well_information_block[v]
                null = poluchenie_dannih_las_20(null_line)
    return null

def find_start(well_information_block):
    'Поиск кровли интервала представленного в лас'
    start = '-'
    for v in xrange (0, len(well_information_block)):
        if well_information_block[v].startswith('STRT') == 1 :
            start_line = well_information_block[v]
            start = poluchenie_dannih_las_20(start_line)
    return start

def find_stop(well_information_block):
    'Поиск подошвы интервала представленного в лас'
    stop = '-'
    for v in xrange (0, len(well_information_block)):
         if well_information_block[v].startswith('STOP') == 1 :
              stop_line = well_information_block[v]
              stop = poluchenie_dannih_las_20(stop_line)
    return stop

def find_date(well_information_block, version):
    'Поиск даты каротажа'
    date = '-'
    for v in xrange (0, len(well_information_block)):
        if ((version == '2.00') or (version == '2.0')or (version == '2')):
            if well_information_block[v].startswith('DATE') == 1 :
                date_line = well_information_block[v]
                date = poluchenie_dannih_las_20(date_line)
        if ((version == '1.20') or (version == '1.2')):
            if well_information_block[v].startswith('DATE') == 1 :
                date_line = well_information_block[v]
                date = poluchenie_dannih_las_12(date_line)
    return date

def find_well(well_information_block, version):
    "Поиск названия скважины"
    well = '-'
    for v in xrange (0, len(well_information_block)):
        if ((version == '2.00') or (version == '2.0')or (version == '2')):
            if well_information_block[v].startswith('WELL') == 1 :
                well_line = well_information_block[v]
                well = poluchenie_dannih_las_20(well_line)
        if ((version == '1.20') or (version == '1.2')):
            if well_information_block[v].startswith('WELL') == 1 :
                well_line = well_information_block[v]
                well = poluchenie_dannih_las_12(well_line)
    return well

def find_step(well_information_block):
    'поиск шага квантования'
    step = '-'
    for v in xrange (0, len(well_information_block)):
        if well_information_block[v].startswith("STEP") == 1 :
            step_line = well_information_block[v]
            step = poluchenie_dannih_las_20(step_line)
    return step 
        
def find_uwi(well_information_block, version):
    'поиск UWI'
    uwi = '-'
    for v in xrange (0, len(well_information_block)):
        if ((version == '2.00') or (version == '2.0')or (version == '2')):
            if well_information_block[v].startswith('UWI') == 1 :
                uwi_line = well_information_block[v]
                uwi = poluchenie_dannih_las_20(uwi_line)
        if ((version == '1.20') or (version == '1.2')):
            if well_information_block[v].startswith('UWI') == 1 :
                uwi_line = well_information_block[v]
                uwi = poluchenie_dannih_las_12(uwi_line)
    return uwi


def logs_stat_obtain(version, data_information_block, curve_information_block, null_parametr):
        'Получение статистических данных по ласам для каждой скважины'
        nakoplenie_do_kol_metodov = []
        massiv_metodov = []
        summ_massiv = []
        count_massive = []
        count_missing_massiv = []
        min_massiv = []
        max_massiv = []
        averege_massiv = []
        
        summ = 0
        count = 0
        min = 99999999
        max = -99999999
        count_missing = 0
        
        for l in xrange (0, len(data_information_block)):
            list_one_line = split(data_information_block[l])
            nakoplenie_do_kol_metodov=nakoplenie_do_kol_metodov+list_one_line
            if len(nakoplenie_do_kol_metodov) == len(spisok_metodov(curve_information_block)):
                massiv_metodov.append(nakoplenie_do_kol_metodov)
                nakoplenie_do_kol_metodov =[]
        kolvo_otschetov =len(massiv_metodov)-1
   
        for v in xrange(0, len(spisok_metodov(curve_information_block))):
            for f in xrange (0 ,kolvo_otschetov):
                data_unit  = massiv_metodov[f][v]
                if (data_unit == '1.#INF') or (data_unit == '-1.#INF') or (data_unit == '-1.#IND') or (data_unit == '1.#IND'):
                    data_unit = null_parametr
                                  
                if float(data_unit) != float(null_parametr):
                    summ = float(data_unit)+summ
                    count = count+1
                    averege = summ/count
                    if float(data_unit)< min:
                        min = float(data_unit)
                    if float(data_unit)> max:
                        max = float(data_unit)
                if float(data_unit) == float(null_parametr):
                    count_missing = count_missing+1
                    
            averege_massiv.append(averege)                 
            summ_massiv.append(summ)
            count_massive.append(count)
            count_missing_massiv.append(count_missing)
            min_massiv.append(min)
            max_massiv.append(max)
              
            summ = 0
            count = 0
            averege = 0
            min = 99999999
            max = -99999999
            count_missing = 0

        return summ_massiv, count_massive, count_missing_massiv, min_massiv, max_massiv, averege_massiv

def help_data_block():
    opisanie_data_block = {0: 'version_information_block', 1: 'well_information_block', 2: 'curve_information_block', 3: 'parametr_information_block', 4: 'optional_information_block', 5: 'data_information_block', 6: 'B_information_block'}

def massive_statistiki(las_file):
    'формирование конечного массива статистики по одному лас для записи в файл'
    data_blocks = combine_data_bloks(las_file)
    null_parametr = find_null(data_blocks[1])
    version, wrap = version_search(data_blocks[0])
    well = find_well(data_blocks[1], version)
    start = find_start(data_blocks[1])
    stop = find_stop(data_blocks[1])
    date = find_date(data_blocks[1], version)
    uwi = find_uwi(data_blocks[1], version)
    step = find_step(data_blocks[1])
    summ_massiv, count_massive, count_missing_massiv, min_massiv, max_massiv, averege_massive = logs_stat_obtain(version, data_blocks[5], data_blocks[2], null_parametr)   
    spisok_metodov_gis = spisok_metodov(data_blocks[2])
    spisok_opisaniy_gis = spisok_opisaniy(data_blocks[2])
    spisok_ed_izm = edinici_izmereniya(data_blocks[2])  
    
    
    vihidnoy_massiv_param_name = []
    vihodnoy_massiv_param = []
    vihidnoy_massiv_stat_name = []
    vihodnoy_massiv_stat = []
    vihodnoy_massiv_one = []

    vihidnoy_massiv_param_name.append('Path')
    vihodnoy_massiv_param.append(las_file)
    vihidnoy_massiv_param_name.append('Version')
    vihodnoy_massiv_param.append(version)
    vihidnoy_massiv_param_name.append('Well')
    vihodnoy_massiv_param.append(well)
    vihidnoy_massiv_param_name.append('UWI')
    vihodnoy_massiv_param.append(uwi)
    vihidnoy_massiv_param_name.append('Start')
    vihodnoy_massiv_param.append(start)
    vihidnoy_massiv_param_name.append('Stop')
    vihodnoy_massiv_param.append(stop)
    vihidnoy_massiv_param_name.append('Step')
    vihodnoy_massiv_param.append(step)
    vihidnoy_massiv_param_name.append('Date')
    vihodnoy_massiv_param.append(date)
    vihidnoy_massiv_param_name.append('Null')
    vihodnoy_massiv_param.append(null_parametr)       
    vihidnoy_massiv_stat_name.append('Metodi')
    vihodnoy_massiv_stat.append(spisok_metodov_gis)
    vihidnoy_massiv_stat_name.append('Opisaniya')
    vihodnoy_massiv_stat.append(spisok_opisaniy_gis)
    vihidnoy_massiv_stat_name.append('Units')
    vihodnoy_massiv_stat.append(spisok_ed_izm)
    vihidnoy_massiv_stat_name.append('Summ')
    vihodnoy_massiv_stat.append(summ_massiv)        
    vihidnoy_massiv_stat_name.append('Count')
    vihodnoy_massiv_stat.append(count_massive)  
    vihidnoy_massiv_stat_name.append('Count_missing')
    vihodnoy_massiv_stat.append(count_missing_massiv)  
    vihidnoy_massiv_stat_name.append('Min')
    vihodnoy_massiv_stat.append(min_massiv)
    vihidnoy_massiv_stat_name.append('Max')
    vihodnoy_massiv_stat.append(max_massiv)
    vihidnoy_massiv_stat_name.append('AVG')
    vihodnoy_massiv_stat.append(averege_massive)

    vihodnoy_massiv_one.append(vihidnoy_massiv_param_name)
    vihodnoy_massiv_one.append(vihodnoy_massiv_param)
    vihodnoy_massiv_one.append(vihidnoy_massiv_stat_name)
    vihodnoy_massiv_one.append(vihodnoy_massiv_stat)
        
    return vihodnoy_massiv_one


#DATA FOR TEST
#las_file = u'c:/Python26/1/Work/01_wire.las'
