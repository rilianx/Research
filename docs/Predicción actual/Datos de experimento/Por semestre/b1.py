#@title **Main**
from urllib.request import urlopen
import json
import numpy as np
import pandas as pd
import os
import copy
import math
import statistics
import sklearn.metrics as metrics
 
# Evitar truncar data mostrada al usar jupyter notebook
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
 
# Constante que aloja el diccionario JSON con toda la data
DATA = None

# Obtener data JSON
if os.path.exists('./out/dataout.json'):
    DATA = json.load(open('./out/dataout.json', 'r'))
else:
    data_url = urlopen('http://nutriexcel.cl/UMDU/dataout_v2.json')
    DATA = json.loads(data_url.read())
 
# Labels base de las columnas
LABELS_BASE = {
    # Parámetros del alumno (Target)
    'p1':                            ['p1'],
    'p2':                            ['p2'],
    'np':                            ['np'],
    'p1p2':                          ['p1p2'], # Promedio p1p2 y p2p2
    'p2p2':                          ['p2p2'],
    
    # Parámetros del laboratorio (Features)
    'grade':                         ['g_lab#'],
    'attempts':                      ['a_lab#'],
    'usedtime':                      ['ut_lab#'],
    'activetime':                    ['act_lab#'],
    'disconnections':                ['dis_lab#'],      # log
    'compilationtime':               ['ct_lab#'],
    'runtimedebuggingtime':          ['rt_lab#'],
    'compilationtimeratio':          ['ctr_lab#'],
    'runtimedebuggingtimeratio':     ['rtr_lab#'],
    'errorsreductionratio':          ['err_lab#'],
    'compilationerrorsratio':        ['cer_lab#'],
    'activequartiles':               ['actq1_lab#','actq2_lab#','actq3_lab#'],
    'questionsdifficulty':           ['qd$_lab#'],
    'questionsgrades':               ['qg$_lab#'],      # Promedio
    'questionsattempts':             ['qat$_lab#'],     # Sumar - Max   # log
    'questionsactivetime':           ['qact$_lab#'],    # Promedio
    'questionsavgtime':              ['qavt$_lab#'],    # Promedio
    'questionsmaxerrors':            ['qme$_lab#'],     # Max
    'questionsmaxconsecutiveerrors': ['qmce$_lab#'],    # Max
    'questionsmaxsimilarityratio':   ['qmsr$_lab#'],    # Promedio
    'questionscorrectness':          ['qc$_lab#']       # Promedio
}
 
 
# Cantidad de preguntas por lab
LABS_LENGTHS = {
    '1': 7,
    '2': 6,
    '3': 6,
    '4': 5,
    '5': 3
}
 
def get_labels(labs:list, obj_param:list, params:list):
    '''Retorna una lista con los nombres de las columnas correspondientes.'''
    labels = []
    
    if not obj_param == None:
        for obj_p in obj_param:
            labels.extend(LABELS_BASE[obj_p])
 
    for lab in labs:
        for param in params:
            label_base = LABELS_BASE[param]
            for lb in label_base:
                aux_label = lb.replace('#', str(lab))
                if '$' in aux_label:
                    for i in range(LABS_LENGTHS[str(lab)]):
                        labels.extend([aux_label.replace('$', str(i + 1))])
                else:
                    labels.extend([aux_label])
    return labels
                    
 
def load_data(filepath = './out/dataout.json'):
    '''Retorna un diccionario importado desde un archivo JSON.'''
    return readJSON(filepath)
 
 
def convert_to_dataframe(arr:list, labels:list=None, ids_idx:list=None):
    '''Retorna un Pandas Dataframe.'''
    return pd.DataFrame(np.array(arr), columns=labels, index=ids_idx)
 
 
def get_custom_dataframe(data:dict, labs:list, obj_param:list, params:list, labels:bool=False, index:str=None):
    '''Retorna un DataFrame de Pandas con etiquetas.'''
    if params == 'all':
        params = list(LABELS_BASE.keys())[5:]
        
    data, ids_idx,cursoData = get_custom_data(labs, obj_param, params, data, index)
    if labels:
        return convert_to_dataframe(data, labels=get_labels(labs, obj_param, params), ids_idx=ids_idx) , cursoData
    else:
        return convert_to_dataframe(data, labels=None, ids_idx=ids_idx)
 
 
 
 
