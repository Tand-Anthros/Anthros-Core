from tools import simple, info, stdinout
import os, shutil, sys, pickle

def remove(path: 'str'):
    r'''Удаляет файл или папку по переданному раположению'''
    if simple.file_exist(path) == 'folder':
        return shutil.rmtree(path)
    elif simple.file_exist(path) == 'file':
        return shutil.os.remove(path)
    else:
        raise Exception('file or folder not exist')

def make_folders(link: 'str'):
    r'''Создаёт папку и все промежуточные папки до неё'''
    os.makedirs(link)

def open_stream(link: 'str', mode = 'r'):
    try:
        if info.system_name() == 'win32': save_pos = simple.pos_switch(sys.path[0].split(simple.slash_os())[0])
        file = open(link, mode, encoding='utf-8')
        if info.system_name() == 'win32': simple.pos_switch(save_pos)
    except:
        simple.pos_switch(info.project_path())
        file = open(link, mode, encoding='utf-8')
        simple.pos_switch(save_pos)
    return file

def open_file(link: 'str', stream: bool = False):
    r'''Возвращает данные из файла в виде строки
    *При stream = True вернёт io.stream объект'''
    pos = link.split(simple.slash_os())
    save_pos = simple.pos_switch(simple.slash_os().join(pos[:len(pos) - 1]))
    file = open_stream(link)
    if stream: return file
    file = file.read()
    if len(file) > 0 and file[0] == '\ufeff':
        file = file[1:]
    simple.pos_switch(**save_pos)
    return file

def save_file(link: 'str', fill: 'str', rewrite: bool = False):
    r'''Записывает файл по указанному пути с переданными данными
    *Если переменная rewrite = True перезапишет существующий файл'''
    if rewrite: mode = 'w'
    else: mode = 'x'

    pos = link.split(simple.slash_os())
    temp_pos = simple.slash_os().join(pos[:len(pos) - 1])
    if simple.file_exist(temp_pos) != 'folder': make_folders(temp_pos)
    save_pos = simple.pos_switch(temp_pos)
    def _save_file(link, mode):
        file = open_stream(link, mode = mode)
        file.write(fill)
        file.close()

    try:
        _save_file(link, mode)
    except:
        exc = stdinout.exception(sys.exc_info())
        if exc.exception() == 'FileNotFoundError':
            _link = link.split(simple.slash_os())
            make_folders(simple.slash_os().join(_link[:len(_link) - 1]))
            _save_file(link, mode)
            return None
        raise
    simple.pos_switch(**save_pos)

pickling_args = (str, 'link')
def pickling(link: pickling_args, fill):
    pickle.dump(fill, open(link, 'bw'))

unpickling_args = (str, 'link')
def unpickling(link: unpickling_args):
    try:
        file = pickle.load(open(link, 'br'))
    except:
        pickle.dump(None, open(link, 'bw'))
        file = pickle.load(open(link, 'br'))
    return file

def open_with(var, choice = False):
    r'''Открывает файл с приложением в системе по умолчанию
*Непостоянный аргумент choice позволяет активировать режим выбора приложения
*Если вы передаёте объект, то он будет сохранён как временый файл
 Убедитесь, что ваш объект может быть представлен как строка или имет для этого метод __file__()'''
    if simple.type(var) != 'str':
        path = simple.slash_os().join([info.project_path(), 'ac_temp.' + simple.type(var)])
        try: save_file(path, getattr(var, '__file__'))
        except: save_file(path, str(var))
        var = path
    print('manager:', type(var))

    if info.system_name() == 'termux':
        os.system('termux-open ' + var)
    else:
        print('manager:', var)
        os.system(var)

def fold_dict(path: 'str'): #Удалить из represent
    r'''Получить словарь, который содержит всю информацию о папке, файлы, вложенные папки и ссылки на них
    *Ссылка на папку, будет хранится в ключе "/"'''
    path = simple.path_os(path)
    out = dict()
    out['/'] = path
    for elem in os.listdir(path):
        if os.path.isdir(path + simple.path_os('/') + elem):
            out[elem] = fold_dict(path + simple.path_os('/') + elem)
        else:
            out[elem] = path + simple.path_os('/') + elem
    return out