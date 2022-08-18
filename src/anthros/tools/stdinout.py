from traceback import extract_tb
from tools import info
import sys, os, inspect

_print = print
_input = input
variables = dict()

class exception: #0.2
    def __init__(self, exc_info: 'tuple'):
        self.type = exc_info[0]
        self.desc = sys.exc_info()[1]
        self.poss = extract_tb(sys.exc_info()[2])

        self.name = exc_info[0].__name__
        self.text = str(sys.exc_info()[1])
        self.posl = []
        i = 0
        for line in self.poss:
            line = str(line).split()
            self.posl.append(dict())
            _i = 0
            while _i < len(line):
                if '/' in line[_i] or '\\' in line[_i]:
                    if line[_i][len(line[_i]) - 1] == ',': line[_i] = line[_i][:len(line[_i]) - 1]
                    self.posl[i]['path'] = line[_i]
                if 'line' in line[_i]:
                    self.posl[i]['line'] = line[_i + 1]
                _i += 1
            i += 1

    def __str__(self):
        return self.standard_out()

    def __call__(self):
        return self.standard_out()

    def __getitem__(self, item):
        return self.poss

    def standard_out(self):
        r'''Симулирует стандартного вида ошибку и возвращает её в виде строки
*На данный момент не реализовано, так как не удалось получить полную информацию из sys.extract_tb'''
        return self.custom_out()

    def custom_out(self):
        r'''Возвращает строку с упрощёным видом, которая содержит информацию об ошибке'''
        posl = self.posl
        i = 0
        out = 'exception in:\n'
        while i < len(posl):
            if 'path' not in posl[i].keys():
                out += f'system output: "{posl[i]["line"]}"\n'
            else:
                out += f'file "{posl[i]["path"]}", line {posl[i]["line"]}:\n'
            i += 1
        return out + f'{self.name}: {self.desc}'

    def short_out(self):
        r'''Возвращает краткую информацию об ошибке в виде строки'''
        posl = self.posl[len(self.posl) - 1]
        return f'exception in "{posl["path"]}", line {posl["line"]}:\n    {self.name}: {self.desc}'

    def description(self):
        r'''Возвращает описание текущей ошибки'''
        return self.desc

    def exception(self):
        r'''Возвращает тип ошибки'''
        return self.name

_exception = exception

def exception(exc_info: 'tuple'): #0.1
    r'''Принимает результат функции sys.exc_info(). Создаёт объект ошибки, не вызывая остановку выполения
    *Вы можете просто сделать print(exception) для вывода'''
    return _exception(exc_info)

def var(name: 'str', value = None, namespace: 'str' = '__pj__'): #0.1
    r''' метод, позволяющий сохранить переменные на время работы программы
    *если указанно имя, возвращает значение переменной
    *если указанно имя и новое значение, возвращает предыдущее значение и задёт новое'''
    global variables
    try: temp_namespace = variables[namespace]
    except:
        variables[namespace] = dict()
        temp_namespace = variables[namespace]

    previous = temp_namespace.setdefault(name)
    if value: temp_namespace[name] = value
    variables[namespace] = temp_namespace

    return previous

def clear(): #0.1
    r'''Очищает консоль от вывода'''
    if info.system_name() == 'win32': os.system('cls')
    else: os.system('clear')

def called_by():
    r'''Возвращает информацию о том, что вызвало текущий объект в виде словаря'''
    # 'clear', 'f_back', 'f_builtins', 'f_code', 'f_globals', 'f_lasti', 'f_lineno', 'f_locals', 'f_trace', 'f_trace_lines', 'f_trace_opcodes'
    # 'co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags', 'co_freevars', 'co_kwonlyargcount', 'co_lnotab', 'co_name', 'co_names', 'co_nlocals', 'co_posonlyargcount', 'co_stacksize', 'co_varnames', 'replace'
    frame = inspect.currentframe()
    f_code = frame.f_back.f_back.f_code
    out = dict(file = f_code.co_filename, name = f_code.co_name, attrs = f_code.co_names)
    return out