def get_custom_data(labs:list, obj_param:list, params:list, data:dict, index:str):
    dataout = []
    idxs = []
    curso = []
    contador = 0
    
    for id in data['courses']:
        curso.append(id)    
        
    cursoData = []
    for v1 in data['courses'].values():
        print(curso[contador])
        for k2,v2 in v1['students'].items():
            if index == 'id':
                idxs.append(k2)
            elif not index == None:
                idxs.append(v2[index])
            
            studentdata = []
            
            if not obj_param == None:
                for obj_p in obj_param:
                    studentdata.extend([v2[obj_p]])
            
            for labnumber in labs:
                labkey = str(list(v2['labs'].keys())[int(labnumber) - 1])
                
                for param in params:
                    val = v2['labs'][labkey][param]
                    if isinstance(val, list):
                        studentdata.extend(val)
                    else:
                        studentdata.extend([val])
            
            dataout.append(studentdata)
            cursoData.append(curso[contador])
        contador = contador + 1
    if len(idxs) == 0:
        idxs = None
 
    return dataout, idxs, cursoData

 
def readJSON(filename:str):
    print('Leyendo archivo: \'' + filename + '\'')
    return json.load(open(filename, 'r'))
 
# --------------------------------------------------------------------------
 
def norm_log(df):
    min_value = min(df)
    for i in range(len(df)):
        df[i] = math.log(df[i] - min_value + 1)
 
    return df
 
# --------------------------------------------------------------------------
 
def apply(df:pd.core.frame.DataFrame, columns, func, c=None, replace:bool=True):
    '''
    Aplica una función dada a una serie de parámetros dados.
    df: Dataframe.
    func: Función a aplicar (Ej.: 'sum', 'max', 'math.log', etc.).
    params: Parámetro o lista de parámetros al cual/a los cuales aplicar la función. Si el parámetro param tiene un signo '?' al final, 
            se considerarán todos aquellos que empiecen con param. Si es una lista de parámetros, cada parámetro debe ser el nombre exacto,
            es decir, no deben llevar '?'.
    c: constante o parámetro a utilizar en el cálculo (Ej: sumar constante c; log base c). Se debe omitir si no aplica.
    replace: Si es True, reemplaza la columna o columnas a las cuales se la aplica la función. Si es False, se agregan nuevas columnas.
    '''
 
    def one_param(df_new:pd.core.frame.DataFrame):
        if not columns[-1] == '?':
            try:
                aux_column = function_handler(func, df_new[columns], c)
            except KeyError:
                raise Exception('Columna ' + columns + ' no existe.')
 
            aux_column = pd.DataFrame(aux_column)
            insert_columns(df_new, aux_column, [columns], replace, func.__name__, c)
            
            return df_new
        else:
            labels = list(df_new.columns) + ['???']
            target_cols = []
            target_cols_names = []
            fg_newarr = True
            fg_endarr = False
            i = 0
 
            while i < len(labels):
                if labels[i][0] == columns[0] and columns[:-1] in labels[i]:
                    target_cols.append(i)
                    target_cols_names.append(labels[i])
                    fg_newarr = False
                elif not fg_newarr:
                    fg_endarr = True
                
                if not fg_newarr and fg_endarr:
                    fg_newarr = True
                    fg_endarr = False
                    aux_columns = []
                    
                    for row in df_new.values:
                        aux_row = [row[col] for col in target_cols]
                        aux_columns.append(function_handler(func, aux_row, c))
 
                    aux_columns = pd.DataFrame(aux_columns)
                    insert_columns(df_new, aux_columns, target_cols_names, replace, func.__name__, c)
 
                    if replace:
                        i -= len(target_cols)
                        labels = list(df_new.columns) + ['???']
 
                    target_cols = []
                    target_cols_names = []
                i += 1
            
            return df_new
 
 
    def multi_param(df_new:pd.core.frame.DataFrame):
        aux_columns = []
        target_cols = [df_new.columns.get_loc(col) for col in columns]
 
        for row in df_new.values:
            try:
                aux_row = [row[col] for col in range(len(target_cols))]
            except KeyError:
                raise Exception('Columna ' + columns + ' no existe.')
            
            aux_columns.append(function_handler(func, aux_row, c))
 
        aux_columns = pd.DataFrame(aux_columns)
        insert_columns(df_new, aux_columns, columns, replace, func.__name__, c)
 
        return df_new
 
    
    def function_handler(func, col, c=None):
        arr = copy.deepcopy(col)
        try:
            if c == None:
                return func(arr)
            else:
                return func(arr, c)
        except TypeError:
            try:
                return [function_handler(func, datum, c) for datum in arr]
            except TypeError:
                raise Exception('Operación sin sentido: x = ' + func.__name__ + '(x).')
    
 
    def insert_columns(df_new, sub_df, labels, replace, func_name, c):
        const_name = ''
 
        if not c == None:
                const_name = ',' + str(c)
 
        if len(sub_df.columns) == 1:
            merg_name = labels[0]
            
            if len(labels) > 1:
                merg_name = get_merged_name(labels[0])
 
            new_name = func_name + '(' + merg_name + const_name + ')'
 
            if replace:
                df_new[labels[0]] = sub_df
                df_new.rename(columns={labels[0]: new_name}, inplace=True)
 
                if len(labels) > 1:
                    for i in range(1, len(labels)):
                        df_new.pop(labels[i])
            else:
                df_new[new_name] = sub_df
        else:
            new_names = [func_name + '(' + cur_name + const_name + ')' for cur_name in labels]
 
            if replace:
                for i in range(len(labels)):
                    df_new[labels[i]] = sub_df[i]
                    df_new.rename(columns={labels[i]: new_names[i]}, inplace=True)
            else:
                for i in range(len(labels)):
                    df_new[new_names[i]] = sub_df[i]
 
 
    def get_merged_name(basename:str):
        merged_name = ''
        flag = True
        for i in range(len(basename)):
            if flag and basename[i].isnumeric():
                merged_name += '$'
                flag = False
            else:
                merged_name += basename[i]
 
        return merged_name
 
 
    def are_valid_column_names(columns):
        if type(columns) == list:
            for col in columns:
                if '?' in col:
                    raise Exception('Nombres de columna en lista no deben contener \'?\'.')
        
        return True
 
 
    df_new = copy.deepcopy(df)
    are_valid_column_names(columns)
    if type(columns) == list:
        return multi_param(df_new)
    else:
        return one_param(df_new)
 
 
