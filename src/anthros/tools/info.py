r'''Данный модуль отвечает за предоставление информации системы или python'''
from tools import simple, represent, stdinout
import inspect, copy, sys, datetime, http.client

#Переписать с getfullargspec, так как воспринимает непостоянные аргументы как постоянные
def args(obj: ('_def', '_class')): #0.1
    r'''Принимает объект и возвращает аргументы для вызова этого объекта функции или класса
    *При неккоректном использовании может возвращать пустую информацию
    *Игнорирует переменные с наименованием safe'''
    try:
        if type(obj).__name__ not in ['method', 'function']:
            if obj.__class__.__name__ == 'type': argspec = inspect.getfullargspec(obj.__init__)
            else: argspec = inspect.getfullargspec(obj.__call__)
        else: argspec = inspect.getfullargspec(obj)
    except:
        err = stdinout.exception(sys.exc_info())
        if err.exception() == 'AttributeError' and 'has no attribute \'__call__\'' in str(err.description()):
            return {'args': [], '*args': None, '**kwargs': None}

    arguments = copy.copy(argspec[0])
    defaults = copy.copy(argspec[3])
    arguments.reverse()
    if type(defaults).__name__ != 'tuple': defaults = tuple()

    temp = dict()
    for i in range(len(arguments) - 1):
        if i < len(defaults): temp[arguments[i]] = defaults[i]
        else: temp[arguments[i]] = None

    arguments.reverse()
    defaults = temp
    arguments += argspec[4]
    if type(argspec[5]).__name__ == 'dict': defaults.update(argspec[5])
    annotation = copy.copy(argspec[6])

    temp = list()
    for name in arguments:
        arg = dict(name = name)
        if annotation.get(name) != None: arg['ann'] = annotation[name]
        else: arg['ann'] = None
        if defaults.get(name) != None: arg['def'] = defaults[name]
        else: arg['def'] = None
        temp.append(arg)

    i = 0
    while i < len(temp):
        if temp[i]['name'] in ['self']: temp.pop(i)
        else: i += 1
    out = dict(args = temp)

    if argspec[1] != None:
        temp = dict(name = argspec[1])
        if annotation.get(argspec[1]) != None: temp['ann'] = annotation[argspec[1]]
        else: temp['ann'] = None
        if defaults.get(argspec[1]) != None: temp['def'] = defaults[argspec[1]]
        else: temp['def'] = None
        out['*args'] = temp
    else: out['*args'] = None

    if argspec[2] != None:
        temp = dict(name = argspec[2])
        if annotation.get(argspec[2]) != None: temp['ann'] = annotation[argspec[2]]
        else: temp['ann'] = None
        if defaults.get(argspec[2]) != None: temp['def'] = defaults[argspec[2]]
        else: temp['def'] = None
        out['**kwargs'] = temp
    else: out['**kwargs'] = None

    return out

def attrs(obj: '_class', sys: 'bool' = False, modul: 'bool' = False):
    r'''Возвращает доступные атрибуты для переданного объкта
*Непосоянный аргумент sys отвечает за вывод системных атрибутов
*Непостояный аргумент modul отвечает за вывод модулей, если объектом анализа является модуль'''
    out = dir(obj)
    i = 0
    while i < len(out):
        if '__' in out[i]:
            if not sys: out.pop(i)
            i -= 1
        i += 1

    i = 0
    while i < len(out):
        if simple.type(getattr(obj, out[i])) == 'module':
            if not modul: out.pop(i)
            i -= 1
        i += 1
    return out

def ac_path():
    r'''Показывает расположение АС'''
    sb = simple.slash_os()
    _path = __file__
    _path = _path.split(sb)
    _path = _path[:len(_path) - 2]
    _path = sb.join(_path)
    return _path

def project_path(): #Берёт просто текущее системное расположение
    r'''Достаёт информацию о расположении проекта из ac/data/manifest.ini'''
    #return represent.manifest(ac_path() + simple.path_os('/manifest.ini'))['environment']['project']
    out = sys.path[0]
    if out == '' or out == ac_path(): out = ac_path() + simple.slash_os() + 'project'
    return out

def time(timezone: ('boolean', 'int', 'float') = True):
    r'''Показывает текущее время в системе
    *При непостоянном аргументе timezone False покажет общее время на планете (UTC + 0)'''
    if timezone == True: time = datetime.datetime.now()
    else: time == datetime.datetime.now().astimezone().utcnow()
    return dict(hour = time.hour, minute = time.minute, second = time.second, microsecond = time.microsecond, day = time.day, month = time.month, year = time.year)

def system_name():
    r'''Возвращает имя текущей операционной системы
*На андроид по умолчанию считает что вы запустили AC в termux'''
    if hasattr(sys, 'getandroidapilevel'): return 'termux'
    return sys.platform

def get_ip():
    r'''Возвращает текущий ip адрес в сети'''
    conn = http.client.HTTPConnection("ifconfig.me")
    conn.request("GET", "/ip")
    return conn.getresponse().read().decode()

def test_2():
    return None

vars = locals()