def remove_col(df, column:str):
    if column[-1] == '?':
        for x in df.columns:
            if x[0] == column[0] and column[:-1] in x:
                df.pop(x)
    else:
        df.pop(column)
 
 
def normalise_row(df):
    df_aux = copy.deepcopy(df)
 
    for i in range(len(df_aux)):
        min_value = min(df_aux.iloc[i])
        max_value = max(df_aux.iloc[i])
 
        df_aux.iloc[i] = (df_aux.iloc[i] - min_value) / (max_value - min_value)
 
    return df_aux
 
 
def normalise_col(df, norm_params=None):
    norm_params_aux = {}
    df_aux = copy.deepcopy(df)
 
    if norm_params == None:
        for col in df_aux.columns:
            min_value = min(df_aux[col])
            max_value = max(df_aux[col])
            
            norm_params_aux[col] = {
                'min_value': min_value,
                'max_value': max_value
            }
 
            for i in range(len(df_aux[col])):
                if not max_value - min_value == 0:
                    df_aux[col].iloc[i] = (df_aux[col].iloc[i] - min_value) / (max_value - min_value)
                else:
                    df_aux[col].iloc[i] = 0
 
        return df_aux, norm_params_aux
    else:
        for col in df_aux.columns:
            for i in range(len(df_aux[col])):
                if not norm_params[col]['max_value'] - norm_params[col]['min_value'] == 0:
                    df_aux[col].iloc[i] = (df_aux[col].iloc[i] - norm_params[col]['min_value']) / (norm_params[col]['max_value'] - norm_params[col]['min_value'])
                else:
                    df_aux[col].iloc[i] = 0
        return df_aux
 
 
def normalise_log(df):
    df_aux = copy.deepcopy(df)
 
    for i in range(len(df_aux)):
        for j in range(len(df_aux.iloc[i])):
            df_aux.iloc[i][j] = math.log(df_aux.iloc[i][j]) if df_aux.iloc[i][j] > 0 else 0
 
    return df_aux